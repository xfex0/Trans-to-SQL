import tkinter as tk
from tkinter import simpledialog, messagebox
import config

def edit_db_config():
    new_server = simpledialog.askstring("Edit Server", "Enter new server:", initialvalue=config.server)
    new_db = simpledialog.askstring("Edit Database", "Enter new database:", initialvalue=config.database)
    new_user = simpledialog.askstring("Edit Username", "Enter new username:", initialvalue=config.username)
    new_pass = simpledialog.askstring("Edit Password", "Enter new password:", initialvalue=config.password)

    if new_server and new_db and new_user and new_pass:
        lines = []
        with open("config.py", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("server ="):
                    line = f"server = '{new_server}'\n"
                elif line.startswith("database ="):
                    line = f"database = '{new_db}'\n"
                elif line.startswith("username ="):
                    line = f"username = '{new_user}'\n"
                elif line.startswith("password ="):
                    line = f"password = '{new_pass}'\n"
                lines.append(line)
        with open("config.py", "w", encoding="utf-8") as f:
            f.writelines(lines)
        messagebox.showinfo("Success", "Database config updated. Please restart the app.")

def edit_app_config():
    new_table_dbf = simpledialog.askstring("DBF Table", "DBF table name:", initialvalue=config.table_name_dbf)
    new_table_excel = simpledialog.askstring("Excel Table", "Excel table name:", initialvalue=config.table_name_excel)
    new_table_datappm = simpledialog.askstring("Datappm Table", "Datappm table name:", initialvalue=config.table_name_datappm)
    new_table_finmap = simpledialog.askstring("Finmap Table", "Finmap table name:", initialvalue=config.table_name_finmap)
    new_token = simpledialog.askstring("Telegram Token", "Telegram BOT token:", initialvalue=config.TOKEN)
    new_chat_id = simpledialog.askstring("Telegram Chat ID", "Telegram Chat ID:", initialvalue=config.CHAT_ID)

    if all([new_table_dbf, new_table_excel, new_table_datappm, new_table_finmap, new_token, new_chat_id]):
        lines = []
        with open("config.py", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("table_name_dbf"):
                    line = f"table_name_dbf = '{new_table_dbf}'\n"
                elif line.startswith("table_name_excel"):
                    line = f"table_name_excel = '{new_table_excel}'\n"
                elif line.startswith("table_name_datappm"):
                    line = f"table_name_datappm = '{new_table_datappm}'\n"
                elif line.startswith("table_name_finmap"):
                    line = f"table_name_finmap = '{new_table_finmap}'\n"
                elif line.startswith("TOKEN"):
                    line = f"TOKEN = '{new_token}'\n"
                elif line.startswith("CHAT_ID"):
                    line = f"CHAT_ID = '{new_chat_id}'\n"
                lines.append(line)
        with open("config.py", "w", encoding="utf-8") as f:
            f.writelines(lines)
        messagebox.showinfo("Success", "App config updated. Please restart the app.")
