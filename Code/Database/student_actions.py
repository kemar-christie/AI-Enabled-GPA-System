#from Database.database_connection import get_db_connection
from database_connection import get_db_connection
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



def get_student_grades_and_credits(student_id, academic_year):
    # Establish database connection
    dbConn = get_db_connection()
    cursor = dbConn.cursor()

    try:
        # SQL query to get grades and credits for each module for the specified academic year
        cursor.execute("""
            SELECT 
                e.semester,
                e.grade,
                m.num_of_credits
            FROM 
                enroll e
            JOIN 
                module m ON e.moduleID = m.moduleID
            WHERE 
                e.stdID = %s
                AND e.year = %s
            ORDER BY 
                e.semester, e.moduleID
        """, (student_id, academic_year))

        # Fetch the results
        results = cursor.fetchall()

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

    except Exception as e:
        print(f"Error fetching grades with credits: {e}")
        return None

    finally:
        # Close the cursor and database connection
        cursor.close()
        dbConn.close()
        print("Database connection closed.")


results=get_student_grades_and_credits(2400000,'2024/2025')
print(results)