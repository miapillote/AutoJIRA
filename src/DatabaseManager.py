import sqlite3
from datetime import datetime
import Ticket

"""

The goal of this is to have the database track the items that have been loaned so that they can be selected from in a 
drop-down menu. Secondarily, it's to prevent you from submitting a jira ticket twice and from creating a two of the 
same G-Cal event. For now, though, I am exhausted.

"""

# Connect to SQLite (creates the file if it doesn't exist)
conn = sqlite3.connect('../resources/tickets.db')
cursor = conn.cursor()

# Create the table (only if it doesn't exist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tickets (
        netid TEXT NOT NULL,
        item TEXT NOT NULL,
        date TEXT NOT NULL,
        calendarEvent BOOLEAN NOT NULL,
        jiraTicket BOOLEAN NOT NULL,
        filePath TEXT NOT NULL,
        UNIQUE(netid, item)
    )
''')


# Function to create a new ticket
def create_record(ticket: Ticket):
    cursor.execute('''
        INSERT OR IGNORE INTO tickets (netid, item, date, calendarEvent, jiraTicket, filePath)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        ticket.netid, ticket.item, ticket.date.isoformat(), ticket.calendar_event, ticket.jira_ticket,
        ticket.file_path))
    conn.commit()
    print(f"Ticket created: {ticket.netid}, {ticket.item}")


# Function to mark a ticket as completed
def delete_record(ticket: Ticket):
    cursor.execute("""DELETE FROM tickets WHERE netid = ? AND item = ?""", (ticket.netid, ticket.item))
    print(f"record {ticket.netid} {ticket.item} deleted.")


def search_records(ticket: Ticket):
    cursor.execute("""SELECT * FROM tickets WHERE netid = ? AND item = ?""",
                   (ticket.netid, ticket.item))
    return True if cursor.fetchall() else False


def retrieve_all():
    cursor.execute('SELECT * FROM tickets')
    tickets = cursor.fetchall()
    for item in tickets:
        print(item[0] + " " + item[1])


def test():
    ticket = Ticket.Ticket()
    ticket.read_form("../resources/forms/mpillote.pdf")
    create_record(ticket)
    retrieve_all()
    print(search_records(ticket))


# Close the connection when done
conn.close()
