from Database.database_connection import get_db_connection
#from database_connection import get_db_connection
import tkinter.messagebox as messagebox
import mysql.connector


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
    module_codes_str = ",".join(module_codes)  # Convert to comma-separated string

    # Establish database connection
    dbConn = get_db_connection()
    cursor = dbConn.cursor()

    try:
        # Call the stored procedure
        cursor.callproc('check_and_add_modules', 
                        (student_id, semester, academic_year, module_codes_str))

        # Commit the transaction if the procedure executes successfully
        dbConn.commit()
        messagebox.showinfo("Success", "Modules have been successfully enrolled.")
    except Exception as e:
        # Show a warning if the procedure raises an error
        messagebox.showwarning("Warning", str(e))
    finally:
        # Close the cursor and database connection
        cursor.close()
        dbConn.close()
        print("Database connection closed.")      


def find_latest_academic_year_with_all_grades(student_id):
    try:
        # Get database connection
        dbConn = get_db_connection()
        cursor = dbConn.cursor(dictionary=True)

        # Query to find the latest academic year where the student has enrolled and received grades
        query = """
            SELECT year
            FROM enroll
            WHERE stdID = %s
              AND grade IS NOT NULL
            GROUP BY year
            HAVING COUNT(DISTINCT semester) = 2
            ORDER BY year DESC
            LIMIT 1
        """
        
        cursor.execute(query, (student_id,))
        result = cursor.fetchone()

        if result:
            # Return the latest academic year found
            return result['year']
        else:
            # Show error message if no records are found
            messagebox.showerror("No Records Found", "The student has not received grades for both semesters in any academic year.")
            return None
    except mysql.connector.Error as err:
        # Handle any database errors
        messagebox.showerror("Database Error", f"Error occurred: {err}")
        return None
    finally:
        if dbConn.is_connected():
            cursor.close()
            dbConn.close()