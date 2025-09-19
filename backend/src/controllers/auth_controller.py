from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..models.schemas import LoginRequest, RegisterRequest, LoginResponse, UserResponse
from ..services.auth_service import AuthService

auth_router = APIRouter(prefix="/api/auth", tags=["認證"])
security = HTTPBearer()

@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """用戶註冊"""
    try:
        user = AuthService.register_user(db, user_data)
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@auth_router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """用戶登入"""
    try:
        user = AuthService.authenticate_user(db, login_data)
        access_token = AuthService.create_access_token(data={"sub": user.username})
        
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                full_name=user.full_name,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@auth_router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """獲取當前用戶資訊"""
    try:
        username = AuthService.verify_token(credentials.credentials)
        user = AuthService.get_user_by_username(db, username)
        
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user info: {str(e)}"
        )
