from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


#open auto acct
options = webdriver.ChromeOptions()
options.add_argument(r'--user-data-dir=C:\\Users\\miapi\\AppData\\Local\\Google\\Chrome')
options.add_argument('--profile-directory=Profile 4')
browser = webdriver.Chrome(options=options)

#navigate to ticket page
browser.get('https://service.rochester.edu/servicedesk/customer/portal/101/create/358?q=lending&q_time=1693601714516')
print('Landing page accessed')
time.sleep(2)

print('Filling form') 
customer = browser.find_elements(By.XPATH, '//*[@id="react-select-2-input"]')
source = browser.find_elements(By.XPATH, '//*[@id="react-select-customfield_10808-instance-input"]')
summary = browser.find_elements(By.XPATH, '//*[@id="summary"]')

customer[0].send_keys('Pillote, Mia')
time.sleep(2)
customer[0].send_keys(Keys.RETURN)
source[0].send_keys('Walk In')
source[0].send_keys(Keys.RETURN)
summary[0].send_keys('Test')
summary[0].send_keys(Keys.RETURN)
time.sleep(15)

print('Resolving')
resolve = browser.find_elements(By.XPATH, '//*[@id="com.atlassian.servicedesk:workflow-transition-761"]')
resolve[0].click()
time.sleep(2)
browser.find_elements(By.XPATH, '/html/body/section/form')[0].submit()
time.sleep(15)

print('Opening ticket information')
browser.find_elements(By.XPATH, '//*[@id="content"]/div/header/div/div/div[2]/div[2]/div/ol/li[3]/a')[0].click()
time.sleep(15)

print('Assigning to you')
browser.find_elements(By.XPATH, '//*[@id="assign-to-me"]')[0].click()
time.sleep(15)

print('Closing')
browser.find_elements(By.XPATH, '//*[@id="opsbar-transitions_more"]')[0].click()
time.sleep(15)
browser.find_elements(By.XPATH, '//*[@id="action_id_941"]/a/div/div[1]')[0].click()

time.sleep(10)
print('Ticket Closed.')

