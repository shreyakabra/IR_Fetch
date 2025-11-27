@echo off
echo Starting Backend...
start /B python -m uvicorn backend.main:app --reload --port 8008
echo Starting Frontend (Dev)...
cd frontend
call npm install
start /B npm run dev
cd ..
echo Both services started.
echo Backend API: http://localhost:8008
echo Frontend Dev Server: http://localhost:5173
pause
