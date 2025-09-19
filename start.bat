@echo off
echo 啟動 Resource School 專案...
echo.

echo 啟動 MySQL 和後端服務...
docker-compose up -d mysql backend

echo 等待服務啟動...
timeout /t 10 /nobreak > nul

echo 啟動前端服務...
cd frontend
start cmd /k "npm run dev"

echo.
echo 專案已啟動！
echo 前端: http://localhost:3000 (生產環境: https://morago.com.tw)
echo 後端 API: http://localhost:8000 (生產環境: https://api.morago.com.tw)
echo API 文檔: http://localhost:8000/docs
echo.
pause
