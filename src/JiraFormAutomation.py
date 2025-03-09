import Login
import sys
import tkinter as tk
import time
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class JiraFormAutomation:
    def __init__(self, customer, action, items):
        self.customer = customer
        self.action = action
        self.items = items
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r'--user-data-dir=C:/Users/rettnerhelpdesk/AppData/Local/Google/Chrome')
        self.options.add_argument('--profile-directory=Profile 4')
        self.browser = webdriver.Chrome(options=self.options)

    def open_landing_page(self):
        landing = "https://service.rochester.edu/servicedesk/customer/portal/101/create/358?q=lending&q_time=1693601714516"
        self.browser.get(landing)

        # Wait for page load and check if login is required
        WebDriverWait(self.browser, 15).until(EC.url_contains("service.rochester.edu"))
        if "service.rochester.edu" not in self.browser.current_url:
            Login.LoginForm(tk.Tk(), self.browser)
            self.open_landing_page()

    def fill_form(self):
        # Wait until the customer input is present
        customer_element = WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="react-select-2-input"]'))
        )
        source_element = self.browser.find_elements(By.XPATH,
                                                    '//*[@id="react-select-customfield_10808-instance-input"]')
        summary_element = self.browser.find_elements(By.XPATH, '//*[@id="summary"]')

        customer_element.send_keys(self.customer[1], ", ", self.customer[0])
        time.sleep(2)
        customer_element.send_keys(Keys.RETURN)

        WebDriverWait(self.browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="react-select-customfield_10808-instance-input"]')))
        source_element[0].send_keys('Walk In')
        source_element[0].send_keys(Keys.RETURN)

        summary_element[0].send_keys(self.action, ": ", self.items)
        summary_element[0].send_keys(Keys.RETURN)
        print("Form filled")

        # Wait for form submission and completion
        WebDriverWait(self.browser, 20).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="summary"]')))

    def resolve_ticket(self):
        print('Resolving')
        resolve = WebDriverWait(self.browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="com.atlassian.servicedesk:workflow-transition-761"]'))
        )
        resolve.click()
        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/section/form')))
        self.browser.find_elements(By.XPATH, '/html/body/section/form')[0].submit()
        print("Ticket resolved")

    def assign_ticket(self):
        print('Opening ticket information')
        time.sleep(2)
        self.browser.find_elements(By.XPATH, '//*[@id="content"]/div/header/div/div/div[2]/div[2]/div/ol/li[3]/a')[
            0].click()

        # Wait until the assign-to-me button is clickable
        assign_button = WebDriverWait(self.browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="assign-to-me"]'))
        )
        assign_button.click()
        print('Assigned to me')

    def close_ticket(self):
        print('Closing ticket')
        time.sleep(10)
        transition_bar = WebDriverWait(self.browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="opsbar-transitions_more"]/span')))
        transition_bar.click()
        close_button = WebDriverWait(self.browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="action_id_941"]/a/div/div[1]'))
        )
        close_button.click()
        time.sleep(10)
        print('Ticket closed successfully.')

    def run(self):
        self.open_landing_page()
        self.fill_form()
        self.resolve_ticket()
        self.assign_ticket()
        self.close_ticket()
        self.browser.quit()
        return True


if __name__ == "__main__":
    customer = [sys.argv[1], sys.argv[2]]
    action = sys.argv[3]
    items = sys.argv[4:]

    jira_automation = JiraFormAutomation(customer, action, items)
    jira_automation.run()
