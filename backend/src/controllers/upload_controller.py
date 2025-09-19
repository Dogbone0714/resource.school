from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..models.schemas import UploadResponse
from ..services.auth_service import AuthService
from ..services.upload_service import UploadService
from ..services.recommendation_service import RecommendationService
import json

upload_router = APIRouter(prefix="/api", tags=["上傳"])
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """獲取當前用戶"""
    username = AuthService.verify_token(credentials.credentials)
    return AuthService.get_user_by_username(db, username)

@upload_router.post("/upload", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """上傳備審資料 JSON 檔案"""
    try:
        # 處理檔案上傳
        upload_response = UploadService.process_upload(db, file, current_user)
        
        # 獲取上傳的 JSON 資料
        upload_record = db.query(Upload).filter(Upload.id == upload_response.upload_id).first()
        if upload_record and upload_record.data:
            json_data = json.loads(upload_record.data)
            
            # 生成推薦結果
            RecommendationService.generate_recommendations(
                db, current_user.id, upload_record.id, json_data
            )
        
        return upload_response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )

@upload_router.get("/uploads")
async def get_user_uploads(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """獲取用戶上傳記錄"""
    try:
        uploads = UploadService.get_user_uploads(db, current_user.id, skip, limit)
        return {
            "uploads": uploads,
            "total": len(uploads),
            "user_id": current_user.id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get uploads: {str(e)}"
        )
