from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import APP_NAME, APP_VERSION, APP_DESCRIPTION, ALLOWED_ORIGINS
from .routes import main_router
from .models.database import engine, Base

# 建立資料表
Base.metadata.create_all(bind=engine)

# 創建 FastAPI 應用程式
app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 根路由
@app.get("/")
async def root():
    return {
        "message": "歡迎使用 特殊選才備審分析系統 API",
        "version": APP_VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": APP_NAME,
        "version": APP_VERSION
    }

# 包含所有路由
app.include_router(main_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
