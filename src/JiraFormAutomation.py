import Ticket 
import config
import local
import time 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as ec

TESTING_MODE = False

LANDING = config.global_config['url']['landing_page']
CHROME_PATH = local.local['chrome_path']
CHROME_PROFILE = local.local['chrome_profile']
SIGNATURE = config.global_config['text']['ticket_signature']
XPATH = config.global_config['xpath']


class JiraFormAutomation:
    def __init__(self, ticket: Ticket, root, progress_bar, progress):
        if TESTING_MODE:
            print("Testing mode ON.")
        self.NUM_UPDATES = 11

        self.progress_int = 0
        self.progress = progress
        self.root = root
        self.progress_bar = progress_bar
        self.customer = ticket.name
        self.action = ticket.action
        self.items = ticket.item
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(CHROME_PATH)
        self.options.add_argument(CHROME_PROFILE)
        if not TESTING_MODE:
            self.options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=self.options)

    def wait_until_clickable(self, xpath):
        return WebDriverWait(self.browser, 30).until(ec.element_to_be_clickable((By.XPATH, xpath)))

    def open_landing_page(self):
        self.browser.get(LANDING)
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

        self.wait_until_clickable(XPATH['source_element'])
        source_element[0].send_keys('Walk In')
        source_element[0].send_keys(Keys.RETURN)
        description_element[0].send_keys(SIGNATURE)
        summary_element[0].send_keys(self.action, ": ", self.items)
        
        if TESTING_MODE:
            time.sleep(30)
            return
        
        summary_element[0].send_keys(Keys.RETURN)
        
        print("Form filled")
        self.update_progress()

        # Wait for form submission and completion
        WebDriverWait(self.browser, 30).until(ec.invisibility_of_element_located((By.XPATH, XPATH['summary_element'])))

    def resolve_ticket(self):
        print('Resolving')
        self.wait_until_clickable(XPATH['resolve_menu_element']).click()
        self.wait_until_clickable(XPATH['resolve_menu_submit'])[0].submit()
        print("Ticket resolved")
        self.update_progress()

    def assign_ticket(self):
        print('Opening ticket information')
        self.wait_until_clickable(XPATH['open_ticket_information'])[0].click()
        self.update_progress()
        
        # try to click the "assign to me" button
        try:
            print("attempting to find \"assign to me\"")
            self.wait_until_clickable(XPATH['assign_to_me']).click()
        except:
            print("could not find \"assign to me\" button, expanding the \"people\" bar.")
            self.wait_until_clickable(XPATH['people_module']).click()
            print("\"People\" bar expanded")
            self.wait_until_clickable(XPATH['assign_to_me']).click()
        
        print("Clicked assign button")
        self.update_progress()
        print('Assigned to me')

    def close_ticket(self):
        print('Closing ticket')
        self.wait_until_clickable(XPATH['transition_bar']).click()
        self.update_progress()
        self.wait_until_clickable(XPATH['close_button']).click()
        self.wait_until_clickable(XPATH['transition_bar'])
        self.update_progress()
        print('Ticket closed successfully.')

    def run(self):
        try:
            self.open_landing_page()
            self.fill_form()
            self.resolve_ticket()
            self.assign_ticket()
            self.close_ticket()
            self.browser.quit()
            return "Successfully submitted ticket."
        except:
            print("ticket submission failed")
            print(self.browser.current_url)
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
            
