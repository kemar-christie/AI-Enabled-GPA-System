import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox




def backToMenu(root,frame):
    
    #the frame may be none is the studnet clicks academic progress and has not gotten all grades for any academic year

    if frame is not None:
        frame.destroy()

    from student_navbar import student_navbar
    student_navbar(root)#go back to nav bar


def getStudentGPA(root, specifiedYear):

    from Database.admin_Actions import get_student_grades_and_credits

    #when the  program is running for the first  time we get the gpa info for the latest valid year 
    if specifiedYear is None:
        gradesAndCredit=get_student_grades_and_credits(root.stdID, root.academicYear)
    else:
        gradesAndCredit=get_student_grades_and_credits(root.stdID, specifiedYear)


    #if the student does not exists or no modules were selecteed in that academic year then we exit the function
    if(gradesAndCredit == None):
        return
    
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


def on_select(event, academicYear_dropdown,sem1GPALabel,sem2GPALabel,cumGPALabel,root):
    
    #stores gpa info in variable
    gpaInfo=getStudentGPA(root,academicYear_dropdown.get())

    #if the student did nto select any modules in that academic year or recieved grades for 
    #all modules in that year none will be returned
    if gpaInfo is None:
        #ensure the dropdown changes back to a valid year 
        academicYear_dropdown.set(root.academicYear)
        return
    else:
        root.academicYear = academicYear_dropdown.get()
    
    academicYear_dropdown.set(root.academicYear)

    sem1GPA,sem2GPA,cumGPA= gpaInfo

    sem1GPALabel.config(text=sem1GPA)
    sem2GPALabel.config(text=sem2GPA)
    cumGPALabel.config(text=cumGPA)



def view_acadmic_progress(root):

    #get the latest year that the student has all grdes for both sem in a academic year
    from Database.student_actions import find_latest_academic_year_with_all_grades
    root.academicYear=find_latest_academic_year_with_all_grades(root.stdID)

    #if there is not a academic year where the student got all grades for both sem then they will be sent back to nav bar screen
    if root.academicYear is None:
        backToMenu(root,None)
        return #prevent the rest of the program from running if a year was not returned

    #get default GPA from Prolog
    import connect_prolog_and_python as prologConn
    prologConn.consult_prolog()
    defaultGPA=prologConn.get_default_gpa()

    #get student name from the database by using their ID
    from Database.student_actions import get_student_name
    stdName = get_student_name(root.stdID)

    frame = tk.Frame(root, bd=1, relief="solid", bg='white',padx=20, pady=20)
    frame.pack(expand=True)

    label = tk.Label(frame, text="Academic Progress", font=('default', 18), bg="white")
    label.pack(pady=(0,10))

    adminName_frame = tk.Frame(frame,  bg='white')
    adminName_frame.pack(fill="both",expand=True)

    label = tk.Label(adminName_frame, text=f"Hello, {stdName}", font=('default', 12), bg="white")
    label.pack(side=tk.LEFT)

    separator = ttk.Separator(frame, orient='horizontal')
    separator.pack(fill='x', pady=(10, 0))

    yearFrame=tk.Frame(frame,bg='white')
    yearFrame.pack()

    # Create and pack the label
    label = tk.Label(yearFrame, text="Year:", font=('default', 12), bg="white")
    label.grid(row=0,column=0)

    # Academic year options
    academicYear = [
        '2015/2016', '2016/2017', '2017/2018', '2018/2019', '2019/2020',
        '2020/2021', '2021/2022', '2022/2023', '2023/2024', '2024/2025'
    ]

    # Create the dropdown (Combobox) and set the default value to root.academicYear
    academicYear_dropdown = ttk.Combobox(yearFrame, values=academicYear, font=('Arial', 10), state="readonly", width=9)
    academicYear_dropdown.set(root.academicYear)  # Set default value to the academic year
    academicYear_dropdown.grid(row=0,column=1,pady=5)
    
    label = tk.Label(frame, text=f"GPA: {defaultGPA}", font=('default', 12), bg="white")
    label.pack(pady=(0,15))
    
    #frame that holds the labels for student Info
    labelFrame = tk.Frame(frame,  bg='white')
    labelFrame.pack(fill="both",expand=True)

    label = tk.Label(labelFrame, text="Student ID", font=('default', 12), bg="white")
    label.pack(side=tk.LEFT,padx=(0,10))

    label = tk.Label(labelFrame, text="Student Name", font=('default', 12), bg="white")
    label.pack(side=tk.LEFT,padx=(0,30))

    label = tk.Label(labelFrame, text="GPA Sem 1", font=('default', 12), bg="white")
    label.pack(side=tk.LEFT,padx=(0,10))

    label = tk.Label(labelFrame, text="GPA Sem 2", font=('default', 12), bg="white")
    label.pack(side=tk.LEFT,padx=(0,10))

    label = tk.Label(labelFrame, text="Cumulative GPA", font=('default', 12), bg="white")
    label.pack(side=tk.LEFT)

    #frame that holds the labels for student Info
    stdInfoFrame = tk.Frame(frame,  bg='white')
    stdInfoFrame.pack(fill="both",expand=True)

    #label that display student id
    label = tk.Label(stdInfoFrame, text=root.stdID, font=('default', 10), bg="white")
    label.pack(side=tk.LEFT,padx=(0,30))

    #retrieve student name from database using the ID
    from Database.student_actions import get_student_name
    stdName= get_student_name(root.stdID)
    stdName = tk.StringVar(value=stdName)
    
    #input field that display student name
    stdNameEntry=tk.Entry(stdInfoFrame,width=10, textvariable=stdName,state="readonly")
    stdNameEntry.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    
    #get the student GPA 
    sem1GPA,sem2GPA,cumGPA=getStudentGPA(root,None)
    
    #label that display sem1GPA
    sem1GPALabel = tk.Label(stdInfoFrame, text=sem1GPA, font=('default', 10), bg="white")
    sem1GPALabel.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    
    sem2GPALabel = tk.Label(stdInfoFrame, text=sem2GPA, font=('default', 10), bg="white")
    sem2GPALabel.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    cumGPALabel = tk.Label(stdInfoFrame, text=cumGPA, font=('default', 10), bg="white")
    cumGPALabel.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    backtoStdMenu = tk.Button(frame, text="Back to Menu", font=("Arial", 12), padx=20, bg="#007bff", fg="white", width=12, command= lambda: backToMenu(root,frame))
    backtoStdMenu.pack(pady=(10,0), side=tk.LEFT)

    # Bind the selection event to the on_select function
    academicYear_dropdown.bind("<<ComboboxSelected>>", lambda event: on_select(event, academicYear_dropdown,sem1GPALabel,sem2GPALabel,cumGPALabel,root))

    

if __name__ == "__main__":
    
    root = tk.Tk()
    root.geometry("700x700")
    root.title("Academic Probation Login")

    # Set the background color of the root window to white
    root.configure(bg="white")
    root.stdID='2400026'
    view_acadmic_progress(root)

    root.mainloop()  # Start the Tkinter main loop

