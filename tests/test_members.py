# tests/test_members.py
import pytest
from app import crud, models
from app.database import SessionLocal, engine

@pytest.fixture
def db():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()

def test_create_member(db):
    member = crud.create_member(db, name="Test User", email="test@example.com")
    assert member.name == "Test User"
    assert member.email == "test@example.com"

def test_get_member_by_email(db):
    crud.create_member(db, name="Test User", email="test@example.com")
    member = crud.get_member_by_email(db, email="test@example.com")
    assert member is not None
    assert member.email == "test@example.com"
