import Ticket
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from Variables import URL, TEXT, XPATH
import logging

TESTING_MODE = False
logger = logging.getLogger(__name__)

class JiraFormAutomation:
    def __init__(self, ticket: Ticket, root, progress_bar, progress, browser):
        logging.basicConfig(filename='../resources/AutoJIRA.log', level=logging.INFO)
        self.NUM_UPDATES = 21
        self.ticket = ticket
        self.progress_int = 0
        self.progress = progress
        self.root = root
        self.progress_bar = progress_bar
        self.customer = ticket.name
        self.action = ticket.action
        self.items = ticket.item
        self.browser = browser
        if TESTING_MODE:
            self.update("Testing mode ON.")

    def update(self, message):
        logger.info(f"[{self.ticket.netid} {self.items}] {message}")

    def wait(self, element):
        self.update(element)
        return WebDriverWait(self.browser, 30).until(ec.element_to_be_clickable((By.XPATH, XPATH[element])))

    def open_landing_page(self):
        self.browser.get(URL['landing'])
        self.update_progress()

        # Wait for page load and check if login is required
        WebDriverWait(self.browser, 30).until(ec.url_contains("service.rochester.edu"))
        if "service.rochester.edu" not in self.browser.current_url:
            return "Could not reach landing page, try logging in."
            # Login.LoginForm(tk.Tk(), self.browser)
            # self.open_landing_page()
        self.update_progress()

    def fill_form(self):
        # Wait until the customer input is present
        customer_element = WebDriverWait(self.browser, 30).until(
            ec.presence_of_element_located((By.XPATH, XPATH['customer_element']))
        )
        self.update_progress()
        source_element = self.browser.find_elements(By.XPATH, XPATH['source_element'])
        summary_element = self.browser.find_elements(By.XPATH, XPATH['summary_element'])
        description_element = self.browser.find_elements(By.XPATH, XPATH['description_element'])

        customer_element.send_keys(self.customer[1], ", ", self.customer[0])
        time.sleep(2)
        customer_element.send_keys(Keys.RETURN)
        self.update_progress()

        self.wait('source_element')
        source_element[0].send_keys('Walk In')
        source_element[0].send_keys(Keys.RETURN)
        description_element[0].send_keys(TEXT['ticket_signature'])
        summary_element[0].send_keys(self.action, ": ", self.items)

        if TESTING_MODE:
            time.sleep(30)
            return

        summary_element[0].send_keys(Keys.RETURN)
        self.update_progress()

        # Wait for form submission and completion
        WebDriverWait(self.browser, 30).until(ec.invisibility_of_element_located((By.XPATH, XPATH['summary_element'])))

    def resolve_ticket(self):
        self.wait('resolve_element').click()
        self.wait('submit_element')
        self.browser.find_elements(By.XPATH, XPATH['submit_element'])[0].submit()
        self.update_progress()

    def assign_ticket(self):
        # TODO: add in error handling in case the menu is already toggled open
        self.wait('open_ticket_element')
        self.browser.find_elements(By.XPATH, XPATH['open_ticket_element'])[0].click()
        self.update_progress()

        # try to click the "assign to me" button
        try:
            self.wait('assign_to_me_element').click()
        except:
            self.wait('people_dropdown_element').click()
            self.wait('assign_to_me_element').click()

        self.update_progress()

    def close_ticket(self):
        WebDriverWait(self.browser, 30).until(ec.invisibility_of_element((By.CLASS_NAME, 'aui-blanket')))
        self.wait('transition_bar_element').click()
        self.update_progress()
        self.wait('close_button_element').click()
        self.wait('transition_bar_element')
        self.update_progress()

    def run(self):
        try:
            self.open_landing_page()
            self.fill_form()
            self.resolve_ticket()
            self.assign_ticket()
            self.close_ticket()
            self.update(f"Ticket submission success: {self.browser.current_url}")
            return "Successfully submitted ticket."
        except Exception as e:
            self.update(f"Ticket submission failed: {e}")
            self.update(self.browser.current_url)
            failure_message = "Ticket submission failure: " + self.browser.current_url
            return failure_message

    def update_progress(self):
        if self.root is not None:
            self.progress_int += 10
            self.progress.set(self.progress_int)
            self.progress_bar.update_idletasks()
            self.root.update_idletasks()
        else:
            self.progress_int += 10
            #TODO: command line progress bar here
