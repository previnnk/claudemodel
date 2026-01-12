# AI Coding Assistant - Complete Tech Stack

## Overview
This document outlines the complete technology stack for building an AI coding assistant similar to Claude Code using open-source components.

---

## 1. Core LLM Models (Open Source)

### Primary Coding Models
| Model | Parameters | Use Case | VRAM Required | License |
|-------|------------|----------|---------------|---------|
| **CodeLlama-34B-Instruct** | 34B | Code generation, completion | 20GB (FP16) | Llama 2 License |
| **DeepSeek-Coder-33B-Instruct** | 33B | Advanced coding tasks | 20GB (FP16) | DeepSeek License |
| **Mistral-7B-Instruct** | 7B | General reasoning, fast inference | 5GB (FP16) | Apache 2.0 |
| **Mixtral-8x7B-Instruct** | 47B (8x7B MoE) | Complex multi-step tasks | 28GB (FP16) | Apache 2.0 |
| **StarCoder2-15B** | 15B | Code completion | 9GB (FP16) | BigCode License |

### Quantized Models (for CPU/Low-memory GPU)
- **GGUF format** (llama.cpp compatible)
- **Q4_K_M**: 4-bit quantization, ~3-5GB per 7B model
- **Q5_K_M**: 5-bit quantization, better quality

### Recommended for NHS Fine-tuning
- **Base**: Mistral-7B or Llama-2-13B
- **Method**: LoRA/QLoRA fine-tuning (parameter-efficient)

---

## 2. LLM Inference Engines

### Option A: vLLM (Recommended for GPU Production)
- **Purpose**: High-throughput LLM serving
- **Features**:
  - Continuous batching
  - PagedAttention for memory efficiency
  - OpenAI-compatible API
  - Multi-GPU support via tensor parallelism
- **Best for**: Production GPU deployment

### Option B: Ollama (Recommended for Local CPU/GPU)
- **Purpose**: Easy local LLM deployment
- **Features**:
  - Simple CLI interface
  - Automatic model downloading
  - CPU & GPU support
  - Model library management
- **Best for**: Local development, prototyping

### Option C: llama.cpp + llama-cpp-python
- **Purpose**: Efficient CPU inference
- **Features**:
  - GGUF quantized models
  - Metal (Mac), CUDA, OpenCL support
  - Low memory footprint
- **Best for**: CPU-only deployment

### Option D: TGI (Text Generation Inference by HuggingFace)
- **Purpose**: Production-grade inference
- **Features**:
  - Streaming, batching
  - Distributed inference
  - Token streaming
- **Best for**: HuggingFace model ecosystem

---

## 3. Backend Framework

### API Framework: FastAPI (Python)
```
Why FastAPI:
- High performance (async/await)
- Automatic OpenAPI docs
- WebSocket support
- Easy integration with Python ML ecosystem
- Type hints and validation (Pydantic)
```

### Alternative: Node.js + Express
```
For TypeScript-based teams, but Python preferred for ML integration
```

---

## 4. Frontend Stack

### Web UI: React + TypeScript
- **UI Framework**: ShadCN UI / Radix UI (modern, accessible)
- **Styling**: Tailwind CSS
- **Code Editor**: Monaco Editor (VS Code editor component)
- **Terminal**: Xterm.js
- **State Management**: Zustand or React Query

### Alternative: Svelte + SvelteKit
```
Lighter weight, faster builds, but smaller ecosystem
```

---

## 5. Vector Database & RAG

### Vector Database: Qdrant
```yaml
Why Qdrant:
- Fast similarity search
- Filtering capabilities
- Easy Docker deployment
- Scalable (cluster mode)
- Good Python client
```

### Alternatives:
- **Milvus**: More enterprise features, complex setup
- **Weaviate**: GraphQL API, good for knowledge graphs
- **ChromaDB**: Simple, embedded mode, good for prototyping

### Embedding Models:
- **all-MiniLM-L6-v2**: Fast, 384 dimensions, general purpose
- **e5-large-v2**: Better quality, 1024 dimensions
- **bge-large-en-v1.5**: State-of-the-art, 1024 dimensions

