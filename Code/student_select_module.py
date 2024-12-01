import tkinter as tk
from tkinter import messagebox

# Function to update the table with the entered data
def add_row(table, module_code_combobox, module_name_combobox, module_credit_combobox,creditsLabel):
    module_code = module_code_combobox.get()
    module_name = module_name_combobox.get()
    
    try:
        # Try to convert the credit input to an integer
        module_credit = int(module_credit_combobox.get())
    except ValueError:
        module_credit=''
        
    

    if module_code and module_name and module_credit:  # Check that all fields are filled

        # Check if the module already exists in the table
        for item in table.get_children():
            existing_code, _ , _ = table.item(item, 'values')
            if module_code == existing_code:
                
                messagebox.showinfo("Duplicate Module", "This module is already in the table.")
                return  # Exit the function if a duplicate is found
        
        # Get all rows (items) currently in the table
        rows = table.get_children()

        # Extract the credit value for each row and convert it to an integer
        credits = [int(table.item(row, 'values')[2]) for row in rows]

        # Calculate the total credits by summing up the credits list
        total_credits = sum(credits)

        # Check if adding this module will exceed the 21 credit limit
        if total_credits + module_credit > 21:
            messagebox.showinfo("Credit Limit Exceeded", "Adding this module would exceed the 21 credit limit,\ntherefore this module will not be added")
            return  # Exit the function if adding would exceed the credit limit

        table.insert('', 'end', values=(module_code, module_name, module_credit))
        module_code_combobox.delete(0, 'end')
        module_name_combobox.delete(0, 'end')
        module_credit_combobox.delete(0, 'end')

        # Update the total credits by adding the new module's credit
        total_credits += module_credit
        creditsLabel.config(text=f"Total Credits: {total_credits}")
    else:
        messagebox.showinfo("No Module Selected", "Please select a module from the dropdown")
# End of add_row()

#when user selects the record from the drop down this function populates teh input fields
def update_fields(modified_comboBox, module_codes, module_names, module_credits, module_name_combobox, module_credit_combobox, module_code_combobox):
    selected_code = module_code_combobox.get()
    selected_name = module_name_combobox.get()

    # Get the index of the selected module code or name
    index = None
    if modified_comboBox == 'code':
        index = module_codes.index(selected_code)
    elif modified_comboBox == 'module_name':
        index = module_names.index(selected_name)

    if index is not None:
        if modified_comboBox == 'code':
            # Populate the corresponding fields
            module_name_combobox.set(module_names[index])
            module_credit_combobox.set(module_credits[index])
        elif modified_comboBox == 'module_name':
            # Populate the corresponding fields
            module_code_combobox.set(module_codes[index])
            module_credit_combobox.set(module_credits[index])
   

# Function to delete the selected row
def delete_selected_row(table, creditsLabel):
    # Get all selected items in the table
    selected_item = table.selection()

    # Check if any item is selected
    if selected_item:
        recordsCount = 0
        # Calculate the total credits before deleting
        total_credits_to_decrement = 0
        
        # Get all rows (items) and calculate the total credits
        rows = table.get_children()
        credits = [int(table.item(row, 'values')[2]) for row in rows]
        total_credits = sum(credits)

        # Loop through each selected item
        for item in selected_item:
            # Get the credit value of the selected item
            credit_value = int(table.item(item, 'values')[2])
            total_credits_to_decrement += credit_value  # Add the credit to the total to decrement
            
            # Delete the selected item
            table.delete(item)
            
            # Count the number of records deleted
            recordsCount += 1

        # Subtract the total credits of the deleted items from the current total credit
        total_credits -= total_credits_to_decrement


        # Update the credits label with the new total credits
        creditsLabel.config(text=f"Total Credits: {total_credits}")
    else:
        messagebox.showinfo("No Selection", "Please select a record or records, then click Delete.")


