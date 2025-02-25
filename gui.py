# gui.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QHBoxLayout, QLineEdit
)
from app.database import SessionLocal
from app import crud
import pandas as pd
from app.config import config

# ← 新增: 從 etl 模組匯入 etl_process 函式
from etl import etl_process

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("課程資料管理系統")
        self.resize(900, 600)
        self.init_ui()
    
    def init_ui(self):
        # 主垂直布局
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # 按鈕水平布局
        btn_layout = QHBoxLayout()
        self.layout.addLayout(btn_layout)
        
        # 「列出學員」按鈕
        self.btn_list = QPushButton("列出學員")
        self.btn_list.clicked.connect(self.load_members)
        btn_layout.addWidget(self.btn_list)
        
        # 「重新整理」按鈕
        self.btn_refresh = QPushButton("重新整理")
        self.btn_refresh.clicked.connect(self.load_members)
        btn_layout.addWidget(self.btn_refresh)
        
        # 「更新資料庫」按鈕  ← 新增
        self.btn_update = QPushButton("更新資料庫")
        self.btn_update.clicked.connect(self.update_database)
        btn_layout.addWidget(self.btn_update)

        # 搜尋輸入與「搜尋」按鈕（如有需要）
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("輸入姓名或單位搜尋...")
        btn_layout.addWidget(self.search_input)

        self.btn_search = QPushButton("搜尋")
        self.btn_search.clicked.connect(self.search_members)
        btn_layout.addWidget(self.btn_search)
        
        # 「匯出 CSV」按鈕
        self.btn_export = QPushButton("匯出 CSV")
        self.btn_export.clicked.connect(self.export_to_csv)
        btn_layout.addWidget(self.btn_export)
        
        # 資料表格
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
    
    def load_members(self):
        """
        從資料庫讀取學員資料，並更新表格內容。
        """
        try:
            db = SessionLocal()
            members = crud.get_members(db)
            db.close()
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"讀取資料失敗：{str(e)}")
            return
        
        if not members:
            QMessageBox.information(self, "訊息", "目前沒有學員資料。")
            self.table.setRowCount(0)
            return
        
        self.table.setRowCount(len(members))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "姓名", "Email", "所屬單位", "電話"])
        
        for row, member in enumerate(members):
            self.table.setItem(row, 0, QTableWidgetItem(member.id))
            self.table.setItem(row, 1, QTableWidgetItem(member.name))
            self.table.setItem(row, 2, QTableWidgetItem(member.email or "-"))
            self.table.setItem(row, 3, QTableWidgetItem(member.affiliation or "-"))
            self.table.setItem(row, 4, QTableWidgetItem(member.phone or "-"))
    
    def update_database(self):  # ← 新增
        """
        透過呼叫 etl_process() 更新本地資料庫，並重新載入列表。
        """
        try:
            etl_process()  # 呼叫 etl.py 中的 ETL 流程
            QMessageBox.information(self, "成功", "資料庫已更新並重新載入。")
            self.load_members()  # 更新完成後，再次載入以顯示最新資料
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"更新資料失敗：{str(e)}")
    
    def search_members(self):
        """
        根據搜尋欄位輸入內容搜尋學員資料。
        """
        keyword = self.search_input.text()
        db = SessionLocal()
        from sqlalchemy import or_
        from app.models import Member
        members = db.query(Member).filter(
            or_(Member.name.contains(keyword), Member.affiliation.contains(keyword))
        ).all()
        db.close()
        
        self.table.setRowCount(len(members))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "姓名", "Email", "所屬單位", "電話"])
        for row, member in enumerate(members):
            self.table.setItem(row, 0, QTableWidgetItem(member.id))
            self.table.setItem(row, 1, QTableWidgetItem(member.name))
            self.table.setItem(row, 2, QTableWidgetItem(member.email or "-"))
            self.table.setItem(row, 3, QTableWidgetItem(member.affiliation or "-"))
            self.table.setItem(row, 4, QTableWidgetItem(member.phone or "-"))
    
    def export_to_csv(self):
        """
        將資料庫中的學員資料匯出為 CSV 檔案。
        """
        db = SessionLocal()
        members = crud.get_members(db)
        db.close()
        # 將 ORM 物件轉換為字典列表，再用 Pandas 寫入 CSV
        data = [m.__dict__ for m in members]
        df = pd.DataFrame(data)
        df.to_csv(config.EXPORT_PATH, index=False, encoding="utf-8-sig")
        QMessageBox.information(self, "成功", f"資料已匯出至 {config.EXPORT_PATH}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
