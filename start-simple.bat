@echo off
echo ============================================
echo AI Coding Assistant - Simple Startup
echo ============================================
echo.

echo Step 1: Starting core services (databases, LLM)...
docker-compose -f docker-compose-simple.yml up -d

echo.
echo Step 2: Waiting for services to be ready...
timeout /t 30 /nobreak

echo.
echo Step 3: Checking service status...
docker-compose -f docker-compose-simple.yml ps

echo.
echo ============================================
echo Next Steps:
echo ============================================
echo 1. Download AI model:
echo    docker exec ai-assistant-ollama ollama pull mistral:7b-instruct
echo.
echo 2. Test Ollama:
echo    curl http://localhost:11434/api/tags
echo.
echo 3. Access services:
echo    - PostgreSQL: localhost:5432
echo    - Redis: localhost:6379
echo    - Qdrant: http://localhost:6333/dashboard
echo    - MinIO: http://localhost:9001 (admin/minioadmin123)
echo    - Ollama: http://localhost:11434
echo.
echo ============================================
pause
