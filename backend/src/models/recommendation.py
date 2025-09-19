from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    upload_id = Column(Integer, ForeignKey("uploads.id"), nullable=True)
    department = Column(String(255), nullable=False)
    university = Column(String(255))
    major = Column(String(255))
    score = Column(Float, nullable=False)
    reason = Column(Text)
    rank = Column(Integer, nullable=True)  # 推薦排名
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 關聯
    user = relationship("User", back_populates="recommendations")
