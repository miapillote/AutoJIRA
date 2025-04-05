import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import JiraFormAutomation as Jira
from tkcalendar import Calendar
from datetime import datetime
import os
import Ticket
import CalendarTool


# TODO: create a separate thread for the automations so they don't lock up the ui
# This would let the user queue multiple operations at once

def submit_form():
    # Set up progress bar
    progress.set(0)
    progress_bar.grid(row=4, column=1, padx=20, pady=1, sticky="w")

    # Initialize ticket
    ticket = Ticket.Ticket()
    file_path = file_path_var.get()  # Get the selected file path

    # If a file is selected, no other inputs are needed
    if file_path:
        ticket.read_form(file_path, status_var.get())
    """
    else:
        first_name = first_name_entry.get().strip()
        last_name = last_name_entry.get().strip()
        status = status_var.get()
        items = items_text.get("1.0", tk.END).strip()
        selected_date_str = date_picker.get_date()  # Get the selected date as a string

        # Validate other fields when no file is selected
        if not first_name or not last_name or not items:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        # Convert the selected date string to a datetime object
        try:
            selected_date = datetime.strptime(selected_date_str,
                                              "%m/%d/%y")  # Adjust the format as per the date pattern
        except ValueError:
            messagebox.showerror("Error", "Invalid date format.")
            return
        ticket.manual_input([first_name, last_name], items, selected_date, status)
    """

    # TODO: give error message when the automation fails
    clear_fields()
    # TODO: change calendar oauth to Rettner account
    if calendar_checkbox_var.get():
        CalendarTool.create_event(ticket)
        messagebox.showinfo("Successfully created Google Calendar event.")
    if jira_ticket_checkbox_var.get():
        automation = Jira.JiraFormAutomation(ticket, root, progress_bar, progress)
        messagebox.showinfo(automation.run())
    if not (calendar_checkbox_var.get() or jira_ticket_checkbox_var.get()):
        messagebox.showwarning("Select at least one action to continue.")
    return


def clear_fields():
    """
    # Clear Entry fields
    first_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    """

    # Clear Status Radio Buttons
    status_var.set("Loaned")  # or set it to the default value

    """
    # Clear Items Text field
    items_text.delete("1.0", tk.END)

    # Clear Date Picker (default to today)
    date_picker.selection_set(datetime.today())  # Set to today's date
    """

    # Clear File Path
    file_path_var.set("")
    file_label.config(text="No file selected")  # Reset the label text


def browse_file():
    file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("All Files", "*.*")])
    if file_path:
        file_path_var.set(file_path)
        file_label.config(text=os.path.basename(file_path))  # Update label with file name

# Create main window
root = tk.Tk()
root.title("AutoJIRA")
root.geometry("800x500")  # Increase the initial window size

# Create a frame for left-side elements (form fields)
left_frame = tk.Frame(root)
left_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

# File Picker (optional) - Moved to the top
tk.Label(left_frame, text="Select a File (optional):").grid(row=0, column=0, padx=20, pady=5, sticky="w")
file_path_var = tk.StringVar()

# Browse Button
file_picker_button = tk.Button(left_frame, text="Browse", command=browse_file)
file_picker_button.grid(row=1, column=0, padx=20, pady=5, sticky="w")

# Label to display the selected file name
file_label = tk.Label(left_frame, text="No file selected")  # Default text when no file is chosen
file_label.grid(row=2, column=0, padx=20, pady=5, sticky="w")

"""
# First Name and Last Name (stacked on top of each other)
tk.Label(left_frame, text="First Name:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
first_name_entry = tk.Entry(left_frame, width=20)
first_name_entry.grid(row=4, column=0, padx=5, pady=5, sticky="w")

tk.Label(left_frame, text="Last Name:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
last_name_entry = tk.Entry(left_frame, width=20)
last_name_entry.grid(row=6, column=0, padx=5, pady=5, sticky="w")
"""

# Status (Radio Buttons)
tk.Label(left_frame, text="Status:").grid(row=7, column=0, padx=20, pady=5, sticky="w")
status_var = tk.StringVar(value="Loaned")
tk.Radiobutton(left_frame, text="Loaned", variable=status_var, value="Loaned").grid(row=8, column=0, padx=20, pady=5,
                                                                                    sticky="w")
tk.Radiobutton(left_frame, text="Returned", variable=status_var, value="Returned").grid(row=9, column=0, padx=20,
                                              
                                              pady=5, sticky="w")
                                              
"""
# Items List
tk.Label(left_frame, text="Items:").grid(row=10, column=0, padx=20, pady=5, sticky="w")
items_text = tk.Text(left_frame, height=5, width=40)  # Adjust width to make it less wide
items_text.grid(row=11, column=0, padx=20, pady=5, sticky="w")
"""

# Submit Button
tk.Button(root, text="Submit", command=submit_form).grid(row=12, column=0, padx=20, pady=10, sticky="w")

# Jira Ticket Checkbox
jira_ticket_checkbox_var = tk.BooleanVar()
jira_ticket_checkbox_var.set(True)
jira_ticket_checkbox = tk.Checkbutton(root, text="Create JIRA Ticket", variable=jira_ticket_checkbox_var)
jira_ticket_checkbox.grid(row=12, column=0, padx=20, pady=10)


# Calendar Event Checkbox
calendar_checkbox_var = tk.BooleanVar()
calendar_checkbox_var.set(False)
calendar_checkbox = tk.Checkbutton(root, text="Create Calendar Event", variable=calendar_checkbox_var)
calendar_checkbox.grid(row=12, column=0, padx=20, pady=10, sticky="e")


# Progress Bar
progress = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress, maximum=100, length=200)

# Create a frame for the calendar (right side)
right_frame = tk.Frame(root)
right_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

"""
# Date Picker (defaults to today's date) - Moved to the right
tk.Label(right_frame, text="Select Date:").grid(row=0, column=0, padx=20, pady=5, sticky="w")
date_picker = Calendar(right_frame, date_pattern="mm/dd/yy")  # Adjust the format if needed
date_picker.grid(row=1, column=0, padx=20, pady=5, sticky="w")

# Set default date to today
date_picker.selection_set(datetime.today())
"""

# Adjust column and row weights for resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Run application
root.mainloop()
