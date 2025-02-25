# app/main.py
from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import members

# 建立所有資料表（首次運行時）
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="課程資料管理 API",
    description="內部單機／內網環境下的資料管理 CRUD 服務",
    version="0.1.0"
)

# 將 members 路由加入 FastAPI 應用，前綴 /members
app.include_router(members.router, prefix="/members")
