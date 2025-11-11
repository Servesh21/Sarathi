@echo off
REM Startup script for Sarathi FastAPI backend

echo Starting Sarathi FastAPI Server...
echo.

cd /d "%~dp0"

set PYTHONPATH=.

C:\Python313\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

pause