def addModuleToDatabase(academicYearComboBox, semesterComboBox, table,root):
    # Check if an academic year and semester have been selected
    academic_year = academicYearComboBox.get().strip()
    semester = semesterComboBox.get().strip()
    
    if not academic_year:  # If no academic year is selected
        messagebox.showinfo("Missing Selection", "Please select an academic year.")
        return  # Exit function
    
    if not semester:  # If no semester is selected
        messagebox.showinfo("Missing Selection", "Please select a semester.")
        return  # Exit function

    # Get all rows (items) and calculate the total credits
    rows = table.get_children()
    credits = [int(table.item(row, 'values')[2]) for row in rows]
    total_credits = sum(credits)

    # Check if the student has at least the minimum amount of credits in sem 1 or sem 2
    #student can select modules that come up to less than 9 credit in sem 3 (summer)
    if total_credits < 9 and (semester== '1' or semester=='2'):
        messagebox.showinfo("Insufficient Credit", "You need to have a minimum of 9 credits in order to confirm selection.")
        return  # Exit function
    
    from Database.student_actions import add_modules_to_enroll

    add_modules_to_enroll(academic_year,semester,root.stdID,table)

     

def backToMenu(frame,root):
        frame.destroy()
        import student_navbar as stdNav
        stdNav.student_navbar(root)


