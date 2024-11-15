import tkinter as tk
from tkinter import messagebox


def backToMenu(frame,root):
        frame.destroy()
        import student_navbar as stdNav
        stdNav.student_navbar(root,id)



def getAdminName(root, adminID):
    #imports the database actions for the admin
    from Database.admin_Actions import get_admin_name
    #retrieves the name of the admin
    adminName = get_admin_name(adminID)

    #if a name was not recieved teh user is sent back to the login interface
    if adminName is None:
        from Login_Interface import login_interface
        login_interface(root)

    return adminName



def addModuleToTable(table, moduleCodeEntry, moduleNameEntry, moduleCreditEntry):
    # Retrieve module information from entry fields
    module_code = moduleCodeEntry.get().strip()
    module_name = moduleNameEntry.get().strip()
    module_credit = moduleCreditEntry.get().strip()

    # Validate that all fields are filled
    if not module_code or not module_name or not module_credit:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    #ensure
    if len(module_code)>10 or len(module_code)<7:
        messagebox.showwarning("Module Code Error", "Module Code should not be longer than 10\nand less than 7 char long")
        return
    
    # Ensure module credit is a whole number between 0 and 4
    try:
        module_credit = int(module_credit)  # Attempt to convert to an integer
        if module_credit not in [0, 1, 2, 3, 4]:  # Check if it's within the acceptable range
            messagebox.showwarning("Credit Error", "Module credit must be an integer between 0 and 4.")
            return
    except ValueError:
        messagebox.showwarning("Credit Error", "Module credit must be a whole number between 0 and 4.")
        return

    # Check if module code already exists in the table
    for item in table.get_children():
        if table.item(item, 'values')[0] == module_code:
            messagebox.showwarning("Duplicate Module", "A module with this code already exists.")
            return

    # If module is unique and credit is valid, add it to the table
    table.insert("", "end", values=(module_code.upper(), module_name, module_credit))

    # Clear the entry fields after adding
    moduleCodeEntry.delete(0, tk.END)
    moduleNameEntry.delete(0, tk.END)
    moduleCreditEntry.delete(0, tk.END)


def deleteRecordFromTable(table):
    # Get selected items in the table
    selected_items = table.selection()
    
    if not selected_items:
        messagebox.showwarning("Selection Error", "Please select at least one record to delete.")
        return

    # Confirm deletion
    if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected record(s)?"):
        # Remove each selected item from the table
        for item in selected_items:
            table.delete(item)


def addModuleToDatabase(table):
    # Check if the table has any records
    if not table.get_children():
        # If there are no records, show a message and return
        messagebox.showinfo("No Modules", "There are no modules to add to the database.")
        return

    # If there are records, proceed with adding them to the database
    from Database.admin_Actions import add_modules_to_database
    add_modules_to_database(table)



def add_module_interface(root, adminID):

    adminName=getAdminName(root, adminID)

    #if a name was not recieved the user will not be able to add a module
    if adminName is None:
        return 
    
    from tkinter import ttk

    frame = tk.Frame(root, bg="white")
    frame.pack(expand=True)  # keeps the content in the center of the window

    label = tk.Label(frame, text="Add Modules", font=('default', 20), bg="white")
    label.grid(row=0, column=0, columnspan=3)

    label = tk.Label(frame, text=f"Welcome {adminName}", font=('default', 12), bg="white",anchor='w')
    label.grid(row=1, column=0, columnspan=3,sticky='w')

    # Horizontal separator line
    separator = ttk.Separator(frame, orient='horizontal')
    separator.grid(row=2, column=0, columnspan=3, sticky='ew', pady=(10, 20))

    # Table setup with a Scrollbar
    table_frame = tk.Frame(frame)  # Frame to hold the table and scrollbar
    table_frame.grid(row=3, column=0, columnspan=3, sticky='w')

    table = ttk.Treeview(table_frame, columns=('Column1', 'Column2', 'Column3'), show='headings', height=4)
    table.heading('Column1', text='Module Code')
    table.heading('Column2', text='Module Name')
    table.heading('Column3', text='Module Credit')

    # Set the width of each column and center the data
    table.column('Column1', width=100, anchor='center')
    table.column('Column2', width=250, anchor='center')
    table.column('Column3', width=100, anchor='center')
    table.pack(side="left", fill="y")  # Packs the table inside the frame

    # Add a vertical scrollbar to the table
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Buttons
    removeBtn = tk.Button(frame, text="Remove Module", command=lambda: deleteRecordFromTable(table))
    removeBtn.grid(row=4, column=0, sticky='w', pady=(5,10),columnspan=2)
    
    addToDatabaseBtn = tk.Button(frame, text="Add to Database", command= lambda: addModuleToDatabase(table))
    addToDatabaseBtn.grid(row=4, column=1, sticky='w', pady=(5,10), padx=(0,0),columnspan=2)

    # Horizontal separator line
    separator = ttk.Separator(frame, orient='horizontal')
    separator.grid(row=5, column=0, columnspan=3, sticky='ew', pady=(10, 20))


    #heading for input field
    label = tk.Label(frame, text="Module Code", font=('default', 10), bg="white", anchor='w')
    label.grid(row=6, column=0, sticky='w',columnspan=2)

    label = tk.Label(frame, text="Module Name", font=('default', 10), bg="white", anchor='w')
    label.grid(row=6, column=1)

    label = tk.Label(frame, text="Module Credits", font=('default', 10), bg="white", anchor='w')
    label.grid(row=6, column=2,columnspan=2)

    #input fields to add module
    moduleCodeEntry = tk.Entry(frame, width=13,background="#f0f0f0")
    moduleCodeEntry.grid(row=7, column=0,sticky='w',columnspan=3)

    moduleNameEntry = tk.Entry(frame, width=30,background="#f0f0f0")
    moduleNameEntry.grid(row=7, column=1,columnspan=2,sticky='w')

    moduleCreditEntry = tk.Entry(frame, width=5,background="#f0f0f0")
    moduleCreditEntry.grid(row=7, column=2)

    add_button = tk.Button(frame, text="Add Module", command= lambda: addModuleToTable(table, moduleCodeEntry, moduleNameEntry, moduleCreditEntry))
    add_button.grid(row=8, column=0, pady=15, sticky='w',columnspan=2)
    
    backtoStdMenu = tk.Button(frame, text="Back to Menu", font=("Arial", 12), padx=20, bg="#007bff", fg="white", width=12, command= lambda: backToMenu(frame,root,id))
    backtoStdMenu.grid(row=9, column=0, sticky="w",columnspan=3)
        


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")
    root.title("Academic Probation Login")

    # Set the background color of the root window to white
    root.configure(bg="white")

    add_module_interface(root, "adm1")

    root.mainloop()  # Start the Tkinter main loop



'''
    1) Ensure that after all modules have been added the table is empty
    2) create a display button to show all modules
'''