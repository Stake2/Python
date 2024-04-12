# Project_Zomboid.py

from copy import deepcopy

class Project_Zomboid(object):
	def __init__(self):
		# Define the module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Folders, files, lists, and dictionaries methods
		self.Define_Folders_And_Files()

		# Define the "Cities" dictionary
		self.Define_The_Cities()

		# Create the survivor dictionaries
		self.Create_The_Survivor_Dictionaries()

	def Define_Basic_Variables(self):
		from copy import deepcopy

		# Import the JSON module
		from Utility.JSON import JSON as JSON

		self.JSON = JSON()

		# Get the modules list
		self.modules = self.JSON.To_Python(self.folders["apps"]["modules"]["modules"])

		# Import the "importlib" module
		import importlib

		# Create a list of the modules that will not be imported
		remove_list = [
			"Define_Folders",
			"Language",
			"JSON"
		]

		# Iterate through the Utility modules
		for module_title in self.modules["Utility"]["List"]:
			# If the module title is not inside the remove list
			if module_title not in remove_list:
				# Import the module
				module = importlib.import_module("." + module_title, "Utility")

				# Get the sub-class
				sub_class = getattr(module, module_title)

				# Add the sub-class to the current module
				setattr(self, module_title, sub_class())

		# Make a backup of the module folders
		self.module_folders = {}

		for item in ["modules", "module_files"]:
			self.module_folders[item] = deepcopy(self.folders["apps"][item][self.module["key"]])

		# Define the local folders dictionary as the Folder folders dictionary
		self.folders = self.Folder.folders

		# Restore the backup of the module folders
		for item in ["modules", "module_files"]:
			self.folders["apps"][item][self.module["key"]] = self.module_folders[item]

		# Get the switches dictionary from the "Global Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# Get the Languages dictionary
		self.languages = self.JSON.Language.languages

		# Get the user language and full user language
		self.user_language = self.JSON.Language.user_language
		self.full_user_language = self.JSON.Language.full_user_language

		# Get the Sanitize method of the File class
		self.Sanitize = self.File.Sanitize

		# Get the current date from the Date module
		self.date = self.Date.date

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.JSON.Language.Item(self.texts)

		# Define the "Separators" dictionary
		self.separators = {}

		# Create separators from one to ten characters
		for number in range(1, 11):
			# Define the empty string
			string = ""

			# Add separators to it
			while len(string) != number:
				string += "-"

			# Add the string to the Separators dictionary
			self.separators[str(number)] = string

	def Define_Folders_And_Files(self):
		# Define the root "Project Zomboid" dictionary
		self.project_zomboid = {
			"Folders": {
				"root": self.folders["Mega"]["Stories"]["Game Multiverse Bubble"]["root"] + "Project Zomboid/"
			}
		}

		# Create the root folder
		self.Folder.Create(self.project_zomboid["Folders"]["root"])

		# Create the sub-folders
		folders = [
			"Database",
			"Cities"
		]

		# Iterate through the list of folders
		for key in folders:
			# Define the text key
			text_key = key.lower() + ", title()"

			# Define the folder name
			name = self.JSON.Language.language_texts[text_key]

			# Define and create the folder
			self.project_zomboid["Folders"][key] = {
				"root": self.project_zomboid["Folders"]["root"] + name + "/"
			}

			self.Folder.Create(self.project_zomboid["Folders"][key]["root"])

		# Define and create the "Cities.json" file inside the "Cities" folder
		self.project_zomboid["Folders"]["Cities"]["Cities"] = self.project_zomboid["Folders"]["Cities"]["root"] + "Cities.json"
		self.File.Create(self.project_zomboid["Folders"]["Cities"]["Cities"])

		# Define and create the "Pre-defined values.json" file
		self.project_zomboid["Folders"]["Pre-defined values"] = self.project_zomboid["Folders"]["root"] + "Pre-defined values.json"
		self.File.Create(self.project_zomboid["Folders"]["Pre-defined values"])

		# Read the pre-defined values file
		self.project_zomboid["Pre-defined values"] = self.JSON.To_Python(self.project_zomboid["Folders"]["Pre-defined values"])

	def Define_The_Cities(self):
		# Define the "Cities" dictionary
		self.project_zomboid["Cities"] = {
			"Names": [
				"Muldraugh",
				"Riverside",
				"Rosewood",
				"West Point"
			],
			"Dictionary": {}
		}

		# Iterate through the list of city names
		for city in self.project_zomboid["Cities"]["Names"]:
			# Define the empty dictionary
			dictionary = {
				"Name": city
			}

			# Define the city "Folders" dictionary
			dictionary["Folders"] = {
				"root": self.project_zomboid["Folders"]["Cities"]["root"] + city + "/"
			}

			self.Folder.Create(dictionary["Folders"]["root"])

			# Define and create the "City.json" file
			dictionary["Folders"]["City"] = dictionary["Folders"]["root"] + "City.json"
			self.File.Create(dictionary["Folders"]["City"])

			# Add the local dictionary to the root "Cities" dictionary
			self.project_zomboid["Cities"]["Dictionary"][city] = dictionary

	def Create_The_Survivor_Dictionaries(self):
		# Iterate through the list of "City" dictionaries
		for name, dictionary in self.project_zomboid["Cities"]["Dictionary"].items():
			# Define the "Survivors" dictionary
			dictionary["Survivors"] = {
				"Numbers": {
					"Total": 0
				},
				"List": [],
				"Dictionary": {}
			}

			# Get the list of survivors
			dictionary["Survivors"]["List"] = self.Folder.Contents(dictionary["Folders"]["root"])["folder"]["names"]

			# Get the number of survivors
			dictionary["Survivors"]["Numbers"]["Total"] = len(dictionary["Survivors"]["List"])

			# Iterate through the list of survivors
			for survivor in dictionary["Survivors"]["List"]:
				survivor = {
					"Name": survivor,
					"Folders": {
						"root": dictionary["Folders"]["root"] + survivor + "/"
					},
					"Numbers": {
						"Files": 0
					},
					"Dates": {
						"Numbers": {
							"Day": 1,
							"Month": 1,
							"Year": 1993,
							"Survival day": 1,
						},
						"Folders": {}
					}
				}

				# Create the root folder
				self.Folder.Create(survivor["Folders"]["root"])

				# Define and create the "Survivor.json" file
				survivor["Folders"]["Survivor"] = survivor["Folders"]["root"] + "Survivor.json"
				self.File.Create(survivor["Folders"]["Survivor"])

				# If the survivor file is not empty
				if self.File.Contents(survivor["Folders"]["Survivor"])["lines"] != []:
					# Read the "Survivor.json" file to get the local dictionary
					local_dictionary = self.JSON.To_Python(survivor["Folders"]["Survivor"])

					# Update the "Numbers" and "Dates" dictionaries
					survivor["Numbers"] = local_dictionary["Numbers"]
					survivor["Dates"] = local_dictionary["Dates"]

				# ----- #

				# Define some variables for easier typing
				dates = survivor["Dates"]["Numbers"]

				year = str(dates["Year"])
				month = str(dates["Month"])
				day = str(dates["Day"])

				# Define and create the year folder
				if year not in survivor["Dates"]["Folders"]:
					survivor["Dates"]["Folders"][year] = {
						"root": survivor["Folders"]["root"] + year + "/"
					}

					self.Folder.Create(survivor["Dates"]["Folders"][year]["root"])

				# Define the date
				date = self.Date.From_String(str(1) + "/" + month + "/" + year)

				# Get the month name with number in the user language
				month_name_with_number = date["Texts"]["Month name with number"][self.user_language]

				# Define and create the month folder
				if month not in survivor["Dates"]["Folders"][year]:
					survivor["Dates"]["Folders"][year][month] = {
						"root": survivor["Dates"]["Folders"][year]["root"] + month_name_with_number + "/"
					}

				self.Folder.Create(survivor["Dates"]["Folders"][year][month]["root"])

				# Define the "Year" folder key
				survivor["Dates"]["Folders"]["Year"] = {
					"root": survivor["Dates"]["Folders"][year]["root"],
					"Month": deepcopy(survivor["Dates"]["Folders"][year][month])
				}

				# ----- #

				# Add the local "Survivor" dictionary to the root "Survivors" dictionary
				dictionary["Survivors"]["Dictionary"][survivor["Name"]] = survivor

				# Update the "Survivor.json" file with the new "Survivor" dictionary
				self.JSON.Edit(survivor["Folders"]["Survivor"], survivor)

			# Add the local dictionary to the root "Cities" dictionary
			self.project_zomboid["Cities"]["Dictionary"][name] = dictionary

			# Define the "City" dictionary and add the "Name" key and the "Survivors" list
			city = {
				"Name": dictionary["Name"],
				"Survivors": dictionary["Survivors"]
			}

			# Update the "City.json" file with the new "City" dictionary
			self.JSON.Edit(dictionary["Folders"]["City"], city)

		# Create a local copy of each "City" dictionary
		cities = deepcopy(self.project_zomboid["Cities"])

		# Iterate through the "Cities" dictionary
		for name in self.project_zomboid["Cities"]["Names"]:
			# Remove the "Folders" key
			cities["Dictionary"][name].pop("Folders")

		# Update the "Cities.json" file with the new local "Cities" dictionary
		self.JSON.Edit(self.project_zomboid["Folders"]["Cities"]["Cities"], cities)