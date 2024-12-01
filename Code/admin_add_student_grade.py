import tkinter as tk
from tkinter import ttk
from tkinter import messagebox



def backToMenu(frame,root):
    frame.destroy()
    
    import admin_navbar as adminNav
    adminNav.admin_navbar(root)


def getAdminName(root):
    # Imports the database actions for the admin
    from Database.admin_Actions import get_admin_name
    # Retrieves the name of the admin
    adminName = get_admin_name(root.adminID)

    # If a name was not received, the user is sent back to the login interface
    if adminName is None:
        from Login_Interface import login_interface
        login_interface(root)

    return adminName


# The function to populate the input fields when a record is selected
def populate_input_fields(tree, moduleCodeEntry, moduleNameEntry, moduleGradeEntry):
    """Populate the input fields with selected record values."""
    selected_item = tree.selection()  # Get selected item

    if moduleGradeEntry == "Not Graded":
        messagebox.showwarning("No Grade","Please select a grade for the student")
        return
    

    if selected_item:

        moduleCodeEntry.config(state="normal")  # Temporarily allow changes to auto-fill
        moduleNameEntry.config(state="normal")  # Temporarily allow changes to auto-fill
        # Get the values of the selected record
        values = tree.item(selected_item[0], 'values')
        module_code, module_name, grade = values

        # Populate the input fields
        moduleCodeEntry.delete(0, tk.END)  # Clear current entry
        moduleCodeEntry.insert(0, module_code)  # Insert module code

        moduleNameEntry.delete(0, tk.END)  # Clear current entry
        moduleNameEntry.insert(0, module_name)  # Insert module name

        moduleGradeEntry.set(grade)  # Set the grade in the combobox

        moduleNameEntry.config(state="readonly")  # Make it readonly again
        moduleCodeEntry.config(state="readonly")  # Make it readonly again



def updateStdGRade(stdID,moduleID,semester,year,moduleGradeEntry,tree):
    
    # Get the selected value from the combobox
    selected_grade = moduleGradeEntry.get()
    import Database.admin_Actions as adminActions
    result=adminActions.update_student_grade(stdID,moduleID,semester,year,selected_grade)
    
    if result == True:
        updatedGrades = adminActions.get_student_grades_for_semester(stdID,year,semester)


        # Clear the tree before inserting new records
        for item in tree.get_children():
            tree.delete(item)
            # Insert grades into the table
        for grade in updatedGrades :
            # Check if there's a grade (i.e., it's not None)
            module_code, module_name, grade_value = grade
            tree.insert("", "end", values=(module_code, module_name, grade_value if grade_value else "Not Graded"))

    





