import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class TreeManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Municipal Tree Preservation and Monitoring System")
        self.root.geometry("400x500")  # Adjusted size for better visibility

        # Configure grid
        self.root.grid_rowconfigure(6, weight=1)  # Make the listbox's row expandable
        self.root.grid_columnconfigure(1, weight=1)  # Make the listbox's column expandable

        # Connect to the database
        self.conn = sqlite3.connect('trees.db')
        self.create_table()

        # Create and pack widgets
        self.create_widgets()
        self.display_trees()

    def create_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS trees
                 (id INTEGER PRIMARY KEY, name TEXT NOT NULL, origin TEXT, height REAL, age INTEGER)''')

    def add_tree(self):
        name = self.name_entry.get()
        origin = self.origin_entry.get()
        height = float(self.height_entry.get())
        age = int(self.age_entry.get())
        self.conn.execute('''INSERT INTO trees (name, origin, height, age)
                            VALUES (?, ?, ?, ?)''', (name, origin, height, age))
        self.conn.commit()
        messagebox.showinfo("Success", "Tree added successfully!")
        self.clear_entries()
        self.display_trees()

    def delete_tree(self):
        selected_tree = self.tree_listbox.curselection()
        if selected_tree:
            tree_index = selected_tree[0]
            tree_id = self.conn.execute("SELECT id FROM trees").fetchall()[tree_index][0]
            self.conn.execute("DELETE FROM trees WHERE id = ?", (tree_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Tree deleted successfully!")
            self.display_trees()
        else:
            messagebox.showwarning("Warning", "No tree selected")

    def display_trees(self):
        self.tree_listbox.delete(0, tk.END)  # Clear previous items
        trees = self.conn.execute("SELECT * FROM trees").fetchall()
        for tree in trees:
            self.tree_listbox.insert(tk.END, f"Name: {tree[1]}, Origin: {tree[2]}, Height: {tree[3]}m, Age: {tree[4]} years")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.origin_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)

    def create_widgets(self):
        style = ttk.Style()
        style.configure('TButton', foreground='white', background='#2ecc71')

        # Labels
        name_label = ttk.Label(self.root, text="Name:")
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        origin_label = ttk.Label(self.root, text="Origin:")
        origin_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        height_label = ttk.Label(self.root, text="Height (m):")
        height_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        age_label = ttk.Label(self.root, text="Age (years):")
        age_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")

        # Entry fields
        self.name_entry = ttk.Entry(self.root)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.origin_entry = ttk.Entry(self.root)
        self.origin_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.height_entry = ttk.Entry(self.root)
        self.height_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.age_entry = ttk.Entry(self.root)
        self.age_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Add Tree button
        add_button = ttk.Button(self.root, text="Add Tree", command=self.add_tree, style='TButton')
        add_button.grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        # Delete Tree button
        delete_button = ttk.Button(self.root, text="Delete Tree", command=self.delete_tree, style='TButton')
        delete_button.grid(row=5, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        # View Trees listbox with scrollbar
        self.tree_listbox = tk.Listbox(self.root, height=15)  # Increased height for better visibility
        self.tree_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Add scrollbar to the listbox
        self.scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.tree_listbox.yview)
        self.scrollbar.grid(row=6, column=2, sticky='ns')
        self.tree_listbox.config(yscrollcommand=self.scrollbar.set)

        # Quit button
        quit_button = ttk.Button(self.root, text="Quit", command=self.root.quit, style='TButton')
        quit_button.grid(row=7, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

# Main function
def main():
    root = tk.Tk()
    app = TreeManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
