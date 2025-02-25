# test_credentials_env.py
import os
import json
from dotenv import load_dotenv

def main():
    # 載入 .env
    load_dotenv()
    
    creds_str = os.getenv("GOOGLE_CREDENTIALS")
    if not creds_str:
        print("未在環境變數中找到 GOOGLE_CREDENTIALS，請檢查 .env 檔案。")
        return
    
    # 嘗試解析 JSON
    try:
        creds_data = json.loads(creds_str)
        print("[成功] 已成功解析 GOOGLE_CREDENTIALS 的 JSON。")
        print("[檢查] 'type' =>", creds_data.get("type"))
        print("[檢查] 'project_id' =>", creds_data.get("project_id"))
        # 若需更多檢查可自行加上
    except json.JSONDecodeError as e:
        print("[失敗] GOOGLE_CREDENTIALS 不是合法的 JSON 格式！")
        print("錯誤訊息：", e)

if __name__ == "__main__":
    main()
