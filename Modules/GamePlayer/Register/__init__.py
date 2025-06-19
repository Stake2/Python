# Register.py

from GamePlayer.GamePlayer import GamePlayer as GamePlayer

from copy import deepcopy

class Register(GamePlayer):
	def __init__(self, dictionary = {}):
		super().__init__()

		# Define the class dictionary as the parameter dictionary
		self.dictionary = dictionary

		# If the class dictionary is empty
		if self.dictionary == {}:
			# Ask for the entry information
			self.Type_Entry_Information()

		# Update the "Entry" dictionary with additional structured data:
		# "Diary Slim": initializes empty fields for Diary Slim related text entries
		# "States": sets the initial state for social network posting as False
		self.dictionary["Entry"].update({
			"Diary Slim": {
				"Text": "",
				"Descriptions": {},
				"Write description": False
			},
			"States": {
				"Post on the Social Networks": False
			}
		})

		# Define the media variable to make typing the media dictionary easier
		self.game = self.dictionary["Game"]

		# Check the game status
		self.Check_Game_Status()

		# If the user is not replaying the game
		# And they completed the game
		if (
			self.game["States"]["Re-playing"] == False and
			self.game["States"]["Completed game"] == True
		):
			# Check the game dates
			self.Check_Game_Dates()

		# Ask the user if it wants to write a description for the gaming session
		self.Ask_For_Gaming_Session_Description()

		# Define the "test things" switch as [the value I am using if I am testing the class]
		test_stuff = False

		# If the switch is False
		if test_stuff == False:
			# Save the entry to the database in the JSON format
			self.Register_In_JSON()

			# Create the individual entry file for the played game
			self.Create_Entry_File()

			# Create the entry files inside their corresponding year folders
			self.Add_Entry_File_To_Year_Folder()

			# Diary Slim related methods
			self.Define_Diary_Slim_Text()

			# Post the gaming session on the social networks
			self.Post_On_Social_Networks()

			# Write the information about the session on Diary Slim
			self.Write_On_Diary_Slim()

		# Update the statistic about the gaming session played
		self.Update_Statistic()

		# Show the information about the gaming session
		self.Show_Information(self.dictionary)

		# Re-initiate the root class to update the files
		del self.folders

		super().__init__()

	def Type_Entry_Information(self):
		# Select the game type and the game if the dictionary is empty
		if self.dictionary == {}:
			# Ask the user to select a game type and game
			self.dictionary = self.Select_Game_Type_And_Game()

		self.game = self.dictionary["Game"]

		# Import the "Play" class and set it as an attribute of this class
		if hasattr(self, "Play") == False:
			from GamePlayer.Play import Play as Play

			self.Play = Play

		# Define the "Register" class inside the "Play" class as None so it does not get run
		setattr(self.Play, "Register", None)

		# Define the "dictionary" of the "Play" class as the local dictionary inside this "Register" class
		setattr(self.Play, "dictionary", self.dictionary)

		# Run the Play class to define the session variables
		self.Play()

		# Get the dictionary from the "Play" class with the session and time related keys
		self.dictionary = self.Play.dictionary

	def Ask_For_Gaming_Session_Description(self):
		# Ask the user if it wants to write a description for the gaming session
		print()
		print(self.separators["5"])

		# If the "Testing" switch is False
		if self.switches["Testing"] == False:
			self.dictionary["Entry"]["Diary Slim"]["Write description"] = self.Input.Yes_Or_No(self.language_texts["write_a_description_for_the_gaming_session"])

		# Else, define it as True
		else:
			self.dictionary["Entry"]["Diary Slim"]["Write description"] = True

		# If the user wants to write a description
		if self.dictionary["Entry"]["Diary Slim"]["Write description"] == True:
			# Define the keyword parameters dictionary
			parameters = {
				"line_options_parameter": {
					"print": True,
					"next_line": False,
					"show_finish_text": True
				}
			}

			# Iterate through the list of small languages
			for language in self.languages["small"]:
				# If the language is not the first one
				if language != self.languages["small"][0]:
					# Enumerate the lines
					parameters["line_options_parameter"]["enumerate"] = True
					parameters["line_options_parameter"]["enumerate_text"] = False

					# Get the last description
					last_description = list(self.dictionary["Entry"]["Diary Slim"]["Descriptions"].values())[0]

					# Define the number of needed lines as the number of lines of the previous description
					parameters["length"] = last_description["length"]

				# Get the translated language in the user language
				translated_language = self.languages["full_translated"][language][self.user_language]

				# Define the type text
				type_text = self.Language.language_texts["description_in_{}"] + ":"

				# Format it
				type_text = type_text.format(translated_language)

				# If the "Testing" switch is False
				if self.switches["Testing"] == False:
					# Ask the user to type a session description
					self.dictionary["Entry"]["Diary Slim"]["Descriptions"][language] = self.Input.Lines(type_text, **parameters)

				# Else, define a default session description
				else:
					# Define the description text
					description = "[" + self.Language.texts["description, title()"][language] + "]"

					# Show it
					print()
					print(type_text)
					print(description)

					# Define it inside the "Descriptions" dictionary
					self.dictionary["Entry"]["Diary Slim"]["Descriptions"][language] = {
						"lines": [
							description
						],
						"string": description,
						"length": 1
					}

	def Register_In_JSON(self):
		# Define a shortcut for the plural form of the game type in English and make a sanitized version
		self.game_type = self.dictionary["Type"]["Type"]["en"]
		self.sanitized_game_type = self.game_type.lower().replace(" ", "_")

		# ---------- #

		# Re-read the main JSON files to retrieve the most up-to-date data
		self.dictionaries["Sessions"] = self.JSON.To_Python(self.folders["Play History"]["Current year"]["Sessions"])
		self.dictionaries["Game type"][self.game_type] = self.JSON.To_Python(self.folders["Play History"]["Current year"]["By game type"][self.sanitized_game_type]["Sessions"])
		self.dictionaries["Played"] = self.JSON.To_Python(self.game["Folders"]["Played"]["entries"])

		# If the game has sub-games
		if self.game["States"]["Has sub-games"] == True:
			# Get the "Sub-game played" dictionary
			self.dictionaries["Sub-game played"] = self.JSON.To_Python(self.game["Sub-game"]["Folders"]["Played"]["entries"])

		# Re-read the game "Played" JSON file to retrieve the most up-to-date data
		self.game["Played"] = self.JSON.To_Python(self.game["Folders"]["Played"]["entries"])

		# ---------- #

		# Define the "First gaming session in the year" state as False by default
		self.game["States"]["First gaming session in the year"] = False

		# If the total number of entries is zero, the gaming session is the first one in the year
		if self.dictionaries["Sessions"]["Numbers"]["Total"] == 0:
			self.game["States"]["First gaming session in the year"] = True

		# Define the "First gaming session by game type in the year" state as False by default
		self.game["States"]["First gaming session by game type in the year"] = False

		# If the total number of game type entries is zero, the gaming session by game type is the first one in the year
		if self.dictionaries["Game type"][self.game_type]["Numbers"]["Total"] == 0:
			self.game["States"]["First gaming session by game type in the year"] = True

		# ---------- #

		# Create a local list of dictionaries to update
		dictionaries_to_update = [
			self.dictionaries["Sessions"],
			self.dictionaries["Game type"][self.game_type],
			self.dictionaries["Played"]
		]

		# If the game has sub-games
		if self.game["States"]["Has sub-games"] == True:
			# Add the "Sub-game played" dictionary
			dictionaries_to_update.append(self.dictionaries["Sub-game played"])

		# Increment the total count for entries, game type entries, game played, and sub-game played entries
		for current_dict in dictionaries_to_update:
			current_dict["Numbers"]["Total"] += 1

			# If the "By game type" key exists, increment the count for the specific game type
			if "By game type" in current_dict["Numbers"]:
				current_dict["Numbers"]["By game type"][self.game_type] += 1

		# ---------- #

		# Define shortcuts for the total entries number and the entry times 
		entries_number = self.dictionaries["Sessions"]["Numbers"]["Total"]
		entry_time = self.dictionary["Entry"]["Times"]["Finished playing"]["Formats"]["HH:MM DD/MM/YYYY"]

		# Define the entry "Name" dictionary
		self.dictionary["Entry"]["Name"] = {}

		# Define the template for the entry name
		template = "{}. {} ({})"

		# Iterate through the list of small languages
		for language in self.languages["small"]:
			# Get the language game type
			language_game_type = self.dictionary["Type"]["Type"][language]

			# Define the list of items to use to format the template
			items = [
				entries_number,
				language_game_type,
				entry_time
			]

			# Format the template with the list of items, making the entry name
			entry_name = template.format(*items)

			# Create the language entry name dictionary
			dictionary = {
				"Normal": entry_name,
				"Sanitized": entry_name.replace(":", ";").replace("/", "-")
			}

			# Add the dictionary to the "Languages" dictionary
			self.dictionary["Entry"]["Name"][language] = dictionary

		# Add the entry name to the "Entries" lists in each dictionary
		for current_dict in dictionaries_to_update:
			if self.dictionary["Entry"]["Name"]["en"]["Normal"] not in current_dict["Entries"]:
				current_dict["Entries"].append(self.dictionary["Entry"]["Name"]["en"]["Normal"])

		# ---------- #

		# Update the total number of entries in all dictionaries based on the length of the "Entries" list
		for current_dict in dictionaries_to_update:
			current_dict["Numbers"]["Total"] = len(current_dict["Entries"])

		# ---------- #

		# Define the local game and sub-game titles to remove some keys from them
		game_titles = self.game["Titles"].copy()

		# Define the list of titles to remove some keys
		titles = [
			game_titles
		]

		sub_game_titles = []

		if "Sub-game" in self.game:
			sub_game_titles = self.game["Sub-game"]["Titles"].copy()

			titles.append(sub_game_titles)

		# ---------- #

		# Remove specified keys from each title dictionary
		for current_dict in titles:
			# Remove the "Language" and "Language sanitized" keys
			current_dict.pop("Language")
			current_dict.pop("Language sanitized")

			# Remove specific language keys
			for key in ["ja", "Sanitized"]:
				current_dict.pop(key, None) # Use None to avoid KeyError if the key does not exist

			# Remove language keys that match the original or romanized titles
			for language in self.languages["small"]:
				if language in current_dict:
					if (
						current_dict["Original"] == current_dict[language] or
						("Romanized" in current_dict and current_dict["Romanized"] == current_dict[language])
					):
						current_dict.pop(language, None) # Use None to avoid KeyError if the key does not exist

		# ---------- #

		# Get the normal entry name from the dictionary
		self.entry_name = self.dictionary["Entry"]["Name"]["en"]["Normal"]

		# Add the "Entry" dictionary to the "Dictionary" dictionary
		self.dictionaries["Sessions"]["Dictionary"][self.entry_name] = {
			"Gaming session number": self.dictionaries["Sessions"]["Numbers"]["Total"], # The number of the gaming session, by year
			"Gaming session number by game type": self.dictionaries["Game type"][self.game_type]["Numbers"]["Total"], # The number of the gaming session by game type and by year
			"Game type": self.game_type, # The game type
			"Times": deepcopy(self.dictionary["Entry"]["Times"]), # The dictionary of the played times, including the started and finished playing time and the duration between those two
			"Entry": self.dictionary["Entry"]["Name"]["en"]["Normal"], # The English name of the entry
			"Game titles": game_titles, # The dictionary of the game titles
			"Sub-game titles": sub_game_titles, # The dictionary of the sub-game titles
			"Platform": self.game["Platform"]["en"], # The platform where the game was played
		}

		# Define a shortcut for the entry dictionary
		self.entry_dictionary = self.dictionaries["Sessions"]["Dictionary"][self.entry_name]

		# Remove the media "Sub-game titles" key from the dictionary if:
		# 1. The game does not contain sub-games
		# 2. The game contains sub-games and the sub-game is the root game
		if (
			self.game["States"]["Has sub-games"] == False or
			self.game["States"]["Has sub-games"] == True and
			self.game["Sub-game"]["Title"] == self.game["Title"]
		):
			self.dictionaries["Sessions"]["Dictionary"][self.entry_name].pop("Sub-game titles")

		# ---------- #

		# Define a list of time keys
		time_keys = [
			"Started playing",
			"Finished playing",
			"Finished playing (UTC)"
		]

		# Iterate through the list of time types
		for time_key in time_keys:
			# Define the timezone key as "Timezone"
			timezone_key = "Timezone"

			# Define the format as the timezone one
			format = "HH:MM DD/MM/YYYY"

			# If the "UTC" text is inside the time key
			if "UTC" in time_key:
				# Update the timezone key to be the UTC one
				timezone_key = "UTC"

				# Define the format as the UTC one
				format = "YYYY-MM-DDTHH:MM:SSZ"

			# Get the time for the current time type, timezone, and format
			time = self.entry_dictionary["Times"][time_key][timezone_key]["DateTime"]["Formats"][format]

			# Update the entry dictionary with the obtained time
			self.entry_dictionary["Times"][time_key] = time

		# Define a shortcut to the "Gaming session duration" dictionary
		dictionary = self.entry_dictionary["Times"]["Gaming session duration"]

		# Update the dictionary
		self.entry_dictionary["Times"]["Gaming session duration"] = {
			**dictionary["Difference"], # Extract the keys and values of the "Difference" dictionary
			"Text": dictionary["Text"]
		}

		# ---------- #

		# Get the "States" dictionary with its states and state texts using the "Define_States_Dictionary" root method
		self.dictionary["States"] = self.Define_States_Dictionary(self.dictionary)

		# Add the "States" dictionary to the entry dictionary if it is not empty
		if self.dictionary["States"]["States"] != {}: # Check if the "States" dictionary is not empty
			self.dictionaries["Sessions"]["Dictionary"][self.entry_name]["States"] = self.dictionary["States"]["States"]

		# Add the entry dictionary to the game type and played entry dictionaries
		for current_dict in dictionaries_to_update:
			if current_dict != self.dictionaries["Sessions"]: # Ensure we do not update the "Entries" dictionary itself
				current_dict["Dictionary"][self.entry_name] = self.dictionaries["Sessions"]["Dictionary"][self.entry_name].copy()

		# ---------- #

		# Update the root current year"Entries.json" file
		self.JSON.Edit(self.folders["Play History"]["Current year"]["Sessions"], self.dictionaries["Sessions"])

		# Update the type current year "Entries.json" file
		self.JSON.Edit(self.dictionary["Type"]["Folders"]["By game type"]["Sessions"], self.dictionaries["Game type"][self.game_type])

		# Update the game "Played.json" file
		self.JSON.Edit(self.game["Folders"]["Played"]["entries"], self.dictionaries["Played"])

		if self.game["States"]["Has sub-games"] == True:
			# Update the sub-game "Played.json" file
			self.JSON.Edit(self.game["Sub-game"]["Folders"]["Played"]["entries"], self.dictionaries["Sub-game played"])

		# ---------- #

		# Make a list of "Entry list.txt" files to add to
		files = [
			self.folders["Play History"]["Current year"]["Entry list"],
			self.dictionary["Type"]["Folders"]["By game type"]["Entry list"],
			self.game["Folders"]["Played"]["entry_list"]
		]

		# If the game has sub-games
		if self.game["States"]["Has sub-games"] == True:
			# Add the played "Entry list.txt" file of the sub-game
			files.append(self.game["Sub-game"]["Folders"]["Played"]["entry_list"])

		# Iterate through those files
		for file in files:
			# Get the lines of the file
			lines = self.File.Contents(file)["Lines"]

			# If the entry name is not inside the text file, add it
			if self.entry_name not in lines:
				self.File.Edit(file, self.entry_name, "a")

	def Create_Entry_File(self):
		# This is a template for organizing the gaming session information in a text file
		# Each section contains placeholders that should be replaced with actual data
		# The structure includes details about the game, game type, playing times and states
		# Optional values are indicated in parentheses

		# Gaming session number:
		# [Gaming session number]
		# 
		# Gaming session number by game type:
		# [Gaming session number by game type]
		# 
		# Game type:
		# [Game type]
		# 
		# Entry:
		# [Gaming session number. Game type (Finished playing time)]
		# 
		# Game titles:
		# [Game titles]
		# 
		# (
		# Sub-game titles:
		# [Sub-game titles]
		# )
		#
		# Platform:
		# [Platform]
		# 
		# When I started playing:
		# [Started playing time in local timezone]
		# 
		# When I finished playing:
		# [Finished playing time in the local timezone]
		# 
		# When I finished playing (UTC):
		# [Finished playing time in the UTC time]
		# 
		# Gaming session duration:
		# [Gaming session duration]
		#
		# Gaming session description:
		# [Gaming session description]
		# 
		# (
		# States:
		# [State texts]
		# )

		# Define the gaming session folder, file name, and file by game type
		by_game_type_folder = self.dictionary["Type"]["Folders"]["By game type"]["Files"]["root"]
		file_name = self.dictionary["Entry"]["Name"]["en"]["Sanitized"]
		file = by_game_type_folder + file_name + ".txt"

		# Create the gaming session file inside the "By game type" folder
		self.File.Create(file)

		# ---------- #

		# Define the dictionary for the gaming session texts
		self.dictionary["Entry"]["Text"] = {
			"General": self.Define_File_Text("General")
		}

		# Fill the entry "Text" dictionary with the entry texts of each language
		for language in self.languages["small"]:
			self.dictionary["Entry"]["Text"][language] = self.Define_File_Text(language)

		# ---------- #

		# Write the general entry text into the general entry file
		self.File.Edit(file, self.dictionary["Entry"]["Text"]["General"], "w")

		# ---------- #

		# Define the entry file for the "Played" folder of the game folder
		played_folder = self.game["Folders"]["Played"]["files"]["root"]
		file_name = self.dictionary["Entry"]["Name"][self.user_language]["Sanitized"] + ".txt"
		file = played_folder + file_name

		# Create the played entry file
		self.File.Create(file)

		# Write the entry text in the user's language into the played entry file
		self.File.Edit(file, self.dictionary["Entry"]["Text"][self.user_language], "w")

		# ---------- #

		# If the game has sub-games
		if self.game["States"]["Has sub-games"] == True:
			# Define the entry file for the "Played" folder of the sub-game folder
			played_folder = self.game["Sub-game"]["Folders"]["Played"]["files"]["root"]
			file_name = self.dictionary["Entry"]["Name"][self.user_language]["Sanitized"] + ".txt"
			file = played_folder + file_name

			# Create the played sub-game entry file
			self.File.Create(file)

			# Write the entry text in the user's language into the played sub-game entry file
			self.File.Edit(file, self.dictionary["Entry"]["Text"][self.user_language], "w")

	def Define_Titles(self, language_parameter, language, titles_dictionary):
		# Initialize a variable to hold the game or sub-game titles
		game_titles = []

		# Initialize the key to access the original game or sub-game title
		key = "Original"

		# Check if there is a romanized title available
		if "Romanized" in titles_dictionary:
			# If a romanized title exists, add the original title to the list of titles
			game_titles.append(titles_dictionary["Original"])

			# Update the key to access the romanized title for later use
			key = "Romanized"

		# Add the original or romanized title to the list of titles
		game_titles.append(titles_dictionary[key])

		# Check if the language parameter is "General"
		# And if the language title is different from the original or romanized title
		if (
			language_parameter == "General" and
			titles_dictionary["Language"] != titles_dictionary[key]
		):
			# Add the language title to the list of titles
			game_titles.append(titles_dictionary["Language"])

			# Iterate through the small languages list
			for local_language in self.languages["small"]:
				# Check if the local language exists in the titles dictionary
				# And if the title in that language is different from the language title
				if (
					local_language in titles_dictionary and
					titles_dictionary[local_language] != titles_dictionary["Language"]
				):
					# Add the current local language title to the list of titles
					game_titles.append(titles_dictionary[local_language])

		# Check if the language parameter is not "General"
		# And if the specified language exists in the media (item) titles
		if (
			language_parameter != "General" and
			language in titles_dictionary
		):
			# Add the language title to the list of titles
			game_titles.append(titles_dictionary[language])

		# Return the list of titles
		return game_titles

	def Define_File_Text(self, language_parameter = None):
		# Check if a specific language parameter is provided
		if language_parameter != "General":
			# Define the local language as the language parameter
			language = language_parameter # Use the provided language parameter

		# If the language parameter is "General", use the user's preferred language
		if language_parameter == "General":
			language = self.user_language

		# Retrieve the full language name from the languages dictionary
		full_language = self.languages["full"][language]

		# ---------- #

		# Define the list of entry text lines
		lines = [
			# Add the gaming session number
			self.texts["gaming_session_number"][language] + ":" + "\n" + str(self.dictionaries["Sessions"]["Numbers"]["Total"]) + "\n",

			# Add the gaming session number by game type
			self.texts["gaming_session_number_by_game_type"][language] + ":" + "\n" + str(self.dictionaries["Game type"][self.game_type]["Numbers"]["Total"]) + "\n",

			# Add the game type
			self.texts["game_type"][language] + ":" + "\n" + self.dictionary["Type"]["Type"][language] + "\n",

			# Add the entry text and the entry name
			self.Language.texts["entry, title()"][language] + ":" + "\n" + self.dictionary["Entry"]["Name"]["en"]["Normal"] + "\n"
		]

		# ---------- #

		# Define the game titles
		game_titles = self.Define_Titles(language_parameter, language, self.game["Titles"])

		# Determine the appropriate game title text based on the list of game titles
		text = self.texts["game_title"][language]

		# If it has more than one title, use the plural text
		if len(game_titles) > 1:
			text = self.texts["game_titles"][language]

		# Add a newline and the "game title(s)" text
		lines.append(text + ":" + "\n" + "{}")

		# ---------- #

		# If the game has sub-games
		# And the sub-game title is not the same as the game title
		if (
			self.game["States"]["Has sub-games"] == True and
			self.game["Sub-game"]["Title"] != self.game["Title"]
		):
			# Define the sub-game titles
			sub_game_titles = self.Define_Titles(language_parameter, language, self.game["Sub-game"]["Titles"])

			# Determine the appropriate sub-game title text based on the list of sub-game titles
			text = self.game["Sub-games"]["Texts"]["Singular"][language]

			# If it has more than one title, use the plural text
			if len(sub_game_titles) > 1:
				text = self.game["Sub-games"]["Texts"]["Singular"][language]

			# Add a newline and the sub-game title text
			lines.append(text + ":" + "\n" + "{}")

		# ---------- #

		# Add the "Platform" text and the platform where the user played the game
		lines.append(self.Language.texts["platform, title()"][language] + ":" + "\n" + self.game["Platform"][language] + "\n")

		# ---------- #

		# Add the "When I started playing" (local timezone) title and format string
		started_playing_text = self.texts["when_i_started_playing"][language] + ":" + "\n" + "{}"
		lines.append(started_playing_text)

		# Add the "When I finished playing" (local timezone) title and format string
		finished_playing_timezone_text = self.texts["when_i_finished_playing"][language] + ":" + "\n" + "{}"
		lines.append(finished_playing_timezone_text)

		# Add the "When I finished playing (UTC)" title and format string
		finished_playing_utc_text = self.texts["when_i_finished_playing"][language] + " (" + self.Date.texts["utc"][language] + ")" + ":" + "\n" + "{}"
		lines.append(finished_playing_utc_text)

		# Add the "Gaming session duration" title and format string
		duration_text = self.Language.texts["gaming_session_duration"][language] + ":" + "\n" + "{}"
		lines.append(duration_text)

		# ---------- #

		# If the user wrote a description for the gaming session
		if self.dictionary["Entry"]["Diary Slim"]["Write description"] == True:
			# Define the gaming session description text as the plural one by default
			text = self.texts["gaming_session_descriptions"][language]
			line_break = "\n\n"

			# If the language parameter is not "General"
			if language_parameter != "General":
				# Define the gaming session description text as the singular one
				text = self.texts["gaming_session_description"][language]
				line_break = "\n"

			# Add the gaming session description and the line break(s) with a format character
			lines.append("\n" + text + ":" + line_break + "{}")

		# ---------- #

		# Add the state texts lines if there are any state texts defined
		if self.dictionary["States"]["Texts"] != {}:
			# Initialize the text for the states section
			text = "\n" + self.Language.texts["states, title()"][language] + ":" + "\n"

			# Iterate through each state text in the dictionary
			for key in self.dictionary["States"]["Texts"]:
				# Get the text for the current state in the specified language
				language_text = self.dictionary["States"]["Texts"][key][language]

				# Append the current state text to the overall text
				text += language_text

				# Add a newline if this is not the last state text
				if key != list(self.dictionary["States"]["Texts"].keys())[-1]:
					text += "\n"

			# Append the constructed state text to the list of lines
			lines.append(text)

		# ---------- #

		# Define the language entry text by converting the list of lines to a single text block
		file_text = self.Text.From_List(lines, next_line = True)

		# ---------- #

		# Define items to be added to file text format
		items = []

		# ---------- #

		# Now create the string with the game titles to add to the list of items
		titles = "\n".join(game_titles) + "\n"

		# Add the game titles to the list of items
		items.append(titles)

		# ---------- #

		# If the game has sub-games
		# And the sub-game title is not the same as the game title
		if (
			self.game["States"]["Has sub-games"] == True and
			self.game["Sub-game"]["Title"] != self.game["Title"]
		):
			# Remove ": " from the beginning of the titles, if it exists
			sub_game_titles = [title.lstrip(": ") for title in sub_game_titles]

			# Now create the string with the sub-game titles to add to the list of items
			titles = "\n".join(sub_game_titles) + "\n"

			# Add the sub-game titles to the list of items
			items.append(titles)

		# ---------- #

		# Add the started playing time
		items.append(self.entry_dictionary["Times"]["Started playing"] + "\n")

		# Iterate over the relevant keys to obtain the times
		for time_key in ["Finished playing", "Finished playing (UTC)"]:
			# Check if the key exists
			if time_key in self.dictionary["Entry"]["Times"]:
				# Define the timezone key as "Timezone"
				timezone_key = "Timezone"

				# Define the format as the timezone one
				format = "HH:MM DD/MM/YYYY"

				# If the "UTC" text is inside the time key
				if "UTC" in time_key:
					# Update the timezone key to be the UTC one
					timezone_key = "UTC"

					# Define the format as the UTC one
					format = "YYYY-MM-DDTHH:MM:SSZ"

				# Retrieve the formatted datetime string from the "Times" dictionary,
				# using the specified time key (e.g., "Finished playing"), timezone key (e.g., "UTC"),
				# and format (e.g., "YYYY-MM-DDTHH:MM:SSZ")
				time = self.dictionary["Entry"]["Times"][time_key][timezone_key]["DateTime"]["Formats"][format]

				# Append the times to the list of items
				items.append(time + "\n")

		# Add the gaming session duration (the difference between the start and finished playing times)
		items.append(self.entry_dictionary["Times"]["Gaming session duration"]["Text"][language])

		# ---------- #

		# If the user wrote a description for the gaming session
		if self.dictionary["Entry"]["Diary Slim"]["Write description"] == True:
			# Define an empty string to add the descriptions to
			descriptions = ""

			# Define a shortcut for the descriptions dictionary
			descriptions_dictionary = self.dictionary["Entry"]["Diary Slim"]["Descriptions"]

			# Define the description to be added based on the language
			# Only the description for the current language
			if language_parameter != "General":
				descriptions = descriptions_dictionary[language]["string"]

			# Or all language descriptions
			else:
				# Iterate through the list of small languages
				for local_language in self.languages["small"]:
					# Get the full language
					full_language = self.languages["full"][local_language]

					# Add the full language and the language description to the root descriptions text
					descriptions += full_language + ":" + "\n" + descriptions_dictionary[local_language]["string"]

					# If the local language is not the last language in the list
					if local_language != self.languages["small"][-1]:
						# Add two line breaks to the root descriptions text
						descriptions += "\n\n"

			# Add the descriptions to the list of items
			items.append(descriptions)

		# ---------- #

		# Return the formatted text with the items, including the times
		return file_text.format(*items)

	def Add_Entry_File_To_Year_Folder(self):
		# Iterate through the list of small languages
		for language in self.languages["small"]:
			# Get the full language
			full_language = self.languages["full"][language]

			# Define a shortcut for the folder
			folder = self.current_year["Folders"][language]["Gaming sessions"]

			# Define the game type folder name
			game_type_folder = self.dictionary["Type"]["Type"][language]

			# Define and create the game type folder
			folder["Game type"] = {
				"root": folder["root"] + game_type_folder + "/"
			}

			self.Folder.Create(folder["Game type"]["root"])

			# Update the folder to be the game type folder
			folder = folder["Game type"]

			# Get the entry file name
			entry_file_name = self.dictionary["Entry"]["Name"][language]["Sanitized"]

			# Define and create the entry file
			folder["Entry file"] = folder["root"] + entry_file_name + ".txt"
			self.File.Create(folder["Entry file"])

			# Write the entry text by language inside the year entry file
			self.File.Edit(folder["Entry file"], self.dictionary["Entry"]["Text"][language], "w")

			# ---------- #

			# Create the "First of the Year" entry file
			if self.game["States"]["First gaming session by game type in the year"] == True:
				# Define the folder shortcut
				folder = self.current_year["Folders"][language]["Firsts of the Year"]["Gaming sessions"]

				# Define and create the "First of the Year" entry file
				folder["Entry file"] = folder["root"] + entry_file_name + ".txt"
				self.File.Create(folder["Entry file"])

				# Write the entry text by language inside the "First of the Year" entry file
				self.File.Edit(folder["Entry file"], self.dictionary["Entry"]["Text"][language], "w")

	def Check_Game_Status(self):
		# Define the game type variable for easier typing
		self.game_type = self.dictionary["Type"]["Type"]["en"]

		# Define the "Ask if the game was completed" state as True
		self.game["States"]["Ask if the game was completed"] = True

		# Define the list of game types that do not have an ending
		game_types_without_ending = []

		# Define the keys for those game types
		keys = [
			"FPS",
			"Idle Clicker",
			"Multiplayer",
			"Rhythm",
			"RPG",
			"Survival"
		]

		# Iterate through the list of keys
		for key in keys:
			# Get the English game type
			game_type = self.game_types["Dictionary"][key]["Type"]["en"]

			# Add it to the list of game types
			game_types_without_ending.append(game_type)

		# If the game type is inside the list of game types with no ending
		if self.game_type in game_types_without_ending:
			# Define the "Ask if the game was completed" state as False
			self.game["States"]["Ask if the game was completed"] = False

		# If the "Ask if the game was completed" state is True
		if self.game["States"]["Ask if the game was completed"] == True:
			# Ask if the user completed the whole game
			self.game["States"]["Completed game"] = self.Input.Yes_Or_No(self.language_texts["did_you_finished_the_whole_game"])

		# If the user completed the whole game
		if self.game["States"]["Completed game"] == True:
			# Update the status key in the game details to be the "Completed" one
			self.Change_Status(self.dictionary)

	def Check_Game_Dates(self):
		# Completed game time and date template
		template = self.language_texts["when_i_finished_playing"] + ":" + "\n" + \
		self.dictionary["Entry"]["Times"]["Finished playing"]["Formats"]["HH:MM DD/MM/YYYY"] + "\n" + \
		"\n" + \
		self.Date.language_texts["duration, title()"] + ":" + "\n" + \
		"{}"

		# Gets the date that the user started and finished playing the game and writes it to the game dates text file
		if self.game["States"]["Completed game"] == True:
			# Gets the game dates from the game dates file
			self.game["Dates"] = self.File.Dictionary(self.game["Folders"]["dates"], next_line = True)

			# Define the key to search for the date
			key = self.language_texts["when_i_started_playing"]

			# Get the started playing time
			self.game["Started playing"] = self.Date.To_UTC(self.Date.From_String(self.game["Dates"][key]))

			# Define time spent playing using started playing time and finished playing time
			self.game["Time spent playing"] = self.Date.Difference(self.game["Started playing"], self.dictionary["Entry"]["Times"]["Finished playing (UTC)"])["Text"][self.user_language]

			if self.game["Time spent playing"][0] + self.game["Time spent playing"][1] == ", ":
				self.game["Time spent playing"] = self.game["Time spent playing"][2:]

			# Format the time template
			self.game["Formatted datetime template"] = "\n\n" + template.format(self.game["Time spent playing"])

			# Read the game dates file
			self.game["Finished playing text"] = self.File.Contents(self.game["Folders"]["dates"])["string"]

			# Add the time template to the game dates text
			self.game["Finished playing text"] += self.game["Formatted datetime template"]

			# Update the game dates text file
			self.File.Edit(self.game["Folders"]["dates"], self.game["Finished playing text"], "w")

			text = self.game_types["Genders"][self.user_language]["masculine"]["the"] + " " + self.language_texts["game, title()"].lower()

			# Add the time template to the Diary Slim text
			self.game["Finished playing text"] = self.game["Finished playing text"].replace(self.language_texts["when_i_started_playing"], self.language_texts["when_i_started_playing"] + " " + text)

			self.dictionary["Entry"]["Diary Slim"]["Dates"] = "\n\n" + self.game["Finished playing text"]

	def Define_Diary_Slim_Text(self):
		# Define the list of items
		items = [
			self.dictionary["Type"]["Type"][self.user_language].lower(),
			self.game["Titles"]["Language"],
			self.dictionary["Entry"]["Times"]["Gaming session duration"]["Text"][self.user_language]
		]

		# Replace the title inside the list of items if the game has sub-games
		# And the sub-game title is not the game title
		if (
			self.game["States"]["Has sub-games"] == True and
			self.game["Sub-game"]["Title"] != self.game["Title"]
		):
			items[1] = self.game["Sub-game"]["With game title"]["Language"]

		# Define the template
		template = self.language_texts["i_played_the_{}_game_called_{}_for_{}"] + "."

		# Format the template with the items
		self.dictionary["Entry"]["Diary Slim"]["Text"] = template.format(*items)

		# If the user wants to write a description
		if self.dictionary["Entry"]["Diary Slim"]["Write description"] == True:
			# Add the session description to the "Diary Slim" text
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.dictionary["Entry"]["Diary Slim"]["Descriptions"][self.user_language]["string"]

		# If there are states, add the texts to the Diary Slim text
		if self.dictionary["States"]["States"] != {}:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.Language.language_texts["states, title()"] + ":" + "\n"

			for key in self.dictionary["States"]["Texts"]:
				self.dictionary["Entry"]["Diary Slim"]["Text"] += self.dictionary["States"]["Texts"][key][self.user_language]

				if key != list(self.dictionary["States"]["Texts"].keys())[-1]:
					self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n"

		# If there are dates, add them to the Diary Slim text
		if "Dates" in self.dictionary["Entry"]["Diary Slim"]:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += self.dictionary["Entry"]["Diary Slim"]["Dates"]

	def Post_On_Social_Networks(self):
		# Define the "Social Networks" dictionary
		self.social_networks = {
			"List": [
				"Discord",
				"WhatsApp",
				"Instagram",
				"Facebook"
			],
			"List text": ""
		}

		# Define the list text, with all the Social Networks separated by commas
		self.social_networks["List text"] = self.Text.From_List(self.social_networks["List"], and_text = False)

		# Remove the "Discord" social networks
		self.social_networks["List"].remove("Discord")

		# Define the list text, with all the Social Networks separated by commas
		# But without Discord
		self.social_networks["List text (without Discord)"] = self.Text.From_List(self.social_networks["List"])

		# Define the item text to be used
		self.social_networks["Item text"] = self.language_texts["the_game_cover"]

		# Define the "posted" template
		self.social_networks["Template"] = self.language_texts["i_posted_the_played_game_text, type: template"] + "."

		# Define the template list of items
		self.social_networks["Items"] = [
			self.social_networks["Item text"],
			"Discord",
			self.social_networks["List text (without Discord)"],
			"Twitter, Bluesky, " + self.Language.language_texts["and"] + " Threads"
		]

		# Format the template with the list of items
		self.dictionary["Entry"]["Diary Slim"]["Posted on the Social Networks text"] = self.social_networks["Template"].format(*self.social_networks["Items"])

		# Define the text to show while asking the user if they want to post on the social networks
		text = self.language_texts["post_on_the_social_networks"] + " (" + self.social_networks["List text"] 

		# Add the "and others" text
		text += ", " + self.Language.language_texts["and_others, feminine"]

		# Add the closing parenthesis
		text += ")"

		# Define the "ask for input" switch as False
		ask_for_input = False

		# Define the "Post on the social networks" state as True
		self.dictionary["Entry"]["States"]["Post on the Social Networks"] = True

		# If the "Testing" switch is False
		# If the "ask for input" switch is True
		if (
			self.switches["Testing"] == False and
			ask_for_input == True
		):
			# Show a separator
			print()
			print(self.separators["5"])

			# Ask if the user wants to post the played session status on the social networks
			self.dictionary["Entry"]["States"]["Post on the Social Networks"] = self.Input.Yes_Or_No(text)

		# If the user answer is yes
		if self.dictionary["Entry"]["States"]["Post on the Social Networks"] == True:
			# Import the "Open_Social_Network" sub-class of the "Social_Networks" module
			from Social_Networks.Open_Social_Network import Open_Social_Network as Open_Social_Network

			# Define the "Social Networks" dictionary
			social_networks = {
				"List": [
					"WhatsApp",
					"Facebook",
					"Discord"
				],
				"Custom links": {
					"Discord": "https://discord.com/channels/311004778777935872/1126797917693427762" # "#play-history" channel on my Discord server
				}
			}

			# Open the social networks, one by one
			# (Commented out because this class is not working properly)
			#Open_Social_Network(social_networks)

		# Show a separator
		print()
		print(self.separators["5"])
		print()

	def Write_On_Diary_Slim(self):
		# Add "Posted on Social Networks" text if the user wanted to post the entry text on the Social Networks
		if self.dictionary["Entry"]["States"]["Post on the Social Networks"] == True:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.dictionary["Entry"]["Diary Slim"]["Posted on the Social Networks text"]

		from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

		# Define the "Write on Diary Slim" dictionary
		dictionary = {
			"Text": self.dictionary["Entry"]["Diary Slim"]["Text"],
			"Time": self.dictionary["Entry"]["Times"]["Finished playing"]["Formats"]["HH:MM DD/MM/YYYY"],
			"Add": {
				"Dot": False
			}
		}

		# Write the entry text on Diary Slim
		Write_On_Diary_Slim_Module(dictionary)

	def Get_Game_Title(self, is_sub_game = False, sub_game = None, language = False, no_game_title = False):
		# Define the key to get the game title
		key = "Original"

		if "Romanized" in self.game["Titles"]:
			key = "Romanized"

		# If the "language" parameter is True
		if language == True:
			# Define the game title key as the "Language" one
			key = "Language"

		# Define the local game title variable
		game_title = self.game["Titles"][key]

		# If the "is sub-game" parameter is True
		# And there is a sub-game inside the game dictionary
		# And the sub-game is not the root game
		if (
			is_sub_game == True and
			"Sub-game" in self.game and
			self.game["Sub-game"]["Title"] != self.game["Title"]
		):
			# Define the key to get the sub-game title
			key = "Original"

			if "Romanized" in self.game["Titles"]:
				key = "Romanized"

			# If the "language" parameter is True
			if language == True:
				# Define the game title key as the "Language" one
				key = "Language"

			# If the sub-game parameter is None
			if sub_game == None:
				sub_game = self.game["Sub-game"]

			# Get the sub-game title using the key
			sub_game_title = sub_game["Titles"][key]

			# If the first two characters of the title are not a colon and a space
			if sub_game_title[0] + sub_game_title[1] != ": ":
				# Add a space
				game_title += " "

			# If the "no game title" parameter is True
			if no_game_title == True:
				# Reset the game title to an empty string
				game_title = ""

			# Add the sub-game title to the root game title
			game_title += sub_game_title

			# If the "no game title" parameter is True
			# And the first two characters of the game title is a colon and a space
			if (
				no_game_title == True and
				game_title[0] + game_title[1] == ": "
			):
				# Remove the colon and space
				game_title = game_title[2:]

		# Return the game title
		return game_title

	def Update_Statistic(self):
		# Define a local game dictionary
		game = {
			"Titles": {
				"Original": self.Get_Game_Title(),
				"Language": self.Get_Game_Title(language = True)
			}
		}

		# If there is a sub-game inside the game dictionary
		if "Sub-game" in self.game:
			# Create a sub-game titles dictionary and add it to the "Sub-item" key
			game["Titles"]["Sub-game"] = {
				"Original": self.Get_Game_Title(is_sub_game = True),
				"Original (no game title)": self.Get_Game_Title(is_sub_game = True, no_game_title = True),
				"Language": self.Get_Game_Title(is_sub_game = True, language = True)
			}

		# If the game contains sub-games
		if "Sub-games" in self.game:
			# Pass the "Items" dictionary to the local game dictionary
			game["Items"] = self.game["Sub-games"]["Items"]

		# Define the game type
		game_type = self.dictionary["Type"]["Type"][self.user_language].lower()

		# Update the game statistics for the current year and month, passing the local game dictionary and the game type
		# And getting the statistics text back
		self.dictionary["Statistics text"] = GamePlayer.Update_Statistics(self, game, game_type)