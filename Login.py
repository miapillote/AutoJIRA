import getpass

def getCreds():
	print("Username: ")
	username = input()
	print("Password: ")
	getpass.getpass("Entering password: ")
	return username, password

