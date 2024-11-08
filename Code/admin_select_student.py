# admin_select_student.py

import tkinter as tk

def admin_select_student(root):
    # Create main frame
    frame = tk.Frame(root, bg="white", bd=2, relief="solid", padx=20, pady=20)
    frame.pack(expand=True, pady=(20, 20))

    # Title
    title = tk.Label(frame, text="Admin Select Student", font=('Arial', 16), bg="white")
    title.pack(pady=(0, 30))

    # Student ID Entry label
    id_label = tk.Label(frame, text="Enter Student ID", font=('Arial', 12), bg="white")
    id_label.pack(pady=(0, 10))

    # Student ID Entry field
    id_entry = tk.Entry(frame, font=('Arial', 12), width=30)
    id_entry.pack(pady=(0, 20))

    # Button frame for layout
    button_frame = tk.Frame(frame, bg="white")
    button_frame.pack(fill="x", pady=(10, 0))

    # Back button
    back_btn = tk.Button(
        button_frame,
        text="Back",
        font=("Arial", 12),
        width=10,
        bg="#007bff",
        fg="white",
        command=lambda: back_to_admin(frame, root)
    )
    back_btn.pack(side="left", padx=10)

    # Next button
    next_btn = tk.Button(
        button_frame,
        text="Next",
        font=("Arial", 12),
        width=10,
        bg="#007bff",
        fg="white",
        command=lambda: validate_and_proceed(id_entry.get(), frame, root)
    )
    next_btn.pack(side="right", padx=10)

def back_to_admin(frame, root):
    frame.destroy()
    import admin_navbar as nav
    nav.admin_navbar(root)

def validate_and_proceed(student_id, frame, root):
    # Check if the field is empty
    if student_id.strip() == "":
        messagebox.showerror("Error", "Please enter a student ID")
        return
    
    # Check if the input contains only numbers
    if not student_id.isdigit():
        messagebox.showerror("Error", "Student ID must contain only numbers")
        return
    
    # If we get here, the input is valid (contains only numbers)
    print(f"Proceeding with student ID: {student_id}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")
    root.title("Admin Select Student")
    root.configure(bg="white")
    
    admin_select_student(root)
    root.mainloop()