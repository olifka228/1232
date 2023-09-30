import tkinter as tk
from tkinter import ttk
import sqlite3

conn = sqlite3.connect('employees.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS employees
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                number TEXT,
                email TEXT)''')

conn.commit()

def add_employee():
    name = name_entry.get()
    number = number_entry.get()
    email = email_entry.get()

    if name != "" and number != "" and email != "":
        data = (name, number, email)
        query = "INSERT INTO employees (name, number, email) VALUES (?, ?, ?)"
        cursor.execute(query, data)
        conn.commit()
        show_employees()
        clear_entries()

def update_employee():
    id = id_entry.get()
    name = name_entry.get()
    number = number_entry.get()
    email = email_entry.get()

    if id != "" and name != "" and number != "" and email != "":
        data = (name, number, email, id)
        query = "UPDATE employees SET name=?, number=?, email=? WHERE id=?"
        cursor.execute(query, data)
        conn.commit()
        show_employees()
        clear_entries()

def delete_employee():
    id = id_entry.get()

    if id != "":
        query = "DELETE FROM employees WHERE id=?"
        cursor.execute(query, (id,))
        conn.commit()
        show_employees()
        clear_entries()

def search_employee():
    name = name_entry.get()

    if name != "":
        query = "SELECT * FROM employees WHERE name=?"
        cursor.execute(query, (name,))
        result = cursor.fetchone()

        if result:
            id_entry.delete(0, tk.END)
            id_entry.insert(tk.END, result[0])
            number_entry.delete(0, tk.END)
            number_entry.insert(tk.END, result[2])
            email_entry.delete(0, tk.END)
            email_entry.insert(tk.END, result[3])
        else:
            clear_entries()

def show_employees():
    for row in treeview.get_children():
        treeview.delete(row)

    query = "SELECT * FROM employees"
    cursor.execute(query)
    results = cursor.fetchall()

    for result in results:
        treeview.insert("", tk.END, values=result)

def clear_entries():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    number_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Employee Database")

id_label = ttk.Label(root, text="ID:")
id_label.grid(row=0, column=0)
id_entry = ttk.Entry(root)
id_entry.grid(row=0, column=1)

name_label = ttk.Label(root, text="Name:")
name_label.grid(row=1, column=0)
name_entry = ttk.Entry(root)
name_entry.grid(row=1, column=1)

number_label = ttk.Label(root, text="Number:")
number_label.grid(row=2, column=0)
number_entry = ttk.Entry(root)
number_entry.grid(row=2, column=1)

email_label = ttk.Label(root, text="Email:")
email_label.grid(row=3, column=0)
email_entry = ttk.Entry(root)
email_entry.grid(row=3, column=1)

add_button = ttk.Button(root, text="Add", command=add_employee)
add_button.grid(row=4, column=0)

update_button = ttk.Button(root, text="Update", command=update_employee)
update_button.grid(row=4, column=1)

delete_button = ttk.Button(root, text="Delete", command=delete_employee)
delete_button.grid(row=4, column=2)

search_button = ttk.Button(root, text="Search", command=search_employee)
search_button.grid(row=4, column=3)

treeview = ttk.Treeview(root, columns=("ID", "Name", "Number", "Email"), show="headings")
treeview.heading("ID", text="ID")
treeview.heading("Name", text="Name")
treeview.heading("Number", text="Number")
treeview.heading("Email", text="Email")
treeview.grid(row=5, columnspan=4)
show_employees()

root.mainloop()

conn.close()