import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox


def backToMenu(frame,root):
    frame.destroy()
    
    import admin_navbar as adminNav
    adminNav.admin_navbar(root)

def getStudentGPA(stdID, specifiedYear):

    from Database.admin_Actions import get_student_grades_and_credits


    gradesAndCredit=get_student_grades_and_credits(stdID, specifiedYear)


    #variables that will store credit and grade for each semester
    sem1Credit=[]
    sem1Grade=[]
    sem2Credit=[]
    sem2Grade=[]
    
    #stored credit and grade detail that was returned from database
    sem1Credit,sem1Grade,sem2Credit,sem2Grade= gradesAndCredit[0],gradesAndCredit[1],gradesAndCredit[2],gradesAndCredit[3]
    
    #call the prolog  file to set the gpa to what the user entered
    import connect_prolog_and_python as prologConn
    
    #call a function that is linked to the prolog code that processes the grades and credits 
    # and output the sem 1, sem2 and cumulative GPA in a comma sperated string
    allGPA=prologConn.process_student_grades(sem1Credit,sem1Grade,sem2Credit,sem2Grade)
    allGPA= allGPA.split(',')#put each element in the comma seperated string in its own index
    
    return[allGPA[0],allGPA[1],allGPA[2]]



def addGPADetails(studentRecord,table,academicYear):
    import connect_prolog_and_python as prologConn
    prologConn.consult_prolog
    defaultGPA=prologConn.get_default_gpa()
    #iterate through the list of all studentsID
    for stdID in studentRecord:
        #passes the default academic year and stID to get student GPA info
        getDetails=getStudentGPA(stdID[0],academicYear)
        #display std info in a table if the student info gpa is less than desired gpa
        if float(getDetails[2]) < defaultGPA:
            table.insert("", "end", values=(stdID[0], stdID[1], getDetails[0], getDetails[1], getDetails[2]))
    
    recordCount= len(table.get_children())
    #check if the table is empty
    if recordCount == 0 :
        messagebox.showerror("No records","No student in this academic Year is below the threshold")
    else:
        messagebox.showinfo("Records generated",f"{recordCount} students are below the threshold")

def backToMenu(frame,root):
    frame.destroy()
    
    import admin_navbar as adminNav
    adminNav.admin_navbar(root)


def modifyTable(table,root,academic_year_dropdown):
    
    from Database.admin_Actions import get_students_with_all_grades_in_semester
    studentRecord=get_students_with_all_grades_in_semester(academic_year_dropdown.get())

    # Delete all items from the treeview
    for item in table.get_children():
        table.delete(item)

    #student records were returned
    if studentRecord !=[]:
        root.academicYear = academic_year_dropdown.get()
        addGPADetails(studentRecord,table,academic_year_dropdown.get())
    else:
        messagebox.showinfo("No Students",f"No students has all their grades entered for any semester\nof the {root.academicYear} academic year")




def validate_and_proceed(desired_gpa,root,desired_GPA_label,table,academicYearValue):  

    if desired_gpa != '':
        try:
            # Attempt to convert desired_gpa to float
            desired_gpa = float(desired_gpa)
            
            # Check if GPA is within the range 0.0 to 4.3 and has a max of two decimal places
            if 0.0 <= desired_gpa <= 4.3 and len(str(desired_gpa)) <= 4:
                root.destroy()#closes window when a valid GPA was entered

                #call the prolog  file to set the gpa to what the user entered
                import connect_prolog_and_python as prologConn
                prologConn.consult_prolog()

                #change the gpa in the prolog knowledge base
                prologConn.update_default_gpa(desired_gpa)

                #get default gpa from prolog
                defaultGPA=prologConn.get_default_gpa()
                #update label to display new GPA
                desired_GPA_label.config(text=f"GPA : {defaultGPA}")


                # Clear the table
                for row in table.get_children():
                    table.delete(row)

                from Database.admin_Actions import get_students_with_all_grades_in_semester
                studentRecords=get_students_with_all_grades_in_semester(academicYearValue)

                addGPADetails(studentRecords,table,academicYearValue)

            
            else:
                messagebox.showerror("Invalid GPA", "GPA must be between 0.0 and 4.3 with no more than two decimal places.")
                return
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a numeric GPA value.")
            return
    else :
        messagebox.showerror("Empty Field","Enter your a new GPA threshold")


