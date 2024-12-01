import tkinter as tk
from tkinter import ttk


def view_acadmic_progress(root):

    from Database.admin_Actions import get_admin_name
    adminName = get_admin_name(root.adminID)

    frame = tk.Frame(root, bd=1, relief="solid", bg='white')
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
    
    label = tk.Label(frame, text=f"GPA: {root.desiredGPA}", font=('default', 12), bg="white")
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

    label = tk.Label(stdInfoFrame, text=root.stdID, font=('default', 10), bg="white")
    label.pack(side=tk.LEFT,padx=(0,30))

    from Database.student_actions import get_student_name
    stdName= get_student_name(root.stdID)
    stdName = tk.StringVar(value=stdName)
    
    stdNameEntry=tk.Entry(stdInfoFrame,width=10, textvariable=stdName,state="readonly")
    stdNameEntry.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    label = tk.Label(stdInfoFrame, text=root.stdID, font=('default', 10), bg="white")
    label.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    label = tk.Label(stdInfoFrame, text=root.stdID, font=('default', 10), bg="white")
    label.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    label = tk.Label(stdInfoFrame, text=root.stdID, font=('default', 10), bg="white")
    label.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)



    





if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")
    root.title("Academic Probation Login")

    # Set the background color of the root window to white
    root.configure(bg="white")
    root.academicYear ='2020/2021'
    root.stdID=2400000
    root.desiredGPA = 2.0
    root.adminID='adm1'
    view_acadmic_progress(root)

    root.mainloop()  # Start the Tkinter main loop