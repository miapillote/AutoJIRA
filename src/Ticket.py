from pypdf import PdfReader
import re
import datetime


class Ticket:
    def __init__(self, pdf):
        self.name, self.netid, self.item, self.date, self.due, self.email = self.read_form(pdf)
        print(self.name, " ", self.netid, " ", self.item, " ", self.date, " ", self.due, " ", self.email)

    def read_form(self, pdf):
        reader = PdfReader(pdf)
        page = reader.pages[0]
        text = page.extract_text(0)
        name = self.read_name(re.findall(r"NAME:\s*(.*?)(?=\s*NETID:)", text)[0])
        netid = re.findall(r"NETID:\s*(\S+)", text)[0]
        item = re.findall(r"ITEM:\s*(.*?)(?=\s*DUE:)", text)[0]
        date = self.read_date(re.findall(r"OUT:\s*(.*?)(?=\s*CONDITION)", text)[0])
        due = self.read_date(re.findall(r"DUE:\s*(.*?)(?=\s*NAME:)", text)[0])
        email = re.findall(r"EMAIL:\s*(.*?)(?=\s*ATTENDANT)", text)[0]
        return name, netid, item, date, due, email

    def read_name(self, full_name):
        full_name = full_name.split()
        first_name = full_name[0]
        last_name = " ".join(full_name[1:])
        return [first_name, last_name]

    def read_date(self, date_string):
        date_string_cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_string)
        date_format = "%A, %B %d %Y, %I:%M %p"
        return datetime.datetime.strptime(date_string_cleaned, date_format)

