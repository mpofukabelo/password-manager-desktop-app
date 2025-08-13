import tkinter as tk
from tkinter import simpledialog, messagebox
import json, os, hashlib

DATA_FILE = "simple_users.json"

# Hash password function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load users from file
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        users = json.load(f)
else:
    users = {}

# Save users to file
def save_users():
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

# Apply dark theme colors
BG_COLOR = "#1e1e1e"  # Dark background
FG_COLOR = "#ffffff"  # White text
BUTTON_COLOR = "#3c3f41"
ENTRY_BG = "#2d2d2d"
ENTRY_FG = "#ffffff"
HIGHLIGHT = "#4e9a06"  # Green highlight

# Registration window
def open_register():
    def register_user():
        username = user_entry.get().strip()
        password = pass_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "All fields required!")
        elif username in users:
            messagebox.showerror("Error", "Username already exists!")
        else:
            users[username] = {
                "password": hash_password(password),
                "vault": {}
            }
            save_users()
            messagebox.showinfo("Success", "Registered successfully!")
            reg.destroy()

    reg = tk.Toplevel(root)
    reg.title("Register")
    reg.configure(bg=BG_COLOR)

    tk.Label(reg, text="Username:", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 11, "bold")).pack(pady=3)
    user_entry = tk.Entry(reg, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR)
    user_entry.pack(pady=3)

    tk.Label(reg, text="Password:", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 11, "bold")).pack(pady=3)
    pass_entry = tk.Entry(reg, show="*", bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR)
    pass_entry.pack(pady=3)

    tk.Button(reg, text="Register", command=register_user, bg=BUTTON_COLOR, fg=FG_COLOR, activebackground=HIGHLIGHT).pack(pady=10)

# Vault window
def open_vault(username):
    vault = tk.Toplevel(root)
    vault.title(f"{username}'s Vault")
    vault.configure(bg=BG_COLOR)

    def add_entry():
        service = simpledialog.askstring("Service", "Service name:")
        user = simpledialog.askstring("Username", "Service username:")
        pwd = simpledialog.askstring("Password", "Service password:")

        if service and user and pwd:
            users[username]["vault"][service] = {"username": user, "password": pwd}
            save_users()
            list_services()

    def list_services():
        for widget in frame.winfo_children():
            widget.destroy()
        if users[username]["vault"]:
            for service, data in users[username]["vault"].items():
                tk.Label(frame, text=f"{service} | {data['username']} | {data['password']}", 
                         bg=BG_COLOR, fg=FG_COLOR, font=("Courier", 10)).pack(anchor="w")
        else:
            tk.Label(frame, text="No entries yet...", bg=BG_COLOR, fg="#bbbbbb", font=("Arial", 10, "italic")).pack()

    def logout():
        vault.destroy()
        messagebox.showinfo("Logout", "You have logged out successfully!")

    tk.Button(vault, text="Add Entry", command=add_entry, bg=BUTTON_COLOR, fg=FG_COLOR, activebackground=HIGHLIGHT).pack(pady=5)
    tk.Button(vault, text="Logout", command=logout, bg=BUTTON_COLOR, fg=FG_COLOR, activebackground=HIGHLIGHT).pack(pady=5)

    frame = tk.Frame(vault, bg=BG_COLOR)
    frame.pack(pady=5, fill="both", expand=True)
    list_services()

# Login function
def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if username in users and users[username]["password"] == hash_password(password):
        messagebox.showinfo("Login Success", f"Welcome {username}!")
        open_vault(username)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password!")

# Main window
root = tk.Tk()
root.title("Secure Password Manager")
root.configure(bg=BG_COLOR)
root.geometry("320x200")

tk.Label(root, text="Username:", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 11, "bold")).pack(pady=3)
username_entry = tk.Entry(root, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR)
username_entry.pack(pady=3)

tk.Label(root, text="Password:", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 11, "bold")).pack(pady=3)
password_entry = tk.Entry(root, show="*", bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR)
password_entry.pack(pady=3)

tk.Button(root, text="Login", command=login, bg=BUTTON_COLOR, fg=FG_COLOR, activebackground=HIGHLIGHT).pack(pady=5)
tk.Button(root, text="Register", command=open_register, bg=BUTTON_COLOR, fg=FG_COLOR, activebackground=HIGHLIGHT).pack(pady=5)

root.mainloop()


