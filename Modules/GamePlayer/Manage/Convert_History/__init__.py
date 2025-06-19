# Convert_History.py

# Import the root "GamePlayer" class
from GamePlayer.GamePlayer import GamePlayer as GamePlayer

# Import the "importlib" module
import importlib

# Import the "deepcopy" module from the "copy" module
from copy import deepcopy

class Convert_History(GamePlayer):
	def __init__(self):
		# Import the root "GamePlayer" class to import its variables and methods
		super().__init__()

		# Show a ten dash space separator
		print()
		print(self.separators["10"])
		print()

		# Show the "Convert history" text in the user language
		print(self.Language.language_texts["convert_history"] + ":")

		# Create the states dictionary
		self.states = {
			"Verbose": {
				"JSON": True,
				"Text": True
			},
			"Wait for input": True
		}

		# If the "Testing" switch is True
		if self.switches["Testing"] == True:
			# Change the "Verbose" states to False
			for state in self.states["Verbose"]:
				self.states["Verbose"][state] = False

			# Define a local "skip input" switch
			skip_input = False

			# If the "skip input" switch is False
			if skip_input == False:
				# Change the "Wait for input" to True
				self.states["Wait for input"] = True

		# Create the years dictionary
		self.Create_Years_Dictionary()

		# Create the games dictionary
		self.Create_Games_Dictionary()

		# Iterate through the year dictionary
		self.Iterate_Through_The_Year_Dictionary()

	def Create_Years_Dictionary(self):
		# Define the starting year as 2021
		starting_year = 2021

		# Create a list of years starting from the starting year to the current year
		years_list = self.Date.Create_Years_List(start = starting_year)

		# Create the years dictionary
		self.years = {
			"Numbers": {
				"Total": len(years_list) # The total number of years
			},
			"List": years_list, # The list of years
			"Lists": { # The dictionary of year lists
				"Skip": [
					#"2021",
					#"2022",
					#"2023",
					#"2024"
				],
				"Skip input": [ # The list of years where to skip the user input
					"2021",
					"2022",
					"2023",
					"2024",
					"2025"
				]
			},
			"Dictionary": {} # The years dictionary
		}

		# Remove the years from the skip list from the list of years
		for year_number in self.years["Lists"]["Skip"]:
			if year_number in self.years["List"]:
				self.years["List"].remove(year_number)

		# Iterate through the list of years
		for year_number in self.years["List"]:
			# Define the year dictionary with its keys and values
			year = {
				"Number": str(year_number),
				"Folders": {
					"Play History": {
						"root": "",
						"Entries": "",
						"Entry list": ""
					},
					"Play History (by game type)": {
						"root": ""
					},
					"Year": {
						"Gaming sessions": {},
						"Firsts of the Year": {}
					}
				},
				"Entries": {
					"Play History": {},
					"Play History (by game type)": {}
				},
				"Entry list": {
					"Play History": {},
					"Play History (by game type)": {}
				}
			}

			# ---------- #

			# Play History folders and files

			# Define the "Play History" root folder
			year["Folders"]["Play History"]["root"] = self.folders["Play History"]["root"] + str(year_number) + "/"

			# Define a shortcut to the play history folder
			play_history = year["Folders"]["Play History"]

			# ----- #

			# Define the play history "Sessions.json" file
			play_history["Entries"] = play_history["root"] + "Sessions.json"

			# Read the file and add the JSON dictionary to the play history "Entries" dictionary
			year["Entries"]["Play History"] = self.JSON.To_Python(play_history["Entries"])

			# ----- #

			# Define the play history "Entry list.txt" file
			play_history["Entry list"] = play_history["root"] + "Entry list.txt"

			# Read the file to get the file contents
			contents = self.File.Contents(play_history["Entry list"])

			# Add the text contents dictionary to the "Entry list" dictionary
			year["Entry list"]["Play History"] = {
				"Lines": contents["Lines"]
			}

			# ----- #

			# Define the "By game type" root folder
			year["Folders"]["Play History (by game type)"]["root"] = play_history["root"] + "By game type/"

			# Define a shortcut to the by game type folder
			by_game_type = year["Folders"]["Play History (by game type)"]

			# ---------- #

			# Play History (by game type) folders and files

			# Iterate through the English game types list
			for english_game_type in self.game_types["Types"]["en"]:
				# Get the root game type dictionary
				root_game_type = self.game_types[english_game_type]

				# Define the game type dictionary
				game_type = {
					"Game type": root_game_type["Type"],
					"Folders": {
						"root": by_game_type["root"] + english_game_type + "/"
					}
				}

				# Define a shortcut to the game type folders
				game_type_folders = game_type["Folders"]

				# ----- #

				# Define the game type "Sessions.json" file
				game_type_folders["Entries"] = game_type_folders["root"] + "Sessions.json"

				# Read the file and add the JSON dictionary to the play history (by game type) "Entries" dictionary of the current game type
				year["Entries"]["Play History (by game type)"][english_game_type] = self.JSON.To_Python(game_type_folders["Entries"])

				# ----- #

				# Define the game type "Entry list.txt" file
				game_type_folders["Entry list"] = game_type_folders["root"] + "Entry list.txt"

				# Read the file to get the file lines
				lines = self.File.Contents(game_type_folders["Entry list"])["Lines"]

				# Add the text contents dictionary to the play history (by game type) "Entry list" dictionary of the current game type
				year["Entry list"]["Play History (by game type)"][english_game_type] = contents["Lines"]

				# ----- #

				# Define the "Files" folder
				game_type_folders["Files"] = {
					"root": game_type_folders["root"] + "Files/"
				}

				# Add the game type dictionary to the "Play History (by game type)" dictionary
				year["Folders"]["Play History (by game type)"][english_game_type] = game_type

			# ---------- #

			# Year folders

			# Iterate through the list of folder types
			for folder_type in ["Gaming sessions", "Firsts of the Year"]:
				# Get the folder dictionary of the folder type
				dictionary = year["Folders"]["Year"][folder_type]

				# Iterate through the list of small languages
				for language in self.languages["small"]:
					# If the language folder key does not exist, create it
					if language not in dictionary:
						dictionary[language] = {}

					# Get the root year folders dictionary from the "Years" module
					year_folders = self.Years.years["Dictionary"][year_number]["Folders"]

					# Define a shortcut for the [folder type] folder
					folder = year_folders[language][folder_type]

					# If the folder type is "Gaming sessions"
					if folder_type == "Gaming sessions":
						# Iterate through the English game types list
						for english_game_type in self.game_types["Types"]["en"]:
							# Get the root game type dictionary
							root_game_type = self.game_types[english_game_type]

							# Get the language game type for the current language
							language_game_type = root_game_type["Type"][language]

							# Define the folder
							folder[english_game_type] = {
								"root": folder["root"] + language_game_type + "/"
							}

					# If the folder type is "Firsts of the Year"
					if folder_type == "Firsts of the Year":
						# Define the sub-folder name as the "Gaming session" text in the current language
						sub_folder_name = self.Language.texts["gaming_session"][language]

						# Define the folder as the root "Firsts of the Year" plus the sub-folder
						folder = {
							"root": folder["root"] + sub_folder_name + "/"
						}

						# Create the folder
						self.Folder.Create(folder["root"])

					# Add the [folder type] folder to the local folder dictionary
					dictionary[language] = folder

			# ---------- #

			# Add the local year dictionary to the root years dictionary
			self.years["Dictionary"][year_number] = year

			# ---------- #

			# Create a "Year.json" file to store the year dictionary
			year_file = year["Folders"]["Play History"]["root"] + "Year.json"
			self.File.Create(year_file)

			# Write the year dictionary into the "Year.json" file
			self.JSON.Edit(year_file, year, verbose = self.states["Verbose"]["JSON"])

	def Create_Games_Dictionary(self):
		# Define the root games dictionary
		self.games = {
			"Numbers": {
				"Total": 0
			},
			"List": [],
			"Dictionary": {}
		}

	def Iterate_Through_The_Year_Dictionary(self):
		# Define a list of JSON files to update:
		# [X] - Game type "Sessions.json" file

		# Define a list of JSON and entry list files to update:
		# Action:
		# Iterate through the games inside the games dictionary to update the "Played":
		# [X] - Game "Entries.json" file
		# [X] - Game "Entry list.txt" file
		# [X] - Sub-game "Entries.json" file
		# [X] - Sub-game "Entry list.txt" file

		# Define a list of entry text files to update:
		# Action:
		# Iterate through the years inside the years dictionary to update the root and sub-game "Played" entry text files with the "Replace_Text" method
		# 
		# [X] - Game "Played" entry text files

		# Todo:
		# Check all the checkboxes, then test the class

		# ---------- #

		# Initialize the index of the current year, starting at one
		current_year_index = 1

		# Get the number of years
		number_of_years = str(self.years["Numbers"]["Total"])

		# Iterate through the years dictionary, getting the year number and dictionary
		for year_number, year in self.years["Dictionary"].items():
			# Define the year information text
			year_information = f"""
			{self.separators["10"]}

			{self.Date.language_texts["number_of_the_year"]}:
			[{current_year_index}/{number_of_years}]

			{self.Date.language_texts["year"].title()}:
			[{year_number}]""".replace("\t", "")

			# Show the year information text
			print(year_information)

			# ---------- #

			# Define a local game type number as one
			game_type_number = 1

			# Get the number of game types
			number_of_game_types = str(len(self.game_types["Types"]["en"]))

			# Iterate through the English game types list
			for english_game_type in self.game_types["Types"]["en"]:
				# Get the root game type dictionary
				root_game_type = self.game_types[english_game_type]

				# Get the language game type for the user language
				language_game_type = root_game_type["Type"][self.user_language]

				# Get the game type folders
				game_type_folders = year["Folders"]["Play History (by game type)"][english_game_type]["Folders"]

				# Show the year information text
				print(year_information)

				# Show the number of the game type
				print()
				print(self.language_texts["number_of_the_game_type"] + ":")
				print("[" + str(game_type_number) + "/" + str(number_of_game_types) + "]")

				# Show the language game type
				print()
				print(self.language_texts["game_type"] + ":")
				print("[" + language_game_type + "]")

				# Get the "Entries" dictionary of the current game type
				game_type_entries = year["Entries"]["Play History (by game type)"][english_game_type]

				# Define a shortcut to the list of entries of the current game type
				entry_list = game_type_entries["Entries"]

				# Get the game type entries dictionary
				entries_dictionary = game_type_entries["Dictionary"]

				# Get the keys of the dictionary
				keys = list(entries_dictionary.keys())

				# If the list of entries ("Entries" key) is not the same as the list of dictionary keys
				if entry_list != keys:
					# Update the list of entries to be the list of dictionary keys
					game_type_entries["Entries"] = keys

				# Get the entries file of the current game type
				game_type_entries_file = game_type_folders["Entries"]

				# Update the game type "Sessions.json" file with the updated game type "Entries" dictionary
				# (Game type "Sessions.json" file)
				self.JSON.Edit(game_type_entries_file, game_type_entries)

				# Add one to the game type number
				game_type_number += 1

			# ---------- #

			# Get the entries for the current year
			entries = year["Entries"]["Play History"]

			# Define a local entry number as one
			entry_number = 1

			# Get the number of entries
			number_of_entries = str(len(entries["Entries"]))

			# Iterate through the entries dictionary
			for entry_name, entry in entries["Dictionary"].items():
				# Show the year information text
				print(year_information)

				# ----- #

				# Show the number of the entry
				print()
				print(self.Language.language_texts["number_of_the_entry"] + ":")
				print("[" + str(entry_number) + "/" + str(number_of_entries) + "]")

				# Show the name of the entry
				print()
				print(self.Language.language_texts["entry_name"] + ":")
				print("[" + entry_name + "]")

				# ----- #

				# Get the game type of the entry
				english_game_type = entry["Game type"]

				# Get the root game type dictionary
				root_game_type = self.game_types[english_game_type]

				# Get the language game type for the user language
				language_game_type = root_game_type["Type"][self.user_language]

				# Get the "Entries" dictionary of the current game type
				game_type_entries = year["Entries"]["Play History (by game type)"][english_game_type]

				# If the entry name is not inside the list of game type entries
				if entry_name not in game_type_entries["Entries"]:
					# Show a text telling that to the user
					print(self.language_texts["the_entry_is_not_inside_the_list_of_game_type_entries"] + ".")
					input()

				# Define a shortcut to the game type folders
				game_type_folders = year["Folders"]["Play History (by game type)"][english_game_type]["Folders"]

				# Get the game type "Game information" folder
				game_information_folder = self.game_types[english_game_type]["Folders"]["Game information"]

				# ----- #

				# Define a shortcut to the game titles dictionary
				game_titles = entry["Game titles"]

				# Get the original game title
				game_title = self.Define_Title(game_titles, add_language = False)

				# Get the language game title
				language_game_title = self.Define_Title(game_titles)

				# Show the language game title
				print()
				print(self.language_texts["game_title"] + ":")
				print("[" + language_game_title + "]")

				# ----- #

				# If the game title is not in the game dictionary
				if game_title not in self.games["List"]:
					# Define the game dictionary
					game = {
						"Title": game_title,
						"Titles": game_titles,
						"Root dictionary": {},
						"Folders": {
							"root": "",
							"Played": {
								"root": "",
								"Entries": "",
								"Entry list": "",
								"Files": {
									"root": ""
								}
							},
							"Played (sub-games)": {}
						},
						"Entries": {
							"Played": {},
							"Played (sub-games)": {}
						},
						"Entry list": {
							"Played": [],
							"Played (sub-games)": {}
						}
					}

					# ----- #

					# Define the root game dictionary with the game type and the game
					game["Root dictionary"] = {
						"Type": root_game_type,
						"Game": {
							"Title": game_title
						}
					}

					# Select the game and define its variables, returning the game dictionary (without asking the user to select the game)
					game["Root dictionary"] = self.Select_Game(game["Root dictionary"])

					# ----- #

					# Import the root folder
					game["Folders"]["root"] = game["Root dictionary"]["Game"]["Folders"]["root"]

					# ----- #

					# Define a shortcut to the game "Played" folder
					played_folder = game["Root dictionary"]["Game"]["Folders"]["Played"]

					# Import the "Played" folders and files
					game["Folders"]["Played"]["root"] = played_folder["root"]
					game["Folders"]["Played"]["Entries"] = played_folder["entries"]
					game["Folders"]["Played"]["Entry list"] = played_folder["entry_list"]
					game["Folders"]["Played"]["Files"] = played_folder["files"]

					# ----- #

					# If the entries "Played" key is an empty dictionary
					if game["Entries"]["Played"] == {}:
						# Define a default played"Entries" dictionary
						game["Entries"]["Played"] = {
							"Numbers": {
								"Total": 0
							},
							"Entries": [],
							"Dictionary": {}
						}

					# ----- #

					# Add the game to the list of games
					self.games["List"].append(game_title)

					# Update the number of games in the list
					self.games["Numbers"]["Total"] = len(self.games["List"])

					# ----- #

					# Add the game dictionary to the dictionary of games
					self.games["Dictionary"][game_title] = game

				# ----- #

				# If the game title is in the list of games
				if game_title in self.games["List"]:
					# Get the game dictionary
					game = self.games["Dictionary"][game_title]

				# ----- #

				# If the "Sub-game titles" key is in the entry dictionary
				# Or the game has sub-games
				if (
					"Sub-game titles" in entry or
					game["Root dictionary"]["Game"]["States"]["Has sub-games"] == True
				):
					# Define the titles key to search for the titles
					titles_key = "Game titles"

					# If the "Sub-game titles" key is in the entry dictionary
					if "Sub-game titles" in entry:
						# Define the titles key as "Sub-game titles"
						titles_key = "Sub-game titles"

					# Get the sub-game title
					sub_game_title = self.Define_Title(entry[titles_key], add_language = False)

					# Get the language sub-game title
					language_sub_game_title = self.Define_Title(entry[titles_key])

					# Show the language game title
					print()
					print(self.language_texts["sub_game_title"] + ":")
					print("[" + language_sub_game_title + "]")

				# ----- #

				# Define a shortcut to the entries dictionary
				entries = game["Entries"]["Played"]

				# If the entry is not in the "Entries" list
				if entry_name not in entries["Entries"]:
					# Add the entry to the entries list
					entries["Entries"].append(entry_name)

				# Update the number of entries in the list
				entries["Numbers"]["Total"] = len(entries["Entries"])

				# ----- #

				# Add the entry dictionary to the entries dictionary
				entries["Dictionary"][entry_name] = entry

				# ----- #

				# Define a shortcut to the game entry list
				entry_list = game["Entry list"]["Played"]

				# If the entry is not in the "Entry list" list
				if entry_name not in entry_list:
					# Add the entry to the entry list
					entry_list.append(entry_name)

				# ----- #

				# If the "Sub-game titles" key is in the entry dictionary
				# Or the game has sub-games
				if (
					"Sub-game titles" in entry or
					game["Root dictionary"]["Game"]["States"]["Has sub-games"] == True
				):
					# And the sub-game is not in the played (sub-games) "Entries" dictionary
					if sub_game_title not in game["Entries"]["Played (sub-games)"]:
						# Define the sub-game in the root game dictionary
						game["Root dictionary"] = self.Define_Sub_Games(game["Root dictionary"], sub_game_title = sub_game_title)

						# ----- #

						# Define a shortcut to the sub-game "Played" folder
						played_folder = game["Root dictionary"]["Game"]["Sub-game"]["Folders"]["Played"]

						# Define the sub-game dictionary
						game["Folders"]["Played (sub-games)"][sub_game_title] = {}

						# Import the "Played" folders and files
						game["Folders"]["Played (sub-games)"][sub_game_title]["root"] = played_folder["root"]
						game["Folders"]["Played (sub-games)"][sub_game_title]["Entries"] = played_folder["entries"]
						game["Folders"]["Played (sub-games)"][sub_game_title]["Entry list"] = played_folder["entry_list"]
						game["Folders"]["Played (sub-games)"][sub_game_title]["Files"] = played_folder["files"]

						# Define a default played (sub-games) "Entries" dictionary
						game["Entries"]["Played (sub-games)"][sub_game_title] = {
							"Numbers": {
								"Total": 0
							},
							"Entries": [],
							"Dictionary": {}
						}

					# ----- #

					# If the sub-game is not in the played (sub-games) "Entry list" dictionary
					if sub_game_title not in game["Entry list"]["Played (sub-games)"]:
						# Define a default played (sub-games) "Entry list" list
						game["Entry list"]["Played (sub-games)"][sub_game_title] = []

					# ----- #

					# Define a shortcut to the sub-game entries dictionary
					sub_game_entries = game["Entries"]["Played (sub-games)"][sub_game_title]

					# If the entry is not in the "Entries" list
					if entry_name not in sub_game_entries["Entries"]:
						# Add the entry to the entries list
						sub_game_entries["Entries"].append(entry_name)

					# Update the number of entries in the list
					sub_game_entries["Numbers"]["Total"] = len(sub_game_entries["Entries"])

					# Add the entry dictionary to the entries dictionary
					sub_game_entries["Dictionary"][entry_name] = entry

					# ----- #

					# Define a shortcut to the sub-game entry list
					sub_game_entry_list = game["Entry list"]["Played (sub-games)"][sub_game_title]

					# If the entry is not in the "Entry list" list
					if entry_name not in sub_game_entry_list:
						# Add the entry to the entry list
						sub_game_entry_list.append(entry_name)

					# ----- #

					# Update the game dictionary in the dictionary of games
					self.games["Dictionary"][game_title] = game

				# ----- #

				# Get the gaming session number
				gaming_session_number = entry["Gaming session number"]

				# Get the finished playing time
				finished_playing_time = entry["Times"]["Finished playing"]

				# Define a file name template
				template = str(gaming_session_number) + ". {} (" + finished_playing_time + ")"

				# Define a dictionary of entry file names
				file_names = {
					"Normal": {},
					"Sanitized": {}
				}

				# Iterate through the list of small languages
				for language in self.languages["small"]:
					# Define the normal file name of the current language with the current language media type
					file_names["Normal"][language] = template.format(root_game_type["Type"][language])

					# Define the sanitized version of it
					file_names["Sanitized"][language] = file_names["Normal"][language].replace(":", ";").replace("/", "-")

				# ----- #

				# Define a dictionary of entry files to update
				entry_files = {
					"Play History (by game type)": {},
					"Gaming sessions (Português)": {},
					"Gaming sessions (English)": {},
					"Firsts of the Year (Português)": {},
					"Firsts of the Year (English)": {},
					"Played": {},
					"Played (sub-game)": {}
				}

				# Define the play history (by game type) entry file dictionary
				entry_files["Play History (by game type)"] = {
					"Language": self.user_language,
					"File": game_type_folders["Files"]["root"] + file_names["Sanitized"]["en"] + ".txt"
				}

				# Iterate through the list of small languages
				for language in self.languages["small"]:
					# Get the full language
					full_language = self.languages["full"][language]

					# Define the language gaming sessions entry file dictionary
					entry_files["Gaming sessions ({})".format(full_language)] = {
						"Language": language,
						"File": year["Folders"]["Year"]["Gaming sessions"][language][english_game_type]["root"] + file_names["Sanitized"][language] + ".txt"
					}

					# If the gaming session is the first one in the year
					if gaming_session_number == 1:
						# Define the language firsts of the year entry file dictionary
						entry_files["Firsts of the Year ({})".format(full_language)] = {
							"Language": language,
							"File": year["Folders"]["Year"]["Firsts of the Year"][language]["root"] + file_names["Sanitized"][language] + ".txt"
						}

				# ----- #

				# Define a shortcut to the played "Files" folder
				folder = game["Folders"]["Played"]["Files"]["root"]

				# Define the old file
				old_file = folder + file_names["Sanitized"]["en"] + ".txt"

				# Define the new file
				new_file = folder + file_names["Sanitized"][self.user_language] + ".txt"

				# If the new file does not exist
				if self.File.Exist(new_file) == False:
					# Rename the file
					self.File.Move(old_file, new_file)

				# Define the game "Played" entry file
				entry_files["Played"] = {
					"Language": self.user_language,
					"File": new_file
				}

				# ----- #

				# If the "Sub-game titles" key is in the entry dictionary
				# Or the game has sub-games
				if (
					"Sub-game titles" in entry or
					game["Root dictionary"]["Game"]["States"]["Has sub-games"] == True
				):
					# Define a shortcut to the folder
					folder = game["Folders"]["Played (sub-games)"][sub_game_title]["Files"]["root"]

					# Define the old file	
					old_file = folder + file_names["Sanitized"]["en"] + ".txt"

					# Define the new file
					new_file = folder + file_names["Sanitized"][self.user_language] + ".txt"

					# If the new file does not exist
					if self.File.Exist(new_file) == False:
						# Rename the file
						self.File.Move(old_file, new_file)

					# Define the sub-game "Played" entry file
					entry_files["Played (sub-game)"] = {
						"Language": self.user_language,
						"File": new_file
					}

				# ----- #

				# Iterate through the dictionary of entry text files
				for dictionary in entry_files.values():
					# If the dictionary is not empty
					if dictionary != {}:
						# Get the file language
						file_language = dictionary["Language"]

						# Get the file
						entry_file = dictionary["File"]

						# Get the file text contents
						contents = self.File.Contents(entry_file)

						# If the file does not exist
						if self.File.Exist(entry_file) == False:
							# Show a ten dash space separator
							print()
							print(self.separators["10"])
							print()

							# Tell the user that the file does not exist
							print(self.File.language_texts["this_file_does_not_exist"] + ":")

							# Format the file to show to the user (make it clickable in a better console, like ConEmu)
							file = self.Language.language_texts["file_format, type: format"].format(entry_file.replace(" ", "%20"))

							# Show the file
							print(file)
							print()

							# If the current year is not inside the list of years to skip the input part
							if year_number not in self.years["Lists"]["Skip input"]:
								# Ask for user input before continuing the program execution
								input()

						# Update the entry text to fix some wrong texts
						# Passing the entry dictionary, the file text contents, and the file language as method parameters
						# And getting back the updated text
						text = self.Update_Entry_Text(entry, contents, file_language)

						# If the file text contents and the updated text are not the same
						if contents["String"] != text:
							# Show a ten dash space separator
							print()
							print(self.separators["10"])
							print()

							# Format the file to show to the user (make it clickable in a better console, like ConEmu)
							file = self.Language.language_texts["file_format, type: format"].format(entry_file.replace(" ", "%20"))

							# Show the file
							print(self.File.language_texts["file, title()"] + ":")
							print(file)
							print()

							# Show the text
							print(self.Language.language_texts["text, title()"] + ":")
							print("[" + text + "]")

							# If the current year is not inside the list of years to skip the input part
							if year_number not in self.years["Lists"]["Skip input"]:
								# Ask for user input before continuing the program execution
								input()

						# Write the updated text into the entry file
						self.File.Edit(entry_file, text, "w")

				# ----- #

				# Increment the entry number by one
				entry_number += 1

			# ---------- #

			# Increment the current year index by one
			current_year_index += 1

			# ---------- #

			# If the "Testing" switch is enabled
			# And the "Wait for input" state is active
			# And the current year is not the last one in the list
			if (
				self.switches["Testing"] == True and
				self.states["Wait for input"] == True and
				year_number != self.years["List"][-1]
			):
				# Show a ten dash space separator
				print()
				print(self.separators["10"])

				# Define the next text
				next_text = self.Language.language_texts["next, title()"] + " " + self.Date.language_texts["year, title()"]

				# Format it
				next_text = " ({})".format(next_text.lower())

				# Ask the user to press Enter to advance to the next year
				self.Input.Type(self.Language.language_texts["continue, title()"] + next_text)

		# ---------- #

		# Show a ten dash space separator
		print()
		print(self.separators["10"])

		# Initialize the index of the current game, starting at one
		current_game_index = 1

		# Get the number of games
		number_of_games = str(self.games["Numbers"]["Total"])

		# Iterate through the dictionary of games, getting the game title and dictionary
		for game_title, game in self.games["Dictionary"].items():
			# Show the number of the game
			print()
			print(self.language_texts["number_of_the_game"] + ":")
			print("[" + str(current_game_index) + "/" + str(number_of_games) + "]")

			# ----- #

			# Define a shortcut to the root game dictionary
			root_game_dictionary = game["Root dictionary"]["Game"]

			if "Titles" not in root_game_dictionary:
				self.JSON.Show(game)
				input()

			# Define a shortcut to the game titles dictionary
			game_titles = root_game_dictionary["Titles"]

			# Get the original game title
			game_title = self.Define_Title(game_titles, add_language = False)

			# Get the language game title
			language_game_title = self.Define_Title(game_titles)

			# Show the language game title
			print()
			print(self.language_texts["game_title"] + ":")
			print("[" + language_game_title + "]")

			# ----- #

			# Define a shortcut to the game played "Entries.json" file
			game_entries_file = game["Folders"]["Played"]["Entries"]

			# Define a shortcut to the game played "Entries" dictionary
			game_entries = game["Entries"]["Played"]

			if game_title == "Don't Starve":
				self.JSON.Show(game_entries)

			# Update the game played "Entries.json" file with the updated "Entries" dictionary
			# (Game played "Entries.json" file)
			self.JSON.Edit(game_entries_file, game_entries)

			# ----- #

			# Define a shortcut to the game played "Entry list.txt" file
			game_entry_list_file = game["Folders"]["Played"]["Entry list"]

			# Define a shortcut to the game played "Entry list" list
			game_entry_list = game["Entry list"]["Played"]

			# Convert it to a string
			game_entry_list = self.Text.From_List(game_entry_list, next_line = True)

			# Update the game played "Entry list.txt" file with the updated "Entry list" list
			# (Game played "Entry list.txt" file)
			self.File.Edit(game_entry_list_file, game_entry_list, "w")

			# ----- #

			# If the sub-game "Entries" dictionary is not empty
			if game["Entries"]["Played (sub-games)"] != {}:
				# Initialize the index of the current sub-game, starting at one
				current_sub_game_index = 1

				# Get the number of sub-games
				number_of_sub_games = str(len(list(game["Entries"]["Played (sub-games)"].keys())))

				# Iterate through the sub-games
				for sub_game_title, sub_game_entries in game["Entries"]["Played (sub-games)"].items():
					# Show the number of the sub-game
					print()
					print(self.language_texts["number_of_the_sub_game"] + ":")
					print("[" + str(current_sub_game_index) + "/" + str(number_of_sub_games) + "]")

					# ----- #

					# Define the sub-game dictionary
					game["Root dictionary"] = self.Define_Sub_Games(game["Root dictionary"], sub_game_title = sub_game_title)

					# Define a shortcut to the root game dictionary
					root_game_dictionary = game["Root dictionary"]["Game"]

					# Define a shortcut to the sub-game dictionary
					sub_game = root_game_dictionary["Sub-game"]

					# ----- #

					# Define a shortcut to the sub-game titles dictionary
					sub_game_titles = sub_game["Titles"]

					# Get the original sub-game title
					sub_game_title = self.Define_Title(sub_game_titles, add_language = False)

					# Get the language sub-game title
					language_sub_game_title = self.Define_Title(sub_game_titles)

					# Show the language sub-game title
					print()
					print(self.language_texts["sub_game_title"] + ":")
					print("[" + language_sub_game_title + "]")

					# ----- #

					# Define a shortcut to the sub-game played "Entries.json" file
					sub_game_entries_file = game["Folders"]["Played (sub-games)"][sub_game_title]["Entries"]

					if game_title == "Don't Starve":
						self.JSON.Show(sub_game_entries)

					# Update the sub-game played "Entries.json" file with the updated "Entries" dictionary
					# (Sub-game played "Entries.json" file)
					self.JSON.Edit(sub_game_entries_file, sub_game_entries)

					# ----- #

					# Define a shortcut to the sub-game played "Entry list.txt" file
					sub_game_entry_list_file = game["Folders"]["Played (sub-games)"][sub_game_title]["Entry list"]

					# Define a shortcut to the sub-game played "Entry list" list
					sub_game_entry_list = game["Entry list"]["Played (sub-games)"][sub_game_title]

					# Convert it to a string
					sub_game_entry_list = self.Text.From_List(sub_game_entry_list, next_line = True)

					# Update the sub-game played "Entry list.txt" file with the updated "Entry list" list
					# (Sub-game played "Entry list.txt" file)
					self.File.Edit(sub_game_entry_list_file, sub_game_entry_list, "w")

					# ----- #

					# Increment the current sub-game index by one
					current_sub_game_index += 1

			# ----- #

			# Increment the current game index by one
			current_game_index += 1

			# ---------- #

			# If the "Testing" switch is enabled
			# And the "Wait for input" state is active
			# And the current game is not the last one in the list
			if (
				self.switches["Testing"] == True and
				self.states["Wait for input"] == True and
				game_title != self.games["List"][-1]
			):
				# Show a ten dash space separator
				print()
				print(self.separators["10"])

				# Define the next text
				next_text = self.Language.language_texts["next, title()"] + " " + self.language_texts["game, title()"]

				# Format it
				next_text = " ({})".format(next_text.lower())

				# Ask the user to press Enter to advance to the next game
				self.Input.Type(self.Language.language_texts["continue, title()"] + next_text)

	def Update_Entry_Text(self, entry, contents, language):
		# Import the regex module
		import re

		# ---------- #

		# Define the text variable as the "String" key (the text string)
		text = contents["String"]

		# Define the lines variable as the "Lines" key (the text lines)
		lines = contents["Lines"]

		# Add None to the start of the list so the indexes start at one and not zero
		lines = [None] + lines

		# ---------- #

		# Define an "update file" switch as False
		update_file = False
		
		# Define the search text as the "Game type" text
		search_text = self.texts["game_type"][language]

		# If the seventh line is not "Game type:"
		if lines[7] != search_text + ":":
			# Make a backup of the search line and remove it
			search_result = re.search(rf"{search_text}:\n(.+)\n\n", text)
			text = re.sub(rf"{search_text}:\n(.+)\n\n", "", text)

			# Define the after line as "Gaming session number by game type" text
			after_line = self.texts["gaming_session_number_by_game_type"][language]

			# Re-add the line after the after line
			if search_result:
				game_type = "\n" + (search_result.group(0))[:-1]

				text = re.sub(
					rf"({after_line}:\n.*\n)",
					r"\1" + game_type,
					text
				)

			# Switch the "update file" switch to True
			update_file = True

		# ---------- #

		# Define the search text as the "Entry" text
		search_text = self.Language.texts["entry, title()"][language]

		# If the tenth line is not "Entry:"
		if lines[10] != search_text + ":":
			# Make a backup of the search line and remove it
			search_result = re.search(rf"{search_text}:\n(.*)", text)
			text = re.sub(rf"(?:\n\n)?{search_text}:\n(.*)", "", text)

			# Define the after line as "Game type" text
			after_line = self.texts["game_type"][language]

			# Re-add the line after the after line
			if search_result:
				game_type = "\n" + (search_result.group(0)) + "\n"

				text = re.sub(
					rf"({after_line}:\n.*\n)",
					r"\1" + game_type,
					text
				)

		# ---------- #

		# If the entry name is not inside the text string
		if entry["Entry"] not in text:
			# Replace the entry name
			text = re.sub(
				rf"({search_text}:\n)(.+\n)",
				r"\g<1>" + entry["Entry"] + "\n",
				text
			)

		# ---------- #

		# If the "update file" switch is True
		if update_file == True:
			# Get the game title and game titles texts
			game_title_text = self.texts["game_title"][language]
			game_titles_text = self.texts["game_titles"][language]

			# If the "Romanized" key is in the game titles dictionary
			if "Romanized" in entry["Game titles"]:
				# Get the original game title
				original_title = entry["Game titles"]["Original"]

				# If the original title is not already present
				if original_title not in text:
					# Replace the "Game title" text with the "Game titles" text
					text = text.replace(game_title_text + ":", game_titles_text + ":")

					# Insert the original title below the romainzed title
					text = re.sub(
						rf"({game_titles_text}:\n)(.+\n)",
						rf"\1{original_title}\n\2",
						text
					)

			# ---------- #

			# Iterate through the list of small languages
			for local_language in self.languages["small"]:
				# If the language is in the list of game titles
				if local_language in entry["Game titles"]:
					# Get the language title
					language_title = entry["Game titles"][local_language]

					# If the language title is not already present
					if language_title not in text:
						# Replace the "Game title" text with the "Game titles" text
						text = re.sub(rf"{game_title_text}:", f"{game_titles_text}:", text)

						# Insert the original title below the romainzed title
						text = re.sub(
							rf"({game_titles_text}:\n.+\n)",
							rf"\1{language_title}\n",
							text
						)

			# ---------- #

			# Search for the "Game titles" text
			match = re.search(rf"({game_titles_text}:\n)((?:.+\n)+?)\n", text)

			# If the text is found
			if match:
				header = match.group(1) # The text with a line break
				titles_block = match.group(2) # The block with the game titles
				titles = titles_block.strip().split("\n") # The list with the game titles

				# If there is only one title, change the header text to the singular form
				if len(titles) == 1:
					text = text.replace(game_titles_text + ":", game_title_text + ":")

			# ---------- #

			# Define the search text as the "Platform" text
			search_text = self.Language.texts["platform, title()"][language]

			# Make a backup of the search line and search for the current platform value
			search_result = re.search(rf"{search_text}:\n(.+)\n\n", text)

			# Check if the search was successful and if the current value is "PC"
			if (
				search_result and
				search_result.group(1) == "PC"
			):
				# Define the new platform value
				new_platform_value = self.Language.texts["computer, title()"][language]

				# Re-add the line with the new platform value
				platform_line = f"{search_text}:\n{new_platform_value}\n\n"
				text = re.sub(
					rf"({search_text}:\n{search_result.group(1)}\n\n)",
					platform_line,
					text
				)

			# ---------- #

			# Define the search text as the "When I finished playing" text
			search_text = self.texts["when_i_finished_playing"][language] + ":"

			# Search for the search text
			search_result = re.search(rf"({search_text})", text)

			# Check if the search found results
			if (
				search_result and
				self.texts["when_i_started_playing"][language] + ":" not in text
			):
				# Group the result
				result = search_result.group(0)

				# Define the new value
				new_value = self.texts["when_i_started_playing"][language] + ":" + "\n" + \
				entry["Times"]["Started playing"] + "\n\n" + \
				result

				# Re-add the line with the new value
				text = re.sub(
					result,
					new_value,
					text
				)

			# ---------- #

			# Define the search text as the "Session duration" text
			search_text = self.texts["session_duration"][language] + ":"

			# Search for the search text
			search_result = re.search(rf"({search_text})", text)

			# Check if the search found results
			if search_result:
				# Group the result
				result = search_result.group(0)

				# Define the new value
				new_value = self.Language.texts["gaming_session_duration"][language] + ":"

				# Re-add the line with the new value
				text = re.sub(
					result,
					new_value,
					text
				)

			# ---------- #

			# Define the search text as the "Gaming session description" text
			search_text = self.texts["gaming_session_description"][language] + ":"

			# Search for the search text
			result = re.search(rf"({search_text})\n(.*)\n(.*)", text)

			# Check if the search found results
			# And the full Portuguese language (Português) with a line break is inside the text
			if (
				result and
				self.languages["full"]["pt"] + ":\n" in text
			):
				# Define the new value
				new_value = self.texts["gaming_session_descriptions"][language] + ":" + "\n" + \
				"\n" + \
				self.languages["full"]["pt"] + ":" + "\n" + \
				result.group(2) + "\n" + \
				"\n" + \
				self.languages["full"]["en"] + ":" + "\n" + \
				result.group(3)

				# Re-add the line with the new value
				text = re.sub(
					rf"({search_text})\n(.*)\n(.*)",
					new_value,
					text
				)

		# ---------- #

		# Define the search text as the "When I started playing" text
		search_text = self.texts["when_i_started_playing"][language] + ":"

		# Search for the search text
		result = re.findall(rf"({search_text}\n.*?)\n\n", text)

		if len(result) == 3:
			result.pop(2)

		# Check if the search found results
		if (
			result and
			len(result) > 1
		):
			# Define the new value
			new_value = result[0]

			# Re-add the line with the new value
			text = re.sub(
				"\n\n".join(result),
				new_value,
				text,
				count = 1
			)

		# ---------- #

		# Remove the ": " at the start of lines if it exists
		text = re.sub(
			r"^: ",
			"",
			text,
			flags = re.MULTILINE
		)

		# ---------- #

		# Split the text into a list of lines
		lines = text.splitlines()

		# Define a list of lines to keep
		lines_to_keep = []

		# Iterate through each line
		for line in lines:
			# Define the "keep line" switch as False
			keep_line = False

			# Check if the line contains only numbers
			if line.strip().isdigit():
				keep_line = True # Keep lines that contain only numbers

			# Check if the line is not just numbers and not already in the list
			# Or the line is empty
			elif (
				line not in lines_to_keep or
				line == ""
			):
				keep_line = True # Keep lines that are not just numbers and not in the list

			# If the "keep line" switch is True
			if keep_line == True:
				lines_to_keep.append(line)

		# Transform the list of lines into a text string
		text = self.Text.From_List(lines_to_keep, next_line = True)

		# ---------- #

		# Return the text
		return text

	def Process_Entry(self, entry, english_game_type = None, entries = None, entry_list_file = None):
		# If the "Number" key is in the entry dictionary
		if "Number" in entry:
			# Change the "Number" key to "Gaming session number"
			old_key = "Number"
			new_key = "Gaming session number"
			entry = self.JSON.Add_Key_After_Key(entry, {new_key: entry[old_key]}, after_key = old_key, remove_after_key = True)

		# ---------- #

		# If the "Type number" key is in the entry dictionary
		if "Type number" in entry:
			# Change the "Type number" key to "Gaming session number by game type"
			old_key = "Type number"
			new_key = "Gaming session number by game type"
			entry = self.JSON.Add_Key_After_Key(entry, {new_key: entry[old_key]}, after_key = old_key, remove_after_key = True)

		# ---------- #

		# If the "Type" key is in the entry dictionary
		if "Type" in entry:
			# Add the "Game type" key after the "Gaming session number by game type" key, then remove the "Type" key
			after_key = "Gaming session number by game type"
			entry = self.JSON.Add_Key_After_Key(entry, {"Game type": entry["Type"]}, after_key = after_key)
			entry.pop("Type")

		# ---------- #

		# If the "Date" key is in the entry dictionary
		if "Date" in entry:
			# Make a backup of the entry time
			entry_time_backup = entry["Date"]

			# Get the "Date" key of the entry dictionary and transform it into a date dictionary
			date = self.Date.From_String(entry["Date"])

			# Create a "Times" dictionary based on the date dictionary
			times = {
				"Started playing": "", # The time when the user started playing the game

				"Finished playing": date["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"], # The "Finished playing" with the "HH:MM DD/MM/YYYY" format in the user timezone

				"Finished playing (UTC)": date["UTC"]["DateTime"]["Formats"]["YYYY-MM-DDTHH:MM:SSZ"], # The "Finished playing" in the ISO-8601 format and UTC time

				"Gaming session duration": {} # The gaming session duration dictionary
			}

			# Get the after time as the current time
			after_time = date

			# Define a subtract dictionary
			subtract = {}

			# Fill the subtract dictionary
			for key, value in entry["Session duration"].items():
				# If the key is not "Text"
				if key != "Text":
					subtract[key.lower()] = value

			# Define the relative delta
			relative_delta = self.Date.Relativedelta(**subtract)

			# Subtract the subtract time from the after time, creating the after time
			before_time = self.Date.Now(after_time["Object"] - relative_delta)

			# Update the "Started playing" time to be the before time
			times["Started playing"] = before_time["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"]

			# Get the time difference between the before and the after times
			difference = self.Date.Difference(before_time, after_time)

			# Update the difference dictionary
			difference = {
				**difference["Difference"], # Extract the keys and values of the "Difference" sub-dictionary
				"Text": difference["Text"]
			}

			# Update the root "Gaming session duration" dictionary
			times["Gaming session duration"] = difference

			# Add the "Times" key after the "Game type" key
			after_key = "Game type"
			entry = self.JSON.Add_Key_After_Key(entry, {"Times": times}, after_key = after_key)

			# Remove the "Date" key
			entry.pop("Date")

			# Remove the "Session duration" key
			entry.pop("Session duration")

		# ---------- #

		# If the "Titles" key is in the entry dictionary
		if "Titles" in entry:
			# Change the "Titles" key to "Game titles"
			old_key = "Titles"
			new_key = "Game titles"
			entry = self.JSON.Add_Key_After_Key(entry, {new_key: entry[old_key]}, after_key = old_key, remove_after_key = True)

		# ---------- #

		# If the "Sub-game" key exists in the entry dictionary
		if "Sub-game" in entry:
			# Change the "Sub-game" key to "Sub-game titles"
			old_key = "Sub-game"
			new_key = "Sub-game titles"
			entry = self.JSON.Add_Key_After_Key(entry, {new_key: entry[old_key]}, after_key = old_key, remove_after_key = True)

		# ---------- #

		# If the "Platform" value is "PC"
		if entry["Platform"] == "PC":
			# Change it to "Computer"
			entry["Platform"] = "Computer"

		# ---------- #

		# Define a dictionary of files to update
		files = {
			"Entry file": {},
			"Entry list": {},
			"JSON": {}
		}

		# ---------- #

		# If the English game type parameter is not None
		if english_game_type != None:
			# Define the local entry name dictionary
			entry_name = {
				"en": entry["Entry"]
			}

			# Get the game type dictionary
			game_type = self.game_types[english_game_type]

			# Get the language game type for the current language
			language_game_type = game_type["Type"][language]

			# Create the language entry name by changing the English game type with the language game type
			entry_name[self.user_language] = entry_name["en"].replace(english_game_type, language_game_type)

			# ---------- #

			# By game type

			# Get the by game type folder
			by_game_type_folder = year["Folders"]["By game type"][english_game_type]

			# Get the files folder
			files_folder = by_game_type_folder["Files"]["root"]

			# Get the entry list file by game type
			files["Entry list"]["By game type"] = by_game_type_folder["root"] + "Entry list.txt"

			# ---------- #

			# Iterate through the list of small languages
			for language in self.languages["small"]:
				# Define the key addon
				key_addon = " ({})".format(language)

				# Get the played game folder of the current year, language, and game type
				folder = year["Folders"][language]["Gaming sessions"][english_game_type]["root"]

				# Get the entry file
				files["Entry file"]["Gaming sessions"] = folder + entry_name[language] + ".txt"

				# If the entry is the first for the curremt game type
				if entry["Gaming session number by game type"] == 1:
					# Get the "Firsts of the Year" folder of the current year and language
					folder = year["Folders"][language]["Firsts of the Year"]["root"]

					# Get the entry file
					files["Entry file"]["Firsts of the Year"] = folder + entry_name[language] + ".txt"

			# ---------- #

			# Get the game information folder
			game_information_folder = self.game_types[english_game_type]["Folders"]["Game information"]

			# ---------- #

			# Define the title key as "Original"
			title_key = "Original"

			# If the "Romanized" key is in the "Game titles" dictionary
			if "Romanized" in entry["Game titles"]:
				# Define the alternative key as "Romanized"
				alternative_key = "Romanized"

				# Get the alternative folder
				alternative_folder = game_information_folder["root"] + self.Sanitize_Title(entry["Game titles"][alternative_key]) + "/"

				# If the alternative folder exists
				if self.Folder.Exist(alternative_folder) == True:
					# Change the title key to be the alternative key
					title_key = alternative_key

			# Get the game title
			game_title = self.Sanitize_Title(entry["Game titles"][title_key])

			# Get the game folder
			game_folder = game_information_folder["root"] + game_title + "/"

			# ---------- #

			# Define the sub-games folder as an empty string
			sub_games_folder = ""

			# If the DLCs folder exists
			dlcs_folder = game_folder + self.language_texts["dlcs, upper()"] + "/"

			if self.Folder.Exist(dlcs_folder) == True:
				# Define it as the sub-games folder
				sub_games_folder = dlcs_folder

			# If the "Sub-game titles" key is not in the entry dictionary
			# And the sub-games folder is not empty
			if (
				"Sub-game titles" not in entry and
				sub_games_folder != ""
			):
				# Update the game folder to add the root game title
				game_folder = sub_games_folder + game_title + "/"

			# ---------- #

			# If the "Sub-game titles" key is in the entry dictionary
			if "Sub-game titles" in entry:
				# Define the title key as "Original"
				title_key = "Original"

				# If the "Romanized" key is in the "Sub-game titles" dictionary
				if "Romanized" in entry["Sub-game titles"]:
					# Define the title key as "Romanized"
					title_key = "Romanized"

				# Get the sub-game title
				sub_game_title = self.Sanitize_Title(entry["Sub-game titles"][title_key])

				# Update the game folder to add the sub-game title
				game_folder = sub_games_folder + sub_game_title + "/"

			# ---------- #

			# Get the "Played" folder
			played_folder = game_folder + self.Language.language_texts["played, title()"] + "/"

			# Get the played files folder
			files_folder = played_folder + self.File.language_texts["files, title()"] + "/"

			# Get the played "Sessions.json" file
			played_entries_file = played_folder + "Entries.json"

			# If the played "Sessions.json" file is not empty
			if (
				self.File.Contents(played_entries_file)["lines"] != [] and
				self.JSON.To_Python(played_entries_file)["Entries"] != []
			):
				# Read it
				played_entries = self.JSON.To_Python(played_entries_file)

				# Update the entry dictionary
				played_entries["Dictionary"][entry["Entry"]] = entry

				# Add the played folder to the list of folders
				folders["Played"] = files_folder

			# ---------- #

			# Get the played "Entry list.txt" file
			played_entry_list_file = played_folder + "Entry list.txt"

		# ---------- #

		# Define the local entry title
		entry_title = entry["Entry"]

		# Make a backup of the entry name
		entry_name_backup = entry["Entry"]

		# ---------- #

		# Iterate through the folders in the folders dictionary
		for folder_name, folder in deepcopy(folders).items():
			# If the folder is empty
			if folder == "":
				# Remove the folder key
				folders.pop(folder_name)

		# ---------- #

		# Iterate through the folders in the folders dictionary
		for folder_name, folder in folders.items():
			# Define the language as the user language by default
			language = self.user_language

			# If the folder is "Game type files"
			if folder_name == "Game type files":
				# Change the language to the user language
				language = self.user_language

			# If the "Gaming sessions" or "Firsts of the Year" texts are in the folder name
			if (
				"Gaming sessions" in folder_name or
				"Firsts of the Year" in folder_name
			):
				# Get the folder name, remove the folder name and keep only the language
				language = folder_name.split(" (")[1].replace(")", "")

			# ---------- #

			# Get the sanitized entry name
			entry_name = entry_name_backup.replace(":", ";").replace("/", "-")

			# Get the entry file
			entry_file = folder + entry_name + ".txt"

			# Make a backup of the entry file
			entry_file_backup = entry_file

			# Define the default new entry name and file
			new_entry_name = entry["Entry"]
			new_entry_file = ""

			# ---------- #

			# Get the game type dictionary
			game_type = self.game_types[english_game_type]

			# Get the language game type for the current language
			language_game_type = game_type["Type"][language]

			# Create the language entry name by changing the English game type with the language game type
			language_entry_name = new_entry_name.replace(english_game_type, language_game_type)

			# Define the "renamed file" switch as False
			renamed_file = False

			# ---------- #

			# Define shortcuts for the old and new keys
			old_key = entry_name_backup
			new_key = new_entry_name

			# If the two keys are not the same
			# Or the local language is not English
			# And the folder is not "Game type files"
			if (
				old_key != new_key or
				language != "en" and
				folder_name != "Game type files"
			):
				# If the old key is in the entries dictionary
				if old_key in entries["Dictionary"]:
					# Make a backup of the entry dictionary
					entry_dictionary = deepcopy(entries["Dictionary"][old_key])

					# Change the key in the root dictionary
					entries["Dictionary"] = self.JSON.Add_Key_After_Key(entries["Dictionary"], {new_key: entry_dictionary}, after_key = old_key, remove_after_key = True)

					# ---------- #

					# If the played entries file is not an empty string
					if played_entries_file != "":
						# Read it
						played_entries = self.JSON.To_Python(played_entries_file)

						# Update the entry in the dictionary
						entry["Entry"] = new_entry_name

						# If the old key is in the dictionary
						if old_key in played_entries["Dictionary"]:
							# Change the key in the played dictionary
							played_entries["Dictionary"] = self.JSON.Add_Key_After_Key(played_entries["Dictionary"], {new_key: entry}, after_key = old_key, remove_after_key = True)

				# ---------- #

				# Iterate through the entries in the list of entries
				e = 0
				for local_entry in entries["Entries"]:
					# If the local entry is the current entry
					if local_entry == entry_name_backup:
						# Replace it with the new entry name
						entries["Entries"][e] = new_entry_name

				# ---------- #

				# If the game type entry list file is not an empty string
				if game_type_entry_list_file != "":
					# Read the file
					file_text = self.File.Contents(game_type_entry_list_file)["String"]

					# Replace the old entry name with the new one
					file_text = file_text.replace(entry_name_backup, new_entry_name)

					# If the "write to file" switch is True
					if self.write_to_file == True:
						# Update the text in the file
						self.File.Edit(game_type_entry_list_file, file_text, "w")

				# ---------- #

				# If the played entry list file is not an empty string
				if played_entry_list_file != "":
					# Read the file
					file_text = self.File.Contents(played_entry_list_file)["String"]

					# Replace the old entry name with the new one
					file_text = file_text.replace(entry_name_backup, new_entry_name)

					# If the "write to file" switch is True
					if self.write_to_file == True:
						# Update the text in the file
						self.File.Edit(played_entry_list_file, file_text, "w")

				# ---------- #

				# Update the entry in the dictionary
				entry["Entry"] = new_entry_name

				# Update the local entry title
				entry_title = new_entry_name

				# Sanitize the entry name
				sanitized_entry_name = language_entry_name.replace(":", ";").replace("/", "-")

				# Define a new (renamed) entry file
				new_entry_file = folder + sanitized_entry_name + ".txt"

				# If the first and second file are not the same file
				if entry_file != new_entry_file:
					# Rename the file
					self.File.Move(entry_file, new_entry_file)

					# Update the entry file variable
					entry_file = new_entry_file

					# Set the "renamed file" switch to True
					renamed_file = True

				# ---------- #

			# Get the contents of the file as a string
			text = self.File.Contents(entry_file)["String"]

			# Replace the file text to correct text order
			text = self.Replace_Text(entry, text, language)

			if "By game type" in entry_file:
				print(entry_file)
				print("[{}]".format(text))

			# Write the updated contents into the entry file
			self.File.Edit(entry_file, text, "w")

		# Return the entry dictionary, entry title, and entries dictionary
		return entry, entry_title, entries