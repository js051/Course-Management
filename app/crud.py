# app/crud.py
from sqlalchemy.orm import Session
from app.models import Member

def get_member(db: Session, member_id: str):
    """
    根據 member_id 取得學員資料
    """
    return db.query(Member).filter(Member.id == member_id).first()

def get_member_by_email(db: Session, email: str):
    """
    根據電子信箱取得學員資料
    """
    return db.query(Member).filter(Member.email == email).first()

def get_members(db: Session, skip: int = 0, limit: int = 100):
    """
    取得學員資料（支援分頁）
    """
    return db.query(Member).offset(skip).limit(limit).all()

def create_member(db: Session, name: str, email: str = None, affiliation: str = None, phone: str = None):
    """
    新增一筆學員資料
    """
    db_member = Member(name=name, email=email, affiliation=affiliation, phone=phone)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member
