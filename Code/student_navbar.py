import tkinter as tk

def backToLogin(frame,root):
    frame.destroy()#remove current interface

    import Login_Interface as lgInterface
    lgInterface.login_interface(root)#display the login screen

def moduleEnrollment(frame,root):
    frame.destroy()

    import student_select_module as stdModule
    stdModule.select_module_interface(root)
    

def student_navbar(root):
    # Create a frame for the student navbar
    frame = tk.Frame(root, bg="white", bd=2, relief="solid", padx=20, pady=20)
    frame.pack(expand=True, pady=(20,20))  # keeps the content in the center of the window

    # Heading label
    label = tk.Label(frame, text="Student Menu", font=('default', 20), bg="white")
    label.grid(row=0, column=0, pady=(0, 30), columnspan=3)

    # Buttons
    enrollButton = tk.Button(frame, text="Module Enrollment", font=("Arial", 12), padx=20, bg="#007bff",fg="white", width=12, command= lambda: moduleEnrollment(frame,root))
    enrollButton.grid(row=1, column=0, sticky="e", padx=(0,10))

    academicProgButton = tk.Button(frame, text="Academic Progress", font=("Arial", 12), padx=20, bg="#007bff", fg="white", width=12)
    academicProgButton.grid(row=1, column=1, sticky="e", padx=(0,10))

    exitButton = tk.Button(frame, text="Logout", font=("Arial", 12), padx=20, bg="#007bff", fg="white", width=12, command= lambda: backToLogin(frame,root))
    exitButton.grid(row=2, column=0, sticky="w",pady=(10,0))



if __name__ == "__main__":
    
    root = tk.Tk()
    root.geometry("600x600")
    root.title("Academic Probation Login")

    # Set the background color of the root window to white
    root.configure(bg="white")
    
    root.stdID='2400000'
    student_navbar(root)

    root.mainloop()  # Start the Tkinter main loop
