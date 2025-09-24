"""
PDF 上傳控制器
處理 PDF 檔案上傳相關的 API 端點
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List
from ..models.database import get_db
from ..models.schemas import PDFUploadResponse, PDFUploadInfo
from ..services.auth_service import AuthService
from ..services.pdf_service import PDFService

pdf_router = APIRouter(prefix="/api", tags=["PDF 上傳"])
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """獲取當前用戶"""
    username = AuthService.verify_token(credentials.credentials)
    return AuthService.get_user_by_username(db, username)

@pdf_router.post("/upload/pdf", response_model=PDFUploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """上傳 PDF 備審資料"""
    try:
        result = PDFService.process_pdf_upload(db, file, current_user.id)
        return PDFUploadResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"PDF 上傳失敗: {str(e)}"
        )

@pdf_router.get("/pdf-uploads", response_model=List[PDFUploadInfo])
async def get_user_pdf_uploads(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """獲取用戶的 PDF 上傳記錄"""
    try:
        uploads = PDFService.get_user_pdf_uploads(db, current_user.id, skip, limit)
        return [PDFUploadInfo(
            id=upload.id,
            filename=upload.filename,
            file_size=upload.file_size,
            page_count=upload.page_count,
            word_count=upload.word_count,
            status=upload.status,
            processing_time=upload.processing_time,
            created_at=upload.created_at
        ) for upload in uploads]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"獲取 PDF 上傳記錄失敗: {str(e)}"
        )

@pdf_router.get("/pdf-uploads/{upload_id}")
async def get_pdf_upload_detail(
    upload_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """獲取特定 PDF 上傳的詳細資訊"""
    try:
        upload = PDFService.get_pdf_upload_by_id(db, upload_id, current_user.id)
        
        if not upload:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="PDF 上傳記錄不存在"
            )
        
        # 解析處理後的資料
        analysis_result = None
        if upload.processed_data:
            import json
            analysis_result = json.loads(upload.processed_data)
        
        return {
            "id": upload.id,
            "filename": upload.filename,
            "file_size": upload.file_size,
            "page_count": upload.page_count,
            "word_count": upload.word_count,
            "status": upload.status,
            "processing_time": upload.processing_time,
            "created_at": upload.created_at,
            "analysis_result": analysis_result,
            "raw_text_preview": upload.raw_text[:500] + "..." if upload.raw_text and len(upload.raw_text) > 500 else upload.raw_text
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"獲取 PDF 詳細資訊失敗: {str(e)}"
        )

@pdf_router.delete("/pdf-uploads/{upload_id}")
async def delete_pdf_upload(
    upload_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """刪除 PDF 上傳記錄"""
    try:
        upload = PDFService.get_pdf_upload_by_id(db, upload_id, current_user.id)
        
        if not upload:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="PDF 上傳記錄不存在"
            )
        
        # 刪除檔案
        import os
        if os.path.exists(upload.file_path):
            os.remove(upload.file_path)
        
        # 刪除資料庫記錄
        db.delete(upload)
        db.commit()
        
        return {"message": "PDF 上傳記錄已刪除"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"刪除 PDF 上傳記錄失敗: {str(e)}"
        )
