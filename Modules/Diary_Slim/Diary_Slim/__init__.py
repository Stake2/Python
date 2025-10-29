# Diary_Slim.py

# Import the "importlib" module
import importlib

# Import the "collections" module
import collections

# Import the "deepcopy" module
from copy import deepcopy

class Diary_Slim():
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.folders = self.Define_Folders(object = self).folders

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Folders, files, lists, and dictionaries methods
		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()

		# Class methods

		# Define the template dictionaries
		self.Define_Templates()

		# Define the History of Diary Slim
		self.Define_History()

		# Define the story information and dictionary
		self.Define_Story_Information()

		# Define the current year dictionary
		self.Define_Current_Year()

		# Define the Diary Slim texts
		self.Define_Diary_Slim_Texts()

		# Define the statistics for the Diary Slim
		self.Define_Statistics()

	def Import_Classes(self):
		# Define the list of modules to be imported
		modules = [
			"Define_Folders",
			"JSON"
		]

		# Iterate through the list of modules
		for module_title in modules:
			# Import the module
			module = importlib.import_module("." + module_title, "Utility")

			# Get the sub-class
			sub_class = getattr(module, module_title)

			# If the module title is not "Define_Folders"
			if module_title != "Define_Folders":
				# Run the sub-class to define its variable
				sub_class = sub_class()

			# Add the sub-class to the current module
			setattr(self, module_title, sub_class)

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

	def Define_Basic_Variables(self):
		# Get the dictionary of modules
		self.modules = self.JSON.To_Python(self.folders["Apps"]["Modules"]["Modules"])

		# Create a list of the modules that will not be imported
		remove_list = [
			"Define_Folders",
			"Modules",
			"Language",
			"JSON"
		]

		# Iterate through the list of utility modules
		for module_title in self.modules["Utility"]["List"]:
			# If the module title is not inside the remove list
			if module_title not in remove_list:
				# Import the module
				module = importlib.import_module("." + module_title, "Utility")

				# Get the sub-class of the module
				sub_class = getattr(module, module_title)

				# Add the sub-class to the current class
				setattr(self, module_title, sub_class())

		# ---------- #

		# Get the switches dictionary from the "Global Switches" class
		self.switches = self.Global_Switches.switches["Global"]

		# ---------- #

		# Import some variables from the "Language" class

		# Import the "languages" dictionary
		self.languages = self.Language.languages

		# Import the "language" dictionary
		self.language = self.Language.language

		# Import the "separators" dictionary
		self.separators = self.Language.separators

		# ---------- #

		# Import the "folders" dictionary from the "Folder" class
		self.folders = self.Folder.folders

		# ---------- #

		# Import the "Sanitize" method from the "File" class
		self.Sanitize = self.File.Sanitize

		# ---------- #

		# Get the current date from the "Date" class
		self.date = self.Date.date

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

	def Define_Folders_And_Files(self):
		# Define the root "Diary Slim" dictionary
		self.diary_slim = {
			"Folders": {
				"root": self.folders["Notepad"]["Diary Slim"]["root"],
				"Image": {
					"root": self.folders["Image"]["Diary"]
				}
			}
		}

		# Add the current year to the dictionary if it is defined
		if hasattr(self, "current_year") == True:
			self.diary_slim["Current year"] = {
				"Number": self.current_year
			}

		# If there is no current year defined
		else:
			# Get the current year number from the "Date" module
			self.diary_slim["Current year"] = {
				"Number": str(self.date["Units"]["Year"])
			}

		# ---------- #

		# Define the sub-folders
		names = [
			"Data",
			"Story",
			"Years"
		]

		# Iterate through the names list
		for name in names:
			# Define the key
			key = name

			# Define the text key for the folder
			text_key = key.lower().replace(" ", "_")

			if "_" not in text_key:
				text_key += ", title()"

			# Define the folder name
			name = self.Language.language_texts[text_key]

			# Define the folder with its key and name
			self.diary_slim["Folders"][key] = {
				"root": self.diary_slim["Folders"]["root"] + name + "/"
			}

			# Create it
			self.Folder.Create(self.diary_slim["Folders"][key]["root"])

		# ---------- #

		# Define the "Data" sub-folders
		names = [
			"Header",
			"Texts",
			"External statistics"
		]

		# Define the folder for easier typing
		folder = self.diary_slim["Folders"]["Data"]

		# Iterate through the names list
		for name in names:
			# Define the key
			key = name

			# Define the text key for the folder
			text_key = key.lower().replace(" ", "_")

			if "_" not in text_key:
				text_key += ", title()"

			# Define the texts dictionary
			texts = self.Language.language_texts

			# If the text key is inside the texts dictionary of this class
			if text_key in self.language_texts:
				# Update the local texts dictionary to be that one
				texts = self.language_texts

			# Define the folder name
			name = texts[text_key]

			# Define the folder with its key and name
			folder[key] = {
				"root": folder["root"] + name + "/"
			}

			# Create it
			self.Folder.Create(folder[key]["root"])

		# ---------- #

		# Define the folder for easier typing
		folder = self.diary_slim["Folders"]["Data"]["Header"]

		# Define the "Header" files
		for language in self.languages["Small"]:
			# Get the full language
			full_language = self.languages["Full"][language]

			# Define the file
			folder[language] = folder["root"] + full_language + ".txt"

			# Create it
			self.File.Create(folder[language])

		# ---------- #

		# Define the Diary Slim "Texts" files
		names = [
			"Texts"
		]

		# Define the folder for easier typing
		folder = self.diary_slim["Folders"]["Data"]["Texts"]

		for name in names:
			# Define the file
			folder[name] = folder["root"] + name + ".json"

			# Create it
			self.File.Create(folder[name])

		# ---------- #

		# Define the Diary Slim "External statistics" files
		names = [
			"Statistics"
		]

		# Define the folder for easier typing
		folder = self.diary_slim["Folders"]["Data"]["External statistics"]

		for name in names:
			# Define the file
			folder[name] = folder["root"] + name + ".json"

			# Create it
			self.File.Create(folder[name])

		# ---------- #

		# Define the "Years" files
		names = [
			"History"
		]

		# Define the folder for easier typing
		folder = self.diary_slim["Folders"]["Years"]

		for name in names:
			# Define the file
			folder[name] = folder["root"] + name + ".json"

			# Create it
			self.File.Create(folder[name])

	def Define_Lists_And_Dictionaries(self):
		# Get the "Diary Slim" header in the user language
		file = self.diary_slim["Folders"]["Data"]["Header"][self.language["Small"]]

		self.diary_slim["Header template"] = self.File.Contents(file)["string"]

	def Define_Templates(self):
		# Define the root template dictionary
		self.template = {
			"Numbers": {
				"Months": 12,
				"Days": self.date["Units"]["Year days"]
			},
			"Months": {
				self.date["Texts"]["Month name with number"][self.language["Small"]]: {
					"Numbers": {
						"Year": self.date["Units"]["Year"],
						"Month": self.date["Units"]["Month"],
						"Days": self.date["Units"]["Month days"],
						"Diary Slims": 0
					},
					"Names": self.date["Texts"]["Month name"],
					"Formats": {
						"Diary Slim": self.date["Texts"]["Month name with number"][self.language["Small"]]
					},
					"Diary Slims": {}
				}
			}
		}

		# Define the dictionary of templates
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
					"Diary Slim": self.date["Texts"]["Month name with number"][self.language["Small"]]
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

		# ---------- #

		# Define the lines and json variables for faster typing
		file = self.diary_slim["Folders"]["Years"]["History"]

		lines = self.File.Contents(file)["lines"]
		json = self.JSON.To_Python(file)

		# If the "History.json" file is not empty
		# And the years list is not empty
		if (
			lines != [] and
			json["Years"] != []
		):
			# Get the filled "History" dictionary from the file
			self.history = self.JSON.To_Python(self.diary_slim["Folders"]["Years"]["History"])

		# ---------- #

		# Create a list of years starting from the year "2020" to the current year
		self.years_list = self.Date.Create_Years_List(start = 2020, function = str)

		# If the years list inside the History dictionary is empty, create a new one
		if self.history["Years"] == []:
			self.history["Years"] = self.years_list

		# If the current year is not inside the "History" years list, add it to the list
		if self.diary_slim["Current year"]["Number"] not in self.history["Years"]:
			self.history["Years"].append(self.diary_slim["Current year"]["Number"])

		# Sort the years list
		self.history["Years"] = sorted(self.history["Years"], key = str.lower)

		# ---------- #

		# Define the default numbers dictionary
		numbers = {
			"Years": len(self.years_list),
			"Months": 0,
			"Days": 0,
			"Diary Slims": 0
		}

		# ---------- #

		# Iterate through the years list
		# Years list: "2020" to the current year
		for year in self.years_list:
			# Create the year folder
			folders = {
				"root": self.diary_slim["Folders"]["Years"]["root"] + year + "/"
			}

			self.Folder.Create(folders["root"])

			# Define and create the "Year.json" file
			folders["Year"] = folders["root"] + "Year.json"

			self.File.Create(folders["Year"])

			# Define the file variable for easier typing
			file = folders["Year"]

			# If the file is not empty
			if self.File.Contents(file)["lines"] != []:
				# Get the "Year" dictionary from the file
				year_dictionary = self.JSON.To_Python(folders["Year"])

				# Iterate through the number keys
				for key in numbers.keys():
					# If the key is not equal to "Years"
					if key != "Years":
						# Add the current number to the local numbers dictionary
						numbers[key] += year_dictionary["Numbers"][key]

				# Update the "Months" number key
				year_dictionary["Numbers"]["Months"] = len(list(year_dictionary["Months"].keys()))

				# Update the "Diary Slims" number key
				year_dictionary["Numbers"]["Diary Slims"] = 0

				# Iterate through the month dictionaries
				for month in year_dictionary["Months"].values():
					# Add it to the "Diary Slims" number
					year_dictionary["Numbers"]["Diary Slims"] += month["Numbers"]["Diary Slims"]

			# If the file is empty
			else:
				# Get the "Year" template
				template = self.templates["Year"]

				# Update the number of the year
				template["Numbers"]["Year"] = int(year)

				# Update the number of months
				template["Numbers"]["Months"] = 12

				# Get a "Date" dictionary from the current year in the iteration
				date = self.Date.Now(self.Date.Date(year = int(year), month = 1, day = 1))

				# Update the days number
				template["Numbers"]["Days"] = date["Units"]["Year days"]

				# Redefine the "year_dictionary" variable
				year_dictionary = template

			# Update the empty "Year.json" file with the updated "Year" dictionary
			self.JSON.Edit(file, year_dictionary)

			# Add the local "folders" dictionary to the root "Diary Slim" folders dictionary
			self.diary_slim["Folders"]["Years"][year] = folders

		# Define the History "Numbers" dictionary as the local numbers dictionary
		self.history["Numbers"] = numbers

		# ---------- #

		# Update the "History.json" file with the updated "History" dictionary
		self.JSON.Edit(self.diary_slim["Folders"]["Years"]["History"], self.history)

	def Define_Story_Information(self):
		# Define the story JSON files
		names = [
			"Story",
			"Titles"
		]

		# Iterate through the names list
		for name in names:
			# Define the file and create it
			self.diary_slim["Folders"]["Story"][name] = self.diary_slim["Folders"]["Story"]["root"] + name + ".json"
			self.File.Create(self.diary_slim["Folders"]["Story"][name])

		# ---------- #

		# Define the default Story "Information" dictionary
		self.story = {
			"Titles": {},
			"Chapters": {
				"Numbers": {
					"Total": 0
				},
				"List": []
			},
			"Status": {
				"Number": 0,
				"Names": self.Language.language_texts["writing, title()"]
			},
			"HEX color": "f1858d"
		}

		# ---------- #

		# If the "Information.json" file is not empty
		file = self.diary_slim["Folders"]["Story"]["Story"]

		if self.File.Contents(file)["lines"] != []:
			# Get the filled "Information" dictionary from the file
			self.story = self.JSON.To_Python(self.diary_slim["Folders"]["Story"]["Story"])

		# ---------- #

		# If the "Titles" dictionary is empty
		if self.story["Titles"] == {}:
			# Get the "Titles" dictionary from the "Titles.json" file
			self.story["Titles"] = self.JSON.To_Python(self.diary_slim["Folders"]["Story"]["Titles"])

		# Define the number of chapters as the number of Diary Slims
		self.story["Chapters"]["Numbers"]["Total"] = self.history["Numbers"]["Diary Slims"]

		# ---------- #

		# Update the "Story.json" file with the updated "Story" dictionary
		self.JSON.Edit(self.diary_slim["Folders"]["Story"]["Story"], self.story)

	def Define_Current_Year(self):
		# Define the current year "Folders" dictionary
		self.diary_slim["Current year"]["Folders"] = self.diary_slim["Folders"]["Years"][self.diary_slim["Current year"]["Number"]]

		# ---------- #

		# Define the default "Year" dictionary
		self.diary_slim["Current year"]["Year"] = deepcopy(self.templates["Year"])

		# If the "Year.json" file is not empty
		file = self.diary_slim["Current year"]["Folders"]["Year"]

		if self.File.Contents(file)["lines"] != []:
			# Get the filled "Year" dictionary from its file
			self.diary_slim["Current year"]["Year"] = self.JSON.To_Python(file)

		# ---------- #

		# Define the year "Month" dictionary
		self.diary_slim["Current year"]["Month"] = {
			"Number": self.date["Units"]["Month"],
			"Name": self.date["Texts"]["Month name with number"][self.language["Small"]],
			"Name text": self.date["Texts"]["Month name"][self.language["Small"]],
			"Folders": {},
			"File": "",
			"Dictionary": {},
			"Statistics": {}
		}

		# Define and create the month folder
		self.diary_slim["Current year"]["Month"]["Folders"] = {
			"root": self.diary_slim["Current year"]["Folders"]["root"] + self.diary_slim["Current year"]["Month"]["Name"] + "/"
		}

		self.Folder.Create(self.diary_slim["Current year"]["Month"]["Folders"]["root"])

		# ---------- #

		# Define and create the "Month.json" file
		self.diary_slim["Current year"]["Month"]["File"] = self.diary_slim["Current year"]["Month"]["Folders"]["root"] + "Month.json"
		self.File.Create(self.diary_slim["Current year"]["Month"]["File"])

		# ---------- #

		# Define and create the "Statistics.json" file
		self.diary_slim["Current year"]["Month"]["Folders"]["Statistics"] = self.diary_slim["Current year"]["Month"]["Folders"]["root"] + "Statistics.json"
		self.File.Create(self.diary_slim["Current year"]["Month"]["Folders"]["Statistics"])

		# ---------- #

		# Define the default "Month" dictionary
		self.diary_slim["Current year"]["Month"]["Dictionary"] = deepcopy(self.templates["Month"])

		# If the "Month.json" file is not empty
		file = self.diary_slim["Current year"]["Month"]["File"]

		if self.File.Contents(file)["lines"] != []:
			# Get the filled "Month" dictionary from its file
			self.diary_slim["Current year"]["Month"]["Dictionary"] = self.JSON.To_Python(file)

		# Else, update the "Month" dictionary template
		else:
			# Update the "Month" dictionary
			self.diary_slim["Current year"]["Month"]["Dictionary"] = deepcopy(self.templates["Month"])

			# Update the number of Diary Slims
			self.diary_slim["Current year"]["Month"]["Dictionary"]["Numbers"]["Diary Slims"] = len(list(self.diary_slim["Current year"]["Month"]["Dictionary"]["Diary Slims"].keys()))

			# Update the "Month" dictionary inside the "Year" dictionary
			key = self.diary_slim["Current year"]["Month"]["Dictionary"]["Formats"]["Diary Slim"]

			self.diary_slim["Current year"]["Year"]["Months"][key] = self.diary_slim["Current year"]["Month"]["Dictionary"]

		# ---------- #

		# Update the "Month.json" file
		self.JSON.Edit(self.diary_slim["Current year"]["Month"]["File"], self.diary_slim["Current year"]["Month"]["Dictionary"])

		# Update the "Year.json" file
		self.JSON.Edit(self.diary_slim["Current year"]["Folders"]["Year"], self.diary_slim["Current year"]["Year"])

		# ---------- #

		# Define the "current_month" variable for easier typing
		self.current_month = self.diary_slim["Current year"]["Month"]

		# Get the current Diary Slim file
		self.diary_slim["Current year"]["Current Diary Slim file"] = self.Current_Diary_Slim()["File"]

		# Define the "current_year" variable for easier typing
		self.current_year = self.diary_slim["Current year"]

	def Current_Diary_Slim(self, current_year = None, date = None, current_diary_slim = True):
		# If the "current_year" parameter is None
		if current_year == None:
			# Get the current year from the "Diary Slim" dictionary
			current_year = self.diary_slim["Current year"]

		# If the "date" parameter is None
		if date == None:
			# Get the date from the root object
			date = self.date

		# ---------- #

		# Get the "Diary Slim" dictionary
		dictionary = self.Make_Diary_Slim_Dictionary(date, current_year)

		# Define the months and values variables for easier typing
		months = self.diary_slim["Current year"]["Year"]["Months"]
		values = list(months.values())

		# If the current Diary Slim file does not exist
		# And the current Diary Slim needs to be retrieved
		# And the "Months" dictionary of the current year is not empty
		# And the number of Diary Slims on the current month are not zero
		if (
			self.File.Exists(dictionary["File"]) == False and
			current_diary_slim == True and
			months != {} and
			values[-1]["Diary Slims"] != {}
		):
			# Get the most recent month and the most recent Diary Slim
			most_recent_month = values[-1]
			most_recent_diary_slim = list(most_recent_month["Diary Slims"].values())[-1]

			# Create the custom "Date" dictionary of the most recent Diary Slim
			date = self.Date.From_String(most_recent_diary_slim["Formats"]["DD-MM-YYYY"], format = "%d-%m-%Y")

			# Get the "Diary Slim" dictionary of the last Diary Slim file
			dictionary = self.Make_Diary_Slim_Dictionary(date, current_year)

		# ---------- #

		# Return the dictionary
		return dictionary

	def Make_Diary_Slim_Dictionary(self, date, current_year = None):
		# If the "current_year" parameter is None
		if current_year == None:
			# Get the current year from the "Diary Slim" dictionary
			current_year = self.diary_slim["Current year"]

		# ---------- #

		# Define the "Diary Slim" dictionary with the "Date" key
		# (Not the root module "Diary Slim" dictionary, the "Diary Slim" file dictionary)
		dictionary = {
			"Date": date
		}

		# ---------- #

		# Define the date variables for easier typing
		datetime = date["Timezone"]["DateTime"]
		units = datetime["Units"]
		texts = datetime["Texts"]
		formats = datetime["Formats"]

		# ---------- #

		# Define the "Day" key
		items = [
			self.Text.Add_Leading_Zeroes(units["Day"]),
			texts["Day name"][self.language["Small"]],
			formats["DD-MM-YYYY"]
		]

		dictionary["Day"] = "{} {}, {}".format(*items)

		# ---------- #

		# Define the "Month" dictionary with its keys
		dictionary["Month"] = {
			"Name": texts["Month name with number"][self.language["Small"]]
		}

		# ---------- #

		# Define the "Folders" dictionary
		dictionary["Folders"] = {
			"Year": self.diary_slim["Folders"]["Years"][current_year["Number"]]
		}

		# Define the month folder
		dictionary["Folders"]["Month"] = dictionary["Folders"]["Year"]["root"] + dictionary["Month"]["Name"] + "/"

		# Define the Diary Slim file
		dictionary["File"] = dictionary["Folders"]["Month"] + dictionary["Day"] + ".txt"

		# ---------- #

		# Return the dictionary
		return dictionary

	def Define_Diary_Slim_Texts(self):
		# Define the default Diary Slim texts dictionary
		self.diary_slim["Texts"] = {
			"Numbers": {
				"Total": 0
			},
			"List": [],
			"Options": {},
			"Dictionary": {}
		}

		# Define the "Texts.json" file variable for easier typing
		file = self.diary_slim["Folders"]["Data"]["Texts"]["Texts"]

		# If the "Texts.json" file is not empty
		if self.File.Contents(file)["Lines"] != []:
			# Get the filled "Texts" dictionary from its file
			dictionary = self.JSON.To_Python(file)

			# If the "Options" key is not inside the local file dictionary
			if "Options" not in dictionary:
				# Add the "Options" dictionary to the local dictionary
				# After the "List" key
				key_value = {
					"Options": self.diary_slim["Texts"]["Options"]
				}

				dictionary = self.JSON.Add_Key_After_Key(dictionary, key_value, after_key = "List")

			# Define the root "Texts" dictionary as the local file dictionary
			self.diary_slim["Texts"] = dictionary

		# ---------- #

		# Get the sub-folders of the "Texts" folder
		contents = self.Folder.Contents(self.diary_slim["Folders"]["Data"]["Texts"]["root"])

		# Get the text folders dictionary
		folders = contents["folder"]["dictionary"]

		# Get the number of texts
		self.diary_slim["Texts"]["Numbers"]["Total"] = len(contents["folder"]["names"])

		# Define the list of texts
		self.diary_slim["Texts"]["List"] = contents["folder"]["names"]

		# ---------- #

		# Iterate through the text folders dictionary
		for text, folder in folders.items():
			# Create the "Text" dictionary
			dictionary = {
				"Key": text,
				"Folders": {
					"root": folder
				},
				"Files": {},
				"Texts": {}
			}

			# ----- #

			# Define the text "Data.json" file
			dictionary["Files"]["Data"] = dictionary["Folders"]["root"] + "Data.json"

			# If the "Data.json" file exists
			if self.File.Exists(dictionary["Files"]["Data"]) == True:
				# Update the local dictionary with the one inside the file
				dictionary.update(self.JSON.To_Python(dictionary["Files"]["Data"]))

			# Else, remove the key
			else:
				dictionary["Files"].pop("Data")

			# ----- #

			# Manage the text "States" 

			# Define the text "States.json" file
			dictionary["Files"]["States"] = dictionary["Folders"]["root"] + "States.json"

			# Read the "States.json" file if it exists
			if self.File.Exists(dictionary["Files"]["States"]) == True:
				dictionary["States"] = self.JSON.To_Python(dictionary["Files"]["States"])

				# Get the list of state dictionaries
				states = list(dictionary["States"]["Dictionary"].values())

				# If the current state is empty, get the first state
				if dictionary["States"]["Current state"] == {}:
					dictionary["States"]["Current state"] = states[0]

				# Update the "States.json" file
				self.JSON.Edit(dictionary["Files"]["States"], dictionary["States"])

				# Iterate through the small languages list
				for language in self.languages["Small"]:
					# Define the state name
					dictionary["Texts"][language] = dictionary["States"]["Names"][language]

					# Get the current state
					current_state = dictionary["States"]["Current state"][language]

					# Add the current state
					dictionary["Texts"][language] += " (" + current_state + ")"

			# Else, remove the key
			else:
				dictionary["Files"].pop("States")

			# ----- #

			# Define the language text files
			for language in self.languages["Small"]:
				# Get the full language
				full_language = self.languages["Full"][language]

				# Define and create the language text file
				dictionary["Files"][language] = dictionary["Folders"]["root"] + full_language + ".txt"

				# If the "States" key is not inside the "Text" dictionary, create the file
				if "States" not in dictionary:
					self.File.Create(dictionary["Files"][language])

				# If the language file exists
				if self.File.Exists(dictionary["Files"][language]) == True:
					# Read the language text file and add its contents to the "Texts" dictionary
					dictionary["Texts"][language] = self.File.Contents(dictionary["Files"][language])["string"]

			# ----- #

			if "Data" in dictionary["Files"]:
				# Move the "Data" file key to the end if the key is present
				file = dictionary["Files"]["Data"]

				dictionary["Files"].pop("Data")

				dictionary["Files"]["Data"] = file

			# ----- #

			# If the "Item" key is inside the text dictionary
			if "Item" in dictionary:
				# Define the "Descriptions" dictionary if it is not already present
				if "Descriptions" not in dictionary:
					dictionary["Descriptions"] = {}

				# If the singular name is not present inside the "Descriptions" dictionary
				if "Singular" not in dictionary["Descriptions"]:
					# Define it as the item
					dictionary["Descriptions"]["Singular"] = dictionary["Item"]

				# If the plural name is not present inside the "Descriptions" dictionary
				if "Plural" not in dictionary["Descriptions"]:
					# Define it as the singular name plus an "s"
					dictionary["Descriptions"]["Plural"] = dictionary["Descriptions"]["Singular"] + "s"

				# Define the explain text if it is not present
				if "Explanation text" not in dictionary:
					dictionary["Explanation text"] = "say_what_you_did_on_the_{}"

			# ----- #

			# Define the "Quotes" key if it is not already present
			if "Quotes" not in dictionary:
				dictionary["Quotes"] = True

			# Add the "Is statistic" state to the dictionary, with a default value of False
			dictionary["Is statistic"] = False

			# ----- #

			# Define the text "Statistic.json" file
			dictionary["Files"]["Statistic"] = dictionary["Folders"]["root"] + "Statistic.json"

			# Read the "Statistic.json" file if it exists
			if self.File.Exists(dictionary["Files"]["Statistic"]) == True:
				dictionary["Statistic"] = self.JSON.To_Python(dictionary["Files"]["Statistic"])

			# Else, remove the key
			else:
				dictionary["Files"].pop("Statistic")

			# ----- #

			# Add the Diary Slim text dictionary to the root "Texts" dictionary
			self.diary_slim["Texts"]["Dictionary"][text] = dictionary

		# ---------- #

		# Iterate through the keys inside the Diary Slim Texts dictionary
		for key in deepcopy(self.diary_slim["Texts"]["Dictionary"]):
			# If the key is not inside the "folders" dictionary
			if key not in folders:
				# Remove the key
				self.diary_slim["Texts"]["Dictionary"].pop(key)

		# ---------- #

		# Add the "Keys" key inside the "Options" dictionary
		self.diary_slim["Texts"]["Options"]["Keys"] = []

		# Create empty language lists inside the "Options" dictionary
		for language in self.languages["Small"]:
			self.diary_slim["Texts"]["Options"][language] = []

		# Iterate through the keys inside the Diary Slim Texts dictionary
		for key, dictionary in self.diary_slim["Texts"]["Dictionary"].items():
			# Add the key
			self.diary_slim["Texts"]["Options"]["Keys"].append(key)

			# Add the English text
			english_text = dictionary["Texts"]["en"]

			self.diary_slim["Texts"]["Options"]["en"].append(english_text)

			# Add the user language text
			language_text = dictionary["Texts"][self.language["Small"]]

			self.diary_slim["Texts"]["Options"][self.language["Small"]].append(language_text)

		# ---------- #

		# Iterate through the keys inside the Diary Slim Texts dictionary
		for key in self.diary_slim["Texts"]["Dictionary"].copy():
			# If the key is not inside the "List" list, remove it
			if key not in self.diary_slim["Texts"]["List"]:
				self.diary_slim["Texts"]["Dictionary"].pop(key)

	def Define_Statistics(self):
		# Define the root statistics dictionary
		self.statistics = {
			"Numbers": {
				"Total": 0
			},
			"List": [],
			"Dictionary": {}
		}

		# Create a template of the statistics dictionary
		self.statistics_template = {}

		# ---------- #

		# Create a local dictionary of text dictionaries
		dictionaries = {}

		# Iterate through the keys and dictionaries inside the Diary Slim Texts dictionary
		for key, dictionary in self.diary_slim["Texts"]["Dictionary"].items():
			# If the "Statistic" key is inside the text dictionary
			if "Statistic" in dictionary:
				# Add the dictionary to the local dictionary of dictionaries
				dictionaries[key] = dictionary

		# Iterate through the keys and dictionaries inside the dictionary of text dictionaries that have a statistic
		for key, dictionary in dictionaries.items():
			# Define a shortcut for the statistic dictionary
			statistic = dictionary["Statistic"]

			# ----- #

			# If the "Question" or "Questions" keys are inside the statistic dictionary
			if (
				"Question" in statistic or
				"Questions" in statistic
			):
				# Define the list of keys to search for
				keys = [
					"Input text",
					"Show text",
					"Select text"
				]

				# Iterate through the list of keys
				for item in keys:
					# If the "Question" key is inside the statistic dictionary
					if "Question" in statistic:
						# Define the language text for the question dictionary, using the current key
						statistic["Question"] = self.Define_Language_Text(statistic["Question"], item)

					# Iterate through the list of sub-keys
					for sub_key in ["Questions", "Answers"]:
						# Define the local dictionary to use
						local_dictionary = statistic

						# If the sub-key is "Answers"
						# And the "Question" key is inside the statistic dictionary
						if (
							sub_key == "Answers" and
							"Question" in statistic
						):
							# Define the local dictionary as the question one
							local_dictionary = statistic["Question"]

						# If the sub-key is inside the local dictionary
						if sub_key in local_dictionary:
							# Iterate through the dictionary of question, getting the question key and question dictionary
							for question_key, question in local_dictionary[sub_key].items():
								# Define the language text for the question dictionary, using the current key
								local_dictionary[sub_key][question_key] = self.Define_Language_Text(question, item)

			# ----- #

			# Define a local empty template dictionary
			template = {}

			# Define the statistic key as the root key
			statistic_key = statistic["Key"]

			# If the "Alternative key" key is inside the text dictionary
			if "Alternative key" in statistic:
				# Change the statistic key the alternative key
				statistic_key = statistic["Alternative key"]

			# If the key is not "List"
			if statistic["Key"] != "List":
				# Add the statistic key to the template dictionary with a value of zero
				template[statistic_key] = 0

			# If the "Questions" key is inside the statistic dictionary
			if "Questions" in statistic:
				# Iterate through the questions dictionary, getting the question dictionary
				for question in statistic["Questions"].values():
					# If the question has a key
					if "Key" in question:
						# Add the question key to the template
						template[question["Key"]] = 0

			# If the "Question" key is inside the statistic dictionary
			if "Question" in statistic:
				# Define a shortcut for the question
				question = statistic["Question"]

				# If the question has a key
				if "Key" in question:
					# Add the question key to the template
					template[question["Key"]] = 0

			# Add the local statistic dictionary to the root statistics dictionary template
			self.statistics_template[key] = template

			# ----- #

			# If the "Add to statistics" key is inside the text dictionary
			# And the "Options" key is inside the statistic dictionary
			# And the "List" key is inside the options dictionary
			if (
				"Add to statistics" in dictionary and
				"Question" in statistic and
				"List" in statistic["Question"]
			):
				# Add the list of the text dictionary inside the statistic dictionary
				statistic["List"] = statistic["Question"]["List"]

				# Add each one of the items of the list to the statistics template
				for item in statistic["List"]:
					self.statistics_template[key][item] = 0

			# ----- #

			# If the "Secondary statistics" key is inside the statistics dictionary
			if "Secondary statistics" in statistic:
				# Add each one of the items of the dictionary to the statistics template
				for item in statistic["Secondary statistics"]:
					self.statistics_template[key][item] = 0

			# ----- #

			# Switch the "Is statistic" state to True
			dictionary["Is statistic"] = True

			# Add the statistic dictionary to the root statistics dictionary
			self.statistics["Dictionary"][key] = statistic

			# Update the root statistic dictionary of the text with the local one
			dictionary["Statistic"] = statistic

			# Update the root text dictionary with the local one
			self.diary_slim["Texts"]["Dictionary"][key] = dictionary

		# ---------- #

		# Create the external statistics dictionary
		self.Create_External_Statistics()

		# ---------- #

		# Make a copy of the "Texts" dictionary
		texts_copy = deepcopy(self.diary_slim["Texts"])

		# Remove the "Options" key
		texts_copy.pop("Options")

		# Update the "Texts.json" file with the updated Diary Slim "Texts" dictionary
		self.JSON.Edit(self.diary_slim["Folders"]["Data"]["Texts"]["Texts"], texts_copy)

		# ---------- #

		# List the statistics
		self.statistics["List"] = list(self.statistics["Dictionary"].keys())

		# Get the number of statistics
		self.statistics["Numbers"]["Total"] = len(self.statistics["List"])

		# Create the data "Statistics.json" file
		self.diary_slim["Folders"]["Data"]["Statistics"] = self.diary_slim["Folders"]["Data"]["root"] + "Statistics.json"
		self.File.Create(self.diary_slim["Folders"]["Data"]["Statistics"])

		# ---------- #

		# Create the "Years" dictionary
		self.years = {
			"List": self.history["Years"].copy(),
			"Dictionary": {}
		}

		# Iterate through the list of years
		for key in self.years["List"]:
			# Create the empty year dictionary
			year = {
				"Number": key,
				"Folders": {},
				"Months": {},
				"Statistics": {}
			}

			# Get the year folders
			year["Folders"] = self.diary_slim["Folders"]["Years"][key]

			# Define and create the files
			for file in ["Year", "Statistics"]:
				year["Folders"][file] = year["Folders"]["root"] + file + ".json"
				self.File.Create(year["Folders"][file])

			# If the local year is the current year
			if key == self.diary_slim["Current year"]["Number"]:
				# Add the statistics file to the "Current year" key
				self.diary_slim["Current year"]["Folders"]["Statistics"] = year["Folders"]["Statistics"]

			# ---------- #

			# Get the year dictionary
			dictionary = self.JSON.To_Python(year["Folders"]["Year"])

			# Iterate through the dictionary of months
			for month_key in dictionary["Months"]:
				# Define the local month dictionary
				month = {
					"Name": month_key,
					"Folders": {
						"root": year["Folders"]["root"] + month_key + "/"
					},
					"Statistics": {}
				}

				# Define and create the files
				for file in ["Month", "Statistics"]:
					month["Folders"][file] = month["Folders"]["root"] + file + ".json"
					self.File.Create(month["Folders"][file])

				# If the local year is the current year
				# And the local month is the current month
				if (
					key == self.diary_slim["Current year"]["Number"] and
					month_key == self.diary_slim["Current year"]["Month"]["Name"]
				):
					# Add the statistics file to the current month key
					self.diary_slim["Current year"]["Month"]["Folders"]["Statistics"] = month["Folders"]["Statistics"]

				# Add the current month dictionary to the root months dictionary
				year["Months"][month_key] = month

			# ---------- #

			# Add the current year dictionary to the root years dictionary
			self.years["Dictionary"][key] = year

		# Update the statistics
		self.Update_Statistics()

	def Get_Methods(self, class_):
		# Get the members
		import inspect
 
		members = inspect.getmembers(class_, predicate = inspect.ismethod)

		# Define a list of methods to remove
		remove_list = [
			"__init__",
			"Define_Basic_Variables",
			"Define_Texts",
			"Import_Classes"
		]

		# Define the empty list of methods
		methods = []

		# Iterate through the tuples in the members
		for tuple_ in members.copy():
			# Get the method name
			method = tuple_[0]

			# If the method is not in the remove list
			if method not in remove_list:
				# Add it to the list of methods
				methods.append(method)

		# Return the list of methods
		return methods

	def Create_External_Statistics(self):
		# Define the dictionary of modules
		modules = {
			"Numbers": {
				"Total": 0
			},
			"List": [],
			"Dictionary": {
				"Stories": {
					"Statistic key": "Story chapters"
				},
				"Watch_History": {
					"Statistic key": "Watched media"
				},
				"GamePlayer": {
					"Statistic key": "Gaming sessions played"
				}
			}
		}

		# Define the list of modules as the keys of the dictionary
		modules["List"] = list(modules["Dictionary"].keys())

		# Define the number of modules
		modules["Numbers"]["Total"] = len(modules["List"])

		# ---------- #

		# Create the local external statistics dictionary
		external_statistics = {
			"Numbers": {
				"Total": 0
			},
			"List": [],
			"Keys": [],
			"Dictionary": {}
		}

		# Define a shortcut for the file
		file = self.diary_slim["Folders"]["Data"]["External statistics"]["Statistics"]

		# If the external statistics file is not empty
		if self.File.Contents(file)["lines"] != []:
			# Get the JSON dictionary
			json_dictionary = self.JSON.To_Python(file)

			# Update the root year dictionary with the local JSON one, using the "Define_Options" method
			external_statistics = self.Define_Options(external_statistics, json_dictionary)

		# ---------- #

		# Iterate through the dictionary of modules
		for module_title, module in modules["Dictionary"].items():
			# Update the module dictionary
			module = {
				"Title": module_title,
				**module
			}

			# Get the statistic key from the module dictionary
			statistic_key = module["Statistic key"]

			# Add the module title to the list of external statistics if it is not already present
			if module_title not in external_statistics["List"]:
				external_statistics["List"].append(module_title)

			# Add the module title to the dictionary of external statistics if it is not already present
			if module_title not in external_statistics["Dictionary"]:
				external_statistics["Dictionary"][module_title] = {
					"Module": module_title,
					"Statistic key": statistic_key,
					"Text key": "",
					"Text": {},
					"List": [],
					"Years": {}
				}

			# Add the statistic key to the list of keys if it is not already present
			if statistic_key not in external_statistics["Keys"]:
				external_statistics["Keys"].append(statistic_key)

			# Define the "check empty dictionary" switch
			check_empty_dictionary = True

			# If the "check empty dictionary" switch is True
			# And the "Years" dictionary of the external statistic is empty
			# or the "check empty dictionary" switch is False
			if (
				check_empty_dictionary == True and
				external_statistics["Dictionary"][module["Title"]]["Years"] == {} or
				check_empty_dictionary == False
			):
				# Import the module
				module["Module"] = importlib.import_module("." + module["Title"], module["Title"])

				# Get the class of the module
				module["Class"] = getattr(module["Module"], module["Title"])()

				# Get the methods of the module
				module["Methods"] = self.Get_Methods(module["Class"])

				# Add the module to the modules dictionary
				modules["Dictionary"][module["Title"]] = module

				# If the module contains a method called "Create_Statistics"
				if "Create_Statistics" in module["Methods"]:
					# Get the dictionary of statistics from the "Create_Statistics" method
					# Passing the list of years as a parameter
					# Years list: "2020" to the current year
					statistics = module["Class"].Create_Statistics(self.years_list)

					# Define the dictionary of parameters
					parameters = {
						"text": statistic_key,
						"text_key": ""
					}

					# If the "Text key" key is present, update the parameters dictionary
					if "Text key" in statistics:
						parameters["text_key"] = statistics["Text key"]

					# Get the texts dictionary to use as the statistic text
					statistics["Text"] = self.Get_Text_Dictionary(**parameters)

					# ----- #

					# Add the statistics to the dictionary of external statistics
					external_statistics["Dictionary"][module["Title"]] = statistics

					# ----- #

					# Add the local statistic dictionary to the root statistics dictionary template
					self.statistics_template[statistic_key] = {
						"Module": module["Title"],
						"Total": 0,
						"Dictionary": {}
					}

			# Update the module dictionary inside the modules dictionary
			modules["Dictionary"][module["Title"]] = module

		# Update the number of external statistics
		external_statistics["Numbers"]["Total"] = len(external_statistics["List"])

		# Add the local external statistics dictionary to the root statistics dictionary
		self.statistics["External statistics"] = external_statistics

	def Get_Text_Dictionary(self, text, text_key = ""):
		# If the text key parameter is an empty string
		if text_key == "":
			# Define the text key for the text
			text_key = text.lower().replace(" ", "_")

			if "_" not in text_key:
				text_key += ", title()"

		# Define the texts dictionary
		texts = self.Language.texts

		# If the text key is inside the texts dictionary of this class
		if text_key in self.texts:
			# Update the local texts dictionary to be that one
			texts = self.texts

		# Get the text dictionary
		text = texts[text_key]

		# Return the text dictionary
		return text

	def Define_Language_Text(self, question, item):
		# If the current key is inside the question dictionary
		if item in question:
			# Get the text key as the value inside the dictionary, accessing it with the current key
			text_key = question[item]

			# Define the local language texts dictionary
			language_texts = self.Language.language_texts

			# If the text key is inside the language texts dictionary of this module
			if text_key in self.language_texts:
				# Define the local language texts dictionary as that one
				language_texts = self.language_texts

			# Define the text dictionary from the text key
			question[item] = language_texts[text_key]

		# Return the question dictionary
		return question

	def Define_Options(self, dictionary, options):
		for key in options:
			if type(options[key]) == dict:
				if (
					key in dictionary and
					dictionary[key] != {}
				):
					for sub_key in dictionary[key]:
						if sub_key in options[key]:
							dictionary[key][sub_key] = options[key][sub_key]

					for sub_key in options[key]:
						if sub_key not in dictionary[key]:
							dictionary[key][sub_key] = options[key][sub_key]

				if (
					key not in dictionary or
					dictionary[key] == {}
				):
					dictionary[key] = options[key]

			if type(options[key]) in [str, int, list]:
				dictionary[key] = options[key]

		return dictionary

	def Update_Statistics(self):
		# Make a copy of the statistics dictionary
		statistics_dictionary = deepcopy(self.statistics)

		# Remove the unneeded keys
		keys = [
			"External statistics"
		]

		for key in keys:
			statistics_dictionary.pop(key)

		# Update the data statistics file with the root statistics dictionary
		self.JSON.Edit(self.diary_slim["Folders"]["Data"]["Statistics"], statistics_dictionary)

		# ---------- #

		# Create a local dictionary of years
		years_dictionary = {}

		# Iterate through the dictionary of years
		for key, year in self.years["Dictionary"].items():
			# Update the "Statistics" dictionary of the year dictionary
			year["Statistics"] = deepcopy(self.statistics_template)

			# If the statistics file is not empty
			if self.File.Contents(year["Folders"]["Statistics"])["lines"] != []:
				# Get the JSON dictionary
				json_dictionary = self.JSON.To_Python(year["Folders"]["Statistics"])

				# Update the root year dictionary with the local JSON one, using the "Define_Options" method
				year["Statistics"] = self.Define_Options(year["Statistics"], json_dictionary)

			# Iterate through the keys inside the year statistics dictionary
			for statistic_key in year["Statistics"].copy():
				# If the key is not inside the root statistics dictionary
				# And the key is not an external statistic
				if (
					statistic_key not in self.statistics["Dictionary"] and
					statistic_key not in self.statistics["External statistics"]["Keys"]
				):
					# Remove it
					year["Statistics"].pop(statistic_key)

			# If the local year is the current year
			if key == self.diary_slim["Current year"]["Number"]:
				# Add the "Statistics" dictionary to the "Current year" key
				self.diary_slim["Current year"]["Statistics"] = year["Statistics"]

			# ---------- #

			# Iterate through the dictionary of months
			for month_key, month in year["Months"].items():
				# Update the "Statistics" dictionary of the month dictionary
				month["Statistics"] = deepcopy(self.statistics_template)

				# If the statistics file is not empty
				if self.File.Contents(month["Folders"]["Statistics"])["lines"] != []:
					# Get the JSON dictionary
					json_dictionary = self.JSON.To_Python(month["Folders"]["Statistics"])

					# Update the root month dictionary with the local JSON one, using the "Define_Options" method
					month["Statistics"] = self.Define_Options(month["Statistics"], json_dictionary)

				# Iterate through the keys inside the month "Statistics" dictionary
				for statistic_key in month["Statistics"].copy():
					# If the key is not inside the root statistics dictionary
					# And the key is not an external statistic
					if (
						statistic_key not in self.statistics["Dictionary"] and
						statistic_key not in self.statistics["External statistics"]["Keys"]
					):
						# Remove it
						month["Statistics"].pop(statistic_key)

				# If the local year is the current year
				# And the local month is the current month
				if (
					key == self.diary_slim["Current year"]["Number"] and
					month_key == self.diary_slim["Current year"]["Month"]["Name"]
				):
					# Add the statistics dictionary to the current month key
					self.diary_slim["Current year"]["Month"]["Statistics"] = month["Statistics"]

				# Update the current month dictionary on the root year dictionary
				year["Months"][month_key] = month

			# Add the year dictionary to the local dictionary of years
			years_dictionary[key] = year

			# ---------- #

			# Add the current year dictionary to the root years dictionary
			self.years["Dictionary"][key] = year

		# ---------- #

		# Update the external statistics dictionaries of the years and months

		# Define the "update root statistics" switch as False by default
		update_root_statistics = False

		# Iterate through the "External statistics" dictionary
		for statistics in self.statistics["External statistics"]["Dictionary"].values():
			# Define the statistic key
			statistic_key = statistics["Statistic key"]

			# Get the "Years" dictionary
			years = statistics["Years"]

			# Get the list of years
			years_list = list(years.keys())

			# Iterate through the list of years
			for key in years_list.copy():
				# If the year key is not inside the dictionary of years
				if key not in self.years["Dictionary"]:
					# Remove the key
					years_list.pop(key)

			# Iterate through the year dictionaries
			for year in years.values():
				# Get the root year dictionary
				root_year = self.years["Dictionary"][year["Key"]]

				# Get the root statistics dictionary
				root_statistics = root_year["Statistics"][statistic_key]

				# If the "update root statistics" switch is True
				if update_root_statistics == True:
					# Add the "Total" key and the number dictionaries inside the "Numbers" to the root year statistics dictionary
					root_year["Statistics"][statistic_key] = {
						"Module": root_statistics["Module"],
						"Total": year["Total"],
						"Dictionary": {
							**year["Numbers"]
						}
					}

				# Iterate through the months inside the year dictionary
				for month in year["Months"].values():
					# Get the month key using the list of month names in the user language with the month number with leading zeroes
					month_key = month["Key"] + " - " + self.Date.language_texts["month_names, type: list"][int(month["Key"])]

					# If the month key exists inside the dictionary of months of the root year
					# (I created the Diary Slim on July (07) of 2020, so the months from January to June (01 - 06) do not exist inside the "Months" dictionary)
					if month_key in root_year["Months"]:
						# Get the root statistics dictionary
						root_statistics = root_year["Months"][month_key]["Statistics"][statistic_key]

						# If the "update root statistics" switch is True
						if update_root_statistics == True:
							# Add the "Total" key and the number dictionaries inside the "Numbers" to the root month statistics dictionary
							root_year["Months"][month_key]["Statistics"][statistic_key] = {
								"Module": root_statistics["Module"],
								"Total": month["Total"],
								"Dictionary": {
									**month["Numbers"]
								}
							}

				# If the "update root statistics" switch is True
				if update_root_statistics == True:
					# Add the year dictionary to the local dictionary of years
					years_dictionary[year["Key"]] = root_year

		# Iterate through the dictionary of years
		for year_key, year in self.years["Dictionary"].items():
			# Iterate through the local external statistics dictionary
			for statistic in self.statistics["External statistics"]["Dictionary"].values():
				# Get the statistic key
				statistic_key = statistic["Statistic key"]

				# If the statistic key is inside the year dictionary
				if statistic_key in year["Statistics"]:
					# Get the year root statistics dictionary
					root_statistics = year["Statistics"][statistic_key]

					# If the only keys inside the current year root statistics dictionary are "Module" and "Total"
					# (That means there is no statistic inside the dictionary and the "Total" number is zero)
					if list(root_statistics.keys()) == ["Module", "Total"]:
						# Remove the statistic from the "Statistics" dictionary
						year["Statistics"].pop(statistic_key)

					# If the year key exists inside the "Years" dictionary of the external statistic dictionary
					if year_key in statistic["Years"]:
						# Get the year dictionary inside the statistics dictionary
						year_dictionary = statistic["Years"][year_key]

						# Update the "Total" key with the "Total" key of the root statistics
						year_dictionary["Total"] = root_statistics["Total"]

						# Update the "Numbers" key with the "Dictionary" key of the root statistics
						year_dictionary["Numbers"] = root_statistics["Dictionary"]

			# Iterate through the months inside the root year dictionary
			for month_key, month in year["Months"].items():
				# Iterate through the local external statistics dictionary
				for statistic in self.statistics["External statistics"]["Dictionary"].values():
					# Get the statistic key
					statistic_key = statistic["Statistic key"]

					# If the statistic key is inside the month dictionary
					if statistic_key in month["Statistics"]:
						# Get the month root statistics dictionary
						root_statistics = month["Statistics"][statistic_key]

						# If the only keys inside the current month root statistics dictionary are "Module" and "Total"
						# (That means there is no statistic inside the dictionary and the "Total" number is zero)
						if list(root_statistics.keys()) == ["Module", "Total"]:
							# Remove the statistic from the "Statistics" dictionary
							year["Months"][month_key]["Statistics"].pop(statistic_key)

						# Split the month key to get its number
						month_number = month_key.split(" - ")[0]

						# If the year key exists inside the "Years" dictionary of the external statistic dictionary
						if year_key in statistic["Years"]:
							# Get the year dictionary inside the statistics dictionary
							year_dictionary = statistic["Years"][year_key]

							# Update the "Total" key with the "Total" key of the root statistics
							year_dictionary["Total"] = root_statistics["Total"]

							# Update the "Numbers" key with the "Dictionary" key of the root statistics
							year_dictionary["Numbers"] = root_statistics["Dictionary"]

						# If the month number exists inside the "Months" dictionary of the external statistic dictionary
						if month_number in year_dictionary["Months"]:
							# Get the month dictionary inside the year statistics dictionary
							month_dictionary = year_dictionary["Months"][month_number]

							# Update the "Total" key with the "Total" key of the root statistics
							month_dictionary["Total"] = root_statistics["Total"]

							# Update the "Numbers" key with the "Dictionary" key of the root statistics
							month_dictionary["Numbers"] = root_statistics["Dictionary"]

						# If the month number does not exist inside the "Months" dictionary of the external statistic dictionary
						if month_number not in year_dictionary["Months"]:
							# Then create the month dictionary with its keys and values
							year_dictionary["Months"][month_number] = {
								"Key": month_number,
								"Total": root_statistics["Total"],
								"Numbers": root_statistics["Dictionary"]
							}

							# Sort the "Months" dictionary based on its keys
							year_dictionary["Months"] = dict(collections.OrderedDict(sorted(year_dictionary["Months"].items())))

					# If the statistic key is not inside the month dictionary
					if statistic_key not in month["Statistics"]:
						# Add the "Total" key and the number dictionaries inside the "Numbers" to the root month statistics dictionary
						year["Months"][month_key]["Statistics"][statistic_key] = {
							"Module": statistic["Module"],
							"Total": 0,
							"Dictionary": {}
						}

			# Add the year dictionary to the local dictionary of years
			years_dictionary[key] = year

		# ---------- #

		# Update the year and month "Statistics.json" files

		# Iterate through the local dictionary of years
		for year in years_dictionary.values():
			# Write the "Statistics" dictionary into the year "Statistics" file
			self.JSON.Edit(year["Folders"]["Statistics"], year["Statistics"])

			# Iterate through the dictionary of months
			for month in year["Months"].values():
				# Write the "Statistics" dictionary into the month "Statistics" file
				self.JSON.Edit(month["Folders"]["Statistics"], month["Statistics"])

		# ---------- #

		# Update the "External statistics" JSON file with the "External statistics" dictionary
		self.JSON.Edit(self.diary_slim["Folders"]["Data"]["External statistics"]["Statistics"], self.statistics["External statistics"])

	def Update_Current_Year_Statistics(self, year_statistics = None, month_statistics = None):
		# Write the year statistics dictionary into the year statistics file
		self.JSON.Edit(self.diary_slim["Current year"]["Folders"]["Statistics"], year_statistics)

		# Write the month statistics dictionary into the month statistics file
		self.JSON.Edit(self.diary_slim["Current year"]["Month"]["Folders"]["Statistics"], month_statistics)

	def Update_External_Statistics(self, statistic_key, statistics):
		# Define the list of parameters (statistic dictionaries to update)
		parameters = [
			self.diary_slim["Current year"]["Statistics"],
			self.diary_slim["Current year"]["Month"]["Statistics"]
		]

		# Define the root statistics text
		text = ""

		# ---------- #

		# Get the current year statistics
		year_statistics = statistics["Year"]

		# Update the statistic key inside the root year statistics dictionary
		parameters[0][statistic_key] = year_statistics

		# Get the year statistics text
		text += self.Show_Statistics("Year", statistics, return_text = True) + "\n"

		# ---------- #

		# Get the current month statistics
		month_statistics = statistics["Month"]

		# Update the statistic key inside the root month statistics dictionary
		parameters[1][statistic_key] = month_statistics

		# Get the year statistics text
		text += self.Show_Statistics("Month", statistics, return_text = True)

		# ---------- #

		# Update the statistics of the current year, with the two parameters
		self.Update_Current_Year_Statistics(*parameters)

		# Return the statistics text
		return text

	def Show_Statistics(self, date_type, statistics, return_text = False):
		# Define the text key
		text_key = date_type.lower()

		# Define the new number as one
		new_number = 1

		# If the "Number" key is inside the statistics dictionary
		if "Number" in statistics:
			# Get the number of updated statistics for the month/year
			new_number = statistics["Number"]

		# Define the statistic text to show as singular or plural depending on the number
		singular = self.Language.language_texts["updated_" + text_key + "_statistic"]
		plural = self.Language.language_texts["updated_" + text_key + "_statistics"]

		show_text = self.Text.By_Number(new_number, singular, plural)

		# Define the root statistics text
		statistics_text = "\n" + \
		show_text + ":"

		# If the "return text" parameter is False
		if return_text == False:
			# Show the statistics text
			print(statistics_text)

		# Add a line break to the root statistics text
		statistics_text += "\n"

		# Define the default "in text" as "in [year]"
		in_text = self.Language.language_texts["in"] + " " + str(self.diary_slim["Current year"]["Number"])

		# If the date type is "Month"
		if date_type == "Month":
			# Re-define the in text to be "in [month name]"
			in_text = self.Language.language_texts["in"] + " " + str(self.diary_slim["Current year"]["Month"]["Name text"])

		# If the "External statistic" key is inside the statistics dictionary
		if "External statistic" in statistics:
			# Get the first key of the statistics dictionary
			first_key = list(statistics["Dictionary"].keys())[0]

			# Make a copy of the statistics dictionary to not modify the root one
			statistics = deepcopy(statistics)

			# Make the dictionary only have the first key
			statistics["Dictionary"] = {
				first_key: {
					"Old number": statistics["Dictionary"]["Numbers"][date_type]["Old"],
					"Number": statistics["Dictionary"]["Numbers"][date_type]["New"],
					"Text": statistics["Text"]
				}
			}

		# Iterate through the dictionary of statistics
		for statistic in statistics["Dictionary"].values():
			# Get the old number
			old_number = statistic["Old number"]

			# Get the new number
			new_number = statistic["Number"]

			# If the "Text" key is inside the statistic dictionary
			if "Text" in statistic:
				# Define the text as it
				text = statistic["Text"]

			# Else, try to find it inside the root statistics dictionary
			else:
				text = statistics["Text"]

			# Add the in text text and a colon and space
			text = "\t" + text + " " + in_text + ": "

			# Define the number
			number = str(new_number)

			# If the "Money" key is inside the statistic dictionary
			if "Money" in statistic:
				# Define the money text
				number = self.Define_Money_Text(number)

			# Add the current number of the statistic
			text += number

			# Add the old number with the "before" text
			text += " (" + self.Language.language_texts["before, title()"].lower() + ": " + str(old_number) + ")"

			# Add the text to the root statistics text
			statistics_text += text

			# If the "return text" parameter is False
			if return_text == False:
				# Show the text and number with a tab
				print(text)

		# Return the statistics text
		return statistics_text

	def Next_State(self, dictionary):
		# Define the states variable for easier typing
		states = dictionary["States"]

		# Get the list of state dictionaries
		states_list = list(states["Dictionary"].values())

		# Get the index of the next state
		index = states_list.index(states["Current state"]) + 1

		# If the index is the last one, define the index as the first one
		if index == len(states_list):
			index = 0

		# Define the next state
		states["Current state"] = states_list[index]

		# Update the "States.json" file
		self.JSON.Edit(dictionary["Files"]["States"], states)