# GamePlayer.py

# Import the "importlib" module
import importlib

from copy import deepcopy
import collections

class GamePlayer(object):
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.folders = self.Define_Folders(object = self).folders

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Import some usage classes
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

		# Get the "Today_Is_Christmas" True or False variable
		self.Today_Is_Christmas = self.Christmas.Today_Is_Christmas()

	def Define_Folders_And_Files(self):
		# If there is no current year variable inside the self object
		if hasattr(self, "current_year") == False:
			# Get the current year variable from the "Years" module
			self.current_year = self.Years.years["Current year"]

		# Iterate through the list of small languages
		for language in self.languages["Small"]:
			# Define a shortcut for the folder
			folder = self.current_year["Folders"][language]

			# Get the "Gaming sessions" text in the current language to be the folder name
			folder_name = self.Language.texts["gaming_sessions"][language]

			# Define the gaming sessions folder
			folder["Gaming sessions"] = {
				"root": folder["root"] + folder_name + "/"
			}

			# Create the folder
			self.Folder.Create(folder["Gaming sessions"]["root"])

			# Update the folder shortcut
			folder = self.current_year["Folders"][language]["Firsts of the Year"]

			# Update the folder name to "Gaming session"
			folder_name = self.Language.texts["gaming_session"][language]

			# Define the sub-folder dictionary
			folder["Gaming sessions"] = {
				"root": folder["root"] + folder_name + "/"
			}

			self.Folder.Create(folder["Gaming sessions"]["root"])

		# ---------- #

		# Replace the "self.folders" folder dictionary with the "Games" network folder dictionary
		self.folders = self.folders["Notepad"]["Data Networks"]["Games"]

		# Define the current year folder for easier typing
		self.folders["Play History"]["Current year"] = self.folders["Play History"][self.current_year["Number"]]

		# Define the "History" dictionary
		self.history = {
			"Key": "Sessions",
			"Numbers": {
				"Gaming sessions played": ""
			},
			"Folder": self.Folder.folders["Notepad"]["Data Networks"]["Games"]["Play History"]["root"]
		}

	def Parse_Arguments(self):
		# If the "Verbose" switch is True
		# And the "Active argument" is inside the root arguments dictionary
		if (
			self.switches["Verbose"] == True and
			"Active argument" in self.arguments
		):
			# Show the "Arguments" text in the user language
			print()
			print(self.Language.language_texts["arguments, title()"] + ":")
			print()

			# Show the dictionary arguments
			self.JSON.Show(self.arguments)

	def Define_Types(self):
		# Define the game types dictionary
		self.game_types = self.JSON.To_Python(self.folders["Data"]["Types"])

		# Update the game types dictionary to add some keys
		self.game_types.update({
			"Genders": self.Language.texts["genders, type: dictionary"],
			"Gender items": self.Language.texts["gender_items"],
			"Game list": {
				"Number": 0,
				"Numbers": {}
			},
			"Dictionary": {}
		})

		# Reset the game number to zero
		if self.game_types["Game list"]["Number"] != 0:
			self.game_types["Game list"]["Number"] = 0

		# If the root "Information.json" file is not empty
		if self.File.Contents(self.folders["Game information"]["Information"])["lines"] != []:
			# Get the information dictionary from it
			info_dictionary = self.JSON.To_Python(self.folders["Game information"]["Information"])

		# If the root "Information.json" file is empty
		if self.File.Contents(self.folders["Game information"]["Information"])["lines"] == []:
			# Define a default empty information dictionary
			info_dictionary = {
				"Types": self.game_types["Types"],
				"Number": 0,
				"Numbers": {}
			}

		# Iterate through the list of English game types
		i = 0
		for game_type in self.game_types["Types"]["en"]:
			# Define the game type key
			key = game_type.lower().replace(" ", "_")

			# Define the user language version of the game type
			language_type = self.game_types["Types"][self.language["Small"]][i]

			# Create the game type dictionary
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

			# Define the game types by language
			for language in self.languages["Small"]:
				self.game_types[game_type]["Type"][language] = self.game_types["Types"][language][i]

			# Create type folders
			for root_folder in ["Game information", "Play History", "Shortcuts"]:
				# Create the "Game information" folder
				if root_folder == "Game information":
					self.folders[root_folder][key] = {
						"root": self.folders[root_folder]["root"] + language_type + "/"
					}

					self.Folder.Create(self.folders[root_folder][key]["root"])

				# "Play History By Game Type" folder
				if root_folder == "Play History":
					# Define the "By game type" folder
					self.folders[root_folder]["Current year"]["By game type"][key] = {
						"root": self.folders[root_folder]["Current year"]["By game type"]["root"] + game_type + "/"
					}

					self.Folder.Create(self.folders[root_folder]["Current year"]["By game type"][key]["root"])

					# Create the "Sessions.json" file
					self.folders[root_folder]["Current year"]["By game type"][key]["Sessions"] = self.folders[root_folder]["Current year"]["By game type"][key]["root"] + "Sessions.json"
					self.File.Create(self.folders[root_folder]["Current year"]["By game type"][key]["Sessions"])

					# Create the "Entry list.txt" file
					self.folders[root_folder]["Current year"]["By game type"][key]["Entry list"] = self.folders[root_folder]["Current year"]["By game type"][key]["root"] + "Entry list.txt"
					self.File.Create(self.folders[root_folder]["Current year"]["By game type"][key]["Entry list"])

					# Create the "Files" folder 
					self.folders[root_folder]["Current year"]["By game type"][key]["Files"] = {
						"root": self.folders[root_folder]["Current year"]["By game type"][key]["root"] + "Files/"
					}

					self.Folder.Create(self.folders[root_folder]["Current year"]["By game type"][key]["Files"]["root"])

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
				"Game information": self.folders["Game information"][key],
				"By game type": self.folders["Play History"]["Current year"]["By game type"][key],
				"Shortcuts": self.folders["Shortcuts"][key]
			}

			# Define the "Information.json" file
			self.game_types[game_type]["Folders"]["Game information"]["Information"] = self.game_types[game_type]["Folders"]["Game information"]["root"] + "Information.json"
			self.File.Create(self.game_types[game_type]["Folders"]["Game information"]["Information"])

			# Read the "Information.json" file
			if self.File.Contents(self.game_types[game_type]["Folders"]["Game information"]["Information"])["lines"] != []:
				self.game_types[game_type]["JSON"] = self.JSON.To_Python(self.game_types[game_type]["Folders"]["Game information"]["Information"])

			# If the "Information.json" file is empty, add a default JSON dictionary inside it
			if self.File.Contents(self.game_types[game_type]["Folders"]["Game information"]["Information"])["lines"] == []:
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
			self.JSON.Edit(self.game_types[game_type]["Folders"]["Game information"]["Information"], self.game_types[game_type]["JSON"])

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
			self.game_types[game_type]["Texts"]["Show"] = self.game_types[game_type]["Type"][self.language["Small"]] + " (" + str(len(self.game_types[game_type]["Game list"])) + ")"

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
		self.JSON.Edit(self.folders["Game information"]["Information"], info_dictionary)

	def Define_Registry_Format(self):
		# Define the default entries dictionary template
		self.template = {
			"Numbers": {
				"Total": 0
			},
			"Entries": [],
			"Dictionary": {}
		}

		# Define the root dictionary of dictionaries
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

		# If the "History.json" file is not empty
		# And the list of the "Years" key is not empty
		if (
			self.File.Contents(self.folders["Play History"]["History"])["lines"] != [] and
			self.JSON.To_Python(self.folders["Play History"]["History"])["Years"] != []
		):
			# Get the "History" dictionary from the JSON file
			self.dictionaries["History"] = self.JSON.To_Python(self.folders["Play History"]["History"])

		# If the current year is not inside the "History" years list, add it to the list
		if self.current_year["Number"] not in self.dictionaries["History"]["Years"]:
			self.dictionaries["History"]["Years"].append(self.current_year["Number"])

		# Define the default sessions number as zero
		sessions = 0

		# Iterate through the years inside the years list, from 2021 to the current year
		for year in self.Date.Create_Years_List(start = 2021, function = str):
			# Get the year folder and the entries file
			year_folder = self.folders["Play History"]["root"] + year + "/"
			entries_file = year_folder + "Sessions.json"

			# If the file exists and it is not empty
			if (
				self.File.Exists(entries_file) == True and
				self.File.Contents(entries_file)["lines"] != []
			):
				# Add the number of lines of the file to the local number of entries
				sessions += self.JSON.To_Python(entries_file)["Numbers"]["Total"]

			# Add the year to the list of years if it is not inside it
			if year not in self.dictionaries["History"]["Years"]:
				self.dictionaries["History"]["Years"].append(year)

		# Sort the list of years
		self.dictionaries["History"]["Years"] = sorted(self.dictionaries["History"]["Years"], key = str.lower)

		# Update the number of years with the length of the years list
		self.dictionaries["History"]["Numbers"]["Years"] = len(self.dictionaries["History"]["Years"])

		# Define the number of entries of all years as the local number of entries
		self.dictionaries["History"]["Numbers"]["Sessions"] = sessions

		# Update the "History.json" file with the updated "History" dictionary
		self.JSON.Edit(self.folders["Play History"]["History"], self.dictionaries["History"])

		# Create the "By game type" key inside the "Numbers" dictionary of the "Sessions" dictionary
		self.dictionaries["Sessions"]["Numbers"]["By game type"] = {}

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
				self.File.Contents(self.folders["Play History"]["Current year"]["By game type"][key]["Sessions"])["lines"] != [] and
				self.JSON.To_Python(self.folders["Play History"]["Current year"]["By game type"][key]["Sessions"])["Entries"] != []
			):
				self.dictionaries["Game type"][game_type] = self.JSON.To_Python(self.folders["Play History"]["Current year"]["By game type"][key]["Sessions"])

			# Add the game type number to the root numbers by game type if it does not exist in there
			if game_type not in self.dictionaries["Sessions"]["Numbers"]["By game type"]:
				self.dictionaries["Sessions"]["Numbers"]["By game type"][game_type] = 0

			# Else, define the root total number by game type as the number inside the Sessions dictionary by game type
			if game_type in self.dictionaries["Sessions"]["Numbers"]["By game type"]:
				self.dictionaries["Sessions"]["Numbers"]["By game type"][game_type] = self.dictionaries["Game type"][game_type]["Numbers"]["Total"]

			# Update the by game type "Sessions.json" file with the updated by game type "Sessions" dictionary
			self.JSON.Edit(self.folders["Play History"]["Current year"]["By game type"][key]["Sessions"], self.dictionaries["Game type"][game_type])

		# Sort the dictionary of game type numbers based on its keys
		self.dictionaries["Sessions"]["Numbers"]["By game type"] = dict(collections.OrderedDict(sorted(self.dictionaries["Sessions"]["Numbers"]["By game type"].items())))

		# Update the "Sessions.json" file with the updated "Sessions" dictionary
		self.JSON.Edit(self.folders["Play History"]["Current year"]["Sessions"], self.dictionaries["Sessions"])

	def Create_Statistics(self, years_list):
		# Define a local dictionary of statistics
		statistics = {
			"Module": "GamePlayer",
			"Statistic key": "Gaming sessions played",
			"Text": {},
			"List": [],
			"Years": {}
		}

		# Create a root dictionary of games
		self.games = {
			"List": [],
			"Dictionary": {}
		}

		# ---------- #

		# Fill the "Years" dictionary

		# Update the list of years to be from the year "2021" to the current year
		years_list = self.Date.Create_Years_List(start = 2021)

		# Iterate through the list of years from 2020 to the current year
		for year_number in years_list:
			# Create the year dictionary
			year = {
				"Key": year_number,
				"Total": 0,
				"Numbers": {},
				"Months": {}
			}

			# Get the year folder and the entries file
			year_folder = self.folders["Play History"]["root"] + year_number + "/"
			entries_file = year_folder + "Sessions.json"

			# Read the "Entries.json" file, getting the "Entries" dictionary and adding it into the year dictionary
			year["Entries"] = self.JSON.To_Python(entries_file)

			# Iterate through the dictionary of entries, updating the "Numbers" dictionary of the year dictionary
			year = self.Iterate_Through_Entries(year)

			# ---------- #

			# Fill the "Months" dictionary
			for month in range(1, 13):
				# Add leading zeroes to the month number
				month_number = str(self.Text.Add_Leading_Zeroes(month))

				# Create the month dictionary
				month = {
					"Key": month_number,
					"Total": 0,
					"Numbers": {}
				}

				# Iterate through the entries dictionary
				for entry in year["Entries"]["Dictionary"].values():
					# Get the local month number of the entry
					local_month_number = entry["Entry"].split("/")[1]

					# If the local month number is equal to the root month number
					if local_month_number == month_number:
						# Define the game dictionary (game or sub-game), and add the game played numbers
						month = self.Define_Game_Dictionary(month, entry)

						# Add one to the month total entries number
						month["Total"] += 1

				# Add the month dictionary to the "Months" dictionary of the year dictionary
				year["Months"][month_number] = month

			# ---------- #

			# Remove the "Entries" key
			year.pop("Entries")

			# Add the year dictionary to the "Years" dictionary
			statistics["Years"][year_number] = year

		# Iterate through the dictionary of years
		for year in statistics["Years"].values():
			# Iterate through the month keys and month dictionaries inside the year "Months" dictionary
			for month_key, month in deepcopy(year["Months"]).items():
				# If the number of total entries of the month is zero
				if month["Total"] == 0:
					# Remove the month from the dictionary of months
					year["Months"].pop(month_key)

		# Sort the list of games in alphabetical order
		self.games["List"] = sorted(self.games["List"], key = str.lower)

		# Define the list of statistics as the list of games
		statistics["List"] = self.games["List"]

		# Return the statistics dictionary
		return statistics

	def Define_Game_Dictionary(self, dictionary, entry):
		# Define the key to get the game title
		key = "Original"

		if "Romanized" in entry["Titles"]:
			key = "Romanized"

		# Get the game title
		game_title = entry["Titles"][key]

		# Add the game title to the root games dictionary
		if game_title not in self.games["List"]:
			self.games["List"].append(game_title)

		# If there is a sub-game inside the entry dictionary
		if "Sub-game" in entry:
			# If the game title is not inside the "Numbers" dictionary
			if game_title not in dictionary["Numbers"]:
				# Define the root game dictionary
				dictionary["Numbers"][game_title] = {
					"Total": 0,
					"Dictionary": {}
				}

			# Else, if the game title key inside the "Numbers" dictionary is a number
			elif isinstance(dictionary["Numbers"][game_title], int):
				# Get the original number of times played
				played_number = dictionary["Numbers"][game_title]

				# Define the root game dictionary
				dictionary["Numbers"][game_title] = {
					"Total": played_number,
					"Dictionary": {
						game_title: played_number
					}
				}

			# Update the game variable
			game = dictionary["Numbers"][game_title]

			# Define the key to get the sub-game title
			key = "Original"

			if "Romanized" in entry["Sub-game"]:
				key = "Romanized"

			# Get the sub-game title
			sub_game_title = entry["Sub-game"][key]

			# Make a backup of the full game title (game and sub-game titles joined together)
			self.games["Dictionary"][game_title] = game_title

			# If the ": " string is not the first two characters of the sub-game title
			if sub_game_title[0] + sub_game_title[1] != ": ":
				# Add a space to the backup of the full game title
				self.games["Dictionary"][game_title] += " "

			# Add the sub-game title to the backup of the full game title
			self.games["Dictionary"][game_title] += sub_game_title

			# Add the full game title to the root games dictionary
			if self.games["Dictionary"][game_title] not in self.games["List"]:
				self.games["List"].append(self.games["Dictionary"][game_title])

			# If the ": " string is inside the sub-game title, remove it
			if ": " in sub_game_title:
				sub_game_title = sub_game_title.replace(": ", "")

			# Add the sub-game key to the game dictionary if it is not already present
			if sub_game_title not in game["Dictionary"]:
				game["Dictionary"][sub_game_title] = 0

			# Add one to the number of times the sub-game was played
			game["Dictionary"][sub_game_title] += 1

		# Define the game inside the "Numbers" dictionary as zero if it is not there already
		if game_title not in dictionary["Numbers"]:
			dictionary["Numbers"][game_title] = 0

		# Define a shortcut for the game variable
		game = dictionary["Numbers"][game_title]

		# If the game variable is an integer
		if isinstance(game, int):
			# Add one to the number of times the game was played
			dictionary["Numbers"][game_title] += 1

		else:
			# Add one to the number of times the game was played in the "Total" key
			game["Total"] += 1

		# ---------- #

		# If the game key is a dictionary
		if isinstance(game, dict):
			# List the keys inside the game dictionary
			keys = list(game.keys())

			# If the number of keys is equal to two
			# And the value of the keys is equal
			if (
				len(keys) == 2 and
				game[keys[0]] == list(game["Dictionary"].values())[0]
			):
				# Get the full game title from the root games dictionary
				title = self.games["Dictionary"][game_title]

				# Define the title inside the "Numbers" dictionary
				dictionary["Numbers"][title] = game["Total"]

				# Remove the old game title key
				dictionary["Numbers"].pop(game_title)

		return dictionary

	def Iterate_Through_Entries(self, dictionary, month = True):
		# Iterate through the entries dictionary
		for entry in dictionary["Entries"]["Dictionary"].values():
			# Define the game dictionary (game or sub-game), and add the game played numbers
			dictionary = self.Define_Game_Dictionary(dictionary, entry)

			# Add one to the total number of games played in the year or month
			dictionary["Total"] += 1

		return dictionary

	def Add_To_Index(self, dictionary, original_key, new_key, new_value):
		# List the keys of the dictionary
		keys = list(dictionary.keys())

		# Checks if the original key exists inside the dictionary
		if original_key not in keys:
			# Returns the original dictionary if not
			return dictionary

		# Get the index of the original key
		index = keys.index(original_key)

		# Define a new local dictionary
		new_dictionary = {}

		# Iterate through the indexes and keys of the list of keys
		for i, key in enumerate(keys):
			# If the "i" variable is the index we are looking for
			if i == index:
				# Replace the original key with the new key 
				new_dictionary[new_key] = new_value

			else:
				# Add the original key that existed before
				new_dictionary[key] = dictionary[key]

		# Return the new dictionary
		return new_dictionary

	def Update_Statistics(self, game, game_type):
		# Import the "Diary_Slim" module
		from Diary_Slim.Diary_Slim import Diary_Slim as Diary_Slim

		# Define the "Diary_Slim" class inside this class
		self.Diary_Slim = Diary_Slim()

		# Get the "diary_slim" dictionary from the class above
		self.diary_slim = self.Diary_Slim.diary_slim

		# ---------- #

		# Define a local dictionary of statistics
		statistics = {
			"Module": "GamePlayer",
			"Statistic key": "Gaming sessions played",
			"External statistic": True,
			"Year": {},
			"Month": {},
			"Text": "",
			"Dictionary": {
				"Numbers": {
					"Year": {
						"Old": 0,
						"New": 1
					},
					"Month": {
						"Old": 0,
						"New": 1
					}
				}
			}
		}

		# Define a shortcut for the statistic key
		statistic_key = statistics["Statistic key"]

		# ---------- #

		# Define the key to get the game title
		title_key = "Original"

		if "Romanized" in game["Titles"]:
			title_key = "Romanized"

		# Define a shortcut for the game title
		game_title = game["Titles"][title_key]

		# Iterate through the list of keys
		for key in ["Year", "Month"]:
			# Define the default dictionary as the year dictionary
			dictionary = self.diary_slim["Current year"]

			# If the key is "Month"
			if key == "Month":
				# Define the default dictionary as the month dictionary
				dictionary = self.diary_slim["Current year"]["Month"]

			# Get the year statistics for the "Stories" module
			statistics[key] = dictionary["Statistics"][statistic_key]

			# Add one to the total number of statistics
			statistics[key]["Total"] += 1

			# Make a copy of the statistics dictionary
			statistics_copy = deepcopy(statistics[key]["Dictionary"])

			# If the "Sub-game" key is inside the game titles dictionary
			if "Sub-game" in game["Titles"]:
				# Define the key to get the game and sub-game titles
				title_key = "Original"
				item_key = "Original"

				# Define the key as "Romanized" if that key exists inside the "Titles" dictionary, for the title and item key
				if "Romanized" in game["Titles"]:
					title_key = "Romanized"

				if "Romanized" in game["Titles"]["Sub-game"]:
					item_key = "Romanized"

			# If the "Items" key does not exist in the local game dictionary
			# Or the "Items" key does exist in the local game dictionary
			# And the "Sub-game" key is inside the game titles dictionary
			# And the sub-game title is the same as the game title
			if (
				"Items" not in game or
				"Items" in game and
				"Sub-game" in game["Titles"] and
				game["Titles"]["Sub-game"][item_key] == game["Titles"][title_key]
			):
				# If the game title is not inside the dictionary of games
				if game_title not in statistics[key]["Dictionary"]:
					# Define the game statistic key as zero
					statistics[key]["Dictionary"][game_title] = 0

			# Define the "sub-game found in dictionary" switch as False
			sub_game_found_in_dictionary = False

			# If the "Items" key exists in the local game dictionary
			if "Items" in game:
				# Make a list of sub-games to iterate through
				sub_games = game["Items"]["List"]

				# Iterate through the list of items
				for item_title in sub_games:
					# If the sub-game title key exists inside the items dictionary
					if item_title in game["Items"]["Dictionary"]:
						# Get the item dictionary from it
						item = game["Items"]["Dictionary"][item_title]

						# If the first two characters of the item title is a colon and a space
						if item_title[0] + item_title[1] == ": ":
							# Remove the colon and space
							item_title = item_title[2:]

						# Define the key to get the number of times the sub-game was played
						sub_game_title = item["With game title"]["Original"]

						# If the sub-game title with the root game title title is inside the statistics dictionary
						# And the current sub-game title is the same as the title of the played sub-game
						if (
							sub_game_title in statistics[key]["Dictionary"] and
							item_title == game["Titles"]["Sub-game"]["Original (no game title)"]
						):
							# Define the "sub-game found in dictionary" switch as False
							sub_game_found_in_dictionary = True

			# Define the default game title key
			game_title_key = game_title

			# If the "Items" key exists in the local game dictionary
			# And the sub-game was found inside the statistics dictionary
			if (
				"Items" in game and
				sub_game_found_in_dictionary == True
			):
				# Define the game title key as the sub-game title
				game_title_key = game["Titles"]["Sub-game"][item_key]

			# Define the default played title as the game title
			played_title = game["Titles"]["Original"]

			# If the "Sub-game" key is inside the game titles dictionary
			if "Sub-game" in game["Titles"]:
				# Define the played title as the sub-game title
				played_title = game["Titles"]["Sub-game"]["Original (no game title)"]

			# Define the "added sub-game dictionary" switch as False
			added_sub_game_dictionary = False

			# If the "Items" key exist in the local game dictionary
			# And the "Sub-game" key is inside the game titles dictionary
			# And the sub-game title is not the same as the game title
			# And the sub-game was not found inside the statistics dictionary
			# Or the "Items" key exist in the local game dictionary
			# And the "Sub-game" key is inside the game titles dictionary
			# And the sub-game title is the same as the game title
			if (
				"Items" in game and
				"Sub-game" in game["Titles"] and
				game["Titles"]["Sub-game"]["Original"] != game["Titles"]["Original"] and
				sub_game_found_in_dictionary == False or
				"Items" in game and
				"Sub-game" in game["Titles"] and
				game["Titles"]["Sub-game"]["Original"] == game["Titles"]["Original"]
			):
				# If the game title is inside the statistics dictionary of the module
				if game_title in statistics_copy:
					# Define the "converted dictionary" switch as False
					converted_dictionary = False

					# If the game title key is a number
					if isinstance(statistics[key]["Dictionary"][game_title], int):
						# Create the game statistics dictionary
						statistics[key]["Dictionary"][game_title] = {
							"Total": statistics[key]["Dictionary"][game_title],
							"Dictionary": {}
						}

						# Switch the "converted dictionary" switch to True
						converted_dictionary = True

					# Add one to the total number of times the root game was played
					statistics[key]["Dictionary"][game_title]["Total"] += 1

					# Iterate through the list of items
					for item_title, item in game["Items"]["Dictionary"].items():
						# Define the local number as zero
						number = 0

						# If the item title is the game title
						# And the total number of played times is not zero
						# And the "converted dictionary" switch is True
						if (
							item_title == game_title and
							statistics[key]["Dictionary"][game_title]["Total"] != 0 and
							converted_dictionary == True
						):
							# Define the local number as the total number of played times
							number = statistics[key]["Dictionary"][game_title]["Total"]

						# If the first two characters of the item title is a colon and a space
						# (Remove the colon and space from the item title so the sub-game title is more beautiful inside the dictionary)
						if item_title[0] + item_title[1] == ": ":
							# Remove the colon and space
							item_title = item_title[2:]

						# If the "converted dictionary" switch is True
						if converted_dictionary == True:
							# Add the item title to the dictionary with the correct number (zero or the number of times the user played the root game)
							statistics[key]["Dictionary"][game_title]["Dictionary"][item_title] = number

						# If the current sub-game is the sub-game that was played
						if item_title == played_title:
							# Add one to the number of times the sub-game was played
							statistics[key]["Dictionary"][game_title]["Dictionary"][item_title] += 1

				# If the game title is not inside the statistics dictionary of the module
				if game_title not in statistics_copy:
					# Make a list of sub-games to iterate through
					sub_games = game["Items"]["List"]

					# Iterate through the list of items
					for item_title in sub_games:
						# Define the default sub-game title as the item title
						sub_game_title = item_title

						# If the sub-game title key exists inside the items dictionary
						if item_title in game["Items"]["Dictionary"]:
							# Get the item dictionary from it
							item = game["Items"]["Dictionary"][item_title]

							# Define the key to get the sub-game title
							item_key = "Original"

							if "Romanized" in item["With game title"]:
								item_key = "Romanized"

							# Define the key to get the number of times the sub-game was played
							sub_game_title = item["With game title"][item_key]

						# Define a local number as zero
						number = 0

						# If the sub-game title (with the game title) is inside the copy of the statistics dictionary
						if sub_game_title in statistics_copy:
							# Define the local number as the total number times the sub-game was played
							number = statistics_copy[sub_game_title]

						# If the game title is not inside the statistics dictionary of the module
						# Or it is, and the key is a number
						if (
							game_title not in statistics[key]["Dictionary"] or
							game_title in statistics[key]["Dictionary"] and
							isinstance(statistics[key]["Dictionary"][game_title], int)
						):
							# Define the new value dictionary as the game statistics dictionary
							new_value = {
								"Total": number,
								"Dictionary": {}
							}

							# If the item title is the game title
							if item_title == game_title:
								# Add the game title to the game dictionary
								new_value["Dictionary"][item_title] = 0

							# Define the "has previous key" switch as False
							has_previous_key = False

							# Define the default original key as None
							original_key = None

							# Iterate through the list of item titles
							for local_item in game["Items"]["Dictionary"].values():
								# Define the key to get the sub-game title
								item_key = "Original"

								if "Romanized" in local_item["With game title"]:
									item_key = "Romanized"

								# Define local sub-game title
								local_sub_game_title = local_item["With game title"][item_key]

								# If the sub-game title (with the game title) is inside the statistics dictionary
								if local_sub_game_title in statistics_copy:
									# Define the original key as the sub-game title
									original_key = local_sub_game_title

									# Switch the "has previous key" switch to True
									has_previous_key = True

							# If the original key is not None (it was found)
							if original_key != None:
								# Replaces the sub-game key with the root game key using the previous index
								statistics[key]["Dictionary"] = self.Add_To_Index(
									statistics_copy, # The dictionary of statistics
									original_key, # The original sub-game title key
									game_title, # The new key that is the root game title
									new_value # The new value to replace the sub-game dictionary
								)

							# If the "has previous key" switch is False
							if has_previous_key == False:
								# If the first two characters of the item title is a colon and a space
								# (Remove the colon and space from the item title so the sub-game title is more beautiful inside the dictionary)
								if item_title[0] + item_title[1] == ": ":
									# Remove the colon and space
									item_title = item_title[2:]

								# If the game title is not inside the statistics dictionary of the module
								# And the current sub-game is the root game or sub-game that was played
								if (
									game_title not in statistics[key]["Dictionary"] and
									item_title == played_title
								):
									# Add the the sub-game dictionary to the statistics dictionary with a value of zero
									statistics[key]["Dictionary"][sub_game_title] = 0

									# Update the game title key
									game_title_key = sub_game_title

									# Switch the "added sub-game dictionary" switch to True
									added_sub_game_dictionary = True

								# If the game title is inside the statistics dictionary of the module
								# And the key is a number
								if (
									game_title in statistics[key]["Dictionary"] and
									isinstance(statistics[key]["Dictionary"][game_title], int)
								):
									# Add the the game dictionary to the end of the statistics dictionary
									statistics[key]["Dictionary"][game_title] = new_value

						# If the first two characters of the item title is a colon and a space
						# (Remove the colon and space from the item title so the sub-game title is more beautiful inside the dictionary)
						if item_title[0] + item_title[1] == ": ":
							# Remove the colon and space
							item_title = item_title[2:]

						# Define the item dictionary as an empty dictionary
						item_dictionary = {}

						# If the sub-game title key is inside the statistics dictionary of the module
						if sub_game_title in statistics[key]["Dictionary"]:
							# Define a shortcut for the root sub-game dictionary as the "item dictionary" variable
							item_dictionary = statistics[key]["Dictionary"]

							# Define the "key to use" as the sub-game title
							key_to_use = sub_game_title

						# If the game title is inside the statistics dictionary of the module
						if game_title in statistics[key]["Dictionary"]:
							# Add the item title to the dictionary with the correct number (zero or the number of times the user played the root game)
							statistics[key]["Dictionary"][game_title]["Dictionary"][item_title] = number

							# Define a shortcut for the sub-game dictionary on the game title dictionary as the "item dictionary" variable
							item_dictionary = statistics[key]["Dictionary"][game_title]["Dictionary"]

							# Define the "key to use" as the item title
							key_to_use = item_title

						# If the current sub-game is the root game or sub-game that was played
						# And the item dictionary is not an empty dictionary
						if (
							item_title == played_title and
							item_dictionary != {}
						):
							# Add one to the number of times the sub-game was played, inside the item dictionary with the key to use
							item_dictionary[key_to_use] += 1

						# If the sub-game title is not the same as the game title
						# And the old sub-game title (with the game title) key is present inside the root game statistics dictionary
						# And the game title is inside the statistics dictionary of the module
						if (
							item_title != game_title and
							sub_game_title in statistics[key]["Dictionary"] and
							game_title in statistics[key]["Dictionary"]
						):
							# Remove the key
							statistics[key]["Dictionary"].pop(sub_game_title)

					# If the game title is inside the statistics dictionary of the module
					if game_title in statistics[key]["Dictionary"]:
						# Reset the total number to be zero
						statistics[key]["Dictionary"][game_title]["Total"] = 0

						# Iterate through the keys inside the root game dictionary
						for game_number in statistics[key]["Dictionary"][game_title]["Dictionary"].values():
							# Add the game number to the total number of times the root game was played
							statistics[key]["Dictionary"][game_title]["Total"] += game_number

			# Define the old number as the current number
			statistics["Dictionary"]["Numbers"][key]["Old"] = statistics[key]["Dictionary"][game_title_key]

			# If the "added sub-game dictionary" switch is True
			# And the old number is not zero
			if (
				added_sub_game_dictionary == True and
				statistics["Dictionary"]["Numbers"][key]["Old"] != 0
			):
				# Remove one from the old number
				statistics["Dictionary"]["Numbers"][key]["Old"] -= 1

			# If the old key is a dictionary
			if isinstance(statistics["Dictionary"]["Numbers"][key]["Old"], dict):
				# Get the number of the "Total" key
				statistics["Dictionary"]["Numbers"][key]["Old"] = statistics["Dictionary"]["Numbers"][key]["Old"]["Total"]

				# If the "Items" key does exist in the local game dictionary
				if "Items" in game:
					# Remove one from the number of times the sub-game was played
					statistics["Dictionary"]["Numbers"][key]["Old"] = statistics[key]["Dictionary"][game_title]["Dictionary"][played_title] - 1

			# If the "Items" key does not exist in the local game dictionary
			# And the game title key is a number
			if (
				"Items" not in game and
				isinstance(statistics[key]["Dictionary"][game_title_key], int)
			):
				# Update the number of times the root game was played
				statistics[key]["Dictionary"][game_title_key] += 1

			# Define the new number as the old number
			# (If the "Items" key exists inside the game dictionary, the old number has already been increased by 1)
			statistics["Dictionary"]["Numbers"][key]["New"] = statistics["Dictionary"]["Numbers"][key]["Old"]

			# Make a shortcut for the old and new numbers
			old = statistics["Dictionary"]["Numbers"][key]["Old"]
			new = statistics["Dictionary"]["Numbers"][key]["New"]

			# If the "Items" key does exist in the local game dictionary
			# Or the new and old number are equal
			if (
				"Items" in game or
				old == new
			):
				# Add one to the new number
				statistics["Dictionary"]["Numbers"][key]["New"] += 1

		# Define the local game title as the game title in the user language
		game_title = game["Titles"]["Language"]

		# If the "Sub-game" key is inside the dictionary of game titles
		if "Sub-game" in game["Titles"]:
			# Define the local game title as the sub-game title with the game title in the user language
			game_title = game["Titles"]["Sub-game"]["Language"]

		# Define the statistic text, formatting the template with the language game title
		statistics["Text"] = self.language_texts["times_that_i_played_the_{}_game_called_{}"].format(game_type, game_title)

		# ---------- #

		# Update the external statistics of the current year using the "Update_External_Statistics" root method of the "Diary_Slim" class
		# And return the statistics text
		return self.Diary_Slim.Update_External_Statistics(statistic_key, statistics)

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

		# Read the "Information.json" file of the game type
		dictionary["JSON"] = self.JSON.To_Python(dictionary["Folders"]["Game information"]["Information"])

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
				self.language["Small"]: self.game_types["Types"][self.language["Small"]].copy()
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
		numbers = self.JSON.To_Python(self.folders["Game information"]["Information"])["Numbers"]

		# Iterate through the list of English game types
		i = 0
		for game_type in self.game_types["Types"]["en"]:
			# Get the game type dictionary
			game_type = self.game_types[game_type]

			# If the number of games is zero, remove the game type from the lists
			if game_type["Game number"] == 0:
				dictionary["List"]["en"].remove(game_type["Type"]["en"])
				dictionary["List"][self.language["Small"]].remove(game_type["Type"][self.language["Small"]])

			i += 1

		# Iterate through the list of English game types
		i = 0
		for game_type in dictionary["List"]["en"]:
			# Iterate through the list of small languages
			for language in self.languages["Small"]:
				# Add the number of games to the game type text
				dictionary["List"][language][i] = dictionary["List"][language][i] + " (" + str(numbers[game_type]) + ")"

			i += 1

		# Select the game type
		if (
			"option" not in dictionary and
			"number" not in dictionary
		):
			dictionary["option"] = self.Input.Select(dictionary["List"]["en"], dictionary["List"][self.language["Small"]], show_text = dictionary["Texts"]["Show"], select_text = dictionary["Texts"]["Select"])["option"]

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
		dictionary["Texts"]["Show"] = dictionary["Type"][self.language["Small"]] + " (" + str(len(dictionary["Game list"])) + ")"

		return dictionary

	def Select_Game(self, options = None, define_item = False, play = False, game_title = None, sub_game_title = None):
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
		text = dictionary["Type"]["Type"][self.language["Small"]]

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
		root_folder = dictionary["Type"]["Folders"]["Game information"]["root"]

		# If the define item variable is True
		# And the sub-game is not the root game
		if (
			self.define_item == True and
			dictionary["Game"]["Sub-game"]["Title"] != dictionary["Game"]["Title"]
		):
			root_folder = dictionary["Game"]["Sub-games"]["Folders"]["root"]

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
			game["Information"]["File name"] = dictionary["Game"]["Sub-games"]["Texts"]["Singular"]["en"]

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
			items["Sub-game"] = dictionary["Game"]["Sub-games"]["Folders"]["root"] + self.Sanitize_Title(game["Title"]) + "/"

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

			# Get the "Gaming time" dictionary from the file if it is not empty
			if self.File.Contents(folder["Gaming time"]["Gaming time"])["lines"] != []:
				gaming_time = self.JSON.To_Python(folder["Gaming time"]["Gaming time"])

			# ----- #

			# Update the last played time

			entries_file = folder["Played"]["entries"]

			# If the file exists and is not empty
			if (
				self.File.Exists(entries_file) == True and
				self.File.Contents(entries_file)["lines"] != []
			):
				# Read the "Entries.json" file
				entries = self.JSON.To_Python(entries_file)

				# Get the dictionary of entries and transform it into a list
				dictionaries = list(entries["Dictionary"].values())

				# If the list is not empty
				if dictionaries != []:
					# Get the last entry from the dictionary
					last_entry = dictionaries[-1]

					# Get the last played time by using the correct key
					if "Times" in last_entry:
						last_played_time = last_entry["Times"]["Finished playing (UTC)"]

					if "Date" in last_entry:
						last_played_time = last_entry["Date"]

					# Update the last played time
					gaming_time["Times"]["Last"] = last_played_time

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
			if gaming_time["Text"][self.language["Small"]] != "":
				self.File.Edit(folder["Gaming time"]["Language gaming time"], gaming_time["Text"][self.language["Small"]], "w")

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
			game["Language"] = self.language["Full"]

			# Define a shortcut to the "Original language" text
			original_language_text = self.Language.language_texts["original_language"]

			# If the "Original language" key exists in the game "Details" dictionary
			if original_language_text in game["Details"]:
				# Define the game language as the original language
				game["Language"] = game["Details"][original_language_text]

			# Define a local list of full languages
			full_languages = list(self.languages["Full"].values())

			# If the game language is inside the local list of full languages
			if game["Language"] in full_languages:
				# Iterate through the language keys and dictionaries
				for small_language, language in self.languages["Dictionary"].items():
					# Define a shortcut to the full language
					full_language = language["Full"]

					# If the full current language is the same as the media language
					if full_language == game["Language"]:
						# Define the game full and small language as the current language
						game["Full language"] = full_language
						game["Language"] = small_language

			# ---------- #

			# Get the game platform from the game "Details" dictionary
			game_platform = game["Details"][self.Language.language_texts["platform, title()"]]

			# Iterate through the platforms inside the dictionary of platforms
			for platform in self.game_types["Platforms"].values():
				# Get the language platform
				language_platform = platform[self.language["Small"]]

				# If the game platform is the same as the current language platform
				if game_platform == language_platform:
					# Define the game platform dictionary as the current platform
					game["Platform"] = platform

			# ---------- #

			# Define the "Gaming environment" key as the language platform
			game["Gaming environment"] = game["Platform"]

			# Get the "Gaming environment" text and define it as the text key
			text_key = self.language_texts["gaming_environment"]

			# If the text key is inside the game "Details" dictionary
			if text_key in game["Details"]:
				# Define a local gaming environment dictionary
				gaming_environment = {}

				# Iterate through the list of small languages
				for language in self.languages["Small"]:
					# Define it as the gaming environment inside the game "Details" dictionary
					gaming_environment[language] = game["Details"][text_key]

				# Define it as the "Gaming environment" key
				game["Gaming environment"] = gaming_environment

			# ---------- #

			# Get the "Game link" text and define it as the text key
			text_key = self.language_texts["game_link"]

			# If the text key is inside the game "Details" dictionary
			if text_key in game["Details"]:
				# Get the game link from the game "Details" dictionary and define it in the "Link" key
				game["Link"] = game["Details"][text_key]

			# ---------- #

			# Define a dictionary of text keys to find
			text_keys = {
				"Game ID": self.language_texts["game_id"],
				"Asset ID": self.language_texts["asset_id"]
			}

			# Iterate through the dictionary keys and text keys
			for key, text_key in text_keys.items():
				# If the text key is inside the game "Details" dictionary
				if text_key in game["Details"]:
					# Get the game detail from the game "Details" dictionary and define it in the correct key
					game[key] = game["Details"][text_key]

			# ---------- #

			# Define the game states dictionary
			states = {
				"Re-playing": False,
				"Christmas": False,
				"Completed game": False,
				"First gaming session in the year": False,
				"First gaming session by game type in the year": False,
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

			game["States"]["First gaming session in the year"] = False

			if self.dictionaries["Sessions"]["Numbers"]["Total"] == 0:
				game["States"]["First gaming session in the year"] = True

			game["States"]["First gaming session by game type in the year"] = False

			if self.dictionaries["Game type"][dictionary["Type"]["Type"]["en"]]["Numbers"]["Total"] == 0:
				game["States"]["First gaming session by game type in the year"] = True

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

				if self.File.Exists(file) == True:
					game["Files"]["Shortcut"]["File"] += extension

					found_shortcut = True

			# If the shortcut is found, get its path
			if found_shortcut == True:
				import win32com.client

				shell = win32com.client.Dispatch("WScript.Shell")

				game["Files"]["Shortcut"]["Path"] = shell.CreateShortCut(game["Files"]["Shortcut"]["File"]).Targetpath.replace("\\", "/")

				if self.File.Exists(game["Files"]["Shortcut"]["Path"]) == False:
					game["Files"]["Shortcut"]["Path"] += "/"

			# Define the bat File for the game if it exists
			file = self.Folder.folders["Apps"]["Shortcuts"]["root"] + self.Sanitize(game["Title"], restricted_characters = True) + ".bat"

			if self.File.Exists(file) == True:
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
				value = self.Define_Sub_Games(dictionary, play = play, sub_game_title = sub_game_title)

				if value["Game"]["Sub-game"]["Title"] != dictionary["Game"]["Title"]:
					dictionary = value

			# ------------------------------ #

		return dictionary

	def Define_Sub_Games(self, dictionary, play = False, sub_game_title = None):
		# Define the "game" variable for easier typing
		game = dictionary["Game"]

		# Define the sub-game type dictionary
		game["Sub-games"] = {
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

			game["Sub-games"]["Key"] = game["Details"][key]

		# Define the sub-game type variable for easier typing
		sub_game_type = game["Sub-games"]["Key"]

		# Iterate through the text types list
		for text_type in ["Singular", "Plural"]:
			# Iterate through the small languages list
			# To define the sub-game type texts for all languages
			for language in self.languages["Small"]:
				# Define the text key
				text_key = sub_game_type[:-1].lower().replace(" ", "_")

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
				game["Sub-games"]["Texts"][text_type][language] = text

		# Create the [Sub-game type] folder
		game["Folders"][sub_game_type] = {
			"root": game["Folders"]["root"] + game["Sub-games"]["Texts"]["Plural"][self.language["Small"]] + "/"
		}

		self.Folder.Create(game["Folders"][sub_game_type]["root"])

		# Define the root folder of the "Sub-game type" dictionary
		game["Sub-games"]["Folders"] = deepcopy(game["Folders"][sub_game_type])

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
			game["Sub-games"]["Folders"][name] = game["Sub-games"]["Folders"]["root"] + text + ".txt"

			# Create the file
			self.File.Create(game["Sub-games"]["Folders"][name])

			# Get the contents of the file
			file = game["Sub-games"]["Folders"][name]

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
			game["Sub-games"]["Items"][name] = contents

			# If the name is "List"
			if name == "List":
				# Define the items number as the number of lines of the text file
				game["Sub-games"]["Items"]["Number"] = len(game["Sub-games"]["Items"]["List"])

		if game["Sub-games"]["Items"]["List"] == []:
			# Define the list of sub-games inside the dictionary as the list of folders
			game["Sub-games"]["Items"]["List"] = self.Folder.Contents(game["Sub-games"]["Folders"]["root"])["folder"]["names"]

			# Update the "List.txt" file
			self.File.Edit(game["Sub-games"]["Folders"]["List"], self.Text.From_List(game["Sub-games"]["Items"]["List"], next_line = True), "w")

		# Update the number of sub-games
		game["Sub-games"]["Items"]["Number"] = len(game["Sub-games"]["Items"]["List"])

		# Define the current sub-game as the first one if it is empty
		if game["Sub-games"]["Items"]["Current"] == "":
			# Define the first sub-game variable for easier typing
			first_sub_game = game["Sub-games"]["Items"]["List"][0]

			# Define the current sub-game
			game["Sub-games"]["Items"]["Current"] = first_sub_game

			# Update the "Current.txt" file
			self.File.Edit(game["Sub-games"]["Folders"]["Current"], first_sub_game, "w")

		# Iterate through the sub-games
		for sub_game in game["Sub-games"]["Items"]["List"]:
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

			# Create the "With game title" dictionary
			sub_game["With game title"] = {}

			# Iterate through the list of keys
			for key in ["Original", "Language"]:
				# Define the title as the game title in the user language
				title = game["Titles"][key]

				# Define the sub-game title variable for easier typing
				local_sub_game_title = sub_game["Titles"][key]

				# If the first two characters of the title are not a colon and a space
				if local_sub_game_title[0] + local_sub_game_title[1] != ": ":
					# Add a space
					title += " "

				# Add the sub-game title
				title += local_sub_game_title

				# Define the "sub-game title with the game title" text
				sub_game["With game title"][key] = title

			# Add the sub-game dictionary to the items dictionary
			game["Sub-games"]["Items"]["Dictionary"][sub_game["Title"]] = sub_game

			# Add the language sub-game title to the language list
			game["Sub-games"]["Items"]["Language list"].append(sub_game["Titles"]["Language"])

		# Ask the user to select a sub-game
		parameters = {
			"options": game["Sub-games"]["Items"]["List"],
			"language_options": game["Sub-games"]["Items"]["Language list"],

			"show_text": game["Sub-games"]["Texts"]["Plural"][self.language["Small"]],
			"select_text": self.Language.language_texts["select_an_item_from_the_list"]
		}

		# Sanitize the language titles
		i = 0
		for title in parameters["language_options"]:
			title = self.Sanitize_Title(title)

			parameters["language_options"][i] = title

			i += 1

		# If the sub-game title is None
		# And the play parameter is True
		if (
			sub_game_title == None and
			play == True
		):
			# Ask the user to select the sub-game
			game["Sub-game"] = self.Input.Select(**parameters)["option"]

		# Else, define the selected sub-game as the sub-game title (already selected/defined in the "game" dictionary)
		else:
			# Define the sub-game title
			game["Sub-game"] = sub_game_title

		# If the sub-game title is not the same as the game title
		if (
			game["Sub-game"] != None and
			game["Sub-game"] != game["Title"]
		):
			# Define a shortcut for the "Items" dictionary
			items_dictionary = game["Sub-games"]["Items"]["Dictionary"]

			# Define a shortcut for the sub-game title
			sub_game_title = game["Sub-game"]

			# If the sub-game title is present inside the dictionary
			if sub_game_title in items_dictionary:
				# Get the sub-game dictionary
				game["Sub-game"] = items_dictionary[sub_game_title]

			else:
				# Add a colon and a space before the sub-game title
				sub_game_title = ": " + sub_game_title

				# Try to find the sub-game again
				game["Sub-game"] = items_dictionary[sub_game_title]

		# Else, define the sub-game dictionary as a dictionary with only the game titles
		else:
			# Create the "Sub-game" key as an empty dictionary
			game["Sub-game"] = {}

			# Define the list of keys to import
			keys = [
				"Title",
				"Titles",
				"Folders"
			]

			# Add the "With game title" key if it exists inside the game dictionary
			if "With game title" in game:
				keys.append("With game title")

			# Copy the keys of the list to the sub-game dictionary
			game["Sub-game"] = {key: game[key] for key in keys}

			# Select the game to define its variables
			dict_ = self.Select_Game(dictionary, define_item = True)["Game"]["Sub-game"]

			# Add the returned keys to the sub-game dictionary
			game["Sub-game"].update({
				"Folders": dict_["Folders"],
				"Gaming time": dict_["Gaming time"]
			})

		return dictionary

	def Select_Game_Type_And_Game(self, options = None, game_title = None, sub_game_title = None, play = False):
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
			dictionary["Game"] = self.Select_Game(dictionary, play = play, game_title = game_title, sub_game_title = sub_game_title)["Game"]

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
			"First gaming session in the year",
			"First gaming session by game type in the year"
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

				for language in self.languages["Small"]:
					text = ""

					if key != "First gaming session by game type in the year":
						text_key = key.lower()

						if " " not in text_key:
							text_key += ", title()"

						if ", title()" not in text_key:
							text_key = text_key.replace(" ", "_")

						if text_key in self.Language.texts:
							text = self.Language.texts[text_key][language]

						else:
							text = self.texts[text_key][language]

					if key == "First gaming session by game type in the year":
						entry_item = dictionary["Type"]["Type"][language]

						text = self.texts["first_gaming_session_of_the_{}_game_category_in_the_year"][language].format(entry_item)

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

		if self.File.Exists(game["Folders"]["details"]) == True:
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

				if self.language["Small"] in game["Titles"]:
					game["Titles"][self.language["Small"]] = game["Titles"][self.language["Small"]] + " (" + game["Titles"]["Original"].split(" (")[-1]

			# Define game titles by language
			for language in self.languages["Small"]:
				key = self.Language.texts["title_in_language"][language][self.language["Small"]]

				if key in game["Details"]:
					game["Titles"][language] = game["Details"][key]

			game["Titles"]["Language"] = game["Titles"]["Original"]

			if self.language["Small"] in game["Titles"]:
				game["Titles"]["Language"] = game["Titles"][self.language["Small"]]

			if (
				self.language["Small"] not in game["Titles"] and
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
				# Get it from the gaming session duration inside the entry
				game["Gaming time"]["Times"][key] = entry["Session duration"][sub_key]["UTC"]["DateTime"]["Formats"]["YYYY-MM-DDTHH:MM:SSZ"]

			# If the key is "Last"
			# And the time string is not empty
			if (
				key == "Last" and
				game["Gaming time"]["Times"][key] != ""
			):
				# Get it from the gaming session duration inside the entry
				game["Gaming time"]["Times"][key] = entry["Session duration"][sub_key]["UTC"]["DateTime"]["Formats"]["YYYY-MM-DDTHH:MM:SSZ"]

			# Create the date dictionary of the played time
			game["Gaming time"]["Times"][key] = self.Date.From_String(game["Gaming time"]["Times"][key])

		# Iterate through the time difference keys
		for key, difference in entry["Session duration"]["Difference"]["Difference"].items():
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
		time_units = {}

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
				time_units[key] = game["Gaming time"]["Units"][key.capitalize()]

		# Define the added time as the first time
		game["Gaming time"]["Times"]["Added"] = deepcopy(game["Gaming time"]["Times"]["First"])

		# Add the game time difference time unit to the added time date object
		game["Gaming time"]["Times"]["Added"]["Object"] += self.Date.Relativedelta(**time_units)

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
		if game["Gaming time"]["Text"][self.language["Small"]] != "":
			self.File.Edit(game["Folders"]["Gaming time"]["Language gaming time"], game["Gaming time"]["Text"][self.language["Small"]], "w")

		# Return the game dictionary
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
				for language in self.languages["Small"]:
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
			for language in self.languages["Small"]:
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

		if status in self.texts["statuses, type: list"][self.language["Small"]]:
			return_english = True

		s = 0
		for english_status in self.texts["statuses, type: list"]["en"]:
			# Return the user language status
			if (
				return_english == False and
				english_status == status
			):
				status_to_return = self.texts["statuses, type: list"][self.language["Small"]][s]

			# Return the English status
			if (
				return_english == True and
				status == self.texts["statuses, type: list"][self.language["Small"]][s]
			):
				status_to_return = english_status

			s += 1

		return status_to_return

	def Change_Status(self, dictionary, status = ""):
		# If the "status" parameter is an empty string
		if status == "":
			# Define the status variable as the "Completed" status
			status = self.Language.language_texts["completed, title()"]

		# Update the "Status" language key in the game "Details" dictionary
		dictionary["Game"]["Details"][self.Language.language_texts["status, title()"]] = status

		# Update the game "Details.txt" file
		self.File.Edit(dictionary["Game"]["Folders"]["details"], self.Text.From_Dictionary(dictionary["Game"]["Details"]), "w")

		# Check the status of the game to update it inside the JSON files that lists the games
		self.Check_Status(dictionary)

	def Check_Status(self, dictionary):
		# Define a shortcut for the game type
		game_type = dictionary

		# If the "Type" key is inside the dictionary parameter
		# And the "JSON" key is inside the "Type" dictionary
		if (
			"Type" in dictionary and
			"JSON" in dictionary["Type"]
		):
			# Define the game type as the "Type" dictionary
			game_type = dictionary["Type"]

			# Get the language status of the game
			language_status = dictionary["Game"]["Details"][self.Language.language_texts["status, title()"]]

			# Get the English status of the game using the language status
			status = self.Get_Language_Status(language_status)

		# Read the "Information.json" file of the game type
		dictionary["JSON"] = self.JSON.To_Python(game_type["Folders"]["Game information"]["Information"])

		# Update the number of games inside the file
		dictionary["JSON"]["Number"] = len(dictionary["JSON"]["Titles"])

		# Sort the list of game titles of the game type
		dictionary["JSON"]["Titles"] = sorted(dictionary["JSON"]["Titles"], key = str.lower)

		# Make a local list of titles
		titles = []

		# If the "Type" key is inside the dictionary parameter
		# And the "JSON" key is not inside the "Type" dictionary
		if (
			"Type" in dictionary and
			"JSON" not in dictionary["Type"]
		):
			# Add the list of game titles from the JSON file to the local list of titles
			titles.extend(dictionary["JSON"]["Titles"])

		# If the "Type" key is inside the dictionary parameter
		# And the "JSON" key is inside the "Type" dictionary
		if (
			"Type" in dictionary and
			"JSON" in dictionary["Type"]
		):
			# Add the game title to the local list of titles
			titles.append(dictionary["Game"]["Title"])

		# Iterate through the list of playing statuses
		for playing_status in self.texts["statuses, type: list"]["en"]:
			# Iterate through the local list of game titles
			for game_title in titles:
				# If the "Type" key is inside the dictionary parameter
				# And the "JSON" key is not inside the "Type" dictionary
				if (
					"Type" in dictionary and
					"JSON" not in dictionary["Type"]
				):
					# Get the game folder
					folder = game_type["Folders"]["Game information"]["root"] + self.Sanitize_Title(game_title) + "/"

					# Get and read the game details file
					details_file = folder + self.Language.language_texts["details, title()"] + ".txt"
					details = self.File.Dictionary(details_file)

					# Get the language status of the game
					language_status = details[self.Language.language_texts["status, title()"]]

					# Get the English status of the game using the language status
					status = self.Get_Language_Status(language_status)

				# If the game status is equal to the current playing status on the for loop
				# And the game is not in the correct playing status list, add it to the correct list
				# (The list of the current playing status in the for loop)
				if (
					status == playing_status and
					game_title not in dictionary["JSON"]["Status"][playing_status]
				):
					dictionary["JSON"]["Status"][playing_status].append(game_title)

				# If the game status is not equal to the current playing status on the for loop
				# And the game is in the wrong playing status list, remove it from the wrong list
				# (The list of the current playing status in the for loop)
				if (
					status != playing_status and
					game_title in dictionary["JSON"]["Status"][playing_status]
				):
					dictionary["JSON"]["Status"][playing_status].remove(game_title)

			# Sort the list of games for the current playing status in the for loop
			dictionary["JSON"]["Status"][playing_status] = sorted(dictionary["JSON"]["Status"][playing_status], key = str.lower)

		# Update the "Information.json" file of the game type
		self.JSON.Edit(game_type["Folders"]["Game information"]["Information"], dictionary["JSON"])

		# Return the root dictionary
		return dictionary

	def Define_Title(self, titles, language = None, add_language = True, remove_colon = True):
		# If the language parameter is None
		if language == None:
			# Use the user language
			language = self.language["Small"]

		# Define the list of keys to search for the title
		keys = [
			"Original",
			language,
			"Romanized"
		]

		# If the "add language" parameter is False
		if add_language == False:
			keys.remove(language)

		# Iterate through the list of keys
		for key in keys:
			# If the key is inside the dictionary of titles
			if key in titles:
				# Define the current key as the 
				title_key = key

		# Get the title from the dictionary of titles using the defined title key
		title = titles[title_key]

		# If the number of characters in the title is more than one
		# And the first two characters of the title are a colon and a space
		# And the "remove colon" parameter is True
		if (
			len(title) > 1 and
			title[0] + title[1] == ": " and
			remove_colon == True
		):
			# Remove the colon and a space
			title = title[2:]

		# Return the title
		return title

	def Define_Year_Summary_Data(self, entry, language):
		# Get the language game type
		game_type = self.game_types[entry["Type"]]["Type"][language]

		# Define the game text, with the entry title with quotes
		text = '"' + self.Define_Title(entry["Game titles"], language) + '"'

		# If the "Sub-game titles" key is in the entry dictionary
		if "Sub-game titles" in entry:
			# Get the language sub-game title (and do not remove the colon)
			sub_game_title = self.Define_Title(entry["Sub-game titles"], remove_colon = False)

			# If the number of characters in the sub-game title is more than one
			# And the first two characters of the sub-game title are not colon and a space
			if (
				len(title) > 1 and
				title[0] + title[1] != ": "
			):
				# Add a space before the sub-game title
				sub_game_title = " " + sub_game_title

			# Add it to the entry text
			text += sub_game_title

		# Add the game type with a space to the text
		#text += " (" + game_type + ")"

		# Add a comma
		text += ", "

		# Add the gaming session duration to the text
		duration = deepcopy(entry["Times"]["Gaming session duration"])

		# Remove the text key
		duration.pop("Text")

		# Make the time text in the defined language
		duration = self.Date.Make_Time_Text(duration)[language]

		# Add the duration text and the duration
		text += self.Date.texts["duration, title()"][language] + ": " + duration + ", "

		# Get the date that the gaming session was finished
		date = self.texts["played_in"][language] + ": " + entry["Times"]["Finished playing"]

		# Add it to the text
		text += date

		# Return the text to the class that called the method
		return text

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
		for language in self.languages["Small"]:
			if language in game["Titles"]:
				print("\t" + game["Titles"][language])

		# --------------- #

		# Show the sub-game type text and the sub-game title
		# If the game has sub-games and the sub-game is not the game
		if (
			game["States"]["Has sub-games"] == True and
			game["Sub-game"]["Title"] != game["Title"]
		):
			# Define the sub-game variable for easier typing
			sub_game = game["Sub-game"]

			# Show the sub-game type text
			sub_game_type_text = game["Sub-games"]["Texts"]["Singular"][self.language["Small"]]

			print()
			print(sub_game_type_text + ":")

			# Show the original or romanized sub-game title
			key = "Original"

			if "Romanized" in sub_game["Titles"]:
				key = "Romanized"

			title = self.Sanitize_Title(sub_game["Titles"][key])

			print("\t" + title)

			# Show the language titles if they exist
			for language in self.languages["Small"]:
				if language in sub_game["Titles"]:
					title = self.Sanitize_Title(sub_game["Titles"][language])

					print("\t" + title)

			# Show the "With the game title" text
			text = sub_game_type_text + " " + self.language_texts["with_the_game_title"] 

			# Get the sub-game "With game title"
			title = game["Sub-game"]["With game title"]["Language"]

			print()
			print(text + ":")
			print("\t" + title)

		# --------------- #

		# Show the "Category" text
		print()
		print(self.Language.language_texts["category, title()"] + ":")

		# Show the categories
		types = []

		for language in self.languages["Small"]:
			text = "\t" + dictionary["Type"]["Type"][language]

			if text not in types:
				types.append(text)

		for item in types:
			print(item)

		# --------------- #

		# Show the platforms
		print()

		# Define a local list of platforms
		platforms = []

		# Iterate through the list of small languages
		for language in self.languages["Small"]:
			# Define the platform text in the current language
			text = "\t" + dictionary["Game"]["Platform"][language]

			# If it is not inside the local list of platforms
			if text not in platforms:
				platforms.append(text)

		# Show the "Platform" text
		print(self.Language.language_texts["platform, title()"] + ":")

		# Show the platforms
		for item in platforms:
			print(item)

		# --------------- #

		# Show the gaming environment if it is not the same as the platform

		# Define shortcuts for the game platform and gaming environment
		platform = dictionary["Game"]["Platform"]
		gaming_environment = dictionary["Game"]["Gaming environment"]

		# If the game platform and gaming environment are not the same
		if platform != gaming_environment:
			# Then show the gaming environment
			print()
			print(self.language_texts["gaming_environment"] + ":")
			print("\t" + gaming_environment[self.language["Small"]])

		# --------------- #

		# Show the folders of the game

		# Show only the information folder of the game if there is no local game folder
		# (The game must be web-based or played outside of the main platform (computer))
		if game["Folders"]["Local"]["root"] == "":
			print()
			print(self.Folder.language_texts["folder, title()"] + ":")
			print("\t" + game["Folders"]["root"])

		# If there is a local game folder
		if game["Folders"]["Local"]["root"] != "":
			# Show the "Folders" text
			print()
			print(self.Folder.language_texts["folders, title()"] + ":")

			# Show the "Information" game folder
			print("\t" + self.Language.language_texts["informations, title()"] + ":")
			print("\t" + game["Folders"]["root"])
			print()

			# Show the "Local" game folder
			print("\t" + self.Language.language_texts["local, title()"] + ":")
			print("\t" + game["Folders"]["Local"]["root"])

		# Show the sub-game folder if the game has sub-games and the sub-game title is not the root game title
		if (
			game["States"]["Has sub-games"] == True and
			game["Sub-game"]["Title"] != game["Title"]
		):
			print()
			print(self.language_texts["sub_game_folder"] + ":")
			print("\t" + game["Sub-game"]["Folders"]["root"])

		# --------------- #

		# Show the game shortcut file
		if self.File.Exists(game["Files"]["Shortcut"]["File"]) == True:
			print()
			print(self.Language.language_texts["shortcut, title()"] + ":")
			print("\t" + game["Files"]["Shortcut"]["File"])

		# Show the game shortcut file path
		if game["Files"]["Shortcut"]["Path"] != "":
			print()
			print(self.Language.language_texts["shortcut_path"] + ":")
			print("\t" + game["Files"]["Shortcut"]["Path"])

		# --------------- #

		# Show information about the gaming session played if the "Entry" key is present in the local dictionary
		if "Entry" in dictionary:
			# Check if the "Times" key is in the dictionary
			if "Times" in dictionary["Entry"]:
				# Define the playing text
				playing_text = " " + self.language_texts["playing, infinitive action"]

				# Iterate over the time types "started" and "finished"
				for time_key in ["started", "finished"]:
					# Construct the display text dynamically, e.g. "when_you_started" or "when_you_finished"
					text = self.Language.language_texts["when_you_" + time_key] + playing_text 

					# Format the dictionary key to match the stored time entries, e.g. "Started playing"
					time_key = time_key.capitalize() + " playing"

					# Show the composed text and the corresponding formatted time
					print()
					print(text + ":")
					print("\t" + dictionary["Entry"]["Times"][time_key]["Formats"]["HH:MM DD/MM/YYYY"])

				# Show the gaming session duration text in the user language
				print()
				print(self.Language.language_texts["gaming_session_duration"] + ":")
				print("\t" + dictionary["Entry"]["Times"]["Gaming session duration"]["Text"][self.language["Small"]])

			# --------------- #

			# If there are states, show them
			if (
				"States" in dictionary and
				dictionary["States"]["Texts"] != {}
			):
				print()
				print(self.Language.language_texts["states, title()"] + ":")

				for key in dictionary["States"]["Texts"]:
					print("\t" + dictionary["States"]["Texts"][key][self.language["Small"]])

			# If there is a session description, show it
			if (
				"Descriptions" in self.dictionary["Entry"]["Diary Slim"] and
				self.language["Small"] in self.dictionary["Entry"]["Diary Slim"]["Descriptions"]
			):
				# Show the user language "Gaming session description" text
				print()
				print(self.language_texts["gaming_session_description"] + ":")

				# Define the description variable for easier typing and a more beautiful code
				description = self.dictionary["Entry"]["Diary Slim"]["Descriptions"][self.language["Small"]]["lines"]

				# Show the description lines
				for line in description:
					print("\t" + line)

		# If the "Statistics text" key is present
		if "Statistics text" in self.dictionary:
			# Show the statistics text
			print(self.dictionary["Statistics text"])