# Kubernetes Installation Guide

Complete guide for deploying the AI Coding Assistant on Kubernetes (local and production).

---

## Table of Contents
1. [Local Kubernetes (Docker Desktop)](#local-kubernetes)
2. [Production Kubernetes (Nutonics GPU Cluster)](#production-kubernetes)
3. [GPU Support Setup](#gpu-support)
4. [Monitoring Setup](#monitoring)

---

## Local Kubernetes (Docker Desktop)

### Prerequisites
- Docker Desktop with Kubernetes enabled
- kubectl installed and configured
- 32GB RAM minimum
- 200GB free storage

### Step 1: Enable Kubernetes in Docker Desktop

1. Open Docker Desktop
2. Settings → Kubernetes
3. ✅ Enable Kubernetes
4. Apply & Restart

Verify:
```bash
kubectl cluster-info
kubectl get nodes
```

### Step 2: Create Namespace

```bash
kubectl apply -f k8s/base/namespace.yaml
```

### Step 3: Deploy Storage Layer

```bash
# PostgreSQL
kubectl apply -f k8s/base/postgres.yaml

# Redis
kubectl apply -f k8s/base/redis.yaml

# Qdrant Vector DB
kubectl apply -f k8s/base/qdrant.yaml

# Verify deployments
kubectl get pods -n ai-assistant
kubectl get pvc -n ai-assistant
```

Wait for all pods to be `Running`:
```bash
kubectl wait --for=condition=ready pod -l app=postgres -n ai-assistant --timeout=300s
kubectl wait --for=condition=ready pod -l app=redis -n ai-assistant --timeout=300s
kubectl wait --for=condition=ready pod -l app=qdrant -n ai-assistant --timeout=300s
```

### Step 4: Deploy LLM Layer

```bash
# Ollama for local deployment
kubectl apply -f k8s/base/ollama.yaml

# Wait for Ollama to be ready
kubectl wait --for=condition=ready pod -l app=ollama -n ai-assistant --timeout=600s

# Download models
kubectl exec -n ai-assistant deployment/ollama -- ollama pull mistral:7b-instruct
kubectl exec -n ai-assistant deployment/ollama -- ollama pull codellama:34b-instruct
```

### Step 5: Build and Load Docker Images

Since we're using local images, build and load them into Docker Desktop:

```bash
# Build images
docker build -t ai-assistant-backend:latest ./services/backend
docker build -t ai-assistant-frontend:latest ./services/frontend
docker build -t ai-assistant-embedding:latest ./services/embedding
docker build -t ai-assistant-code-agent:latest ./services/code-agent

# Verify images
docker images | grep ai-assistant
```

### Step 6: Deploy Application Layer

```bash
# Backend API
kubectl apply -f k8s/base/backend.yaml

# Frontend
kubectl apply -f k8s/base/frontend.yaml

# Verify deployments
kubectl get deployments -n ai-assistant
kubectl get pods -n ai-assistant
```

### Step 7: Install Ingress Controller

```bash
# Install NGINX Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.0/deploy/static/provider/cloud/deploy.yaml

# Wait for ingress controller
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=300s

# Deploy ingress
kubectl apply -f k8s/base/ingress.yaml
```

### Step 8: Access the Application

```bash
# Get ingress info
kubectl get ingress -n ai-assistant

# Add to /etc/hosts (Windows: C:\Windows\System32\drivers\etc\hosts)
# Add this line:
# 127.0.0.1 localhost
```

Access:
- **Frontend**: http://localhost
- **Backend API**: http://localhost/api/docs

### Step 9: Verify Installation

```bash
# Check all resources
kubectl get all -n ai-assistant

# Check logs
kubectl logs -n ai-assistant -l app=backend --tail=50
kubectl logs -n ai-assistant -l app=frontend --tail=50

# Test backend
kubectl port-forward -n ai-assistant svc/backend 8000:8000
# In another terminal:
curl http://localhost:8000/health
```

---

## Production Kubernetes (Nutonics GPU Cluster)

### Prerequisites
- Kubernetes cluster (1.28+)
- 3-6 GPU nodes (NVIDIA A100/H100)
- kubectl configured for cluster access
- Helm 3.x installed
- NVIDIA GPU Operator installed

### Architecture Overview

```
Production Cluster:
├── Control Plane (3 nodes)
├── GPU Nodes (3-6 nodes with A100/H100)
├── CPU Worker Nodes (5+ nodes for services)
└── Storage Nodes (3 nodes - Ceph/NFS)
```

### Step 1: Set Up Cluster Access

```bash
# Copy kubeconfig from cluster
scp admin@nutonics-master:/etc/kubernetes/admin.conf ~/.kube/config

# Verify access
kubectl get nodes
kubectl get nodes -l nvidia.com/gpu=true  # Check GPU nodes
```

### Step 2: Install NVIDIA GPU Operator

```bash
# Add NVIDIA Helm repo
helm repo add nvidia https://nvidia.github.io/gpu-operator
helm repo update

# Install GPU Operator
helm install --wait --generate-name \
  -n gpu-operator --create-namespace \
  nvidia/gpu-operator \
  --set driver.enabled=true

# Verify GPU support
kubectl get nodes -o json | jq '.items[].status.capacity | select(."nvidia.com/gpu" != null)'
```

### Step 3: Create Namespace and Storage Classes

```bash
# Create namespace
kubectl apply -f k8s/base/namespace.yaml

# Create storage class for fast NVMe (adjust based on your storage solution)
cat <<EOF | kubectl apply -f -
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: kubernetes.io/no-provisioner  # Or your CSI driver
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
EOF
```

### Step 4: Deploy Storage Layer (HA Configuration)

```bash
# PostgreSQL HA (3 replicas)
kubectl apply -f k8s/production/postgres-ha.yaml

# Redis Cluster (6 nodes: 3 master + 3 replica)
kubectl apply -f k8s/production/redis-cluster.yaml

# Qdrant Cluster (3 nodes)
kubectl apply -f k8s/production/qdrant-cluster.yaml

# Verify storage
kubectl get statefulsets -n ai-assistant
kubectl get pvc -n ai-assistant
```

### Step 5: Deploy vLLM with GPU Support

```bash
# Deploy vLLM inference servers
kubectl apply -f k8s/production/vllm-gpu.yaml

# Monitor GPU utilization
kubectl exec -n ai-assistant deployment/vllm-inference -- nvidia-smi

# Check vLLM logs
kubectl logs -n ai-assistant -l app=vllm -f
```

**Expected startup time**: 5-10 minutes (model download + loading)

### Step 6: Build and Push Images to Registry

```bash
# Set your registry
REGISTRY="your-registry.com"

# Build and push
docker build -t $REGISTRY/ai-assistant-backend:v1.0 ./services/backend
docker push $REGISTRY/ai-assistant-backend:v1.0

docker build -t $REGISTRY/ai-assistant-frontend:v1.0 ./services/frontend
docker push $REGISTRY/ai-assistant-frontend:v1.0

# Update image references in k8s/base/*.yaml
```

### Step 7: Deploy Application with HA

```bash
# Update backend replicas for HA
kubectl apply -f k8s/base/backend.yaml  # 5 replicas

# Deploy frontend (2+ replicas)
kubectl apply -f k8s/base/frontend.yaml

# Deploy horizontal autoscaling
kubectl apply -f k8s/production/hpa.yaml

# Verify HPA
kubectl get hpa -n ai-assistant
```

### Step 8: Deploy Ingress with SSL

```bash
# Install cert-manager for SSL
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create ClusterIssuer for Let's Encrypt
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF

# Deploy production ingress with SSL
kubectl apply -f k8s/production/ingress-ssl.yaml
```

### Step 9: Set Up Monitoring

```bash
# Install Prometheus Operator
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace \
  --set prometheus.prometheusSpec.retention=30d \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=100Gi

# Install Grafana dashboards
kubectl apply -f k8s/production/monitoring/

# Get Grafana password
kubectl get secret -n monitoring prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode

# Port forward to access
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
```

### Step 10: Deploy NHS Fine-tuned Model

```bash
# Ensure NHS model is in PVC or upload
kubectl cp ./nhs-model ai-assistant/vllm-models-pvc:/models/nhs-finetuned

# Deploy NHS-specific vLLM instance
kubectl apply -f k8s/production/vllm-gpu.yaml

# Verify NHS model serving
kubectl logs -n ai-assistant -l app=vllm-nhs -f
```

---

## GPU Support Setup

### NVIDIA GPU Operator Installation (Detailed)

```bash
# Verify GPU nodes
kubectl get nodes -l nvidia.com/gpu=true

# Label GPU nodes (if not auto-labeled)
kubectl label nodes <node-name> nvidia.com/gpu=true

# Install GPU Operator
helm install gpu-operator nvidia/gpu-operator \
  -n gpu-operator --create-namespace \
  --set driver.enabled=true \
  --set toolkit.enabled=true \
  --set devicePlugin.enabled=true \
  --set migManager.enabled=false

# Wait for installation
kubectl wait --for=condition=ready pod -n gpu-operator --all --timeout=600s

# Verify GPU devices
kubectl get nodes -o json | jq '.items[].status.capacity."nvidia.com/gpu"'
```

### Test GPU Access

```bash
# Run test pod
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: gpu-test
spec:
  containers:
  - name: cuda
    image: nvidia/cuda:11.8.0-base-ubuntu22.04
    command: ["nvidia-smi"]
    resources:
      limits:
        nvidia.com/gpu: 1
  restartPolicy: Never
EOF

# Check output
kubectl logs gpu-test

# Cleanup
kubectl delete pod gpu-test
```

---

## Monitoring Setup

### Prometheus + Grafana

```bash
# Deploy monitoring stack
kubectl apply -f k8s/production/monitoring/prometheus.yaml
kubectl apply -f k8s/production/monitoring/grafana.yaml

# Access Grafana
kubectl port-forward -n monitoring svc/grafana 3000:3000
```

### GPU Monitoring Dashboard

```bash
# Install DCGM exporter for GPU metrics
helm install dcgm-exporter nvidia/dcgm-exporter \
  -n gpu-operator \
  --set serviceMonitor.enabled=true

# Import GPU dashboard in Grafana (Dashboard ID: 12239)
```

---

## Scaling Guidelines

### Horizontal Scaling

```bash
# Scale backend manually
kubectl scale deployment backend -n ai-assistant --replicas=10

# Configure auto-scaling
kubectl autoscale deployment backend -n ai-assistant \
  --cpu-percent=70 \
  --min=3 \
  --max=20
```

### Vertical Scaling (Increase Resources)

```bash
# Update resource limits in deployment
kubectl edit deployment backend -n ai-assistant

# Modify:
resources:
  requests:
    memory: "1Gi"
    cpu: "1000m"
  limits:
    memory: "4Gi"
    cpu: "4000m"
```

---

## Backup and Restore

### Backup

```bash
# Backup PostgreSQL
kubectl exec -n ai-assistant postgres-0 -- \
  pg_dumpall -U aiuser > backup-$(date +%Y%m%d).sql

# Backup Qdrant
kubectl exec -n ai-assistant qdrant-0 -- \
  tar czf - /qdrant/storage > qdrant-backup-$(date +%Y%m%d).tar.gz
```

### Restore

```bash
# Restore PostgreSQL
kubectl exec -i -n ai-assistant postgres-0 -- \
  psql -U aiuser < backup-20260110.sql

# Restore Qdrant
kubectl cp qdrant-backup.tar.gz ai-assistant/qdrant-0:/tmp/
kubectl exec -n ai-assistant qdrant-0 -- \
  tar xzf /tmp/qdrant-backup.tar.gz -C /
```

---

## Troubleshooting

### Pods not starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n ai-assistant

# Check events
kubectl get events -n ai-assistant --sort-by='.lastTimestamp'

# Check resource availability
kubectl top nodes
kubectl top pods -n ai-assistant
```

### GPU not allocated

```bash
# Verify GPU operator
kubectl get pods -n gpu-operator

# Check node labels
kubectl describe node <gpu-node-name> | grep nvidia.com/gpu

# Restart GPU operator
kubectl rollout restart daemonset -n gpu-operator
```

### Performance issues

```bash
# Check resource usage
kubectl top pods -n ai-assistant

# Check HPA status
kubectl get hpa -n ai-assistant

# Scale up if needed
kubectl scale deployment backend -n ai-assistant --replicas=10
```

---

## Useful Commands

```bash
# View all resources
kubectl get all -n ai-assistant

# Logs from deployment
kubectl logs -n ai-assistant deployment/backend -f

# Execute into pod
kubectl exec -it -n ai-assistant deployment/backend -- bash

# Port forward for debugging
kubectl port-forward -n ai-assistant svc/backend 8000:8000

# Restart deployment
kubectl rollout restart deployment backend -n ai-assistant

# Check rollout status
kubectl rollout status deployment backend -n ai-assistant

# View resource usage
kubectl top nodes
kubectl top pods -n ai-assistant

# Delete and recreate
kubectl delete -f k8s/base/backend.yaml
kubectl apply -f k8s/base/backend.yaml
```

---

## Next Steps

1. ✅ Kubernetes cluster running
2. 📊 **Set up monitoring dashboards** → Configure Grafana
3. 🔐 **Configure HTTPS and authentication** → Set up OAuth2
4. 🏥 **Deploy NHS fine-tuned model** → See `NHS_FINETUNING.md`
5. 📱 **Remote access from laptop** → See `REMOTE_ACCESS.md`

---

## Production Checklist

- [ ] SSL/TLS certificates configured
- [ ] Authentication and RBAC enabled
- [ ] Monitoring and alerting set up
- [ ] Backup automation configured
- [ ] Resource limits properly set
- [ ] HPA configured for all deployments
- [ ] Network policies applied
- [ ] Secrets encrypted at rest
- [ ] GPU scheduling working
- [ ] Disaster recovery plan documented
