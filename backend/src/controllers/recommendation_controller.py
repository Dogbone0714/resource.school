from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..models.schemas import RecommendationListResponse
from ..services.auth_service import AuthService
from ..services.recommendation_service import RecommendationService

recommendation_router = APIRouter(prefix="/api", tags=["推薦"])
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """獲取當前用戶"""
    username = AuthService.verify_token(credentials.credentials)
    return AuthService.get_user_by_username(db, username)

@recommendation_router.get("/recommendation/{user_id}", response_model=RecommendationListResponse)
async def get_recommendation(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """獲取學系推薦結果"""
    try:
        # 檢查用戶權限
        if current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this user's recommendations"
            )
        
        recommendations = RecommendationService.get_user_recommendations(
            db, user_id, skip, limit
        )
        
        return recommendations
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get recommendations: {str(e)}"
        )

@recommendation_router.get("/recommendation/me/latest")
async def get_my_latest_recommendations(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """獲取當前用戶的最新推薦結果"""
    try:
        recommendations = RecommendationService.get_latest_recommendations(
            db, current_user.id
        )
        
        return {
            "recommendations": recommendations,
            "total": len(recommendations),
            "user_id": current_user.id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get latest recommendations: {str(e)}"
        )
