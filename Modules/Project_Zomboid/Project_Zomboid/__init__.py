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

		# Update the cities and survivors dictionaries
		self.Update_The_Dictionaries()

	def Define_Basic_Variables(self):
		from copy import deepcopy

		# Import the JSON module
		from Utility.JSON import JSON as JSON

		self.JSON = JSON()

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

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
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

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
			"Cities",
			"Survivors"
		]

		# Iterate through the list of folders
		for key in folders:
			# Define the text key
			text_key = key.lower() + ", title()"

			# Define the folder name
			name = self.Language.language_texts[text_key]

			# Define and create the folder
			self.project_zomboid["Folders"][key] = {
				"root": self.project_zomboid["Folders"]["root"] + name + "/"
			}

			self.Folder.Create(self.project_zomboid["Folders"][key]["root"])

		# Define and create the "Cities.json" file inside the "Cities" folder
		self.project_zomboid["Folders"]["Cities"]["Cities"] = self.project_zomboid["Folders"]["Cities"]["root"] + "Cities.json"
		self.File.Create(self.project_zomboid["Folders"]["Cities"]["Cities"])

		# ---------- #

		# Create the "Survivors" sub-folders
		folders = [
			"Deceased"
		]

		# Iterate through the list of folders
		for key in folders:
			# Define the text key
			text_key = key.lower() + ", title()"

			# Define the folder name
			name = self.Language.language_texts[text_key]

			# Define and create the folder
			self.project_zomboid["Folders"]["Survivors"][key] = {
				"root": self.project_zomboid["Folders"]["Survivors"]["root"] + name + "/"
			}

			self.Folder.Create(self.project_zomboid["Folders"]["Survivors"][key]["root"])

		# Define and create the "Survivors.json" file inside the "Survivors" folder
		self.project_zomboid["Folders"]["Survivors"]["Survivors"] = self.project_zomboid["Folders"]["Survivors"]["root"] + "Survivors.json"
		self.File.Create(self.project_zomboid["Folders"]["Survivors"]["Survivors"])

		# Define and create the "Pre-defined values.json" file
		self.project_zomboid["Folders"]["Pre-defined values"] = self.project_zomboid["Folders"]["root"] + "Pre-defined values.json"
		self.File.Create(self.project_zomboid["Folders"]["Pre-defined values"])

		# Define the default pre-defined values dictionary
		self.project_zomboid["Pre-defined values"] = {
			"Survivor": ""
		}

		file = self.project_zomboid["Folders"]["Pre-defined values"]

		# If the file is not empty
		if self.File.Contents(file)["lines"] != []:
			# Read the pre-defined values file
			self.project_zomboid["Pre-defined values"] = self.JSON.To_Python(self.project_zomboid["Folders"]["Pre-defined values"])

		# Write the default or updated "Pre-defined values" dictionary into the "Pre-defined values.json" file
		self.JSON.Edit(self.project_zomboid["Folders"]["Pre-defined values"], self.project_zomboid["Pre-defined values"])

	def Define_The_Cities(self):
		# Define the "Cities" dictionary
		self.project_zomboid["Cities"] = {
			"Numbers": {
				"Total": 0
			},
			"List": [],
			"Dictionary": {},
			"State": "Kentucky"
		}

		# Get the list of cities
		folder = self.project_zomboid["Folders"]["Cities"]["root"]

		self.project_zomboid["Cities"]["List"] = self.Folder.Contents(folder)["folder"]["names"]

		# Sort the list of cities
		self.project_zomboid["Cities"]["List"] = sorted(self.project_zomboid["Cities"]["List"], key = str.lower)

		# Update the number of cities
		self.project_zomboid["Cities"]["Numbers"]["Total"] = len(self.project_zomboid["Cities"]["List"])

		# Iterate through the list of city names
		for city in self.project_zomboid["Cities"]["List"]:
			# Define the empty dictionary
			dictionary = {
				"Name": city,
				"Locality": {},
				"Folders": {},
				"Numbers": {
					"Survivors": 0
				},
				"Survivors": []
			}

			# Define the city "Folders" dictionary
			dictionary["Folders"] = {
				"root": self.project_zomboid["Folders"]["Cities"]["root"] + city + "/"
			}

			self.Folder.Create(dictionary["Folders"]["root"])

			# Define and create the "City.json" file
			dictionary["Folders"]["City"] = dictionary["Folders"]["root"] + "City.json"
			self.File.Create(dictionary["Folders"]["City"])

			# Define the full locality of the city for each language
			# 
			# Format:
			# [City] - [State] - [Country]
			for language in self.languages["small"]:
				dictionary["Locality"][language] = city + " - " + self.project_zomboid["Cities"]["State"] + " - " + self.Language.texts["united_states"][language]

			# Add the local "City" dictionary to the root "Cities" dictionary
			self.project_zomboid["Cities"]["Dictionary"][city] = dictionary

	def Select_City(self):
		# Define the parameters dictionary for the "Select" method of the "Input" class
		parameters = {
			"options": self.project_zomboid["Cities"]["List"],
			"show_text": self.Language.language_texts["cities, title()"],
			"select_text": self.Language.language_texts["city, title()"]
		}

		# Ask the user to select a city from the list
		city = self.Input.Select(**parameters)["option"]

		# Get the city from the "Cities" dictionary
		city = self.project_zomboid["Cities"]["Dictionary"][city]

		# Return the city
		return city

	def Create_The_Survivor_Dictionaries(self):
		# Define the local "Survivors" dictionary
		dictionary = {
			"Numbers": {
				"Total": 0,
				"Deceased": 0
			},
			"List": [],
			"Deceased": [],
			"Dictionary": {}
		}

		# Get the list of survivors
		folder = self.project_zomboid["Folders"]["Survivors"]["root"]

		dictionary["List"] = self.Folder.Contents(folder)["folder"]["names"]

		# Remove the "Deceased" folder
		deceased = self.Language.language_texts["deceased, title()"]

		dictionary["List"].remove(deceased)

		# Get the number of survivors
		dictionary["Numbers"]["Total"] = len(dictionary["List"])

		# ---------- #

		# Get the list of deceased survivors
		folder = self.project_zomboid["Folders"]["Survivors"]["Deceased"]["root"]

		dictionary["Deceased"] = self.Folder.Contents(folder)["folder"]["names"]

		# Get the number of deceased survivors
		dictionary["Numbers"]["Deceased"] = len(dictionary["Deceased"])

		# Update the total number of survivors
		dictionary["Numbers"]["Total"] += dictionary["Numbers"]["Deceased"]

		# ---------- #

		# Create the local list of survivors
		survivors = dictionary["List"] + dictionary["Deceased"]

		# Iterate through the list of survivors
		for survivor in survivors:
			# Define the root folder
			root_folder = self.project_zomboid["Folders"]["Survivors"]

			# If the survivor is in the "Deceased survivors" list
			if survivor in dictionary["Deceased"]:
				# Define the root folder as the "Deceased" folder
				root_folder = self.project_zomboid["Folders"]["Survivors"]["Deceased"]

			# Create the local "Survivor" dictionary
			survivor = {
				"Name": survivor,
				"City": "",
				"Details": {
					"Gender": "",
					"Age": 27,
					"Date of birth": "01/01/1966"
				},
				"Folders": {
					"root": root_folder["root"] + survivor + "/",
					"Survivor": ""
				},
				"Diary": {
					"Numbers": {
						"Survival day": 0,
						"Day": 8,
						"Month": 7,
						"Year": 1993
					},
					"Folders": {}
				}
			}

			# Create the root folder
			self.Folder.Create(survivor["Folders"]["root"])

			# Define and create the "Survivor.json" file
			survivor["Folders"]["Survivor"] = survivor["Folders"]["root"] + "Survivor.json"
			self.File.Create(survivor["Folders"]["Survivor"])

			# If the "Survivor.json" file is not empty
			if self.File.Contents(survivor["Folders"]["Survivor"])["lines"] != []:
				# Read the "Survivor.json" file to get the local dictionary
				local_dictionary = self.JSON.To_Python(survivor["Folders"]["Survivor"])

				# Update the keys of the root "Survivor" dictionary
				for key, value in local_dictionary.items():
					survivor[key] = value

			# ---------- #

			# Define and create the "Diary" folder
			name = self.Language.language_texts["diary, title()"]

			survivor["Diary"]["Folders"] = {
				"root": survivor["Folders"]["root"] + name + "/"
			}

			self.Folder.Create(survivor["Diary"]["Folders"]["root"])

			# ---------- #

			# Define some variables for easier typing
			numbers = survivor["Diary"]["Numbers"]

			year = str(numbers["Year"])
			month = str(self.Text.Add_Leading_Zeroes(numbers["Month"]))
			day = str(numbers["Day"])

			# Define the "Date" dictionary
			date = self.Date.From_String(day + "/" + month + "/" + year, format = "%d/%m/%Y")

			# Define and create the year folder
			survivor["Diary"]["Folders"]["Year"] = {
				"root": survivor["Diary"]["Folders"]["root"] + year + "/"
			}

			self.Folder.Create(survivor["Diary"]["Folders"]["Year"]["root"])

			# Get the month name with number in the user language
			month_name_with_number = date["Texts"]["Month name with number"][self.user_language]

			# Define and create the month folder
			survivor["Diary"]["Folders"]["Year"]["Month"] = {
				"root": survivor["Diary"]["Folders"]["Year"]["root"] + month_name_with_number + "/"
			}

			self.Folder.Create(survivor["Diary"]["Folders"]["Year"]["Month"]["root"])

			# Make a shortcut to the month folder
			survivor["Diary"]["Folders"]["Month"] = survivor["Diary"]["Folders"]["Year"]["Month"]

			# ---------- #

			# Add the local "Survivor" dictionary to the root "Survivors" dictionary
			dictionary["Dictionary"][survivor["Name"]] = survivor

			# ---------- #

			# Define the "city" variable with the city of the survivor
			city = survivor["City"]

			# Get the "City" dictionary of the city of the survivor
			city = self.project_zomboid["Cities"]["Dictionary"][city]

			# Add the survivor to the "Survivors" list of the city
			city["Survivors"].append(survivor["Name"])

			# Update the number of survivors in the city
			city["Numbers"]["Survivors"] = len(city["Survivors"])

		# Define the root "Survivors" dictionary as the local dictionary
		self.project_zomboid["Survivors"] = dictionary

	def Update_The_Dictionaries(self):
		# Define the local "Types" dictionary
		types = {
			"Survivor": "Survivors",
			"City": "Cities"
		}

		# Iterate through the list of dictionary types
		for type_, key in types.items():
			# Create a local copy of the dictionary type from the root "Project Zomboid" dictionary
			local_dictionary = deepcopy(self.project_zomboid[key])

			# Define the list of items as a copy as the root list
			list_ = deepcopy(local_dictionary["List"])

			# If the dictionary type is "Survivor"
			if type_ == "Survivor":
				# Update the local list of items to add the deceased survivors
				list_ = local_dictionary["List"] + local_dictionary["Deceased"]

			# Iterate through the list of items
			for item in list_:
				# Get the dictionary of the item
				item = local_dictionary["Dictionary"][item]

				# Update the dictionary of the item and its file
				self.Update_Dictionary(item, copy = False)

				# If the dictionary type is "Survivor"
				# And the survivor is a deceased survivor
				if (
					type_ == "Survivor" and
					item["Name"] in local_dictionary["Deceased"]
				):
					# Remove the survivor dictionary from the "Dictionary" key
					local_dictionary["Dictionary"].pop(item["Name"])

			# Sort the root list of items
			local_dictionary["List"] = sorted(local_dictionary["List"], key = str.lower)

			# If the dictionary type is "Survivor"
			if type_ == "Survivor":
				# Sort the root list of deceased survivors
				local_dictionary["Deceased"] = sorted(local_dictionary["Deceased"], key = str.lower)

			# If the dictionary type is "City"
			if type_ == "City":
				# Remove the "State" key
				local_dictionary.pop("State")

			# Update the JSON file with the updated local dictionary
			self.JSON.Edit(self.project_zomboid["Folders"][key][key], local_dictionary)

	def Update_Dictionary(self, dictionary, copy = True):
		# Define the default dictionary type as "Survivor"
		type_ = "Survivor"

		# If the name inside the dictionary is inside the list of cities
		if dictionary["Name"] in self.project_zomboid["Cities"]["List"]:
			type_ = "City"

		# If the "copy" parameter is True
		if copy == True:
			# Make a local copy of the dictionary to not modify it by reference (modifying the original dictionary)
			dictionary = deepcopy(dictionary)

		# Get the dictionary JSON file before the "Folders" key is removed
		json_file = dictionary["Folders"][type_]

		# Remove the "Folders" key from the current dictionary
		dictionary.pop("Folders")

		# If the dictionary type is "Survivor"
		if type_ == "Survivor":
			# Remove the "Folders" key from the "Diary" dictionary
			dictionary["Diary"].pop("Folders")

		# If the dictionary type is "City"
		if type_ == "City":
			# Sort the list of survivors
			dictionary["Survivors"] = sorted(dictionary["Survivors"], key = str.lower)

		# Update the dictionary JSON file with the updated dictionary
		self.JSON.Edit(json_file, dictionary)

	def Define_Date_Dictionary(self, dictionary):
		# Define the "diary" variable
		diary = dictionary["Survivor"]["Diary"]

		# Define the "Date" dictionary
		day = str(diary["Numbers"]["Day"])
		month = str(self.Text.Add_Leading_Zeroes(diary["Numbers"]["Month"]))
		year = str(diary["Numbers"]["Year"])

		dictionary["Date"] = self.Date.From_String(day + "/" + month + "/" + year, format = "%d/%m/%Y")

		return dictionary

	def Verify_Diary_Date(self, dictionary):
		# Define the "diary" variable
		diary = dictionary["Survivor"]["Diary"]

		# If the current month is the last month
		if diary["Numbers"]["Month"] == 12:
			# Add one to the year number
			diary["Numbers"]["Year"] += 1

			# Reset the month number to one
			diary["Numbers"]["Month"] = 1

			# Define and create the year folder
			diary["Folders"]["Year"] = {
				"root": diary["Folders"]["root"] + str(diary["Numbers"]["Year"]) + "/"
			}

			self.Folder.Create(diary["Folders"]["Year"]["root"])

		# If the current month is not the last month
		else:
			# Add one to the month number
			diary["Numbers"]["Month"] += 1

		# Reset the day number to one
		diary["Numbers"]["Day"] = 1

		# Re-define the "Date" dictionary
		self.dictionary = self.Define_Date_Dictionary(self.dictionary)

		# Get the month name with number in the user language
		month_name_with_number = self.dictionary["Date"]["Texts"]["Month name with number"][self.user_language]

		# Define and create the month folder
		diary["Folders"]["Year"]["Month"] = {
			"root": diary["Folders"]["Year"]["root"] + month_name_with_number + "/"
		}

		self.Folder.Create(diary["Folders"]["Year"]["Month"]["root"])

		# Make a shortcut to the month folder
		diary["Folders"]["Month"] = diary["Folders"]["Year"]["Month"]

		# Return the dictionary
		return dictionary