### RAG Framework: LangChain
```python
Components:
- Document loaders (code parsers)
- Text splitters (semantic chunking)
- Vector stores
- Retrievers
- Chains for complex workflows
```

### Alternative: LlamaIndex
```
More focused on RAG, better for document Q&A
```

---

## 6. Code Understanding

### Code Parser: Tree-sitter
```
- Parse code into AST
- Support 40+ languages
- Fast incremental parsing
- Extract functions, classes, imports
```

### Code Search: ripgrep (rg)
```
- Blazing fast code search
- Respects .gitignore
- Regex support
```

---

## 7. Databases

### Primary Database: PostgreSQL 16
```yaml
Use cases:
- Store conversations
- User sessions
- Project metadata
- Audit logs

Features:
- JSONB for flexible schemas
- Full-text search
- pgvector extension (vector storage backup)
```

### Cache & Session Store: Redis 7
```yaml
Use cases:
- Session management
- Rate limiting
- Job queues (Bull/BullMQ)
- Caching LLM responses

Features:
- In-memory speed
- Pub/Sub for real-time updates
- Redis Streams for event sourcing
```

---

## 8. Object Storage

### Local Development: MinIO
```
S3-compatible, easy Docker deployment
```

### Production: AWS S3 / Azure Blob / Google Cloud Storage
```
Store:
- Uploaded files
- Generated artifacts
- Model checkpoints
- Backup data
```

---

## 9. Container & Orchestration

### Containers: Docker
```
All services containerized for consistency
```

### Local Orchestration: Docker Compose
```
Simple multi-container deployment for development
```

### Production Orchestration: Kubernetes (K8s)
```yaml
Features:
- Auto-scaling (HPA)
- Self-healing
- Load balancing
- Rolling updates
- GPU scheduling (NVIDIA GPU Operator)
```

### K8s Distributions:
- **Local**: Docker Desktop K8s, Minikube, k3d
- **Production**: K3s (lightweight), RKE2, vanilla K8s

---

## 10. API Gateway & Ingress

### Development: Direct service access
### Production: Kong or Traefik
```yaml
Features:
- Rate limiting
- Authentication
- Load balancing
- Request routing
- SSL termination
```

---

## 11. Monitoring & Observability

### Metrics: Prometheus + Grafana
```
- Service metrics
- GPU utilization
- Request latency
- Error rates
```

### Logging: Loki + Promtail
```
- Centralized logging
- Log aggregation from all pods
- Grafana integration
```

### Tracing: Jaeger
```
- Distributed tracing
- Request flow visualization
- Performance bottleneck identification
```

### LLM Observability: LangSmith or PromptLayer
```
- Track prompts and responses
- Debug RAG pipeline
- A/B testing prompts
```

---

## 12. Authentication & Authorization

### Development: Simple API keys

### Production:
- **OAuth2/OIDC**: Keycloak (self-hosted) or Auth0
- **JWT tokens**: For stateless auth
- **RBAC**: Role-based access control in K8s

---

## 13. Fine-tuning Infrastructure

### Training Framework: PyTorch + HuggingFace Transformers
```python
Components:
- transformers: Model loading, training
- peft: LoRA/QLoRA implementation
- datasets: Data loading
- accelerate: Multi-GPU training
- bitsandbytes: 4-bit/8-bit quantization
```

### Workflow Orchestration: Kubeflow Pipelines
```
- ML workflow management
- Experiment tracking
- Hyperparameter tuning
```

### Experiment Tracking: MLflow or Weights & Biases
```
- Track metrics
- Compare runs
- Model registry
```

---

## 14. CI/CD

### GitOps: ArgoCD or Flux
```
Continuous deployment to K8s from Git
```

### CI Pipeline: GitHub Actions or GitLab CI
```yaml
Stages:
- Lint & test code
- Build Docker images
- Push to registry
- Deploy to K8s
```

---

## 15. Development Tools

### IDE Integration:
- **VS Code Extension**: TypeScript + VS Code Extension API
- **Protocol**: Language Server Protocol (LSP) compatible