def select_module_interface(root):
    import Database.student_actions as stdAction
    import student_navbar as stdNav

    # Get the student ID the user entered and search the dataase for the student name corresponding with the ID
    stdName=stdAction.get_student_name(root.stdID)
    if stdName == 'N/A':
        stdNav.student_navbar(root)

    else:
        from tkinter import ttk
        stdNameAndID = "Student : " + root.stdID +" - " + stdName
        frame = tk.Frame(root, bg="white")
        frame.pack(expand=True)  # keeps the content in the center of the window

        # Title label
        label = tk.Label(frame, text="Select Your Modules", font=('default', 20), bg="white")
        label.grid(row=0, column=0, pady=(0, 15), columnspan=4)

        # Student information labels

        label = tk.Label(frame, text= stdNameAndID, font=('default', 12), anchor='w', bg="white")
        label.grid(row=1, column=0,columnspan=4,sticky='w')
        # Label and ComboBox combined into a single row, spanning two columns
        label = tk.Label(frame, text="Year : ", anchor='w', font=('default', 12), bg="white")
        label.grid(row=2, column=0, sticky='w')

        
        # Define academic years
        academicYear = ['2015/2016','2016/2017','2017/2018','2018/2019','2019/2020','2020/2021','2021/2022', '2022/2023', '2023/2024', '2024/2025']
        academicYearComboBox = ttk.Combobox(frame, width=10, values=academicYear, state="readonly")
        academicYearComboBox.grid(row=2, column=1, sticky='w')
        
        label = tk.Label(frame, text="Semester : ", anchor='e', font=('default', 12), bg="white")
        label.grid(row=2, column=2, sticky='e')
        
                
        # Define academic years
        semester = [1,2,3]
        semesterComboBox = ttk.Combobox(frame, width=5, values=semester,state="readonly")
        semesterComboBox.grid(row=2, column=3, sticky='w')
        
        # Horizontal separator line
        separator = ttk.Separator(frame, orient='horizontal')
        separator.grid(row=3, column=0, columnspan=4, sticky='ew', pady=(20, 10))
        
        # Subtitle label for the table
        label = tk.Label(frame, text="Modules you selected will appear in this table", font=('default', 10), bg="white", anchor='w')
        label.grid(row=4, column=0, pady=(0,5), sticky='w', columnspan=4)
        
        # Table setup
        table_frame = tk.Frame(frame, bg="white")
        table_frame.grid(row=5, column=0, columnspan=4, sticky="w")  # Added a frame for the table and scrollbar

        table = ttk.Treeview(
            table_frame,
            columns=('Column1', 'Column2', 'Column3'),
            show='headings',
            height=4  # Display only 4 records at a time
        )
        table.heading('Column1', text='Module Code')
        table.heading('Column2', text='Module Name')
        table.heading('Column3', text='Module Credit')

        # Set the width of each column and center the data
        table.column('Column1', width=100, anchor='center')
        table.column('Column2', width=250, anchor='center')
        table.column('Column3', width=100, anchor='center')

        # Add a vertical scrollbar linked to the table
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
        table.configure(yscroll=scrollbar.set)

        # Pack the table and scrollbar side by side
        table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

                
        # Buttons
        removeBtn = tk.Button(frame, text="Remove Module", command=lambda: delete_selected_row(table,creditsLabel))
        removeBtn.grid(row=6, column=0, sticky='w', pady=(5,10),columnspan=2)
        
        confirmModuleBtn = tk.Button(frame, text="Confirm Module Selection", command=lambda : addModuleToDatabase(academicYearComboBox,semesterComboBox,table,root))
        confirmModuleBtn.grid(row=6, column=1, sticky='w', columnspan=2,pady=(5,10), padx=(20,0))

        creditsLabel = tk.Label(frame, text="Total Credits = 0", font=('default', 10), bg="white", anchor='w')
        creditsLabel.grid(row=6, column=3, pady=(5,10), sticky='w',columnspan=2)

        # Horizontal separator line
        separator = ttk.Separator(frame, orient='horizontal')
        separator.grid(row=7, column=0, columnspan=4, sticky='ew', pady=(10, 10))
        
        # Subtitle label for the table
        label = tk.Label(frame, text="Select a module from the drop down", font=('default', 12), bg="white", anchor='w')
        label.grid(row=8, column=0, columnspan=3, pady=(0,5), sticky='w')

        label = tk.Label(frame, text="Module Code", font=('default', 10), bg="white", anchor='w')
        label.grid(row=9, column=0, sticky='w',columnspan=2)

        label = tk.Label(frame, text="Module Name", font=('default', 10), bg="white", anchor='w')
        label.grid(row=9, column=1, sticky='w')

        label = tk.Label(frame, text="Credits", font=('default', 10), bg="white", anchor='w')
        label.grid(row=9, column=3, sticky='w')
        
        # Call the database to retrieve data for dropdowns from the database
        
        module_codes, module_names, module_credits = stdAction.get_all_modules()
        
        # Entry fields for each column
        module_code_combobox = ttk.Combobox(frame, width=9,values=module_codes, state="readonly")
        module_code_combobox.grid(row=10, column=0, sticky='w',columnspan=4)
        module_code_combobox.bind("<<ComboboxSelected>>", lambda event: update_fields('code',module_codes, module_names, module_credits, module_name_combobox, module_credit_combobox,module_code_combobox))
        
        module_name_combobox = ttk.Combobox(frame, width=37, values=module_names,state="readonly")
        module_name_combobox.grid(row=10, column=1, sticky='w', columnspan= 2)
        module_name_combobox.bind("<<ComboboxSelected>>", lambda event: update_fields('module_name',module_codes, module_names, module_credits, module_name_combobox, module_credit_combobox,module_code_combobox))
        
        module_credit_combobox = ttk.Combobox(frame, width=10, values=module_credits,state="readonly")
        module_credit_combobox.grid(row=10, column=3, sticky='w', columnspan=2)
        
        # Button to add row to the table
        add_button = tk.Button(frame, text="Add Module", command=lambda: add_row(table, module_code_combobox, module_name_combobox, module_credit_combobox,creditsLabel))
        add_button.grid(row=11, column=0, pady=10, sticky='w',columnspan=2)
        
        backtoStdMenu = tk.Button(frame, text="Back to Menu", font=("Arial", 12), padx=20, bg="#007bff", fg="white", width=12, command= lambda: backToMenu(frame,root))
        backtoStdMenu.grid(row=12, column=0, sticky="w",pady=(10,0),columnspan=3)
        

