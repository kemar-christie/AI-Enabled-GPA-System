# main.py
import tkinter as tk
import Login_Interface as lgInterface

def main():
    
    root = tk.Tk()
    root.geometry("600x600")
    root.title("Academic Probation Login")

    # Set the background color of the root window to white
    root.configure(bg="white")

    lgInterface.login_interface(root)

    root.mainloop()  # Start the Tkinter main loop

if __name__ == "__main__":
    main()
