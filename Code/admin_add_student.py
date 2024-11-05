import tkinter as tk
import tkinter.ttk as ttk  # Import ttk for styling



def clearAll(fullNameEntry, emailEntry, passwordEntry, schoolEntry, programmeEntry,advNameEntry, advEmailEntry, progDirNameEntry, progDirEmailEntry, facAdminNameEntry, facAdminEmailEntry):
    # Clear all entry fields
    fullNameEntry.delete(0, tk.END)
    emailEntry.delete(0, tk.END)
    passwordEntry.delete(0, tk.END)
    schoolEntry.delete(0, tk.END)
    programmeEntry.delete(0, tk.END)
    advNameEntry.delete(0, tk.END)
    advEmailEntry.delete(0, tk.END)
    progDirNameEntry.delete(0, tk.END)
    progDirEmailEntry.delete(0, tk.END)
    facAdminNameEntry.delete(0, tk.END)
    facAdminEmailEntry.delete(0, tk.END)

def validation( fullNameEntry, emailEntry, passwordEntry, schoolEntry, programmeEntry,advNameEntry, advEmailEntry, progDirNameEntry, progDirEmailEntry, facAdminNameEntry, facAdminEmailEntry):
    fullName = fullNameEntry.get().strip()
    email = emailEntry.get().strip()
    password= passwordEntry.get()
    school = schoolEntry.get().strip()
    programme = programmeEntry.get().strip()
    advName= advNameEntry.get().strip()
    advEmail=advEmailEntry.get().strip()
    progDirName=progDirNameEntry.get().strip()
    progDirEmail=progDirEmailEntry.get().strip()
    facAdminName=facAdminNameEntry.get().strip()
    facAdminEmail=facAdminEmailEntry.get().strip()

    import re  # Importing regex for password validation

    validationMessage = ''
    # Regular expression for validating an Email
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    if fullName == '':
        validationMessage += "• First name field is empty\n"
    if email=='':
        validationMessage += "• Email field is empty\n"
    elif not re.match(regex, email):
        validationMessage += "• Email field is Invalid\n"
    if password == '':
        validationMessage += "• Password field is empty\n"
    elif len(password) < 8:
        validationMessage += "• Password must be at least 8 characters long\n"
    elif not re.search("[a-z]", password):  # Check for lowercase letter
        validationMessage += "• Password must contain at least one lowercase letter\n"
    elif not re.search("[A-Z]", password):  # Check for uppercase letter
        validationMessage += "• Password must contain at least one uppercase letter\n"
    elif not re.search("[0-9]", password):  # Check for a digit
        validationMessage += "• Password must contain at least one digit\n"

    if school =='':
        validationMessage+="• School field is empty\n"

    if programme=='':
        validationMessage+="• Programme field is empty\n"

    if advName =='':
        validationMessage+="• Advisor name field is empty\n"
    if advEmail =='':
        validationMessage+="• Advisor email field is empty\n"
    elif not re.match(regex, advEmail):
        validationMessage += "• Advisor email is Invalid\n"

    if progDirName =='':
        validationMessage+="• Programme Director name field is empty\n"
    if progDirEmail=='':
        validationMessage+="• Programme Director email is empty\n"
    elif not re.match(regex, progDirEmail):
        validationMessage += "• Programme Director email is Invalid\n"

    if facAdminName =='':
        validationMessage+="• Faculty Admin name field is empty\n"
    if facAdminEmail=='':
        validationMessage+="• Faculty Admin email field is empty\n"
    elif not re.match(regex, facAdminEmail):
        validationMessage += "• Faculty Admin email is Invalid\n"

    if validationMessage != '':
        # Display validation messages in a messagebox
        import tkinter.messagebox as messagebox
        messagebox.showerror("Validation Error", validationMessage)
    else:

        import Database.admin_Actions as adminAction
        adminAction.add_student_and_alert(fullName,email,password,school,programme,advName,advEmail,progDirName,progDirEmail,facAdminEmail,facAdminName)
        
        #clear all data in the field
        clearAll(fullNameEntry, emailEntry, passwordEntry, schoolEntry, programmeEntry,advNameEntry, advEmailEntry, progDirNameEntry, progDirEmailEntry, facAdminNameEntry, facAdminEmailEntry)
        
def backToMenu(frame,root):
    # Destroy the current frame (navbar) before loading the new one
    frame.destroy()
    #Displays the admin menu
    import admin_navbar as adminNav
    adminNav.admin_navbar(root)

