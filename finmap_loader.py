#finmap_loader
import requests
from datetime import datetime
from dateutil import parser
from sqlalchemy import create_engine, text
import config
from config import finmap_url, finmap_headers, table_name_finmap
from telegram_utils import send_telegram_message
from db_engine import engine




def load_finmap_to_sql():
    try:
        payload = {"filters": {}, "page": 1, "limit": 100}
        response = requests.post(finmap_url, headers=finmap_headers, json=payload)
        response.raise_for_status()
        data = response.json()
        operations = data.get('list', [])

        if not operations:
            send_telegram_message("ℹ️ Finmap: Дані операцій відсутні.")
            return

        with engine.begin() as conn:
            inserted_count = 0
            for op in operations:
                # === Обробка дати ===
                raw_date = op.get('date')
                date = None
                try:
                    if isinstance(raw_date, (int, float)):
                        date = datetime.fromtimestamp(raw_date / 1000)
                    elif isinstance(raw_date, str):
                        date = parser.parse(raw_date)
                except Exception as e:
                    print(f"❗ Неможливо розпарсити дату: {raw_date} — {e}")
                    continue

                # === Інші поля ===
                amount = op.get('sum', 0)

                project = op.get('project') or ''
                account_info = op.get('account', {})
                account = account_info.get('title', '') or ''
                balance = account_info.get('balance')
                if isinstance(balance, str):
                    try:
                        balance = float(balance.replace(' ', '').replace(',', '.'))
                    except:
                        balance = None

                counterparty = op.get('counterparty', {}).get('title', '') or ''
                category = op.get('category', {}).get('title', '') or ''
                description = op.get('comment') or ''
                currency = op.get('currency') or ''

                # === Унікальність — з урахуванням balance ===
                exists_query = text(f"""
                    SELECT COUNT(*) FROM {table_name_finmap}
                    WHERE 
                        date = :date AND 
                        amount = :amount AND 
                        project = :project AND 
                        account = :account AND
                        counterparty = :counterparty AND
                        category = :category AND 
                        description = :description AND 
                        currency = :currency AND
                        (balance = :balance OR (balance IS NULL AND :balance IS NULL))
                """)
                res = conn.execute(exists_query, {
                    "date": date,
                    "amount": amount,
                    "project": project,
                    "account": account,
                    "counterparty": counterparty,
                    "category": category,
                    "description": description,
                    "currency": currency,
                    "balance": balance
                })

                if res.scalar() > 0:
                    continue

                # === Вставка ===
                insert_query = text(f"""
                    INSERT INTO {table_name_finmap} 
                        (date, amount, project, account, counterparty, category, description, currency, balance)
                    VALUES 
                        (:date, :amount, :project, :account, :counterparty, :category, :description, :currency, :balance)
                """)
                conn.execute(insert_query, {
                    "date": date,
                    "amount": amount,
                    "project": project,
                    "account": account,
                    "counterparty": counterparty,
                    "category": category,
                    "description": description,
                    "currency": currency,
                    "balance": balance
                })
                inserted_count += 1

        send_telegram_message(f"✅ Finmap: Завантажено {inserted_count} нових операцій")

    except Exception as e:
        send_telegram_message(f"❌ Finmap API error: {e}")