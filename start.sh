#!/bin/bash

echo "啟動 特殊選才備審分析系統 專案..."
echo

echo "啟動 MySQL 和後端服務..."
docker-compose up -d mysql backend

echo "等待服務啟動..."
sleep 15

echo "初始化資料庫..."
cd backend
python init_database.py
cd ..

echo "啟動前端服務..."
cd frontend
npm run dev &

echo
echo "專案已啟動！"
echo "前端: http://localhost:3000 (生產環境: https://morago.com.tw)"
echo "後端 API: http://localhost:8000 (生產環境: https://api.morago.com.tw)"
echo "API 文檔: http://localhost:8000/docs"
echo
echo "資料庫資訊:"
echo "  資料庫名稱: hhkone_resourceschool"
echo "  用戶名稱: hhkone_resourceschool"
echo "  密碼: C7W7sTvpuwrWQ2v2GV28"
echo
