# dbf_handler.py
import os
import pandas as pd
from dbfread import DBF
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from config import table_name_dbf, watch_folder
from db_engine import engine
from telegram_utils import send_telegram_message

def read_dbf_to_df(file_path):
    try:
        table = DBF(file_path, encoding='cp1251')
        return pd.DataFrame(iter(table))
    except Exception as e:
        print(f"DBF read error: {e}")
        return None

def upload_dbf_to_sql(file_path):
    df = read_dbf_to_df(file_path)
    if df is None or df.empty:
        return
    df["source_file"] = os.path.basename(file_path)
    try:
        with engine.begin() as conn:
            for _, row in df.iterrows():
                cols = ', '.join(df.columns)
                placeholders = ', '.join(f":{col}" for col in df.columns)
                query = text(f"INSERT INTO {table_name_dbf} ({cols}) VALUES ({placeholders})")
                conn.execute(query, {col: row[col] for col in df.columns})
        print(f"✅ DBF uploaded: {file_path}")
    except SQLAlchemyError as e:
        print(f"SQL error: {e}")

def process_all_dbf_files():
    files = sorted([
        os.path.join(watch_folder, f)
        for f in os.listdir(watch_folder) if f.endswith('.dbf')
    ], key=os.path.getmtime)
    for file in files:
        upload_dbf_to_sql(file)