def addAdminInterface(root):

    frame = tk.Frame(root, bg='white', bd=2, relief="solid", padx=20, pady=20)
    frame.pack(expand=True)

    #heading
    label = tk.Label(frame, text="--- Student Info ---", font=('default',22), bg="white")
    label.grid(row=0, column=0, pady=(0, 10), columnspan=2)

    label = tk.Label(frame, text="Full Name",anchor="w", font=('default',12),bg="white")
    label.grid(row=1,column=0, sticky="w")

    fullNameEntry = tk.Entry(frame,width=20,bd=1,relief="solid",background="#f0f0f0")
    fullNameEntry.grid(row=2, column=0,sticky="w")

    label = tk.Label(frame, text="Email", font=('default',12),bg="white",anchor="w")
    label.grid(row=1,column=1,sticky="w")
    
    emailEntry = tk.Entry(frame,width=20,bd=1, relief="solid",background="#f0f0f0")
    emailEntry.grid(row=2, column=1,sticky="w")

    label = tk.Label(frame, text="Password",anchor="w", font=('default',12),bg="white")
    label.grid(row=3,column=0,sticky="w",pady=(15,0))

    passwordEntry = tk.Entry(frame,width=20,bd=1, show="*",relief="solid",background="#f0f0f0")
    passwordEntry.grid(row=4, column=0,sticky="w")

    label = tk.Label(frame, text="School", font=('default',12),bg="white",anchor="w")
    label.grid(row=3,column=1,pady=(15,0),sticky="w")
    
    schoolEntry = tk.Entry(frame,width=20,bd=1, relief="solid",background="#f0f0f0")
    schoolEntry.grid(row=4, column=1,sticky="w")


    label = tk.Label(frame, text="Programme",anchor="w", font=('default',12),bg="white")
    label.grid(row=5,column=0,sticky="w",pady=(15,0))

    programmeEntry = tk.Entry(frame,width=20,bd=1, relief="solid",background="#f0f0f0")
    programmeEntry.grid(row=6, column=0,sticky="w")

    """
        This section of the form accepts input for persons that will be notified if
        the student does not meet the desired GPA
    """

    label = tk.Label(frame, text="--- Alert ---", font=('default',22), bg="white")
    label.grid(row=7, column=0, pady=(20, 10), columnspan=2)


    label= tk.Label(frame, text="Advisor Name", font=("TKDefaultFont",12),bg="white",anchor="w")
    label.grid(row=8, column=0,sticky="w")

    label= tk.Label(frame, text="Advisor Email", font=("TKDefaultFont",12),bg="white",anchor="w")
    label.grid(row=8, column=1,sticky="w")

    advNameEntry = tk.Entry(frame,width=20,bd=1, relief="solid",background="#f0f0f0")
    advNameEntry.grid(row=9, column=0,pady=(0,20),sticky="w")

    advEmailEntry = tk.Entry(frame,width=20,bd=1, relief="solid",background="#f0f0f0")
    advEmailEntry.grid(row=9, column=1,pady=(0,20) ,sticky="w")

    #Program Director

    label= tk.Label(frame, text="Prog. Dir. Name", font=("TKDefaultFont",12),bg="white",anchor="w")
    label.grid(row=10, column=0,sticky="w")

    label= tk.Label(frame, text="Prog. Dir. Email", font=("TKDefaultFont",12),bg="white",anchor="w")
    label.grid(row=10, column=1,sticky="w")

    progDirNameEntry = tk.Entry(frame,width=20,bd=1, relief="solid",background="#f0f0f0")
    progDirNameEntry.grid(row=11, column=0,pady=(0,20) ,sticky="w")

    progDirEmailEntry = tk.Entry(frame,width=20,bd=1, relief="solid",background="#f0f0f0")
    progDirEmailEntry.grid(row=11, column=1,pady=(0,20),sticky="w")

    #Faculty Admin

    label= tk.Label(frame, text="Fac. Admin Name", font=("TKDefaultFont",12),bg="white",anchor="w")
    label.grid(row=12, column=0,sticky="w")

    label= tk.Label(frame, text="Fac. Admin Email", font=("TKDefaultFont",12),bg="white",anchor="w")
    label.grid(row=12, column=1,sticky="w")

    facAdminNameEntry = tk.Entry(frame,width=20,bd=1, relief="solid",background="#f0f0f0")
    facAdminNameEntry.grid(row=13, column=0, pady=(0,15),sticky="w")

    facAdminEmailEntry = tk.Entry(frame,width=20,bd=1, relief="solid",background="#f0f0f0")
    facAdminEmailEntry.grid(row=13, column=1,pady=(0,15) ,sticky="w")

    #buttons

    # Clear and Submit buttons
    clearButton = tk.Button(frame,text="Clear", font=("Arial", 12),padx=20,bg="#007bff",fg="white",width=6, command=lambda: clearAll(fullNameEntry, emailEntry, passwordEntry, schoolEntry, programmeEntry,advNameEntry, advEmailEntry, progDirNameEntry, progDirEmailEntry, facAdminNameEntry, facAdminEmailEntry))
    clearButton.grid(row=14, column=0,sticky="w")

    submitButton = tk.Button(frame, text="Submit",font=("Arial", 12), padx=20, bg="#007bff",fg="white", width=6,command=lambda: validation(fullNameEntry, emailEntry, passwordEntry, schoolEntry, programmeEntry, advNameEntry, advEmailEntry, progDirNameEntry, progDirEmailEntry, facAdminNameEntry, facAdminEmailEntry))
    submitButton.grid(row=14, column=1,sticky="e", padx=(0,7))

    backButton = tk.Button(frame,text="Back to Menu", font=("Arial", 12),padx=20,bg="#007bff",fg="white",width=23,command=lambda: backToMenu(frame,root))
    backButton.grid(row=15, column=0,sticky="w", pady=(10,0), columnspan=2)
    
    root.mainloop()  # Keep the Tkinter main loop active



