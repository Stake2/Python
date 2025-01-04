# GamePlayer.py

# Import the "importlib" module
import importlib

from copy import deepcopy

class GamePlayer(object):
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.folders = self.Define_Folders(object = self).folders

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Import the usage classes
		self.Import_Usage_Classes()

		# Folders and files method
		self.Define_Folders_And_Files()

		# Class methods
		self.Define_Types()
		self.Define_Registry_Format()

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

	def Import_Usage_Classes(self):
		# Define the classes to be imported
		classes = [
			"Years",
			"Christmas"
		]

		# Import them
		for title in classes:
			# Import the module
			module = importlib.import_module("." + title, title)

			# Get the sub-class
			sub_class = getattr(module, title)

			# Add the sub-class to the current module
			setattr(self, title, sub_class())

		self.Today_Is_Christmas = self.Christmas.Today_Is_Christmas()

	def Define_Folders_And_Files(self):
		# If there is no current year variable inside the self object, get the current year variable from the "Years" module
		if hasattr(self, "current_year") == False:
			self.current_year = self.Years.years["Current year"]

		# Replace the "self.folders" folder dictionary with the "Games" network folder dictionary
		self.folders = self.folders["Notepad"]["Data Networks"]["Games"]

		# Define the current year folder for easier typing
		self.folders["Play History"]["Current year"] = self.folders["Play History"][self.current_year["Number"]]

		# Define the "History" dictionary
		self.history = {
			"Key": "Sessions",
			"Numbers": {
				"Game sessions played": ""
			},
			"Folder": self.Folder.folders["Notepad"]["Data Networks"]["Games"]["Play History"]["root"]
		}

	def Parse_Arguments(self):
		if (
			self.switches["Verbose"] == True and
			"Active argument" in self.arguments
		):
			print()
			print(self.Language.language_texts["arguments, title()"] + ":")
			print()

			self.JSON.Show(self.arguments)

	def Define_Types(self):
		self.game_types = self.JSON.To_Python(self.folders["Data"]["Types"])

		self.game_types.update({
			"Genders": self.Language.texts["genders, type: dict"],
			"Gender items": self.Language.texts["gender_items"],
			"Game list": {
				"Number": 0,
				"Numbers": {}
			},
			"Dictionary": {}
		})

		# Reset the game number to 0
		if self.game_types["Game list"]["Number"] != 0:
			self.game_types["Game list"]["Number"] = 0

		# Read the root "Information.json" file
		if self.File.Contents(self.folders["Information"]["Information"])["lines"] != []:
			info_dictionary = self.JSON.To_Python(self.folders["Information"]["Information"])

		# If the root "Information.json" file is empty, add a default JSON dictionary inside it
		if self.File.Contents(self.folders["Information"]["Information"])["lines"] == []:
			info_dictionary = {
				"Types": self.game_types["Types"],
				"Number": 0,
				"Numbers": {}
			}

		# Iterate through the English plural types list
		i = 0
		for game_type in self.game_types["Types"]["en"]:
			key = game_type.lower().replace(" ", "_")

			language_type = self.game_types["Types"][self.user_language][i]

			# Create game type dictionary
			self.game_types[game_type] = {
				"Type": {},
				"Folders": {},
				"Status": [
					self.texts["plan_to_play, title()"]["en"],
					self.texts["playing, title()"]["en"],
					self.texts["re_playing, title()"]["en"],
					self.Language.texts["on_hold, title()"]["en"]
				],
				"Texts": {},
				"Game number": 0,
				"Game list": []
			}

			# Define the game types per language
			for language in self.languages["small"]:
				self.game_types[game_type]["Type"][language] = self.game_types["Types"][language][i]

			# Create type folders
			for root_folder in ["Information", "Play History", "Shortcuts"]:
				# "Game Information" folder
				if root_folder == "Information":
					self.folders[root_folder][key] = {
						"root": self.folders[root_folder]["root"] + language_type + "/"
					}

					self.Folder.Create(self.folders[root_folder][key]["root"])

				# "Play History Per Game Type" folder
				if root_folder == "Play History":
					self.folders[root_folder]["Current year"]["Per Game Type"][key] = {
						"root": self.folders[root_folder]["Current year"]["Per Game Type"]["root"] + game_type + "/"
					}

					self.Folder.Create(self.folders[root_folder]["Current year"]["Per Game Type"][key]["root"])

					# Create "Sessions.json" file
					self.folders[root_folder]["Current year"]["Per Game Type"][key]["Sessions"] = self.folders[root_folder]["Current year"]["Per Game Type"][key]["root"] + "Sessions.json"
					self.File.Create(self.folders[root_folder]["Current year"]["Per Game Type"][key]["Sessions"])

					# Create "Entry list.txt" file
					self.folders[root_folder]["Current year"]["Per Game Type"][key]["Entry list"] = self.folders[root_folder]["Current year"]["Per Game Type"][key]["root"] + "Entry list.txt"
					self.File.Create(self.folders[root_folder]["Current year"]["Per Game Type"][key]["Entry list"])

					# Create "Files" folder 
					self.folders[root_folder]["Current year"]["Per Game Type"][key]["Files"] = {
						"root": self.folders[root_folder]["Current year"]["Per Game Type"][key]["root"] + "Files/"
					}

					self.Folder.Create(self.folders[root_folder]["Current year"]["Per Game Type"][key]["Files"]["root"])

				# "Shortcuts" folder
				if root_folder == "Shortcuts":
					self.folders[root_folder] = {
						key: {
							"root": self.Folder.folders["Games"]["Shortcuts"]["root"] + self.Sanitize(language_type) + "/"
						}
					}

					self.Folder.Create(self.folders[root_folder][key]["root"])

			# Define game type folders and files
			self.game_types[game_type]["Folders"] = {
				"Information": self.folders["Information"][key],
				"Per Game Type": self.folders["Play History"]["Current year"]["Per Game Type"][key],
				"Shortcuts": self.folders["Shortcuts"][key]
			}

			# Define the "Information.json" file
			self.game_types[game_type]["Folders"]["Information"]["Information"] = self.game_types[game_type]["Folders"]["Information"]["root"] + "Information.json"
			self.File.Create(self.game_types[game_type]["Folders"]["Information"]["Information"])

			# Read the "Information.json" file
			if self.File.Contents(self.game_types[game_type]["Folders"]["Information"]["Information"])["lines"] != []:
				self.game_types[game_type]["JSON"] = self.JSON.To_Python(self.game_types[game_type]["Folders"]["Information"]["Information"])

			# If the "Information.json" file is empty, add a default JSON dictionary inside it
			if self.File.Contents(self.game_types[game_type]["Folders"]["Information"]["Information"])["lines"] == []:
				# Define the default JSON dictionary
				self.game_types[game_type]["JSON"] = {
					"Number": 0,
					"Titles": [],
					"Status": {}
				}

				# Create an empty list for each status
				for english_status in self.texts["statuses, type: list"]["en"]:
					self.game_types[game_type]["JSON"]["Status"][english_status] = []

			# Update the number of games inside the json dictionary
			self.game_types[game_type]["JSON"]["Number"] = len(self.game_types[game_type]["JSON"]["Titles"])

			# Sort the game titles list
			self.game_types[game_type]["JSON"]["Titles"] = sorted(self.game_types[game_type]["JSON"]["Titles"], key = str.lower)

			# Sort the status lists
			for english_status in self.texts["statuses, type: list"]["en"]:
				self.game_types[game_type]["JSON"]["Status"][english_status] = sorted(self.game_types[game_type]["JSON"]["Status"][english_status], key = str.lower)

			# Edit the "Information.json" file with the updated dictionary
			self.JSON.Edit(self.game_types[game_type]["Folders"]["Information"]["Information"], self.game_types[game_type]["JSON"])

			# Check the status of the game list
			# Add the game inside the correct status list if it is not there already
			# Remove the game from the wrong status list if it is there
			self.game_types[game_type] = self.Check_Status(self.game_types[game_type])

			# Add the game number to the game number
			self.game_types["Game list"]["Number"] += self.game_types[game_type]["JSON"]["Number"]

			# Add the game number to the root game number
			info_dictionary["Numbers"][game_type] = self.game_types[game_type]["JSON"]["Number"]

			# Add the game number to the game type game numbers
			self.game_types["Game list"]["Numbers"][game_type] = self.game_types[game_type]["JSON"]["Number"]

			# Get the game list with "Playing" and "Re-playing" statuses
			self.game_types[game_type]["Game list"] = self.Get_Game_List(self.game_types[game_type])

			# Define the game number of the game type
			self.game_types[game_type]["Game number"] = len(self.game_types[game_type]["Game list"])

			add_status = True

			# Add status to the "game list option" list if add_status is True
			if add_status == True:
				self.game_types[game_type]["Game list (option)"] = self.game_types[game_type]["Game list"].copy()

				d = 0
				for game in self.game_types[game_type]["Game list"]:
					for status in self.game_types[game_type]["Status"]:
						if game in self.game_types[game_type]["JSON"]["Status"][status]:
							language_status = self.Get_Language_Status(status)

					items = [
						self.game_types[game_type]["Game list (option)"][d],
						language_status
					]

					self.game_types[game_type]["Game list (option)"][d] = "{} - ({})".format(*items)

					d += 1

				if self.game_types[game_type]["Game list (option)"] == []:
					self.game_types[game_type].pop("Game list (option)")

			# Remove the "JSON" key
			self.game_types[game_type].pop("JSON")

			# Add the game list length numbers to the game types list to show on select game type
			self.game_types[game_type]["Texts"]["Show"] = self.game_types[game_type]["Type"][self.user_language] + " (" + str(len(self.game_types[game_type]["Game list"])) + ")"

			# Add the game type dictionary to the "Dictionary" key
			self.game_types["Dictionary"][game_type] = self.game_types[game_type]

			i += 1

		# Copy the game types dictionary
		types = deepcopy(self.game_types)

		# Remove the "Dictionary" key
		types.pop("Dictionary")

		# Write the local game types dictionary into the "Types.json" file
		self.JSON.Edit(self.folders["Data"]["Types"], types)

		# Update the game list inside the root "Information.json" dictionary
		info_dictionary.update(self.game_types["Game list"])

		# Update the root "Information.json" file
		self.JSON.Edit(self.folders["Information"]["Information"], info_dictionary)

	def Define_Registry_Format(self):
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
					"Sessions": 0
				},
				"Years": []
			},
			"Sessions": deepcopy(self.template),
			"Game type": {},
			"Played": deepcopy(self.template)
		}

		if (
			self.File.Contents(self.folders["Play History"]["History"])["lines"] != [] and
			self.JSON.To_Python(self.folders["Play History"]["History"])["Years"] != []
		):
			# Get the History dictionary from file
			self.dictionaries["History"] = self.JSON.To_Python(self.folders["Play History"]["History"])

		# If the current year is not inside the "History" years list, add it to the list
		if self.current_year["Number"] not in self.dictionaries["History"]["Years"]:
			self.dictionaries["History"]["Years"].append(self.current_year["Number"])

		sessions = 0

		# Update the number of sessions of all years
		for year in self.Date.Create_Years_List(start = 2021, function = str):
			# Get the year folder and the entries file
			year_folder = self.folders["Play History"]["root"] + year + "/"
			entries_file = year_folder + "Sessions.json"

			# If the file exists and it is not empty
			if (
				self.File.Exist(entries_file) == True and
				self.File.Contents(entries_file)["lines"] != []
			):
				# Add the number of lines of the file to the local number of entries
				sessions += self.JSON.To_Python(entries_file)["Numbers"]["Total"]

			# Add the year to the Years list if it is not inside it
			if year not in self.dictionaries["History"]["Years"]:
				self.dictionaries["History"]["Years"].append(year)

		# Sort the Years list
		self.dictionaries["History"]["Years"] = sorted(self.dictionaries["History"]["Years"], key = str.lower)

		# Update the number of years with the length of the years list
		self.dictionaries["History"]["Numbers"]["Years"] = len(self.dictionaries["History"]["Years"])

		# Define the number of Entries of all years as the local number of entries
		self.dictionaries["History"]["Numbers"]["Sessions"] = sessions

		# Update the "History.json" file with the updated "History" dictionary
		self.JSON.Edit(self.folders["Play History"]["History"], self.dictionaries["History"])

		# Create the "Per Game Type" key inside the "Numbers" dictionary of the "Sessions" dictionary
		self.dictionaries["Sessions"]["Numbers"]["Per Game Type"] = {}

		# If the "Sessions.json" is not empty and has entries, get the Sessions dictionary from it
		if (
			self.File.Contents(self.folders["Play History"]["Current year"]["Sessions"])["lines"] != [] and
			self.JSON.To_Python(self.folders["Play History"]["Current year"]["Sessions"])["Entries"] != []
		):
			self.dictionaries["Sessions"] = self.JSON.To_Python(self.folders["Play History"]["Current year"]["Sessions"])

		# Iterate through the English game types list
		for game_type in self.game_types["Types"]["en"]:
			key = game_type.lower().replace(" ", "_")

			# Define default type dictionary
			self.dictionaries["Game type"][game_type] = deepcopy(self.template)

			# If the game type "Sessions.json" is not empty, get the game type Sessions dictionary from it
			if (
				self.File.Contents(self.folders["Play History"]["Current year"]["Per Game Type"][key]["Sessions"])["lines"] != [] and
				self.JSON.To_Python(self.folders["Play History"]["Current year"]["Per Game Type"][key]["Sessions"])["Entries"] != []
			):
				self.dictionaries["Game type"][game_type] = self.JSON.To_Python(self.folders["Play History"]["Current year"]["Per Game Type"][key]["Sessions"])

			# Add the game type number to the root numbers per game type if it does not exist in there
			if game_type not in self.dictionaries["Sessions"]["Numbers"]["Per Game Type"]:
				self.dictionaries["Sessions"]["Numbers"]["Per Game Type"][game_type] = 0

			# Else, define the root total number per game type as the number inside the Sessions dictionary per game type
			if game_type in self.dictionaries["Sessions"]["Numbers"]["Per Game Type"]:
				self.dictionaries["Sessions"]["Numbers"]["Per Game Type"][game_type] = self.dictionaries["Game type"][game_type]["Numbers"]["Total"]

			# Update the per game type "Sessions.json" file with the updated per game type "Sessions" dictionary
			self.JSON.Edit(self.folders["Play History"]["Current year"]["Per Game Type"][key]["Sessions"], self.dictionaries["Game type"][game_type])

		# Update the "Sessions.json" file with the updated "Sessions" dictionary
		self.JSON.Edit(self.folders["Play History"]["Current year"]["Sessions"], self.dictionaries["Sessions"])

	def Get_Game_List(self, dictionary, status = None):
		'''

		Returns a game list of a specific game type that contains a game status

			Parameters:
				dictionary (dict): a game_type dictionary containing the game type folders
				status (str or list): a status string or list used to get the games that has that status

			Returns:
				game_list (list): The game list that contains the game that has the passed status string or list

		'''

		# Get the status list from the game type dictionary
		status_list = dictionary["Status"].copy()

		# If the status parameter is not None, use it as the status list
		if status != None:
			status_list = status

		# If the "Status" key is present inside the dictionary, use it as the status list
		if "Status" in dictionary:
			status_list = dictionary["Status"]

		# If the type of the status list is string, transform it into a list with the string
		if type(status_list) == str:
			status_list = [status_list]

		# Read the "Information.json" file of game type
		dictionary["JSON"] = self.JSON.To_Python(dictionary["Folders"]["Information"]["Information"])

		# Define the empty game list
		game_list = []

		# Add the games of each status to the game list
		for status in status_list:
			if type(status) == dict:
				status = status["en"]

			game_list.extend(dictionary["JSON"]["Status"][status])

		# Sort the game list
		game_list = sorted(game_list, key = str.lower)

		return game_list

	def Select_Game_Type(self, options = None):
		dictionary = {
			"Texts": {
				"Show": self.language_texts["game_categories"],
				"Select": self.language_texts["select_one_game_category_to_play"]
			},
			"List": {
				"en": self.game_types["Types"]["en"].copy(),
				self.user_language: self.game_types["Types"][self.user_language].copy()
			},
			"Status": [
				self.texts["plan_to_play, title()"]["en"],
				self.texts["playing, title()"]["en"],
				self.texts["re_playing, title()"]["en"],
				self.Language.texts["on_hold, title()"]["en"]
			]
		}

		if options != None:
			dictionary = self.Define_Options(dictionary, options)

		# Get the game type game numbers
		numbers = self.JSON.To_Python(self.folders["Information"]["Information"])["Numbers"]

		# Add the number of game inside each game type text
		i = 0
		for game_type in self.game_types["Types"]["en"]:
			if game_type in dictionary["List"]["en"]:
				for language in self.languages["small"]:
					dictionary["List"][language][i] = dictionary["List"][language][i] + " (" + str(numbers[game_type]) + ")"

				i += 1

		# Select the game type
		if (
			"option" not in dictionary and
			"number" not in dictionary
		):
			dictionary["option"] = self.Input.Select(dictionary["List"]["en"], dictionary["List"][self.user_language], show_text = dictionary["Texts"]["Show"], select_text = dictionary["Texts"]["Select"])["option"]

			dictionary["option"] = dictionary["option"].split(" (")[0]

		if "number" in dictionary:
			dictionary["option"] = dictionary["List"]["en"][dictionary["number"]]

		# Get the selected game type dictionary from the game types dictionary
		dictionary.update(self.game_types[dictionary["option"]])

		# Get the status from the options dictionary
		if (
			options != None and
			"Status" in options
		):
			dictionary["Status"] = options["Status"]

		# Get the game list using the correct status
		dictionary["Game list"] = self.Get_Game_List(dictionary)

		# Add the game list length numbers to the game types list to show on select game type
		dictionary["Texts"]["Show"] = dictionary["Type"][self.user_language] + " (" + str(len(dictionary["Game list"])) + ")"

		return dictionary

	def Select_Game(self, options = None, define_item = False, play = False, game_title = None):
		# Define the empty dictionary
		dictionary = {}

		if options != None:
			dictionary = self.Define_Options(dictionary, options)

		# Add the "define_item" variable to the class instance
		self.define_item = define_item

		# Define the "game" variable for easier typing
		game = dictionary["Game"]

		# If the define item variable is True
		# And the sub-game is not the root game
		if (
			self.define_item == True and
			dictionary["Game"]["Sub-game"]["Title"] != dictionary["Game"]["Title"]
		):
			game = game["Sub-game"]

		# Define the texts
		dictionary["Texts"] = dictionary["Type"]["Texts"]

		# Define the select text
		text = dictionary["Type"]["Type"][self.user_language]

		if "Select" in dictionary["Type"]:
			text = dictionary["Type"]["Select"]

		# Define the select texts
		dictionary["Texts"]["Select"] = self.language_texts["select_one_game_to_play"]

		# Select the game
		if "Title" not in game:
			# Define the list of options as the game list
			language_options = dictionary["Type"]["Game list"]

			# If a custom game list is present inside the game type dictionary, use it 
			if "Game list (option)" in dictionary["Type"]:
				language_options = dictionary["Type"]["Game list (option)"]

			# If the game title variable is None, ask the user to select the game
			if game_title == None:
				# Define the list of options, and show and select texts
				options_list = dictionary["Type"]["Game list"]
				show_text = dictionary["Texts"]["Show"]
				select_text = dictionary["Texts"]["Select"]

				# Ask the user to select the game
				title = self.Input.Select(options_list, language_options = language_options, show_text = show_text, select_text = select_text)["option"]

			# If the game title is not None, use it as the game title
			if game_title != None:
				title = game_title

			game.update({
				"Title": title
			})

		# Define the "Titles" key
		game["Titles"] = {}

		# Define the root folder
		root_folder = dictionary["Type"]["Folders"]["Information"]["root"]

		# If the define item variable is True
		# And the sub-game is not the root game
		if (
			self.define_item == True and
			dictionary["Game"]["Sub-game"]["Title"] != dictionary["Game"]["Title"]
		):
			root_folder = dictionary["Game"]["Sub-game type"]["Folders"]["root"]

		# Define the game information folder
		game["Folders"] = {
			"root": root_folder + self.Sanitize_Title(game["Title"]) + "/"
		}

		# Create the folders
		for key in game["Folders"]:
			folder = game["Folders"][key]

			if "root" in folder:
				folder = folder["root"]

			self.Folder.Create(folder)

		# Define the list of file names
		file_names = [
			"Details",
			"Dates"
		]

		# Define the "Information" dictionary
		game["Information"] = {
			"File name": "Game",
			"Key": ""
		}

		# If the define item variable is True
		# And the sub-game is not the root game
		if (
			self.define_item == True and
			dictionary["Game"]["Sub-game"]["Title"] != dictionary["Game"]["Title"]
		):
			game["Information"]["File name"] = dictionary["Game"]["Sub-game type"]["Texts"]["Singular"]["en"]

		# Add the Information file name to the file names list
		file_names.append(game["Information"]["File name"] + ".json")

		# Define the Information key
		game["Information"]["Key"] = game["Information"]["File name"].lower().replace(" ", "_")

		# Define and create the game text files
		for file_name in file_names:
			key = file_name.lower().replace(" ", "_").replace(".json", "")

			if key == "details":
				texts_list = self.Language.language_texts

			if key == "dates":
				texts_list = self.Date.language_texts

			if ".json" not in file_name:
				file_name = texts_list[key + ", title()"] + ".txt"

			game["Folders"][key] = game["Folders"]["root"] + file_name
			self.File.Create(game["Folders"][key])

		# If the Information file is not empty, read it
		if self.File.Contents(game["Folders"][game["Information"]["Key"]])["lines"] != []:
			game["Information"]["Dictionary"] = self.JSON.To_Python(game["Folders"][game["Information"]["Key"]])

		# Define the dictionary of items to create the "Played folder"
		items = {
			"None": game["Folders"]["root"]
		}

		# If the define item variable is True
		# And the sub-game is the root game
		if (
			self.define_item == True and
			dictionary["Game"]["Sub-game"]["Title"] == dictionary["Game"]["Title"]
		):
			items["Sub-game"] = dictionary["Game"]["Sub-game type"]["Folders"]["root"] + self.Sanitize_Title(game["Title"]) + "/"

		# Iterate through the items dictionary
		for item, root_folder in items.items():
			folder = game["Folders"]

			if item == "Sub-game":
				folder = dictionary["Game"]["Sub-game"]["Folders"]

			# Create the "Played" folder
			folder["Played"] = {
				"root": root_folder + self.Language.language_texts["played, title()"] + "/"
			}

			self.Folder.Create(folder["Played"]["root"])

			# Create the "Played" files
			files = [
				"Entries.json",
				"Entry list.txt"
			]

			for file in files:
				key = file.lower().split(".")[0].replace(" ", "_")

				folder["Played"][key] = folder["Played"]["root"] + file
				self.File.Create(folder["Played"][key])

			# Create the "Files" folder file inside the "Played" folder
			folder["Played"]["files"] = {
				"root": folder["Played"]["root"] + self.File.language_texts["files, title()"] + "/"
			}

			self.Folder.Create(folder["Played"]["files"]["root"])

			# Define the "Played" dictionary as the template
			self.dictionaries["Played"] = deepcopy(self.template)

			# Get the "Played" dictionary from file if the dictionary is not empty and has entries
			if (
				self.File.Contents(folder["Played"]["entries"])["lines"] != [] and
				self.JSON.To_Python(folder["Played"]["entries"])["Entries"] != []
			):
				self.dictionaries["Played"] = self.JSON.To_Python(folder["Played"]["entries"])

			# Update the number of entries with the length of the entries list
			self.dictionaries["Played"]["Numbers"]["Total"] = len(self.dictionaries["Played"]["Entries"])

			# Define the "Played" dictionary inside the data dictionary
			game["Played"] = deepcopy(self.dictionaries["Played"])

			# Write the default or updated dictionary into the "Played.json" file
			self.JSON.Edit(folder["Played"]["entries"], self.dictionaries["Played"])

			# --------------- #

			# Create the "Gaming time" folder
			folder["Gaming time"] = {
				"root": root_folder + self.language_texts["gaming_time"] + "/"
			}

			self.Folder.Create(folder["Gaming time"]["root"])

			# Create the "Gaming time" files
			files = [
				"Gaming time.json",
				self.language_texts["gaming_time"] + ".txt"
			]

			for file in files:
				key = file.split(".")[0]

				if key == self.language_texts["gaming_time"]:
					key = "Language gaming time"

				folder["Gaming time"][key] = folder["Gaming time"]["root"] + file
				self.File.Create(folder["Gaming time"][key])

			# Define the "Gaming time" dictionary as a template
			gaming_time = {
				"Units": {
					"Years": 0,
					"Months": 0,
					"Days": 0,
					"Hours": 0,
					"Minutes": 0,
					"Seconds": 0
				},
				"Text": {},
				"Times": {
					"First": "",
					"Added": "",
					"Last": ""
				}
			}

			# Get the "Time" dictionary from the file if the file is not empty
			if self.File.Contents(folder["Gaming time"]["Gaming time"])["lines"] != []:
				gaming_time = self.JSON.To_Python(folder["Gaming time"]["Gaming time"])

			# ----- #

			# Update the "Last played time"

			entries_file = folder["Played"]["entries"]

			# If the file exists and it is not empty
			if (
				self.File.Exist(entries_file) == True and
				self.File.Contents(entries_file)["lines"] != []
			):
				# Read the "Entries.json" file
				entries = self.JSON.To_Python(entries_file)

				# Get the entry dictionaries
				dictionaries = list(entries["Dictionary"].values())

				if dictionaries != []:
					# Get the last entry
					last_entry = dictionaries[-1]

					# Update the "Last played time"
					gaming_time["Times"]["Last"] = last_entry["Date"]

			# ----- #

			# Create the gaming time text
			gaming_time = self.Make_Gaming_Time_Text(game, gaming_time)

			# Define the "Gaming time" key inside the sub-game dictionary if the item is the "Sub-game" one
			if item == "Sub-game":
				dictionary["Game"]["Sub-game"]["Gaming time"] = gaming_time

			# If the item is not "Sub-game"
			if item != "Sub-game":
				game["Gaming time"] = gaming_time

			# Write the default or updated dictionary into the "Gaming time.json" file
			self.JSON.Edit(folder["Gaming time"]["Gaming time"], gaming_time)

			# Write the language gaming time into the language gaming time file if the text is not an empty string
			if gaming_time["Text"][self.user_language] != "":
				self.File.Edit(folder["Gaming time"]["Language gaming time"], gaming_time["Text"][self.user_language], "w")

		# --------------- #

		# Define the game details
		if "Details" not in game:
			game["Details"] = self.File.Dictionary(game["Folders"]["details"])

		# Edit the game details file with the details above (or the one that already existed in the dictionary)
		self.File.Edit(game["Folders"]["details"], self.Text.From_Dictionary(game["Details"]), "w")

		# Define the game titles
		dictionary = self.Define_Game_Titles(dictionary, self.define_item)

		# Define the "Local" folder dictionary
		game["Folders"]["Local"] = {
			"root": ""
		}

		# Define stuff that only needs to be defined for the base game, not for sub-games
		if self.define_item == False:
			# Define the default game language as the user language
			game["Language"] = self.full_user_language

			# Change user language to original game language if the key exists inside the game details
			if self.Language.language_texts["original_language"] in game["Details"]:
				game["Language"] = game["Details"][self.Language.language_texts["original_language"]]

			if game["Language"] in list(self.languages["full"].values()):
				# Iterate through full languages list to find small language from the full language
				for small_language in self.languages["full"]:
					full_language = self.languages["full"][small_language]

					if full_language == game["Language"]:
						game["Language"] = small_language

			game["Platform"] = game["Details"][self.Language.language_texts["platform, title()"]]

			i = 0
			for platform in self.game_types["Platforms"][self.user_language]:
				if platform == game["Platform"]:
					game["Platform"] = {}

					for language in self.languages["small"]:
						game["Platform"][language] = self.game_types["Platforms"][language][i]

				i += 1

			# Define the game states dictionary
			states = {
				"Re-playing": False,
				"Christmas": False,
				"Completed game": False,
				"First game session in year": False,
				"First game type session in year": False,
				"Finished playing": False,
				"Remote game": False,
				"Has sub-games": False
			}

			if "States" in game:
				game["States"].update(states)

			elif "States" not in game:
				game["States"] = states

			if self.Today_Is_Christmas == True:
				game["States"]["Christmas"] = True

			# Define Re-playing state for Re-playing status
			if (
				self.Language.language_texts["status, title()"] in game["Details"] and
				game["Details"][self.Language.language_texts["status, title()"]] == self.language_texts["re_playing, title()"]
			):
				game["States"]["Re-playing"] = True

			game["States"]["First game session in year"] = False

			if self.dictionaries["Sessions"]["Numbers"]["Total"] == 0:
				game["States"]["First game session in year"] = True

			game["States"]["First game type session in year"] = False

			if self.dictionaries["Game type"][dictionary["Type"]["Type"]["en"]]["Numbers"]["Total"] == 0:
				game["States"]["First game type session in year"] = True

			# Define the game "Files" dictionary
			game["Files"] = {
				"Shortcut": {
					"File": dictionary["Type"]["Folders"]["Shortcuts"]["root"] + self.Sanitize(game["Title"], restricted_characters = True),
					"Path": ""
				}
			}

			# Try to find the game shortcut
			found_shortcut = False

			for extension in [".lnk", ".url"]:
				file = game["Files"]["Shortcut"]["File"] + extension

				if self.File.Exist(file) == True:
					game["Files"]["Shortcut"]["File"] += extension

					found_shortcut = True

			# If the shortcut is found, get its path
			if found_shortcut == True:
				import win32com.client

				shell = win32com.client.Dispatch("WScript.Shell")

				game["Files"]["Shortcut"]["Path"] = shell.CreateShortCut(game["Files"]["Shortcut"]["File"]).Targetpath.replace("\\", "/")

				if self.File.Exist(game["Files"]["Shortcut"]["Path"]) == False:
					game["Files"]["Shortcut"]["Path"] += "/"

			# Define the bat File for the game if it exists
			file = self.Folder.folders["Apps"]["Shortcuts"]["root"] + self.Sanitize(game["Title"], restricted_characters = True) + ".bat"

			if self.File.Exist(file) == True:
				game["Files"]["Bat"] = file

			# Create the local game folder
			root_folder = self.Folder.folders["Games"]["Folders"]["root"]

			# Add the "Root folder" of the same key of the game details dictionary if it exists
			if self.Folder.language_texts["root_folder"] in game["Details"]:
				root_folder += game["Details"][self.Folder.language_texts["root_folder"]] + "/"

			# Define the list of game types that has a sub-folder
			sub_folder_types = [
				"Flash",
				"Nintendo 64",
				"Super Nintendo"
			]

			# If the type of the game is one of the three types in the list
			if dictionary["Type"]["Type"]["en"] in sub_folder_types:
				# Add the type sub-folder
				root_folder += dictionary["Type"]["Type"]["en"] + "/"

			# Define the game folder as the sanitized game title with restricted characters
			game_folder = self.Sanitize(game["Title"], restricted_characters = True)

			# If the "Folder" key is inside the game details dictionary
			if self.Folder.language_texts["folder, title()"] in game["Details"]:
				# Use its value as the game folder
				game_folder = game["Details"][self.Folder.language_texts["folder, title()"]]

			# Define the local game folder as the game folder added to the root folder with a slash
			game["Folders"]["Local"] = {
				"root": root_folder + game_folder + "/"
			}

			if (
				self.Folder.language_texts["root_folder"] in game["Details"] or
				dictionary["Type"]["Type"]["en"] in sub_folder_types
			):
				# Define the root folder of the game folders dictionary
				game["Folders"]["Local folder"] = {
					"root": root_folder,
					"Game": game["Folders"]["Local"]["root"]
				}

			# Add the game files to the "Folders" dictionary
			game["Folders"]["Shortcut"] = game["Files"]["Shortcut"]

			if "Bat" in game["Files"]:
				game["Folders"]["Bat"] = game["Files"]["Bat"]

			# If the "Create folder" key is not inside the game details dictionary
			if self.Folder.language_texts["create_folder"] not in game["Details"]:
				# If the platform of the game is not Console, Mobile, Super Nintendo, or Nintendo 64
				# And the type of the game is not Flash, Nintendo 64, or Super Nintendo
				# And the "Steam" key is not inside the game details dictionary
				# And the "steam" or "https" texts are not inside the path of the shortcut of the game
				if (
					game["Platform"]["en"] not in ["Console", "Mobile", "Super Nintendo", "Nintendo 64"] and
					dictionary["Type"]["Type"]["en"] not in ["Flash", "Nintendo 64", "Super Nintendo"] and
					self.Language.language_texts["steam, title()"] not in game["Details"] and
					"steam://" not in game["Files"]["Shortcut"]["Path"] and
					"https://" not in game["Files"]["Shortcut"]["Path"]
				):
					# Create the game folder
					self.Folder.Create(game["Folders"]["Local"]["root"])

				# Else, define the local game folder as an empty string
				else:
					game["Folders"]["Local"]["root"] = ""

					game["States"]["Remote game"] = True

			else:
				game["States"]["Remote game"] = True

			# Add the "lnk" (link) or "url" extension based on local or remote game conditions, respectively
			file = game["Folders"]["Shortcut"]["File"]

			if (
				game["States"]["Remote game"] == False and
				".lnk" not in file
			):
				game["Folders"]["Shortcut"]["File"] += ".lnk"

			if (
				game["States"]["Remote game"] == True and
				".url" not in file
			):
				game["Folders"]["Shortcut"]["File"] += ".url"

			# ------------------------------ #

			# Define the "sub-game types" list
			self.dictionaries["Sub-game types"] = [
				"DLCs"
			]

			# Define the default key for the sub-game type
			key = "DLCs"

			# Get the sub-game type from the game details if it is present
			if self.language_texts["sub_game_type"] in game["Details"]:
				# Define the "Sub-game type" text key
				text_key = self.language_texts["sub_game_type"]

				# Get the sub-game type key
				key = game["Details"][text_key]

				# Define the "Has sub-games" state as True
				game["States"]["Has sub-games"] = True

			# Else, try to find a folder which is named after one of the sub-game types
			else:
				# Get the list of folders
				folders = self.Folder.Contents(game["Folders"]["root"])["folder"]["names"]

				# Iterate through the list of folderse
				for folder in folders:
					# If the folder is inside the list of sub-game types
					if folder in self.dictionaries["Sub-game types"]:
						# Define the key as the folder name
						key = folder

						# Define the "Has sub-games" state as True
						game["States"]["Has sub-games"] = True

			# If the "Has sub-games" state is True
			if game["States"]["Has sub-games"] == True:
				# Define the "Key" key
				dictionary["Key"] = key

				# Update the "Game" key
				dictionary["Game"] = game

				# Define the sub-games
				value = self.Define_Sub_Games(dictionary, play = play)

				if value["Game"]["Sub-game"]["Title"] != dictionary["Game"]["Title"]:
					dictionary = value

			# ------------------------------ #

		return dictionary

	def Define_Sub_Games(self, dictionary, play = False, sub_game_title = None):
		# Define the "game" variable for easier typing
		game = dictionary["Game"]

		# Define the sub-game type dictionary
		game["Sub-game type"] = {
			"Key": dictionary["Key"],
			"Texts": {
				"Singular": {},
				"Plural": {}
			},
			"Folders": {},
			"Items": {
				"Number": 0,
				"Current": "",
				"List": [],
				"Language list": [],
				"Dictionary": {}
			}
		}

		# Get the sub-game type from the game details if it is present
		if self.language_texts["sub_game_type"] in game["Details"]:
			key = self.language_texts["sub_game_type"]

			game["Sub-game type"]["Key"] = game["Details"][key]

		# Define the sub-game type variable for easier typing
		subgame_type = game["Sub-game type"]["Key"]

		# Iterate through the text types list
		for text_type in ["Singular", "Plural"]:
			# Iterate through the small languages list
			# To define the sub-game type texts for all languages
			for language in self.languages["small"]:
				# Define the text key
				text_key = subgame_type[:-1].lower().replace(" ", "_")

				# Add the "s" letter to make the text plural if the current text type is "plural"
				# Only if the "s" letter is not at the end of the word
				if (
					text_type == "Plural" and
					text_key[-1] != "s"
				):
					text_key += "s"

				if "_" not in text_key:
					text_key += ", title()"

				if text_key not in self.language_texts:
					text_key = text_key.replace("title", "upper")

				# Get the language text
				text = self.texts[text_key][language]

				# Define the language text inside the "Text" dictionary, inside the correct text type dictionary
				game["Sub-game type"]["Texts"][text_type][language] = text

		# Create the "Sub-game type" folder
		game["Folders"][subgame_type] = {
			"root": game["Folders"]["root"] + game["Sub-game type"]["Texts"]["Plural"][self.user_language] + "/"
		}

		self.Folder.Create(game["Folders"][subgame_type]["root"])

		# Define the root folder of the "Sub-game type" dictionary
		game["Sub-game type"]["Folders"] = deepcopy(game["Folders"][subgame_type])

		# Create the sub-game type files
		file_names = [
			"List",
			"Current"
		]

		# Iterate through the file names list
		for name in file_names:
			# Define the text key
			text_key = name.lower().replace(" ", "_")

			if "_" not in text_key:
				text_key += ", title()"

			# Get the user language text to use it as the file name
			text = self.Language.language_texts[text_key]

			# Define the file name inside the "Folders" dictionary
			game["Sub-game type"]["Folders"][name] = game["Sub-game type"]["Folders"]["root"] + text + ".txt"

			# Create the file
			self.File.Create(game["Sub-game type"]["Folders"][name])

			# Get the contents of the file
			file = game["Sub-game type"]["Folders"][name]

			# Get the file contents
			contents = self.File.Contents(file)["lines"]

			# If the name is "Current"
			if name == "Current":
				# And the file is not empty
				if contents != []:
					# Define the contents as the first line of the text file
					contents = contents[0]

				# If the file is empty, define the contents as an empty string
				if contents == []:
					contents = ""

			# Define the contents inside the dictionary
			game["Sub-game type"]["Items"][name] = contents

			# If the name is "List"
			if name == "List":
				# Define the items number as the number of lines of the text file
				game["Sub-game type"]["Items"]["Number"] = len(game["Sub-game type"]["Items"]["List"])

		if game["Sub-game type"]["Items"]["List"] == []:
			# Define the list of sub-games inside the dictionary as the list of folders
			game["Sub-game type"]["Items"]["List"] = self.Folder.Contents(game["Sub-game type"]["Folders"]["root"])["folder"]["names"]

			# Update the "List.txt" file
			self.File.Edit(game["Sub-game type"]["Folders"]["List"], self.Text.From_List(game["Sub-game type"]["Items"]["List"], next_line = True), "w")

		# Update the number of sub-games
		game["Sub-game type"]["Items"]["Number"] = len(game["Sub-game type"]["Items"]["List"])

		# Define the current sub-game as the first one if it is empty
		if game["Sub-game type"]["Items"]["Current"] == "":
			# Define the first sub-game variable for easier typing
			first_sub_game = game["Sub-game type"]["Items"]["List"][0]

			# Define the current sub-game
			game["Sub-game type"]["Items"]["Current"] = first_sub_game

			# Update the "Current.txt" file
			self.File.Edit(game["Sub-game type"]["Folders"]["Current"], first_sub_game, "w")

		# Iterate through the sub-games
		for sub_game in game["Sub-game type"]["Items"]["List"]:
			# Define the sub-game dictionary
			sub_game = {
				"Title": sub_game,
				"Titles": {}
			}

			# If the title of the sub-game is the same the as the game title
			if sub_game["Title"] == game["Title"]:
				# Update the titles dictionary
				sub_game["Titles"] = game["Titles"]

			# Define the sub-game dictionary inside the "Game" dictionary
			game["Sub-game"] = deepcopy(sub_game)

			# If the title of the sub-game is not the same the as the game title
			if sub_game["Title"] != game["Title"]:
				# Select the sub-game to define its variables
				dict_ = self.Select_Game(dictionary, define_item = True)

				if "Sub-game" in dictionary["Game"]:
					# Update the sub-game variable
					sub_game = dictionary["Game"]["Sub-game"]

			# Add the sub-game dictionary to the items dictionary
			game["Sub-game type"]["Items"]["Dictionary"][sub_game["Title"]] = sub_game

			# Add the language sub-game title to the language list
			game["Sub-game type"]["Items"]["Language list"].append(sub_game["Titles"]["Language"])

		# Ask the user to select a sub-game
		parameters = {
			"options": game["Sub-game type"]["Items"]["List"],
			"language_options": game["Sub-game type"]["Items"]["Language list"],

			"show_text": game["Sub-game type"]["Texts"]["Plural"][self.user_language],
			"select_text": self.Language.language_texts["select_an_item_from_the_list"]
		}

		# Sanitize the language titles
		i = 0
		for title in parameters["language_options"]:
			title = self.Sanitize_Title(title)

			parameters["language_options"][i] = title

			i += 1

		if (
			sub_game_title == None and
			play == True
		):
			# Select the sub-game
			game["Sub-game"] = self.Input.Select(**parameters)["option"]

		else:
			# Define the sub-game title
			game["Sub-game"] = sub_game_title

		# If the sub-game title is not the same as the game title
		if (
			game["Sub-game"] != None and
			game["Sub-game"] != game["Title"]
		):
			# Get the sub-game dictionary
			game["Sub-game"] = game["Sub-game type"]["Items"]["Dictionary"][game["Sub-game"]]

		# Else, define the sub-game dictionary as a dictionary with only the game titles
		else:
			game["Sub-game"] = {
				"Title": game["Title"],
				"Titles": game["Titles"],
				"Folders": game["Folders"]
			}

			# Select the game to define its variables
			dict_ = self.Select_Game(dictionary, define_item = True)["Game"]["Sub-game"]

			game["Sub-game"]["Folders"] = dict_["Folders"]

			game["Sub-game"]["Gaming time"] = dict_["Gaming time"]

		# Define the title as the game title in the user language
		title = game["Titles"]["Language"]

		# Define the sub-game title variable for easier typing
		sub_game_title = game["Sub-game"]["Titles"]["Language"]

		# If the first two characters of the title are not a colon and a space
		if sub_game_title[0] + sub_game_title[1] != ": ":
			# Add a slash
			title += " - "

		# Add the sub-game title
		title += sub_game_title

		# Define the "sub-game title with the game title" text
		game["Sub-game"]["With game title"] = title

		return dictionary

	def Select_Game_Type_And_Game(self, options = None, game_title = None, play = False):
		dictionary = {
			"Type": {
				"Select": True,
				"Status": [
					self.texts["plan_to_play, title()"]["en"],
					self.texts["playing, title()"]["en"],
					self.texts["re_playing, title()"]["en"],
					self.Language.texts["on_hold, title()"]["en"]
				]
			},
			"Game": {
				"Select": True,
				"List": {}
			}
		}

		if options != None:
			dictionary = self.Define_Options(dictionary, options)

		if dictionary["Type"]["Select"] == True:
			if game_title == None:
				dictionary["Type"] = self.Select_Game_Type(dictionary["Type"])

			# If the game is not "None"
			# The selected game must have come from the command line argument "- game"
			if game_title != None: 
				# Iterate through the game types
				for game_type in self.game_types["Types"]["en"]:
					# Get the game type dictionary
					game_type = self.game_types[game_type]

					if game_title in game_type["Game list"]:
						dictionary["Type"] = game_type

		if dictionary["Game"]["Select"] == True:
			dictionary["Game"] = self.Select_Game(dictionary, play = play, game_title = game_title)["Game"]

		return dictionary

	def Define_States_Dictionary(self, dictionary):
		states_dictionary = {
			"States": {},
			"Texts": {}
		}

		# Define the keys for the states
		keys = [
			"Re-playing",
			"Christmas",
			"Completed game",
			"First game session in year",
			"First game type session in year"
		]

		state_texts = {
			"Re-playing": "Re-played",
			"Completed game": "Completed the game"
		}

		# Iterate through the states keys
		for key in keys:
			# If the state is True
			if dictionary["Game"]["States"][key] == True:
				# If the key has a different state text, get it
				if key in state_texts:
					key = state_texts[key]

				state = True

				# Define the state dictionary
				states_dictionary["States"][key] = state

				# Define the state texts of the current state dictionary
				states_dictionary["Texts"][key] = {}

				for language in self.languages["small"]:
					text = ""

					if key != "First game type session in year":
						text_key = key.lower()

						if " " not in text_key:
							text_key += ", title()"

						if ", title()" not in text_key:
							text_key = text_key.replace(" ", "_")

						if text_key in self.Language.texts:
							text = self.Language.texts[text_key][language]

						else:
							text = self.texts[text_key][language]

					if key == "First game type session in year":
						entry_item = dictionary["Type"]["Type"][language]

						text = self.texts["first_game_session_of_the_{}_category_in_year"][language].format(entry_item)

					states_dictionary["Texts"][key][language] = text

		return states_dictionary

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

			if type(options[key]) in [str, list]:
				dictionary[key] = options[key]

		return dictionary

	def Define_Game_Titles(self, dictionary, define_item = False):
		game = dictionary["Game"]

		# If the define item variable is True
		# And the sub-game is not the root game
		if (
			self.define_item == True and
			game["Sub-game"]["Title"] != game["Title"]
		):
			game = game["Sub-game"]

		if self.File.Exist(game["Folders"]["details"]) == True:
			game["Details"] = self.File.Dictionary(game["Folders"]["details"])

			# Define titles key
			game["Titles"] = {
				"Original": game["Details"][self.Language.language_texts["title, title()"]],
				"Sanitized": game["Details"][self.Language.language_texts["title, title()"]],
			}

			game["Titles"]["Language"] = game["Titles"]["Original"]

			# If the "romanized_title" key exists inside the game details, define the romanized name and ja name
			if self.Language.language_texts["romanized_title"] in game["Details"]:
				if self.Language.language_texts["romanized_title"] in game["Details"]:
					game["Titles"]["Romanized"] = game["Details"][self.Language.language_texts["romanized_title"]]
					game["Titles"]["Language"] = game["Titles"]["Romanized"]

				if "Romanized" in game["Titles"]:
					game["Titles"]["Sanitized"] = game["Titles"]["Romanized"]

				game["Titles"]["ja"] = game["Details"][self.Language.language_texts["title, title()"]]

			if (
				" (" in game["Titles"]["Original"] and
				" (" not in game["Titles"]["Language"]
			):
				game["Titles"]["Language"] = game["Titles"]["Language"] + " (" + game["Titles"]["Original"].split(" (")[-1]

				if self.user_language in game["Titles"]:
					game["Titles"][self.user_language] = game["Titles"][self.user_language] + " (" + game["Titles"]["Original"].split(" (")[-1]

			# Define game titles per language
			for language in self.languages["small"]:
				key = self.Language.texts["title_in_language"][language][self.user_language]

				if key in game["Details"]:
					game["Titles"][language] = game["Details"][key]

			game["Titles"]["Language"] = game["Titles"]["Original"]

			if self.user_language in game["Titles"]:
				game["Titles"]["Language"] = game["Titles"][self.user_language]

			if (
				self.user_language not in game["Titles"] and
				"Romanized" in game["Titles"]
			):
				game["Titles"]["Language"] = game["Titles"]["Romanized"]

			# Sanitize the language title
			game["Titles"]["Language sanitized"] = self.Sanitize_Title(game["Titles"]["Language"])

			# Sanitize the game title
			game["Titles"]["Sanitized"] = self.Sanitize_Title(game["Titles"]["Sanitized"])

		return dictionary

	def Sanitize_Title(self, title):
		# If the number of characters in the title is more than one
		# And the first two characters of the title are a colon and a space
		if (
			len(title) > 1 and
			title[0] + title[1] == ": "
		):
			# Remove the colon and a space
			title = title[2:]

		if ". " in title:
			title = title.replace(". ", " ")

		elif "." in title:
			title = title.replace(".", "")

		title = self.Sanitize(title, restricted_characters = True)

		return title

	def Calculate_Gaming_Time(self, dictionary, item = False):
		# Define the game variable
		game = deepcopy(dictionary["Game"])

		# If the item parameter is True, define the game variable as the sub-game
		if item == True:
			game = deepcopy(game["Sub-game"])

		# Get the entry if it exists
		if "Entry" in dictionary:
			entry = dictionary["Entry"]

		# Define the first and last times
		for key in ["First", "Last"]:
			sub_key = "Before"

			if key == "Last":
				sub_key = "After"

			# If the time string is empty
			if game["Gaming time"]["Times"][key] == "":
				# Get it from the session duration inside the entry
				game["Gaming time"]["Times"][key] = entry["Session duration"][sub_key]["UTC"]["DateTime"]["Formats"]["YYYY-MM-DDTHH:MM:SSZ"]

			# If the key is "Last"
			# And the time string is not empty
			if (
				key == "Last" and
				game["Gaming time"]["Times"][key] != ""
			):
				# Get it from the session duration inside the entry
				game["Gaming time"]["Times"][key] = entry["Session duration"][sub_key]["UTC"]["DateTime"]["Formats"]["YYYY-MM-DDTHH:MM:SSZ"]

			# Create the date dictionary of the played time
			game["Gaming time"]["Times"][key] = self.Date.From_String(game["Gaming time"]["Times"][key])

		# Iterate through the time difference keys
		for key, difference in entry["Session duration"]["Difference"].items():
			# Add the difference to the game units
			game["Gaming time"]["Units"][key] += difference

			# Define the division number
			division_number = 60

			if key == "Hours":
				division_number = 24

			# Make the division
			division = divmod(game["Gaming time"]["Units"][key], division_number)

			# Define the divison_has_remainder variable
			divison_has_remainder = False

			# If the key is hours and there is more than 24 hours
			# Add days
			if (
				key == "Hours" and
				division[1] != 0
			):
				# Add the days to the days key
				game["Gaming time"]["Units"]["Days"] += division[0]

			# If the key is minutes and there is more than 60 minutes
			# Add hours and change minutes
			if (
				key == "Minutes" and
				division[1] != 0
			):
				# Add hours to the hours key
				game["Gaming time"]["Units"]["Hours"] += division[0]

			# If the key is seconds and there is more than 60 seconds
			# Add minutes and change seconds
			if (
				key == "Seconds" and
				division[1] != 0
			):
				# Add minutes to the minutes key
				game["Gaming time"]["Units"]["Minutes"] += division[0]

			# Update the difference
			game["Gaming time"]["Units"][key] = division[1]

		# Create a local time units dictionary
		dict_ = {}

		# Create a list of keys
		keys = [
			"days",
			"hours",
			"minutes",
			"seconds"
		]

		# Iterate through the time difference keys
		for key in keys:
			# If the key is in the time units dictionary
			if key.capitalize() in game["Gaming time"]["Units"]:
				# Add the key to the local dictionary
				dict_[key] = game["Gaming time"]["Units"][key.capitalize()]

		# Define the added time as the first time
		game["Gaming time"]["Times"]["Added"] = deepcopy(game["Gaming time"]["Times"]["First"])

		# Add the game time difference time unit to the added time date object
		game["Gaming time"]["Times"]["Added"]["Object"] += self.Date.Relativedelta(**dict_)

		# Transform the added time into a date dictionary with the updated object (the added time above)
		game["Gaming time"]["Times"]["Added"] = self.Date.Now(game["Gaming time"]["Times"]["Added"]["Object"])

		# --------------- #

		# Make the difference between the first time and the added time
		difference = self.Date.Difference(game["Gaming time"]["Times"]["First"]["Object"], game["Gaming time"]["Times"]["Added"]["Object"])

		# Transform the times back into date strings
		for key in ["First", "Last", "Added"]:
			game["Gaming time"]["Times"][key] = self.Date.To_String(game["Gaming time"]["Times"][key], utc = True)

		# Create the gaming time text
		game["Gaming time"] = self.Make_Gaming_Time_Text(game)

		# Update the "Gaming time.json" file
		self.JSON.Edit(game["Folders"]["Gaming time"]["Gaming time"], game["Gaming time"])

		# Write the language gaming time into the language gaming time file if the text is not an empty string
		if game["Gaming time"]["Text"][self.user_language] != "":
			self.File.Edit(game["Folders"]["Gaming time"]["Language gaming time"], game["Gaming time"]["Text"][self.user_language], "w")

		return game

	def Make_Gaming_Time_Text(self, game, gaming_time = None):
		if gaming_time == None:
			# Copy the "Gaming time" dictionary and remove the unused keys
			gaming_time = deepcopy(game["Gaming time"])

		# Define the singular and plural time text lists
		singular = deepcopy(self.Date.texts["date_attributes, type: list"])
		plural = deepcopy(self.Date.texts["plural_date_attributes, type: list"])

		# Define the local time units dictionary
		time_units = deepcopy(gaming_time["Units"])

		# Iterate through the gaming time units dictionary to remove the zero time units
		# And also remove time unit texts of zero unit times from the singular and plural lists
		i = 0
		for key in gaming_time["Units"].copy():
			# Get the time unit
			time_unit = gaming_time["Units"][key]

			# If the time unit is zero
			if time_unit == 0:
				# Remove the time from the units dictionary
				time_units.pop(key)

				# Iterate through the small languages list
				# And remove the singular and plural time unit texts
				for language in self.languages["small"]:
					# Define the language key inside the "Text" dictionary
					gaming_time["Text"][language] = ""

					# Define the text key
					text_key = key.lower()[:-1] + ", title()"

					# Define the singular unit text
					singular_text = self.Date.texts[text_key][language].lower()

					# Remove the singular text as the time unit is zero
					if singular_text in singular[language]:
						singular[language].remove(singular_text)

					# Define the text key
					text_key = key.lower() + ", title()"

					# Define the plural unit text
					plural_text = self.Date.texts[text_key][language].lower()

					# Remove the plural text as the time unit is zero
					if plural_text in plural[language]:
						plural[language].remove(plural_text)

			i += 1

		# Iterate through the gaming time units dictionary
		keys = list(time_units.keys())

		i = 0
		for key, time_unit in time_units.items():
			# Iterate through the small languages list
			for language in self.languages["small"]:
				# If the time unit key is not the first one
				if key != keys[0]:
					# Define the end of text for easier typing
					end_of_text = gaming_time["Text"][language][-1] + gaming_time["Text"][language][-2]

					# If the number of time units is more than one
					# And not two
					# And the end of the gaming time text does not contain a space and a comma, or a comma and a space
					if (
						len(time_units) > 1 and
						len(time_units) != 2 and
						end_of_text not in [" ,", ", "]
					):
						# Add a comma and a space to the gaming time
						gaming_time["Text"][language] += ", "

					# If the number of time units is two
					if len(time_units) == 2:
						# Add the " and " text
						gaming_time["Text"][language] += " " + self.Language.texts["and"][language] + " "

				# If the time unit key is the last one
				# And the number of time units is more than two
				if (
					key == keys[-1] and
					len(time_units) > 2
				):
					# Define the end of text for easier typing
					end_of_text = gaming_time["Text"][language][-1] + gaming_time["Text"][language][-2]

					# If the end of the gaming time text does not contain a space and a comma
					if end_of_text != " ,":
						# Add a comma and a space to the gaming time
						gaming_time["Text"][language] += ", "

					# Add the " and " text
					gaming_time["Text"][language] += self.Language.texts["and"][language] + " "

				# Add the time unit to the full gaming time text
				gaming_time["Text"][language] += str(time_unit)

				# Define the default time unit text list as the singular one 
				list_ = singular[language]

				# If the time unit is more than one, define the time unit text list as the plural one
				if time_unit > 1:
					list_ = plural[language]

				# Add a space and the time unit text to the full gaming time text
				gaming_time["Text"][language] += " " + list_[i]

			i += 1

		return gaming_time

	def Get_Language_Status(self, status):
		return_english = False

		if status in self.texts["statuses, type: list"][self.user_language]:
			return_english = True

		s = 0
		for english_status in self.texts["statuses, type: list"]["en"]:
			# Return the user language status
			if (
				return_english == False and
				english_status == status
			):
				status_to_return = self.texts["statuses, type: list"][self.user_language][s]

			# Return the English status
			if (
				return_english == True and
				status == self.texts["statuses, type: list"][self.user_language][s]
			):
				status_to_return = english_status

			s += 1

		return status_to_return

	def Change_Status(self, dictionary, status = ""):
		if status == "":
			status = self.Language.language_texts["completed, title()"]

		# Update the status key in the game details
		dictionary["Game"]["Details"][self.Language.language_texts["status, title()"]] = status

		# Update the game details file
		self.File.Edit(dictionary["Game"]["Folders"]["details"], self.Text.From_Dictionary(dictionary["Game"]["Details"]), "w")

		self.Check_Status(dictionary)

	def Check_Status(self, dictionary):
		game_type = dictionary

		if (
			"Type" in dictionary and
			"JSON" in dictionary["Type"]
		):
			game_type = dictionary["Type"]

			self.language_status = dictionary["Game"]["Details"][self.Language.language_texts["status, title()"]]

			# Get the English status from the language status of the game details
			status = self.Get_Language_Status(self.language_status)

		dictionary["JSON"] = self.JSON.To_Python(game_type["Folders"]["Information"]["Information"])

		# Update the number of games
		dictionary["JSON"]["Number"] = len(dictionary["JSON"]["Titles"])

		# Sort the titles list
		dictionary["JSON"]["Titles"] = sorted(dictionary["JSON"]["Titles"], key = str.lower)

		titles = []

		if (
			"Type" in dictionary and
			"JSON" not in dictionary["Type"]
		):
			titles.extend(dictionary["JSON"]["Titles"])

		if (
			"Type" in dictionary and
			"JSON" in dictionary["Type"]
		):
			titles.append(dictionary["Game"]["Title"])

		# Iterate through the statuses list
		for playing_status in self.texts["statuses, type: list"]["en"]:
			for game_title in titles:
				if (
					"Type" in dictionary and
					"JSON" not in dictionary["Type"]
				):
					folder = game_type["Folders"]["Information"]["root"] + self.Sanitize_Title(game_title) + "/"
					details_file = folder + self.Language.language_texts["details, title()"] + ".txt"
					details = self.File.Dictionary(details_file)

					self.language_status = details[self.Language.language_texts["status, title()"]]

					# Get the English status from the language status of the game details
					status = self.Get_Language_Status(self.language_status)

				# If the game status is equal to the playing status
				# And the game is not in the correct status list, add it to the list
				if (
					status == playing_status and
					game_title not in dictionary["JSON"]["Status"][playing_status]
				):
					dictionary["JSON"]["Status"][playing_status].append(game_title)

				# If the game status is not equal to the playing status
				# And the game is in the wrong playing status list, remove it from the list
				if (
					status != playing_status and
					game_title in dictionary["JSON"]["Status"][playing_status]
				):
					dictionary["JSON"]["Status"][playing_status].remove(game_title)

			# Sort the games list
			dictionary["JSON"]["Status"][playing_status] = sorted(dictionary["JSON"]["Status"][playing_status], key = str.lower)

		# Update the game type "Information.json" file
		self.JSON.Edit(game_type["Folders"]["Information"]["Information"], dictionary["JSON"])

		return dictionary

	def Define_Title(self, title, language = None):
		if language == None:
			language = self.user_language

		keys = [
			"Original",
			language,
			"Romanized"
		]

		for title_key in keys:
			if title_key in title:
				key = title_key

		title = title[key]

		return title

	def Define_Year_Summary_Data(self, entry, language):
		# Get the language game type
		game_type = self.game_types[entry["Type"]]["Type"][language]

		# Define the item text, with the entry title with quotes
		item = '"' + self.Define_Title(entry["Titles"], language) + '"'

		# Add the game type with a space, to the item text
		#item += " (" + game_type + ")"

		# Add a comma
		item += ", "

		# Add the session duration
		duration = deepcopy(entry["Session duration"])
		duration.pop("Text")

		duration = self.Date.Make_Time_Text(duration)[language]

		item += self.Date.texts["duration, title()"][language] + ": " + duration + ", "

		# Add the date
		date = self.Date.texts["date, title()"][language] + ": " + self.Date.From_String(entry["Date"])["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"]

		item += date

		return item

	def Show_Information(self, dictionary):
		game = dictionary["Game"]

		# Show a separator
		if "First separator" not in dictionary:
			print()
			print(self.separators["5"])

		# --------------- #

		# Show the "Game title" text
		print()
		print(self.language_texts["game_title"] + ":")

		# Show the original or romanized game title
		key = "Original"

		if "Romanized" in game["Titles"]:
			key = "Romanized"

		print("\t" + game["Titles"][key])

		# Show the language titles if they exist
		for language in self.languages["small"]:
			if language in game["Titles"]:
				print("\t" + game["Titles"][language])

		# --------------- #

		# Show the "Sub-game type" text and the sub-game title
		# If the game has sub-games and the sub-game is not the game
		if (
			game["States"]["Has sub-games"] == True and
			game["Sub-game"]["Title"] != game["Title"]
		):
			# Define the sub-game variable for easier typing
			sub_game = game["Sub-game"]

			# Show the "Sub-game type" text
			sub_game_type_text = game["Sub-game type"]["Texts"]["Singular"][self.user_language]

			print()
			print(sub_game_type_text + ":")

			# Show the original or romanized sub-game title
			key = "Original"

			if "Romanized" in sub_game["Titles"]:
				key = "Romanized"

			title = self.Sanitize_Title(sub_game["Titles"][key])

			print("\t" + title)

			# Show the language titles if they exist
			for language in self.languages["small"]:
				if language in sub_game["Titles"]:
					title = self.Sanitize_Title(sub_game["Titles"][language])

					print("\t" + title)

			# Show the "With the game title" text
			text = sub_game_type_text + " " + self.language_texts["with_the_game_title"] 

			# Get the sub-game "With game title"
			title = game["Sub-game"]["With game title"]

			print()
			print(text + ":")
			print("\t" + title)

		# --------------- #

		# Show the "Category" text
		print()
		print(self.Language.language_texts["category, title()"] + ":")

		# Show the categories
		types = []

		for language in self.languages["small"]:
			text = "\t" + dictionary["Type"]["Type"][language]

			if text not in types:
				types.append(text)

		for item in types:
			print(item)

		# --------------- #

		# Show the platforms
		print()

		platforms = []

		for language in self.languages["small"]:
			text = "\t" + dictionary["Game"]["Platform"][language]

			if text not in platforms:
				platforms.append(text)

		print(self.Language.language_texts["platform, title()"] + ":")

		for item in platforms:
			print(item)

		# --------------- #

		# Show the folders

		folders = game["Folders"]

		# If the game has sub-games and the sub-game is not the game
		if (
			game["States"]["Has sub-games"] == True and
			game["Sub-game"]["Title"] != game["Title"]
		):
			folders = sub_game["Folders"]

		# Show the root folder of the game
		if game["Folders"]["Local"]["root"] == "":
			print()
			print(self.Folder.language_texts["folder, title()"] + ":")
			print("\t" + game["Folders"]["root"])

		# Show the information and local folders
		if game["Folders"]["Local"]["root"] != "":
			print()
			print(self.Folder.language_texts["folders, title()"] + ":")
			print("\t" + self.Language.language_texts["informations, title()"] + ":")
			print("\t" + folders["root"])
			print()
			print("\t" + self.Language.language_texts["local, title()"] + ":")
			print("\t" + game["Folders"]["Local"]["root"])

		# Show the sub-game folder if the game has sub-games and the sub-game is not the game
		if (
			game["States"]["Has sub-games"] == True and
			game["Sub-game"]["Title"] != game["Title"]
		):
			print()
			print(self.language_texts["sub_game_folder"] + ":")
			print("\t" + game["Sub-game"]["Folders"]["root"])

		# --------------- #

		# Show the shortcut file
		if self.File.Exist(game["Files"]["Shortcut"]["File"]) == True:
			print()
			print(self.File.language_texts["shortcut, title()"] + ":")
			print("\t" + game["Files"]["Shortcut"]["File"])

		# Show the shortcut path
		if game["Files"]["Shortcut"]["Path"] != "":
			print()
			print(self.Language.language_texts["path, title()"] + ":")
			print("\t" + game["Files"]["Shortcut"]["Path"])

		# --------------- #

		# Show information about the game session played
		if "Entry" in dictionary:
			print()

			# --------------- #

			# Show when the user finished playing
			print(self.language_texts["when_you_finished_playing"] + ":")
			print("\t" + dictionary["Entry"]["Dates"]["Timezone"])
			print()

			# Show the session duration text
			print(self.Language.language_texts["session_duration"] + ":")
			print("\t" + dictionary["Entry"]["Session duration"]["Text"][self.user_language])

			# --------------- #

			# Show the dates when the user started and finished playing the game, if the user finished the game
			if "Dates" in game:
				print()
				print(self.Date.language_texts["dates, title()"] + ":")

				for key, value in game["Dates"].items():
					print("\t" + key + ":")
					print("\t" + value)

			# --------------- #

			# If there are states, show them
			if (
				"States" in dictionary and
				dictionary["States"]["Texts"] != {}
			):
				print()
				print(self.Language.language_texts["states, title()"] + ":")

				for key in dictionary["States"]["Texts"]:
					print("\t" + dictionary["States"]["Texts"][key][self.user_language])

			# If there is a session description, show it
			if "Description" in self.dictionary["Entry"]["Diary Slim"]:
				print()
				print(self.Language.language_texts["description, title()"] + ":")

				# Define the "description" variable for easier typing and a more beautiful code
				description = self.dictionary["Entry"]["Diary Slim"]["Description"]["lines"]

				# Show the description lines
				for line in description:
					print("\t" + line)