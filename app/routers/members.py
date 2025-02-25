# app/routers/members.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal
from app.security import get_api_key
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.MemberOut)
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    if member.email:
        db_member = crud.get_member_by_email(db, email=member.email)
        if db_member:
            raise HTTPException(status_code=400, detail="Email 已存在")
    new_member = crud.create_member(db, name=member.name, email=member.email, affiliation=member.affiliation, phone=member.phone)
    return new_member

@router.get("/", response_model=List[schemas.MemberOut])
def read_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    members = crud.get_members(db, skip=skip, limit=limit)
    return members
