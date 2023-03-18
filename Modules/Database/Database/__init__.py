# Database.py

class Database(object):
	def __init__(self):
		self.Define_Basic_Variables()

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.Define_Texts()

		# Import Years class
		from Years.Years import Years as Years
		self.Years = Years()

		self.Define_Folders_And_Files()

		self.Define_Types()
		self.Define_Registry_Format()

	def Define_Basic_Variables(self):
		from Utility.Global_Switches import Global_Switches as Global_Switches

		from Utility.File import File as File
		from Utility.Folder import Folder as Folder
		from Utility.Date import Date as Date
		from Utility.Input import Input as Input
		from Utility.JSON import JSON as JSON
		from Utility.Text import Text as Text

		self.switches = Global_Switches().switches["global"]

		self.File = File()
		self.Folder = Folder()
		self.Date = Date()
		self.Input = Input()
		self.JSON = JSON()
		self.Text = Text()

		self.languages = self.JSON.Language.languages

		self.user_language = self.JSON.Language.user_language
		self.full_user_language = self.JSON.Language.full_user_language

		self.Sanitize = self.File.Sanitize

		self.folders = self.Folder.folders

		self.date = self.Date.date

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.JSON.Language.Item(self.texts)

		self.large_bar = "-----"
		self.dash_space = "-"

	def Define_Folders_And_Files(self):
		self.current_year = self.Years.current_year

		# Folders dictionary
		self.folders = self.Folder.Contents(self.folders["notepad"]["networks"]["database_network"]["root"], lower_key = True)["dictionary"]

		# Audiovisual Media Network root files
		self.folders["history"]["current_year"] = self.folders["history"][str(self.date["year"])]

	def Define_Types(self):
		self.types = self.JSON.To_Python(self.folders["data"]["types"])

		# Iterate through English plural types list
		i = 0
		for plural_type in self.types["plural"]["en"]:
			key = plural_type.lower().replace(" ", "_")

			# Create type dictionary
			self.types[plural_type] = {
				"singular": {},
				"plural": {},
				"folders": {},
				"items": {}
			}

			# Define singular and plural types
			for language in self.languages["small"]:
				for item in ["singular", "plural"]:
					self.types[plural_type][item][language] = self.types[item][language][i]

			# Create "Per Type" type folder
			self.folders["history"]["current_year"]["per_type"][key] = {
				"root": self.folders["history"]["current_year"]["per_type"]["root"] + plural_type + "/"
			}

			self.Folder.Create(self.folders["history"]["current_year"]["per_type"][key]["root"])

			# Create "Entries.json" file in "Per Type" type folder
			self.folders["history"]["current_year"]["per_type"][key]["entries"] = self.folders["history"]["current_year"]["per_type"][key]["root"] + "Entries.json"
			self.File.Create(self.folders["history"]["current_year"]["per_type"][key]["entries"])

			# Create "Entry list.txt" file in "Per Type" type folder
			self.folders["history"]["current_year"]["per_type"][key]["entry_list"] = self.folders["history"]["current_year"]["per_type"][key]["root"] + "Entry list.txt"
			self.File.Create(self.folders["history"]["current_year"]["per_type"][key]["entry_list"])

			# Create "Files" folder on "Per Type" type folder
			self.folders["history"]["current_year"]["per_type"][key]["files"] = {
				"root": self.folders["history"]["current_year"]["per_type"][key]["root"] + "Files/",
			}

			self.Folder.Create(self.folders["history"]["current_year"]["per_type"][key]["files"]["root"])

			# Define type folders and files
			self.types[plural_type]["folders"] = {
				"per_type": self.folders["history"]["current_year"]["per_type"][key]
			}

			# Define entry item
			for language in self.languages["small"]:
				self.types[plural_type]["items"][language] = self.types["items, type: dict"][plural_type][language]

			i += 1

		# Write the types dictionary into "Types.json" file
		self.JSON.Edit(self.folders["data"]["types"], self.types)

	def Define_Registry_Format(self):
		from copy import deepcopy

		# Define default Entries dictionary template
		self.template = {
			"Numbers": {
				"Total": 0,
			},
			"Entries": [],
			"Dictionary": {}
		}

		self.dictionaries = {
			"Entries": deepcopy(self.template),
			"Entry": {},
			"Entry Type": {}
		}

		# If Entries.json is not empty and has entries, get Entries dictionary from it
		if self.File.Contents(self.folders["history"]["current_year"]["entries"])["lines"] != [] and self.JSON.To_Python(self.folders["history"]["current_year"]["entries"])["Entries"] != []:
			self.dictionaries["Entries"] = self.JSON.To_Python(self.folders["history"]["current_year"]["entries"])

		self.JSON.Edit(self.folders["history"]["current_year"]["entries"], self.dictionaries["Entries"])

		# Iterate through English types list
		for plural_type in self.types["plural"]["en"]:
			key = plural_type.lower().replace(" ", "_")

			# Define default type dictionary
			self.dictionaries["Entry Type"][plural_type] = deepcopy(self.template)

			# If type "Entries.json" is not empty, get type Entries dictionary from it
			if self.File.Contents(self.folders["history"]["current_year"]["per_type"][key]["entries"])["lines"] != [] and self.JSON.To_Python(self.folders["history"]["current_year"]["per_type"][key]["entries"])["Entries"] != []:
				self.type_entries[plural_type] = self.JSON.To_Python(self.folders["history"]["current_year"]["per_type"][key]["entries"])

			self.JSON.Edit(self.folders["history"]["current_year"]["per_type"][key]["entries"], self.dictionaries["Entry Type"][plural_type])

	def Define_States_Dictionary(self, dictionary):
		states_dictionary = {
			"States": {},
			"Texts": {}
		}

		# Define keys for the states
		keys = [
			"First entry in year",
			"First type entry in year"
		]

		# Iterate through the states keys
		for key in keys:
			# If the state is True
			if dictionary["States"][key] == True:
				state = True

				# Define the state dictionary
				states_dictionary["States"][key] = state

				# Define the state texts of the current state dictionary
				states_dictionary["Texts"][key] = {}

				for language in self.languages["small"]:
					text = ""

					if key != "First type entry in year":
						text_key = key.lower().replace(" ", "_")

						if text_key in self.JSON.Language.texts:
							text = self.JSON.Language.texts[text_key][language]

						else:
							text = self.texts[text_key][language]

					if key == "First type entry in year":
						entry_item = self.types["items, type: dict"][dictionary["Type"]["plural"]["en"]][language].lower()

						text = self.JSON.Language.texts["first_{}_in_year"][language].format(entry_item)

					states_dictionary["Texts"][key][language] = text

		return states_dictionary

if __name__ == "__main__":
	Database()