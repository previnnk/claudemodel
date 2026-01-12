# Local Installation Guide - Docker Desktop

This guide will help you set up the AI Coding Assistant on your local desktop using Docker Compose.

## Prerequisites

### Hardware Requirements
- **CPU**: 8+ cores (Intel i7/AMD Ryzen 7 or better)
- **RAM**: 32GB minimum (64GB recommended)
- **Storage**: 200GB free space (SSD recommended)
- **GPU** (Optional): NVIDIA GPU with 12GB+ VRAM for faster inference

### Software Requirements
1. **Docker Desktop** (with Kubernetes enabled)
   - Version 4.25+
   - Download: https://www.docker.com/products/docker-desktop

2. **Git**
   - Download: https://git-scm.com/downloads

3. **For GPU Support (Optional)**:
   - NVIDIA Docker Runtime
   - NVIDIA Container Toolkit
   - CUDA 11.8+ drivers

---

## Step 1: Install Docker Desktop

### Windows
1. Download Docker Desktop for Windows
2. Run the installer
3. Follow the installation wizard
4. **Enable WSL 2** when prompted (recommended)
5. Restart your computer

### Verify Installation
```bash
docker --version
docker-compose --version
```

Expected output:
```
Docker version 24.0.x
Docker Compose version v2.x.x
```

---

## Step 2: Enable Kubernetes (Optional but Recommended)

1. Open Docker Desktop
2. Go to **Settings** → **Kubernetes**
3. Check **Enable Kubernetes**
4. Click **Apply & Restart**
5. Wait for Kubernetes to start (green indicator)

Verify:
```bash
kubectl version --client
kubectl get nodes
```

---

## Step 3: Clone the Repository

```bash
cd D:\workspace\NHS
git clone <your-repo-url> ClaudeModel
cd ClaudeModel
```

---

## Step 4: Configure Environment Variables

Create a `.env` file in the root directory:

```bash
# Copy the example
cp .env.example .env

# Edit with your values
notepad .env
```

Example `.env` file:
```env
# Database
POSTGRES_USER=aiuser
POSTGRES_PASSWORD=secure_password_here
POSTGRES_DB=ai_assistant

# Redis
REDIS_PASSWORD=redis_password_here

# Backend
SECRET_KEY=your-secret-key-min-32-chars
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# LLM Configuration
OLLAMA_MODEL=mistral:7b-instruct
# For more powerful coding: codellama:34b-instruct

# MinIO/S3
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin123

# GPU Support (uncomment if you have NVIDIA GPU)
# OLLAMA_GPU_ENABLED=true
```

---

## Step 5: Start Services with Docker Compose

### Basic Startup (All Services)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

### Start Specific Services

```bash
# Start only core services (without monitoring)
docker-compose up -d postgres redis qdrant minio ollama backend frontend
```

### Start with Monitoring

```bash
# Start all including Prometheus and Grafana
docker-compose --profile monitoring up -d
```

---

## Step 6: Download LLM Models

Once Ollama is running, download models:

```bash
# Download Mistral 7B (recommended for starting)
docker exec -it ai-assistant-ollama ollama pull mistral:7b-instruct

# Download CodeLlama 34B (for better code generation, requires 20GB RAM)
docker exec -it ai-assistant-ollama ollama pull codellama:34b-instruct

# Download smaller model for faster responses
docker exec -it ai-assistant-ollama ollama pull deepseek-coder:6.7b

# List downloaded models
docker exec -it ai-assistant-ollama ollama list
```

**Model Download Times**:
- Mistral 7B: ~2-5 minutes (4.1GB)
- CodeLlama 34B: ~10-15 minutes (19GB)
- DeepSeek Coder 6.7B: ~3-5 minutes (3.8GB)

---

## Step 7: Initialize Database

```bash
# Run database migrations
docker-compose exec backend python -m alembic upgrade head

# Create initial data (optional)
docker-compose exec backend python scripts/init_db.py
```

---

## Step 8: Verify Installation

### Check Service Health

```bash
# Backend health check
curl http://localhost:8000/health

# Frontend
curl http://localhost:3000

# Ollama
curl http://localhost:11434/api/tags
```

### Access Web Interfaces

