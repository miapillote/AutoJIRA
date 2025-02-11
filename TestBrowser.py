from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys

class TestBrowser:
	def __init__(self):
		options = webdriver.ChromeOptions()
		options.add_argument(r'--user-data-dir=C:\\Users\\miapi\\AppData\\Local\\Google\\Chrome')
		options.add_argument(r'--profile-directory=Profile4')
		options.add_experimental_option("detach",True) #keep browser open
		self.browser = webdriver.Chrome(options=options)
		self.browser.implicitly_wait(15)

