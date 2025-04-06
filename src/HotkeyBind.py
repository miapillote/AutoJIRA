import keyboard
import pyautogui
import pyperclip
import Ticket
import JiraFormAutomation as Jira
import time
import CalendarTool

def on_hotkey():
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
    ticket.read_clipboard(copied_text)

    #restore clipboard
    pyperclip.copy(clipboard_buffer)

    ticket.print_ticket()
    CalendarTool.create_event(ticket)
    print("Created calendar event for ", ticket.netid, " ", ticket.action, " ", ticket.item, ".")
    progress = 0
    automation = Jira.JiraFormAutomation(ticket, None, None, progress)
    automation.run()
    

keyboard.add_hotkey('ctrl+shift+l', on_hotkey)

keyboard.wait() # Keep the script running to listen for hotkeys