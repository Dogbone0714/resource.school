from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# 用戶相關 Schema
class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# 認證相關 Schema
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    password: str
    full_name: Optional[str] = None

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# 上傳相關 Schema
class UploadResponse(BaseModel):
    message: str
    upload_id: int
    status: str

# 推薦相關 Schema
class RecommendationResponse(BaseModel):
    id: int
    department: str
    university: Optional[str] = None
    major: Optional[str] = None
    score: float
    reason: Optional[str] = None
    rank: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class RecommendationListResponse(BaseModel):
    recommendations: List[RecommendationResponse]
    total: int
    user_id: int

# 資源相關 Schema
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
