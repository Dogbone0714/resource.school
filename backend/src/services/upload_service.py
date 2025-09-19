import json
import os
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from ..models.upload import Upload
from ..models.user import User
from ..models.schemas import UploadResponse

class UploadService:
    UPLOAD_DIR = "uploads"
    
    @staticmethod
    def ensure_upload_dir():
        """確保上傳目錄存在"""
        if not os.path.exists(UploadService.UPLOAD_DIR):
            os.makedirs(UploadService.UPLOAD_DIR)
    
    @staticmethod
    def validate_json_file(file: UploadFile) -> dict:
        """驗證並解析 JSON 檔案"""
        if not file.filename.endswith('.json'):
            raise HTTPException(status_code=400, detail="Only JSON files are allowed")
        
        # 讀取檔案內容
        content = file.file.read()
        try:
            json_data = json.loads(content.decode('utf-8'))
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON format: {str(e)}")
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="File encoding error")
        
        # 驗證 JSON 結構
        required_fields = ["personal_info", "academic_scores"]
        for field in required_fields:
            if field not in json_data:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Missing required field: {field}"
                )
        
        return json_data
    
    @staticmethod
    def save_upload_file(file: UploadFile, user_id: int) -> str:
        """儲存上傳檔案"""
        UploadService.ensure_upload_dir()
        
        # 生成唯一檔案名
        timestamp = int(datetime.utcnow().timestamp())
        filename = f"{user_id}_{timestamp}_{file.filename}"
        file_path = os.path.join(UploadService.UPLOAD_DIR, filename)
        
        # 儲存檔案
        with open(file_path, "wb") as buffer:
            file.file.seek(0)  # 重置檔案指標
            buffer.write(file.file.read())
        
        return file_path, filename
    
    @staticmethod
    def create_upload_record(
        db: Session, 
        user_id: int, 
        filename: str, 
        file_path: str, 
        json_data: dict
    ) -> Upload:
        """創建上傳記錄"""
        file_size = os.path.getsize(file_path)
        
        upload = Upload(
            user_id=user_id,
            filename=filename,
            file_path=file_path,
            file_size=file_size,
            data=json.dumps(json_data, ensure_ascii=False),
            status="completed"
        )
        
        db.add(upload)
        db.commit()
        db.refresh(upload)
        return upload
    
    @staticmethod
    def process_upload(
        db: Session, 
        file: UploadFile, 
        current_user: User
    ) -> UploadResponse:
        """處理檔案上傳"""
        # 驗證檔案
        json_data = UploadService.validate_json_file(file)
        
        # 儲存檔案
        file_path, filename = UploadService.save_upload_file(file, current_user.id)
        
        # 創建上傳記錄
        upload = UploadService.create_upload_record(
            db, current_user.id, filename, file_path, json_data
        )
        
        return UploadResponse(
            message="File uploaded successfully",
            upload_id=upload.id,
            status=upload.status
        )
    
    @staticmethod
    def get_user_uploads(db: Session, user_id: int, skip: int = 0, limit: int = 100):
        """獲取用戶上傳記錄"""
        uploads = db.query(Upload).filter(
            Upload.user_id == user_id
        ).offset(skip).limit(limit).all()
        return uploads
