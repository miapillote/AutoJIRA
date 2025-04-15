# 🛠️ Rettner Helpdesk Ticket Automation Tool

This tool automates the submission of support requests to the **Rettner Helpdesk** at the University of Rochester. It streamlines the process of reporting common technical issues, saving time and ensuring consistent formatting across tickets.

## ✨ Features

- 📄 Automatically fills out and submits requests to the [Rettner Helpdesk Portal](https://tech.rochester.edu/help/)
- 🧾 Creates and shares a Google Calendar event for every loaner ticket request
- 💬 Option of GUI orr CLI
- 📌 Supports multithreading for batch ticket submission
- ✅ Confirms successful submission of each request

## 🧰 Requirements

- Python 3.7+
- Chrome + ChromeDriver (or another compatible browser/driver)
- University of Rochester SSO credentials (NetID login)

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/miapillote/AutoJIRA
   cd AutoJIRA
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure settings**
   - Edit `config.py` to set:
     - Chrome driver & profile locations
     - Calendar IDs
     - Preferred issue description template

4. **Run the script**
   ```bash
   python HotkeyBind.py # for CLI
   python GUI.py        # for GUI
   ```

   You'll be prompted to enter the issue details, or you can use a predefined set of hotkeys to scrape information from LASSO forms.
   
## 🛟 Support

For questions or suggestions, open an issue.
