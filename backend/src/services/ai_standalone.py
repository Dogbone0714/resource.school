"""
獨立 AI 推薦服務模組
使用 Pandas 和 scikit-learn 進行學系推薦分析
不依賴其他服務模組
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from typing import List, Dict, Any, Tuple
import json
import pickle
import os

class DepartmentRecommendationAI:
    """學系推薦 AI 系統"""
    
    def __init__(self):
        self.model = None
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        self.departments = []
        self.feature_columns = []
        self.model_path = "ai_models/department_recommendation_model.pkl"
        self.scaler_path = "ai_models/scaler.pkl"
        self.encoder_path = "ai_models/label_encoder.pkl"
        
        # 確保模型目錄存在
        os.makedirs("ai_models", exist_ok=True)
        
        # 初始化或載入模型
        self._initialize_model()
    
    def _initialize_model(self):
        """初始化或載入模型"""
        if os.path.exists(self.model_path):
            self._load_model()
        else:
            self._create_mock_data_and_train()
    
    def _create_mock_data_and_train(self):
        """創建假資料並訓練模型"""
        print("🤖 創建假資料並訓練學系推薦模型...")
        
        # 生成假資料
        mock_data = self._generate_mock_data()
        
        # 準備特徵和標籤
        X, y = self._prepare_features_and_labels(mock_data)
        
        # 訓練模型
        self._train_model(X, y)
        
        # 儲存模型
        self._save_model()
        
        print("✅ 模型訓練完成並儲存")
    
    def _generate_mock_data(self) -> pd.DataFrame:
        """生成假資料"""
        np.random.seed(42)  # 確保結果可重現
        
        n_samples = 1000
        
        # 生成學科成績 (0-100)
        data = {
            'chinese_score': np.random.normal(75, 15, n_samples).clip(0, 100),
            'english_score': np.random.normal(80, 12, n_samples).clip(0, 100),
            'math_score': np.random.normal(70, 18, n_samples).clip(0, 100),
            'science_score': np.random.normal(75, 16, n_samples).clip(0, 100),
            'social_score': np.random.normal(78, 14, n_samples).clip(0, 100),
        }
        
        # 生成興趣特徵 (0-1 之間的分數)
        interests = [
            'programming', 'mathematics', 'physics', 'chemistry', 'biology',
            'literature', 'history', 'art', 'music', 'sports', 'leadership',
            'research', 'communication', 'creativity', 'analysis'
        ]
        
        for interest in interests:
            data[f'interest_{interest}'] = np.random.beta(2, 5, n_samples)
        
        # 生成社團經歷特徵
        data['club_leadership'] = np.random.binomial(1, 0.3, n_samples)
        data['club_tech'] = np.random.binomial(1, 0.4, n_samples)
        data['club_art'] = np.random.binomial(1, 0.2, n_samples)
        data['club_sports'] = np.random.binomial(1, 0.3, n_samples)
        data['club_academic'] = np.random.binomial(1, 0.5, n_samples)
        
        # 生成競賽獲獎特徵
        data['competition_math'] = np.random.binomial(1, 0.15, n_samples)
        data['competition_science'] = np.random.binomial(1, 0.12, n_samples)
        data['competition_programming'] = np.random.binomial(1, 0.08, n_samples)
        data['competition_language'] = np.random.binomial(1, 0.1, n_samples)
        data['competition_art'] = np.random.binomial(1, 0.05, n_samples)
        
        # 生成學系標籤 (基於特徵的邏輯規則)
        departments = []
        for i in range(n_samples):
            dept = self._assign_department_by_rules(data, i)
            departments.append(dept)
        
        data['department'] = departments
        
        return pd.DataFrame(data)
    
    def _assign_department_by_rules(self, data: Dict, idx: int) -> str:
        """根據規則分配學系"""
        # 計算各領域的綜合分數
        tech_score = (
            data['math_score'][idx] * 0.3 +
            data['science_score'][idx] * 0.3 +
            data['interest_programming'][idx] * 100 * 0.2 +
            data['interest_mathematics'][idx] * 100 * 0.1 +
            data['club_tech'][idx] * 20 +
            data['competition_programming'][idx] * 30 +
            data['competition_math'][idx] * 20
        )
        
        engineering_score = (
            data['math_score'][idx] * 0.25 +
            data['science_score'][idx] * 0.35 +
            data['interest_physics'][idx] * 100 * 0.2 +
            data['interest_mathematics'][idx] * 100 * 0.1 +
            data['club_tech'][idx] * 15 +
            data['competition_math'][idx] * 25 +
            data['competition_science'][idx] * 25
        )
        
        business_score = (
            data['chinese_score'][idx] * 0.3 +
            data['english_score'][idx] * 0.3 +
            data['social_score'][idx] * 0.2 +
            data['interest_leadership'][idx] * 100 * 0.1 +
            data['interest_communication'][idx] * 100 * 0.1 +
            data['club_leadership'][idx] * 25 +
            data['competition_language'][idx] * 20
        )
        
        science_score = (
            data['math_score'][idx] * 0.3 +
            data['science_score'][idx] * 0.4 +
            data['interest_research'][idx] * 100 * 0.2 +
            data['interest_analysis'][idx] * 100 * 0.1 +
            data['club_academic'][idx] * 20 +
            data['competition_science'][idx] * 30 +
            data['competition_math'][idx] * 20
        )
        
        art_score = (
            data['chinese_score'][idx] * 0.3 +
            data['interest_art'][idx] * 100 * 0.4 +
            data['interest_creativity'][idx] * 100 * 0.3 +
            data['club_art'][idx] * 30 +
            data['competition_art'][idx] * 40
        )
        
        # 選擇分數最高的學系
        scores = {
            '資訊工程學系': tech_score,
            '電機工程學系': engineering_score,
            '商業管理學系': business_score,
            '數學系': science_score,
            '外國語文學系': art_score
        }
        
        return max(scores, key=scores.get)
    
    def _prepare_features_and_labels(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """準備特徵和標籤"""
        # 分離特徵和標籤
        feature_columns = [col for col in data.columns if col != 'department']
        X = data[feature_columns].values
        y = data['department'].values
        
        # 儲存特徵列名
        self.feature_columns = feature_columns
        
        # 編碼標籤
        y_encoded = self.label_encoder.fit_transform(y)
        self.departments = self.label_encoder.classes_.tolist()
        
        return X, y_encoded
    
    def _train_model(self, X: np.ndarray, y: np.ndarray):
        """訓練模型"""
        # 分割資料
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # 標準化特徵
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # 訓練隨機森林模型
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # 評估模型
        y_pred = self.model.predict(X_test_scaled)
        accuracy = np.mean(y_pred == y_test)
        
        print(f"📊 模型準確率: {accuracy:.3f}")
    
    def _save_model(self):
        """儲存模型"""
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        with open(self.scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        
        with open(self.encoder_path, 'wb') as f:
            pickle.dump(self.label_encoder, f)
    
    def _load_model(self):
        """載入模型"""
        with open(self.model_path, 'rb') as f:
            self.model = pickle.load(f)
        
        with open(self.scaler_path, 'rb') as f:
            self.scaler = pickle.load(f)
        
        with open(self.encoder_path, 'rb') as f:
            self.label_encoder = pickle.load(f)
        
        # 重建特徵列名和學系列表
        self.feature_columns = [
            'chinese_score', 'english_score', 'math_score', 'science_score', 'social_score',
            'interest_programming', 'interest_mathematics', 'interest_physics', 'interest_chemistry',
            'interest_biology', 'interest_literature', 'interest_history', 'interest_art',
            'interest_music', 'interest_sports', 'interest_leadership', 'interest_research',
            'interest_communication', 'interest_creativity', 'interest_analysis',
            'club_leadership', 'club_tech', 'club_art', 'club_sports', 'club_academic',
            'competition_math', 'competition_science', 'competition_programming',
            'competition_language', 'competition_art'
        ]
        self.departments = self.label_encoder.classes_.tolist()
    
    def analyze_student_data(self, student_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """分析學生資料並生成推薦"""
        # 提取和處理學生資料
        features = self._extract_features(student_data)
        
        # 預測學系
        predictions = self._predict_departments(features)
        
        # 生成推薦結果
        recommendations = self._generate_recommendations(predictions, student_data)
        
        return recommendations
    
    def _extract_features(self, student_data: Dict[str, Any]) -> np.ndarray:
        """從學生資料中提取特徵"""
        features = np.zeros(len(self.feature_columns))
        
        # 學科成績
        academic_scores = student_data.get('academic_scores', {})
        score_mapping = {
            'chinese_score': 'chinese',
            'english_score': 'english', 
            'math_score': 'math',
            'science_score': 'science',
            'social_score': 'social'
        }
        
        for feature_name, score_key in score_mapping.items():
            if feature_name in self.feature_columns:
                idx = self.feature_columns.index(feature_name)
                features[idx] = academic_scores.get(score_key, 0)
        
        # 興趣特徵
        interests = student_data.get('interests', [])
        interest_mapping = {
            'programming': ['程式設計', '程式', 'coding', '軟體', '資訊'],
            'mathematics': ['數學', '統計', '計算'],
            'physics': ['物理', '力學', '電學'],
            'chemistry': ['化學', '實驗'],
            'biology': ['生物', '生命科學'],
            'literature': ['文學', '語文', '寫作'],
            'history': ['歷史', '社會'],
            'art': ['藝術', '美術', '設計'],
            'music': ['音樂', '樂器'],
            'sports': ['運動', '體育', '健身'],
            'leadership': ['領導', '管理', '組織'],
            'research': ['研究', '學術', '實驗'],
            'communication': ['溝通', '表達', '演講'],
            'creativity': ['創意', '創新', '創作'],
            'analysis': ['分析', '邏輯', '思考']
        }
        
        for interest_type, keywords in interest_mapping.items():
            feature_name = f'interest_{interest_type}'
            if feature_name in self.feature_columns:
                idx = self.feature_columns.index(feature_name)
                # 計算興趣匹配度
                match_score = sum(1 for interest in interests 
                                for keyword in keywords 
                                if keyword in interest.lower()) / len(keywords)
                features[idx] = min(match_score, 1.0)
        
        # 社團經歷
        achievements = student_data.get('achievements', [])
        club_mapping = {
            'club_leadership': ['社長', '會長', '幹部', '領導'],
            'club_tech': ['資訊', '程式', '電腦', '科技'],
            'club_art': ['美術', '藝術', '設計', '創作'],
            'club_sports': ['運動', '體育', '球隊', '健身'],
            'club_academic': ['學術', '研究', '讀書', '競賽']
        }
        
        for club_type, keywords in club_mapping.items():
            if club_type in self.feature_columns:
                idx = self.feature_columns.index(club_type)
                features[idx] = 1 if any(any(keyword in achievement.lower() 
                                           for keyword in keywords) 
                                       for achievement in achievements) else 0
        
        # 競賽獲獎
        competition_mapping = {
            'competition_math': ['數學', '奧林匹亞', '競賽'],
            'competition_science': ['科學', '物理', '化學', '生物'],
            'competition_programming': ['程式', '資訊', '軟體'],
            'competition_language': ['語文', '英文', '國文'],
            'competition_art': ['美術', '藝術', '創作']
        }
        
        for comp_type, keywords in competition_mapping.items():
            if comp_type in self.feature_columns:
                idx = self.feature_columns.index(comp_type)
                features[idx] = 1 if any(any(keyword in achievement.lower() 
                                           for keyword in keywords) 
                                       for achievement in achievements) else 0
        
        return features.reshape(1, -1)
    
    def _predict_departments(self, features: np.ndarray) -> List[Tuple[str, float]]:
        """預測學系"""
        # 標準化特徵
        features_scaled = self.scaler.transform(features)
        
        # 預測機率
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        # 獲取預測結果
        predictions = []
        for i, prob in enumerate(probabilities):
            dept_name = self.departments[i]
            predictions.append((dept_name, prob))
        
        # 按機率排序
        predictions.sort(key=lambda x: x[1], reverse=True)
        
        return predictions
    
    def _generate_recommendations(self, predictions: List[Tuple[str, float]], 
                                student_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成推薦結果"""
        recommendations = []
        
        # 學系對應的大學和專業
        dept_info = {
            '資訊工程學系': {
                'universities': ['國立台灣大學', '國立清華大學', '國立交通大學', '國立成功大學'],
                'majors': ['軟體工程', '人工智慧', '資料科學', '網路工程']
            },
            '電機工程學系': {
                'universities': ['國立台灣大學', '國立清華大學', '國立交通大學', '國立成功大學'],
                'majors': ['電力工程', '控制工程', '通訊工程', '電子工程']
            },
            '商業管理學系': {
                'universities': ['國立政治大學', '國立台灣大學', '國立清華大學', '國立中央大學'],
                'majors': ['企業管理', '行銷管理', '人力資源管理', '營運管理']
            },
            '數學系': {
                'universities': ['國立台灣大學', '國立清華大學', '國立交通大學', '國立中央大學'],
                'majors': ['應用數學', '統計學', '計算數學', '純數學']
            },
            '外國語文學系': {
                'universities': ['國立台灣大學', '國立政治大學', '國立清華大學', '國立中央大學'],
                'majors': ['英語文學', '翻譯', '語言學', '比較文學']
            }
        }
        
        # 生成前3名推薦
        for i, (dept_name, score) in enumerate(predictions[:3]):
            if dept_name in dept_info:
                info = dept_info[dept_name]
                import random
                
                recommendation = {
                    'department': dept_name,
                    'university': random.choice(info['universities']),
                    'major': random.choice(info['majors']),
                    'score': round(score, 3),
                    'reason': self._generate_reason(dept_name, score, student_data),
                    'rank': i + 1
                }
                recommendations.append(recommendation)
        
        return recommendations
    
    def _generate_reason(self, dept_name: str, score: float, student_data: Dict[str, Any]) -> str:
        """生成推薦理由"""
        reasons = []
        
        # 基於分數的理由
        if score > 0.8:
            reasons.append("AI 分析顯示您非常適合此領域")
        elif score > 0.6:
            reasons.append("AI 分析顯示您適合此領域")
        else:
            reasons.append("AI 分析顯示此領域值得考慮")
        
        # 基於成績的理由
        academic_scores = student_data.get('academic_scores', {})
        if dept_name in ['資訊工程學系', '電機工程學系', '數學系']:
            if academic_scores.get('math', 0) >= 85:
                reasons.append("您的數學成績優秀")
            if academic_scores.get('science', 0) >= 85:
                reasons.append("您的自然科成績優異")
        elif dept_name == '商業管理學系':
            if academic_scores.get('chinese', 0) >= 85:
                reasons.append("您的國文成績優秀")
            if academic_scores.get('english', 0) >= 85:
                reasons.append("您的英文能力佳")
        
        # 基於興趣的理由
        interests = student_data.get('interests', [])
        if any('程式' in interest or '資訊' in interest for interest in interests):
            if dept_name in ['資訊工程學系', '電機工程學系']:
                reasons.append("您的興趣與此領域高度相關")
        
        # 預設理由
        if not reasons:
            reasons.append("根據您的整體表現，此領域適合您的發展潛力")
        
        return f"推薦{dept_name}的原因：{'; '.join(reasons[:2])}"

# 全域實例
ai_recommendation = DepartmentRecommendationAI()

def analyze_student_data(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """分析學生資料並生成推薦（對外接口）"""
    return ai_recommendation.analyze_student_data(data)
