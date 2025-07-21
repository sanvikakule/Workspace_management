import tkinter as tk
from tkinter import Label, messagebox, ttk
from PIL import Image, ImageTk
import os
from database import Database
from adminhomepage import HomePage

db = Database()

def set_background():
    root.update_idletasks()  # Ensure root window is fully initialized
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    bg_image = Image.open("bg1.png")
    bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

def role_selection():
    for widget in root.winfo_children():
        widget.destroy()
    set_background()

    # Custom Title Label
    title_label = tk.Label(root, text="Workspace!", font=("Times New Roman", 28, "bold"), bg="#d3d3d3", fg="#0D1A42")
    title_label.pack(pady=20)

    box_frame = tk.Frame(root, bg="#d3d3d3", padx=60, pady=40)
    box_frame.place(relx=0.3, rely=0.55, anchor="center")

    tk.Label(box_frame, text="Select Role !", font=("Times New Roman", 20, "bold"), bg="#d3d3d3").pack(pady=70)
    
    tk.Button(box_frame, text="Admin", font=("Times New Roman", 14), bg="#333333", fg="#d3d3d3",
          relief="groove", bd=2, width=20, command=lambda: login_page("admin")).pack(pady=(0,20))

    tk.Button(box_frame, text="User", font=("Times New Roman", 14), bg="#333333", fg="#d3d3d3",
          relief="groove", bd=2, width=20, command=lambda: login_page("user")).pack(pady=(0,25))

def login_page(role):
    for widget in root.winfo_children():
        widget.destroy()
    set_background()

    # Custom Title Label
    title_label = tk.Label(root, text="Workspace!", font=("Times New Roman", 28, "bold"), bg="#d3d3d3", fg="#0D1A42")
    title_label.pack(pady=20)

    # Updated frame to match previous size and position
    frame = tk.Frame(root, bg="#d3d3d3", padx=60, pady=40)
    frame.place(relx=0.3, rely=0.55, anchor="center")  # Adjust position as per your previous frame

    # Add the title for the login page, adjusted for your custom frame size
    tk.Label(frame, text=f"{role.capitalize()} Login...", font=("Times New Roman", 20, "bold"), bg="#d3d3d3").grid(row=0, column=0, columnspan=2, pady=40)
    
    # Username label and entry field
    
    tk.Label(frame, text="Username", bg="#d3d3d3", font=("Times New Roman", 14)).grid(row=1, column=0, sticky="w",pady=(0, 5))
    username_entry = tk.Entry(frame, font=("Times New Roman", 14), width=25)
    username_entry.grid(row=1, column=1, pady=(0, 10), padx=(10, 0))

    # Password label and entry field
    tk.Label(frame, text="Password", bg="#d3d3d3", font=("Times New Roman", 14)).grid(row=2, column=0, sticky="w",pady=(0, 5))
    password_entry = tk.Entry(frame,  show="*", font=("Times New Roman", 14), width=25)
    password_entry.grid(row=2, column=1, pady=(0, 10), padx=(10, 0))

    def login():
        username = username_entry.get()
        password = password_entry.get()

        if db.verify_login(username, password, role):
            if db.mark_attendance(username):
                messagebox.showinfo("Success", f"Welcome {role.capitalize()} {username}!")
                root.destroy()
                new_root = tk.Tk()
                app = HomePage(new_root, username, role)
                new_root.mainloop()
            else:
                messagebox.showwarning("Warning", "Welcome, but attendance marking failed!")
                root.destroy()
                new_root = tk.Tk()
                app = HomePage(new_root, username, role)
                new_root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid credentials!")
    
    tk.Button(frame, text="Login", command=login, width=20, font=("Times New Roman", 14), bg="green", fg="#d3d3d3", relief="groove", bd=2).grid(row=3, column=1, pady=20, sticky="w")


    tk.Button(frame, text="Register Now", command=lambda: register_page(role), width=15, bg="#333333", fg="#d3d3d3").grid(row=4, column=1, padx=20, pady=10, sticky="e", columnspan=2)

    tk.Button(frame, text="Back", command=role_selection, fg="#d3d3d3", bg="red", width=15).grid(row=4, column=0, padx=20, pady=10, sticky="e")
    


