import tkinter as tk
import tkinter.ttk as ttk  # Import ttk for 
import Database.verify_credentials  as dbVerify
import tkinter.messagebox as messagebox
import admin_navbar as adminNav
#functions

def validateLoginDetails():
    id = usernameEntry.get().strip()
    password = passwordEntry.get().strip()
    userType = dropdown.get()
    validationMessage=''

    if id == '':
        validationMessage += "• Username field is empty\n"
    if password == '':
        validationMessage += "• password field is empty\n"
    if userType=='Select a User Type':
        validationMessage += "• A user type was not selected\n"

    if validationMessage != '':
        # Display validation messages in a messagebox
        messagebox.showerror("Validation Error", validationMessage)
    else:
        verifyLoginDetails(id,password,userType)
        

root = tk.Tk()

root.geometry("600x600")
root.title("Academic Probation Login")

# Set the background color of the root window to white
root.configure(bg="white")


def verifyLoginDetails(id,password,userType):

    result = False

    #if the user want to login as an admin then the respective function will run to check if the data entered matched a record in the database
    if userType =='Admin':
        #return true if a corresponding record is found in the database and false if a record could not be found
        result=dbVerify.verify_admin_credentials(id, password)
    elif userType =='Student':
        result=dbVerify.verify_student_credentials(id,password)

    #if a corresponding record could or could not be found then the user will be alerted with a popup message
    if result == False:
       messagebox.showerror("Validation Error", "Invalid Credentials")
    elif result == True :
        
        messagebox.showinfo("Confirmation Message", "You have logged in successfully")
                # Clear the current frame and replace it with the admin navbar

        #if a person has successfully login as admin then they will see the dashboard
        if userType =='Admin':
            for widget in root.winfo_children():  # Remove all widgets in the current window
                widget.destroy()  # Destroy each widget

            admin_frame = adminNav.admin_navbar(root)  # Create the new admin navbar frame
            admin_frame.pack(expand=True)  # Pack the new frame


frame = tk.Frame(root,bg="white")
frame.pack(expand=True)#keeps the  content in the center of the window

label = tk.Label(frame, text="Login", font=('default', 20),bg="white")
label.grid(row=0, column=0, pady=(0, 30), columnspan=2)


userType=["Select a User Type","Student","Admin"]
dropdown=ttk.Combobox(frame,values=userType, state="readonly",width=16)
dropdown.set(userType[0])
dropdown.grid(row=1,column=1)


# Create the left-aligned username label
label = tk.Label(frame, text="Username", anchor='w', font=('default', 15),bg="white")
label.grid(row=2, column=0, sticky='w', columnspan=2)


# Input field for username using ttk.Entry
usernameEntry = tk.Entry(frame, width=38,bd=0,bg="white", background="#f0f0f0")
usernameEntry.grid(row=3, column=0, columnspan=2)

# Simulate the bottom border using a frame right below the Entry widget
bottom_border = tk.Frame(frame, bg="black", height=2, width=230)  
bottom_border.grid(row=4, column=0, pady=(0, 15), columnspan=2)

label = tk.Label(frame, text="Password", font=("Arial", 15),bg="white")
label.grid(row=5, column=0, sticky='w', columnspan=2)

# Input field for password
passwordEntry = tk.Entry(frame, width=38, show="*",bd=0,bg="#f0f0f0")
passwordEntry.grid(row=6, column=0, columnspan=2)

# Simulate the bottom border using a frame right below the Entry widget
bottom_border = tk.Frame(frame, bg="black", height=2, width=230)  
bottom_border.grid(row=7, column=0, pady=(0, 15), columnspan=2)

# Clear and Submit buttons
clearButton = tk.Button(frame,text="Clear", font=("Arial", 12),padx=20,bg="#007bff",fg="white",width=6)
clearButton.grid(row=8, column=0,sticky="w")

submitButton = tk.Button(frame, text="Submit",font=("Arial", 12), padx=20, bg="#007bff",fg="white", width=6, command=validateLoginDetails )
submitButton.grid(row=8, column=1,sticky="e")



# Loop to display GUI
root.mainloop()