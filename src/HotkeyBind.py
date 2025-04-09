import keyboard
import pyautogui
import pyperclip
import Ticket
import JiraFormAutomation as Jira
import time
import CalendarTool

def on_hotkey(action):
    #copy whatever's on the clipboard first so it doesn't get tossed
    clipboard_buffer = pyperclip.paste()
    
    time.sleep(0.5)
    keyboard.send("ctrl+a")
    time.sleep(1)
    keyboard.send("ctrl+c")
    time.sleep(1)
    pyautogui.click()
    
    copied_text = None
    for _ in range(5):  # Try a few times to get clipboard content
        copied_text = pyperclip.paste()
        if copied_text:
            break
        time.sleep(0.5)  # Wait and try again if clipboard is empty
    
    ticket = Ticket.Ticket()
    
    try:
        ticket.read_clipboard(copied_text, action)
    except:
        print("Parsing failed, Loaner Form page not detected.")
        return

    #restore clipboard
    pyperclip.copy(clipboard_buffer)

    ticket.print_ticket()
    
    try:
        CalendarTool.create_event(ticket)
        print("Created calendar event for ", ticket.netid, " ", ticket.action, " ", ticket.item, ".")
    except:
        print("Failed to create calendar event.")
        
    progress = 0
    automation = Jira.JiraFormAutomation(ticket, None, None, progress)
    
    try:
        automation.run()
    except:
        print("Ticket close failed.")

def on_loan_hotkey():
    on_hotkey("Loaned")

def on_return_hotkey():
    on_hotkey("Returned")

keyboard.add_hotkey('ctrl+shift+l', on_loan_hotkey)
keyboard.add_hotkey('ctrl+shift+;', on_return_hotkey)

keyboard.wait() # Keep the script running to listen for hotkeys