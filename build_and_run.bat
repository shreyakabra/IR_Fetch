@echo off
echo Building Frontend...
cd frontend
call npm install
call npm run build
cd ..
echo Starting Backend (serving static files)...
echo Access the app at http://localhost:8008
python -m uvicorn backend.main:app --port 8008
