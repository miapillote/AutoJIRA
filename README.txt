Welcome to AutoJIRA for the Rettner Helpdesk!

This application uses Selenium to automate the task of creating and submitting JIRA tickets for equipment rentals and returns, a process that used to take about two minutes per ticket. The manual process is inconsistent, and compliance among employees is poor. This tool reduces the active work associated with submitting IT tickets to the time it takes you to fill out the basic information needed--in my experience, about 20 seconds. That's an 83% time reduction in time spent on IT tickets. Nice!

Key Features:
- Automated JIRA ticket creation, assignment, and resolution
- Automated rental period invites for customers
- Graphical user interface
- Command line interface

Install:
1. Clone this repository into a directory of your choice.
2. Install the required dependencies*
3. Run the following in a python terminal in the src directory:

import CalendarTool
CalendarTool.get_service()

The command should redirect you to a Google consent form. Agree to sharing the requested data and close the window when prompted.

Use:
Graphical Interface:
Run GUI.py. In the AutoJIRA window you may either manually input information or use a PDF form from LASSO. PDFs are the preferred source of information, as they are least likely to contain typos.

Command Line Interface:
Please reference the Documentation for a detailed guide.
