import tkinter as tk
from tkinter import ttk


def backToMenu(frame,root):
    frame.destroy()
    
    import admin_navbar as adminNav
    adminNav.admin_navbar(root)



def view_acadmic_progress(root):

    import connect_prolog_and_python as prologConn
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


    label = tk.Label(frame, text=f"Year: {root.academicYear}", font=('default', 12), bg="white")
    label.pack()
    
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

    #label that display sem1GPA
    sem1GPALabel = tk.Label(stdInfoFrame, text=root.sem1GPA, font=('default', 10), bg="white")
    sem1GPALabel.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    sem2GPALabel = tk.Label(stdInfoFrame, text=root.sem2GPA, font=('default', 10), bg="white")
    sem2GPALabel.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    cumGPALabel = tk.Label(stdInfoFrame, text=root.cumGPA, font=('default', 10), bg="white")
    cumGPALabel.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    backtoStdMenu = tk.Button(frame, text="Back to Menu", font=("Arial", 12), padx=20, bg="#007bff", fg="white", width=12, command= lambda: backToMenu(frame,root))
    backtoStdMenu.pack(pady=(10,0), side=tk.LEFT)


