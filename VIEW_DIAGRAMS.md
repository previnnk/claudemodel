# How to View Architecture Diagrams

## 📐 PlantUML Diagrams in This Project

All architecture diagrams are in **PlantUML format** (`.puml` files).

---

## 🖼️ Method 1: Online Viewer (Easiest)

### PlantText (Recommended)
1. Go to: https://www.planttext.com/
2. Copy the contents of any `.puml` file
3. Paste into the text area
4. Click **"Refresh"**
5. View/download the diagram

### PlantUML Server
1. Go to: http://www.plantuml.com/plantuml/uml/
2. Paste the PlantUML code
3. View the rendered diagram

---

## 💻 Method 2: VS Code Extension

### Install PlantUML Extension
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for **"PlantUML"**
4. Install by **jebbs**

### View Diagrams
1. Open any `.puml` file
2. Press **Alt+D** (or Ctrl+Shift+P → "PlantUML: Preview Current Diagram")
3. Diagram renders in preview pane

### Export
- Right-click on `.puml` file
- Select **"PlantUML: Export Current Diagram"**
- Choose format (PNG, SVG, PDF)

---

## 🖥️ Method 3: Local PlantUML Installation

### Install PlantUML
```bash
# Install Java (required)
# Download plantuml.jar from https://plantuml.com/download

# Or use Chocolatey (Windows)
choco install plantuml

# Or use Homebrew (Mac)
brew install plantuml
```

### Generate Diagrams
```bash
# Generate PNG
java -jar plantuml.jar architecture-local.puml

# Generate SVG (scalable)
java -jar plantuml.jar -tsvg architecture-local.puml

# Generate all diagrams
java -jar plantuml.jar *.puml
```

---

## 📁 Available Diagrams

### System Architecture
| File | Description | View Priority |
|------|-------------|---------------|
| **architecture-local.puml** | Local Docker/K8s setup | ⭐⭐⭐ Start here |
| **architecture-production.puml** | Production GPU cluster | ⭐⭐⭐ For deployment |

### C4 Model Diagrams
| File | Level | Description |
|------|-------|-------------|
| **architecture-c4-context.puml** | Level 1 | System context & integrations |
| **architecture-c4-container.puml** | Level 2 | Containers & services |
| **architecture-c4-component-integration.puml** | Level 3 | Integration layer details |
| **architecture-c4-component-backend.puml** | Level 3 | Backend API details |

---

## 🎨 Quick View Guide

### For Local Desktop Setup
1. **Start with**: `architecture-local.puml`
2. Shows: Docker Compose services, data flow, remote access options
3. **Use case**: Understanding local deployment

### For Production Deployment
1. **Start with**: `architecture-production.puml`
2. Shows: Kubernetes cluster, GPU nodes, HA setup
3. **Use case**: Planning Nutonics deployment

### For Enterprise Integrations
1. **Start with**: `architecture-c4-context.puml` (big picture)
2. **Then**: `architecture-c4-component-integration.puml` (details)
3. Shows: SharePoint, GitHub, Confluence, database connectors
4. **Use case**: Understanding integration architecture

---

## 🔍 What Each Diagram Shows

### architecture-local.puml
```
- Web Browser (laptop)
- SSH Tunnel / VPN
- Docker containers:
  * Frontend (React)
  * Backend (FastAPI)
  * Ollama (LLM)
  * PostgreSQL, Redis, Qdrant, MinIO
- Resource requirements
- Remote access methods
```

### architecture-production.puml
```
- Kubernetes cluster structure
- GPU nodes (vLLM inference)
- Load balancer & ingress
- High availability setup
- Enterprise integrations
- Monitoring stack
- Backup strategy
```

### architecture-c4-context.puml
```
- External systems (GitHub, SharePoint, etc.)
- User types (developers, NHS staff, admins)
- System boundaries
- Data flows
- MCP protocol
```

### architecture-c4-container.puml
```
- All microservices
- Databases & storage
- Communication patterns
- Integration layer
- LLM router
```

---

## 📸 Export High-Quality Images

### For Presentations
```bash
# Export as SVG (best quality, scalable)
java -jar plantuml.jar -tsvg architecture-production.puml

# Export as PNG (300 DPI)
java -jar plantuml.jar -DPPI=300 architecture-production.puml
```

### For Documentation
```bash
# Export all diagrams as PNG
java -jar plantuml.jar -tpng *.puml

# Creates: architecture-local.png, architecture-production.png, etc.
```

---

## 🛠️ Troubleshooting

### "Diagram not rendering"
- Check for syntax errors in `.puml` file
- Ensure PlantUML server is accessible
- Try a different viewer

### "Fonts look bad"
- Use SVG format instead of PNG
- Increase DPI for PNG export

### "Diagram too large"
- PlantUML auto-sizes diagrams
- Use SVG and zoom in your viewer
- Or split into multiple diagrams

---

## 💡 Tips

1. **Start Simple**: View `architecture-local.puml` first
2. **Use SVG**: Best quality for presentations
3. **VS Code**: Best for quick edits and preview
4. **Export All**: Generate PNGs for easy sharing

---

## 🚀 Quick Start

**Fastest way to view ALL diagrams:**

1. Go to: https://www.planttext.com/
2. Open `architecture-local.puml` in notepad
3. Copy all contents
4. Paste into PlantText
5. Click "Refresh"
6. Repeat for other diagrams

**Or use this script:**

```bash
# view_diagrams.bat (Windows)
@echo off
echo Opening PlantText in browser...
start https://www.planttext.com/
echo.
echo Copy contents from:
dir *.puml /b
echo.
echo Paste into the browser and click Refresh
pause
```

---

## 📋 Diagram Checklist

Before deployment, review these diagrams:

- [ ] `architecture-local.puml` - Understand local setup
- [ ] `architecture-production.puml` - Understand production setup
- [ ] `architecture-c4-context.puml` - Verify all integrations shown
- [ ] `architecture-c4-container.puml` - Verify all services shown
- [ ] Export to PNG/SVG for documentation

---

## 🔗 Helpful Links

- PlantUML Official: https://plantuml.com/
- PlantText Viewer: https://www.planttext.com/
- C4 Model: https://c4model.com/
- VS Code Extension: https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml

---

**Next**: After viewing diagrams, proceed to deployment guides:
- Local: `INSTALLATION_LOCAL.md`
- Production: `INSTALLATION_K8S.md`
