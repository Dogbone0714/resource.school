#!/usr/bin/env python3
"""
資料庫初始化腳本
用於建立 hhkone_resourceschool 資料庫和相關表結構
"""

import pymysql
import sys
import os

# 添加 src 目錄到路徑
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.models.database import engine, Base
from src.models import User, Resource, Upload, Recommendation

def create_database():
    """建立資料庫"""
    try:
        # 連接到 MySQL 伺服器（不指定資料庫）
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='rootpassword',  # 使用 root 密碼
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # 建立資料庫
            cursor.execute("CREATE DATABASE IF NOT EXISTS hhkone_resourceschool CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("✅ 資料庫 hhkone_resourceschool 建立成功")
            
            # 建立用戶並授權
            cursor.execute("CREATE USER IF NOT EXISTS 'hhkone_resourceschool'@'%' IDENTIFIED BY 'C7W7sTvpuwrWQ2v2GV28'")
            cursor.execute("GRANT ALL PRIVILEGES ON hhkone_resourceschool.* TO 'hhkone_resourceschool'@'%'")
            cursor.execute("FLUSH PRIVILEGES")
            print("✅ 用戶 hhkone_resourceschool 建立成功並授權")
        
        connection.close()
        
    except Exception as e:
        print(f"❌ 建立資料庫失敗: {e}")
        return False
    
    return True

def create_tables():
    """建立資料表"""
    try:
        # 建立所有表
        Base.metadata.create_all(bind=engine)
        print("✅ 資料表建立成功")
        
        # 檢查表是否建立
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"📋 已建立的表: {', '.join(tables)}")
        
    except Exception as e:
        print(f"❌ 建立資料表失敗: {e}")
        return False
    
    return True

def test_connection():
    """測試資料庫連接"""
    try:
        from src.models.database import SessionLocal
        db = SessionLocal()
        
        # 測試查詢
        result = db.execute("SELECT 1 as test")
        test_value = result.fetchone()[0]
        
        if test_value == 1:
            print("✅ 資料庫連接測試成功")
            return True
        else:
            print("❌ 資料庫連接測試失敗")
            return False
            
    except Exception as e:
        print(f"❌ 資料庫連接測試失敗: {e}")
        return False
    finally:
        db.close()

def main():
    """主函數"""
    print("🚀 開始初始化 特殊選才備審分析系統 資料庫...")
    print("=" * 50)
    
    # 步驟 1: 建立資料庫
    print("\n1. 建立資料庫...")
    if not create_database():
        print("❌ 資料庫建立失敗，請檢查 MySQL 服務是否運行")
        return
    
    # 步驟 2: 建立資料表
    print("\n2. 建立資料表...")
    if not create_tables():
        print("❌ 資料表建立失敗")
        return
    
    # 步驟 3: 測試連接
    print("\n3. 測試資料庫連接...")
    if not test_connection():
        print("❌ 資料庫連接測試失敗")
        return
    
    print("\n" + "=" * 50)
    print("🎉 資料庫初始化完成！")
    print("\n📋 資料庫資訊:")
    print("   - 資料庫名稱: hhkone_resourceschool")
    print("   - 用戶名稱: hhkone_resourceschool")
    print("   - 密碼: C7W7sTvpuwrWQ2v2GV28")
    print("   - 主機: localhost:3306")
    print("\n🚀 現在可以啟動應用程式了！")

if __name__ == "__main__":
    main()
