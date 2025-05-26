import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os

DATA_FILE = "simple_users.json"

# Load users
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        users = json.load(f)
else:
    users = {}

# Save users
def save_users():
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# Register window
def open_register():
    def register_user():
        username = user_entry.get()
        password = pass_entry.get()

        if username in users:
            messagebox.showerror("Error", "Username already exists.")
        else:
            users[username] = {
                "password": password,
                "vault": {}
            }
            save_users()
            messagebox.showinfo("Success", "Registered successfully.")
            reg.destroy()

    reg = tk.Toplevel(root)
    reg.title("Register")

    tk.Label(reg, text="Username").pack()
    user_entry = tk.Entry(reg)
    user_entry.pack()

    tk.Label(reg, text="Password").pack()
    pass_entry = tk.Entry(reg, show="*")
    pass_entry.pack()

    tk.Button(reg, text="Register", command=register_user).pack(pady=10)

# Vault window
def open_vault(username):
    vault = tk.Toplevel(root)
    vault.title(f"{username}'s Vault")

    def add_entry():
        service = simpledialog.askstring("Service", "Enter service name:")
        user = simpledialog.askstring("Username", "Enter username for the service:")
        pwd = simpledialog.askstring("Password", "Enter password for the service:")

        if service and user and pwd:
            users[username]["vault"][service] = {
                "username": user,
                "password": pwd
            }
            save_users()
            list_services()

    def list_services():
        for widget in frame.winfo_children():
            widget.destroy()

        for service, data in users[username]["vault"].items():
            tk.Label(frame, text=f"{service} | {data['username']} | {data['password']}").pack()

    tk.Button(vault, text="Add Entry", command=add_entry).pack(pady=5)
    frame = tk.Frame(vault)
    frame.pack(pady=5)
    list_services()

# Login function
def login():
    username = username_entry.get()
    password = password_entry.get()

    if username in users and users[username]["password"] == password:
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        open_vault(username)
    else:
        messagebox.showerror("Login Failed", "Invalid credentials.")

# Main UI
root = tk.Tk()
root.title("Simple Password Manager")

tk.Label(root, text="Username").pack()
username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root, text="Password").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

tk.Button(root, text="Login", command=login).pack(pady=5)
tk.Button(root, text="Register", command=open_register).pack(pady=5)

root.mainloop()