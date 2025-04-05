from pypdf import PdfReader
import re
import datetime
from datetime import timedelta


class Ticket:
    def __init__(self):
        self.name = None
        self.netid = None
        self.item = None
        self.date = None
        self.due = None
        self.email = None
        self.action = None
        self.file_path = None
        self.id = None
        self.calendar_event = True
        self.jira_ticket = True

    def manual_input(self, name, item, date, action):
        self.action = action
        self.name = name
        self.item = item
        self.date = date
        self.due = date + timedelta(days=3)
        self.due = self.due.replace(hour=10, minute=0, second=0, microsecond=0)

    def read_form(self, pdf, action):
        self.file_path = pdf
        reader = PdfReader(pdf)
        page = reader.pages[0]
        text = page.extract_text(0)
        self.action = action
        self.name = self.read_name(re.findall(r"NAME:\s*(.*?)(?=\s*NETID:)", text)[0])
        self.netid = re.findall(r"NETID:\s*(\S+)", text)[0]
        self.item = re.findall(r"ITEM:\s*(.*?)(?=\s*DUE:)", text)[0]
        self.date = self.read_date(re.findall(r"OUT:\s*(.*?)(?=\s*CONDITION)", text)[0])
        self.due = self.read_date(re.findall(r"DUE:\s*(.*?)(?=\s*NAME:)", text)[0])
        self.email = re.findall(r"EMAIL:\s*(.*?)(?=\s*ATTENDANT)", text)[0]
        
    def read_clipboard(self, text):
        self.action = "Loaned"
        self.name = self.read_name(re.findall(r"NAME:\s*(.*?)(?=\s*NETID:)", text)[0])
        self.netid = re.findall(r"NETID:\s*(\S+)", text)[0]
        self.item = re.findall(r"ITEM:\s*(.*?)(?=\s*DUE:)", text)[0]
        self.date = self.read_date(re.findall(r"OUT:\s*(.*?)(?=\s*CONDITION)", text)[0])
        self.due = self.read_date(re.findall(r"DUE:\s*(.*?)(?=\s*NAME:)", text)[0])
        self.email = re.findall(r"EMAIL:\s*(.*?)(?=\s*ATTENDANT)", text)[0]

    @staticmethod
    def read_name(full_name):
        full_name = full_name.split()
        first_name = full_name[0]
        last_name = " ".join(full_name[1:])
        return [first_name, last_name]

    @staticmethod
    def read_date(date_string):
        date_string_cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_string)
        date_format = "%A, %B %d %Y, %I:%M %p"
        print(date_string_cleaned)
        return datetime.datetime.strptime(date_string_cleaned, date_format)
        
    def print_ticket(self):
        print("Action: ", self.action)
        print("Name: ", self.name)
        print("NetID: ", self.netid)
        print("Item: ", self.item)
        print("Date: ", self.date)
        print("Due date: ", self.due)
        print("Email: ", self.email)


def test():
    ticket = Ticket()
    ticket.manual_input(["Mia", "Pillote"], "Test Item", datetime.datetime.now(), "Testing")
    print(ticket.date)
    print(ticket.due)
    return ticket
