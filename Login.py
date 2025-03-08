import tkinter as tk
from tkinter import messagebox

class LoginForm:
    def __init__(self, root): #include browser session
        self.root = root
        self.root.title("Login Form")
        self.root.geometry("300x200")
        
        # Username Label and Entry
        self.label_username = tk.Label(root, text="Username")
        self.label_username.pack(pady=5)
        
        self.entry_username = tk.Entry(root)
        self.entry_username.pack(pady=5)
        
        # Password Label and Entry
        self.label_password = tk.Label(root, text="Password")
        self.label_password.pack(pady=5)
        
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.pack(pady=5)
        
        # Login Button
        self.login_button = tk.Button(root, text="Login", command=self.on_login)
        self.login_button.pack(pady=20)

    def on_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if self.attempt_login:
            messagebox.showinfo("Login Successful","Welcome!")
            self.root.destroy()
        else:
            messagebox.showerror("Login Failed","Please try again.")
            
    def attempt_login(self):
        return True


# Create the main window
root = tk.Tk()

# Create an instance of the LoginForm class
login_form = LoginForm(root)

# Run the Tkinter event loop
root.mainloop()
