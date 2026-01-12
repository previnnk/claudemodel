# Quick Start Guide - AI Coding Assistant

**Complete setup in 3 steps. Everything you need to know.**

---

## 📋 What You Have

✅ **6 Architecture Diagrams** (PlantUML) - Local + Production + C4 Model
✅ **Complete Docker Compose** - Start with one command
✅ **Kubernetes Manifests** - Production-ready
✅ **Enterprise Integrations** - GitHub, SharePoint, Confluence, Databases
✅ **Evaluation Framework** - Compare vs Claude Code, ChatGPT, Grok
✅ **NHS Fine-tuning Guide** - Healthcare specialization
✅ **Beautiful Web UI** - Remote accessible via HTTP

---

## 🚀 Step 1: View the Architecture (5 minutes)

### Quick View - Online

1. Go to: **https://www.planttext.com/**
2. Open: `architecture-local.puml`
3. Copy all contents (Ctrl+A, Ctrl+C)
4. Paste into PlantText
5. Click **"Refresh"**
6. ✅ See your local architecture!

**Repeat for:**
- `architecture-production.puml` - Production GPU setup
- `architecture-c4-context.puml` - Enterprise integrations
- `architecture-c4-container.puml` - Service details

📖 **Full guide**: `VIEW_DIAGRAMS.md`

---

## 🖥️ Step 2: Deploy Locally (10 minutes)

### Prerequisites Check
```bash
# Check Docker Desktop is installed
docker --version
# Should show: Docker version 24.0+

# Check disk space
# Need: 200GB free
```

### Start Everything
```bash
# Navigate to project
cd D:\workspace\NHS\ClaudeModel

# Start all services
docker-compose up -d

# Check status (all should be "running")
docker-compose ps

# Download AI model (Mistral 7B - fast and good)
docker exec ai-assistant-ollama ollama pull mistral:7b-instruct

# Wait ~2 minutes for model download
```

### Access the UI
```
Open browser: http://localhost:3000

You should see:
✅ Beautiful dark-themed chat interface
✅ Monaco code editor
✅ File browser
✅ Terminal
```

### Test It
```
Type in chat:
"Hello! Write me a Python function to check if a number is prime."

Expected:
✅ Streaming response
✅ Properly formatted code
✅ Explanation
```

📖 **Full guide**: `INSTALLATION_LOCAL.md`

---

## 🧪 Step 3: Run Evaluation (30 minutes)

### Setup API Keys

Get free API keys from:
- **Claude**: https://console.anthropic.com/
- **ChatGPT**: https://platform.openai.com/

```powershell
# Windows PowerShell
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"
$env:OPENAI_API_KEY="sk-your-key-here"
$env:LOCAL_AI_URL="http://localhost:8000"
```

### Run Quick Test
```bash
# Install dependencies
pip install anthropic openai requests

# Test one prompt (fastest)
python evaluation_test.py --prompt "Write a function to reverse a string"

# Run simple category (5 tests, ~10 min)
python evaluation_test.py --category simple

# Run everything (20 tests, ~60 min)
python evaluation_test.py --run-all
```

### Review Results
```bash
# Open the generated report
code evaluation_report_YYYYMMDD_HHMMSS.md

# Manually score each response (1-5)
# See EVALUATION_FRAMEWORK.md for scoring guide
```

📖 **Full guide**: `EVALUATION_SETUP.md`

---

## 🌐 Access from Laptop (Remote)

### Option 1: SSH Tunnel (Secure)
```bash
# From laptop
ssh -L 3000:localhost:3000 -L 8000:localhost:8000 user@desktop-ip

# Then access: http://localhost:3000
```

### Option 2: Tailscale (Easiest)
```bash
# Install on both desktop and laptop
# https://tailscale.com/download

# Access: http://<tailscale-ip>:3000
```

### Option 3: Ngrok (Public URL)
```bash
# On desktop
ngrok http 3000

# Share the URL: https://abc123.ngrok.io
```

📖 **Full guide**: `REMOTE_ACCESS.md`

---

## 📚 All Documentation

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **README.md** | Project overview | Start here |
| **VIEW_DIAGRAMS.md** | How to view architecture | Before deployment |
| **INSTALLATION_LOCAL.md** | Docker setup | Local deployment |
| **INSTALLATION_K8S.md** | Kubernetes setup | Production deployment |
| **REMOTE_ACCESS.md** | Laptop→Desktop access | Remote work |
| **EVALUATION_FRAMEWORK.md** | KPI metrics | Quality assessment |
| **EVALUATION_SETUP.md** | Running tests | Compare vs Claude Code |
| **NHS_FINETUNING.md** | Healthcare fine-tuning | NHS specialization |
| **TECH_STACK.md** | Technology details | Understanding stack |
| **PROJECT_SUMMARY.md** | Complete summary | Overview |

---

## 🎯 Common Workflows

### Workflow 1: Initial Setup & Test
```bash
1. View architecture: architecture-local.puml
2. Deploy: docker-compose up -d
3. Download model: docker exec ai-assistant-ollama ollama pull mistral:7b-instruct
4. Test: http://localhost:3000
5. Evaluate: python evaluation_test.py --category simple
```

### Workflow 2: Remote Access Setup
```bash
1. Deploy on desktop: docker-compose up -d
2. Get desktop IP: ipconfig
3. From laptop: ssh -L 3000:localhost:3000 user@desktop-ip
4. Access: http://localhost:3000
```

### Workflow 3: Production Deployment
```bash
1. Review: architecture-production.puml
2. Setup K8s cluster
3. Deploy: kubectl apply -f k8s/base/
4. Deploy GPU: kubectl apply -f k8s/production/vllm-gpu.yaml
5. Configure integrations
```

