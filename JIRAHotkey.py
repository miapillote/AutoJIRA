import keyboard
import pygetwindow as gw
import pyperclip
import pyautogui
import subprocess
import time
from bs4 import BeautifulSoup

def scrapeHTML():
	#get active window
	activeWindow = gw.getActiveWindow()
	if not activeWindow or "chrome" not in activeWindow.title.lower():
		print("Not a chrome window")
		return None
	
	#Copy URL from address bar
	pyautogui.hotkey('ctrl','u') #open html
	time.sleep(0.1)
	pyautogui.hotkey('ctrl','a') #select all
	time.sleep(0.1)
	pyautogui.hotkey('ctrl','c') #copy
	time.sleep(0.1)
	pyautogui.hotkey('ctrl','w') #close tab
	return pyperclip.paste()

def parseHTML(sourceHtml):
	soup = BeautifulSoup(sourceHTML, "html.parser")
	name = [soup.find(id="#loanercalform-custName")[0], soup.find(id="#loanercalform-custName")[1]] #[first last]
	print(name)
	return None
	

time.sleep(10)
sourceHTML = scrapeHTML()
parseHTML(sourceHTML)