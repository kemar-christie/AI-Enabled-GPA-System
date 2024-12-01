import tkinter as tk
from tkinter import ttk



def backToMenu(frame,root):
    frame.destroy()
    
    import admin_navbar as adminNav
    adminNav.admin_navbar(root)

def clear_fields(student_id_entry,academic_year_dropdown,semester_dropdown):
    """Clear the input fields."""
    student_id_entry.delete(0, tk.END)
    academic_year_dropdown.set('')
    semester_dropdown.set('')


def submit_info(student_id_entry,academic_year_dropdown,semester_dropdown,root,frame):
    """Submit the entered information (placeholder functionality)."""
    student_id = student_id_entry.get().strip()
    academic_year = academic_year_dropdown.get().strip()
    semester = semester_dropdown.get().strip()

    from tkinter import messagebox

    # Validation for empty fields
    if not student_id or not academic_year or not semester:
        messagebox.showwarning("Input Error","All fields are required!")
    else:
        from Database.admin_Actions import get_student_grades_for_semester
        grades=get_student_grades_for_semester(student_id,academic_year,semester)

        if grades!= None:
            root.stdID = student_id
            root.semester =semester
            root.year = academic_year
            
            frame.destroy()
            from admin_add_student_grade import std_grade_info
            std_grade_info(root,grades)



def std_info(root):
    # Create a frame for the admin navbar
    frame = tk.Frame(root, bg="white", bd=2, relief="solid", padx=20, pady=20)
    frame.pack(expand=True, pady=20)  # Keeps the content centered in the window

    # Heading label
    label = tk.Label(frame, text="Enter Student Info", font=('default', 20), bg="white")
    label.pack(pady=(0, 20))

    # Academic year options
    academicYear = [
        '2015/2016', '2016/2017', '2017/2018', '2018/2019', '2019/2020',
        '2020/2021', '2021/2022', '2022/2023', '2023/2024', '2024/2025'
    ]
    
    # Semester options
    semesters = ['1', '2', '3']

    # Labels and input fields
    student_id_label = tk.Label(frame, text="Student ID:", font=('Arial', 12), bg="white")
    student_id_label.pack(anchor="w", pady=5)
    student_id_entry = tk.Entry(frame, font=('Arial', 12), width=30)
    student_id_entry.pack(pady=5)

    academic_year_label = tk.Label(frame, text="Academic Year:", font=('Arial', 12), bg="white")
    academic_year_label.pack(anchor="w", pady=5)
    academic_year_dropdown = ttk.Combobox(frame, values=academicYear, font=('Arial', 12), state="readonly", width=28)
    academic_year_dropdown.pack(pady=5)

    semester_label = tk.Label(frame, text="Semester:", font=('Arial', 12), bg="white")
    semester_label.pack(anchor="w", pady=5)
    semester_dropdown = ttk.Combobox(frame, values=semesters, font=('Arial', 12), state="readonly", width=28)
    semester_dropdown.pack(pady=5)

    # Clear and Submit Buttons
    button_frame = tk.Frame(frame, bg="white")
    button_frame.pack(pady=(20, 0))

    clear_button = tk.Button(button_frame, text="Clear", font=("Arial", 12), bg="#007bff", fg="white", width=12, command= lambda: clear_fields(student_id_entry,academic_year_dropdown,semester_dropdown))
    clear_button.pack(side=tk.LEFT, padx=10)

    submit_button = tk.Button(button_frame, text="Submit", font=("Arial", 12), bg="#007bff", fg="white", width=12, command= lambda: submit_info(student_id_entry,academic_year_dropdown,semester_dropdown,root,frame))
    submit_button.pack(side=tk.LEFT, padx=10)

    backtoStdMenu = tk.Button(frame, text="Back to Menu", font=("Arial", 12), padx=20, bg="#007bff", fg="white", width=23,command= lambda: backToMenu(frame,root))
    backtoStdMenu.pack(pady=(10,0) )
        





if __name__ == "__main__":

    root = tk.Tk()
    root.geometry("600x600")
    root.title("Academic Probation")

    # Set the background color of the root window to white
    root.configure(bg="white")
    root.adminID = 'adm1'
    std_info(root)

    root.mainloop()  # Start the Tkinter main loop