def register_page(role):
    for widget in root.winfo_children():
        widget.destroy()
    set_background()

    title_label = tk.Label(root, text="Workspace!", font=("Times New Roman", 28, "bold"), bg="#d3d3d3", fg="#0D1A42")
    title_label.pack(pady=20)

    frame = tk.Frame(root, bg="#d3d3d3", padx=20, pady=20)
    frame.place(relx=0.1, rely=0.2, anchor="nw")

    tk.Label(frame, text=f"{role.capitalize()} Registration..", font=("Times New Roman", 20, "bold"), bg="#d3d3d3").grid(row=0, column=0, columnspan=2, pady=40)

    def validate_email(email):
        return email.endswith("@gmail.com")

    def validate_phone(phone):
        return phone.isdigit() and len(phone) == 10

    def validate_age(age):
        return age.isdigit()

    def register():
        name = name_entry.get()
        age = age_entry.get()
        address = address_entry.get()
        email = email_entry.get()
        qualification = qualification_var.get()
        phone = phone_entry.get()
        emp_id = emp_id_entry.get()
        username = username_entry.get()
        password = password_entry.get()

        invalid_messages = []

        if not all([name, age, address, email, qualification, phone, emp_id, username, password]):
            invalid_messages.append("All fields are required!")

        if not validate_age(age):
            invalid_messages.append("Invalid Age: Age should be a valid number.")

        if not validate_phone(phone):
            invalid_messages.append("Invalid Phone: Phone number must be exactly 10 digits.")

        if not validate_email(email):
            invalid_messages.append("Invalid Email: Email must end with '@gmail.com'.")

        if qualification == "Select":
            invalid_messages.append("Invalid Qualification: Please select a valid qualification.")

        if invalid_messages:
            error_window = tk.Toplevel(root)
            error_window.title("Invalid Details")
            error_window.geometry("500x400")
            tk.Label(error_window, text="Please correct the following errors:", font=("Arial", 14, "bold"), fg="red").pack(pady=10)

            for msg in invalid_messages:
                tk.Label(error_window, text=msg, font=("Arial", 12), fg="red", wraplength=380).pack(anchor="w", padx=10)

            tk.Button(error_window, text="OK", command=error_window.destroy, bg="red", fg="#d3d3d3", width=10).pack(pady=10)
            return

        user_data = {
            'username': username,
            'password': password,
            'role': role,
            'name': name,
            'age': int(age),
            'address': address,
            'email': email,
            'qualification': qualification,
            'phone': phone,
            'employee_id': emp_id
        }

        if db.register_user(user_data):
            messagebox.showinfo("Success", "Registration successful!")
            login_page(role)
        else:
            messagebox.showerror("Error", "Username or Employee ID already exists!")

    tk.Label(frame, text="Full Name", bg="#d3d3d3", font=("Times New Roman", 14)).grid(row=1, column=0, sticky="w", pady=(0, 5))
    name_entry = tk.Entry(frame, font=("Times New Roman", 14), width=25)
    name_entry.grid(row=1, column=1, pady=(0, 10), padx=(10, 0))

    tk.Label(frame, text="Age", bg="#d3d3d3", font=("Times New Roman", 14)).grid(row=2, column=0, sticky="w", pady=(0, 5))
    age_entry = tk.Entry(frame, font=("Times New Roman", 14), width=25)
    age_entry.grid(row=2, column=1, pady=(0, 10), padx=(10, 0))

    tk.Label(frame, text="Address", bg="#d3d3d3", font=("Times New Roman", 14)).grid(row=3, column=0, sticky="w", pady=(0, 5))
    address_entry = tk.Entry(frame, font=("Times New Roman", 14), width=25)
    address_entry.grid(row=3, column=1, pady=(0, 10), padx=(10, 0))

    tk.Label(frame, text="Email", bg="#d3d3d3", font=("Times New Roman", 14)).grid(row=4, column=0, sticky="w", pady=(0, 5))
    email_entry = tk.Entry(frame, font=("Times New Roman", 14), width=25)
    email_entry.grid(row=4, column=1, pady=(0, 10), padx=(10, 0))

    tk.Label(frame, text="Qualification", bg="#d3d3d3", font=("Times New Roman", 14)).grid(row=5, column=0, sticky="w", pady=(0, 5))
    qualification_var = tk.StringVar()
    qualification_dropdown = ttk.Combobox(frame, textvariable=qualification_var, values=["BSc", "BTech", "MSc", "MTech", "PhD"], state="readonly", font=("Times New Roman", 14))
    qualification_dropdown.grid(row=5, column=1, pady=(0, 10), padx=(10, 0))
    qualification_dropdown.set("Select")

    tk.Label(frame, text="Phone Number", bg="#d3d3d3", font=("Times New Roman", 14)).grid(row=6, column=0, sticky="w", pady=(0, 5))
    phone_entry = tk.Entry(frame, font=("Times New Roman", 14), width=25)
    phone_entry.grid(row=6, column=1, pady=(0, 10), padx=(10, 0))

    tk.Label(frame, text="Employee ID", bg="#d3d3d3", font=("Times New Roman", 14)).grid(row=7, column=0, sticky="w", pady=(0, 5))
    emp_id_entry = tk.Entry(frame, font=("Times New Roman", 14), width=25)
    emp_id_entry.grid(row=7, column=1, pady=(0, 10), padx=(10, 0))

    tk.Label(frame, text="Username", bg="#d3d3d3", font=("Times New Roman", 14)).grid(row=8, column=0, sticky="w", pady=(0, 5))
    username_entry = tk.Entry(frame, font=("Times New Roman", 14), width=25)
    username_entry.grid(row=8, column=1, pady=(0, 10), padx=(10, 0))

    tk.Label(frame, text="Password", bg="#d3d3d3", font=("Times New Roman", 14)).grid(row=9, column=0, sticky="w", pady=(0, 5))
    password_entry = tk.Entry(frame, font=("Times New Roman", 14), show="*", width=25)
    password_entry.grid(row=9, column=1, pady=(0, 10), padx=(10, 0))

    tk.Button(frame, text="Register", command=register, bg="green", fg="#d3d3d3", font=("Times New Roman", 14), width=15).grid(row=10, column=2, pady=20, padx=(5, 10), sticky="e")

    tk.Button(frame, text="Back", command=lambda: login_page(role), fg="#d3d3d3", bg="red", font=("Times New Roman", 14), width=15).grid(row=10, column=0, pady=20, padx=(10, 5), sticky="w")
    
    


root = tk.Tk()
root.title("Workspace!")
root.state("zoomed")  # Maximized window with window controls

role_selection()
root.mainloop()
