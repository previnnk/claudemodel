# AI Coding Assistant - Open Source Implementation

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)

**Production-ready AI Coding Assistant similar to Claude Code, built with open-source LLMs**

Supports NHS Healthcare data fine-tuning | Enterprise integrations | GPU acceleration | MCP Protocol

[Features](#features) • [Quick Start](#quick-start) • [Architecture](#architecture) • [Documentation](#documentation)

</div>

---

## 🎯 Overview

This is a **complete, production-ready AI coding assistant** similar to Claude Code or Cursor AI, built entirely with free, open-source components. It features:

- **🤖 Advanced Code Generation** - Using CodeLlama 34B, DeepSeek Coder, Mistral models
- **🏥 NHS Healthcare Specialization** - Fine-tunable for medical/clinical domains
- **🔌 Enterprise Integrations** - SharePoint, Confluence, GitHub, Oracle, SQL Server, Epic EHR
- **📡 MCP Protocol Support** - Standardized context protocol for AI applications
- **☁️ Dual Deployment** - Local Docker setup + Production Kubernetes with GPU
- **🌐 Beautiful Web UI** - Modern React interface accessible remotely via HTTP
- **🛠️ Full Tool Suite** - Read, Write, Edit, Bash, Grep, Glob, and more

---

## ✨ Features

### Core Capabilities
- ✅ **Chat Interface** with streaming responses
- ✅ **Code Generation** and completion
- ✅ **File Operations** - Read, write, edit files
- ✅ **Command Execution** - Run bash commands safely
- ✅ **Code Search** - Fast grep/glob across codebases
- ✅ **RAG (Retrieval Augmented Generation)** - Context from your codebase
- ✅ **Multi-model Support** - Route queries to specialized models

### Enterprise Features (Production Only)
- 🔌 **GitHub Integration** - Code search, PR creation, issue management
- 🔌 **SharePoint Integration** - Document search and retrieval
- 🔌 **Confluence Integration** - Wiki/documentation access
- 🔌 **Database Connectors** - Oracle, SQL Server (read-only)
- 🔌 **FHIR API** - Epic EHR patient data (secure)
- 🔌 **MCP Servers** - Pluggable context providers

### NHS Healthcare Features
- 🏥 **Medical Knowledge** - Fine-tuned on clinical guidelines
- 🏥 **Equipment Documentation** - Integrated maintenance protocols
- 🏥 **NICE Guidelines** - Built-in clinical decision support
- 🏥 **Compliance Ready** - GDPR, NHS Data Security Standards

---

## 🚀 Quick Start

### Prerequisites
- Docker Desktop (with Kubernetes enabled for production)
- 32GB RAM minimum (64GB recommended)
- 200GB free disk space
- Optional: NVIDIA GPU (12GB+ VRAM)

### Option 1: Local Desktop (Docker Compose)

```bash
# Clone repository
git clone <your-repo-url> ClaudeModel
cd ClaudeModel

# Start all services
docker-compose up -d

# Download AI models
docker exec ai-assistant-ollama ollama pull mistral:7b-instruct

# Access the application
open http://localhost:3000
```

**Time to first response:** ~5 minutes

### Option 2: Production (Kubernetes with GPU)

```bash
# Deploy to Kubernetes cluster
kubectl apply -f k8s/base/

# Deploy GPU-accelerated vLLM
kubectl apply -f k8s/production/vllm-gpu.yaml

# Access via ingress
open https://your-domain.com
```

**See [INSTALLATION_K8S.md](INSTALLATION_K8S.md) for complete production setup.**

---

## 📐 Architecture

### High-Level Overview

```
┌──────────────────────────────────────────────────────────────┐
│                      WEB INTERFACE                           │
│              (React + Monaco Editor + Xterm.js)              │
│              Accessible via HTTP/HTTPS remotely              │
└──────────────────────────────────────────────────────────────┘
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                      API GATEWAY                             │
│              (Kong/Traefik - Rate limiting, Auth)            │
└──────────────────────────────────────────────────────────────┘
                              ▼
        ┌────────────────────┴────────────────────┐
        ▼                    ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────────┐
│  Backend API │    │  Code Agent  │    │ Integration Layer│
│   (FastAPI)  │    │   (Tools)    │    │  (Connectors)    │
└──────────────┘    └──────────────┘    └──────────────────┘
        │                    │                     │
        ▼                    ▼                     ▼
┌──────────────────────────────────────────────────────────────┐
│                    LLM INFERENCE LAYER                       │
│   vLLM (CodeLlama 34B) | Ollama (Mistral) | NHS Model       │
└──────────────────────────────────────────────────────────────┘
        │                    │                     │
        ▼                    ▼                     ▼
┌──────────────────────────────────────────────────────────────┐
│                    STORAGE & DATABASES                       │
│  PostgreSQL | Redis | Qdrant (Vector) | MinIO (S3)          │
└──────────────────────────────────────────────────────────────┘
                              ▼
┌──────────────────────────────────────────────────────────────┐
│            ENTERPRISE INTEGRATIONS (Production)              │
│  GitHub | SharePoint | Confluence | Oracle | SQL | FHIR     │
└──────────────────────────────────────────────────────────────┘
```

### C4 Architecture Diagrams

We provide comprehensive **C4 model diagrams** in PlantUML format:

1. **[architecture-c4-context.puml](architecture-c4-context.puml)** - System Context
   - Shows external actors and systems
   - Enterprise integrations (GitHub, SharePoint, Confluence, databases)

2. **[architecture-c4-container.puml](architecture-c4-container.puml)** - Container View
   - Internal services and data stores
   - Communication patterns

3. **[architecture-c4-component-integration.puml](architecture-c4-component-integration.puml)** - Integration Layer
   - Pluggable connector architecture
   - Circuit breaker, rate limiting, auth

4. **[architecture-c4-component-backend.puml](architecture-c4-component-backend.puml)** - Backend API
   - Request flow and processing
   - Tool orchestration

5. **[architecture-local.puml](architecture-local.puml)** - Local Desktop Architecture

6. **[architecture-production.puml](architecture-production.puml)** - Production GPU Architecture

**View diagrams:** Use [PlantText](https://www.planttext.com/) or [PlantUML Server](http://www.plantuml.com/plantuml/uml/)

---

## 🌐 Web Interface - Beautiful & Remote Accessible

### Features

- 🎨 **Modern Dark Theme** - VS Code-inspired design
- 💬 **Real-time Chat** - Streaming LLM responses
- 📝 **Code Editor** - Monaco Editor (VS Code's editor)
- 🖥️ **Terminal** - Xterm.js for command output
- 📁 **File Browser** - Navigate and edit project files
- 🔍 **Search** - Find code and documents
- 📊 **Tool Panel** - Quick access to Read, Write, Bash, Grep
- 🌓 **Responsive** - Works on desktop, tablet, mobile

### Accessing Remotely

#### From Your Laptop → Desktop

**Option 1: SSH Tunnel (Secure)**
```bash
ssh -L 3000:localhost:3000 -L 8000:localhost:8000 user@desktop-ip
# Access: http://localhost:3000
```

**Option 2: Tailscale (Easiest)**
```bash
# Install on both laptop and desktop
# Access: http://<tailscale-ip>:3000
```

**Option 3: Ngrok (Public URL for demos)**
```bash
ngrok http 3000
# Get public URL: https://abc123.ngrok.io
```

**See [REMOTE_ACCESS.md](REMOTE_ACCESS.md) for complete guide with all options.**

### UI Preview

The interface includes:
- **Chat Panel** - Left side, conversation history
- **Code Editor** - Center, Monaco editor with syntax highlighting
- **Terminal** - Bottom, command execution output
- **File Tree** - Left sidebar, project navigation
- **Tool Buttons** - Top toolbar, quick actions

---

## 📚 Complete Documentation

### 📘 Installation & Setup
| Guide | Description | For |
|-------|-------------|-----|
| **[INSTALLATION_LOCAL.md](INSTALLATION_LOCAL.md)** | Docker Compose setup for local development | Desktop users |
| **[INSTALLATION_K8S.md](INSTALLATION_K8S.md)** | Kubernetes deployment (local + production) | DevOps/Production |
| **[REMOTE_ACCESS.md](REMOTE_ACCESS.md)** | Access desktop from laptop (5 methods) | Remote users |

### 📗 Specialized Guides
| Guide | Description | For |
|-------|-------------|-----|
| **[NHS_FINETUNING.md](NHS_FINETUNING.md)** | Fine-tune LLMs on healthcare data | NHS/Medical teams |
| **[TECH_STACK.md](TECH_STACK.md)** | Complete technology stack details | Developers |

### 📐 Architecture Diagrams
| Diagram | Type | Description |
|---------|------|-------------|
| [architecture-local.puml](architecture-local.puml) | System | Local Docker/K8s |
| [architecture-production.puml](architecture-production.puml) | System | Production GPU |
| [architecture-c4-context.puml](architecture-c4-context.puml) | C4 Level 1 | System Context |
| [architecture-c4-container.puml](architecture-c4-container.puml) | C4 Level 2 | Containers |
| [architecture-c4-component-integration.puml](architecture-c4-component-integration.puml) | C4 Level 3 | Integration Layer |
| [architecture-c4-component-backend.puml](architecture-c4-component-backend.puml) | C4 Level 3 | Backend API |

---

## 🔧 Technology Stack

### **Frontend**
- React 18 + TypeScript
- Monaco Editor (VS Code component)
- Xterm.js (Terminal)
- Tailwind CSS
- Zustand (State)
- React Query (Data fetching)

### **Backend**
- FastAPI (Python)
- LangChain (RAG)
- vLLM (Production) / Ollama (Local)
- PostgreSQL 16
- Redis 7
- Qdrant (Vector DB)

### **LLM Models** (All Open Source)
- CodeLlama 34B Instruct
- DeepSeek Coder 33B
- Mistral 7B Instruct
- Mixtral 8x7B
- StarCoder2 15B

### **Enterprise Integrations**
- **GitHub**: PyGithub, GraphQL API
- **SharePoint**: Microsoft Graph API (msal)
- **Confluence**: Atlassian REST API
- **Oracle**: cx_Oracle
- **SQL Server**: pyodbc
- **FHIR**: fhirclient (Epic EHR)
- **MCP**: Model Context Protocol

### **Infrastructure**
- Docker & Docker Compose
- Kubernetes
- NGINX Ingress
- Prometheus + Grafana
- NVIDIA GPU Operator

**💰 Cost: $0 (all open source!)**

---

## 💻 System Requirements

### Local Development (Desktop)

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | 8 cores (i7/Ryzen 7) | 16 cores |
| **RAM** | 32GB | 64GB |
| **Storage** | 200GB SSD | 500GB NVMe |
| **GPU** | Optional (RTX 3060 12GB) | RTX 4090 24GB |
| **OS** | Windows 10/11, Ubuntu 20.04+, macOS 12+ | Any |

### Production (Nutonics GPU Cluster)

| Component | Specification |
|-----------|---------------|
| **GPU Nodes** | 3-6 nodes, NVIDIA A100 40GB/80GB or H100 80GB |
| **CPU per Node** | 32+ cores (AMD EPYC / Intel Xeon) |
| **RAM per Node** | 256GB |
| **Storage** | 2TB NVMe (models) + 10TB SSD (data) |
| **Network** | 100Gbps interconnect |
| **Additional** | 3 storage nodes, 5+ CPU worker nodes, 3 control plane |

---

## 🎓 Getting Started

### Step 1: Deploy Locally (5 minutes)

```bash
# Clone repository
git clone <repo-url> ClaudeModel
cd ClaudeModel

# Start services
docker-compose up -d

# Check status
docker-compose ps

# Download AI model
docker exec ai-assistant-ollama ollama pull mistral:7b-instruct

# Access UI
open http://localhost:3000
```

### Step 2: Test the System

Open browser at `http://localhost:3000`

**Example conversation:**
```
You: Hello! Can you help me write a Python function?