1. **Frontend**: http://localhost:3000
2. **Backend API Docs**: http://localhost:8000/docs
3. **MinIO Console**: http://localhost:9001
   - Username: `minioadmin`
   - Password: `minioadmin123`
4. **Qdrant Dashboard**: http://localhost:6333/dashboard
5. **Grafana** (if monitoring enabled): http://localhost:3001
   - Username: `admin`
   - Password: `admin`

---

## Step 9: Build Custom Images (If Modified)

If you've made changes to the source code:

```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build backend

# Build and start
docker-compose up -d --build
```

---

## Step 10: Test the System

### Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! Can you help me write a Python function?",
    "session_id": "test-123"
  }'
```

### Test Embedding Service

```bash
curl -X POST http://localhost:8001/embed \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["Hello world", "Test embedding"]
  }'
```

### Test Frontend

Open browser: http://localhost:3000

---

## Troubleshooting

### Issue: Ollama fails to start
**Solution**: Increase Docker memory allocation
1. Docker Desktop → Settings → Resources
2. Increase Memory to at least 8GB (16GB recommended)
3. Apply & Restart

### Issue: Services can't connect to each other
**Solution**: Check network configuration
```bash
# Inspect network
docker network inspect claudemodel_ai-network

# Restart services
docker-compose down
docker-compose up -d
```

### Issue: Out of disk space
**Solution**: Clean up Docker resources
```bash
# Remove unused containers, images, volumes
docker system prune -a --volumes

# WARNING: This removes ALL unused Docker data
```

### Issue: Port already in use
**Solution**: Change ports in `docker-compose.yml`
```yaml
# Example: Change frontend port from 3000 to 3001
frontend:
  ports:
    - "3001:80"  # Changed from 3000:80
```

### Issue: GPU not detected
**Solution**: Install NVIDIA Container Toolkit
```bash
# Windows (WSL2)
# Follow: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html

# Verify GPU access
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

---

## Useful Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
```

### Stop Services
```bash
# Stop all (keeps data)
docker-compose stop

# Stop and remove containers (keeps volumes)
docker-compose down

# Stop and remove everything including volumes (DANGER)
docker-compose down -v
```

### Access Container Shell
```bash
# Backend
docker-compose exec backend bash

# Database
docker-compose exec postgres psql -U aiuser -d ai_assistant

# Redis
docker-compose exec redis redis-cli
```

### Monitor Resource Usage
```bash
docker stats
```

---

## Performance Tuning

### For CPU-Only Machines
```yaml
# In docker-compose.yml, use quantized models
environment:
  - OLLAMA_MODEL=mistral:7b-instruct-q4_K_M
```

### For GPU Machines
```yaml
# Uncomment in docker-compose.yml under ollama service
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: 1
          capabilities: [gpu]
```

---

## Next Steps

1. ✅ System is running locally
2. 📱 **Set up remote access** from laptop → See `REMOTE_ACCESS.md`
3. ☸️ **Deploy to Kubernetes** → See `INSTALLATION_K8S.md`
4. 🏥 **Fine-tune for NHS data** → See `NHS_FINETUNING.md`
5. 🔧 **Customize and extend** → See `DEVELOPMENT.md`

---

## Quick Start Script

Save this as `start.sh`:

```bash
#!/bin/bash

echo "Starting AI Coding Assistant..."

# Start services
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 30

# Download models if not present
echo "Checking models..."
docker exec ai-assistant-ollama ollama list | grep mistral || \
  docker exec ai-assistant-ollama ollama pull mistral:7b-instruct

# Show status
echo ""
echo "Service Status:"
docker-compose ps

echo ""
echo "Access URLs:"
echo "  Frontend:  http://localhost:3000"
echo "  Backend:   http://localhost:8000"
echo "  API Docs:  http://localhost:8000/docs"
echo ""
echo "To view logs: docker-compose logs -f"
```

Run with:
```bash
chmod +x start.sh
./start.sh
```

---

## Support

If you encounter issues:
1. Check logs: `docker-compose logs -f`
2. Verify Docker resources (Settings → Resources)
3. Ensure ports are not in use
4. Check firewall settings
5. Review `TROUBLESHOOTING.md` for common issues
