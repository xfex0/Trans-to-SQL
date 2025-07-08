# datappm_sync.py

import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from db_engine import engine
from config import server, database, username, password, excel_path, table_name_datappm
import requests
from telegram_utils import send_telegram_message


def sync_excel_to_sql():
    if not os.path.exists(excel_path):
        print(f"❌ Excel файл не знайдено: {excel_path}")
        send_telegram_message(f"❌ Excel файл не знайдено: {excel_path}")
        return

    df = pd.read_excel(excel_path)
    df.columns = [col.strip().replace(" ", "_") for col in df.columns]
    sql_columns = df.columns.tolist()

    for col in sql_columns:
        if 'amount' in col.lower() or 'sum' in col.lower():
            df[col] = pd.to_numeric(df[col], errors='coerce').round(6)

    columns_str = ', '.join([f"[{col}]" for col in sql_columns])
    placeholders = ', '.join([f":{col}" for col in sql_columns])

    inserted_count = 0
    with engine.begin() as conn:
        for _, row in df.iterrows():
            project_val = row.get("project", None)
            if not project_val:
                continue

            res = conn.execute(
                text(f"SELECT COUNT(*) FROM {table_name_datappm} WHERE project = :project"),
                {"project": project_val}
            )
            if res.scalar() > 0:
                continue

            params = {col: row[col] for col in sql_columns}
            try:
                conn.execute(
                    text(f"""
                        INSERT INTO {table_name_datappm} ({columns_str})
                        VALUES ({placeholders})
                    """),
                    params
                )
                inserted_count += 1
            except SQLAlchemyError as e:
                print(f"⚠️ Пропущено рядок: {e}")

    send_telegram_message(f"✅ Додано до SQL: {inserted_count} рядків")

# === Синхронізація SQL → datappm Excel ===
def sync_sql_to_excel():
    df_sql = pd.read_sql(f"SELECT * FROM {table_name_datappm}", engine)
    df_sql.columns = [col.strip().replace(" ", "_") for col in df_sql.columns]

    if os.path.exists(excel_path):
        df_excel = pd.read_excel(excel_path)
        df_excel.columns = [col.strip().replace(" ", "_") for col in df_excel.columns]

        if "project" not in df_excel.columns:
            print("❌ Excel не має колонки 'project'")
            send_telegram_message("❌ Excel не має колонки 'project'")
            return

        new_rows = df_sql[~df_sql["project"].isin(df_excel["project"])]
        if not new_rows.empty:
            df_combined = pd.concat([df_excel, new_rows], ignore_index=True)
            df_combined.to_excel(excel_path, index=False)
            send_telegram_message(f"🔄 Excel оновлено: додано {len(new_rows)} нових рядків")
        else:
            send_telegram_message("ℹ️ Дані з SQL вже є в Excel. Нових рядків не знайдено.")
    else:
        df_sql.to_excel(excel_path, index=False)
        send_telegram_message(f"📄 Excel створено з SQL ({len(df_sql)} рядків)")

# === Порівняння Excel і SQL ===
def compare_excel_sql():
    if not os.path.exists(excel_path):
        send_telegram_message("❌ Excel файл не знайдено.")
        return

    df_excel = pd.read_excel(excel_path)
    df_excel.columns = [col.strip().replace(" ", "_") for col in df_excel.columns]

    df_sql = pd.read_sql(f"SELECT * FROM {table_name_datappm}", engine)
    df_sql.columns = [col.strip().replace(" ", "_") for col in df_sql.columns]

    excel_cols = set(df_excel.columns)
    sql_cols = set(df_sql.columns)
    only_in_excel = excel_cols - sql_cols
    only_in_sql = sql_cols - excel_cols

    new_in_excel = df_excel[~df_excel["project"].isin(df_sql["project"])]
    new_in_sql = df_sql[~df_sql["project"].isin(df_excel["project"])]

    message = "📊 *Порівняння Excel і SQL:*\n"
    if only_in_excel:
        message += f"➕ *У Excel, але не в SQL:* {', '.join(only_in_excel)}\n"
    if only_in_sql:
        message += f"➕ *У SQL, але не в Excel:* {', '.join(only_in_sql)}\n"
    message += f"📈 Нові рядки у Excel (відсутні в SQL): {len(new_in_excel)}\n"
    message += f"📉 Нові рядки в SQL (відсутні в Excel): {len(new_in_sql)}"

    send_telegram_message(message)