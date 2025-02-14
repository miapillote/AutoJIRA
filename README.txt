To setup on the Rettner machine:

- Clone into an easily accessible directory in on the desktop (ideally the one I made called "startup" (? I think ?)
- Add powershell script in the "startup" folder:
	- probably located at "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup" or something
	- restart the machine and see if it starts up
	- script should be: py <path-to-gui.py>

- Important things to note while I add features and bug fixes:
	- It won't always find the right customer if you spell the name wrong, so be careful
	- Don't close the gui window
	- If you do, reopen it on the command line with py <path-to-gui.py>
	- You can use this from the command line as well by calling py <path-to-JiraFormAutomation.py> -first -last -action -item1 -item... -itemi

Upcoming features:
	- logged out detection + login handling (in progress)
	- google calendar invitation
	- trigger from print form
	- suggest returns
