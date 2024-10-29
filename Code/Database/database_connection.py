import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        # Attempt to establish a connection to the MySQL database
        dbConn = mysql.connector.connect(host="localhost",user="root",password="",database="student_info")
        
        # Check if the connection was successful
        if dbConn.is_connected():
            print("Connection to the database was successful!")
            return dbConn
    except Error as e:
        # Print an error message if the connection failed
        print(f"Error connecting to the database: {e}")
        return None
    