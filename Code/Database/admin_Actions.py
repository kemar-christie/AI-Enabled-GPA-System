from Database.database_connection import get_db_connection
import tkinter as tk
import tkinter.messagebox as messagebox

def add_student_and_alert(fullname, email, password, school, programme, advisor_name, advisor_email, prog_dir_name, prog_dir_email, fac_admin_name, fac_admin_email):
    # Get the database connection
    dbConn = get_db_connection()
    try:
        cursor = dbConn.cursor()

        # Call the stored procedure InsertStudentAndAlert
        sqlcode = """
            CALL InsertStudentAndAlert(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        # Execute the procedure with provided arguments
        cursor.execute(sqlcode, (fullname, email, password, school, programme, advisor_name, advisor_email, prog_dir_name, prog_dir_email, fac_admin_name, fac_admin_email))

        # Commit the transaction to ensure the insertion is complete
        dbConn.commit()

        # Retrieve only the stdID of the last inserted student
        cursor.execute("SELECT stdID FROM student ORDER BY stdID DESC LIMIT 1")
        result = cursor.fetchone()

        # Check if a record was found
        if result:
            stdID = result[0]

            # Prepare the confirmation message
            info_message = (
                "Student info added successfully:\n\n"
                "• Student name: " + fullname + "\n"
                "• Student ID: " + str(stdID) + "\n"
                "• Email: " + email + "\n"
                "• School: " + school + "\n"
                "• Programme: " + programme + "\n"
                "• Advisor name: " + advisor_name + "\n"
                "• Advisor email: " + advisor_email + "\n"
                "• Programme Director name: " + prog_dir_name + "\n"
                "• Programme Director email: " + prog_dir_email + "\n"
                "• Faculty Admin name: " + fac_admin_name + "\n"
                "• Faculty Admin email: " + fac_admin_email
            )

            # Create a new window to display the information with a larger font
            display_info_in_large_font(info_message)
        else:
            messagebox.showerror("Database Error", "No student record found after insertion.")

    except Exception as e:
        messagebox.showerror("Database Error", f"Error adding Student: {e}")
        dbConn.rollback()  # Roll back if there's an error
        return False

    finally:
        cursor.close()
        dbConn.close()
        print("Database connection closed.")
        return True

def display_info_in_large_font(info_message):
    # Create a new window for displaying the info message
    info_window = tk.Toplevel()
    info_window.title("Student Record Status")
    
    # Create a Label widget with a larger font
    label = tk.Label(info_window, text=info_message, font=("Arial", 12), justify="left")
    label.pack(padx=20, pady=20)
    
    # Button to close the window
    close_button = tk.Button(info_window, text="Close", command=info_window.destroy, padx=20, bg="#007bff", fg="white")
    close_button.pack(pady=(0, 20))

    # Make sure the window is above the main window
    info_window.transient()
    info_window.grab_set()


def get_admin_name(adminID):
    # Connect to the database
    dbConn = get_db_connection()
    try:
        cursor = dbConn.cursor()

        # SQL query to fetch the admin_fullname based on adminID
        query = "SELECT admin_fullname FROM admin WHERE adminID = %s"
        cursor.execute(query, (adminID,))

        # Fetch the result
        result = cursor.fetchone()

        # Check if the result exists and return the admin name
        if result:
            return result[0]  # Extract the admin name from the result
        else:
            messagebox.showinfo("Info", "Admin ID not found.")
            return None

    except Exception as e:
        messagebox.showerror("Database Error", f"Error fetching admin name: {e}")
        return None

    finally:
        # Close the database connection
        cursor.close()
        dbConn.close()



def add_modules_to_database(table):
    # Connect to the database
    dbConn = get_db_connection()
    try:
        cursor = dbConn.cursor()

        # Check if all modules are unique in the database
        duplicate_modules = []
        for item in table.get_children():
            module_code = table.item(item, 'values')[0]
            
            # Check if the module code already exists in the database
            cursor.execute("SELECT moduleID FROM module WHERE moduleID = %s", (module_code,))
            if cursor.fetchone() is not None:
                duplicate_modules.append(module_code)

        # If duplicates are found, alert the user and stop the process
        if duplicate_modules:
            messagebox.showwarning("Duplicate Modules", f"The following modules already exist in the database: {', '.join(duplicate_modules)}")
            return

        # Insert all unique modules into the database
        for item in table.get_children():
            values = table.item(item, 'values')
            module_code = values[0]
            module_name = values[1]
            num_of_credits = int(values[2])

            query = """
                INSERT INTO module (moduleID, moduleName, num_of_credits) 
                VALUES (%s, %s, %s);
            """
            cursor.execute(query, (module_code, module_name, num_of_credits))

        # Commit the transaction to ensure all records are added
        dbConn.commit()
        messagebox.showinfo("Success", "All modules have been successfully added to the database.")

    except Exception as e:
        # Roll back in case of any error
        dbConn.rollback()
        messagebox.showerror("Database Error", f"Error adding modules to database: {e}")

    finally:
        cursor.close()
        dbConn.close()

