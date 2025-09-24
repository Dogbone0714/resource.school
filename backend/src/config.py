import os
from datetime import timedelta

# 資料庫配置
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:0h96Laxmn4Q57N2XBj8oepU1ysO3ErCT@cgk1.clusters.zeabur.com:32188/zeabur")

# JWT 配置
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60  # 24 小時

# 上傳配置
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_FILE_TYPES = [".json"]

# CORS 配置
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://frontend:3000", 
    os.getenv("FRONTEND_URL", "https://resouceschool.zeabur.app")
]

# 應用程式配置
APP_NAME = "Resource School API"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "特殊選才備審分析系統 API"
