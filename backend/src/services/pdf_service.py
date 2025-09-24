"""
PDF 處理服務
處理 PDF 檔案上傳、解析和文字提取
"""

import os
import json
import time
from typing import Dict, Any, Optional, Tuple
from fastapi import UploadFile, HTTPException
import PyPDF2
import pdfplumber
from sqlalchemy.orm import Session
from ..models.pdf_upload import PDFUpload, PDFAnalysis
from ..models.user import User
from .ai_standalone import analyze_student_data

class PDFService:
    """PDF 處理服務"""
    
    UPLOAD_DIR = "uploads/pdf"
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = ['.pdf']
    
    @staticmethod
    def ensure_upload_dir():
        """確保上傳目錄存在"""
        if not os.path.exists(PDFService.UPLOAD_DIR):
            os.makedirs(PDFService.UPLOAD_DIR, exist_ok=True)
    
    @staticmethod
    def validate_pdf_file(file: UploadFile) -> None:
        """驗證 PDF 檔案"""
        # 檢查檔案大小
        if hasattr(file, 'size') and file.size > PDFService.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413, 
                detail=f"檔案大小超過限制 ({PDFService.MAX_FILE_SIZE // (1024*1024)}MB)"
            )
        
        # 檢查檔案類型
        if not file.filename or not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400, 
                detail="只支援 PDF 檔案"
            )
    
    @staticmethod
    def save_pdf_file(file: UploadFile, user_id: int) -> Tuple[str, str]:
        """儲存 PDF 檔案"""
        PDFService.ensure_upload_dir()
        
        # 生成唯一檔案名
        timestamp = int(time.time())
        filename = f"{user_id}_{timestamp}_{file.filename}"
        file_path = os.path.join(PDFService.UPLOAD_DIR, filename)
        
        # 儲存檔案
        with open(file_path, "wb") as buffer:
            content = file.file.read()
            buffer.write(content)
        
        return file_path, filename
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> Dict[str, Any]:
        """從 PDF 提取文字"""
        try:
            # 使用 pdfplumber 提取文字（更準確）
            text_content = ""
            page_count = 0
            word_count = 0
            
            with pdfplumber.open(file_path) as pdf:
                page_count = len(pdf.pages)
                
                for page_num, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text_content += f"\n--- 第 {page_num + 1} 頁 ---\n"
                        text_content += page_text
                        word_count += len(page_text.split())
            
            # 如果 pdfplumber 失敗，嘗試 PyPDF2
            if not text_content.strip():
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    page_count = len(pdf_reader.pages)
                    
                    for page_num, page in enumerate(pdf_reader.pages):
                        page_text = page.extract_text()
                        if page_text:
                            text_content += f"\n--- 第 {page_num + 1} 頁 ---\n"
                            text_content += page_text
                            word_count += len(page_text.split())
            
            return {
                "raw_text": text_content.strip(),
                "page_count": page_count,
                "word_count": word_count,
                "extraction_method": "pdfplumber" if text_content.strip() else "PyPDF2"
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"PDF 文字提取失敗: {str(e)}"
            )
    
    @staticmethod
    def analyze_pdf_content(raw_text: str) -> Dict[str, Any]:
        """分析 PDF 內容並提取結構化資料"""
        try:
            # 使用正則表達式提取資訊
            import re
            
            analysis_result = {
                "personal_info": {},
                "academic_scores": {},
                "interests": [],
                "achievements": [],
                "career_goals": "",
                "preferred_majors": []
            }
            
            # 提取姓名
            name_patterns = [
                r'姓名[：:]\s*([^\n\r]+)',
                r'姓名\s*([^\n\r]+)',
                r'學生姓名[：:]\s*([^\n\r]+)'
            ]
            for pattern in name_patterns:
                match = re.search(pattern, raw_text)
                if match:
                    analysis_result["personal_info"]["name"] = match.group(1).strip()
                    break
            
            # 提取學校
            school_patterns = [
                r'學校[：:]\s*([^\n\r]+)',
                r'就讀學校[：:]\s*([^\n\r]+)',
                r'高中[：:]\s*([^\n\r]+)'
            ]
            for pattern in school_patterns:
                match = re.search(pattern, raw_text)
                if match:
                    analysis_result["personal_info"]["school"] = match.group(1).strip()
                    break
            
            # 提取學科成績
            score_patterns = [
                r'國文[：:\s]*(\d+)',
                r'英文[：:\s]*(\d+)',
                r'數學[：:\s]*(\d+)',
                r'自然[：:\s]*(\d+)',
                r'社會[：:\s]*(\d+)',
                r'物理[：:\s]*(\d+)',
                r'化學[：:\s]*(\d+)',
                r'生物[：:\s]*(\d+)'
            ]
            
            score_mapping = {
                '國文': 'chinese',
                '英文': 'english',
                '數學': 'math',
                '自然': 'science',
                '社會': 'social',
                '物理': 'physics',
                '化學': 'chemistry',
                '生物': 'biology'
            }
            
            for pattern, subject in zip(score_patterns, score_mapping.keys()):
                matches = re.findall(pattern, raw_text)
                if matches:
                    # 取最後一個匹配的分數
                    score = int(matches[-1])
                    if 0 <= score <= 100:
                        analysis_result["academic_scores"][score_mapping[subject]] = score
            
            # 提取興趣（基於關鍵字）
            interest_keywords = [
                '程式設計', '程式', '軟體', '資訊', '電腦',
                '數學', '統計', '計算',
                '物理', '力學', '電學',
                '化學', '實驗',
                '生物', '生命科學',
                '文學', '語文', '寫作',
                '歷史', '社會',
                '藝術', '美術', '設計',
                '音樂', '樂器',
                '運動', '體育',
                '領導', '管理', '組織',
                '研究', '學術', '實驗',
                '溝通', '表達', '演講',
                '創意', '創新', '創作',
                '分析', '邏輯', '思考'
            ]
            
            for keyword in interest_keywords:
                if keyword in raw_text:
                    analysis_result["interests"].append(keyword)
            
            # 提取成就（基於關鍵字）
            achievement_keywords = [
                '競賽', '比賽', '獲獎', '得獎', '優勝', '冠軍', '亞軍', '季軍',
                '奧林匹亞', '科展', '科奧', '數奧', '物奧', '化奧', '生奧',
                '社長', '會長', '幹部', '領導', '主編', '隊長',
                '證照', '檢定', '認證', '資格',
                '發表', '論文', '研究', '專題'
            ]
            
            # 提取包含成就關鍵字的句子
            sentences = re.split(r'[。！？\n]', raw_text)
            for sentence in sentences:
                for keyword in achievement_keywords:
                    if keyword in sentence:
                        achievement = sentence.strip()
                        if len(achievement) > 5 and len(achievement) < 100:
                            analysis_result["achievements"].append(achievement)
                        break
            
            # 提取職業目標
            career_patterns = [
                r'希望[^。]*從事[^。]*',
                r'未來[^。]*目標[^。]*',
                r'志向[^。]*',
                r'夢想[^。]*'
            ]
            
            for pattern in career_patterns:
                matches = re.findall(pattern, raw_text)
                if matches:
                    analysis_result["career_goals"] = matches[0].strip()
                    break
            
            # 提取偏好學系
            major_keywords = [
                '資訊工程', '電機工程', '機械工程', '土木工程',
                '商業管理', '企業管理', '經濟學', '會計學',
                '數學系', '物理系', '化學系', '生物系',
                '外國語文', '中文系', '歷史系', '社會系',
                '心理學', '教育學', '法律系', '醫學系'
            ]
            
            for keyword in major_keywords:
                if keyword in raw_text:
                    analysis_result["preferred_majors"].append(keyword)
            
            return analysis_result
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"PDF 內容分析失敗: {str(e)}"
            )
    
    @staticmethod
    def create_pdf_upload_record(
        db: Session,
        user_id: int,
        filename: str,
        file_path: str,
        file_size: int,
        raw_text: str,
        page_count: int,
        word_count: int
    ) -> PDFUpload:
        """創建 PDF 上傳記錄"""
        pdf_upload = PDFUpload(
            user_id=user_id,
            filename=filename,
            file_path=file_path,
            file_size=file_size,
            raw_text=raw_text,
            page_count=page_count,
            word_count=word_count,
            status="uploaded"
        )
        
        db.add(pdf_upload)
        db.commit()
        db.refresh(pdf_upload)
        
        return pdf_upload
    
    @staticmethod
    def process_pdf_upload(
        db: Session,
        file: UploadFile,
        user_id: int
    ) -> Dict[str, Any]:
        """處理 PDF 上傳的完整流程"""
        start_time = time.time()
        
        try:
            # 1. 驗證檔案
            PDFService.validate_pdf_file(file)
            
            # 2. 儲存檔案
            file_path, filename = PDFService.save_pdf_file(file, user_id)
            file_size = os.path.getsize(file_path)
            
            # 3. 提取文字
            text_result = PDFService.extract_text_from_pdf(file_path)
            raw_text = text_result["raw_text"]
            page_count = text_result["page_count"]
            word_count = text_result["word_count"]
            
            # 4. 創建上傳記錄
            pdf_upload = PDFService.create_pdf_upload_record(
                db, user_id, filename, file_path, file_size,
                raw_text, page_count, word_count
            )
            
            # 5. 分析內容
            pdf_upload.status = "processing"
            db.commit()
            
            analysis_result = PDFService.analyze_pdf_content(raw_text)
            
            # 6. 儲存分析結果
            pdf_upload.processed_data = json.dumps(analysis_result, ensure_ascii=False)
            pdf_upload.status = "completed"
            pdf_upload.processing_time = time.time() - start_time
            db.commit()
            
            # 7. 使用 AI 進行推薦分析
            try:
                recommendations = analyze_student_data(analysis_result)
                
                # 儲存推薦結果
                from ..models.recommendation import Recommendation
                for i, rec in enumerate(recommendations):
                    recommendation = Recommendation(
                        user_id=user_id,
                        pdf_upload_id=pdf_upload.id,
                        department=rec["department"],
                        university=rec.get("university"),
                        major=rec.get("major"),
                        score=rec["score"],
                        reason=rec.get("reason"),
                        rank=i + 1
                    )
                    db.add(recommendation)
                
                db.commit()
                
            except Exception as e:
                print(f"AI 分析失敗: {e}")
                # 即使 AI 分析失敗，PDF 上傳仍然成功
            
            return {
                "message": "PDF 上傳並分析完成",
                "upload_id": pdf_upload.id,
                "filename": filename,
                "page_count": page_count,
                "word_count": word_count,
                "processing_time": round(pdf_upload.processing_time, 2),
                "status": pdf_upload.status,
                "analysis_result": analysis_result
            }
            
        except Exception as e:
            # 更新狀態為失敗
            if 'pdf_upload' in locals():
                pdf_upload.status = "failed"
                db.commit()
            
            raise HTTPException(
                status_code=500,
                detail=f"PDF 處理失敗: {str(e)}"
            )
    
    @staticmethod
    def get_user_pdf_uploads(db: Session, user_id: int, skip: int = 0, limit: int = 100):
        """獲取用戶的 PDF 上傳記錄"""
        return db.query(PDFUpload).filter(
            PDFUpload.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_pdf_upload_by_id(db: Session, upload_id: int, user_id: int) -> Optional[PDFUpload]:
        """根據 ID 獲取 PDF 上傳記錄"""
        return db.query(PDFUpload).filter(
            PDFUpload.id == upload_id,
            PDFUpload.user_id == user_id
        ).first()
