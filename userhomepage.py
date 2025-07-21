import tkinter as tk
from tkinter import messagebox, filedialog
import os
import sqlite3

class HomePage:
    def __init__(self, root, username, role):
        self.root = root
        self.username = username
        self.role = role

        self.root.title("Workspace Management System")
        self.root.geometry("800x500")
        self.root.configure(bg="#f0f0f0")

        self.conn = sqlite3.connect('workspace.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.record_attendance()

        # Top Frame
        top_frame = tk.Frame(self.root, bg="#4a4a4a", height=50)
        top_frame.pack(fill=tk.X)

        welcome_label = tk.Label(top_frame, text=f"Welcome, {self.username}", font=("Arial", 12), fg="white", bg="#4a4a4a")
        welcome_label.pack(side=tk.RIGHT, padx=10)

        # Sidebar
        sidebar_frame = tk.Frame(self.root, bg="#333333", width=200)
        sidebar_frame.pack(fill=tk.Y, side=tk.LEFT)

        tk.Label(sidebar_frame, text="Menu", font=("Arial", 14), bg="#333333", fg="white").pack(pady=10)

        if self.role == 'user':
            self.create_button(sidebar_frame, "View Tasks (To-Do List)", self.view_tasks)
            self.create_button(sidebar_frame, "Submit Tasks", self.submit_tasks)
            self.create_button(sidebar_frame, "View Files", self.view_files)
            self.create_button(sidebar_frame, "Attendance", self.view_attendance)
            self.create_button(sidebar_frame, "Logout", self.logout)

        # Main Content Area
        self.main_content = tk.Frame(self.root, bg="white")
        self.main_content.pack(fill=tk.BOTH, expand=True)

    def create_button(self, parent, text, command):
        tk.Button(parent, text=text, font=("Arial", 12), bg="#555555", fg="white", command=command,
                  relief=tk.FLAT, width=20, pady=5).pack(pady=5)

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Attendance (username TEXT, date TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Files (username TEXT, filename TEXT, filetype TEXT)''')
        self.conn.commit()

    def record_attendance(self):
        from datetime import date
        today = date.today().strftime('%Y-%m-%d')
        self.cursor.execute('''INSERT INTO Attendance (username, date) VALUES (?, ?)''', (self.username, today))
        self.conn.commit()

    def view_tasks(self):
        self.show_message("View Tasks functionality is under development.")

    def submit_tasks(self):
        file_path = filedialog.askopenfilename(title="Select a file")
        if file_path:
            filename = os.path.basename(file_path)
            filetype = filename.split('.')[-1].lower()
            if filetype in ['doc', 'docx', 'pdf', 'ppt', 'pptx']:
                self.cursor.execute('''INSERT INTO Files (username, filename, filetype) VALUES (?, ?, ?)''',
                                    (self.username, filename, filetype))
                self.conn.commit()
                self.show_message(f"File '{filename}' uploaded successfully!")
            else:
                self.show_message("Invalid file type. Please upload Word, PDF, or PPT files.")

    def view_files(self):
        self.show_message("View Files functionality is under development.")

    def view_attendance(self):
        self.show_message("View Attendance functionality is under development.")

    def logout(self):
        self.root.destroy()

    def show_message(self, message):
        messagebox.showinfo("Information", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = HomePage(root, username="user1", role="user")
    root.mainloop()
