from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import os

# 資料庫配置
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://appuser:apppassword@localhost:3306/resource_school")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 資料庫模型
class Resource(Base):
    __tablename__ = "resources"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Pydantic 模型
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

# 依賴注入
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API 端點
@app.get("/")
async def root():
    return {"message": "歡迎使用 Resource School API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

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
