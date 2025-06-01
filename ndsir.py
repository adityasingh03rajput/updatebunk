import tkinter as tk
from tkinter import ttk
import requests
import threading

SERVER_URL = "https://updatebunk.onrender.com"  # Change to your server address
UPDATE_INTERVAL = 5

class TeacherClient:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_ui()
        self.start_update_thread()
        self.root.mainloop()

    def setup_ui(self):
        self.root.title("Teacher Dashboard")
        self.root.geometry("600x400")
        
        self.tree = ttk.Treeview(self.root, columns=("Student", "Status"), show="headings")
        self.tree.heading("Student", text="Student")
        self.tree.heading("Status", text="Status")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Register with server
        self.register_teacher()

    def register_teacher(self):
        try:
            requests.post(
                f"{SERVER_URL}/ping",
                json={"type": "teachers", "username": "teacher"}
            )
        except:
            pass

    def start_update_thread(self):
        def update():
            while True:
                try:
                    response = requests.get(f"{SERVER_URL}/get_attendance")
                    if response.status_code == 200:
                        self.update_table(response.json())
                except:
                    pass
                threading.Event().wait(UPDATE_INTERVAL)
        
        threading.Thread(target=update, daemon=True).start()

    def update_table(self, data):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for student, status in data.items():
            self.tree.insert("", "end", values=(student, status))

if __name__ == "__main__":
    TeacherClient()
