import tkinter  as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os

KEYS_FILE = "api_keys.json"

# --- FUNCTIONS ---
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
            messagebox.showinfo("Success", f"Key '{new_key}' added to the list!")

def update_api_list():
    api_listbox.delete(0, tk.END)
    for idx, key in enumerate(api_keys, start=1):
        api_listbox.insert(tk.END, f"{idx}. {key}")

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
            messagebox.showinfo("Success", f"Key '{selected_key}' deleted.")
        else:
            messagebox.showerror("Error", "Key not found.")
    else:
        messagebox.showwarning("Attention", "Please select a key first.")

def show_pass():
    # Тимчасово покажемо заглушку, бо password не визначено
    messagebox.showinfo("Password", "Password is not available.")

def update_combobox():
    combo['values'] = api_keys
    combo.set('')

def run_all_tasks():
    messagebox.showinfo("Start", "Simulation: All tasks running...")

# --- MAIN GUI ---
def create_gui():
    global api_keys, combo, api_listbox
    api_keys = load_keys()

    root = tk.Tk()
    root.title("Upload data to SQL")
    root.geometry("600x500")

    label = tk.Label(root, text="Press Start to begin operations", font=("Arial", 14))
    label.pack(pady=10)

    btn_add = tk.Button(root, text="Add API-key", command=add_api_key, font=("Arial", 14), bg="green", fg="white")
    btn_add.pack(pady=5)

    api_listbox = tk.Listbox(root, width=60)
    api_listbox.pack(pady=5)

    btn_start = tk.Button(root, text="Start", command=run_all_tasks, font=("Arial", 14), bg="green", fg="white")
    btn_start.pack(pady=5)

    btn_show = tk.Button(root, text="Show List", command=show_api_list, font=("Arial", 14), bg="green", fg="white")
    btn_show.pack(pady=5)

    btn_del = tk.Button(root, text="Delete API-key", command=del_api_key_from_list, font=("Arial", 14), bg="green", fg="white")
    btn_del.pack(pady=5)

    btn_pass = tk.Button(root, text="Show Password", command=show_pass, font=("Arial", 14), bg="green", fg="white")
    btn_pass.pack(pady=5)

    combo = ttk.Combobox(root, state="readonly", width=50)
    combo.pack(pady=5)
    update_combobox()

    root.mainloop()

if __name__ == "__main__":
    create_gui()