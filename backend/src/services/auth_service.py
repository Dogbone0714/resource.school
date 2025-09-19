import hashlib
import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.user import User
from ..models.schemas import UserCreate, LoginRequest, UserResponse
from ..config import SECRET_KEY, ALGORITHM

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        """密碼雜湊"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """驗證密碼"""
        return AuthService.hash_password(plain_password) == hashed_password
    
    @staticmethod
    def create_access_token(data: dict) -> str:
        """創建 JWT Token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(hours=24)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> str:
        """驗證 JWT Token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return username
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
    
    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        """用戶註冊"""
        # 檢查用戶名是否已存在
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        # 檢查郵箱是否已存在
        if user_data.email:
            existing_email = db.query(User).filter(User.email == user_data.email).first()
            if existing_email:
                raise HTTPException(status_code=400, detail="Email already registered")
        
        # 創建新用戶
        hashed_password = AuthService.hash_password(user_data.password)
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password,
            full_name=user_data.full_name
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def authenticate_user(db: Session, login_data: LoginRequest) -> User:
        """用戶認證"""
        user = db.query(User).filter(User.username == login_data.username).first()
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if not AuthService.verify_password(login_data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if user.is_active != "Y":
            raise HTTPException(status_code=401, detail="User account is disabled")
        
        return user
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        """根據用戶名獲取用戶"""
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
