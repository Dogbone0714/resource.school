import json
from typing import List, Dict, Any
import random

class AIService:
    """AI 推薦服務"""
    
    # 學系資料庫
    DEPARTMENTS = {
        "理工類": [
            {
                "department": "資訊工程學系",
                "universities": ["國立台灣大學", "國立清華大學", "國立交通大學", "國立成功大學"],
                "majors": ["軟體工程", "人工智慧", "資料科學", "網路工程"],
                "keywords": ["程式設計", "電腦", "軟體", "資訊", "AI", "人工智慧", "資料", "網路"]
            },
            {
                "department": "電機工程學系", 
                "universities": ["國立台灣大學", "國立清華大學", "國立交通大學", "國立成功大學"],
                "majors": ["電力工程", "控制工程", "通訊工程", "電子工程"],
                "keywords": ["電機", "電子", "電力", "控制", "通訊", "電路", "物理", "數學"]
            },
            {
                "department": "機械工程學系",
                "universities": ["國立台灣大學", "國立清華大學", "國立成功大學", "國立中央大學"],
                "majors": ["機械設計", "製造工程", "熱流工程", "材料工程"],
                "keywords": ["機械", "設計", "製造", "材料", "物理", "數學", "工程"]
            },
            {
                "department": "數學系",
                "universities": ["國立台灣大學", "國立清華大學", "國立交通大學", "國立中央大學"],
                "majors": ["應用數學", "統計學", "計算數學", "純數學"],
                "keywords": ["數學", "統計", "計算", "邏輯", "分析"]
            }
        ],
        "商管類": [
            {
                "department": "商業管理學系",
                "universities": ["國立政治大學", "國立台灣大學", "國立清華大學", "國立中央大學"],
                "majors": ["企業管理", "行銷管理", "人力資源管理", "營運管理"],
                "keywords": ["管理", "商業", "企業", "行銷", "領導", "溝通"]
            },
            {
                "department": "經濟學系",
                "universities": ["國立台灣大學", "國立政治大學", "國立清華大學", "國立中央大學"],
                "majors": ["經濟理論", "計量經濟", "國際經濟", "金融經濟"],
                "keywords": ["經濟", "金融", "統計", "數學", "分析", "市場"]
            },
            {
                "department": "會計學系",
                "universities": ["國立政治大學", "國立台灣大學", "國立成功大學", "國立中央大學"],
                "majors": ["財務會計", "管理會計", "審計", "稅務"],
                "keywords": ["會計", "財務", "審計", "稅務", "數字", "精確"]
            }
        ],
        "人文社會類": [
            {
                "department": "心理學系",
                "universities": ["國立台灣大學", "國立政治大學", "國立清華大學", "國立中央大學"],
                "majors": ["臨床心理", "認知心理", "社會心理", "發展心理"],
                "keywords": ["心理", "行為", "認知", "社會", "人類", "研究"]
            },
            {
                "department": "社會學系",
                "universities": ["國立台灣大學", "國立政治大學", "國立清華大學", "國立中央大學"],
                "majors": ["社會理論", "社會政策", "社會工作", "社會研究"],
                "keywords": ["社會", "政策", "研究", "人類", "文化", "分析"]
            },
            {
                "department": "外國語文學系",
                "universities": ["國立台灣大學", "國立政治大學", "國立清華大學", "國立中央大學"],
                "majors": ["英語文學", "翻譯", "語言學", "比較文學"],
                "keywords": ["外語", "英語", "文學", "翻譯", "語言", "溝通"]
            }
        ]
    }
    
    @staticmethod
    def analyze_student_data(data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """分析學生資料並生成推薦"""
        # 提取關鍵資訊
        academic_scores = data.get("academic_scores", {})
        interests = data.get("interests", [])
        achievements = data.get("achievements", [])
        career_goals = data.get("career_goals", "")
        preferred_majors = data.get("preferred_majors", [])
        
        # 計算各科成績
        scores = {
            "chinese": academic_scores.get("chinese", 0),
            "english": academic_scores.get("english", 0),
            "math": academic_scores.get("math", 0),
            "science": academic_scores.get("science", 0),
            "social": academic_scores.get("social", 0)
        }
        
        # 分析興趣和目標
        interest_text = " ".join(interests).lower()
        career_text = career_goals.lower()
        achievement_text = " ".join(achievements).lower()
        
        # 計算推薦分數
        recommendations = []
        
        for category, departments in AIService.DEPARTMENTS.items():
            for dept in departments:
                score = AIService._calculate_department_score(
                    dept, scores, interest_text, career_text, achievement_text, preferred_majors
                )
                
                if score > 0.3:  # 只推薦分數較高的學系
                    university = random.choice(dept["universities"])
                    major = random.choice(dept["majors"])
                    
                    recommendations.append({
                        "department": dept["department"],
                        "university": university,
                        "major": major,
                        "score": round(score, 3),
                        "reason": AIService._generate_reason(dept, scores, interests)
                    })
        
        # 按分數排序並限制數量
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        return recommendations[:5]  # 返回前5個推薦
    
    @staticmethod
    def _calculate_department_score(
        dept: Dict[str, Any], 
        scores: Dict[str, int], 
        interest_text: str, 
        career_text: str, 
        achievement_text: str,
        preferred_majors: List[str]
    ) -> float:
        """計算學系推薦分數"""
        score = 0.0
        
        # 關鍵字匹配分數
        keywords = dept["keywords"]
        keyword_matches = sum(1 for keyword in keywords if keyword in interest_text)
        keyword_score = keyword_matches / len(keywords) * 0.3
        
        # 職業目標匹配
        career_matches = sum(1 for keyword in keywords if keyword in career_text)
        career_score = career_matches / len(keywords) * 0.2
        
        # 成就匹配
        achievement_matches = sum(1 for keyword in keywords if keyword in achievement_text)
        achievement_score = achievement_matches / len(keywords) * 0.2
        
        # 成績匹配
        grade_score = AIService._calculate_grade_score(dept, scores) * 0.3
        
        # 偏好專業匹配
        preference_score = 0.0
        if preferred_majors:
            dept_name = dept["department"].lower()
            for preferred in preferred_majors:
                if any(keyword in preferred.lower() for keyword in keywords):
                    preference_score = 0.1
                    break
        
        score = keyword_score + career_score + achievement_score + grade_score + preference_score
        
        # 添加一些隨機性
        score += random.uniform(-0.05, 0.05)
        
        return max(0, min(1, score))  # 限制在 0-1 範圍
    
    @staticmethod
    def _calculate_grade_score(dept: Dict[str, Any], scores: Dict[str, int]) -> float:
        """根據成績計算分數"""
        # 不同學系對不同科目的重視程度
        weight_map = {
            "資訊工程學系": {"math": 0.4, "science": 0.3, "english": 0.2, "chinese": 0.1},
            "電機工程學系": {"math": 0.4, "science": 0.3, "english": 0.2, "chinese": 0.1},
            "機械工程學系": {"math": 0.3, "science": 0.4, "english": 0.2, "chinese": 0.1},
            "數學系": {"math": 0.6, "science": 0.2, "english": 0.1, "chinese": 0.1},
            "商業管理學系": {"chinese": 0.3, "english": 0.3, "math": 0.2, "social": 0.2},
            "經濟學系": {"math": 0.4, "chinese": 0.2, "english": 0.2, "social": 0.2},
            "會計學系": {"math": 0.3, "chinese": 0.3, "english": 0.2, "social": 0.2},
            "心理學系": {"chinese": 0.3, "english": 0.2, "social": 0.3, "math": 0.2},
            "社會學系": {"chinese": 0.4, "social": 0.4, "english": 0.2},
            "外國語文學系": {"english": 0.5, "chinese": 0.3, "social": 0.2}
        }
        
        dept_name = dept["department"]
        weights = weight_map.get(dept_name, {"math": 0.25, "chinese": 0.25, "english": 0.25, "science": 0.25})
        
        weighted_score = 0
        total_weight = 0
        
        for subject, weight in weights.items():
            if subject in scores:
                weighted_score += (scores[subject] / 100) * weight
                total_weight += weight
        
        return weighted_score / total_weight if total_weight > 0 else 0
    
    @staticmethod
    def _generate_reason(dept: Dict[str, Any], scores: Dict[str, int], interests: List[str]) -> str:
        """生成推薦理由"""
        dept_name = dept["department"]
        reasons = []
        
        # 基於成績的理由
        if scores.get("math", 0) >= 85:
            reasons.append("您的數學成績優秀")
        if scores.get("science", 0) >= 85:
            reasons.append("您的自然科成績優異")
        if scores.get("english", 0) >= 85:
            reasons.append("您的英文能力佳")
        if scores.get("chinese", 0) >= 85:
            reasons.append("您的國文基礎扎實")
        
        # 基於興趣的理由
        if any(keyword in " ".join(interests).lower() for keyword in dept["keywords"]):
            reasons.append("您的興趣與此領域相符")
        
        # 預設理由
        if not reasons:
            reasons.append("根據您的整體表現，此領域適合您的發展")
        
        return f"根據分析，{dept_name}適合您的原因：{', '.join(reasons[:2])}"