def std_grade_info(root,grades):

    # Function that calls and gets admin Name from the database
    adminName = getAdminName(root)

    # Create a frame for the admin navbar
    frame = tk.Frame(root, bg="white", bd=2, relief="solid", padx=20, pady=20)
    frame.pack(expand=True, pady=20)  # Keeps the content centered in the window

    # Heading label
    label = tk.Label(frame, text="Add Student Grades", font=('default', 16), bg="white")
    label.pack(pady=(0, 20))

    label = tk.Label(frame, text=f"Welcome {adminName}", font=('default', 12), bg="white", anchor='w')
    label.pack()

    # Horizontal separator line
    separator = ttk.Separator(frame, orient='horizontal')
    separator.pack(fill='x', pady=(10, 0))

    # Frame for the table and scrollbar
    table_frame = tk.Frame(frame)
    table_frame.pack(fill=tk.BOTH, expand=True, pady=(10,0))

    # Add a scrollbar to the table_frame
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
    scrollbar.pack(side=tk.RIGHT, fill="y")

    # Create the Treeview (table) widget
    tree = ttk.Treeview(table_frame, columns=("module_code", "module_name", "grade"), show="headings", yscrollcommand=scrollbar.set)
    tree.heading("module_code", text="Module Code")
    tree.heading("module_name", text="Module Name")
    tree.heading("grade", text="Grade")

    # Define column widths
    tree.column("module_code", width=80)
    tree.column("module_name", width=300)
    tree.column("grade", width=80)

    tree.pack(fill=tk.BOTH, expand=True)

    # Link the scrollbar to the treeview
    scrollbar.config(command=tree.yview)

    # Insert grades into the table
    for grade in grades:
        # Check if there's a grade (i.e., it's not None)
        module_code, module_name, grade_value = grade
        tree.insert("", "end", values=(module_code, module_name, grade_value if grade_value else "Not Graded"))


    # Ensure the table is not larger than 4 rows visible by setting the height
    tree.config(height=4)

    # Bind the treeview to the selection event
    tree.bind("<<TreeviewSelect>>", lambda event: populate_input_fields(tree, moduleCodeEntry, moduleNameEntry, moduleGradeEntry))


    # Add a separator after the Edit Record button using side=tk.TOP
    separator_after_button = ttk.Separator(frame, orient='horizontal')
    separator_after_button.pack( fill='x', pady=(0, 20))  # Placing separator at the top

    # Frame for side-by-side labels
    labels_frame = tk.Frame(frame, bg='white', padx=0, pady=0)
    labels_frame.pack(fill="both",expand=True)

    # Module Code
    module_code_label = tk.Label(labels_frame, text="Module Code", bg='white', font=('default', 10), anchor='w', width=15)
    module_code_label.pack(side=tk.LEFT,padx=(0,50))

    # Module Name
    module_name_label = tk.Label(labels_frame, text="Module Name", bg='white', font=('default', 10), anchor='center', width=15)
    module_name_label.pack(side=tk.LEFT)

    # Grade
    module_grade_label = tk.Label(labels_frame, text="Grade", bg='white', font=('default', 10), width=15)
    module_grade_label.pack(side=tk.RIGHT)



    inputFrame = tk.Frame(frame, bg='white',padx=0, pady=0)
    inputFrame.pack(fill="both",expand=True)

    moduleCodeEntry = tk.Entry(inputFrame, width=10,state="readonly")
    moduleCodeEntry.pack(side=tk.LEFT,padx=(0,60))

    moduleNameEntry = tk.Entry(inputFrame,width=40, state="readonly")
    moduleNameEntry.pack(side=tk.LEFT,padx=(0,30))

    # Grade dropdown (read-only)
    moduleGradeEntry = ttk.Combobox(inputFrame, values=["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "U"], state="readonly", width=10)
    moduleGradeEntry.pack(side=tk.LEFT)

    updateBtnFram = tk.Frame( frame, bg='white',padx=0,pady=0)
    updateBtnFram.pack(fill="both",expand=True)

    # Edit Record Button (left-aligned)
    updateRecord = tk.Button(updateBtnFram, text="Update Student Grade", bg="#007bff", fg="white", command=lambda:updateStdGRade(root.stdID,moduleCodeEntry.get().strip(),root.semester,root.year,moduleGradeEntry,tree))
    updateRecord.pack(side=tk.LEFT, pady=(5,0), padx=(0,10))  # Left-align the button

    backtoStdMenu = tk.Button(frame, text="Back to Menu", font=("Arial", 12), padx=20, bg="#007bff", fg="white", width=12, command= lambda: backToMenu(frame,root))
    backtoStdMenu.pack(side=tk.LEFT, pady=(10,0))


        



if __name__ == "__main__":

    root = tk.Tk()
    root.geometry("600x600")
    root.title("Academic Probation")

    # Set the background color of the root window to white
    root.configure(bg="white")
    root.adminID = 'adm2'
    grades= [('CIT2004', 'Object Oriented Programming', None), ('CIT3002', 'Operating Systems', None), ('CIT3015', 'Digital Communication/ Telecommunication', None)]
    std_grade_info(root,grades)

    root.mainloop()  # Start the Tkinter main loop
