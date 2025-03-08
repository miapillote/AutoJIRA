import Login
import time
import sys
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class JiraFormAutomation:
    def __init__(self, customer, action, items):
        self.customer = customer
        self.action = action
        self.items = items
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r'--user-data-dir=C:/Users/rettnerhelpdesk/AppData/Local/Google/Chrome')
        self.options.add_argument('--profile-directory=Profile 4')
        self.browser = webdriver.Chrome(options=self.options)
        self.browser.implicitly_wait(15)
        
    def open_landing_page(self):
        landing = "https://service.rochester.edu/servicedesk/customer/portal/101/create/358?q=lending&q_time=1693601714516"
        self.browser.get(landing)
        time.sleep(5)
        if "service.rochester.edu" not in self.browser.current_url:
            Login.LoginForm(tk.Tk(), self.browser)
            self.open_landing_page()
    
    def fill_form(self):
        customer_element = self.browser.find_elements(By.XPATH, '//*[@id="react-select-2-input"]')
        source_element = self.browser.find_elements(By.XPATH, '//*[@id="react-select-customfield_10808-instance-input"]')
        summary_element = self.browser.find_elements(By.XPATH, '//*[@id="summary"]')
        
        customer_element[0].send_keys(self.customer[1], ", ", self.customer[0])
        time.sleep(5)
        customer_element[0].send_keys(Keys.RETURN)
        source_element[0].send_keys('Walk In')
        source_element[0].send_keys(Keys.RETURN)
        summary_element[0].send_keys(self.action, ": ", self.items)
        summary_element[0].send_keys(Keys.RETURN)
        print("Form filled")
        time.sleep(15)
    
    def resolve_ticket(self):
        print('Resolving')
        resolve = self.browser.find_elements(By.XPATH, '//*[@id="com.atlassian.servicedesk:workflow-transition-761"]')
        resolve[0].click()
        time.sleep(2)
        self.browser.find_elements(By.XPATH, '/html/body/section/form')[0].submit()
        time.sleep(15)
    
    def assign_ticket(self):
        print('Opening ticket information')
        self.browser.find_elements(By.XPATH, '//*[@id="content"]/div/header/div/div/div[2]/div[2]/div/ol/li[3]/a')[0].click()
        time.sleep(10)
        print('Assigning to you')
        self.browser.find_elements(By.XPATH, '//*[@id="assign-to-me"]')[0].click()
        time.sleep(10)
    
    def close_ticket(self):
        print('Closing')
        self.browser.find_elements(By.XPATH, '//*[@id="opsbar-transitions_more"]/span')[0].click()
        time.sleep(10)
        self.browser.find_elements(By.XPATH, '//*[@id="action_id_941"]/a/div/div[1]')[0].click()
        time.sleep(10)
        print('Ticket submitted successfully.')
    
    def run(self):
        self.open_landing_page()
        self.fill_form()
        self.resolve_ticket()
        self.assign_ticket()
        self.close_ticket()
        self.browser.quit()

if __name__ == "__main__":
    customer = [sys.argv[1], sys.argv[2]]
    action = sys.argv[3]
    items = sys.argv[4:]
    
    jira_automation = JiraFormAutomation(customer, action, items)
    jira_automation.run()
