@echo off
echo Building Vue.js frontend...
cd portal-frontend-vue
call npm run build
if %ERRORLEVEL% neq 0 (
    echo Frontend build failed!
    exit /b 1
)

echo Frontend build successful!
cd ..

echo Building and starting Docker containers...
docker compose down
docker compose up --build -d

echo Checking container status...
docker compose ps

echo Application should be available at http://localhost:8000
echo Use 'docker compose logs app' to view logs
