# Iterate_Through_The_Game_List.py

from GamePlayer.GamePlayer import GamePlayer as GamePlayer

class Iterate_Through_The_Game_List(GamePlayer):
	def __init__(self):
		super().__init__()

		# Create the "Years" dictionary
		self.Create_Years_Dictionary()

		# Iterate through the game list
		self.Iterate()

	def Iterate(self):
		# Iterate through English game types list
		i = 0
		for game_type in self.game_types["Types"]["en"]:
			# Define the key of the game type for getting game type folders
			key = game_type.lower().replace(" ", "_")

			# Define the language game type
			language_game_type = self.game_types["Types"][self.user_language][i]

			# Get game with all "watching statuses", not just the "Watching" and "Re-watching" ones
			game_list = self.Get_Game_List(self.game_types[game_type], self.texts["statuses, type: list"]["en"])

			# Sort the game item list as case insensitive
			game_list = sorted(game_list, key = str.lower)

			# Show language game type
			print()
			print("----------")
			print()
			print(language_game_type + ":")

			# Define the list of game types to remove
			# (None needed until now)
			game_types_to_skip = []

			# Define the list of game types to use
			game_types_to_use = [
				"Survival"
			]

			# Remove a game type from the list (optional)
			if (
				game_type not in game_types_to_skip and
				game_type in game_types_to_use or
				game_type not in game_types_to_skip and
				game_types_to_use == []
			):
				# Define the current game number and game list length number
				g = 1
				length = len(game_list)

				# Iterate through the games list
				for self.game_title in game_list:
					# Define the root dictionary with the game type and the game
					self.dictionary = {
						"Type": self.game_types[game_type],
						"Game": {
							"Title": self.game_title
						}
					}

					# Select the game and define its variables, returning the game dictionary (without asking user to select the game)
					self.dictionary = self.Select_Game(self.dictionary)

					# Define the "game" variable for easier typing
					self.game = self.dictionary["Game"]

					# If the current game number is not one
					# Show a separator to separate the information of the previous game from the next
					if g != 1:
						print()
						print(self.large_bar)

					# If the length of the game list is not one (more than one game)
					if length != 1:
						# Show the current game number and the number of games inside the game list
						print()
						print(self.JSON.Language.language_texts["number, title()"] + ":")
						print("\t" + "[" + str(g) + "/" + str(length) + "]")
						print()
						print("---")

						# Ask the "Show_Information" method to now show its first separator
						self.dictionary["First separator"] = False

					# Show information about the game
					self.Show_Information(self.dictionary)

					# Add the missing information about the game if the game year is not inside the game details file
					if self.Date.language_texts["year, title()"] not in self.game["Details"]:
						self.Add_Game_Information()

					# Check if the game shortcut exists
					#self.Check_If_Shortcut_Exists()

					# Move the gaming time files
					#self.Move_Gaming_Time_Files()

					# Fix sub-games inside entries dictionaries
					#self.Fix_Sub_Games()

					# Add to the current game number
					g += 1

					# If the "testing" switch is True
					# And the game is not the last one
					# And the game list is not empty
					# And the length of the game list is not one (more than one game)
					if (
						self.switches["testing"] == True and
						self.game_title != game_list[-1] and
						game_list != [] and
						length != 1
					):
						# Ask the user to press Enter to advance to the next game type
						self.Input.Type(self.JSON.Language.language_texts["continue, title()"])

			# If the "testing" switch is True
			# And the game type is not the last one
			# And the game type is not inside the list of game types that needs to be skipped
			# And the game list is not empty
			if (
				self.switches["testing"] == True and
				game_type != self.game_types["Types"]["en"][-1] and
				game_type not in game_types_to_skip and
				game_list != [] and
				game_types_to_use == []
			):
				# Ask the user to press Enter to advance to the next game type
				self.Input.Type(self.JSON.Language.language_texts["continue, title()"])

			# Add to the current game type number
			i += 1

	def Create_Years_Dictionary(self):
		# Define the "Years" dictionary with the list of years from 2021 to the current year
		self.years = {
			"List": self.Date.Create_Years_List(start = 2021, function = str),
			"Dictionary": {}
		}

		# Iterate through the years list
		# Of the years that contain a "Play History" folder, from 2021 to the current year
		for year in self.years["List"]:
			# Define the Year dictionary with the year number and folders
			self.year = {
				"Number": year,
				"Folders": {
					"root": self.folders["Play History"]["root"] + year + "/"
				}
			}

			# Define the "Sessions.json" file
			self.year["Folders"]["Entries"] = self.year["Folders"]["root"] + "Sessions.json"

			# Read the "Sessions.json" file
			self.year["Entries"] = self.JSON.To_Python(self.year["Folders"]["Entries"])

			# Add the Year dictionary into the "Years" dictionary
			self.years[year] = self.year

		# Return the "Years" dictionary
		return self.years

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
		link = self.duckduckgo["Format"].format(self.game["Title"])

		# Open the game search link
		self.System.Open(link)

		# Run the "Add_A_New_Game" sub-class with the game dictionary
		self.Add_A_New_Game(self.dictionary)

	def Check_If_Shortcut_Exists(self):
		# If the game is not a remote game
		if self.game["States"]["Remote game"] == False:
			# Define the "file" variable for easier typing
			file = self.game["Files"]["Shortcut"]["File"]

			# If the file does not exist
			if self.File.Exist(file) == False:
				# Show the text telling the user that the file does not exist
				# Along with the file path
				print()
				print(self.File.language_texts["this_file_does_not_exists"] + ":")
				print("\t" + file)

				# Copy the game title for the user to rename the game shortcut
				self.Text.Copy(self.game["Title"])

				# Open the game folder for the user to create the game shortcut and rename it with the game title
				self.System.Open(self.game["Folders"]["Local"]["root"])

				# Tell the user to press Enter when it finishes doing that
				input()

				# Open the game type shortcuts folder for the user to paste the shortcut into it
				self.System.Open(self.dictionary["Type"]["Folders"]["Shortcuts"]["root"])

				# Tell the user to press Enter when it finishes doing that
				input()

	def Move_Gaming_Time_Files(self):
		# Define some folder variables for easier typing
		played_folder = self.game["Folders"]["Played"]["root"]
		gaming_time_folder = self.game["Folders"]["Gaming time"]["root"]

		# Define the old time JSON file
		time_file = played_folder + "Time.json"

		# Define the new gaming time JSON file
		gaming_time_file = self.game["Folders"]["Gaming time"]["Gaming time"]

		if self.File.Exist(time_file) == True:
			# Move the file
			self.File.Move(time_file, gaming_time_file)

			file = gaming_time_file

			if self.File.Exist(time_file) == True:
				file = time_file

			self.dictionary["Game"]["Gaming time"] = self.JSON.To_Python(file)

		# --------------- #

		# Define the old language gaming time file
		language_gaming_time_file = played_folder + self.language_texts["gaming_time"] + ".txt"

		# Define the new language gaming time file
		new_language_gaming_time_file = self.game["Folders"]["Gaming time"]["Language gaming time"]

		if self.File.Exist(language_gaming_time_file) == True:
			# Move the file
			self.File.Move(language_gaming_time_file, new_language_gaming_time_file)

		# Re-select the game to update the gaming time dictionary
		self.dictionary = self.Select_Game(self.dictionary)

		# Define the "game" variable for easier typing
		self.game = self.dictionary["Game"]

	def Fix_Sub_Games(self):
		# Only for the "Don't Starve" game, which has been registered with sub-game types (DLCs, the "Hamlet" DLC)
		if (
			self.game["Title"] == "Don't Starve"
		):
			# Define the "Hamlet" sub-game
			self.dictionary = self.Define_Sub_Games(self.dictionary, sub_game_title = "Hamlet")

			# Define the "game" variable for easier typing
			self.game = self.dictionary["Game"]

			# Define the "sub-game" variable for easier typing
			sub_game = self.game["Sub-game"]

			# Get the sub-game played entries
			entries = list(sub_game["Played"]["Dictionary"].keys())

			years = {}

			# Iterate through the played Entries dictionary
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

				# Update the entry inside the Entries dictionary
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