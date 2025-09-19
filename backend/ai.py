"""
AI 推薦模組
這個檔案包含進階的 AI 推薦演算法
"""

import json
import numpy as np
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class AdvancedAIRecommendation:
    """進階 AI 推薦系統"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words=None)
        self.department_vectors = None
        self.departments_data = None
        self._initialize_departments()
    
    def _initialize_departments(self):
        """初始化學系資料"""
        self.departments_data = {
            "資訊工程學系": {
                "description": "專注於電腦科學、軟體開發、人工智慧、資料科學等領域",
                "keywords": ["程式設計", "軟體工程", "人工智慧", "資料科學", "網路工程", "演算法", "資料結構"],
                "required_subjects": ["數學", "物理"],
                "career_paths": ["軟體工程師", "資料科學家", "AI工程師", "系統架構師"],
                "universities": ["國立台灣大學", "國立清華大學", "國立交通大學", "國立成功大學"]
            },
            "電機工程學系": {
                "description": "涵蓋電力系統、電子電路、控制系統、通訊工程等領域",
                "keywords": ["電路設計", "電力系統", "控制工程", "通訊工程", "電子元件", "訊號處理"],
                "required_subjects": ["數學", "物理"],
                "career_paths": ["硬體工程師", "電力工程師", "通訊工程師", "控制工程師"],
                "universities": ["國立台灣大學", "國立清華大學", "國立交通大學", "國立成功大學"]
            },
            "機械工程學系": {
                "description": "專精於機械設計、製造工程、熱流工程、材料科學等領域",
                "keywords": ["機械設計", "製造工程", "熱流工程", "材料科學", "CAD", "CAE"],
                "required_subjects": ["數學", "物理"],
                "career_paths": ["機械工程師", "設計工程師", "製造工程師", "研發工程師"],
                "universities": ["國立台灣大學", "國立清華大學", "國立成功大學", "國立中央大學"]
            },
            "商業管理學系": {
                "description": "培養企業管理、行銷、人力資源、營運管理等專業人才",
                "keywords": ["企業管理", "行銷管理", "人力資源", "營運管理", "策略規劃", "領導力"],
                "required_subjects": ["國文", "英文"],
                "career_paths": ["管理顧問", "行銷經理", "人資專員", "營運經理"],
                "universities": ["國立政治大學", "國立台灣大學", "國立清華大學", "國立中央大學"]
            },
            "經濟學系": {
                "description": "研究經濟理論、計量經濟、國際經濟、金融經濟等領域",
                "keywords": ["經濟理論", "計量經濟", "國際經濟", "金融經濟", "統計分析", "市場研究"],
                "required_subjects": ["數學", "國文"],
                "career_paths": ["經濟分析師", "金融分析師", "研究員", "政策分析師"],
                "universities": ["國立台灣大學", "國立政治大學", "國立清華大學", "國立中央大學"]
            }
        }
        
        # 建立 TF-IDF 向量
        descriptions = [dept["description"] for dept in self.departments_data.values()]
        self.department_vectors = self.vectorizer.fit_transform(descriptions)
    
    def analyze_student_profile(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析學生檔案"""
        analysis = {
            "academic_strengths": [],
            "interests_analysis": {},
            "career_orientation": "",
            "recommended_departments": []
        }
        
        # 分析學科成績
        scores = student_data.get("academic_scores", {})
        for subject, score in scores.items():
            if score >= 85:
                analysis["academic_strengths"].append(subject)
        
        # 分析興趣
        interests = student_data.get("interests", [])
        for interest in interests:
            analysis["interests_analysis"][interest] = self._analyze_interest_relevance(interest)
        
        # 分析職業目標
        career_goals = student_data.get("career_goals", "")
        analysis["career_orientation"] = self._analyze_career_orientation(career_goals)
        
        return analysis
    
    def _analyze_interest_relevance(self, interest: str) -> Dict[str, float]:
        """分析興趣與各學系的相關性"""
        relevance = {}
        for dept_name, dept_data in self.departments_data.items():
            score = 0
            for keyword in dept_data["keywords"]:
                if keyword.lower() in interest.lower():
                    score += 1
            relevance[dept_name] = score / len(dept_data["keywords"])
        return relevance
    
    def _analyze_career_orientation(self, career_goals: str) -> str:
        """分析職業導向"""
        if not career_goals:
            return "未明確"
        
        orientations = {
            "技術導向": ["工程師", "開發", "程式", "技術", "研發"],
            "管理導向": ["管理", "領導", "經理", "主管", "經營"],
            "研究導向": ["研究", "分析", "學術", "教授", "學者"],
            "創意導向": ["設計", "創意", "藝術", "創作", "創新"]
        }
        
        scores = {}
        for orientation, keywords in orientations.items():
            score = sum(1 for keyword in keywords if keyword in career_goals)
            scores[orientation] = score
        
        return max(scores, key=scores.get) if max(scores.values()) > 0 else "未明確"
    
    def generate_recommendations(self, student_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成推薦結果"""
        # 分析學生檔案
        analysis = self.analyze_student_profile(student_data)
        
        # 計算推薦分數
        recommendations = []
        for dept_name, dept_data in self.departments_data.items():
            score = self._calculate_recommendation_score(
                student_data, analysis, dept_name, dept_data
            )
            
            if score > 0.3:  # 只推薦分數較高的學系
                recommendations.append({
                    "department": dept_name,
                    "university": self._select_university(dept_data["universities"]),
                    "major": self._select_major(dept_name),
                    "score": round(score, 3),
                    "reason": self._generate_detailed_reason(
                        student_data, analysis, dept_name, dept_data
                    ),
                    "match_factors": self._get_match_factors(
                        student_data, analysis, dept_name, dept_data
                    )
                })
        
        # 按分數排序
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        return recommendations[:5]
    
    def _calculate_recommendation_score(
        self, 
        student_data: Dict[str, Any], 
        analysis: Dict[str, Any], 
        dept_name: str, 
        dept_data: Dict[str, Any]
    ) -> float:
        """計算推薦分數"""
        score = 0.0
        
        # 學科成績匹配 (40%)
        academic_score = self._calculate_academic_score(student_data, dept_data)
        score += academic_score * 0.4
        
        # 興趣匹配 (30%)
        interest_score = self._calculate_interest_score(analysis, dept_name)
        score += interest_score * 0.3
        
        # 職業目標匹配 (20%)
        career_score = self._calculate_career_score(student_data, dept_data)
        score += career_score * 0.2
        
        # 成就匹配 (10%)
        achievement_score = self._calculate_achievement_score(student_data, dept_data)
        score += achievement_score * 0.1
        
        return min(1.0, max(0.0, score))
    
    def _calculate_academic_score(self, student_data: Dict[str, Any], dept_data: Dict[str, Any]) -> float:
        """計算學科成績分數"""
        scores = student_data.get("academic_scores", {})
        required_subjects = dept_data.get("required_subjects", [])
        
        if not required_subjects:
            return 0.5  # 預設分數
        
        total_score = 0
        for subject in required_subjects:
            if subject in scores:
                total_score += scores[subject] / 100
        
        return total_score / len(required_subjects)
    
    def _calculate_interest_score(self, analysis: Dict[str, Any], dept_name: str) -> float:
        """計算興趣匹配分數"""
        interests_analysis = analysis.get("interests_analysis", {})
        if not interests_analysis:
            return 0.0
        
        # 計算平均相關性
        relevance_scores = []
        for interest, relevance in interests_analysis.items():
            if dept_name in relevance:
                relevance_scores.append(relevance[dept_name])
        
        return np.mean(relevance_scores) if relevance_scores else 0.0
    
    def _calculate_career_score(self, student_data: Dict[str, Any], dept_data: Dict[str, Any]) -> float:
        """計算職業目標匹配分數"""
        career_goals = student_data.get("career_goals", "").lower()
        career_paths = dept_data.get("career_paths", [])
        
        if not career_goals or not career_paths:
            return 0.0
        
        matches = 0
        for career_path in career_paths:
            if any(keyword in career_goals for keyword in career_path.lower().split()):
                matches += 1
        
        return matches / len(career_paths)
    
    def _calculate_achievement_score(self, student_data: Dict[str, Any], dept_data: Dict[str, Any]) -> float:
        """計算成就匹配分數"""
        achievements = student_data.get("achievements", [])
        keywords = dept_data.get("keywords", [])
        
        if not achievements or not keywords:
            return 0.0
        
        matches = 0
        for achievement in achievements:
            for keyword in keywords:
                if keyword.lower() in achievement.lower():
                    matches += 1
                    break
        
        return matches / len(achievements)
    
    def _select_university(self, universities: List[str]) -> str:
        """選擇大學"""
        import random
        return random.choice(universities)
    
    def _select_major(self, dept_name: str) -> str:
        """選擇專業"""
        major_map = {
            "資訊工程學系": ["軟體工程", "人工智慧", "資料科學", "網路工程"],
            "電機工程學系": ["電力工程", "控制工程", "通訊工程", "電子工程"],
            "機械工程學系": ["機械設計", "製造工程", "熱流工程", "材料工程"],
            "商業管理學系": ["企業管理", "行銷管理", "人力資源管理", "營運管理"],
            "經濟學系": ["經濟理論", "計量經濟", "國際經濟", "金融經濟"]
        }
        
        majors = major_map.get(dept_name, ["一般"])
        import random
        return random.choice(majors)
    
    def _generate_detailed_reason(
        self, 
        student_data: Dict[str, Any], 
        analysis: Dict[str, Any], 
        dept_name: str, 
        dept_data: Dict[str, Any]
    ) -> str:
        """生成詳細推薦理由"""
        reasons = []
        
        # 基於學科成績
        academic_strengths = analysis.get("academic_strengths", [])
        required_subjects = dept_data.get("required_subjects", [])
        matching_subjects = [s for s in academic_strengths if s in required_subjects]
        
        if matching_subjects:
            reasons.append(f"您在{', '.join(matching_subjects)}方面表現優異")
        
        # 基於興趣
        interests = student_data.get("interests", [])
        matching_interests = []
        for interest in interests:
            for keyword in dept_data.get("keywords", []):
                if keyword.lower() in interest.lower():
                    matching_interests.append(interest)
                    break
        
        if matching_interests:
            reasons.append(f"您的興趣({', '.join(matching_interests)})與此領域高度相關")
        
        # 基於職業目標
        career_goals = student_data.get("career_goals", "")
        if career_goals:
            career_paths = dept_data.get("career_paths", [])
            for career_path in career_paths:
                if any(keyword in career_goals.lower() for keyword in career_path.lower().split()):
                    reasons.append(f"此領域的職業發展路徑符合您的目標")
                    break
        
        # 預設理由
        if not reasons:
            reasons.append("根據您的整體表現，此領域適合您的發展潛力")
        
        return f"推薦{dept_name}的原因：{'; '.join(reasons[:2])}"
    
    def _get_match_factors(
        self, 
        student_data: Dict[str, Any], 
        analysis: Dict[str, Any], 
        dept_name: str, 
        dept_data: Dict[str, Any]
    ) -> List[str]:
        """獲取匹配因素"""
        factors = []
        
        # 學科匹配
        academic_strengths = analysis.get("academic_strengths", [])
        required_subjects = dept_data.get("required_subjects", [])
        if any(s in academic_strengths for s in required_subjects):
            factors.append("學科優勢")
        
        # 興趣匹配
        interests = student_data.get("interests", [])
        if any(any(keyword.lower() in interest.lower() for keyword in dept_data.get("keywords", [])) for interest in interests):
            factors.append("興趣相符")
        
        # 職業目標匹配
        career_goals = student_data.get("career_goals", "")
        if career_goals and any(any(keyword in career_goals.lower() for keyword in career_path.lower().split()) for career_path in dept_data.get("career_paths", [])):
            factors.append("職業目標一致")
        
        return factors

# 全域實例
ai_recommendation = AdvancedAIRecommendation()

def analyze_student_data(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """分析學生資料並生成推薦（對外接口）"""
    return ai_recommendation.generate_recommendations(data)
