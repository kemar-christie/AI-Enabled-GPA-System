from Database.database_connection import get_db_connection
#from database_connection import get_db_connection
import tkinter as tk
import tkinter.messagebox as messagebox
import mysql.connector

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


def getAllModules():
    """
    Retrieves all modules from the database and returns them as a list of tuples.
    Each tuple contains (moduleID, moduleName, num_of_credits).
    """
    dbConn = get_db_connection()
    try:
        cursor = dbConn.cursor()
        cursor.execute("SELECT moduleID, moduleName, num_of_credits FROM module")
        modules = cursor.fetchall()
        return modules
    except Exception as e:
        raise Exception(f"Error retrieving modules: {e}")
    finally:
        cursor.close()
        dbConn.close()


def get_student_grades_for_semester(student_id, year, semester):
    # Use the existing connection method
    dbConn = get_db_connection()
    
    try:
        cursor = dbConn.cursor()

        # Call the stored procedure
        cursor.callproc('get_student_grades_for_semester', (student_id, year, semester))

        # Fetch the result
        grades = None
        for result in cursor.stored_results():
            grades = result.fetchall()

        if grades:
            return grades
        else:
            messagebox.showinfo("No Grades Found", "No grades found for this student in the specified year and semester.")
            return None

    except Exception as e:
        if "Student not found" in str(e):
            messagebox.showinfo("Student Not Found", "The specified student does not exist.")
        else:
            messagebox.showerror("Database Error", f"Error fetching grades: {e}")
        return None

    finally:
        cursor.close()
        dbConn.close()



def update_student_grade(studentID, moduleID, semester, year, grade):
    """Update the grade for a student's module enrollment."""
    
    try:
        # Use the existing connection method
        dbConn = get_db_connection()
        cursor = dbConn.cursor()

        # SQL query to update the grade in the enroll table
        update_query = """
            UPDATE enroll
            SET grade = %s
            WHERE stdID = %s AND moduleID = %s AND semester = %s AND year = %s
        """

        # Execute the query with the provided values
        cursor.execute(update_query, (grade, studentID, moduleID, semester, year))

        # Commit the changes
        dbConn.commit()

        # Check if any rows were affected (i.e., the update was successful)
        if cursor.rowcount > 0:
            messagebox.showinfo("Success", "Grade Updated Successfully")
            return True
        else:
            messagebox.showwarning("No Record Found", "No matching record found for the update.")
            return False
        
    except Exception as err:
        # Handle any database connection or query errors
        messagebox.showerror("Error", f"Error: {err}")

    finally:
        # Close the cursor and connection
        cursor.close()
        dbConn.close()




def get_student_grades_and_credits(student_id, academic_year):
    # Establish database connection
    dbConn = get_db_connection()
    cursor = dbConn.cursor()
    
    try:
        # Call the stored procedure
        cursor.callproc('GetStudentGradesAndCredits', (student_id, academic_year))

        # Fetch the results from the stored procedure
        results = []
        for result in cursor.stored_results():
            results = result.fetchall()

        # Initialize lists for the two semesters
        sem1_credits = []
        sem1_grades = []
        sem2_credits = []
        sem2_grades = []

        # Loop through the results and segregate them by semester
        for row in results:
            semester, grade, credits = row
            # Ensure that the grade is an integer
            try:
                grade = int(grade)
            except ValueError:
                grade = None  # If the grade is invalid, set it to None or handle as necessary

            if semester == 1:
                sem1_credits.append(credits)
                sem1_grades.append(grade)
            elif semester == 2:
                sem2_credits.append(credits)
                sem2_grades.append(grade)

        # Return the data in the desired format
        return [sem1_credits, sem1_grades, sem2_credits, sem2_grades]

    except mysql.connector.Error as err:
        # Handle SQL errors (e.g., custom SIGNAL errors)
        if err.sqlstate == '45000':
            messagebox.showerror("Error", err.msg)
        else:
            messagebox.showerror("Database Error", f"An error occurred: {err}")
        return None

    except Exception as e:
        # Handle other exceptions
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        return None

    finally:
        # Close the cursor and database connection
        cursor.close()
        dbConn.close()
        print("Database connection closed.")