### Testing:
- **Backend**: pytest, pytest-asyncio
- **Frontend**: Jest, React Testing Library
- **E2E**: Playwright or Cypress

---

## 16. Programming Languages

| Component | Language | Why |
|-----------|----------|-----|
| Backend API | Python 3.11+ | ML ecosystem, FastAPI |
| LLM Serving | Python | vLLM, transformers |
| Frontend | TypeScript | Type safety, tooling |
| VS Code Ext | TypeScript | VS Code API |
| Scripts | Python/Bash | Automation |

---

## 17. Recommended Tech Stack Summary

### 🏠 Local Development (Docker)
```yaml
LLM: Ollama (Mistral-7B-Instruct)
Backend: FastAPI
Frontend: React + Vite
Vector DB: Qdrant
Database: PostgreSQL
Cache: Redis
Storage: MinIO
Orchestration: Docker Compose
```

### 🚀 Production (Kubernetes + GPU)
```yaml
LLM: vLLM (CodeLlama-34B + NHS Fine-tuned Model)
Backend: FastAPI (5 replicas)
Frontend: React + Nginx
Vector DB: Qdrant Cluster (3 nodes)
Database: PostgreSQL HA (3 nodes)
Cache: Redis Cluster
Storage: S3/MinIO Distributed
Ingress: Kong/Traefik
Monitoring: Prometheus + Grafana + Loki
Orchestration: Kubernetes
GPU: NVIDIA A100/H100 with NVIDIA GPU Operator
```

---

## 18. Resource Requirements

### Local Desktop (Development)
```
Minimum:
- CPU: 8 cores (Intel i7 / AMD Ryzen 7)
- RAM: 32GB
- Storage: 200GB SSD
- GPU: Optional (NVIDIA RTX 3060 12GB for faster inference)

Recommended:
- CPU: 16 cores
- RAM: 64GB
- Storage: 500GB NVMe SSD
- GPU: NVIDIA RTX 4090 24GB
```

### Production (Nutonics GPU Cluster)
```
Per GPU Node:
- CPU: 32+ cores (AMD EPYC / Intel Xeon)
- RAM: 256GB
- GPU: NVIDIA A100 40GB/80GB or H100 80GB
- Storage: 2TB NVMe (models) + 10TB SSD (data)
- Network: 100Gbps interconnect

Cluster:
- 3-6 GPU nodes
- 3 storage nodes (PostgreSQL, Redis, Qdrant)
- 1 control plane node
- Minimum 3 worker nodes for services
```

---

## 19. Estimated Costs (Open Source)

### Infrastructure Only (no licensing costs):
```
Local Development: Hardware cost only ($2000-5000 for desktop)

Production (Cloud):
- 3x NVIDIA A100 40GB on cloud: ~$8-12/hour = $6000-9000/month
- Supporting infrastructure: ~$1000-2000/month
- Total: ~$7000-11000/month

Production (Self-hosted Nutonics):
- One-time hardware: $50,000-100,000
- Electricity: ~$500-1000/month
- No per-hour GPU costs!
```

---

## 20. Open Source Licenses

All components are open source with permissive licenses:

| Component | License |
|-----------|---------|
| CodeLlama | Llama 2 (commercial use OK) |
| Mistral/Mixtral | Apache 2.0 |
| DeepSeek Coder | MIT-like (commercial OK) |
| FastAPI | MIT |
| React | MIT |
| vLLM | Apache 2.0 |
| Ollama | MIT |
| Qdrant | Apache 2.0 |
| PostgreSQL | PostgreSQL License (permissive) |
| Redis | BSD-3-Clause |
| LangChain | MIT |

**No licensing fees required for any component!**

---

## Next Steps

See the installation guides:
- `INSTALLATION_LOCAL.md` - Docker Compose setup for local development
- `INSTALLATION_K8S.md` - Kubernetes deployment guide
- `REMOTE_ACCESS.md` - Laptop to desktop remote access setup
- `NHS_FINETUNING.md` - Guide for fine-tuning on NHS healthcare data
