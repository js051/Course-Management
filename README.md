# 課程資料管理系統(Course Management)

此專案為一個結合 **FastAPI**、**SQLite**、**PyQt5** 及 **Google Sheets API** 的綜合應用示例，並引入 **命令列（CLI）** 與 **ETL** 流程。專案同時透過 **.env** 與 `python-dotenv` 管理機密變數（如 Google Service Account 憑證），並提供 Dockerfile 作為容器化參考。

## 專案功能概述

1. **FastAPI**  
   - 在 `app/main.py` 中啟動 API 服務，並整合 `routers/members.py` 提供簡易的學員 CRUD 介面（路由前綴 `/members`）。
   - 可於瀏覽器打開 http://127.0.0.1:8000/docs 查看自動生成的 Swagger 文件。

2. **命令列 (CLI)**  
   - 透過 `cli.py` 使用 [Click](https://click.palletsprojects.com/) + [Rich](https://github.com/Textualize/rich) 實作，提供 `list_members` 指令快速查詢資料庫中的學員資料。

3. **圖形化介面 (GUI)**  
   - 透過 `gui.py` 使用 [PyQt5](https://pypi.org/project/PyQt5/)，提供桌面應用，支援「列出學員」、「重新整理」、「搜尋」、「匯出 CSV」等功能。

4. **ETL 流程**  
   - 在 `etl.py` 中，使用 [gspread](https://pypi.org/project/gspread/) 與 [oauth2client](https://pypi.org/project/oauth2client/) 連接 Google 試算表，拉取報名資料後，進行欄位清洗、模糊匹配（[fuzzywuzzy](https://pypi.org/project/fuzzywuzzy/)）等處理，最後寫入本地 SQLite 資料庫並輸出 CSV。

5. **資料庫 (SQLite)**  
   - 預設使用 `course_data.db` 作為嵌入式資料庫，透過 SQLAlchemy 做 ORM 對應 (`app/models.py` 與 `app/crud.py`)。

6. **Docker**  
   - 附帶一個簡易 Dockerfile，若需容器化部署可參考。

7. **測試**  
   - `tests/test_members.py` 測試資料庫 CRUD 功能；  
   - `tests/test_credentials_env.py` 測試 `.env` 讀取的 `GOOGLE_CREDENTIALS` 是否能正確解析。

---

## 安裝與使用

### 1. 建立並啟動虛擬環境

```bash
# Python 3.9+ 建議 (3.10或3.11也可)
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 2. 安裝套件

```bash
pip install -r requirements.txt
```

### 3. 設定環境變數 (.env)

- 在根目錄下有 `.env` 檔案，內含 `GOOGLE_CREDENTIALS` (JSON 字串) 與 `VALID_API_KEY` 等變數。  
- **請勿**公開此檔案，以免外洩機密憑證。

範例：
```bash
GOOGLE_CREDENTIALS={"type":"service_account", ...}
VALID_API_KEY=your-secret-key
```

### 4. 啟動 FastAPI

```bash
uvicorn app.main:app --reload
```
打開 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 查看自動生成的 API 文件。

如需 API Key 驗證，可在 Headers 中加入 `X-API-Key: your-secret-key`。

### 5. 命令列操作 (CLI)

```bash
python cli.py list-members
```
列出目前資料庫中的學員資料。

### 6. 圖形介面 (PyQt5)

```bash
python gui.py
```
彈出桌面視窗，可執行「列出學員」、「重新整理」、「搜尋」、「匯出 CSV」等操作。

### 7. ETL 流程

```bash
python etl.py
```
- 讀取 Google 試算表 (透過 GOOGLE_CREDENTIALS)，清洗資料後寫入 `course_data.db`，並存到 `final_data.csv`。

---

## Docker 部署 (可選)

1. **建置映像**  
   ```bash
   docker build -t course_management:latest .
   ```
2. **執行容器**  
   ```bash
   docker run -p 8000:8000 course_management:latest
   ```
   - 打開瀏覽器至 http://127.0.0.1:8000/docs 瀏覽 API 文件。

> **注意**：若在容器中需要使用 Google Sheets 功能，須透過環境變數或掛載檔案方式提供 `GOOGLE_CREDENTIALS`，並可能需要特殊網路設定。

---

## 測試

- **單元測試**  
  - `tests/test_members.py`：檢驗 CRUD 與資料庫模型。  
  - `tests/test_credentials_env.py`：檢測 `.env` 內 `GOOGLE_CREDENTIALS` 格式是否正確可解析。
  
執行方式：
```bash
pytest tests/
```
或
```bash
python -m pytest
```
(需安裝 pytest 等測試框架)

---

## 注意事項

1. **憑證安全**  
   - `.env` 檔案與 Service Account 憑證**勿**上傳到公開 Repo。  
   - 這裡以範例形式展示，實際請確保 `.gitignore` 內忽略 `.env`、`credentials.json`。

2. **資料庫檔案**  
   - `course_data.db` 若不屬於範例資料庫或不需一同上傳，可忽略或放入 `.gitignore`。

3. **FuzzyWuzzy 警示**  
   - 若執行 ETL 時出現 `Using slow pure-python SequenceMatcher. Install python-Levenshtein to remove this warning`，可於虛擬環境下執行：
     ```bash
     pip install python-Levenshtein
     ```
     以獲得更佳效能。

---

## 參考

- [FastAPI 官方文件](https://fastapi.tiangolo.com/)
- [Click 官方文件](https://click.palletsprojects.com/)
- [PyQt5 官方文件](https://pypi.org/project/PyQt5/)
- [gspread 官方文件](https://docs.gspread.org/en/latest/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [Dockerfile for Python](https://docs.docker.com/language/python/build-images/)
