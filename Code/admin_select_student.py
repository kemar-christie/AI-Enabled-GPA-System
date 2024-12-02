# admin_select_student.py

import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox

def backToMenu(frame,root):
    frame.destroy()
    
    import admin_navbar as adminNav
    adminNav.admin_navbar(root)




def admin_select_student(root):
    # Create main frame
    frame = tk.Frame(root, bg="white", bd=2, relief="solid", padx=20, pady=20)
    frame.pack(expand=True, pady=(20, 20))

    # Title
    title = tk.Label(frame, text="Admin Select Student", font=('Arial', 16), bg="white")
    title.pack(pady=(0, 30))

    # Student ID Entry label
    id_label = tk.Label(frame, text="Enter Student ID", font=('Arial', 12), bg="white")
    id_label.pack(pady=(0, 10),anchor='w')

    # Student ID Entry field
    id_entry = tk.Entry(frame, font=('Arial', 12), width=30)
    id_entry.pack(pady=(0, 20))


    # Student Year Entry label
    year_label = tk.Label(frame, text="Academic Year", font=('Arial', 12), bg="white")
    year_label.pack(pady=(0, 10),anchor='w')
    
    # Academic year options
    academicYear = [
        '2015/2016', '2016/2017', '2017/2018', '2018/2019', '2019/2020',
        '2020/2021', '2021/2022', '2022/2023', '2023/2024', '2024/2025'
    ]

    academic_year_dropdown = ttk.Combobox(frame, values=academicYear, font=('Arial', 12), state="readonly", width=28)
    academic_year_dropdown.pack(pady=(0, 15))


    # Desired GPA Entry label
    gpa_label = tk.Label(frame, text="Desired GPA (Optional)", font=('Arial', 12), bg="white")
    gpa_label.pack(pady=(0, 10),anchor='w')

    # Student ID Entry field
    gpa_entry = tk.Entry(frame, font=('Arial', 12), width=30)
    gpa_entry.pack(pady=(0, 20))

    # Button frame for layout
    button_frame = tk.Frame(frame, bg="white")
    button_frame.pack(fill="x", pady=(10, 20))

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
        command=lambda: validate_and_proceed(id_entry.get().strip(), gpa_entry.get().strip(),academic_year_dropdown.get(),root,frame)
    )
    next_btn.pack(side="right", padx=10)

    backtoStdMenu = tk.Button(frame, text="Back to Menu", font=("Arial", 12), padx=20, bg="#007bff", fg="white", width=23, command= lambda: backToMenu(frame,root))
    backtoStdMenu.pack()



def back_to_admin(frame, root):
    frame.destroy()
    import admin_navbar as nav
    nav.admin_navbar(root)



def validate_and_proceed(student_id,desired_gpa,academic_year,root,frame):  


    # Check if the field is empty
    if student_id == "":
        messagebox.showerror("Error", "Please enter a student ID")
        return
    
    if academic_year =="":
        messagebox.showerror("Error", "Please Select a academic year")
        return
    
    # Check if the input contains only numbers
    if not student_id.isdigit():
        messagebox.showerror("Error", "Student ID must contain only numbers")
        return
    
    #check if the ID entered is 7 digits in length
    if  len(student_id)!=7:
        messagebox.showerror("Error", "Student ID must be 7 digits")
        return
    
    if desired_gpa != '':
        try:
            # Attempt to convert desired_gpa to float
            desired_gpa = float(desired_gpa)
            
            # Check if GPA is within the range 0.0 to 4.3 and has a max of two decimal places
            if 0.0 <= desired_gpa <= 4.3 and len(str(desired_gpa)) <= 4:
                print("Valid GPA entered.")
            else:
                messagebox.showerror("Invalid GPA", "GPA must be between 0.0 and 4.3 with no more than two decimal places.")
                return
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a numeric GPA value.")
            return
    else :
        desired_gpa =2.0



    #check database for student grades
    from Database.admin_Actions import get_student_grades_and_credits
    gradesAndCredit=get_student_grades_and_credits(student_id, academic_year)

    #if the student does not exists or no modules were selecteed in that academic year then we exit the function
    if(gradesAndCredit == None):
        return
    

    sem1Credit=[]
    sem1Grade=[]
    sem2Credit=[]
    sem2Grade=[]
    
    sem1Credit,sem1Grade,sem2Credit,sem2Grade= gradesAndCredit[0],gradesAndCredit[1],gradesAndCredit[2],gradesAndCredit[3]
    root.academicYear =academic_year
    root.stdID=student_id

    #call the prolog  file to set the gpa to what the user entered
    import connect_prolog_and_python as prologConn
    prologConn.consult_prolog()

    #if the gpa is not the default then it will be changes to what the user entered
    if(desired_gpa != 2.0):
        prologConn.update_default_gpa(desired_gpa)
    
    #call a function that is linked to the prolog code that processes the grades and credits 
    # and output the sem 1, sem2 and cumulative GPA
    
    allGPA=prologConn.process_student_grades(sem1Credit,sem1Grade,sem2Credit,sem2Grade)
    allGPA= allGPA.split(',')
    
    root.sem1GPA=allGPA[0]
    root.sem2GPA=allGPA[1]
    root.cumGPA= allGPA[2]
    
    frame.destroy()
    from admin_academic_progress import view_acadmic_progress
    view_acadmic_progress(root)
    


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")
    root.title("Admin Select Student")
    root.adminID = 'adm1'
    root.configure(bg="white")
    
    admin_select_student(root)
    root.mainloop()