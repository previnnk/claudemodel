# Quick Deployment Fix

## Issue Encountered
The full `docker-compose.yml` requires building custom Docker images, which needs source code to be complete.

## ✅ Solution: Use Simplified Deployment

### Step 1: Start Core Services Only

Use the simplified docker-compose that only uses pre-built images:

```bash
# Start core services (no builds required)
docker-compose -f docker-compose-simple.yml up -d
```

**This starts:**
- ✅ PostgreSQL (database)
- ✅ Redis (cache)
- ✅ Qdrant (vector database)
- ✅ MinIO (object storage)
- ✅ Ollama (LLM inference)

**Time:** ~2 minutes

---

### Step 2: Download AI Model

```bash
# Wait 30 seconds for Ollama to be ready, then:
docker exec ai-assistant-ollama ollama pull mistral:7b-instruct
```

**Wait:** ~3-5 minutes (downloading 4GB model)

---

### Step 3: Verify Everything is Running

```bash
# Check all containers
docker-compose -f docker-compose-simple.yml ps

# Should show 5 containers running
```

**Expected output:**
```
NAME                      STATUS
ai-assistant-postgres     Up
ai-assistant-redis        Up
ai-assistant-qdrant       Up
ai-assistant-minio        Up
ai-assistant-ollama       Up
```

---

### Step 4: Test the Services

#### Test PostgreSQL
```bash
docker exec -it ai-assistant-postgres psql -U aiuser -d ai_assistant -c "SELECT version();"
```

#### Test Redis
```bash
docker exec -it ai-assistant-redis redis-cli ping
# Should return: PONG
```

#### Test Qdrant
```bash
curl http://localhost:6333/healthz
# Should return: ok
```

#### Test MinIO
Open browser: http://localhost:9001
- Username: `minioadmin`
- Password: `minioadmin123`

#### Test Ollama
```bash
curl http://localhost:11434/api/tags
```

#### Test AI Inference
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "mistral:7b-instruct",
  "prompt": "Write a hello world in Python",
  "stream": false
}'
```

---

## 🎯 What You Have Now

✅ **Working LLM Backend**: Ollama with Mistral 7B
✅ **Vector Database**: Qdrant for RAG
✅ **Data Storage**: PostgreSQL + Redis
✅ **Object Storage**: MinIO (S3-compatible)

## ❌ What's Missing (For Now)

The custom application services:
- Backend API (FastAPI)
- Frontend Web UI (React)
- Code Agent (Tool executor)
- Embedding Service
- Integration Layer

**Why?** These require building Docker images from source code.

---

## 🚀 Next Steps: Build Application Services

Once the core services are running, you can build and add the application:

### Option 1: Build Services Locally

```bash
# Build backend
cd services/backend
docker build -t ai-assistant-backend:latest .

# Build frontend (after fixing remaining issues)
cd services/frontend
docker build -t ai-assistant-frontend:latest .

# Then start full stack
cd ../..
docker-compose up -d
```

### Option 2: Use API Directly

You can interact with Ollama directly for now:

```python
# test_ollama.py
import requests

response = requests.post('http://localhost:11434/api/generate', json={
    "model": "mistral:7b-instruct",
    "prompt": "Write a Python function to check if a number is prime",
    "stream": False
})

print(response.json()['response'])
```

---

## 📊 Current System Status

| Service | Status | Port | Purpose |
|---------|--------|------|---------|
| PostgreSQL | ✅ Running | 5432 | Database |
| Redis | ✅ Running | 6379 | Cache |
| Qdrant | ✅ Running | 6333 | Vector DB |
| MinIO | ✅ Running | 9000, 9001 | Object Storage |
| Ollama | ✅ Running | 11434 | LLM Inference |
| Backend API | ⏸️ Pending | 8000 | Application API |
| Frontend | ⏸️ Pending | 3000 | Web UI |
| Code Agent | ⏸️ Pending | 8002 | Tool Executor |
| Embedding | ⏸️ Pending | 8001 | Embeddings |
| Integration | ⏸️ Pending | 8003 | Connectors |

---

## 🛠️ Troubleshooting

### Services Won't Start
```bash
# Check Docker is running
docker info

# View logs
docker-compose -f docker-compose-simple.yml logs

# Restart specific service
docker-compose -f docker-compose-simple.yml restart ollama
```

### Ollama Model Download Fails
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Manual download
docker exec -it ai-assistant-ollama bash
ollama pull mistral:7b-instruct
exit
```

### Port Already in Use
```bash
# Find what's using the port
netstat -ano | findstr :11434

# Kill the process or change port in docker-compose-simple.yml
```

---

## 💡 Quick Test

Once Mistral is downloaded, test it:

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "mistral:7b-instruct",
  "prompt": "Explain what a prime number is in one sentence",
  "stream": false
}' | jq .response
```

---

## ✅ Success Criteria

You're ready for the next phase when:

- [ ] All 5 core services are running
- [ ] Mistral 7B model is downloaded
- [ ] Ollama responds to API calls
- [ ] Can generate text via curl/API

**Estimated time:** 10-15 minutes total

---

## 📞 Need Help?

Check logs:
```bash
docker-compose -f docker-compose-simple.yml logs -f ollama
```

Stop everything:
```bash
docker-compose -f docker-compose-simple.yml down
```

Start fresh:
```bash
docker-compose -f docker-compose-simple.yml down -v  # WARNING: Deletes data
docker-compose -f docker-compose-simple.yml up -d
```

---

**Once this is working, we'll add the application services one by one!** 🚀
