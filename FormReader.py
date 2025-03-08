from pypdf import PdfReader
import re

class FormReader:
    def __init__(self, pdf):
        reader = PdfReader(pdf)
        page = reader.pages[0]
        text = page.extract_text(0)
        name = re.findall(r"NAME:\s*(.*?)(?=\s*NETID:)", text)
        netid = re.findall(r"NETID:\s*(\S+)", text)
        item = re.findall(r"ITEM:\s*(.*?)(?=\s*DUE:)", text)
        date = re.findall(r"OUT:\s*(.*?)(?=\s*CONDITION)", text)
        due = re.findall(r"DUE:\s*(.*?)(?=\s*NAME:)", text)
        email = re.findall(r"EMAIL:\s*(.*?)(?=\s*ATTENDANT)", text)
        print(name, " ", netid, " ", item, " ", date, " ", due, " ", email)



