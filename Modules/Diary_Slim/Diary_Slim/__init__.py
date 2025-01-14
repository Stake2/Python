# Diary_Slim.py

# Import the "importlib" module
import importlib

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
		# Get the modules list
		self.modules = self.JSON.To_Python(self.folders["Apps"]["Modules"]["Modules"])

		# Create a list of the modules that will not be imported
		remove_list = [
			"Define_Folders",
			"Modules",
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

		# Get the switches dictionary from the "Global Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# Get the Languages dictionary
		self.languages = self.Language.languages

		# Get the user language and full user language
		self.user_language = self.Language.user_language
		self.full_user_language = self.Language.full_user_language

		# Define the local "folders" dictionary as the dictionary inside the "Folder" class
		self.folders = self.Folder.folders

		# Get the Sanitize method of the File class
		self.Sanitize = self.File.Sanitize

		# Get the current date from the Date module
		self.date = self.Date.date

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

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

		# Define the "Data" sub-folders
		names = [
			"Header",
			"Texts"
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
			self.diary_slim["Folders"]["Data"][key] = {
				"root": self.diary_slim["Folders"]["Data"]["root"] + name + "/"
			}

			# Create it
			self.Folder.Create(self.diary_slim["Folders"]["Data"][key]["root"])

		# Define the "Header" files
		for language in self.languages["small"]:
			# Get the full language
			full_language = self.languages["full"][language]

			# Define the file
			self.diary_slim["Folders"]["Data"]["Header"][language] = self.diary_slim["Folders"]["Data"]["Header"]["root"] + full_language + ".txt"

			# Create it
			self.File.Create(self.diary_slim["Folders"]["Data"]["Header"][language])

		# Define the Diary Slim "Texts" files
		names = [
			"Texts"
		]

		for name in names:
			# Define the file
			self.diary_slim["Folders"]["Data"]["Texts"][name] = self.diary_slim["Folders"]["Data"]["Texts"]["root"] + name + ".json"

			# Create it
			self.File.Create(self.diary_slim["Folders"]["Data"]["Texts"][name])

		# Define the "Years" files
		names = [
			"History"
		]

		for name in names:
			# Define the file
			self.diary_slim["Folders"]["Years"][name] = self.diary_slim["Folders"]["Years"]["root"] + name + ".json"

			# Create it
			self.File.Create(self.diary_slim["Folders"]["Years"][name])

	def Define_Lists_And_Dictionaries(self):
		# Get the "Diary Slim" header in the user language
		file = self.diary_slim["Folders"]["Data"]["Header"][self.user_language]

		self.diary_slim["Header template"] = self.File.Contents(file)["string"]

	def Define_Templates(self):
		# Define the root template dictionary
		self.template = {
			"Numbers": {
				"Months": 12,
				"Days": self.date["Units"]["Year days"]
			},
			"Months": {
				self.date["Texts"]["Month name with number"][self.user_language]: {
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

		# Define the default numbers dictionary
		numbers = {
			"Years": len(self.years_list),
			"Months": 0,
			"Days": 0,
			"Diary Slims": 0
		}

		# Iterate through the years list
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
				# Update the "Year" template
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

		# If the "Information.json" file is not empty
		file = self.diary_slim["Folders"]["Story"]["Story"]

		if self.File.Contents(file)["lines"] != []:
			# Get the filled "Information" dictionary from the file
			self.story = self.JSON.To_Python(self.diary_slim["Folders"]["Story"]["Story"])

		# If the "Titles" dictionary is empty
		if self.story["Titles"] == {}:
			# Get the "Titles" dictionary from the "Titles.json" file
			self.story["Titles"] = self.JSON.To_Python(self.diary_slim["Folders"]["Story"]["Titles"])

		# Define the number of chapters as the number of Diary Slims
		self.story["Chapters"]["Numbers"]["Total"] = self.history["Numbers"]["Diary Slims"]

		# Update the "Story.json" file with the updated "Story" dictionary
		self.JSON.Edit(self.diary_slim["Folders"]["Story"]["Story"], self.story)

	def Define_Current_Year(self):
		# Define the current year "Folders" dictionary
		self.diary_slim["Current year"]["Folders"] = self.diary_slim["Folders"]["Years"][self.diary_slim["Current year"]["Number"]]

		# Define the default "Year" dictionary
		self.diary_slim["Current year"]["Year"] = deepcopy(self.templates["Year"])

		# If the "Year.json" file is not empty
		file = self.diary_slim["Current year"]["Folders"]["Year"]

		if self.File.Contents(file)["lines"] != []:
			# Get the filled "Year" dictionary from its file
			self.diary_slim["Current year"]["Year"] = self.JSON.To_Python(file)

		# Define the year "Month" dictionary
		self.diary_slim["Current year"]["Month"] = {
			"Number": self.date["Units"]["Month"],
			"Name": self.date["Texts"]["Month name with number"][self.user_language],
			"Folders": {},
			"File": "",
			"Dictionary": {}
		}

		# Define and create the month folder
		self.diary_slim["Current year"]["Month"]["Folders"] = {
			"root": self.diary_slim["Current year"]["Folders"]["root"] + self.diary_slim["Current year"]["Month"]["Name"] + "/"
		}

		self.Folder.Create(self.diary_slim["Current year"]["Month"]["Folders"]["root"])

		# Define and create the "Month.json" file
		self.diary_slim["Current year"]["Month"]["File"] = self.diary_slim["Current year"]["Month"]["Folders"]["root"] + "Month.json"
		self.File.Create(self.diary_slim["Current year"]["Month"]["File"])

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

		# Update the "Month.json" file
		self.JSON.Edit(self.diary_slim["Current year"]["Month"]["File"], self.diary_slim["Current year"]["Month"]["Dictionary"])

		# Update the "Year.json" file
		self.JSON.Edit(self.diary_slim["Current year"]["Folders"]["Year"], self.diary_slim["Current year"]["Year"])

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
			self.File.Exist(dictionary["File"]) == False and
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

		# Return the dictionary
		return dictionary

	def Make_Diary_Slim_Dictionary(self, date, current_year = None):
		# If the "current_year" parameter is None
		if current_year == None:
			# Get the current year from the "Diary Slim" dictionary
			current_year = self.diary_slim["Current year"]

		# Define the empty "Diary Slim" dictionary
		# (Not the root module "Diary Slim" dictionary, the "Diary Slim" file dictionary)
		dictionary = {}

		# Define the date variables for easier typing
		datetime = date["Timezone"]["DateTime"]
		units = datetime["Units"]
		texts = datetime["Texts"]
		formats = datetime["Formats"]

		# Define the "Month" dictionary with its keys
		dictionary["Month"] = {
			"Name": texts["Month name with number"][self.user_language]
		}

		# Define the "Day" dictionary
		items = [
			self.Text.Add_Leading_Zeroes(units["Day"]),
			texts["Day name"][self.user_language],
			formats["DD-MM-YYYY"]
		]

		dictionary["Day"] = "{} {}, {}".format(*items)

		# Define the "Folders" dictionary
		dictionary["Folders"] = {
			"Year": self.diary_slim["Folders"]["Years"][current_year["Number"]]
		}

		# Define the month folder
		dictionary["Folders"]["Month"] = dictionary["Folders"]["Year"]["root"] + dictionary["Month"]["Name"] + "/"

		# Define the Diary Slim file
		dictionary["File"] = dictionary["Folders"]["Month"] + dictionary["Day"] + ".txt"

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
		if self.File.Contents(file)["lines"] != []:
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

		# Get the sub-folders of the "Texts" folder
		contents = self.Folder.Contents(self.diary_slim["Folders"]["Data"]["Texts"]["root"])

		# Get the text folders dictionary
		folders = contents["folder"]["dictionary"]

		# Define the texts number
		self.diary_slim["Texts"]["Numbers"]["Total"] = len(contents["folder"]["names"])

		# Define the texts list
		self.diary_slim["Texts"]["List"] = contents["folder"]["names"]

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

			# Read the "Data.json" file if it exists
			if self.File.Exist(dictionary["Files"]["Data"]) == True:
				dictionary.update(self.JSON.To_Python(dictionary["Files"]["Data"]))

			# Else, remove the key
			else:
				dictionary["Files"].pop("Data")

			# ----- #

			# Manage the text "States" 

			# Define the text "States.json" file
			dictionary["Files"]["States"] = dictionary["Folders"]["root"] + "States.json"

			# Read the "States.json" file if it exists
			if self.File.Exist(dictionary["Files"]["States"]) == True:
				dictionary["States"] = self.JSON.To_Python(dictionary["Files"]["States"])

				# Get the list of state dictionaries
				states = list(dictionary["States"]["Dictionary"].values())

				# If the current state is empty, get the first state
				if dictionary["States"]["Current state"] == {}:
					dictionary["States"]["Current state"] = states[0]

				# Update the "States.json" file
				self.JSON.Edit(dictionary["Files"]["States"], dictionary["States"])

				# Iterate through the small languages list
				for language in self.languages["small"]:
					# Define the state name
					dictionary["Texts"][language] = dictionary["States"]["Names"][language]

					# Add the current state
					dictionary["Texts"][language] += " (" + dictionary["States"]["Current state"][language] + ")"

			# Else, remove the key
			else:
				dictionary["Files"].pop("States")

			# ----- #

			# Define the language text files
			for language in self.languages["small"]:
				# Get the full language
				full_language = self.languages["full"][language]

				# Define and create the language text file
				dictionary["Files"][language] = dictionary["Folders"]["root"] + full_language + ".txt"

				# If the "States" key is not inside the "Text" dictionary, create the file
				if "States" not in dictionary:
					self.File.Create(dictionary["Files"][language])

				# If the language file exists
				if self.File.Exist(dictionary["Files"][language]) == True:
					# Read the language text file and add its contents to the "Texts" dictionary
					dictionary["Texts"][language] = self.File.Contents(dictionary["Files"][language])["string"]

					# Add "..." (three dots) if the "Item" key is present inside the "Data" dictionary
					if "Item" in dictionary:
						dictionary["Texts"][language] += "..."

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
			if self.File.Exist(dictionary["Files"]["Statistic"]) == True:
				dictionary["Statistic"] = self.JSON.To_Python(dictionary["Files"]["Statistic"])

			# Else, remove the key
			else:
				dictionary["Files"].pop("Statistic")

			# ----- #

			# Add the Diary Slim "Text" dictionary to the root "Texts" dictionary
			self.diary_slim["Texts"]["Dictionary"][text] = dictionary

		# Iterate through the keys inside the Diary Slim Texts dictionary
		for key, dictionary in deepcopy(self.diary_slim["Texts"]["Dictionary"]).items():
			# If the key is not inside the "folders" dictionary
			if key not in folders:
				# Remove the key
				self.diary_slim["Texts"]["Dictionary"].pop(key)

		# Add the "Keys" key inside the "Options" dictionary
		self.diary_slim["Texts"]["Options"]["Keys"] = []

		# Create empty language lists inside the "Options" dictionary
		for language in self.languages["small"]:
			self.diary_slim["Texts"]["Options"][language] = []

		# Iterate through the keys inside the Diary Slim Texts dictionary
		for key, dictionary in self.diary_slim["Texts"]["Dictionary"].items():
			# Add the key
			self.diary_slim["Texts"]["Options"]["Keys"].append(key)

			# Add the English text
			english_text = dictionary["Texts"]["en"]

			self.diary_slim["Texts"]["Options"]["en"].append(english_text)

			# Add the user language text
			language_text = dictionary["Texts"][self.user_language]

			self.diary_slim["Texts"]["Options"][self.user_language].append(language_text)

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

		# Iterate through the keys inside the Diary Slim Texts dictionary
		for key in self.diary_slim["Texts"]["Dictionary"].copy():
			# Get the text dictionary
			dictionary = self.diary_slim["Texts"]["Dictionary"][key]

			# If the "Statistic" key is inside the text dictionary
			if "Statistic" in dictionary:
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
							template[question["Key"]] = 0

				# Add the local statistic dictionary to the root statistics dictionary template
				self.statistics_template[key] = template

				# ----- #

				# If the "Add to statistics" key is inside the text dictionary
				# And the "Options" key is inside the statistic dictionary
				# And the "List" key is inside the options dictionary
				if (
					"Add to statistics" in dictionary and
					"Question" in dictionary and
					"List" in dictionary["Question"]
				):
					# Add the list of the text dictionary inside the statistic dictionary
					statistic["List"] = dictionary["Question"]["List"]

					# Add each one of the items of the list to the statistics template
					for item in statistic["List"]:
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
		self.years = {}

		# Iterate through the list of years
		for year in self.history["Years"]:
			# Get the year folders
			folders = self.diary_slim["Folders"]["Years"][year]

			# Create the "Statistics.json" file
			folders["Statistics"] = folders["root"] + "Statistics.json"
			self.File.Create(folders["Statistics"])

			# Add the folders and dictionary of statistics to the "Years" dictionary
			self.years[year] = {
				"Folders": folders,
				"Statistics": {}
			}

			# If the local year is the current year
			if year == self.diary_slim["Current year"]["Number"]:
				# Add the statistics file to the "Current year" key
				self.diary_slim["Current year"]["Folders"]["Statistics"] = folders["Statistics"]

		# Update the statistics
		self.Update_Statistics()

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

	def Update_Statistics(self):
		# Update the data statistics file with the root statistics dictionary
		self.JSON.Edit(self.diary_slim["Folders"]["Data"]["Statistics"], self.statistics)

		# Iterate through the list of years
		for year in self.history["Years"]:
			# Update the statistics dictionary of the year dictionary
			self.years[year]["Statistics"] = deepcopy(self.statistics_template)

			# If the statistics file is not empty
			if self.File.Contents(self.years[year]["Folders"]["Statistics"])["lines"] != []:
				# Get the JSON dictionary
				json_dictionary = self.JSON.To_Python(self.years[year]["Folders"]["Statistics"])

				# Update the root dictionary with the local JSON one
				self.years[year]["Statistics"].update(json_dictionary)

			# Iterate through the keys inside the year statistics dictionary
			for key in self.years[year]["Statistics"].copy():
				# If the key is not inside the root statistics dictionary
				if key not in self.statistics["Dictionary"]:
					# Remove it
					self.years[year]["Statistics"].pop(key)

			# Write the statistics dictionary into the file
			self.JSON.Edit(self.years[year]["Folders"]["Statistics"], self.years[year]["Statistics"])

			# If the local year is the current year
			if year == self.diary_slim["Current year"]["Number"]:
				# Add the statistics dictionary to the "Current year" key
				self.diary_slim["Current year"]["Statistics"] = self.years[year]["Statistics"]

	def Update_Current_Year_Statistics(self, statistics):
		# Write the parameter statistics dictionary into the file
		self.JSON.Edit(self.diary_slim["Current year"]["Folders"]["Statistics"], statistics)

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