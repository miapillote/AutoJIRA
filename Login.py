import getpass
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


"""
Flow:

0. Trigger
1. Follow link
2. checkLoginStatus(browser): (using expected conditions)
	case 1: landing page reached -> 3
	case 2: login page reached -> Login(browser); checkLoginStatus(browser)
	case 3: stale request -> Refresh(); checkLoginStatus(browser)
3. SubmitTicket: New ticket object.
	- Customer:
		- Name
		- Email
		- NetID
	- action {Loaned, Returned}
	- item(s)
		- Make a dictionary of loaner items, eventually
		- dropdown menu
4. Add to database
5. Create calendar event

"""

landingURL = "https://service.rochester.edu/servicedesk/customer/portal/101/create/358?q=lending&q_time=1693601714516"
elements = {
	'loginUsername': '//*[@id="usernamevis"]',
	'loginPassword': '//*[@id="password"]',
	'loginSubmit': '//*[@id="log-on"]'
}

def getCreds():
	print("Username: ")
	username = input()
	print("Password: ")
	password = getpass.getpass("Entering password: ")
	return username, password

def jiraLogin(browser, username, password):
	print("Checking session...")
	browser.get(landingURL)
	browser.find_elements(By.XPATH, elements['loginUsername'])[0].send_keys(username)
	browser.find_elements(By.XPATH, elements['loginPassword'])[0].send_keys(password)
	time.sleep(0.5)
	browser.find_elements(By.XPATH, elements['loginSubmit'])[0].click()
	return None

def staleLogin(browser):
	return None
