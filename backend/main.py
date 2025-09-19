from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List, Optional
import os
import json
import jwt
import hashlib
from sqlalchemy.orm import Session

# 資料庫配置
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://appuser:apppassword@localhost:3306/resource_school")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 資料庫模型
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Resource(Base):
    __tablename__ = "resources"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Upload(Base):
    __tablename__ = "uploads"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    data = Column(Text)  # JSON 資料
    created_at = Column(DateTime, default=datetime.utcnow)

class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    department = Column(String(255), nullable=False)
    university = Column(String(255))
    major = Column(String(255))
    score = Column(Float)
    reason = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# JWT 配置
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"

# Pydantic 模型
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str
    user: dict

class ResourceCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    url: Optional[str] = None

class ResourceResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UploadResponse(BaseModel):
    message: str
    upload_id: int

class RecommendationResponse(BaseModel):
    id: int
    department: str
    university: Optional[str] = None
    major: Optional[str] = None
    score: Optional[float] = None
    reason: Optional[str] = None
    
    class Config:
        from_attributes = True

# 建立資料表
Base.metadata.create_all(bind=engine)

# FastAPI 應用程式
app = FastAPI(
    title="Resource School API",
    description="資源管理系統 API",
    version="1.0.0"
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://frontend:3000",
        "https://morago.com.tw",
        "https://www.morago.com.tw"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 認證相關函數
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# 依賴注入
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db), username: str = Depends(verify_token)):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# API 端點
@app.get("/")
async def root():
    return {"message": "歡迎使用 Resource School API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# 認證端點
@app.post("/api/auth/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    # 檢查用戶是否存在
    user = db.query(User).filter(User.username == login_data.username).first()
    
    if not user:
        # 如果用戶不存在，創建新用戶（簡化處理）
        hashed_password = hash_password(login_data.password)
        user = User(username=login_data.username, password_hash=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # 驗證密碼
        if not verify_password(login_data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # 創建 JWT token
    access_token = create_access_token(data={"sub": user.username})
    
    return {
        "token": access_token,
        "user": {
            "id": user.id,
            "username": user.username
        }
    }

# 上傳端點
@app.post("/api/upload", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith('.json'):
        raise HTTPException(status_code=400, detail="Only JSON files are allowed")
    
    # 讀取檔案內容
    content = await file.read()
    try:
        json_data = json.loads(content.decode('utf-8'))
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    
    # 儲存上傳記錄
    upload = Upload(
        user_id=current_user.id,
        filename=file.filename,
        file_path=f"uploads/{file.filename}",
        data=json.dumps(json_data, ensure_ascii=False)
    )
    db.add(upload)
    db.commit()
    db.refresh(upload)
    
    # 模擬推薦分析（這裡可以加入實際的 AI 分析邏輯）
    recommendations = generate_mock_recommendations(json_data)
    
    # 儲存推薦結果
    for rec in recommendations:
        recommendation = Recommendation(
            user_id=current_user.id,
            department=rec["department"],
            university=rec.get("university"),
            major=rec.get("major"),
            score=rec.get("score"),
            reason=rec.get("reason")
        )
        db.add(recommendation)
    
    db.commit()
    
    return {
        "message": "File uploaded successfully",
        "upload_id": upload.id
    }

# 推薦端點
@app.get("/api/recommendation/{user_id}", response_model=List[RecommendationResponse])
async def get_recommendation(user_id: int, db: Session = Depends(get_db)):
    recommendations = db.query(Recommendation).filter(
        Recommendation.user_id == user_id
    ).order_by(Recommendation.score.desc()).all()
    
    return recommendations

def generate_mock_recommendations(data):
    """生成模擬推薦結果"""
    mock_recommendations = [
        {
            "department": "資訊工程學系",
            "university": "國立台灣大學",
            "major": "軟體工程",
            "score": 0.95,
            "reason": "根據您的成績和興趣，非常適合資訊工程領域"
        },
        {
            "department": "電機工程學系",
            "university": "國立清華大學",
            "major": "人工智慧",
            "score": 0.88,
            "reason": "您的數學和物理成績優秀，適合電機工程"
        },
        {
            "department": "商業管理學系",
            "university": "國立政治大學",
            "major": "企業管理",
            "score": 0.82,
            "reason": "您的領導能力和溝通技巧適合商管領域"
        }
    ]
    return mock_recommendations

@app.get("/resources", response_model=List[ResourceResponse])
async def get_resources(skip: int = 0, limit: int = 100):
    db = next(get_db())
    resources = db.query(Resource).offset(skip).limit(limit).all()
    return resources

@app.get("/resources/{resource_id}", response_model=ResourceResponse)
async def get_resource(resource_id: int):
    db = next(get_db())
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if resource is None:
        raise HTTPException(status_code=404, detail="資源不存在")
    return resource

@app.post("/resources", response_model=ResourceResponse)
async def create_resource(resource: ResourceCreate):
    db = next(get_db())
    db_resource = Resource(**resource.dict())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

@app.put("/resources/{resource_id}", response_model=ResourceResponse)
async def update_resource(resource_id: int, resource: ResourceCreate):
    db = next(get_db())
    db_resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if db_resource is None:
        raise HTTPException(status_code=404, detail="資源不存在")
    
    for key, value in resource.dict().items():
        setattr(db_resource, key, value)
    
    db.commit()
    db.refresh(db_resource)
    return db_resource

@app.delete("/resources/{resource_id}")
async def delete_resource(resource_id: int):
    db = next(get_db())
    db_resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if db_resource is None:
        raise HTTPException(status_code=404, detail="資源不存在")
    
    db.delete(db_resource)
    db.commit()
    return {"message": "資源已刪除"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
