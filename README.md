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
├── frontend/                    # React 前端專案
│   ├── src/
│   │   ├── pages/              # 頁面組件
│   │   │   ├── LoginPage.jsx   # 登入頁面
│   │   │   ├── UploadPage.jsx  # 上傳頁面
│   │   │   └── ResultPage.jsx  # 結果頁面
│   │   ├── components/         # 共用組件
│   │   ├── services/           # API 服務
│   │   └── App.tsx            # 主應用程式
│   └── public/
│       └── sample-data.json   # 示例資料
├── backend/                    # FastAPI 後端專案
│   ├── src/                   # 源碼目錄
│   │   ├── controllers/       # 控制器
│   │   ├── models/           # 資料庫模型
│   │   ├── routes/           # 路由
│   │   ├── services/         # 服務層
│   │   ├── config.py         # 配置檔案
│   │   └── main.py          # 主應用程式
│   ├── ai.py                 # AI 推薦模組
│   ├── main.py              # 向後兼容入口
│   └── requirements.txt     # Python 依賴
├── docker-compose.yml         # Docker 容器配置
└── README.md                 # 專案說明
```

## 快速開始

### 使用 Docker (推薦)
```bash
docker-compose up -d
```

### 資料庫配置
- **資料庫名稱**: `hhkone_resourceschool`
- **用戶名稱**: `hhkone_resourceschool`
- **密碼**: `***`

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
- **前端網域**: https://resouceschool.zeabur.app
- **API 網域**: https://resouceschool.zeabur.app
- **本地開發**: 
  - 前端: http://localhost:3000
  - 後端: http://localhost:8000

## 功能特色

### 前端功能
- 🔐 **用戶認證**: 登入/登出功能
- 📤 **檔案上傳**: 支援 JSON 格式的備審資料上傳
- 📊 **結果展示**: 顯示學系推薦結果和分析
- 🎨 **響應式設計**: 使用 TailwindCSS 的現代化 UI
- 🛡️ **路由保護**: 需要登入才能訪問上傳和結果頁面

### 後端功能
- 🔑 **JWT 認證**: 安全的用戶認證機制
- 📁 **檔案處理**: 支援 JSON 檔案上傳和解析
- 🤖 **推薦系統**: 基於上傳資料的學系推薦（目前為模擬數據）
- 🗄️ **資料庫**: MySQL 儲存用戶、上傳記錄和推薦結果
- 📚 **API 文檔**: 自動生成的 Swagger 文檔

## API 端點

### 認證
- `POST /api/auth/register` - 用戶註冊
- `POST /api/auth/login` - 用戶登入
- `GET /api/auth/me` - 獲取當前用戶資訊

### 上傳
- `POST /api/upload` - 上傳備審資料 JSON
- `GET /api/uploads` - 獲取用戶上傳記錄

### 推薦
- `GET /api/recommendation/{userId}` - 獲取學系推薦結果
- `GET /api/recommendation/me/latest` - 獲取最新推薦結果

### 資源管理
- `GET /resources` - 獲取資源列表
- `POST /resources` - 建立新資源
- `PUT /resources/{id}` - 更新資源
- `DELETE /resources/{id}` - 刪除資源

## API 文檔
後端啟動後，可訪問 http://localhost:8000/docs 查看 API 文檔
