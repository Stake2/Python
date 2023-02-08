# Database.py

from Utility.Global_Switches import Global_Switches as Global_Switches

from Utility.Language import Language as Language
from Utility.API import API as API
from Utility.File import File as File
from Utility.Folder import Folder as Folder
from Utility.Date import Date as Date
from Utility.Input import Input as Input
from Utility.JSON import JSON as JSON
from Utility.Text import Text as Text

class Database(object):
	def __init__(self):
		self.Define_Basic_Variables()
		self.Define_Folders_And_Files()

		self.Define_Types()

	def Define_Basic_Variables(self):
		self.switches = Global_Switches().switches["global"]

		self.Language = Language()
		self.API = API()
		self.File = File()
		self.Folder = Folder()
		self.Date = Date()
		self.Input = Input()
		self.JSON = JSON()
		self.Text = Text()

		self.languages = self.Language.languages

		self.user_language = self.Language.user_language
		self.full_user_language = self.Language.full_user_language

		self.Sanitize = self.File.Sanitize

		self.folders = self.Folder.folders

		self.date = self.Date.date

	def Define_Folders_And_Files(self):
		# Folders dictionary
		self.folders = self.Folder.Contents(self.folders["notepad"]["networks"]["database_network"]["root"], lower_key = True)["dictionary"]

		# Network data folder ("Types.json" file)

	def Define_Types(self):
		self.types = self.JSON.To_Python(self.folders["notepad"]["networks"]["database_network"]["network_data"]["types"])

		# On "Types.json"
		#self.types = {
		#	"genders": {},
		#	"gender_items": ["the", "these", "this", "a", "of", "of_the", "first", "last"]
		#}

if __name__ == "__main__":
	Database()