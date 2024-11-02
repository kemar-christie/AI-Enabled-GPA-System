# admin_navbar.py

import tkinter as tk
import admin_add_student as adminAddStd


def show_add_student(frame, root):
    # Destroy the current frame (navbar) before loading the new one
    frame.destroy()
    
    # Call the addAdminInterface function from admin_add_student.py
    adminAddStd.addAdminInterface(root)
    

def admin_navbar(root):
    # Create a frame for the admin navbar
    frame = tk.Frame(root, bg="white", bd=2, relief="solid", padx=20, pady=20)
    frame.pack(expand=True, pady=(20,20))  # keeps the content in the center of the window

    # Heading label
    label = tk.Label(frame, text="Admin Nav bar", font=('default', 20), bg="white")
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

    viewStudentProgress = tk.Button(frame, text="Academic Progress", font=("Arial", 12), padx=20, bg="#007bff", fg="white", width=12)
    viewStudentProgress.grid(row=1, column=2, sticky="e")

    return frame
