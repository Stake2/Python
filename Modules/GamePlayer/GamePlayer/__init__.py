# GamePlayer.py

# Import the "importlib" module
import importlib

class GamePlayer(object):
	def __init__(self):
		# Define the module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Import classes method
		self.Import_Classes()

		# Folders and files method
		self.Define_Folders_And_Files()

		# Class methods
		self.Define_Types()
		self.Define_Registry_Format()

	def Define_Basic_Variables(self):
		from copy import deepcopy

		# Import the JSON module
		from Utility.JSON import JSON as JSON

		self.JSON = JSON()

		# Get the modules list
		self.modules = self.JSON.To_Python(self.folders["apps"]["modules"]["modules"])

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

	def Import_Classes(self):
		# Import the "importlib" module
		import importlib

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
		if self.switches["verbose"] == True:
			print()
			print(self.JSON.Language.language_texts["arguments, title()"] + ":")
			print()

			self.JSON.Show(self.arguments)

			print()
			print(self.large_bar)

	def Define_Types(self):
		self.game_types = self.JSON.To_Python(self.folders["Data"]["Types"])

		self.game_types.update({
			"Genders": self.JSON.Language.texts["genders, type: dict"],
			"Gender items": self.JSON.Language.texts["gender_items"],
			"Game list": {
				"Number": 0,
				"Numbers": {}
			}
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
					self.JSON.Language.texts["on_hold, title()"]["en"]
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

			# Edit the "Information.json" file with the new dictionary
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

			i += 1

		# Write the game types dictionary into the "Types.json" file
		self.JSON.Edit(self.folders["Data"]["Types"], self.game_types)

		# Update the game list inside the root "Information.json" dictionary
		info_dictionary.update(self.game_types["Game list"])

		# Update the root "Information.json" file
		self.JSON.Edit(self.folders["Information"]["Information"], info_dictionary)

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
			year = str(year)

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

		# Update the "History.json" file with the new History dictionary
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

			# Update the per game type "Sessions.json" file with the updated per game type Sessions dictionary
			self.JSON.Edit(self.folders["Play History"]["Current year"]["Per Game Type"][key]["Sessions"], self.dictionaries["Game type"][game_type])

		# Update the "Sessions.json" file with the updated Sessions dictionary
		self.JSON.Edit(self.folders["Play History"]["Current year"]["Sessions"], self.dictionaries["Sessions"])

	def Get_Game_List(self, dictionary, status = None):
		'''

		Returns a game list of a specific game type that contains a game status

			Parameters:
				dictionary (dict): a game_type dictionary containing the game type folders
				status (str or list): a status string or list used to get the game that has that status

			Returns:
				game_list (list): The game list that contains the game that has the passed status string or list

		'''

		# Get the status list from the game type dictionary
		status_list = dictionary["Status"].copy()

		# If the status parameter is not None, use it as the status
		if status != None:
			status_list = status

		# If the type of the status list is string, make it a list of only the string
		if type(status_list) == str:
			status_list = [status_list]

		# Get the game type "Information.json" file and read it
		dictionary["JSON"] = self.JSON.To_Python(dictionary["Folders"]["Information"]["Information"])

		# Define the empty game list
		game_list = []

		# Add the game of each status to the game list
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
				self.JSON.Language.texts["on_hold, title()"]["en"]
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
		dictionary["Game list"] = self.Get_Game_List(dictionary, dictionary["Status"])

		# Add the game list length numbers to the game types list to show on select game type
		dictionary["Texts"]["Show"] = dictionary["Type"][self.user_language] + " (" + str(len(dictionary["Game list"])) + ")"

		return dictionary

	def Select_Game(self, options = None, game_title = None):
		from copy import deepcopy

		dictionary = {}

		if options != None:
			dictionary = self.Define_Options(dictionary, options)

		game = dictionary["Game"]

		dictionary["Texts"] = dictionary["Type"]["Texts"]

		# Define the select text
		text = dictionary["Type"]["Type"][self.user_language]

		if "Select" in dictionary["Type"]:
			text = dictionary["Type"]["Select"]

		dictionary["Texts"]["Select"] = self.language_texts["select_one_game_to_play"]

		# Select the game
		if "Title" not in game:
			language_options = dictionary["Type"]["Game list"]

			if "Game list (option)" in dictionary["Type"]:
				language_options = dictionary["Type"]["Game list (option)"]

			if game_title == None:
				title = self.Input.Select(dictionary["Type"]["Game list"], language_options = language_options, show_text = dictionary["Texts"]["Show"], select_text = dictionary["Texts"]["Select"])["option"]

			if game_title != None:
				title = game_title

			game.update({
				"Title": title
			})

		# Define the game information folder
		game["Folders"] = {
			"root": dictionary["Type"]["Folders"]["Information"]["root"] + self.Sanitize_Title(game["Title"]) + "/"
		}

		# Create the folders
		for key in game["Folders"]:
			folder = game["Folders"][key]

			if "root" in folder:
				folder = folder["root"]

			self.Folder.Create(folder)

		file_names = [
			"Details",
			"Dates"
		]

		game["Information"] = {
			"File name": "Game",
			"Key": ""
		}

		file_names.append(game["Information"]["File name"] + ".json")

		game["Information"]["Key"] = game["Information"]["File name"].lower().replace(" ", "_")

		# Define the game text files
		for file_name in file_names:
			key = file_name.lower().replace(" ", "_").replace(".json", "")

			if key == "details":
				texts_list = self.JSON.Language.language_texts

			if key == "dates":
				texts_list = self.Date.language_texts

			if ".json" not in file_name:
				file_name = texts_list[key + ", title()"] + ".txt"

			game["Folders"][key] = game["Folders"]["root"] + file_name
			self.File.Create(game["Folders"][key])

		if self.File.Contents(game["Folders"][game["Information"]["Key"]])["lines"] != []:
			game["Information"]["Dictionary"] = self.JSON.To_Python(game["Folders"][game["Information"]["Key"]])

		# Create the "Played" folder
		game["Folders"]["played"] = {
			"root": game["Folders"]["root"] + self.JSON.Language.language_texts["played, title()"] + "/"
		}

		self.Folder.Create(game["Folders"]["played"]["root"])

		# Create the "Played" files
		files = [
			"Entries.json",
			"Entry list.txt",
			"Time.json",
			self.language_texts["gaming_time"] + ".txt"
		]

		for file in files:
			key = file.lower().split(".")[0].replace(" ", "_")

			if self.language_texts["gaming_time"] in file:
				key = "gaming_time"

			game["Folders"]["played"][key] = game["Folders"]["played"]["root"] + file
			self.File.Create(game["Folders"]["played"][key])

		# Create the "Files" folder file inside the "Played" folder
		game["Folders"]["played"]["files"] = {
			"root": game["Folders"]["played"]["root"] + self.File.language_texts["files, title()"] + "/"
		}

		self.Folder.Create(game["Folders"]["played"]["files"]["root"])

		# Define the "Played" dictionary as the template
		self.dictionaries["Played"] = deepcopy(self.template)

		# Get the "Played" dictionary from file if the dictionary is not empty and has entries
		if (
			self.File.Contents(game["Folders"]["played"]["entries"])["lines"] != [] and
			self.JSON.To_Python(game["Folders"]["played"]["entries"])["Entries"] != []
		):
			self.dictionaries["Played"] = self.JSON.To_Python(game["Folders"]["played"]["entries"])

		# Update the number of entries with the length of the entries list
		self.dictionaries["Played"]["Numbers"]["Total"] = len(self.dictionaries["Played"]["Entries"])

		# Define the "Played" dictionary inside the data dictionary
		game["Played"] = deepcopy(self.dictionaries["Played"])

		# Write the default or file dictionary into the "Played.json" file
		self.JSON.Edit(game["Folders"]["played"]["entries"], self.dictionaries["Played"])

		# Define the "Time" dictionary as a template
		game["Time"] = {
			"First time": "",
			"Last time": "",
			"Added time": "",
			"Years": 0,
			"Months": 0,
			"Days": 0,
			"Hours": 0,
			"Minutes": 0,
			"Seconds": 0
		}

		# Get the "Time" dictionary from file if the dictionary is not empty
		if self.File.Contents(game["Folders"]["played"]["time"])["lines"] != []:
			game["Time"] = self.JSON.To_Python(game["Folders"]["played"]["time"])

		# Write the default or file dictionary into the "Time.json" file
		self.JSON.Edit(game["Folders"]["played"]["time"], game["Time"])

		gaming_time = self.Make_Gaming_Time_Text(game)

		# Write the gaming time into the gaming time file
		if gaming_time != "":
			self.File.Edit(game["Folders"]["played"]["gaming_time"], gaming_time, "w")

		# Define the game details
		if "Details" not in game:
			game["Details"] = self.File.Dictionary(game["Folders"]["details"])

		# Edit the game details file with the details above (or the one that already existed in the dictionary)
		self.File.Edit(game["Folders"]["details"], self.Text.From_Dictionary(game["Details"]), "w")

		# Define the default game language as the user language
		game["Language"] = self.full_user_language

		# Change user language to original game language if the key exists inside the game details
		if self.JSON.Language.language_texts["original_language"] in game["Details"]:
			game["Language"] = game["Details"][self.JSON.Language.language_texts["original_language"]]

		if game["Language"] in list(self.languages["full"].values()):
			# Iterate through full languages list to find small language from the full language
			for small_language in self.languages["full"]:
				full_language = self.languages["full"][small_language]

				if full_language == game["Language"]:
					game["Language"] = small_language

		game["Platform"] = game["Details"][self.JSON.Language.language_texts["platform, title()"]]

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
			"Finished playing": False
		}

		if "States" in game:
			game["States"].update(states)

		elif "States" not in game:
			game["States"] = states

		if self.Today_Is_Christmas == True:
			game["States"]["Christmas"] = True

		# Define Re-playing state for Re-playing status
		if (
			self.JSON.Language.language_texts["status, title()"] in game["Details"] and
			game["Details"][self.JSON.Language.language_texts["status, title()"]] == self.language_texts["re_playing, title()"]
		):
			game["States"]["Re-playing"] = True

		game["States"]["First game session in year"] = False

		if self.dictionaries["Sessions"]["Numbers"]["Total"] == 0:
			game["States"]["First game session in year"] = True

		game["States"]["First game type session in year"] = False

		if self.dictionaries["Game type"][dictionary["Type"]["Type"]["en"]]["Numbers"]["Total"] == 0:
			game["States"]["First game type session in year"] = True

		dictionary = self.Define_Game_Titles(dictionary)

		# Define game files
		game["Files"] = {
			"Shortcut": dictionary["Type"]["Folders"]["Shortcuts"]["root"] + self.Sanitize(game["Title"], restricted_characters = True),
			"Shortcut path": ""
		}

		found_shortcut = False

		for extension in [".lnk", ".url"]:
			file = game["Files"]["Shortcut"] + extension

			if self.File.Exist(file) == True:
				game["Files"]["Shortcut"] += extension

				found_shortcut = True

		if found_shortcut == False:
			game["Files"]["Shortcut"] = ""

		if found_shortcut == True:
			import win32com.client
			shell = win32com.client.Dispatch("WScript.Shell")

			game["Files"]["Shortcut path"] = shell.CreateShortCut(game["Files"]["Shortcut"]).Targetpath.replace("\\", "/")

		# Define bat File for game
		file = self.Folder.folders["apps"]["shortcuts"]["root"] + self.Sanitize(game["Title"], restricted_characters = True) + ".bat"

		if self.File.Exist(file) == True:
			game["Files"]["Bat"] = file

		# Create the local game folder
		root_folder = self.Folder.folders["Games"]["Folders"]["root"]

		if self.Folder.language_texts["root_folder"] in game["Details"]:
			root_folder += game["Details"][self.Folder.language_texts["root_folder"]] + "/"

		if dictionary["Type"]["Type"]["en"] in ["Flash", "Nintendo 64", "Super Nintendo"]:
			root_folder += dictionary["Type"]["Type"]["en"] + "/"

		game_folder = self.Sanitize(game["Title"], restricted_characters = True)

		if self.Folder.language_texts["folder, title()"] in game["Details"]:
			game_folder = game["Details"][self.Folder.language_texts["folder, title()"]]

		game["Folders"]["local"] = root_folder + game_folder + "/"

		if (
			self.Folder.language_texts["create_folder"] not in game["Details"] or 
			self.Folder.language_texts["create_folder"] in game["Details"] and
			self.Input.Define_Yes_Or_No(game["Details"][self.Folder.language_texts["create_folder"]]) == False
		):
			if (
				game["Platform"]["en"] not in ["Console", "Mobile", "Super Nintendo", "Nintendo 64"] and
				dictionary["Type"]["Type"]["en"] not in ["Flash", "Nintendo 64", "Super Nintendo"] and
				self.JSON.Language.language_texts["steam, title()"] not in game["Details"] and
				"steam://" not in game["Files"]["Shortcut path"] and
				"https://" not in game["Files"]["Shortcut path"]
			):
				self.Folder.Create(game["Folders"]["local"])

			else:
				game["Folders"]["local"] = ""

		return dictionary

	def Select_Game_Type_And_Game(self, options = None, game_title = None):
		dictionary = {
			"Type": {
				"Select": True,
				"Status": [
					self.texts["plan_to_play, title()"]["en"],
					self.texts["playing, title()"]["en"],
					self.texts["re_playing, title()"]["en"],
					self.JSON.Language.texts["on_hold, title()"]["en"]
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
			dictionary["Game"] = self.Select_Game(dictionary, game_title)["Game"]

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

						if text_key in self.JSON.Language.texts:
							text = self.JSON.Language.texts[text_key][language]

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

	def Define_Game_Titles(self, dictionary):
		game = dictionary["Game"]

		if self.File.Exist(game["Folders"]["details"]) == True:
			game["Details"] = self.File.Dictionary(game["Folders"]["details"])

			# Define titles key
			game["Titles"] = {
				"Original": game["Details"][self.JSON.Language.language_texts["title, title()"]],
				"Sanitized": game["Details"][self.JSON.Language.language_texts["title, title()"]],
			}

			game["Titles"]["Language"] = game["Titles"]["Original"]

			# If the "romanized_title" key exists inside the game details, define the romanized name and ja name
			if self.JSON.Language.language_texts["romanized_title"] in game["Details"]:
				if self.JSON.Language.language_texts["romanized_title"] in game["Details"]:
					game["Titles"]["Romanized"] = game["Details"][self.JSON.Language.language_texts["romanized_title"]]
					game["Titles"]["Language"] = game["Titles"]["Romanized"]

				if "Romanized" in game["Titles"]:
					game["Titles"]["Sanitized"] = game["Titles"]["Romanized"]

				game["Titles"]["ja"] = game["Details"][self.JSON.Language.language_texts["title, title()"]]

			if (
				" (" in game["Titles"]["Original"] and
				" (" not in game["Titles"]["Language"]
			):
				game["Titles"]["Language"] = game["Titles"]["Language"] + " (" + game["Titles"]["Original"].split(" (")[-1]

				if self.user_language in game["Titles"]:
					game["Titles"][self.user_language] = game["Titles"][self.user_language] + " (" + game["Titles"]["Original"].split(" (")[-1]

			# Define game titles per language
			for language in self.languages["small"]:
				key = self.JSON.Language.texts["title_in_language"][language][self.user_language]

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

			# Sanitize game title
			game["Titles"]["Sanitized"] = self.Sanitize_Title(game["Titles"]["Sanitized"])

		return dictionary

	def Sanitize_Title(self, title):
		if (
			len(title) > 1 and
			title[0] + title[1] == ": "
		):
			title = title[2:]

		if ". " in title:
			title = title.replace(". ", " ")

		elif "." in title:
			title = title.replace(".", "")

		title = self.Sanitize(title, restricted_characters = True)

		return title

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
			status = self.JSON.Language.language_texts["completed, title()"]

		# Update the status key in the game details
		dictionary["Game"]["Details"][self.JSON.Language.language_texts["status, title()"]] = status

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

			self.language_status = dictionary["Game"]["Details"][self.JSON.Language.language_texts["status, title()"]]

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
			for data_title in titles:
				if (
					"Type" in dictionary and
					"JSON" not in dictionary["Type"]
				):
					folder = game_type["Folders"]["Information"]["root"] + self.Sanitize_Title(data_title) + "/"
					details_file = folder + self.JSON.Language.language_texts["details, title()"] + ".txt"
					details = self.File.Dictionary(details_file)

					self.language_status = details[self.JSON.Language.language_texts["status, title()"]]

					# Get the English status from the language status of the game details
					status = self.Get_Language_Status(self.language_status)

				# If the game status is equal to the playing status
				# And the game is not in the correct status list, add it to the list
				if (
					status == playing_status and
					data_title not in dictionary["JSON"]["Status"][playing_status]
				):
					dictionary["JSON"]["Status"][playing_status].append(data_title)

				# If the game status is not equal to the playing status
				# And the game is in the wrong playing status list, remove it from the list
				if (
					status != playing_status and
					data_title in dictionary["JSON"]["Status"][playing_status]
				):
					dictionary["JSON"]["Status"][playing_status].remove(data_title)

			# Sort the games list
			dictionary["JSON"]["Status"][playing_status] = sorted(dictionary["JSON"]["Status"][playing_status], key = str.lower)

		# Update the game type "Information.json" file
		self.JSON.Edit(game_type["Folders"]["Information"]["Information"], dictionary["JSON"])

		return dictionary

	def Calculate_Gaming_Time(self, dictionary):
		from copy import deepcopy

		game = dictionary["Game"]

		if "Entry" in dictionary:
			entry = dictionary["Entry"]

		# Define the first and last times
		for key in ["First", "Last"]:
			if game["Time"][key + " time"] == "":
				sub_key = "Before"

				if key == "Last":
					sub_key = "After"

				game["Time"][key + " time"] = entry["Session duration"][sub_key]["UTC"]["DateTime"]["Formats"]["YYYY-MM-DDTHH:MM:SSZ"]

			# Create the date dictionary of the played time
			game["Time"][key + " time"] = self.Date.From_String(game["Time"][key + " time"])

		# Define the "Added time" as the first played time
		game["Time"]["Added time"] = game["Time"]["First time"].copy()

		# Iterate through the time difference keys
		for key in entry["Session duration"]["Difference"]:
			diff = entry["Session duration"]["Difference"][key]

			# Add the difference time to the game time
			game["Time"][key] += diff

		# Iterate through the difference time units
		for key in entry["Session duration"]["Difference"]:
			dict_ = {
				key.lower(): game["Time"][key]
			}

			# Add the game time difference time unit to the "Added time" date object
			game["Time"]["Added time"]["Object"] += self.Date.Relativedelta(**dict_)

		# Transform the "Added time" into a date dictionary with the added time above
		game["Time"]["Added time"] = self.Date.Now(game["Time"]["Added time"]["Object"])

		# Make the difference between the first time and the added time
		difference = self.Date.Difference(game["Time"]["First time"]["Object"], game["Time"]["Added time"]["Object"])

		# Define the game time difference units as the difference above
		for key in difference["Difference"]:
			diff = difference["Difference"][key]

			game["Time"][key] = diff

		# Transform the times back into date strings
		for key in ["First", "Last", "Added"]:
			game["Time"][key + " time"] = self.Date.To_String(game["Time"][key + " time"], utc = True)

		# Update the "Time.json" file
		self.JSON.Edit(game["Folders"]["played"]["time"], game["Time"])

		gaming_time = self.Make_Gaming_Time_Text(game)

		# Write the gaming time into the gaming time file
		if gaming_time != "":
			self.File.Edit(game["Folders"]["played"]["gaming_time"], gaming_time, "w")

		return game

	def Make_Gaming_Time_Text(self, game):
		from copy import deepcopy

		# Copy and remove unused keys
		times = deepcopy(game["Time"])

		for key in ["First", "Last", "Added"]:
			key += " time"

			if key in times:
				times.pop(key)

		# Define the singular and plural time text lists
		singular = deepcopy(self.Date.language_texts["date_attributes, type: list"])
		plural = deepcopy(self.Date.language_texts["plural_date_attributes, type: list"])

		# Iterate through the times dictionary to remove zero time keys
		# And also remove time texts of zero times from the singular and plural lists
		i = 0
		for key in times.copy():
			time = times[key]

			if time == 0:
				times.pop(key)

				text = self.Date.language_texts[key.lower()[:-1] + ", title()"].lower()

				if text in singular:
					singular.remove(text)

				text = self.Date.language_texts[key.lower() + ", title()"].lower()

				if text in plural:
					plural.remove(text)

			i += 1

		# Define the empty gaming time string
		gaming_time = ""

		# Iterate through the times dictionary
		i = 0
		for key in times.copy():
			time = times[key]

			# If the time key is not the first one and not the last one
			if key != list(times.keys())[0].capitalize():
				# If the number of times is more than one and not two, add a comma
				if (
					len(times) > 1 and
					len(times) != 2 and
					gaming_time[-1] + gaming_time[-2] not in [" ,", ", "]
				):
					gaming_time += ", "

				# If the number of times is two, add the " and " text
				if len(times) == 2:
					gaming_time += " " + self.JSON.Language.language_texts["and"] + " "

			# If the time key is the last one and the number of times is more or equal to two, add the ", and " text
			if (
				key == list(times.keys())[-1].capitalize() and
				len(times) > 2
			):
				if gaming_time[-1] + gaming_time[-2] != " ,":
					gaming_time += ", "

				gaming_time += self.JSON.Language.language_texts["and"] + " "

			# Add the time to the full gaming time text
			gaming_time += str(time)

			# Define the default time text list as the singular one 
			list_ = singular

			# If the time is more than one, define the time text list as the plural one
			if time > 1:
				list_ = plural

			# Add a space and the time text to the full gaming time text
			gaming_time += " " + list_[i]

			i += 1

		return gaming_time

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
		from copy import deepcopy

		# Get the language game type
		game_type = self.game_types[entry["Type"]]["Type"][language]

		# Define the item text, with the entry title with quotes
		item = '"' + self.Define_Title(entry["Titles"], language) + '"'

		# Add the game type with a comma, to the item text
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
		print()
		print(self.large_bar)

		print()
		print(self.language_texts["game_title"] + ":")

		key = "Original"

		if "Romanized" in game["Titles"]:
			key = "Romanized"

		print("\t" + game["Titles"][key])

		for language in self.languages["small"]:
			if language in game["Titles"]:
				translated_language = self.languages["full_translated"][language][self.user_language]

				print("\t" + translated_language + ":")
				print("\t" + game["Titles"][language])

		print()

		print(self.JSON.Language.language_texts["category, title()"] + ":")

		types = []

		for language in self.languages["small"]:
			text = "\t" + dictionary["Type"]["Type"][language]

			if text not in types:
				types.append(text)

		for item in types:
			print(item)

		print()

		platforms = []

		for language in self.languages["small"]:
			text = "\t" + dictionary["Game"]["Platform"][language]

			if text not in platforms:
				platforms.append(text)

		print(self.JSON.Language.language_texts["platform, title()"] + ":")

		for item in platforms:
			print(item)

		if game["Folders"]["local"] == "":
			print()
			print(self.Folder.language_texts["folder, title()"] + ":")
			print("\t" + game["Folders"]["root"])

		if game["Folders"]["local"] != "":
			print()
			print(self.Folder.language_texts["folders, title()"] + ":")
			print("\t" + self.JSON.Language.language_texts["informations, title()"] + ":")
			print("\t" + game["Folders"]["root"])
			print()
			print("\t" + self.JSON.Language.language_texts["local, title()"] + ":")
			print("\t" + game["Folders"]["local"])

		if game["Files"]["Shortcut"] != "":
			print()
			print(self.File.language_texts["shortcut, title()"] + ":")
			print("\t" + game["Files"]["Shortcut"])

		if game["Files"]["Shortcut path"] != "":
			print()
			print(self.JSON.Language.language_texts["path, title()"] + ":")
			print("\t" + game["Files"]["Shortcut path"])

		if "Entry" in dictionary:
			print()

			print(self.language_texts["when_you_finished_playing"] + ":")
			print("\t" + dictionary["Entry"]["Dates"]["Timezone"])
			print()

			print(self.JSON.Language.language_texts["session_duration"] + ":")
			print("\t" + dictionary["Entry"]["Session duration"]["Text"][self.user_language])

			if "dates" in game:
				print()
				print(self.Date.language_texts["dates, title()"] + ":")

				for key, value in game["dates"].items():
					print("\t" + key + ":")
					print("\t" + value)

			# If there are states, show them
			if (
				"States" in dictionary and
				dictionary["States"]["Texts"] != {}
			):
				print()
				print(self.JSON.Language.language_texts["states, title()"] + ":")

				for key in dictionary["States"]["Texts"]:
					print("\t" + dictionary["States"]["Texts"][key][self.user_language])

			# If the user finished playing, ask for input before ending execution
			print()
			print(self.large_bar)

			self.Input.Type(self.JSON.Language.language_texts["press_enter_when_you_finish_reading_the_info_summary"])