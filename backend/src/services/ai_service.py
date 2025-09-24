from .ai_standalone import analyze_student_data as ai_analyze_student_data
from typing import List, Dict, Any

class AIService:
    """AI 推薦服務 - 使用機器學習模型"""
    
    @staticmethod
    def analyze_student_data(data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """分析學生資料並生成推薦 - 使用機器學習模型"""
        return ai_analyze_student_data(data)