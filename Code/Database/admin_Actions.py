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



