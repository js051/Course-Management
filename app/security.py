# app/security.py
from fastapi.security import APIKeyHeader
from fastapi import Depends, HTTPException
from app.config import config

# 使用 APIKeyHeader 作為安全認證
api_key_header = APIKeyHeader(name="X-API-Key")

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != config.VALID_API_KEY:
        raise HTTPException(status_code=403, detail="無效的 API Key")
    return api_key
