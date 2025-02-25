# etl.py
import os
import json
import time
import pandas as pd
from fuzzywuzzy import process
import gspread
from gspread.exceptions import APIError
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
from app.database import SessionLocal
from app import crud

load_dotenv()  # 載入 .env

def safe_open_worksheet(client, sheet_name, worksheet_title, retries=3, delay=3):
    """
    重試機制：若遇到 503 等暫時性錯誤就延遲並重試。
    """
    for attempt in range(retries):
        try:
            sh = client.open(sheet_name)
            ws = sh.worksheet(worksheet_title)
            return ws
        except APIError as e:
            if "503" in str(e) or "ServiceUnavailable" in str(e):
                print(f"[警告] 第 {attempt + 1} 次嘗試開啟 '{sheet_name}'/'{worksheet_title}' 時遇到 503，等待 {delay} 秒後重試...")
                time.sleep(delay)
            else:
                raise
    raise Exception(f"[失敗] 重試 {retries} 次後仍無法打開試算表 '{sheet_name}'/'{worksheet_title}'，請檢查網路與服務狀態。")

def get_google_sheet(sheet_name, worksheet_title):
    """
    改為讀取環境變數 'GOOGLE_CREDENTIALS' 來授權，而非讀取 credentials.json 檔案。
    """
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # 從環境變數讀取 JSON 字串
    creds_str = os.getenv("GOOGLE_CREDENTIALS")
    if not creds_str:
        raise ValueError("環境變數 'GOOGLE_CREDENTIALS' 未設定，請檢查 .env 檔案。")
    
    # 解析成 Python dict
    creds_dict = json.loads(creds_str)
    # 透過 from_json_keyfile_dict 建立授權物件
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    # 透過 safe_open_worksheet 增加重試機制
    sheet = safe_open_worksheet(client, sheet_name, worksheet_title, retries=3, delay=3)
    return sheet

def fetch_data_from_sheet(sheet_name, worksheet_title):
    """
    從 Google 試算表拉取所有回覆資料，並轉換成 Pandas DataFrame。
    同時去除欄位名稱頭尾空白。
    """
    sheet = get_google_sheet(sheet_name, worksheet_title)
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    # 印出原始欄位
    print("取得的欄位:", df.columns)
    print(df.head())

    # 移除每個欄位名稱頭尾空白
    df.columns = [col.strip() for col in df.columns]
    return df

def standardize_unit(unit):
    mapping = {
        "台北": "臺北",
        "台北地院": "臺北地方法院",
        "台中": "臺中",
        "台中地院": "臺中地方法院",
    }
    return mapping.get(unit, unit)

def fuzzy_correct(unit, standard_units):
    match, score = process.extractOne(unit, standard_units)
    if score > 80:
        return match
    else:
        print(f"[警告] 未匹配單位: {unit} (最佳匹配: {match}, 分數: {score})")
        return unit

def etl_process():
    """
    ETL 流程：
      1. 讀取環境變數中的 GOOGLE_CREDENTIALS 來授權。
      2. 從試算表 ('API測試回復' / 'res') 取得資料，去除欄位空白後 rename。
      3. affiliation 欄位標準化 + 模糊比對。
      4. 寫入 SQLite 資料庫並輸出 CSV。
    """
    sheet_name = "API測試回復"
    worksheet_title = "res"

    df = fetch_data_from_sheet(sheet_name, worksheet_title)

    rename_dict = {
        "時間戳記": "timestamp",
        "姓名": "name",
        "電子信箱": "email",
        "所屬單位": "affiliation",
        "聯絡電話": "phone"
    }
    for old_col, new_col in rename_dict.items():
        if old_col in df.columns:
            df.rename(columns={old_col: new_col}, inplace=True)

    print("rename 後的欄位:", df.columns)
    print(df.head())

    if "affiliation" in df.columns:
        df["affiliation"] = df["affiliation"].apply(standardize_unit)
        standard_units = ["臺北地方法院", "臺中地方法院", "高雄地方法院"]
        df["affiliation"] = df["affiliation"].apply(lambda x: fuzzy_correct(x, standard_units))

    db = SessionLocal()
    for idx, row in df.iterrows():
        name = row.get("name")
        email = row.get("email")
        affiliation = row.get("affiliation")
        phone = row.get("phone")
        if email:
            db_member = crud.get_member_by_email(db, email)
            if not db_member:
                crud.create_member(db, name=name, email=email, affiliation=affiliation, phone=phone)
    db.close()

    os.makedirs("data", exist_ok=True)  # 確保 data 目錄存在
    df.to_csv("data/final_data.csv", index=False, encoding="utf-8-sig")
    print("ETL 處理完成，資料已寫入資料庫並存檔至 data/final_data.csv")

if __name__ == "__main__":
    etl_process()
