# Diary_Slim.py

class Diary_Slim():
	def __init__(self):
		self.Define_Basic_Variables()

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.Define_Texts()

		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()

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

		self.text_header_prototype = "- Diário Slim, {} -"
		self.day_of_of_text = "Dia {} de {} de {}"
		self.today_is_text_header_prototype = "Hoje é {}, " + self.day_of_of_text + "."

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
						"Days": 30
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
					"Year": 0,
					"Month": 0,
					"Days": 0,
					"Diary Slims": 0
				},
				"Names": {},
				"Formats": {},
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

	def Define_Folders_And_Files(self):
		from copy import deepcopy

		# If there is no current year variable inside the self object, get the current year variable from the "Years" module
		if hasattr(self, "current_year") == False:
			self.current_year = {
				"Number": str(self.date["Units"]["Year"])
			}

		# Folders
		self.folders["diary_slim"] = self.folders["mega"]["notepad"]["effort"]["diary_slim"]

		# Subfolders
		names = [
			"Data",
			"Story",
			"Years"
		]

		for name in names:
			key = name.lower().replace(" ", "_")

			if name == "Years":
				name = self.Date.language_texts[name.lower() + ", title()"]

			self.folders["diary_slim"][key] = {
				"root": self.folders["diary_slim"]["root"] + name + "/"
			}

			self.Folder.Create(self.folders["diary_slim"][key]["root"])

		# Data folders
		names = [
			"State texts"
		]

		for name in names:
			key = name.lower().replace(" ", "_")

			self.folders["diary_slim"]["data"][key] = {
				"root": self.folders["diary_slim"]["data"]["root"] + name + "/"
			}

			self.Folder.Create(self.folders["diary_slim"]["data"][key]["root"])

		# Year files
		names = [
			"History"
		]

		for name in names:
			key = name.lower().replace(" ", "_")

			self.folders["diary_slim"]["years"][key] = self.folders["diary_slim"]["years"]["root"] + name + ".json"
			self.File.Create(self.folders["diary_slim"]["years"][key])

		# Years folders
		self.history = {
			"Numbers": {
				"Years": 0,
				"Diary Slims": 0
			},
			"Years": []
		}

		if self.File.Contents(self.folders["diary_slim"]["years"]["history"])["lines"] != [] and self.JSON.To_Python(self.folders["diary_slim"]["years"]["history"])["Years"] != []:
			# Get the History dictionary from the file
			self.history = self.JSON.To_Python(self.folders["diary_slim"]["years"]["history"])

		# If the current year is not inside the "History" years list, add it to the list
		if self.current_year["Number"] not in self.history["Years"]:
			self.history["Years"].append(self.current_year["Number"])

		self.years = self.Date.Create_Years_List(start = 2020, function = str)

		diary_slims = 0

		# Iterate through the Years list
		for year in self.years:
			# Create the year folder
			self.folders["diary_slim"]["years"][year] = {
				"root": self.folders["diary_slim"]["years"]["root"] + year + "/"
			}

			self.Folder.Create(self.folders["diary_slim"]["years"][year]["root"])

			# Create the year file
			self.folders["diary_slim"]["years"][year]["year"] = self.folders["diary_slim"]["years"][year]["root"] + "Year.json"
			self.File.Create(self.folders["diary_slim"]["years"][year]["year"])

			# If the file exists and it is not empty
			if self.File.Contents(self.folders["diary_slim"]["years"][year]["year"])["lines"] != []:
				# Add the days number to the local number of Diary Slims
				diary_slims += self.JSON.To_Python(self.folders["diary_slim"]["years"][year]["year"])["Numbers"]["Days"]

			# Add the year to the Years list if it is not inside it
			if year not in self.history["Years"]:
				self.history["Years"].append(year)

		# Sort the Years list
		self.history["Years"] = sorted(self.history["Years"], key = str.lower)

		# Update the number of years with the length of the years list
		self.history["Numbers"]["Years"] = len(self.history["Years"])

		# Define the number of Diary Slims of all years as the local number of Diary Slims
		self.history["Numbers"]["Diary Slims"] = diary_slims

		# Update the "History.json" file with the new History dictionary
		self.JSON.Edit(self.folders["diary_slim"]["years"]["history"], self.history)

		# Current year folder
		self.folders["diary_slim"]["current_year"] = self.folders["diary_slim"]["years"][self.current_year["Number"]]

		# Define the Year dictionary
		self.current_year["Year"] = deepcopy(self.templates["Year"])

		if self.File.Contents(self.folders["diary_slim"]["current_year"]["year"])["lines"] != []:
			self.current_year["Year"] = self.JSON.To_Python(self.folders["diary_slim"]["current_year"]["year"])

		# Define the year Month dictionary
		self.current_year["Month"] = {
			"Name": str(self.Text.Add_Leading_Zeroes(self.date["Units"]["Month"])) + " - " + self.date["Texts"]["Month name"][self.user_language],
			"Folder": "",
			"File": "",
			"Dictionary": {}
		}

		self.current_year["Month"]["Folder"] = self.folders["diary_slim"]["current_year"]["root"] + self.current_year["Month"]["Name"] + "/"
		self.current_year["Month"]["File"] = self.current_year["Month"]["Folder"] + "Month.json"
		self.current_year["Month"]["Dictionary"] = deepcopy(self.templates["Month"])

		if self.File.Contents(self.current_year["Month"]["File"])["lines"] != []:
			self.current_year["Month"]["Dictionary"] = self.JSON.To_Python(self.current_year["Month"]["File"])

		self.current_month = self.current_year["Month"]

		self.current_year["File"] = self.Current_Diary_Slim()["File"]

		# Files
		self.folders["diary_slim"]["data"]["slim_texts"] = self.folders["diary_slim"]["data"]["root"] + "Slim texts.json"
		self.File.Create(self.folders["diary_slim"]["data"]["slim_texts"])

		# Data files
		names = [
			"Things to do",
			"Things done texts"
		]

		for name in names:
			key = name.lower().replace(" ", "_")

			self.folders["diary_slim"]["data"][key] = self.folders["diary_slim"]["data"]["root"] + name + ".txt"
			self.File.Create(self.folders["diary_slim"]["data"][key])

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
				"current",
			],
			"names": [],
			"folders": self.Folder.Contents(self.folders["diary_slim"]["data"]["state_texts"]["root"]),
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
			if state == selected_state or state == None or selected_state == None:
				self.File.Edit(current_state_file, new_order, "w")

	def Current_Diary_Slim(self, current_year = None, date = None):
		if current_year == None:
			current_year = self.current_year

		if date == None:
			date = self.date

		dictionary = {}

		# Define the month folder name
		dictionary["Month folder name"] = str(self.Text.Add_Leading_Zeroes(date["Timezone"]["DateTime"]["Units"]["Month"])) + " - " + date["Timezone"]["DateTime"]["Texts"]["Month name"][self.user_language]

		# Define the current day
		dictionary["Day"] = "{} {}, {}".format(self.Text.Add_Leading_Zeroes(date["Timezone"]["DateTime"]["Units"]["Day"]), date["Timezone"]["DateTime"]["Texts"]["Day name"][self.user_language], date["Timezone"]["DateTime"]["Formats"]["DD-MM-YYYY"])

		# Define the year and month folder
		dictionary["Year folder"] = self.folders["diary_slim"]["years"]["root"] + current_year["Number"] + "/"
		dictionary["Month folder"] = dictionary["Year folder"] + dictionary["Month folder name"] + "/"

		# Define the Diary Slim file
		dictionary["File"] = dictionary["Month folder"] + dictionary["Day"] + ".txt"

		return dictionary