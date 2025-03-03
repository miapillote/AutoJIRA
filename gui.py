import tkinter as tk
from tkinter import messagebox
import JiraFormAutomation as jira

def submit_form():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    status = status_var.get()
    items = items_text.get("1.0", tk.END).strip()
    
    if not first_name or not last_name or not items:
        messagebox.showerror("Error", "All fields must be filled out.")
        return
    
    print(f"First Name: {first_name}")
    print(f"Last Name: {last_name}")
    print(f"Status: {status}")
    print(f"Items:\n{items}")
    
    ticket = jira.JiraFormAutomation([first_name, last_name],status,items)
    ticket.run()

    messagebox.showinfo("Success", "Form submitted successfully!")

# Create main window
root = tk.Tk()
root.title("Loan Tracker")
root.geometry("300x350")

# First Name
tk.Label(root, text="First Name:").pack()
first_name_entry = tk.Entry(root)
first_name_entry.pack()

# Last Name
tk.Label(root, text="Last Name:").pack()
last_name_entry = tk.Entry(root)
last_name_entry.pack()

# Status (Radio Buttons)
tk.Label(root, text="Status:").pack()
status_var = tk.StringVar(value="Loaned")
tk.Radiobutton(root, text="Loaned", variable=status_var, value="Loaned").pack()
tk.Radiobutton(root, text="Returned", variable=status_var, value="Returned").pack()

# Items List
tk.Label(root, text="Items:").pack()
items_text = tk.Text(root, height=5)
items_text.pack()

# Submit Button
tk.Button(root, text="Submit", command=submit_form).pack()

# Run application
root.mainloop()
