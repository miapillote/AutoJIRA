import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class LoginForm:
    def __init__(self, root, browser): #include browser session
        self.browser = browser
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
        
        self.root.mainloop()

    def on_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        #print("on_login -> attempt_login")
        self.attempt_login(username, password, self.browser)
            
    def attempt_login(self, username, password, driver):
        try:
            # Locate and fill in the username field
            username_field = driver.find_element(By.XPATH, "//*[@id='usernamevis']")
            password_field = driver.find_element(By.XPATH, "//*[@id='password']")
            login_button = driver.find_element(By.XPATH, "//*[@id='log-on']")

            # Fill the username and password fields
            username_field.send_keys(username)
            password_field.send_keys(password)

            # Click the login button
            login_button.click()
            self.root.destroy()
            #print("main loop destroyed")
            # Wait for a few seconds to allow the page to load
            time.sleep(3)
            #print("waited after main loop was destroyed")

        except Exception as e:
            # Handle any exceptions (e.g., element not found)
            return f"Error: {str(e)}"


# Create the main window
#root = tk.Tk()

# Create an instance of the LoginForm class
#login_form = LoginForm(root)

# Run the Tkinter event loop
#root.mainloop()