def showGUI(desired_GPA_label,table,academicYearValue):
    root = tk.Tk()
    root.geometry("300x300")
    root.title("Update GPA")

    # Set the background color of the root window to white
    root.configure(bg="white")


    frame = tk.Frame(root,bg="white")
    frame.pack(expand= True)
    # Desired GPA Entry label
    gpa_label = tk.Label(frame, text="Desired GPA (Optional)", font=('Arial', 12), bg="white")
    gpa_label.pack(pady=(0, 10),anchor='w')

    # Student ID Entry field
    gpa_entry = tk.Entry(frame, font=('Arial', 12), width=30)
    gpa_entry.pack(pady=(0, 20))

        # Next button
    confirmBtn = tk.Button(
        frame,
        text="Confirm",
        font=("Arial", 12),
        width=10,
        bg="#007bff",
        fg="white",
        command=lambda: validate_and_proceed(gpa_entry.get().strip(),root,desired_GPA_label,table,academicYearValue)
    )
    confirmBtn.pack( padx=10)

    root.mainloop()  # Start the Tkinter main loop


def sendAlert(table):
    from Database.admin_Actions import get_student_alert_emails
    from sending_email import send_email
    import connect_prolog_and_python as prologConn
    
    #check if the table is empty
    if len(table.get_children()) == 0 :
        messagebox.showerror("No records","No student in this academic Year is below the threshold")
        return
    email_status=False
    # Consult the Prolog knowledge base and get the default GPA threshold
    prologConn.consult_prolog()
    defaultGPA = prologConn.get_default_gpa()
    
    # Iterate through each record in the table
    for row_id in table.get_children():
        row_data = table.item(row_id)["values"]  # Get the row's data as a list
        
        # Extract necessary values, 
        student_id = row_data[0]  #  first column is Student ID
        cumulative_gpa = row_data[-1]  #  last column is Cumulative GPA
        
        # Check if the GPA is below the default threshold
        if float(cumulative_gpa) < defaultGPA:

            #query database to get the email of the student as well as email of their faculty admin, advisor and program director
            #The query also retrieved the school, programme and name of the student
            
            stdName,student_email,programme,school,faculty_admin_email,advisor_email,prog_dir_email=get_student_alert_emails(student_id)
                    
            send_email(student_email,f"{faculty_admin_email}; {advisor_email}; {prog_dir_email};",cumulative_gpa,defaultGPA,programme,school,stdName,student_id)
            email_status=True
    
    if email_status == True:
        messagebox.showinfo("Alert", "All Emails were sent successfully")
    

