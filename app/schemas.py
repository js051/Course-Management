# app/schemas.py
from pydantic import BaseModel

class MemberCreate(BaseModel):
    name: str
    email: str = None
    affiliation: str = None
    phone: str = None

class MemberOut(BaseModel):
    id: str
    name: str
    email: str = None
    affiliation: str = None
    phone: str = None

    class Config:
        orm_mode = True
