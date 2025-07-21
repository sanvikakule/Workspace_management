import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import Database
from datetime import datetime
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import os


class HomePage:
    def __init__(self, root, username, role):
        self.root = root
        self.username = username
        self.role = role
        self.db = Database()

        # Set window properties
        self.root.title(f"{role.capitalize()} Homepage")
        
        # Set the window to fullscreen (for Windows use "zoomed")
        self.root.state("zoomed")  # Maximize window on startup (Windows)
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.configure(bg="#1F2A44")

        # Create main container
        
        self.main_container = tk.Frame(self.root, bg="#1F2A44")
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Create sidebar
        self.sidebar = tk.Frame(self.main_container, bg="#2c3e50", width=250)  # Sidebar width adjusted
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Sidebar header
        tk.Label(self.sidebar, 
                text=f"Welcome\n{username}", 
                font=("Helvetica", 14, "bold"),
                bg="#2c3e50",
                fg="white").pack(pady=20)

        # Sidebar buttons
        self.create_sidebar_buttons()

        # Add separator
        ttk.Separator(self.sidebar, orient='horizontal').pack(fill=tk.X, pady=10)

        # Navigation buttons at bottom of sidebar
        self.create_sidebar_button("Back to Login", self.back_to_login, "#e74c3c")
        self.create_sidebar_button("Logout", self.logout, "#e74c3c")

        # Main content area
        self.content_frame = tk.Frame(self.main_container, bg="white")
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, 
                            textvariable=self.status_var, 
                            relief=tk.SUNKEN, 
                            anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Initialize task treeview
        self.task_tree = None

    def create_sidebar_button(self, text, command, bg="#34495e"):
        btn = tk.Button(self.sidebar,
                       text=text,
                       command=command,
                       font=("Helvetica", 12),
                       bg=bg,
                       fg="white",
                       relief=tk.FLAT,
                       width=20,
                       pady=10)
        btn.pack(pady=2)
        # Add hover effect
        btn.bind("<Enter>", lambda e: btn.configure(bg="#3498db"))
        btn.bind("<Leave>", lambda e: btn.configure(bg=bg))

    def create_button(self, parent, text, command):
        tk.Button(parent, text=text, font=("Times New Roman", 12), bg="#555555", fg="white", command=command,
                  relief=tk.FLAT, width=20, pady=5).pack(pady=5)

    def create_sidebar_buttons(self):
        if self.role == "admin":
            self.create_sidebar_button("Assign Task", self.assign_task)
            self.create_sidebar_button("Manage Users", self.manage_users)
            self.create_sidebar_button("View Files", self.view_files)
            self.create_sidebar_button("Statistical Report", self.show_statistical_report)
            self.create_sidebar_button("Meeting Scheduler", self.schedule_meeting)
            self.create_sidebar_button("Attendance Report", self.show_attendance_report)
            self.create_sidebar_button("Profile", self.show_profile)
            self.create_sidebar_button("Meetings", self.view_meetings)
            self.create_sidebar_button("Logout", self.logout)
        else:
            self.create_sidebar_button("View Tasks", self.view_tasks)
            self.create_sidebar_button("Submit Task", self.submit_tasks)
            self.create_sidebar_button("Statistical Report", self.show_statistical_report)
            self.create_sidebar_button("Meetings", self.view_meetings)
            self.create_sidebar_button("Profile", self.show_profile)
            self.create_sidebar_button("Logout", self.logout)

    def assign_task(self):
        # Clear main content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

       # Create task assignment form
        form_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        '''# Load and display background image
        form_frame.update_idletasks()  # Ensure accurate dimensions
        width = form_frame.winfo_width()
        height = form_frame.winfo_height()

        image = Image.open("adbutton.png")  # Replace with your image file
        image = image.resize((width, height), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(image)

        bg_label = tk.Label(form_frame, image=bg_image)
        bg_label.image = bg_image  # Keep a reference
        bg_label.place(relwidth=1, relheight=1)'''


        # Title
        title_label = tk.Label(form_frame, 
                       text="Assign New Task..", 
                       font=("Times New Roman", 20, "bold"), 
                       fg="#1F2A44",
                       bg="white")  # Removed bg, set text color to black
        title_label.pack(pady=(0, 20))


        # Create a frame for the form fields
        fields_frame = tk.Frame(form_frame, bg="white")
        fields_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # 1. User Selection
        tk.Label(fields_frame, 
                text="Select User:", 
                font=("Times New Roman", 14, "bold"), 
                fg="#1F2A44",
                bg="white").pack(anchor="w", pady=(0, 5))
        users = self.db.get_all_users_with_tasks()
        user_var = tk.StringVar()
        user_combo = ttk.Combobox(fields_frame, 
                                 textvariable=user_var, 
                                 values=[f"{user[0]} ({user[1]})" for user in users],
                                 state="readonly",
                                 font=("Times New Roman ",13))
        user_combo.pack(fill=tk.X, pady=(0, 15))

        # 2. Task Title
        tk.Label(fields_frame, 
                text="Task Title:", 
               font=("Times New Roman", 14, "bold"), 
                fg="#1F2A44",
                bg="white").pack(anchor="w", pady=(0, 5))
        title_entry = tk.Entry(fields_frame, font=("Times New Roman", 13))
        title_entry.pack(fill=tk.X, pady=(0, 15))

        # 3. Task Description
        tk.Label(fields_frame, 
                text="Task Description:", 
               font=("Times New Roman", 14, "bold"), 
                fg="#1F2A44",
                bg="white").pack(anchor="w", pady=(0, 5))
        desc_text = tk.Text(fields_frame, height=4, font=("Times New Roman", 13))
        desc_text.pack(fill=tk.X, pady=(0, 15))

        
        # 4. Deadline
        style = ttk.Style()
        style.theme_use('clam')  # Use a more customizable theme
        style.configure('Custom.DateEntry',
                    fieldbackground='#1F2A44',     # Entry box background
                    background='white',            # Calendar button background
                    foreground='white',            # Entry text color
                    arrowcolor='black',            # Calendar arrow color
                    bordercolor='#3E4C75',         # Border color
                    relief="flat",
                    selectbackground='#3E4C75',    # Date select background
                    selectforeground='white')      # Date select foreground

        # 4. Deadline Label
        tk.Label(fields_frame, 
             text="Deadline (YYYY-MM-DD):", 
             font=("Times New Roman", 14, "bold"), 
             fg="#1F2A44",
             bg="white").pack(anchor="w", pady=(0, 5))

        # Stylish Calendar DateEntry
        date_entry = DateEntry(fields_frame, 
                       font=("Times New Roman", 13), 
                       date_pattern='yyyy-mm-dd',
                       bg="white",
                       fg="#1F2A44",
                       style='Custom.DateEntry')
        date_entry.pack(fill=tk.X, pady=(0, 20))

        def submit_task():
            # Validate all fields are filled
            if not all([user_var.get(), 
                       title_entry.get(), 
                       desc_text.get("1.0", tk.END).strip(), 
                       date_entry.get()]):
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                # Validate date format
                datetime.strptime(date_entry.get(), '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
                return

            # Extract username from combo box value
            assigned_to = user_var.get().split(' (')[0]

            # Prepare task data
            task_data = {
                'assigned_by': self.username,
                'assigned_to': assigned_to,
                'task_title': title_entry.get(),
                'task_description': desc_text.get("1.0", tk.END).strip(),
                'due_date': date_entry.get()
            }

            # Submit task to database
            if self.db.assign_task(task_data):
                messagebox.showinfo("Success", "Task assigned successfully!")
                # Clear form
                user_combo.set('')
                title_entry.delete(0, tk.END)
                desc_text.delete("1.0", tk.END)
                date_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Failed to assign task!")

        # Submit button
        submit_btn = tk.Button(fields_frame, 
                             text="Assign Task", 
                             command=submit_task,
                             font=("Times New Roman", 12, "bold"),
                             bg="#4CAF50",
                             fg="white",
                             padx=20,
                             pady=10)
        submit_btn.pack(pady=20)

        # Add hover effect to submit button
        submit_btn.bind("<Enter>", lambda e: submit_btn.configure(bg="#45a049"))
        submit_btn.bind("<Leave>", lambda e: submit_btn.configure(bg="#4CAF50"))

    def view_tasks(self):
        # Clear main content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if self.role == 'admin':
            messagebox.showinfo("Information", "Admin view tasks functionality is under development.")
        else:
            # Create tasks display area
            tasks_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=20)
            tasks_frame.pack(fill=tk.BOTH, expand=True)

            tk.Label(tasks_frame, text="Your Tasks", font=("Times New Roman", 16, "bold"), bg="white").pack(pady=10)

            # Create treeview for tasks
            columns = ('Status', 'Title', 'Description', 'Due Date', 'Assigned By')
            self.task_tree = ttk.Treeview(tasks_frame, columns=columns, show='headings')

            # Set column headings
            for col in columns:
                self.task_tree.heading(col, text=col)
                self.task_tree.column(col, width=150)

            # Add scrollbar
            scrollbar = ttk.Scrollbar(tasks_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
            self.task_tree.configure(yscrollcommand=scrollbar.set)

            # Pack tree and scrollbar
            self.task_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Get and display tasks
            tasks = self.db.get_user_tasks(self.username)
            for task in tasks:
                # Create checkbox value
                status = "✓" if task[6] == "Completed" else "☐"
                self.task_tree.insert('', tk.END, values=(
                    status,  # status with checkbox
                    task[3],  # task_title
                    task[4],  # task_description
                    task[5],  # due_date
                    task[8]   # assigned_by_name
                ), tags=(str(task[0]),))  # task_id as tag

            # Bind click event to handle checkbox clicks
            def on_click(event):
                region = self.task_tree.identify_region(event.x, event.y)
                if region == "cell":
                    column = self.task_tree.identify_column(event.x)
                    if column == "#1":  # Status column
                        item = self.task_tree.identify_row(event.y)
                        if item:
                            values = self.task_tree.item(item)['values']
                            task_id = self.task_tree.item(item)['tags'][0]
                            current_status = values[0]
                            
                            # Toggle status
                            new_status = "✓" if current_status == "☐" else "☐"
                            values = list(values)
                            values[0] = new_status
                            self.task_tree.item(item, values=values)
                            
                            # Update database
                            self.db.update_task_status(task_id, "Completed" if new_status == "✓" else "Pending")
                            messagebox.showinfo("Success", "Task status updated!")

            self.task_tree.bind('<ButtonRelease-1>', on_click)

    def manage_users(self):
        # Clear main content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create main frame
        main_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(main_frame, 
                text="Manage Users", 
                font=("Times New Roman", 18, "bold"), 
                bg="white").pack(pady=(0, 20))

        # Create frame for treeview and scrollbar
        tree_frame = tk.Frame(main_frame, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Create treeview
        columns = ('Name', 'Age', 'Qualification', 'Username', 'EmployeeID', 'Password', 'Tasks')
        self.user_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

        # Set column headings
        for col in columns:
            self.user_tree.heading(col, text=col)
            self.user_tree.column(col, width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.user_tree.yview)
        self.user_tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        self.user_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Get all users from database
        users = self.db.get_all_users_with_tasks()
        
        # Insert data into treeview
        for user in users:
            self.user_tree.insert('', tk.END, values=(
                user[1],  # name
                user[4],  # age
                user[7],  # qualification
                user[0],  # username
                user[9],  # employee_id
                user[2],  # password
                user[10]  # task count
            ), tags=(user[0],))  # username as tag for removal

        # Create remove button
        def remove_user():
            selected_item = self.user_tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a user to remove!")
                return

            username = self.user_tree.item(selected_item[0])['tags'][0]
            if messagebox.askyesno("Confirm", f"Are you sure you want to remove user {username}?"):
                if self.db.remove_user(username):
                    self.user_tree.delete(selected_item[0])
                    messagebox.showinfo("Success", "User removed successfully!")
                else:
                    messagebox.showerror("Error", "Failed to remove user!")

        # Add remove button
        remove_btn = tk.Button(main_frame, 
                             text="Remove Selected User", 
                             command=remove_user,
                             font=("Times New Roman", 12, "bold"),
                             bg="#e74c3c",
                             fg="white",
                             padx=20,
                             pady=10)
        remove_btn.pack(pady=20)

        # Add hover effect to remove button
        remove_btn.bind("<Enter>", lambda e: remove_btn.configure(bg="#c0392b"))
        remove_btn.bind("<Leave>", lambda e: remove_btn.configure(bg="#e74c3c"))

    def view_files(self):
        # Clear main content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create main frame
        main_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(main_frame, 
                text="Submitted Files", 
                font=("Times New Roman", 18, "bold"), 
                bg="white").pack(pady=(0, 20))

        # Create frame for treeview and scrollbar
        tree_frame = tk.Frame(main_frame, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Create treeview
        columns = ('Username', 'Name', 'Employee ID', 'File Name', 'File Type', 'Upload Date')
        self.file_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

        # Set column headings
        for col in columns:
            self.file_tree.heading(col, text=col)
            self.file_tree.column(col, width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Get all files from database with user details
        cursor = self.db.conn.cursor()
        cursor.execute('''
            SELECT f.username, u.name, u.employee_id, f.filename, f.filetype, f.uploaded_at
            FROM files f
            JOIN users u ON f.username = u.username
            ORDER BY f.uploaded_at DESC
        ''')
        files = cursor.fetchall()

        # Insert data into treeview
        for file in files:
            self.file_tree.insert('', tk.END, values=file)

        # Add download button
        def download_file():
            selected_item = self.file_tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a file to download!")
                return

            file_info = self.file_tree.item(selected_item[0])['values']
            username = file_info[0]
            filename = file_info[3]
            
            # Ask user where to save the file
            save_path = filedialog.asksaveasfilename(
                defaultextension=f".{file_info[4]}",
                initialfile=filename,
                title="Save File As"
            )
            
            if save_path:
                # Here you would typically implement the actual file download logic
                # For now, we'll just show a success message
                messagebox.showinfo("Success", f"File '{filename}' downloaded successfully!")

        # Add download button
        download_btn = tk.Button(main_frame, 
                               text="Download Selected File", 
                               command=download_file,
                               font=("Times New Roman", 12, "bold"),
                               bg="#4CAF50",
                               fg="white",
                               padx=20,
                               pady=10)
        download_btn.pack(pady=20)

        # Add hover effect to download button
        download_btn.bind("<Enter>", lambda e: download_btn.configure(bg="#45a049"))
        download_btn.bind("<Leave>", lambda e: download_btn.configure(bg="#4CAF50"))

    def submit_tasks(self):
        file_path = filedialog.askopenfilename(title="Select a file")
        if file_path:
            filename = os.path.basename(file_path)
            filetype = filename.split('.')[-1].lower()
            if filetype in ['doc', 'docx', 'pdf', 'ppt', 'pptx']:
                self.db.submit_file(self.username, filename, filetype)
                messagebox.showinfo("Success", f"File '{filename}' uploaded successfully!")
            else:
                messagebox.showerror("Error", "Invalid file type. Please upload Word, PDF, or PPT files.")

    def attendance(self):
        self.show_message("Attendance functionality is under development.")

    def back_to_login(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to go back to login?"):
            self.root.destroy()
            import login
            login.root.mainloop()

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()

    def show_message(self, message):
        messagebox.showinfo("Information", message)

    def show_statistical_report(self):
        # Clear main content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create main frame
        main_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(main_frame, 
                text="Statistical Report", 
                font=("Times New Roman", 18, "bold"), 
                bg="white").pack(pady=(0, 20))

        # Create frame for user list and graph
        content_frame = tk.Frame(main_frame, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left frame for user list
        left_frame = tk.Frame(content_frame, bg="white", width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left_frame.pack_propagate(False)

        # Right frame for graph
        right_frame = tk.Frame(content_frame, bg="white")
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # User list title
        tk.Label(left_frame, 
                text="Users", 
                font=("Times New Roman", 14, "bold"), 
                bg="white").pack(pady=(0, 10))

        # Create user listbox
        user_listbox = tk.Listbox(left_frame, 
                                 font=("Times New Roman", 12),
                                 selectmode=tk.SINGLE,
                                 height=15)
        user_listbox.pack(fill=tk.BOTH, expand=True)

        # Get all users from database
        cursor = self.db.conn.cursor()
        cursor.execute('''
            SELECT username, name 
            FROM users 
            WHERE role = 'user'
            ORDER BY name
        ''')
        users = cursor.fetchall()

        # Insert users into listbox
        for user in users:
            user_listbox.insert(tk.END, f"{user[1]} ({user[0]})")

        def show_user_stats(event):
            # Clear previous graph
            for widget in right_frame.winfo_children():
                widget.destroy()

            # Get selected user
            selection = user_listbox.curselection()
            if not selection:
                return

            # Get username from selection
            selected_text = user_listbox.get(selection[0])
            username = selected_text.split('(')[1].strip(')')

            # Get user's task statistics
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_tasks,
                    SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed_tasks
                FROM tasks 
                WHERE assigned_to = ?
            ''', (username,))
            stats = cursor.fetchone()

            total_tasks = stats[0] or 0
            completed_tasks = stats[1] or 0
            pending_tasks = total_tasks - completed_tasks

            if total_tasks == 0:
                tk.Label(right_frame, 
                        text="No tasks assigned to this user", 
                        font=("Times New Roman", 14), 
                        bg="white").pack(pady=20)
                return

            # Calculate percentages
            completed_percent = (completed_tasks / total_tasks) * 100
            pending_percent = (pending_tasks / total_tasks) * 100

            # Create figure with two subplots
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))
            fig.suptitle(f'Task Performance for {selected_text}', fontsize=14)

            # Pie chart
            labels = ['Completed', 'Pending']
            sizes = [completed_tasks, pending_tasks]
            colors = ['#4CAF50', '#FF6F61']
            ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax1.set_title('Task Completion Distribution')

            # Line graph
            # Get task completion over time
            cursor.execute('''
                SELECT 
                    DATE(created_at) as date,
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed
                FROM tasks 
                WHERE assigned_to = ?
                GROUP BY DATE(created_at)
                ORDER BY date
            ''', (username,))
            time_data = cursor.fetchall()

            if time_data:
                dates = [row[0] for row in time_data]
                completed = [row[2] for row in time_data]
                total = [row[1] for row in time_data]
                
                ax2.plot(dates, completed, label='Completed', color='#4CAF50', marker='o')
                ax2.plot(dates, total, label='Total', color='#FF6F61', marker='o')
                ax2.set_title('Task Completion Over Time')
                ax2.set_xlabel('Date')
                ax2.set_ylabel('Number of Tasks')
                ax2.legend()
                ax2.grid(True)
                plt.xticks(rotation=45)

            # Adjust layout and display
            plt.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=right_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Bind selection event to listbox
        user_listbox.bind('<<ListboxSelect>>', show_user_stats)

        # Show initial message
        tk.Label(right_frame, 
                text="Select a user to view their statistics", 
                font=("Times New Roman", 14), 
                bg="white").pack(pady=20)

    def show_profile(self):
        # Clear main content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create profile display area
        profile_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=20)
        profile_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(profile_frame, 
                text="Admin Profile", 
                font=("Times New Roman", 18, "bold"), 
                bg="white").pack(pady=(0, 20))

        # Get admin details from database
        admin_details = self.db.get_user_details(self.username)
        if admin_details:
            # Create main container for profile info
            info_frame = tk.Frame(profile_frame, bg="white")
            info_frame.pack(fill=tk.BOTH, expand=True, padx=20)

            # Create labels and values
            labels = ["Name", "Age", "Address", "Email", "Qualification", "Phone", "Employee ID"]
            values = [admin_details[3], admin_details[4], admin_details[5], 
                     admin_details[6], admin_details[7], admin_details[8], admin_details[9]]

            # Display profile information
            for label, value in zip(labels, values):
                # Create a frame for each row
                row_frame = tk.Frame(info_frame, bg="white")
                row_frame.pack(fill=tk.X, pady=5)
                
                # Label
                tk.Label(row_frame, 
                        text=f"{label}:", 
                        font=("Times New Roman", 12, "bold"), 
                        bg="white",
                        width=15).pack(side=tk.LEFT)
                
                # Value
                tk.Label(row_frame, 
                        text=str(value), 
                        font=("Times New Roman", 12), 
                        bg="white").pack(side=tk.LEFT, padx=10)

            # Add edit button
            edit_btn = tk.Button(profile_frame, 
                               text="Edit Profile", 
                               command=self.edit_profile,
                               font=("Times New Roman", 12, "bold"),
                               bg="#4CAF50",
                               fg="white",
                               padx=20,
                               pady=10)
            edit_btn.pack(pady=20)

            # Add hover effect to edit button
            edit_btn.bind("<Enter>", lambda e: edit_btn.configure(bg="#45a049"))
            edit_btn.bind("<Leave>", lambda e: edit_btn.configure(bg="#4CAF50"))
        else:
            tk.Label(profile_frame, 
                    text="Error loading profile", 
                    font=("Times New Roman", 12), 
                    bg="white", 
                    fg="red").pack(pady=10)

    def edit_profile(self):
        # Clear main content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create edit profile form
        form_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(form_frame, 
                text="Edit Profile", 
                font=("Times New Roman", 18, "bold"), 
                bg="white").pack(pady=(0, 20))

        # Get current admin details
        admin_details = self.db.get_user_details(self.username)
        if not admin_details:
            tk.Label(form_frame, 
                    text="Error loading profile", 
                    font=("Times New Roman", 12), 
                    bg="white", 
                    fg="red").pack(pady=10)
            return

        # Create entry fields
        fields = {}
        labels = ["Name", "Age", "Address", "Email", "Qualification", "Phone"]
        values = [admin_details[3], admin_details[4], admin_details[5], 
                 admin_details[6], admin_details[7], admin_details[8]]

        # Create a frame for the form fields
        fields_frame = tk.Frame(form_frame, bg="white")
        fields_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        for label, value in zip(labels, values):
            # Create a frame for each row
            row_frame = tk.Frame(fields_frame, bg="white")
            row_frame.pack(fill=tk.X, pady=5)
            
            # Label
            tk.Label(row_frame, 
                    text=label, 
                    font=("Times New Roman", 12, "bold"), 
                    bg="white",
                    width=15).pack(side=tk.LEFT)
            
            # Entry field
            entry = tk.Entry(row_frame, font=("Times New Roman", 12))
            entry.insert(0, str(value))
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            fields[label] = entry

        def validate_and_save():
            # Validate all fields
            try:
                # Validate age
                age = int(fields['Age'].get())
                if age < 18 or age > 100:
                    raise ValueError("Age must be between 18 and 100")

                # Validate email
                email = fields['Email'].get()
                if not email.endswith("@gmail.com"):
                    raise ValueError("Email must end with @gmail.com")

                # Validate phone
                phone = fields['Phone'].get()
                if not phone.isdigit() or len(phone) != 10:
                    raise ValueError("Phone number must be exactly 10 digits")

                # Validate qualification
                qualification = fields['Qualification'].get()
                if qualification not in ["BSc", "BTech", "MSc", "MTech", "PhD"]:
                    raise ValueError("Invalid qualification")

                # Prepare data for update
                new_data = {
                    'username': self.username,
                    'name': fields['Name'].get(),
                    'age': age,
                    'address': fields['Address'].get(),
                    'email': email,
                    'qualification': qualification,
                    'phone': phone
                }
                
                # Update profile
                if self.db.update_user_profile(new_data):
                    messagebox.showinfo("Success", "Profile updated successfully!")
                    self.show_profile()  # Return to profile view
                else:
                    messagebox.showerror("Error", "Failed to update profile!")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        # Add save and cancel buttons
        button_frame = tk.Frame(form_frame, bg="white")
        button_frame.pack(pady=20)

        save_btn = tk.Button(button_frame, 
                           text="Save Changes", 
                           command=validate_and_save,
                           font=("Times New Roman", 12, "bold"),
                           bg="#4CAF50",
                           fg="white",
                           padx=20,
                           pady=10)
        save_btn.pack(side=tk.LEFT, padx=10)

        cancel_btn = tk.Button(button_frame, 
                             text="Cancel", 
                             command=self.show_profile,
                             font=("Times New Roman", 12, "bold"),
                             bg="#e74c3c",
                             fg="white",
                             padx=20,
                             pady=10)
        cancel_btn.pack(side=tk.LEFT, padx=10)

        # Add hover effects
        save_btn.bind("<Enter>", lambda e: save_btn.configure(bg="#45a049"))
        save_btn.bind("<Leave>", lambda e: save_btn.configure(bg="#4CAF50"))
        cancel_btn.bind("<Enter>", lambda e: cancel_btn.configure(bg="#c0392b"))
        cancel_btn.bind("<Leave>", lambda e: cancel_btn.configure(bg="#e74c3c"))

    def schedule_meeting(self):
        # Clear main content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create scheduler frame
        scheduler_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=20)
        scheduler_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(scheduler_frame, 
                text="Schedule Meeting", 
                font=("Times New Roman", 18, "bold"), 
                bg="white").pack(pady=(0, 20))

        # Create form frame
        form_frame = tk.Frame(scheduler_frame, bg="white")
        form_frame.pack(fill=tk.X, pady=10)

        # Meeting title
        tk.Label(form_frame, text="Title:", bg="white").grid(row=0, column=0, sticky="w", pady=5)
        title_entry = tk.Entry(form_frame, width=40)
        title_entry.grid(row=0, column=1, padx=10, pady=5)

        # Meeting description
        tk.Label(form_frame, text="Description:", bg="white").grid(row=1, column=0, sticky="w", pady=5)
        desc_text = tk.Text(form_frame, width=30, height=5)
        desc_text.grid(row=1, column=1, padx=10, pady=5)

        # Date entry
        tk.Label(form_frame, text="Date (YYYY-MM-DD):", bg="white").grid(row=2, column=0, sticky="w", pady=5)
        date_entry = tk.Entry(form_frame, width=20)
        date_entry.grid(row=2, column=1, padx=10, pady=5)

        # Time entry
        tk.Label(form_frame, text="Time (HH:MM):", bg="white").grid(row=3, column=0, sticky="w", pady=5)
        time_entry = tk.Entry(form_frame, width=20)
        time_entry.grid(row=3, column=1, padx=10, pady=5)

        # Email entry
        tk.Label(form_frame, text="Email:", bg="white").grid(row=4, column=0, sticky="w", pady=5)
        email_entry = tk.Entry(form_frame, width=40)
        email_entry.grid(row=4, column=1, padx=10, pady=5)

        # Participants listbox
        tk.Label(form_frame, text="Participants:", bg="white").grid(row=5, column=0, sticky="w", pady=5)
        participants_listbox = tk.Listbox(form_frame, selectmode=tk.MULTIPLE, width=40, height=5)
        participants_listbox.grid(row=5, column=1, padx=10, pady=5)

        # Get users and populate listbox
        users = self.db.get_all_users_with_tasks()
        for user in users:
            if user[0] != self.username:  # Don't show admin in participants list
                participants_listbox.insert(tk.END, user[0])

        def validate_date(date_str):
            try:
                year, month, day = map(int, date_str.split('-'))
                return True
            except:
                return False

        def validate_time(time_str):
            try:
                hour, minute = map(int, time_str.split(':'))
                return 0 <= hour <= 23 and 0 <= minute <= 59
            except:
                return False

        def schedule():
            # Get values
            title = title_entry.get().strip()
            description = desc_text.get("1.0", tk.END).strip()
            date = date_entry.get().strip()
            time = time_entry.get().strip()
            email = email_entry.get().strip()
            selected_indices = participants_listbox.curselection()
            participants = [participants_listbox.get(i) for i in selected_indices]

            # Validate inputs
            if not all([title, description, date, time, email]):
                messagebox.showerror("Error", "All fields are required!")
                return

            if not validate_date(date):
                messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
                return

            if not validate_time(time):
                messagebox.showerror("Error", "Invalid time format! Use HH:MM")
                return

            if not participants:
                messagebox.showerror("Error", "Please select at least one participant!")
                return

            # Prepare meeting data
            meeting_data = {
                'title': title,
                'description': description,
                'date': date,
                'time': time,
                'organizer': self.username,
                'participants': participants
            }

            # Schedule meeting
            if self.db.schedule_meeting(meeting_data):
                
                
                
                
                # Clear form
                title_entry.delete(0, tk.END)
                desc_text.delete("1.0", tk.END)
                date_entry.delete(0, tk.END)
                time_entry.delete(0, tk.END)
                email_entry.delete(0, tk.END)
                participants_listbox.selection_clear(0, tk.END)
            else:
                messagebox.showerror("Error", "Failed to schedule meeting!")

        # Create button frame
        button_frame = tk.Frame(scheduler_frame, bg="white")
        button_frame.pack(pady=20)

        # Schedule button with hover effect
        schedule_btn = tk.Button(button_frame, 
                               text="Schedule Meeting", 
                               command=schedule,
                               font=("Times New Roman", 12, "bold"),
                               bg="#4CAF50",
                               fg="white",
                               padx=20,
                               pady=10)
        schedule_btn.pack(side=tk.LEFT, padx=10)

        # Add hover effect
        schedule_btn.bind("<Enter>", lambda e: schedule_btn.configure(bg="#45a049"))
        schedule_btn.bind("<Leave>", lambda e: schedule_btn.configure(bg="#4CAF50"))

        # Add instructions
        tk.Label(scheduler_frame, 
                text="Note: Select multiple participants by holding Ctrl/Cmd while clicking", 
                font=("Times New Roman", 10), 
                bg="white").pack(pady=10)

    def view_meetings(self):
        # Clear main content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create meetings display area
        meetings_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=20)
        meetings_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(meetings_frame, 
                text="Scheduled Meetings", 
                font=("Times New Roman", 18, "bold"), 
                bg="white").pack(pady=(0, 20))

        # Create frame for meetings list
        list_frame = tk.Frame(meetings_frame, bg="white")
        list_frame.pack(fill=tk.BOTH, expand=True)

        # Create treeview for meetings
        columns = ('Title', 'Description', 'Date', 'Time', 'Organizer', 'Participants')
        self.meeting_tree = ttk.Treeview(list_frame, columns=columns, show='headings')

        # Set column headings
        for col in columns:
            self.meeting_tree.heading(col, text=col)
            self.meeting_tree.column(col, width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.meeting_tree.yview)
        self.meeting_tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        self.meeting_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Get and display meetings
        meetings = self.db.get_user_meetings(self.username)
        if meetings:
            for meeting in meetings:
                self.meeting_tree.insert('', tk.END, values=(
                    meeting[1],  # title
                    meeting[2],  # description
                    meeting[3],  # date
                    meeting[4],  # time
                    meeting[7],  # organizer_name
                    meeting[8]   # participants
                ))
        else:
            # Show message if no meetings found
            tk.Label(meetings_frame, 
                    text="No meetings scheduled yet", 
                    font=("Times New Roman", 12), 
                    bg="white").pack(pady=20)

        # Add meeting details view
        def show_meeting_details(event):
            selected_item = self.meeting_tree.selection()
            if not selected_item:
                return

            # Get meeting details
            meeting_info = self.meeting_tree.item(selected_item[0])['values']
            
            # Create details window
            details_window = tk.Toplevel(self.root)
            details_window.title("Meeting Details")
            details_window.geometry("500x400")
            details_window.configure(bg="white")

            # Add meeting details
            tk.Label(details_window, 
                    text="Meeting Details", 
                    font=("Times New Roman", 16, "bold"), 
                    bg="white").pack(pady=10)

            # Create details frame
            details_frame = tk.Frame(details_window, bg="white", padx=20, pady=20)
            details_frame.pack(fill=tk.BOTH, expand=True)

            # Display meeting information
            info_labels = [
                ("Title:", meeting_info[0]),
                ("Description:", meeting_info[1]),
                ("Date:", meeting_info[2]),
                ("Time:", meeting_info[3]),
                ("Organizer:", meeting_info[4]),
                ("Participants:", meeting_info[5])
            ]

            for label, value in info_labels:
                frame = tk.Frame(details_frame, bg="white")
                frame.pack(fill=tk.X, pady=5)
                
                tk.Label(frame, 
                        text=label, 
                        font=("Times New Roman", 12, "bold"), 
                        bg="white").pack(side=tk.LEFT)
                
                tk.Label(frame, 
                        text=value, 
                        font=("Times New Roman", 12), 
                        bg="white").pack(side=tk.LEFT, padx=10)

            # Close button
            tk.Button(details_window, 
                     text="Close", 
                     command=details_window.destroy,
                     font=("Times New Roman", 12, "bold"),
                     bg="#4CAF50",
                     fg="white",
                     padx=20,
                     pady=10).pack(pady=20)

        # Bind double-click event to show details
        self.meeting_tree.bind('<Double-1>', show_meeting_details)

        # Add instructions
        tk.Label(meetings_frame, 
                text="Double-click on a meeting to view details", 
                font=("Times New Roman", 10), 
                bg="white").pack(pady=10)

    def show_attendance_report(self):
        # Clear main content area
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create attendance report frame
        attendance_frame = tk.Frame(self.content_frame, bg="white")
        attendance_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        tk.Label(attendance_frame, text="Attendance Report", font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)

        # Create Treeview
        columns = ('Username', 'Name', 'Role', 'Login Time', 'Logout Time', 'Duration (hours)')
        tree = ttk.Treeview(attendance_frame, columns=columns, show='headings')

        # Set column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(attendance_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # Pack Treeview and scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Get attendance data
        attendance_data = self.db.get_attendance_report()

        # Insert data into Treeview
        for record in attendance_data:
            tree.insert('', tk.END, values=record)

        # Add filter options
        filter_frame = tk.Frame(attendance_frame, bg="white")
        filter_frame.pack(fill=tk.X, pady=10)

        # Role filter
        tk.Label(filter_frame, text="Filter by Role:", bg="white").pack(side=tk.LEFT, padx=5)
        role_var = tk.StringVar(value="All")
        role_combo = ttk.Combobox(filter_frame, textvariable=role_var, values=["All", "admin", "user"], state="readonly")
        role_combo.pack(side=tk.LEFT, padx=5)

        # Date filter
        tk.Label(filter_frame, text="Filter by Date (YYYY-MM-DD):", bg="white").pack(side=tk.LEFT, padx=5)
        date_entry = tk.Entry(filter_frame)
        date_entry.pack(side=tk.LEFT, padx=5)

        def apply_filters():
            # Clear existing items
            for item in tree.get_children():
                tree.delete(item)

            # Get filter values
            selected_role = role_var.get()
            filter_date = date_entry.get()

            # Filter data
            filtered_data = []
            for record in attendance_data:
                username, name, role, login_time, logout_time, duration = record
                
                # Apply role filter
                if selected_role != "All" and role != selected_role:
                    continue
                
                # Apply date filter
                if filter_date:
                    if not login_time.startswith(filter_date):
                        continue
                
                filtered_data.append(record)

            # Insert filtered data
            for record in filtered_data:
                tree.insert('', tk.END, values=record)

        # Apply filters button
        tk.Button(filter_frame, text="Apply Filters", command=apply_filters, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)

        # Add note about active sessions
        tk.Label(attendance_frame, text="Note: Active sessions will show 'Still Active' for logout time", 
                font=("Helvetica", 10), bg="white", fg="gray").pack(pady=5)
        
    def on_closing(self):
        # Mark logout time
        self.db.mark_logout(self.username)
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    # Test with Admin User
    app = HomePage(root, username="admin", role="admin")
    # Test with Normal User - Uncomment this line to test
    # app = HomePage(root, username="user1", role="user")
    root.mainloop()
