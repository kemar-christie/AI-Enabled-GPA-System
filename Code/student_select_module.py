import tkinter as tk


# Function to update the table with the entered data
def add_row(table, module_code_combobox, module_name_combobox, module_credit_combobox):
    code = module_code_combobox.get()
    name = module_name_combobox.get()
    credit = module_credit_combobox.get()
    
    if code and name and credit:  # Check that all fields are filled
        table.insert('', 'end', values=(code, name, credit))
        module_code_combobox.delete(0, 'end')
        module_name_combobox.delete(0, 'end')
        module_credit_combobox.delete(0, 'end')

        # Increase the height of the table by 1 row
        current_height = table['height']
        table.config(height=current_height + 1)
# End of add_row()


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
def delete_selected_row(table):
    selected_item = table.selection()
    if selected_item:
        table.delete(selected_item)
        # Increase the height of the table by 1 row
        current_height = table['height']
        table.config(height=current_height -1)
    else:
        from tkinter import messagebox
        messagebox.showinfo("No Selection", "Please select a record first, then click Delete.")


def select_module_interface(root):
    frame = tk.Frame(root, bg="white")
    frame.pack(expand=True)  # keeps the content in the center of the window

    # Title label
    label = tk.Label(frame, text="Select Your Modules", font=('default', 20), bg="white")
    label.grid(row=0, column=0, pady=(0, 15), columnspan=3)

    # Student information labels
    tk.Label(frame, text="Student : ", anchor='w', font=('default', 12), bg="white").grid(row=1, column=0, sticky='w', columnspan=2)
    tk.Label(frame, text="Year : ", anchor='w', font=('default', 12), bg="white").grid(row=2, column=0, sticky='w')
    tk.Label(frame, text="Semester : ", anchor='w', font=('default', 12), bg="white").grid(row=2, column=1, sticky='w')
    
    from tkinter import ttk
    # Horizontal separator line
    separator = ttk.Separator(frame, orient='horizontal')
    separator.grid(row=3, column=0, columnspan=3, sticky='ew', pady=(20, 10))

    # Subtitle label for the table
    label = tk.Label(frame, text="Modules you selected will appear in this table", font=('default', 10), bg="white", anchor='w')
    label.grid(row=4, column=0, columnspan=3, pady=(0,5), sticky='w')

    # Table setup
    table = ttk.Treeview(frame, columns=('Column1', 'Column2', 'Column3'), show='headings', height=1)
    table.heading('Column1', text='Module Code')
    table.heading('Column2', text='Module Name')
    table.heading('Column3', text='Module Credit')

    # Set the width of each column and center the data
    table.column('Column1', width=100, anchor='center')
    table.column('Column2', width=250, anchor='center')
    table.column('Column3', width=100, anchor='center')
    # Set the location in the frame the grid will be
    table.grid(row=5, column=0, columnspan=3, sticky='w')

    # Buttons
    deleteBtn = tk.Button(frame, text="Delete a Module", command=lambda: delete_selected_row(table))
    deleteBtn.grid(row=6, column=0, sticky='w', pady=(5,10))

    confirmModuleBtn = tk.Button(frame, text="Confirm Module Selection")
    confirmModuleBtn.grid(row=6, column=1, sticky='w', pady=(5,10))


    # Horizontal separator line
    separator = ttk.Separator(frame, orient='horizontal')
    separator.grid(row=7, column=0, columnspan=3, sticky='ew', pady=(10, 10))

    # Subtitle label for the table
    label = tk.Label(frame, text="Select a module from the drop down", font=('default', 10), bg="white", anchor='w')
    label.grid(row=8, column=0, columnspan=3, pady=(0,5), sticky='w')

    # Call the database to retrieve data for dropdowns from the database
    import Database.student_actions as stdAction
    module_codes, module_names, module_credits = stdAction.get_all_modules()

    # Entry fields for each column
    module_code_combobox = ttk.Combobox(frame, width=15,values=module_codes)
    module_code_combobox.grid(row=9, column=0, pady=5, sticky='w')
    module_code_combobox.bind("<<ComboboxSelected>>", lambda event: update_fields('code',module_codes, module_names, module_credits, module_name_combobox, module_credit_combobox,module_code_combobox))


    module_name_combobox = ttk.Combobox(frame, width=30, values=module_names)
    module_name_combobox.grid(row=9, column=1, pady=5, sticky='w')
    module_name_combobox.bind("<<ComboboxSelected>>", lambda event: update_fields('module_name',module_codes, module_names, module_credits, module_name_combobox, module_credit_combobox,module_code_combobox))

    module_credit_combobox = ttk.Combobox(frame, width=10, values=module_credits)
    module_credit_combobox.grid(row=9, column=2, pady=5, sticky='w')

    # Button to add row to the table
    add_button = tk.Button(frame, text="Add Module", command=lambda: add_row(table, module_code_combobox, module_name_combobox, module_credit_combobox))
    add_button.grid(row=10, column=0, pady=10, sticky='w')


