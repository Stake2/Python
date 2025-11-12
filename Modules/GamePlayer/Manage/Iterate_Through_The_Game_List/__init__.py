# Iterate_Through_The_Game_List.py

# Import the root "GamePlayer" class
from GamePlayer.GamePlayer import GamePlayer as GamePlayer

# Import the "collections" module
import collections

class Iterate_Through_The_Game_List(GamePlayer):
	def __init__(self):
		super().__init__()

		# Create the states dictionary
		self.states = {
			"Write verbose": {
				"JSON": False,
				"Text": False
			}
		}

		# Iterate through the list of games
		self.Iterate()

	def Iterate(self):
		# Define a dictionary of local game types
		local_game_types = {
			"To skip": [ # Game types to skip
				#"Action",
				#"Action and Platform",
				#"Battle royale",
				#"Casual",
				#"Flash",
				#"FPS",
				#"Horror",
				#"Clicker Idle",
				#"Management",
				#"Multiplayer",
				#"Nintendo 64",
				#"Open world",
				#"Platform",
				#"Puzzle",
				#"Racing",
				#"Rhythm",
				#"RPG",
				#"Shoot 'em up",
				#"Simulation",
				#"Story",
				#"Strategy",
				#"Super Nintendo",
				#"Survival",
				#"Tower Defense",
				#"Visual Novel"
			],
			"To use": [] # Game types to use (exclusive mode)
		}

		# ---------- #

		# Define a list of game types to use
		game_types_list = self.game_types["Types"]["en"]

		# If the "To use" list is not empty
		if local_game_types["To use"] != []:
			# Update the list of game types to use
			game_types_list = local_game_types["To use"]

		# Iterate through the list of game types "To skip"
		for game_type in local_game_types["To skip"]:
			# If the game type is inside the list of game types
			if game_type in game_types_list:
				# Remove it
				game_types_list.remove(game_type)

		# ---------- #

		# Define a local game type number as one
		game_type_number = 1

		# Get the number of game types
		number_of_game_types = str(len(game_types_list))

		# Iterate through the English game types list
		for english_game_type in game_types_list:
			# Get the root game type dictionary
			root_game_type = self.game_types[english_game_type]

			# Get the language game type
			language_game_type = root_game_type["Type"][self.language["Small"]]

			# ----- #

			# Get a game list with games with all the playing statuses
			game_list = self.Get_Game_List(root_game_type, self.texts["statuses, type: list"]["en"])

			# Sort the game item list as case insensitive
			game_list = sorted(game_list, key = str.lower)

			# ----- #

			# Define the game type information text
			game_type_information = f"""
			{self.separators["10"]}

			{self.language_texts["number_of_the_game_type"]}:
			[{game_type_number}/{number_of_game_types}]

			{self.language_texts["game_type"]}:
			[{language_game_type}]""".replace("\t", "")

			# Show the game type information text
			print(game_type_information)

			# ----- #

			# Initialize the index of the current game, starting at one
			current_game_index = 1

			# Get the number of games
			number_of_games = str(len(game_list))

			# Iterate through the list of games
			for game_title in game_list:
				# Define the root dictionary with the game type and the game
				dictionary = {
					"Type": root_game_type,
					"Game": {
						"Title": game_title
					}
				}

				# Select the game and define its variables, returning the game dictionary (without asking the user to select the game)
				dictionary = self.Select_Game(dictionary)

				# Define a shortcut to the "Game" dictionary for easier typing
				game = dictionary["Game"]

				# ----- #

				# Replace the ten dash space separator from the game type information with a five dash space separator
				game_type_information = game_type_information.replace(self.separators["10"], self.separators["5"])

				# Show the game type information text
				print(game_type_information)

				# If the number of games is more than one
				if len(game_list) > 1:
					# Show the number of the game
					print()
					print(self.language_texts["number_of_the_game"] + ":")
					print("[" + str(current_game_index) + "/" + str(number_of_games) + "]")

				# ----- #

				# Define a shortcut to the game titles dictionary
				game_titles = game["Titles"]

				# Get the language game title
				language_game_title = self.Define_Title(game_titles)

				# Show the language game title
				print()
				print(self.language_texts["game_title"] + ":")
				print("[" + language_game_title + "]")

				# ----- #

				# If the game has sub-games
				#if game["States"]["Has sub-games"] == True:
					# Update the sub-games
					#self.Update_Sub_Games(dictionary)

				# Add the missing information about the game if the game year is not inside the game details file
				if self.Date.language_texts["year, title()"] not in game["Details"]:
					self.Add_Game_Information()

				# Check if the game shortcut exists
				#self.Check_If_Shortcut_Exists()

				# Move the gaming time files
				#self.Move_Gaming_Time_Files()

				# Fix sub-games inside entries dictionaries
				#self.Fix_Sub_Games()

				# ----- #

				# Increment the current game index by one
				current_game_index += 1

				# ----- #

				# If the "Testing" switch is True
				# And the game is not the last one
				# And the game list is not empty
				# And the number of games is more than one
				if (
					self.switches["Testing"] == True and
					game_title != game_list[-1] and
					game_list != [] and
					len(game_list) > 1
				):
					# Ask the user to press Enter to advance to the next game type
					self.Input.Type(self.Language.language_texts["continue, title()"] + " ({})".format(self.language_texts["game, title()"].lower()))

			# ----- #

			# Add one to the game type number
			game_type_number += 1

			# ----- #

			# If the "Testing" switch is True
			# And the game type is not the last one
			# And the game list is not empty
			# And the number of games is more than one
			if (
				self.switches["Testing"] == True and
				english_game_type != game_types_list[-1] and
				game_list != [] and
				len(game_list) > 1
			):
				# Show a ten dash space separator
				print()
				print(self.separators["10"])

				# Ask the user to press Enter to advance to the next game type
				self.Input.Type(self.Language.language_texts["continue, title()"] + " ({})".format(self.language_texts["game_type"].lower()))

	def Update_Sub_Games(self, dictionary):
		# Define a shortcut to the "Game" dictionary
		game = dictionary["Game"]

		# Initialize the index of the current sub-game, starting at one
		current_sub_game_index = 1

		# Get the number of sub-games
		number_of_sub_games = str(game["Sub-games"]["Items"]["Number"])

		# Define a dictionary of game entries
		game_entries = {
			"Numbers": {
				"Total": 0
			},
			"Entries": [],
			"Dictionary": {}
		}

		# Iterate through the sub-games
		for sub_game_title, sub_game in game["Sub-games"]["Items"]["Dictionary"].items():
			# Show a three dash space separator
			print()
			print(self.separators["3"])

			# ----- #

			# Show the number of the sub-game
			print()
			print(self.language_texts["number_of_the_sub_game"] + ":")
			print("[" + str(current_sub_game_index) + "/" + str(number_of_sub_games) + "]")

			# ----- #

			# Define the sub-game dictionary
			dictionary = self.Define_Sub_Games(dictionary, sub_game_title = sub_game_title)

			# Define a shortcut to the sub-game dictionary
			sub_game = game["Sub-game"]

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
			sub_game_entries_file = sub_game["Folders"]["Played"]["entries"]

			# ----- #

			# Read the entries file
			sub_game_entries = self.JSON.To_Python(sub_game_entries_file)

			# Add the number of entries to the game entries dictionary
			game_entries["Numbers"]["Total"] += sub_game_entries["Numbers"]["Total"]

			# Extend the list of entries of the game dictionary with the one on the sub-game dictionary
			game_entries["Entries"].extend(sub_game_entries["Entries"])

			# Update the dictionary of entries of the game dictionary with the one on the sub-game dictionary
			game_entries["Dictionary"].update(sub_game_entries["Dictionary"])

			# ----- #

			# Increment the current sub-game index by one
			current_sub_game_index += 1

		# ---------- #

		# Define a dictionary of entries by year
		entries_by_year = {}

		# Get the list of entry names
		entry_names = list(game_entries["Entries"])

		# Iterate through the entry names
		for entry_name in entry_names:
			# Get the date from the entry name
			date = entry_name.split("(")[1].strip(")")

			# Convert the date to a date dictionary
			date = self.Date.From_String(date)

			# Get the year from the date
			year = date["Units"]["Year"]

			# If the year is not present in the "entries by year" dictionary, add it
			if year not in entries_by_year:
				entries_by_year[year] = []

			# Add the entry name to the year dictionary
			entries_by_year[year].append(entry_name)

		# Sort the keys of the dictionary of year entries based on its keys
		entries_by_year = dict(collections.OrderedDict(sorted(entries_by_year.items())))

		# ----- #

		# Create an empty local list of entries
		entries_list = []

		# Iterate through the dictionary of years, getting the year and the list of entries for that year
		for year, year_entries in entries_by_year.items():
			# Sort the list of year entries
			year_entries = sorted(year_entries, key = self.Extract_Number)

			# Extend the local entries list with the current list of entries
			entries_list.extend(year_entries)

		# Update the list of entries of the game to be the local one
		game_entries["Entries"] = entries_list

		# ---------- #

		# Get the game played "Entries.json" file
		game_entries_file = game["Folders"]["Played"]["entries"]

		# Get the original entries
		original_game_entries = self.JSON.To_Python(game_entries_file)

		# Update the game played "Entries.json" file with the updated "Entries" dictionary
		# (Game played "Entries.json" file)
		self.JSON.Edit(game_entries_file, game_entries)

	def Extract_Number(self, entry_name):
		# Extracts the number from the entry name
		return int(entry_name.split(".")[0].strip())

	def Add_Game_Information(self):
		# If the current class (Iterate_Through_The_Game_List) does not contain the "Add_A_New_Game" attribute
		if hasattr(self, "Add_A_New_Game") == False:
			# Define it
			from GamePlayer.Manage.Add_A_New_Game import Add_A_New_Game as Add_A_New_Game

			self.Add_A_New_Game = Add_A_New_Game

		# Define the "Update" key as True
		self.dictionary["Update"] = True

		# Define the "DuckDuckGo" dictionary
		self.duckduckgo = {
			"Format": "https://duckduckgo.com/?t=ffab&q={}"
		}

		# Define the game search link
		link = self.duckduckgo["Format"].format(game["Title"])

		# Open the game search link
		self.System.Open(link)

		# Run the "Add_A_New_Game" sub-class with the game dictionary
		self.Add_A_New_Game(self.dictionary)

	def Check_If_Shortcut_Exists(self):
		# If the game is not a remote game
		if game["States"]["Remote game"] == False:
			# Define the "file" variable for easier typing
			file = game["Files"]["Shortcut"]["File"]

			# If the file does not exist
			if self.File.Exists(file) == False:
				# Show the text telling the user that the file does not exist
				# Along with the file path
				print()
				print(self.Language.language_texts["this_file_does_not_exists"] + ":")
				print("\t" + file)

				# Copy the game title for the user to rename the game shortcut
				self.Text.Copy(game["Title"])

				# Open the game folder for the user to create the game shortcut and rename it with the game title
				self.System.Open(game["Folders"]["Local"]["root"])

				# Tell the user to press Enter when it finishes doing that
				input()

				# Open the game type shortcuts folder for the user to paste the shortcut into it
				self.System.Open(self.dictionary["Type"]["Folders"]["Shortcuts"]["root"])

				# Tell the user to press Enter when it finishes doing that
				input()

	def Move_Gaming_Time_Files(self):
		# Define some folder variables for easier typing
		played_folder = game["Folders"]["Played"]["root"]
		gaming_time_folder = game["Folders"]["Gaming time"]["root"]

		# Define the old time JSON file
		time_file = played_folder + "Time.json"

		# Define the new gaming time JSON file
		gaming_time_file = game["Folders"]["Gaming time"]["Gaming time"]

		if self.File.Exists(time_file) == True:
			# Move the file
			self.File.Move(time_file, gaming_time_file)

			file = gaming_time_file

			if self.File.Exists(time_file) == True:
				file = time_file

			self.dictionary["Game"]["Gaming time"] = self.JSON.To_Python(file)

		# --------------- #

		# Define the old language gaming time file
		language_gaming_time_file = played_folder + self.language_texts["gaming_time"] + ".txt"

		# Define the new language gaming time file
		new_language_gaming_time_file = game["Folders"]["Gaming time"]["Language gaming time"]

		if self.File.Exists(language_gaming_time_file) == True:
			# Move the file
			self.File.Move(language_gaming_time_file, new_language_gaming_time_file)

		# Re-select the game to update the gaming time dictionary
		self.dictionary = self.Select_Game(self.dictionary)

		# Define the "game" variable for easier typing
		game = self.dictionary["Game"]

	def Fix_Sub_Games(self):
		# Only for the "Don't Starve" game, which has been registered with sub-game types (DLCs, the "Hamlet" DLC)
		if (
			game["Title"] == "Don't Starve"
		):
			# Define the "Hamlet" sub-game
			self.dictionary = self.Define_Sub_Games(self.dictionary, sub_game_title = "Hamlet")

			# Define the "game" variable for easier typing
			game = self.dictionary["Game"]

			# Define the "sub-game" variable for easier typing
			sub_game = game["Sub-game"]

			# Get the sub-game played entries
			entries = list(sub_game["Played"]["Dictionary"].keys())

			years = {}

			# Iterate through the played entries dictionary
			for entry in entries:
				# Get the Entry dictionary
				entry = sub_game["Played"]["Dictionary"][entry]

				# Change the title
				entry["Titles"]["Original"] = "Don't Starve"

				# Add the "Sub-game" key
				key_value = {
					"Sub-game": {
						"Original": sub_game["Title"]
					}
				}

				entry = self.JSON.Add_Key_After_Key(entry, key_value, after_key = "Titles")

				# Update the entry inside the entries dictionary
				sub_game["Played"]["Dictionary"][entry["Entry"]] = entry

				# Get the year of the entry
				year = entry["Date"].split("-")[0]

				# If the year is not inside the "Years" dictoinary
				if year not in years:
					# Define the Year dictionary
					year = {
						"Number": year,
						"Folder": self.folders["Play History"][year]["root"],
						"File": "",
						"Entries": {},
						"Type": {
							"Folder": "",
							"File": "",
							"Entries": {}
						}
					}

					# Define the Entries file
					year["File"] = year["Folder"] + "Sessions.json"

					# Get the year Entries
					year["Entries"] = self.JSON.To_Python(year["File"])

					# Define the game type folder
					year["Type"]["Folder"] = year["Folder"] + "Per Game Type/" + self.dictionary["Type"]["Type"]["en"] + "/"

					# Define the Entries file
					year["Type"]["File"] = year["Type"]["Folder"] + "Sessions.json"

					# Get the year game type Entries
					year["Type"]["Entries"] = self.JSON.To_Python(year["Type"]["File"])

					# Add the Year dictionary to the "Years" dictionary
					years[year["Number"]] = year

				else:
					# Get the Year dictionary
					year = years[year]

				# Update the year entry
				years[year["Number"]]["Entries"]["Dictionary"][entry["Entry"]] = entry

				# Update the year game entry
				years[year["Number"]]["Type"]["Entries"]["Dictionary"][entry["Entry"]] = entry

			# Iterate through the Year dictionaries
			for year in years.values():
				# Update the year "Sessions.json" file
				self.JSON.Edit(year["File"], year["Entries"])

				# Update the year game type "Sessions.json" file
				self.JSON.Edit(year["Type"]["File"], year["Type"]["Entries"])

			# Update the sub-game "Sessions.json" file
			self.JSON.Edit(sub_game["Folders"]["Played"]["entries"], sub_game["Played"])

			# -------------------- #

			# Get the sub-game played entries
			entries = list(sub_game["Played"]["Dictionary"].keys())