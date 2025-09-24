from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class PDFUpload(Base):
    __tablename__ = "pdf_uploads"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=True)
    raw_text = Column(Text, nullable=True)  # 提取的原始文字
    processed_data = Column(Text, nullable=True)  # 處理後的 JSON 資料
    status = Column(String(20), default="uploaded", nullable=False)  # uploaded, processing, completed, failed
    processing_time = Column(Float, nullable=True)  # 處理時間（秒）
    page_count = Column(Integer, nullable=True)  # PDF 頁數
    word_count = Column(Integer, nullable=True)  # 文字字數
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 關聯
    user = relationship("User", back_populates="pdf_uploads")
    recommendations = relationship("Recommendation", back_populates="pdf_upload")

class PDFAnalysis(Base):
    __tablename__ = "pdf_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    pdf_upload_id = Column(Integer, ForeignKey("pdf_uploads.id"), nullable=False)
    analysis_type = Column(String(50), nullable=False)  # academic_scores, interests, achievements, etc.
    analysis_data = Column(Text, nullable=False)  # JSON 格式的分析結果
    confidence_score = Column(Float, nullable=True)  # 分析信心分數
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 關聯
    pdf_upload = relationship("PDFUpload")
