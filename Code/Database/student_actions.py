from Database.database_connection import get_db_connection
import tkinter.messagebox as messagebox

def get_all_modules():
    # Create a database connection
    dbConn = get_db_connection()
    try:
        cursor = dbConn.cursor()
        
        # Query to fetch module codes, names, and credits
        sql_query = "SELECT moduleID, moduleName, num_of_credits FROM module;"
        cursor.execute(sql_query)
        
        # Fetch all results
        modules = cursor.fetchall()
        
        # Separate the data into lists for the comboboxes
        module_codes = [module[0] for module in modules]  # moduleID
        module_names = [module[1] for module in modules]  # moduleName
        module_credits = [str(module[2]) for module in modules]  # num_of_credits as strings

        return module_codes, module_names, module_credits
        
    except Exception as e:
        messagebox.showerror("Database Error", f"Error adding Student: {e}")
        return [], [], []  # Return empty lists in case of error
    finally:
        cursor.close()
        dbConn.close()
        print("Database connection closed.")



def get_student_name(studentID):
    # Create a database connection
    dbConn = get_db_connection()
    try:
        cursor = dbConn.cursor()
        
        # SQL query to fetch the student's full name based on the student ID
        sql_query = "SELECT full_name FROM student WHERE stdID = %s;"
        cursor.execute(sql_query, (studentID,))
        
        # Fetch the result
        result = cursor.fetchone()
        
        # Check if a result was found
        if result:
            return result[0]  # Return the full_name if found
        else:
            messagebox.showinfo("Not Found", "Student ID not found.")
            return 'N/A'
        
    except Exception as e:
        messagebox.showerror("Database Error", f"Error retrieving student name: {e}")
        return None
    finally:
        cursor.close()
        dbConn.close()
        print("Database connection closed.")



def add_modules_to_enroll(academic_year, semester, student_id, table):
    # Retrieve all module codes from the table
    module_codes = [table.item(item, 'values')[0] for item in table.get_children()]
    
    # Establish database connection
    dbConn = get_db_connection()
    cursor = dbConn.cursor()

    try:
        # Fetch all existing modules the student is already enrolled in for the specified academic year and semester
        cursor.execute("""
            SELECT moduleID
            FROM enroll
            WHERE stdID = %s AND year = %s AND semester = %s
        """, (student_id, academic_year, semester))
        
        # Get the list of already enrolled module IDs
        existing_modules = set(row[0] for row in cursor.fetchall())

        # Check if any of the new modules are already enrolled
        duplicate_modules = [code for code in module_codes if code in existing_modules]
        
        #this ensures the student is not able to enroll for the same module in the same academic year and semester
        if duplicate_modules:
            # If there are duplicates, notify the user and exit without making any changes
            messagebox.showerror("Duplicate Modules", 
                f"The following module/modules are already enrolled for the specified semester and year:\n{', '.join(duplicate_modules)}")
            return  # Exit the function if duplicates are found

        # Proceed to add each module to the enroll table if no duplicates
        for module_code in module_codes:
            cursor.execute("""
                INSERT INTO enroll (stdID, moduleID, year, semester)
                VALUES (%s, %s, %s, %s)
            """, (student_id, module_code, academic_year, semester))
        
        # Commit the transaction to save changes
        dbConn.commit()
        messagebox.showinfo("Success", "Modules have been successfully enrolled.")
    except Exception as e:
        # Rollback in case of an error
        dbConn.rollback()
        messagebox.showerror("Error", f"Failed to enroll modules: {e}")

    finally:
        # Close the cursor and database connection
        cursor.close()
        dbConn.close()
        print("Database connection closed.")

        