### Workflow 4: NHS Fine-tuning
```bash
1. Collect NHS data (with IG approval)
2. Preprocess: python preprocess_nhs_data.py
3. Fine-tune: python train_lora.py
4. Deploy: kubectl apply -f k8s/production/vllm-gpu.yaml
5. Test with medical queries
```

---

## 🔧 Troubleshooting

### Docker won't start
```bash
# Start Docker Desktop manually
# Windows: Start Menu → Docker Desktop
# Wait for green icon in system tray
```

### Services won't start
```bash
# Check logs
docker-compose logs backend

# Restart specific service
docker-compose restart backend

# Full restart
docker-compose down
docker-compose up -d
```

### Can't access from laptop
```bash
# Check desktop firewall
# Windows: Allow port 3000, 8000

# Check desktop IP
ipconfig  # Windows
ip addr   # Linux

# Test connection
ping desktop-ip
```

### Evaluation tests failing
```bash
# Check API keys
echo $ANTHROPIC_API_KEY

# Check local instance
curl http://localhost:8000/health

# Run with debug
python -v evaluation_test.py --category simple
```

---

## 📊 Expected Results

### Local Deployment
- **Time to deploy**: 5-10 minutes
- **First response**: < 10 seconds
- **Quality**: 3.5-4.0/5.0 (adequate to good)
- **Cost**: $0 (hardware only)

### After Fine-tuning
- **Quality**: 4.0-4.5/5.0 (good to excellent)
- **Specialized knowledge**: NHS/healthcare specific
- **Response accuracy**: Improved on domain tasks

### Production Deployment
- **Availability**: 99.9%
- **Response time**: < 2 seconds
- **Concurrent users**: 100+
- **Quality**: 4.5+/5.0 (excellent)

---

## ✅ Checklist

### Before Deployment
- [ ] Reviewed architecture diagrams
- [ ] Docker Desktop installed and running
- [ ] 200GB+ disk space available
- [ ] 32GB+ RAM

### After Deployment
- [ ] All containers running (`docker-compose ps`)
- [ ] Model downloaded
- [ ] Web UI accessible (http://localhost:3000)
- [ ] Chat responds correctly

### For Evaluation
- [ ] API keys configured
- [ ] Dependencies installed
- [ ] Tests run successfully
- [ ] Results manually scored

### For Production
- [ ] Kubernetes cluster ready
- [ ] GPU nodes configured
- [ ] Monitoring deployed
- [ ] Backups configured

---

## 🎓 Learning Path

### Week 1: Local Setup
- Day 1-2: Deploy locally, test basic functionality
- Day 3-4: Run evaluations, compare quality
- Day 5-7: Improve prompts, optimize

### Week 2: Remote Access
- Day 1-2: Setup SSH tunnel
- Day 3-4: Install Tailscale for mesh VPN
- Day 5-7: Test from multiple locations

### Week 3: Integrations
- Day 1-2: Configure GitHub connector
- Day 3-4: Configure SharePoint connector
- Day 5-7: Test RAG with enterprise data

### Week 4: Production
- Day 1-3: Deploy to Kubernetes
- Day 4-5: Setup monitoring
- Day 6-7: Load testing

---

## 💰 Cost Breakdown

### Development (One-time)
- Desktop hardware: $2,000-5,000
- Software: **$0** (all open source)

### Evaluation Testing
- Claude API: ~$0.25 per full test (20 prompts)
- ChatGPT API: ~$0.15 per full test
- Perplexity API: ~$0.10 per full test
- **Total per test**: ~$0.50

### Production (Nutonics)
- Hardware: $50,000-100,000 (one-time)
- Electricity: ~$500-1,000/month
- Software: **$0** (all open source)

### Comparison (Cloud)
- AWS 3x A100 GPU: ~$8,000-12,000/month
- **Savings**: ~$80,000-120,000/year with self-hosted

---

## 🚀 Next Actions

**Right Now:**
1. ✅ View `architecture-local.puml` (PlantText.com)
2. ✅ Run `docker-compose up -d`
3. ✅ Test at `http://localhost:3000`

**This Week:**
4. ✅ Run evaluation tests
5. ✅ Setup remote access
6. ✅ Review documentation

**This Month:**
7. ✅ Deploy to production K8s
8. ✅ Configure integrations
9. ✅ Fine-tune for NHS

---

## 📞 Support

### Documentation Issues
- Check `VIEW_DIAGRAMS.md` for diagram help
- Check `INSTALLATION_LOCAL.md` for deployment help
- Check troubleshooting sections

### Evaluation Questions
- Review `EVALUATION_FRAMEWORK.md` for KPI definitions
- Check `EVALUATION_SETUP.md` for test setup

### Production Deployment
- Review `INSTALLATION_K8S.md`
- Check `architecture-production.puml`

---

## 🎉 Success Criteria

You'll know it's working when:

✅ All Docker containers are running
✅ Web UI loads at http://localhost:3000
✅ Chat responds to prompts
✅ Code generation is readable
✅ Evaluation score > 3.5/5.0
✅ Remote access works from laptop

---

**Ready to start? Pick your path:**

🏃 **Fast Track** (30 min):
1. `docker-compose up -d`
2. Download model
3. Test at http://localhost:3000

📚 **Thorough** (2 hours):
1. View all architecture diagrams
2. Read INSTALLATION_LOCAL.md
3. Deploy with monitoring
4. Run evaluation tests

🚀 **Production** (1 week):
1. Review all documentation
2. Deploy locally first
3. Test and evaluate
4. Deploy to Kubernetes cluster

Good luck! 🎯
