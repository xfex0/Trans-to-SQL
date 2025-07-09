# excel_handler.py
import os
import pandas as pd
from sqlalchemy import text
from config import excel_folder, table_name_excel
from db_engine import engine
from telegram_utils import send_telegram_message

def read_excel_and_upload(folder_path=excel_folder):
    for file in os.listdir(folder_path):
        if not file.endswith(('.xls', '.xlsx')):
            continue
        file_path = os.path.join(folder_path, file)

        with engine.connect() as conn:
            res = conn.execute(
                text(f"SELECT COUNT(*) FROM {table_name_excel} WHERE source_file = :file"),
                {"file": file}
            )
            if res.scalar():
                continue

        try:
            df = pd.read_excel(file_path, header=None)
            # ... обробка рядків ...
            # вставка даних у SQL
        except Exception as e:
            send_telegram_message(f"❌ Excel error: {e}")