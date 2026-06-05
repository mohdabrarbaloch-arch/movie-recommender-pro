@echo off
title MovieBox Server
cd /d "C:\Users\SMIT 123\Desktop\Painding_Projects\recommendation_system"
echo Starting Backend...
start "Backend" cmd /c "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
echo Starting Frontend...
cd /d "C:\Users\SMIT 123\Desktop\Painding_Projects\recommendation_system\frontend"
start "Frontend" cmd /c "npm start"
echo.
echo Both servers started! Close this window to keep them running.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
pause
