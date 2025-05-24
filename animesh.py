import tkinter as tk
from tkinter import messagebox
import json
import os
import ctypes
import subprocess
import requests
import threading

SERVER_URL = "https://updatebunk.onrender.com"  # Change to your server address
PING_INTERVAL = 30

class StudentClient:
    def __init__(self):
        self.username = None
        self.root = tk.Tk()
        self.setup_login_ui()
        self.start_ping_thread()
        self.root.mainloop()

    def setup_login_ui(self):
        self.root.title("Student Login")
        self.root.geometry("300x200")
        
        tk.Label(self.root, text="Username:").pack(pady=5)
        self.entry_username = tk.Entry(self.root)
        self.entry_username.pack(pady=5)
        
        tk.Label(self.root, text="Password:").pack(pady=5)
        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.pack(pady=5)
        
        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if not username or not password:
            messagebox.showwarning("Error", "Please enter both username and password")
            return
            
        # In a real app, verify credentials properly
        self.username = username
        self.root.destroy()
        self.start_attendance_timer()

    def start_ping_thread(self):
        def ping():
            while True:
                if self.username:
                    try:
                        requests.post(
                            f"{SERVER_URL}/ping",
                            json={"type": "students", "username": self.username}
                        )
                    except:
                        pass
                threading.Event().wait(PING_INTERVAL)
        
        threading.Thread(target=ping, daemon=True).start()

    def start_attendance_timer(self):
        # Similar to original attendance timer but with server updates
        attendance_window = tk.Tk()
        attendance_window.title("Attendance Timer")
        
        def mark_present():
            try:
                requests.post(
                    f"{SERVER_URL}/attendance",
                    json={"username": self.username, "status": "present"}
                )
                messagebox.showinfo("Success", "Attendance marked!")
            except:
                messagebox.showerror("Error", "Failed to update attendance")
        
        tk.Label(attendance_window, text="Click to mark attendance").pack(pady=20)
        tk.Button(attendance_window, text="Mark Present", command=mark_present).pack(pady=10)
        attendance_window.mainloop()

if __name__ == "__main__":
    StudentClient()
