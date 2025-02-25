# app/models.py
import uuid
from sqlalchemy import Column, String, DateTime, func
from app.database import Base

def generate_uuid():
    """
    產生隨機 UUID 作為學員資料的主鍵
    """
    return str(uuid.uuid4())

class Member(Base):
    """
    學員資料模型
    """
    __tablename__ = "members"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    name = Column(String, index=True, nullable=False)             # 學員姓名
    email = Column(String, unique=True, index=True, nullable=True)    # 電子信箱
    affiliation = Column(String, nullable=True)                     # 所屬單位
    phone = Column(String, nullable=True)                           # 聯絡電話
    created_at = Column(DateTime(timezone=True), server_default=func.now())
