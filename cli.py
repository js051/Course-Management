# cli.py
import click
from rich.console import Console
from rich.table import Table
from app.database import SessionLocal
from app import crud

console = Console()

@click.group()
def cli():
    """課程資料管理 CLI 工具"""
    pass

@cli.command()
@click.option('--skip', default=0, help='從第幾筆開始')
@click.option('--limit', default=100, help='取得幾筆資料')
def list_members(skip, limit):
    """
    列出所有學員資料，並以表格格式顯示。
    """
    db = SessionLocal()
    members = crud.get_members(db, skip=skip, limit=limit)
    table = Table(title="學員資料")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("姓名", style="magenta")
    table.add_column("Email", style="green")
    table.add_column("所屬單位", style="yellow")
    table.add_column("電話", style="blue")
    
    for member in members:
        table.add_row(
            member.id,
            member.name,
            member.email or "-",
            member.affiliation or "-",
            member.phone or "-"
        )
    
    console.print(table)
    db.close()

if __name__ == "__main__":
    cli()
