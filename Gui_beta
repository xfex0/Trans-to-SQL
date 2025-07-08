import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import json
import os
import config
from api_keys_manager import load_keys as ext_load_keys, save_keys as ext_save_keys
from dbf_handler import process_all_dbf_files
from excel_handler import read_excel_and_upload
from datappm_sync import sync_excel_to_sql, sync_sql_to_excel, compare_excel_sql
from finmap_loader import load_finmap_to_sql

KEYS_FILE = "api_keys.json"

# --- Функції роботи з ключами API ---
def load_keys():
    if os.path.exists(KEYS_FILE):
        with open(KEYS_FILE, "r") as f:
            return json.load(f)
    return []

def save_keys():
    with open(KEYS_FILE, "w") as f:
        json.dump(api_keys, f)

def add_api_key():
    global api_keys
    new_key = simpledialog.askstring("Add new API-key", "Enter new API-key:")
    if new_key:
        if new_key in api_keys:
            messagebox.showwarning("Warning", "This key is already in the list.")
        else:
            api_keys.append(new_key)
            save_keys()
            update_combobox()
            update_api_list()
            messagebox.showinfo("Success", f"Key '{new_key}' added to the list!")

def show_api_list():
    if api_keys:
        keys_text = "\n".join(f"{i+1}. {key}" for i, key in enumerate(api_keys))
    else:
        keys_text = "API-keys list is empty"
    messagebox.showinfo("API-keys list", keys_text)

def del_api_key_from_list():
    global api_keys
    selected_key = combo.get()
    if selected_key:
        if selected_key in api_keys:
            api_keys.remove(selected_key)
            save_keys()
            update_combobox()
            update_api_list()
            messagebox.showinfo("Success", f"Key '{selected_key}' deleted.")
        else:
            messagebox.showerror("Error", "Key not found.")
    else:
        messagebox.showwarning("Attention", "Please select a key first.")

def update_combobox():
    combo['values'] = api_keys
    combo.set('')

def update_api_list():
    api_listbox.delete(0, tk.END)
    for idx, key in enumerate(api_keys, start=1):
        api_listbox.insert(tk.END, f"{idx}. {key}")

def show_pass():
    messagebox.showinfo("Password", "Password is not available.")

def run_all_tasks():
    messagebox.showinfo("Start", "Simulation: All tasks running...")

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

def create_gui():
    global api_keys, combo, api_listbox
    api_keys = load_keys()

    root = tk.Tk()
    root.title("Upload data to SQL")
    root.geometry("900x500")

    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    menu_frame = tk.Frame(main_frame, bg="#f0f0f0", width=200)
    menu_frame.pack(side="left", fill="y")

    content_frame = tk.Frame(main_frame, bg="white")
    content_frame.pack(side="right", fill="both", expand=True)

    def clear_content():
        for widget in content_frame.winfo_children():
            widget.destroy()

    def load_start_screen():
        clear_content()
        label = tk.Label(content_frame, text="Press Start to begin operations", font=("Arial", 14))
        label.pack(pady=10)
        btn_start = tk.Button(content_frame, text="Start", command=run_all_tasks, font=("Arial", 14), bg="green", fg="white")
        btn_start.pack(pady=5)

    def load_api_manager():
        clear_content()
        tk.Button(content_frame, text="Add API-key", command=add_api_key, font=("Arial", 14), bg="green", fg="white").pack(pady=5)
        tk.Label(content_frame, text="Select API-key to delete:").pack()
        combo = ttk.Combobox(content_frame, state="readonly", width=50)
        combo.pack(pady=5)
        update_combobox()
        tk.Button(content_frame, text="Delete API-key", command=del_api_key_from_list, font=("Arial", 14), bg="red", fg="white").pack(pady=5)
        tk.Label(content_frame, text="All API-keys:").pack()
        api_listbox = tk.Listbox(content_frame, width=60)
        api_listbox.pack(pady=5)
        update_api_list()

    def load_server_config():
        clear_content()
        tk.Button(content_frame, text="Edit DB Config", command=edit_db_config, font=("Arial", 14), bg="green", fg="white").pack(pady=10)
        tk.Button(content_frame, text="Edit APP Config", command=edit_app_config, font=("Arial", 14), bg="blue", fg="white").pack(pady=10)

    def load_file_source():
        clear_content()
        label = tk.Label(content_frame, text="File Source configuration placeholder", font=("Arial", 14))
        label.pack(pady=20)

    tk.Button(menu_frame, text="Start", width=25, height=2, command=load_start_screen).pack(pady=2)
    tk.Button(menu_frame, text="Server Authenticator", width=25, height=2, command=load_server_config).pack(pady=2)
    tk.Button(menu_frame, text="API Source", width=25, height=2, command=load_api_manager).pack(pady=2)
    tk.Button(menu_frame, text="File Source", width=25, height=2, command=load_file_source).pack(pady=2)

    load_start_screen()
    root.mainloop()

# Запуск GUI
create_gui()
