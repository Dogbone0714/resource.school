#!/usr/bin/env python3
"""
測試後端 API 的腳本
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api():
    """測試 API 端點"""
    print("🚀 開始測試 Resource School API...")
    
    # 測試健康檢查
    print("\n1. 測試健康檢查...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ 健康檢查: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ 健康檢查失敗: {e}")
        return
    
    # 測試用戶註冊
    print("\n2. 測試用戶註冊...")
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "full_name": "測試用戶"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
        if response.status_code == 201:
            print(f"✅ 用戶註冊成功: {response.json()}")
        else:
            print(f"⚠️ 用戶註冊: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ 用戶註冊失敗: {e}")
    
    # 測試用戶登入
    print("\n3. 測試用戶登入...")
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["access_token"]
            print(f"✅ 用戶登入成功: {token_data['user']['username']}")
        else:
            print(f"❌ 用戶登入失敗: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ 用戶登入失敗: {e}")
        return
    
    # 測試檔案上傳
    print("\n4. 測試檔案上傳...")
    sample_data = {
        "personal_info": {
            "name": "張小明",
            "age": 18,
            "school": "台北市立建國高級中學"
        },
        "academic_scores": {
            "chinese": 85,
            "english": 92,
            "math": 88,
            "science": 90,
            "social": 87
        },
        "interests": ["程式設計", "數學", "物理", "人工智慧"],
        "achievements": ["全國資訊競賽第三名", "數學奧林匹亞初選通過"],
        "career_goals": "希望從事軟體開發或人工智慧相關工作",
        "preferred_majors": ["資訊工程", "電機工程", "數學系"]
    }
    
    # 創建臨時 JSON 檔案
    with open("temp_test_data.json", "w", encoding="utf-8") as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)
    
    try:
        with open("temp_test_data.json", "rb") as f:
            files = {"file": ("test_data.json", f, "application/json")}
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(f"{BASE_URL}/api/upload", files=files, headers=headers)
        
        if response.status_code == 200:
            print(f"✅ 檔案上傳成功: {response.json()}")
        else:
            print(f"❌ 檔案上傳失敗: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ 檔案上傳失敗: {e}")
    finally:
        # 清理臨時檔案
        import os
        if os.path.exists("temp_test_data.json"):
            os.remove("temp_test_data.json")
    
    # 測試推薦結果
    print("\n5. 測試推薦結果...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/recommendation/me/latest", headers=headers)
        
        if response.status_code == 200:
            recommendations = response.json()
            print(f"✅ 推薦結果獲取成功: {len(recommendations['recommendations'])} 個推薦")
            for i, rec in enumerate(recommendations["recommendations"][:3], 1):
                print(f"   {i}. {rec['department']} - {rec['university']} ({rec['score']:.1%})")
        else:
            print(f"❌ 推薦結果獲取失敗: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ 推薦結果獲取失敗: {e}")
    
    # 測試資源列表
    print("\n6. 測試資源列表...")
    try:
        response = requests.get(f"{BASE_URL}/api/resources")
        if response.status_code == 200:
            resources = response.json()
            print(f"✅ 資源列表獲取成功: {len(resources)} 個資源")
        else:
            print(f"❌ 資源列表獲取失敗: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ 資源列表獲取失敗: {e}")
    
    print("\n🎉 API 測試完成！")

if __name__ == "__main__":
    test_api()
