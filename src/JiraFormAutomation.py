import Login
import Ticket
import sys
import tkinter as tk
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class JiraFormAutomation:
    def __init__(self, ticket: Ticket, root, progress_bar, progress):
        self.NUM_UPDATES = 11

        self.progress_int = 0
        self.progress = progress
        self.root = root
        self.progress_bar = progress_bar
        self.customer = ticket.name
        self.action = ticket.action
        self.items = ticket.item
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r'--user-data-dir=C:/Users/rettnerhelpdesk/AppData/Local/Google/Chrome')
        self.options.add_argument('--profile-directory=Profile 4')
        self.options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=self.options)

    def open_landing_page(self):
        landing = "https://service.rochester.edu/servicedesk/customer/portal/101/create/358?q=lending&q_time=1693601714516"
        self.browser.get(landing)
        self.update_progress()

        # Wait for page load and check if login is required
        WebDriverWait(self.browser, 30).until(EC.url_contains("service.rochester.edu"))
        if "service.rochester.edu" not in self.browser.current_url:
            return "Could not reach landing page, try logging in."
            # Login.LoginForm(tk.Tk(), self.browser)
            # self.open_landing_page()
        self.update_progress()

    def fill_form(self):
        # Wait until the customer input is present
        customer_element = WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="react-select-2-input"]'))
        )
        self.update_progress()
        source_element = self.browser.find_elements(By.XPATH,
                                                    '//*[@id="react-select-customfield_10808-instance-input"]')
        summary_element = self.browser.find_elements(By.XPATH, '//*[@id="summary"]')

        customer_element.send_keys(self.customer[1], ", ", self.customer[0])
        time.sleep(2)
        customer_element.send_keys(Keys.RETURN)
        self.update_progress()

        WebDriverWait(self.browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="react-select-customfield_10808-instance-input"]')))
        source_element[0].send_keys('Walk In')
        source_element[0].send_keys(Keys.RETURN)

        summary_element[0].send_keys(self.action, ": ", self.items)
        summary_element[0].send_keys(Keys.RETURN)
        #print("Form filled")
        self.update_progress()

        # Wait for form submission and completion
        WebDriverWait(self.browser, 30).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="summary"]')))

    def resolve_ticket(self):
        #print('Resolving')
        resolve = WebDriverWait(self.browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="com.atlassian.servicedesk:workflow-transition-761"]'))
        )
        resolve.click()
        WebDriverWait(self.browser, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/section/form')))
        self.browser.find_elements(By.XPATH, '/html/body/section/form')[0].submit()
        #print("Ticket resolved")
        self.update_progress()

    def assign_ticket(self):
        #print('Opening ticket information')
        time.sleep(2)
        self.browser.find_elements(By.XPATH, '//*[@id="content"]/div/header/div/div/div[2]/div[2]/div/ol/li[3]/a')[
            0].click()
        self.update_progress()
        # Wait until the assign-to-me button is clickable
        assign_button = WebDriverWait(self.browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="assign-to-me"]'))
        )
        assign_button.click()
        self.update_progress()
        #print('Assigned to me')

    def close_ticket(self):
        #print('Closing ticket')
        time.sleep(20)
        transition_bar = WebDriverWait(self.browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="opsbar-transitions_more"]/span')))
        transition_bar.click()
        self.update_progress()
        close_button = WebDriverWait(self.browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="action_id_941"]/a/div/div[1]'))
        )
        close_button.click()
        time.sleep(10)
        self.update_progress()
        #print('Ticket closed successfully.')

    def run(self):
        self.open_landing_page()
        self.fill_form()
        self.resolve_ticket()
        self.assign_ticket()
        self.close_ticket()
        self.browser.quit()
        return "Successfully submitted ticket."

    def update_progress(self):
        self.progress_int += 10
        self.progress.set(self.progress_int)
        self.progress_bar.update_idletasks()
        self.root.update_idletasks()
