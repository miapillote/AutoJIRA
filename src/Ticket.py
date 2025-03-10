from pypdf import PdfReader
import re
import datetime


class Ticket:
    def __init__(self):
        self.name = None
        self.netid = None
        self.item = None
        self.date = None
        self.due = None
        self.email = None
        self.action = None

    def manual_input(self, name, item, date, action):
        self.action = action
        self.name = name
        self.item = item
        self.date = date

    def read_form(self, pdf):
        reader = PdfReader(pdf)
        page = reader.pages[0]
        text = page.extract_text(0)
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
        return datetime.datetime.strptime(date_string_cleaned, date_format)
