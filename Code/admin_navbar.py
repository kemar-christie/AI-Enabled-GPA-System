# admin_navbar.py

import tkinter as tk

def show_add_student(frame, root):
    # Destroy the current frame (navbar) before loading the new one
    frame.destroy()
    
    # Call the addAdminInterface function from admin_add_student.py
    import admin_add_student as adminAddStd
    adminAddStd.addAdminInterface(root)
    
def backToLogin(frame,root):
    frame.destroy()#remove current interface

    import Login_Interface as lgInterface
    lgInterface.login_interface(root)#display the login screen


def admin_navbar(root):
    # Create a frame for the admin navbar
    frame = tk.Frame(root, bg="white", bd=2, relief="solid", padx=20, pady=20)
    frame.pack(expand=True, pady=(20,20))  # keeps the content in the center of the window

    # Heading label
    label = tk.Label(frame, text="Admin Menu", font=('default', 20), bg="white")
    label.grid(row=0, column=0, pady=(0, 30), columnspan=3)

    # Buttons
    addStudentBtn = tk.Button(
        frame, text="Add a Student", font=("Arial", 12), padx=20, bg="#007bff",
        fg="white", width=12,
        command=lambda: show_add_student(frame, root)  # Replace frame on click
    )
    addStudentBtn.grid(row=1, column=0, sticky="e", padx=(0,10))

    addStudentGradesBtn = tk.Button(frame, text="Student Grades", font=("Arial", 12), padx=20, bg="#007bff", fg="white", width=12)
    addStudentGradesBtn.grid(row=1, column=1, sticky="e", padx=(0,10))

    viewStudentProgressBtn = tk.Button(frame, text="Academic Progress", font=("Arial", 12), padx=20, bg="#007bff", fg="white", width=12)
    viewStudentProgressBtn.grid(row=1, column=2, sticky="e")

    exitButton = tk.Button(frame, text="Logout", font=("Arial", 12), padx=20, bg="#007bff", fg="white", width=12, command= lambda: backToLogin(frame,root))
    exitButton.grid(row=2, column=0, sticky="w",pady=(10,0))
