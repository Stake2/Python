# Database.py

class Database(object):
	def __init__(self):
		from Utility.Modules import Modules as Modules

		Modules().Set(self)

		print(self.Folder)

if __name__ == "__main__":
	Database()