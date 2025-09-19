from sqlalchemy.orm import Session
from typing import List
from ..models.recommendation import Recommendation
from ..models.user import User
from ..models.schemas import RecommendationResponse, RecommendationListResponse
from .ai_service import AIService

class RecommendationService:
    @staticmethod
    def generate_recommendations(
        db: Session, 
        user_id: int, 
        upload_id: int, 
        json_data: dict
    ) -> List[Recommendation]:
        """生成學系推薦"""
        # 使用 AI 服務分析資料
        ai_recommendations = AIService.analyze_student_data(json_data)
        
        # 儲存推薦結果到資料庫
        recommendations = []
        for i, rec_data in enumerate(ai_recommendations):
            recommendation = Recommendation(
                user_id=user_id,
                upload_id=upload_id,
                department=rec_data["department"],
                university=rec_data.get("university"),
                major=rec_data.get("major"),
                score=rec_data["score"],
                reason=rec_data.get("reason"),
                rank=i + 1
            )
            db.add(recommendation)
            recommendations.append(recommendation)
        
        db.commit()
        
        # 刷新所有推薦記錄以獲取 ID
        for rec in recommendations:
            db.refresh(rec)
        
        return recommendations
    
    @staticmethod
    def get_user_recommendations(
        db: Session, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> RecommendationListResponse:
        """獲取用戶推薦結果"""
        # 獲取推薦記錄
        recommendations = db.query(Recommendation).filter(
            Recommendation.user_id == user_id
        ).order_by(Recommendation.score.desc()).offset(skip).limit(limit).all()
        
        # 轉換為響應格式
        rec_responses = [
            RecommendationResponse(
                id=rec.id,
                department=rec.department,
                university=rec.university,
                major=rec.major,
                score=rec.score,
                reason=rec.reason,
                rank=rec.rank,
                created_at=rec.created_at
            ) for rec in recommendations
        ]
        
        # 獲取總數
        total = db.query(Recommendation).filter(
            Recommendation.user_id == user_id
        ).count()
        
        return RecommendationListResponse(
            recommendations=rec_responses,
            total=total,
            user_id=user_id
        )
    
    @staticmethod
    def get_latest_recommendations(
        db: Session, 
        user_id: int
    ) -> List[Recommendation]:
        """獲取用戶最新的推薦結果"""
        # 獲取最新的上傳記錄
        latest_upload = db.query(Upload).filter(
            Upload.user_id == user_id
        ).order_by(Upload.created_at.desc()).first()
        
        if not latest_upload:
            return []
        
        # 獲取該上傳的推薦結果
        recommendations = db.query(Recommendation).filter(
            Recommendation.user_id == user_id,
            Recommendation.upload_id == latest_upload.id
        ).order_by(Recommendation.score.desc()).all()
        
        return recommendations
