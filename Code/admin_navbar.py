import tkinter as tk

def admin_navbar(root):
    # Create a frame for the admin navbar
    frame = tk.Frame(root, bg="white")
    frame.pack(expand=True)  # keeps the content in the center of the window

    label = tk.Label(frame, text="Admin Nav bar", font=('default', 20), bg="white")
    label.grid(row=0, column=0, pady=(0, 30), columnspan=3)

    return frame
