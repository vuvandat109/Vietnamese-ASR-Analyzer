@echo off
cd /d "%~dp0"
docker compose up -d --build
if errorlevel 1 goto end
docker compose ps
echo Open http://127.0.0.1:8001/docs
:end
pause
