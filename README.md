# Resource School 專案

這是一個前後端分離的專案，包含：

## 前端 (Frontend)
- React 18
- Vite
- TailwindCSS
- TypeScript

## 後端 (Backend)
- FastAPI
- MySQL
- SQLAlchemy
- Pydantic

## 專案結構
```
resource.school/
├── frontend/          # React 前端專案
├── backend/           # FastAPI 後端專案
├── docker-compose.yml # Docker 容器配置
└── README.md         # 專案說明
```

## 快速開始

### 使用 Docker (推薦)
```bash
docker-compose up -d
```

### 手動啟動

#### 後端
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

#### 前端
```bash
cd frontend
npm install
npm run dev
```

## 網域配置
- **前端網域**: https://morago.com.tw
- **API 網域**: https://api.morago.com.tw
- **本地開發**: 
  - 前端: http://localhost:3000
  - 後端: http://localhost:8000

## API 文檔
後端啟動後，可訪問 http://localhost:8000/docs 查看 API 文檔
