# app/config.py
import os
from dotenv import load_dotenv

# 載入 .env 檔案內的環境變數
load_dotenv()

class Config:
    # 資料庫連線 URL
    DATABASE_URL = "sqlite:///./course_data.db"
    # API 金鑰（如有需求）
    VALID_API_KEY = os.getenv("VALID_API_KEY", "your-secret-key")
    # Google 憑證，必須為 JSON 格式字串
    GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")
    # 匯出檔案存放路徑
    EXPORT_PATH = os.path.join("data", "export.csv")
    # 日誌檔案路徑
    LOG_PATH = os.path.join("logs", "app.log")

config = Config()
