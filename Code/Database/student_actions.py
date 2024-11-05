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