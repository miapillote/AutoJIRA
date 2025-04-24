import keyboard
import pyautogui
import pyperclip
import Ticket
import JiraFormAutomation as Jira
import time
import CalendarTool
import queue
import threading
from selenium import webdriver

WELCOME = """

Welcome to the Jira Hotkey Console. Keep this open to track the tickets submitted for today.
Instructions:
- To submit a "Loaned" ticket, navigate to the Lasso loaner form and type ctrl+shift+L
- To submit a "Returned" ticket, navigate to the Lasso loaner form and type ctrl+shift+;

"""

CHROME_PATH = r'--user-data-dir=C:/Users/rettnerhelpdesk/AppData/Local/Google/Chrome'
CHROME_PROFILE = '--profile-directory=Profile 4'
print(WELCOME)


def worker():
    print("[Worker] Starting worker thread...")

    # Shared browser instance
    options = webdriver.ChromeOptions()
    options.add_argument(CHROME_PATH)
    options.add_argument(CHROME_PROFILE)
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)

    while True:
        ticket = ticket_queue.get()
        if ticket is None:
            break
        print("[Worker] Processing new ticket...")

        start_timer = time.perf_counter()

        if ticket.action == "Loaned":
            try:
                CalendarTool.create_event(ticket)
                print("[Worker] Created calendar event for ", ticket.netid, " ", ticket.action, " ", ticket.item, ".")
            except Exception as e:
                print(f"[Worker] Failed to create calendar event: {e}")

        try:
            automation = Jira.JiraFormAutomation(ticket, None, None, 0, browser)
            automation.run()
            stop_timer = time.perf_counter()
            print(f"[Worker] Ticket automation done. Time elapsed: {stop_timer - start_timer:0.4f}s.")
        except Exception as e:
            print("[Worker] Error during automation:", e)

        ticket_queue.task_done()
        print("", flush=True)

    # Clean up after thread is done
    print("[Worker] Shutting down browser...")
    browser.quit()


ticket_queue = queue.Queue()
worker_thread = threading.Thread(target=worker, daemon=True)
worker_thread.start()


def on_hotkey(action):
    print(f"\"{action}\" ticket requested, queuing task...")
    # copy whatever's on the clipboard first so it doesn't get tossed
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

    # restore clipboard
    pyperclip.copy(clipboard_buffer)

    try:
        ticket.read_clipboard(copied_text, action)
    except:
        print("Parsing failed, Loaner Form page not detected.")
        return

    ticket.print_ticket()

    ticket_queue.put(ticket)
    print("", flush=True)


def on_loan_hotkey():
    on_hotkey("Loaned")


def on_return_hotkey():
    on_hotkey("Returned")


keyboard.add_hotkey('ctrl+shift+l', on_loan_hotkey)
keyboard.add_hotkey('ctrl+shift+;', on_return_hotkey)
keyboard.wait()  # Keep the script running to listen for hotkeys
