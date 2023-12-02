# Diary_Slim.py

class Diary_Slim():
	def __init__(self):
		# Define the module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Folders, files, lists, and dictionaries methods
		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()

		# Class methods
		self.Define_History()
		self.Define_Story_Information()
		self.Define_Templates()
		self.Define_Current_Year()
		self.Define_Slim_Texts()

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
			"JSON",
			"Language"
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

		self.large_bar = "-----"
		self.dash_space = "-"

	def Define_Folders_And_Files(self):
		# If there is no current year variable inside the self object, get the current year variable from the "Years" module
		if hasattr(self, "current_year") == False:
			self.current_year = {
				"Number": str(self.date["Units"]["Year"])
			}

		# Folders
		self.folders["Diary Slim"] = self.folders["Notepad"]["Diary Slim"]

		# Subfolders
		names = [
			"Data",
			"Story",
			"Years"
		]

		for name in names:
			key = name

			if name == "Years":
				name = self.Date.language_texts[name.lower() + ", title()"]

			self.folders["Diary Slim"][key] = {
				"root": self.folders["Diary Slim"]["root"] + name + "/"
			}

			self.Folder.Create(self.folders["Diary Slim"][key]["root"])

		# Data folders
		names = [
			"State texts"
		]

		for name in names:
			self.folders["Diary Slim"]["Data"][name] = {
				"root": self.folders["Diary Slim"]["Data"]["root"] + name + "/"
			}

			self.Folder.Create(self.folders["Diary Slim"]["Data"][name]["root"])

		# Years folders and files
		names = [
			"History"
		]

		for name in names:
			self.folders["Diary Slim"]["Years"][name] = self.folders["Diary Slim"]["Years"]["root"] + name + ".json"
			self.File.Create(self.folders["Diary Slim"]["Years"][name])

		# ---------- #

		# Slim texts folder
		self.folders["Diary Slim"]["Data"]["Slim texts"] = {
			"root": self.folders["Diary Slim"]["Data"]["root"] + "Slim texts/"
		}

		self.Folder.Create(self.folders["Diary Slim"]["Data"]["Slim texts"]["root"])

		# Slim texts file
		self.folders["Diary Slim"]["Data"]["Slim texts"]["Texts"] = self.folders["Diary Slim"]["Data"]["Slim texts"]["root"] + "Texts.json"
		self.File.Create(self.folders["Diary Slim"]["Data"]["Slim texts"]["Texts"])

		# ---------- #

		# Data files
		names = [
			"Things to do",
			"Things done texts"
		]

		for name in names:
			key = name.lower().replace(" ", "_")

			self.folders["Diary Slim"]["Data"][key] = self.folders["Diary Slim"]["Data"]["root"] + name + ".txt"
			self.File.Create(self.folders["Diary Slim"]["Data"][key])

		self.folders["apps"]["module_files"][self.module["key"]]["header"] = self.folders["apps"]["module_files"][self.module["key"]]["root"] + "Header.txt"
		self.File.Create(self.folders["apps"]["module_files"][self.module["key"]]["header"])

	def Define_Lists_And_Dictionaries(self):
		# Lists
		self.diary_slim_header = self.File.Contents(self.folders["apps"]["module_files"][self.module["key"]]["header"])["string"]

		# Dictionaries
		self.states = {
			"order_names": [
				"first",
				"second",
				"current"
			],
			"names": [],
			"folders": self.Folder.Contents(self.folders["Diary Slim"]["Data"]["State texts"]["root"])
		}

		i = 0
		for state in self.states["folders"]["folder"]["names"]:
			# Read state names
			names = self.JSON.To_Python(self.states["folders"]["folder"]["list"][i] + "Names.json")
			state = names[self.user_language]

			# Add state name to names list
			self.states["names"].append(state)

			# Create state dictionary and sub-keys
			self.states[state] = {}
			self.states[state]["files"] = {}
			self.states[state]["texts"] = {}

			# Add state names file and dictionary
			self.states[state]["files"]["names"] = self.states["folders"]["folder"]["list"][i] + "Names.json"
			self.states[state]["names"] = names

			# List orders of state, add file and list or dictionary to order dictionary
			for order_name in self.states["order_names"]:
				self.states[state]["files"][order_name] = self.states["folders"]["folder"]["list"][i] + order_name.capitalize() + "."

				if order_name == "current":
					self.states[state]["files"][order_name] += "txt"
					function = self.File.Contents

				if order_name != "current":
					self.states[state]["files"][order_name] += "json"
					function = self.JSON.To_Python

				self.states[state]["texts"][order_name] = function(self.states[state]["files"][order_name])

				if order_name == "current":
					self.states[state]["texts"][order_name] = self.states[state]["texts"][order_name]["lines"]

			i += 1

	def Define_History(self):
		# Define the default History dictionary
		self.history = {
			"Numbers": {
				"Years": 0,
				"Months": 0,
				"Diary Slims": 0
			},
			"Years": []
		}

		# If the "History.json" file is not empty
		# And the "Years" list is not empty
		if (
			self.File.Contents(self.folders["Diary Slim"]["Years"]["History"])["lines"] != [] and
			self.JSON.To_Python(self.folders["Diary Slim"]["Years"]["History"])["Years"] != []
		):
			# Get the filled History dictionary from the file
			self.history = self.JSON.To_Python(self.folders["Diary Slim"]["Years"]["History"])

		self.years = self.Date.Create_Years_List(start = 2020, function = str)

		# If the Years list inside the History is empty, create a new one
		if self.history["Years"] == []:
			self.history["Years"] = self.years

		# If the current year is not inside the "History" years list, add it to the list
		if self.current_year["Number"] not in self.history["Years"]:
			self.history["Years"].append(self.current_year["Number"])

		# Sort the Years list
		self.history["Years"] = sorted(self.history["Years"], key = str.lower)

		# Define the default numbers dictionary
		numbers = {
			"Years": len(self.years),
			"Months": 0,
			"Days": 0,
			"Diary Slims": 0
		}

		# Iterate through the Years list
		for year in self.years:
			# Create the year folder
			self.folders["Diary Slim"]["Years"][year] = {
				"root": self.folders["Diary Slim"]["Years"]["root"] + year + "/"
			}

			self.Folder.Create(self.folders["Diary Slim"]["Years"][year]["root"])

			# Create the year file
			self.folders["Diary Slim"]["Years"][year]["year"] = self.folders["Diary Slim"]["Years"][year]["root"] + "Year.json"
			self.File.Create(self.folders["Diary Slim"]["Years"][year]["year"])

			# If the is not empty
			if self.File.Contents(self.folders["Diary Slim"]["Years"][year]["year"])["lines"] != []:
				# Get the Year dictionary
				year_dictionary = self.JSON.To_Python(self.folders["Diary Slim"]["Years"][year]["year"])

				# Iterate through the number keys
				for key in numbers.keys():
					# If the key is not equal to "Years"
					if key != "Years":
						# Add the current number to the local numbers dictionary
						numbers[key] += year_dictionary["Numbers"][key]

		# Define the History numbers dictionary as the local numbers dictionary
		self.history["Numbers"] = numbers

		# Update the "History.json" file with the updated History dictionary
		self.JSON.Edit(self.folders["Diary Slim"]["Years"]["History"], self.history)

	def Define_Story_Information(self):
		# Story folders and files
		names = [
			"Information",
			"Titles"
		]

		for name in names:
			self.folders["Diary Slim"]["Story"][name] = self.folders["Diary Slim"]["Story"]["root"] + name + ".json"
			self.File.Create(self.folders["Diary Slim"]["Story"][name])

		# Define the default Story Information dictionary
		self.information = {
			"Titles": {},
			"Chapters": {
				"Number": 0
			},
			"Status": {
				"Number": 0,
				"Names": self.JSON.Language.language_texts["writing, title()"]
			},
			"HEX color": "f1858d"
		}

		# If the "Information.json" file is not empty
		if self.File.Contents(self.folders["Diary Slim"]["Story"]["Information"])["lines"] != []:
			# Get the filled Information dictionary from the file
			self.information = self.JSON.To_Python(self.folders["Diary Slim"]["Story"]["Information"])

		# If the Titles dictionary is empty
		if self.information["Titles"] == {}:
			# Get the Titles dictionary from the "Titles.json" file
			self.information["Titles"] = self.JSON.To_Python(self.folders["Diary Slim"]["Story"]["Titles"])

		# If the number of chapters is 0 (zero)
		if self.information["Chapters"]["Number"] == 0:
			# Define the number of chapters as the number of Diary Slims
			self.information["Chapters"]["Number"] = self.history["Numbers"]["Diary Slims"]

		# Update the "Information.json" file with the updated Information dictionary
		self.JSON.Edit(self.folders["Diary Slim"]["Story"]["Information"], self.information)

	def Define_Templates(self):
		self.template = {
			"Numbers": {
				"Months": 12,
				"Days": 152
			},
			"Months": {
				"06 - Junho": {
					"Numbers": {
						"Year": 2023,
						"Month": 6,
						"Days": 30,
						"Diary Slims": 0
					},
					"Names": {
						"pt": "Junho",
						"en": "June"
					},
					"Formats": {
						"Diary Slim": "06 - Junho"
					},
					"Diary Slims": {
						"02 Sexta-Feira, 02-06-2023": {
							"Day": 2,
							"Names": {
								"pt": "Sexta-Feira",
								"en": "Friday"
							},
							"Formats": {
								"DD-MM-YYYY": "02-06-2023"
							},
							"Creation time": {
								"HH:MM": "08:27",
								"Hours": 8,
								"Minutes": 27
							},
							"Data": {
								"Sleep times": {
									"Slept": "23:55",
									"Woke up": "08:25"
								}
							}
						}
					}
				}
			}
		}

		self.templates = {
			"Year": {
				"Numbers": {
					"Year": 0,
					"Months": 0,
					"Days": 0,
					"Diary Slims": 0
				},
				"Months": {}
			},
			"Month": {
				"Numbers": {
					"Year": self.date["Units"]["Year"],
					"Month": self.date["Units"]["Month"],
					"Days": self.date["Units"]["Month days"],
					"Diary Slims": 0
				},
				"Names": self.date["Texts"]["Month name"],
				"Formats": {
					"Diary Slim": self.date["Texts"]["Month name with number"][self.user_language]
				},
				"Diary Slims": {}
			},
			"Day": {
				"Day": 0,
				"Names": {},
				"Formats": {
					"DD-MM-YYYY": ""
				},
				"Creation time": {
					"HH:MM": "",
					"Hours": 0,
					"Minutes": 0
				},
				"Data": {
					"Sleep times": {}
				}
			}
		}

	def Define_Current_Year(self):
		from copy import deepcopy

		# Current year folder
		self.folders["Diary Slim"]["current_year"] = self.folders["Diary Slim"]["Years"][self.current_year["Number"]]

		# Define the Year dictionary
		self.current_year["Year"] = deepcopy(self.templates["Year"])

		if self.File.Contents(self.folders["Diary Slim"]["current_year"]["year"])["lines"] != []:
			self.current_year["Year"] = self.JSON.To_Python(self.folders["Diary Slim"]["current_year"]["year"])

		# Define the year Month dictionary
		self.current_year["Month"] = {
			"Name": self.date["Texts"]["Month name with number"][self.user_language],
			"Folder": "",
			"File": "",
			"Dictionary": {}
		}

		# Define and create the month folder
		self.current_year["Month"]["Folder"] = self.folders["Diary Slim"]["current_year"]["root"] + self.current_year["Month"]["Name"] + "/"
		self.Folder.Create(self.current_year["Month"]["Folder"])

		# Define and create the month file
		self.current_year["Month"]["File"] = self.current_year["Month"]["Folder"] + "Month.json"
		self.File.Create(self.current_year["Month"]["File"])

		self.current_year["Month"]["Month"] = deepcopy(self.templates["Month"])

		if self.File.Contents(self.current_year["Month"]["File"])["lines"] != []:
			self.current_year["Month"]["Month"] = self.JSON.To_Python(self.current_year["Month"]["File"])

		self.current_month = self.current_year["Month"]

		self.current_year["File"] = self.Current_Diary_Slim()["File"]

	def Define_Slim_Texts(self):
		# Define the default Slim texts dictionary
		self.slim_texts = {
			"List": [],
			"Dictionary": {}
		}

		file = self.folders["Diary Slim"]["Data"]["Slim texts"]["Texts"]

		# Read the Slim "Texts.json" file if it is not empty
		if self.File.Contents(file)["lines"] != []:
			self.slim_texts = self.JSON.To_Python(file)

		contents = self.Folder.Contents(self.folders["Diary Slim"]["Data"]["Slim texts"]["root"])

		# Get the Slim text folders
		folders = contents["folder"]["dictionary"]

		# Define the Slim texts list
		self.slim_texts["List"] = contents["folder"]["names"]

		# Iterate through the Slim text folders
		for text, folder in folders.items():
			# Create the Slim text dictionary
			dictionary = {
				"Key": text,
				"Folders": {},
				"Files": {},
				"Texts": {}
			}

			# Define the Slim root folder
			dictionary["Folders"]["root"] = folder

			# Define the Slim data file
			file = dictionary["Folders"]["root"] + "Data.json"

			if self.File.Exist(file) == True:
				dictionary["Files"]["Data"] = file
				self.File.Create(dictionary["Files"]["Data"])

			# Define the Slim language text files
			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				# Define and create the language text file
				dictionary["Files"][language] = dictionary["Folders"]["root"] + full_language + ".txt"
				self.File.Create(dictionary["Files"][language])

				# Read the language text file
				dictionary["Texts"][language] = self.File.Contents(dictionary["Files"][language])["string"]

			# Read the "Data.json" file if it exists
			if "Data" in dictionary["Files"]:
				dictionary.update(self.JSON.To_Python(dictionary["Files"]["Data"]))

			self.slim_texts["Dictionary"][text] = dictionary

		# Update the Slim "Texts.json" file with the updated Slim texts dictionary
		self.JSON.Edit(self.folders["Diary Slim"]["Data"]["Slim texts"]["Texts"], self.slim_texts)

	def Update_State(self, selected_state = None, new_order = ""):
		for state in self.states["names"]:
			state_texts = self.states[state]["texts"]

			# Define current state file
			current_state_file = self.states[state]["files"]["current"]
			string = self.File.Contents(current_state_file)["string"]

			# If new order is not empty, get the order from state_texts dictionary
			if new_order != "":
				new_order = state_texts[new_order][self.user_language]

			# Write the new order if the state is equal to the selected state
			# If the state is equal to none, or if the selected state is equal to none
			if (
				state == selected_state or
				state == None or
				selected_state == None
			):
				self.File.Edit(current_state_file, new_order, "w")

	def Current_Diary_Slim(self, current_year = None, date = None, current_diary_slim = True):
		if current_year == None:
			current_year = self.current_year

		if date == None:
			date = self.date

		# Get the Diary Slim dictionary
		dictionary = self.Make_Diary_Slim_Dictionary(current_year, date)

		# If the current Diary Slim file does not exist
		# And the current Diary Slim needs to be retrieved
		if (
			self.File.Exist(dictionary["File"]) == False and
			current_diary_slim == True
		):
			# Get the most recent month and the most recent Diary Slim
			most_recent_month = list(self.current_year["Year"]["Months"].values())[-1]
			most_recent_diary_slim = list(most_recent_month["Diary Slims"].values())[-1]

			# Create the custom date of the most recent Diary Slim
			date = self.Date.From_String(most_recent_diary_slim["Formats"]["DD-MM-YYYY"], format = "%d-%m-%Y")

			# Get the Diary Slim dictionary of the last Diary Slim file
			dictionary = self.Make_Diary_Slim_Dictionary(current_year, date)

		return dictionary

	def Make_Diary_Slim_Dictionary(self, current_year, date):
		dictionary = {}

		datetime = date["Timezone"]["DateTime"]
		units = datetime["Units"]
		texts = datetime["Texts"]
		formats = datetime["Formats"]

		# Define the month folder name
		dictionary["Month folder name"] = texts["Month name with number"][self.user_language]

		# Define the current day
		items = [
			self.Text.Add_Leading_Zeroes(units["Day"]),
			texts["Day name"][self.user_language],
			formats["DD-MM-YYYY"]
		]

		dictionary["Day"] = "{} {}, {}".format(*items)

		# Define the year and month folder
		dictionary["Year folder"] = self.folders["Diary Slim"]["Years"]["root"] + current_year["Number"] + "/"
		dictionary["Month folder"] = dictionary["Year folder"] + dictionary["Month folder name"] + "/"

		# Define the Diary Slim file
		dictionary["File"] = dictionary["Month folder"] + dictionary["Day"] + ".txt"

		return dictionary