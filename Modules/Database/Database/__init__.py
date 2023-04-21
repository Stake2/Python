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

		self.types.update({
			"data_list": {
				"Number": 0,
				"Numbers": {}
			}
		})

		# Reset the data number to 0
		if self.types["data_list"]["Number"] != 0:
			self.types["data_list"]["Number"] = 0

		# Read the root "Info.json" file
		if self.File.Contents(self.folders["information"]["info"])["lines"] != []:
			info_dictionary = self.JSON.To_Python(self.folders["information"]["info"])

		# If the root "Info.json" file is empty, add a default JSON dictionary inside it
		if self.File.Contents(self.folders["information"]["info"])["lines"] == []:
			info_dictionary = {
				"types": self.game_types["plural"],
				"Number": 0,
				"Numbers": {}
			}

		# Iterate through English plural types list
		i = 0
		for plural_type in self.types["plural"]["en"]:
			key = plural_type.lower().replace(" ", "_")

			language_type = self.types["plural"][self.user_language][i]

			# Create type dictionary
			self.types[plural_type] = {
				"singular": {},
				"plural": {},
				"folders": {},
				"status": [
					self.texts["registering, title()"]["en"],
					self.texts["re_registering, title()"]["en"]
				],
				"items": {}
			}

			# Define singular and plural types
			for language in self.languages["small"]:
				for item in ["singular", "plural"]:
					self.types[plural_type][item][language] = self.types[item][language][i]

			# Create type folders
			for root_folder in ["Information", "History"]:
				root_key = root_folder.lower().replace(" ", "_")

				# "Data Information" folder
				if root_folder == "Information":
					self.folders[root_key][key] = {
						"root": self.folders[root_key]["root"] + language_type + "/"
					}

					self.Folder.Create(self.folders[root_key][key]["root"])

				# "History Per Type" folder
				if root_folder == "History":
					self.folders[root_key]["current_year"]["per_type"][key] = {
						"root": self.folders[root_key]["current_year"]["per_type"]["root"] + plural_type + "/"
					}

					self.Folder.Create(self.folders[root_key]["current_year"]["per_type"][key]["root"])

					# Create "Entries.json" file
					self.folders[root_key]["current_year"]["per_type"][key]["entries"] = self.folders[root_key]["current_year"]["per_type"][key]["root"] + "Entries.json"
					self.File.Create(self.folders[root_key]["current_year"]["per_type"][key]["entries"])

					# Create "Entry list.txt" file
					self.folders[root_key]["current_year"]["per_type"][key]["entry_list"] = self.folders[root_key]["current_year"]["per_type"][key]["root"] + "Entry list.txt"
					self.File.Create(self.folders[root_key]["current_year"]["per_type"][key]["entry_list"])

					# Create "Files" folder 
					self.folders[root_key]["current_year"]["per_type"][key]["files"] = {
						"root": self.folders[root_key]["current_year"]["per_type"][key]["root"] + "Files/"
					}

					self.Folder.Create(self.folders[root_key]["current_year"]["per_type"][key]["files"]["root"])

			# Define type folders and files
			self.types[plural_type]["folders"] = {
				"information": self.folders["information"][key],
				"per_type": self.folders["history"]["current_year"]["per_type"][key]
			}

			# Define the "Info.json" file
			self.types[plural_type]["folders"]["information"]["info"] = self.types[plural_type]["folders"]["information"]["root"] + "Info.json"
			self.File.Create(self.types[plural_type]["folders"]["information"]["info"])

			# Read the "Info.json" file
			if self.File.Contents(self.types[plural_type]["folders"]["information"]["info"])["lines"] != []:
				self.types[plural_type]["json"] = self.JSON.To_Python(self.types[plural_type]["folders"]["information"]["info"])

			# If the "Info.json" file is empty, add a default JSON dictionary inside it
			if self.File.Contents(self.types[plural_type]["folders"]["information"]["info"])["lines"] == []:
				# Define the default JSON dictionary
				self.types[plural_type]["json"] = {
					"Number": 0,
					"Titles": [],
					"Status": {}
				}

				# Create an empty list for each status
				for english_status in self.texts["statuses, type: list"]["en"]:
					self.types[plural_type]["json"]["Status"][english_status] = []

			# Update the number of data inside the json dictionary
			self.types[plural_type]["json"]["Number"] = len(self.types[plural_type]["json"]["Titles"])

			# Edit the "Info.json" file with the new dictionary
			self.JSON.Edit(self.types[plural_type]["folders"]["information"]["info"], self.types[plural_type]["json"])

			# Add the data number to the data number inside the data list
			self.types["data_list"]["Number"] += self.types[plural_type]["json"]["Number"]

			# Add the media number to the media type media numbers
			self.types["data_list"]["Numbers"][plural_type] = self.types[plural_type]["json"]["Number"]

			# Add the data number to the root data number
			info_dictionary["Numbers"][plural_type] = self.types[plural_type]["json"]["Number"]

			# Get the data list with "Registering" and "Re-registering" statuses
			self.types[plural_type]["data_list"] = self.Get_Data_List(self.types[plural_type])

			# Remove the "json" key
			self.types[plural_type].pop("json")

			# Define the entry item
			for language in self.languages["small"]:
				self.types[plural_type]["items"][language] = self.types["items, type: dict"][plural_type][language]

			i += 1

		# Write the types dictionary into the "Types.json" file
		self.JSON.Edit(self.folders["data"]["types"], self.types)

		# Update the data list inside the root "Info.json" dictionary
		info_dictionary.update(self.types["data_list"])

		# Update the root "Info.json" file
		self.JSON.Edit(self.folders["information"]["info"], info_dictionary)

	def Define_Registry_Format(self):
		from copy import deepcopy

		# Define the default Entries dictionary template
		self.template = {
			"Numbers": {
				"Total": 0
			},
			"Entries": [],
			"Dictionary": {}
		}

		self.dictionaries = {
			"History": {
				"Numbers": {
					"Years": 0,
					"Entries": 0
				},
				"Years": []
			},
			"Entries": deepcopy(self.template),
			"Entry": {},
			"Entry Type": {}
		}

		if self.File.Contents(self.folders["history"]["history"])["lines"] != [] and self.JSON.To_Python(self.folders["history"]["history"])["Years"] != []:
			# Get the History dictionary from file
			self.dictionaries["History"] = self.JSON.To_Python(self.folders["history"]["history"])

		# If the current year is not inside the "History" years list, add it to the list
		if self.current_year["Number"] not in self.dictionaries["History"]["Years"]:
			self.dictionaries["History"]["Years"].append(self.current_year["Number"])

		# Update the number of years with the length of the years list
		self.dictionaries["History"]["Numbers"]["Years"] = len(self.dictionaries["History"]["Years"])

		entries = 0

		# Update the number of entries of all years
		for year in range(self.date["year"], self.date["year"] + 1):
			year = str(year)

			# Get the year folder and the entries file
			year_folder = self.folders["history"]["root"] + year + "/"
			entries_file = year_folder + "Entries.json"

			# If the file exists and it is not empty
			if self.File.Exist(entries_file) == True and self.File.Contents(entries_file)["lines"] != []:
				# Add the number of lines of the file to the local number of entries
				entries += self.JSON.To_Python(entries_file)["Numbers"]["Total"]

			# Add the year to the Years list if it is not inside it
			if year not in self.dictionaries["History"]["Years"]:
				self.dictionaries["History"]["Years"].append(year)

		# Sort the Years list
		self.dictionaries["History"]["Years"] = sorted(self.dictionaries["History"]["Years"], key = str.lower)

		# Define the number of Entries of all years as the local number of entries
		self.dictionaries["History"]["Numbers"]["Entries"] = entries

		# Update the "History.json" file with the new History dictionary
		self.JSON.Edit(self.folders["history"]["history"], self.dictionaries["History"])

		# If the "Entries.json" is not empty and has entries, get the Entries dictionary from it
		if self.File.Contents(self.folders["history"]["current_year"]["entries"])["lines"] != [] and self.JSON.To_Python(self.folders["history"]["current_year"]["entries"])["Entries"] != []:
			self.dictionaries["Entries"] = self.JSON.To_Python(self.folders["history"]["current_year"]["entries"])

		# Iterate through the English types list
		for plural_type in self.types["plural"]["en"]:
			key = plural_type.lower().replace(" ", "_")

			# Define default type dictionary
			self.dictionaries["Entry Type"][plural_type] = deepcopy(self.template)

			# If the type "Entries.json" is not empty, get the type Entries dictionary from it
			if self.File.Contents(self.folders["history"]["current_year"]["per_type"][key]["entries"])["lines"] != [] and self.JSON.To_Python(self.folders["history"]["current_year"]["per_type"][key]["entries"])["Entries"] != []:
				self.dictionaries["Entry Type"][plural_type] = self.JSON.To_Python(self.folders["history"]["current_year"]["per_type"][key]["entries"])

			# Add the plural type number to the root numbers if it does not exist in there
			if plural_type not in self.dictionaries["Entries"]["Numbers"]:
				self.dictionaries["Entries"]["Numbers"][plural_type] = 0

			# Else, define the root total number per type as the number inside the Entries dictionary per type
			if plural_type in self.dictionaries["Entries"]["Numbers"]:
				self.dictionaries["Entries"]["Numbers"][plural_type] = self.dictionaries["Entry Type"][plural_type]["Numbers"]["Total"]

			# Update the per type "Entries.json" file with the updated per type Entries dictionary
			self.JSON.Edit(self.folders["history"]["current_year"]["per_type"][key]["entries"], self.dictionaries["Entry Type"][plural_type])

		# Update the "Entries.json" file with the updated Entries dictionary
		self.JSON.Edit(self.folders["history"]["current_year"]["entries"], self.dictionaries["Entries"])

	def Get_Data_List(self, dictionary, status = None):
		'''

		Returns a data list of a specific data type that contains a data status

			Parameters:
				dictionary (dict): a data_type dictionary containing the data type folders
				status (str or list): a status string or list used to get the data that has that status

			Returns:
				data_list (list): The data list that contains the data that has the passed status string or list

		'''

		# Get the status list from the data type dictionary
		status_list = dictionary["status"].copy()

		# If the status parameter is not None, use it as the status
		if status != None:
			status_list = status

		# If the type of the status list is string, make it a list of only the string
		if type(status_list) == str:
			status_list = [status_list]

		# Get the data type "Info.json" file and read it
		dictionary["json"] = self.JSON.To_Python(dictionary["folders"]["information"]["info"])

		# Define the empty data list
		data_list = []

		# Add the data of each status to the data list
		for status in status_list:
			if type(status) == dict:
				status = status["en"]

			data_list.extend(dictionary["json"]["Status"][status])

		# Sort the data list
		data_list = sorted(data_list, key = str.lower)

		return data_list

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