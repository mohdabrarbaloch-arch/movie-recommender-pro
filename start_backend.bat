@echo off
title MovieBox Backend
cd /d "C:\Users\SMIT 123\Desktop\Painding_Projects\recommendation_system"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
pause
