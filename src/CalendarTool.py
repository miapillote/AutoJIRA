"""

TODO: add a link to the form they signed, if available

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
CALENDAR_ID = "062010d99253329019c986e3f5d062cf3ae57abc074bfea1328d008158c602ed@group.calendar.google.com"
DESCRIPTION = """
You are about to check out a very expensive piece(s) of electronic equipment from AS&E IT. If you fail to abide by the rules below, your borrowing privileges may be revoked and you may be liable for the full replacement cost. You will be asked to sign an agreement regarding the condition of the item(s) upon return.

1. I will assume full responsibility for the equipment I am checking out.
2. I will not let anyone else use the equipment while it is checked out to me.
3. I will not leave said item(s) unattended. I will always put the item(s) in a safe place when not in use.
4. When not in use I will always carry the item(s) in its provided bag.
5. I will return the item(s) in the same condition as when it/they were checked out to me. If any damage or loss occurs while checked out to me, I will be responsible for the full repair or replacement costs.
6. I will personally return the item(s) before the designated date and time below. Strikes, which expire after 6 months, will be issued for lateness or damage. Bans can be issued for severe violations. An accumulation of 3 strikes will result in a temporary ban. Up to 6 hours late will constitute 1 strike and additional strike(s) will be issued for each subsequent 6 hour period.
7. For loaner laptops, personal data may not be preserved, and will be purged on restart. The data in the Saved Data folder will be saved, and you are responsible for deleting it before returning the computer.
"""


def create_event(ticket: Ticket):
    service = get_calendar_service()

    event = {
        'summary': ticket.item + " Rental",
        'location': LOCATION,
        'description': DESCRIPTION,
        'start': {
            'dateTime': ticket.date.isoformat(),
            'timeZone': TIMEZONE},
        'end': {
            'dateTime': ticket.due.isoformat(),
            'timeZone': TIMEZONE},
        'attendees': [{'email': ticket.email}]
    }

    event_result = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return event_result.get('htmlLink'))


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
