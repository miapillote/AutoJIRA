import getpass

def getCreds():
	print("Username: ")
	username = getpass.getuser()
	print("Password: ")
	password = getpass.getpass("Entering password: ")
	return username, password

