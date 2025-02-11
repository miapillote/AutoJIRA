from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys

customer, action, items = [sys.argv[1], sys.argv[2]], sys.argv[3], ", ".join(sys.argv[4:]) #stringify the items
print("Customer: ", customer)
print("Action: ", action)
print("Items: ", items)

#Rettner acct is 2, auto acct is 4
options = webdriver.ChromeOptions()
#options.add_argument(r'--user-data-dir=C:\\Users\\rettnerhelpdesk\\AppData\\Local\\Google\\Chrome') #Rettner Chrome path
options.add_argument(r'--user-data-dir=C:\\Users\\miapi\\AppData\\Local\\Google\\Chrome') #Test env Chrome path
options.add_argument('--profile-directory=Profile 4')
browser = webdriver.Chrome(options=options)
browser.implicitly_wait(15)

#jira ticket landing page
landing = "https://service.rochester.edu/servicedesk/customer/portal/101/create/358?q=lending&q_time=1693601714516"
browser.get(landing)
time.sleep(5)

#attempt filling form
customerElement = browser.find_elements(By.XPATH, '//*[@id="react-select-2-input"]')
sourceElement = browser.find_elements(By.XPATH, '//*[@id="react-select-customfield_10808-instance-input"]')
summaryElement = browser.find_elements(By.XPATH, '//*[@id="summary"]')

customerElement[0].send_keys(customer[0], ", ", customer[1])
time.sleep(2)
customerElement[0].send_keys(Keys.RETURN)
sourceElement[0].send_keys('Walk In')
sourceElement[0].send_keys(Keys.RETURN)
summaryElement[0].send_keys(action, ": ", items)

#add in checking here if the search turns up no results; 
#make the pane visible and allow the person to do it themselves
#then make them press Enter before it submits the form

summaryElement[0].send_keys(Keys.RETURN)
print("Form filled")
time.sleep(15)

print('Resolving')
resolve = browser.find_elements(By.XPATH, '//*[@id="com.atlassian.servicedesk:workflow-transition-761"]')
resolve[0].click()
time.sleep(2)
browser.find_elements(By.XPATH, '/html/body/section/form')[0].submit()
time.sleep(15)

print('Opening ticket information')
browser.find_elements(By.XPATH, '//*[@id="content"]/div/header/div/div/div[2]/div[2]/div/ol/li[3]/a')[0].click()
time.sleep(10)

print('Assigning to you')
browser.find_elements(By.XPATH, '//*[@id="assign-to-me"]')[0].click()
time.sleep(10)

#fails here, I think //*[@id="action_id_941"]/a/div

print('Closing') 
browser.find_elements(By.XPATH, '//*[@id="opsbar-transitions_more"]/span')[0].click()
time.sleep(10)
browser.find_elements(By.XPATH, '//*[@id="action_id_941"]/a/div/div[1]')[0].click()
time.sleep(10)
print('Ticket submitted successfully.')

