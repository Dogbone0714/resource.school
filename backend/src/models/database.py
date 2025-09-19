from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 資料庫配置
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://appuser:apppassword@localhost:3306/resource_school")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """資料庫依賴注入"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
