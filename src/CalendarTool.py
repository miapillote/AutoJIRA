"""

The idea for this is for the user to be able to prompt the application to create and share a Google Calendar invite
with the customer. This would, ideally, help people remember to return things on time and keep the library running
smoothly.

https://karenapp.io/articles/how-to-automate-google-calendar-with-python-using-the-calendar-api/

I need to switch the project to a different account so I can add rettnerhelpdesk as a test user...?

"""
import Ticket
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = '../resources/secrets/credentials.json'
PICKLE = '../resources/secrets/token.pickle'

# Event parameter constants
TIMEZONE = "America/New_York"
LOCATION = "Rettner Hall Room 201"
CALENDAR_ID = "primary"


def create_event(ticket: Ticket):
    service = get_calendar_service()

    event = {
        'summary': ticket.item + " Rental",
        'location': LOCATION,
        'start': {
            'dateTime': ticket.date.isoformat(),
            'timeZone': TIMEZONE},
        'end': {
            'dateTime': ticket.due.isoformat(),
            'timeZone': TIMEZONE},
        'attendees': [{'email': ticket.email}]
    }

    event_result = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return event_result


def get_calendar_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(PICKLE):
        with open(PICKLE, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(PICKLE, 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


def test():
    ticket = Ticket.Ticket()
    ticket.read_form("../resources/forms/mpillote.pdf")
    event = create_event(ticket)
    return event
