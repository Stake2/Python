# Database.py

class Database(object):
	def __init__(self):
		self.Define_Basic_Variables()

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		# Import Years class
		from Years.Years import Years as Years
		self.Years = Years()

		self.Define_Folders_And_Files()

		self.Define_Types()

	def Define_Basic_Variables(self):
		from Utility.Global_Switches import Global_Switches as Global_Switches

		from Utility.Language import Language as Language
		from Utility.API import API as API
		from Utility.File import File as File
		from Utility.Folder import Folder as Folder
		from Utility.Date import Date as Date
		from Utility.Input import Input as Input
		from Utility.JSON import JSON as JSON
		from Utility.Text import Text as Text

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
		self.current_year = self.Years.current_year

		# Folders dictionary
		self.folders = self.Folder.Contents(self.folders["notepad"]["networks"]["database_network"]["root"], lower_key = True)["dictionary"]

		# Audiovisual Media Network root files
		self.folders["history"]["current_year"] = self.folders["history"][str(self.date["year"])]

	def Define_Types(self):
		self.types = self.JSON.To_Python(self.folders["notepad"]["networks"]["database_network"]["data"]["types"])

		self.types = {
			"singular": self.types["singular"],
			"plural": self.types["plural"],
			"genders": self.Language.texts["genders, type: list"],
			"gender_items": self.Language.texts["gender_items"]
		}

		i = 0
		for plural_type in self.types["plural"]["en"]:
			language_type = self.types["plural"][self.user_language][i]

			# Create type dictionary
			self.types[plural_type] = {
				"singular": {},
				"plural": {},
				"texts": {},
				"folders": {},
				"subfolders": {},
				"genders": {}
			}

			# Define singular and plural types
			for language in self.languages["small"]:
				for item in ["singular", "plural"]:
					self.types[plural_type][item][language] = self.types[item][language][i]

			# Define genders
			gender = "masculine"

			if plural_type == self.texts["series, title()"]["en"]:
				gender = "feminine"

			for language in self.languages["small"]:
				self.types[plural_type]["genders"][language] = self.types["genders"][language][gender]

			# Create folders
			key = plural_type.lower().replace(" ", "_")

			# History Per Type folder
			self.folders["history"]["current_year"]["per_media_type"][key] = {
				"root": self.folders["history"]["current_year"]["per_media_type"]["root"] + language_type + "/",
			}

			self.Folder.Create(self.folders["history"]["current_year"]["per_media_type"][key]["root"])

			# Entries.json file
			self.folders["history"]["current_year"]["per_media_type"][key]["entries"] = self.folders["history"]["current_year"]["per_media_type"][key]["root"] + "Entries.json"
			self.File.Create(self.folders["history"]["current_year"]["per_media_type"][key]["entries"])

			# Entry list.txt file
			self.folders["history"]["current_year"]["per_media_type"][key]["entry_list"] = self.folders["history"]["current_year"]["per_media_type"][key]["root"] + "Entry list.txt"
			self.File.Create(self.folders["history"]["current_year"]["per_media_type"][key]["entry_list"])

			# Files folder
			self.folders["history"]["current_year"]["per_media_type"][key]["files"] = {
				"root": self.folders["history"]["current_year"]["per_media_type"][key]["root"] + "Files/",
			}

			self.Folder.Create(self.folders["history"]["current_year"]["per_media_type"][key]["files"]["root"])

			# Define type folders and files
			self.types[plural_type]["folders"] = {
				"per_media_type": self.folders["history"]["current_year"]["per_media_type"][key]
			}

		# Write types dictionary into "Types.json" file
		self.JSON.Edit(self.folders["data"]["types"], self.types)

	def Define_Registry_Format(self):
		# Define default Entries dictionary template
		self.template = {
			"Number": 0,
			"Entries": [],
			"Dictionary": {}
		}

		self.entries = self.template.copy()

		# If Entries.json is not empty and has entries, get Entries dictionary from it
		if self.File.Contents(self.folders["history"]["current_year"]["entries"])["lines"] != [] and self.JSON.To_Python(self.folders["history"]["current_year"]["entries"])["Entries"] != []:
			self.entries = self.JSON.To_Python(self.folders["history"]["current_year"]["entries"])

		self.JSON.Edit(self.folders["history"]["current_year"]["entries"], self.entries)

		# Define root Entries dictionary
		self.type_entries = {}

		# Iterate through English types list
		for plural_type in self.types["plural"]["en"]:
			key = plural_type.lower().replace(" ", "_")

			# Define default type dictionary
			self.type_entries[plural_type] = deepcopy(self.template)

			# If type "Entries.json" is not empty, get type Entries dictionary from it
			if self.File.Contents(self.folders["history"]["current_year"]["per_media_type"][key]["entries"])["lines"] != [] and self.JSON.To_Python(self.folders["history"]["current_year"]["per_media_type"][key]["entries"])["Entries"] != []:
				self.type_entries[plural_type] = self.JSON.To_Python(self.folders["history"]["current_year"]["per_media_type"][key]["entries"])

			self.JSON.Edit(self.folders["history"]["current_year"]["per_media_type"][key]["entries"], self.type_entries[plural_type])

if __name__ == "__main__":
	Database()