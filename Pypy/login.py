import tkinter as tk
from tkinter import messagebox
import mysql.connector
from main import main as run_tree_manager_app

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="tree"
)

cursor = db.cursor()

# Function for user registration
def register():
    username = username_entry.get()
    password = password_entry.get()

    if username == '' or password == '':
        messagebox.showerror("Error", "Please fill all fields")
        return

    try:
        cursor.execute("INSERT INTO puno (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        messagebox.showinfo("Success", "Registration successful!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Registration failed: {err}")

# Function for user login
def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == '' or password == '':
        messagebox.showerror("Error", "Please fill all fields")
        return

    cursor.execute("SELECT * FROM puno WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    if user:
        messagebox.showinfo("Success", "Login successful!")
        # Call main function from main.py if login successful
        run_tree_manager_app()
    else:
        messagebox.showerror("Error", "Login failed. Invalid username or password.")

# Create main window
root = tk.Tk()
root.title("Login/Register")

# Set background color
root.configure(bg="#8fbc8f")

# Create labels and entries with updated style
tk.Label(root, text="Username:", bg="#8fbc8f").grid(row=0, column=0, sticky="e", padx=10, pady=10)
username_entry = tk.Entry(root, bg="white")
username_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Password:", bg="#8fbc8f").grid(row=1, column=0, sticky="e", padx=10, pady=10)
password_entry = tk.Entry(root, show="*", bg="white")
password_entry.grid(row=1, column=1, padx=10, pady=10)

# Create buttons with updated style
register_button = tk.Button(root, text="Register", command=register, bg="#0077cc", fg="white", padx=10, pady=5)
register_button.grid(row=2, column=0, pady=10)

login_button = tk.Button(root, text="Login", command=login, bg="#0077cc", fg="white", padx=10, pady=5)
login_button.grid(row=2, column=1, pady=10)

# Run the application
root.mainloop()