def view_acadmic_progress(root):

    import connect_prolog_and_python as prologConn
    prologConn.consult_prolog()
    defaultGPA=prologConn.get_default_gpa()


    from Database.admin_Actions import get_admin_name
    adminName = get_admin_name(root.adminID)

    frame = tk.Frame(root, bd=1, relief="solid", bg='white',padx=20, pady=20)
    frame.pack(expand=True)

    label = tk.Label(frame, text="Academic Progress", font=('default', 18), bg="white")
    label.pack(pady=(0,10))

    adminName_frame = tk.Frame(frame,  bg='white')
    adminName_frame.pack(fill="both",expand=True)

    label = tk.Label(adminName_frame, text=f"Welcome: {adminName}", font=('default', 12), bg="white")
    label.pack(side=tk.LEFT)

    separator = ttk.Separator(frame, orient='horizontal')
    separator.pack(fill='x', pady=(10, 0))

    yearFrame = tk.Frame(frame,bg='white')
    yearFrame.pack()

    label = tk.Label(yearFrame, text="Year:", font=('default', 12), bg="white")
    label.pack(side=tk.LEFT)
        # Academic year options
    academicYear = [
        '2015/2016', '2016/2017', '2017/2018', '2018/2019', '2019/2020',
        '2020/2021', '2021/2022', '2022/2023', '2023/2024', '2024/2025'
    ]

    academic_year_dropdown = ttk.Combobox(yearFrame, values=academicYear, font=('Arial', 10), state="readonly", width=11)
    academic_year_dropdown.pack(side=tk.LEFT)
    academic_year_dropdown.set(root.academicYear)

    desired_GPA_label = tk.Label(frame, text=f"GPA: {defaultGPA}", font=('default', 12), bg="white")
    desired_GPA_label.pack(pady=(0,15))

    # Create a frame for the table and scrollbar
    table_frame = ttk.Frame(frame)
    table_frame.pack(fill="both", expand=True)

    # Create a vertical scrollbar
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    # Create the Treeview widget with specified columns
    columns = ("Student ID", "Student Name", "GPA Sem1", "GPA Sem2", "Cumulative GPA")
    table = ttk.Treeview(table_frame,columns=columns,show="headings",height=5,yscrollcommand=scrollbar.set)
    table.pack(fill="both", expand=True)

    # Configure the scrollbar
    scrollbar.config(command=table.yview)

    # Define the headings and column widths
    table.heading("Student ID", text="Student ID")
    table.column("Student ID", width=80)  # Adjust width for Student ID

    table.heading("Student Name", text="Student Name")
    table.column("Student Name", width=200)  # Adjust width for Student Name

    table.heading("GPA Sem1", text="GPA Sem1")
    table.column("GPA Sem1", width=80)  # Adjust width for GPA Sem1

    table.heading("GPA Sem2", text="GPA Sem2")
    table.column("GPA Sem2", width=80)  # Adjust width for GPA Sem2

    table.heading("Cumulative GPA", text="Cumulative GPA")
    table.column("Cumulative GPA", width=100)  # Adjust width for Cumulative GPA
    academic_year_dropdown.bind("<<ComboboxSelected>>", lambda event: modifyTable(table,root,academic_year_dropdown))

    from Database.admin_Actions import get_students_with_all_grades_in_semester
    studentRecord=get_students_with_all_grades_in_semester(root.academicYear)

    if studentRecord !=[]:
        addGPADetails(studentRecord,table,root.academicYear)
    else:
         messagebox.showinfo("No Students",f"No students has all their grades entered for any semester\nof the {root.academicYear} academic year")
    
    buttonFrame = tk.Frame(frame, bg='white')
    buttonFrame.pack(expand= True, fill= "both",pady=(5,0))

    backtoStdMenu = tk.Button(buttonFrame, text="Back to Menu", font=("Arial", 10), bg="#007bff", fg="white", width=10, command= lambda: backToMenu(frame,root))
    backtoStdMenu.pack(side=tk.LEFT, padx=(0,10))

    updateGPABtn=tk.Button(buttonFrame,text="Update Default GPA", command=lambda: showGUI(desired_GPA_label,table,academic_year_dropdown.get()))
    updateGPABtn.pack(side=tk.LEFT, padx=(0,10))
    
    sendEmailBtn=tk.Button(buttonFrame,text="Send Alerts", command=lambda: sendAlert(table))
    sendEmailBtn.pack(side=tk.LEFT, padx=(0,10))




if __name__ == "__main__":
    
    root = tk.Tk()
    root.geometry("700x700")
    root.title("Academic Probation Login")

    # Set the background color of the root window to white
    root.configure(bg="white")
    root.adminID='adm1'
    root.academicYear="2024/2025"
    view_acadmic_progress(root)
    

    root.mainloop()  # Start the Tkinter main loop