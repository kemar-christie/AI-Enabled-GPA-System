from Database.database_connection import get_db_connection
import tkinter.messagebox as messagebox

def verify_admin_credentials(adminID, password):
    # Get the database connection
    dbConn = get_db_connection()
    try:
        cursor = dbConn.cursor()
        # SQL query to check if an admin exists with the provided adminID and password
        # using %s or other placeholders prevent sql injections
        sqlcode = """
            SELECT 1 FROM admin
            WHERE adminID = %s AND password = %s
            LIMIT 1;
        """
        cursor.execute(sqlcode, (adminID, password))
        # Fetch the result; if there's a match, it will return a row
        result = cursor.fetchone()
        return result is not None  # Returns True if a row is found, False otherwise
    except Exception as e:
        messagebox.showerror("Database Error", f"Error adding Student: {e}")
        return False
    finally:
        cursor.close()
        dbConn.close()



def verify_student_credentials(stdID, password):
    # Get the database connection
    dbConn = get_db_connection()
    try:
        cursor = dbConn.cursor()
        # SQL query to check if a student exists with the provided stdID and password
        sqlcode = """
            SELECT 1 FROM student
            WHERE stdID = %s AND password = %s
            LIMIT 1;
        """
        cursor.execute(sqlcode, (stdID, password))
        # Fetch the result; if there's a match, it will return a row
        result = cursor.fetchone()
        return result is not None  # Returns True if a row is found, False otherwise
    except Exception as e:
        messagebox.showerror("Database Error", f"Error adding Student: {e}")
        return False
    finally:
        cursor.close()
        dbConn.close()
