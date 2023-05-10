# Add_A_New_Game.py

from GamePlayer.GamePlayer import GamePlayer as GamePlayer

class Add_A_New_Game(GamePlayer):
	def __init__(self, dictionary = {}):
		super().__init__()

		self.dictionary = dictionary

		# Define the dictionary and select the game type
		if self.dictionary == {}:
			self.dictionary = {
				"Type": self.Select_Game_Type(),
				"Game": {
					"Title": "",
					"Titles": {}
				}
			}

		self.game = self.dictionary["Game"]

		# Ask for the game information
		self.Type_Game_Information()

		# Create the details dictionary
		self.Create_Details()

		# Select the game to define its variables
		self.Select_Game(self.dictionary)

		# Add the game to the Game Information GamePlayer
		self.Add_To_The_Database()

		# Instantiate the root class to update the database files
		super().__init__()

	def Type_Game_Information(self):
		print()
		print(self.large_bar)
		print()
		print(self.language_texts["type_the_game_information_(some_items_can_be_left_empty_by_pressing_enter)"] + ":")

		# Ask for the game titles
		if self.switches["testing"] == False:
			title = self.Input.Type(self.JSON.Language.language_texts["original_title"], next_line = True, accept_enter = False)

		if self.switches["testing"] == True:
			title = self.JSON.Language.language_texts["title, title()"] + " (" + self.dictionary["Type"]["Type"][self.user_language] + ")"

		if self.game["Title"] == "":
			self.game["Title"] = title

		self.game["Titles"]["Original"] = self.game["Title"]

		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language][self.user_language]

			title = ""

			if self.switches["testing"] == False:
				title = self.Input.Type(self.JSON.Language.language_texts["title_in_{}"].format(translated_language), next_line = True)

			if title != "":
				self.game["Titles"][language] = title

		title = ""

		if self.switches["testing"] == False:
			title = self.Input.Type(self.JSON.Language.language_texts["romanized_title"], next_line = True)

		if title != "":
			self.game["Titles"]["Romanized"] = title

		# Ask for the game year and dates
		text = self.Date.language_texts["year, title()"] + " (" + self.JSON.Language.language_texts["format"] + ": " + str(self.Date.Now()["Units"]["Year"]) + ")"

		if self.switches["testing"] == False:
			year = self.Input.Type(text, next_line = True, regex = "^[1-9]{1}[0-9]{3}; " + str(self.Date.Now()["Units"]["Year"]), accept_enter = False)

		if self.switches["testing"] == True:
			year = self.Date.Now()["Units"]["Year"]

		self.game["Year"] = year

		for date_type in ["start", "end"]:
			text = self.Date.language_texts[date_type + "_date"] + " (" + self.JSON.Language.language_texts["format"] + ": " + self.Date.Now()["Formats"]["DD/MM/YYYY"] + ")"

			accept_enter = False
			regex = None

			if date_type == "end":
				accept_enter = True

			if self.switches["testing"] == False:
				date = self.Input.Type(text, next_line = True, accept_enter = accept_enter, regex = "[0-9]{2}\/[0-9]{2}\/[1-9]{1}[0-9]{3}; " + self.Date.Now()["Formats"]["DD/MM/YYYY"])

			if self.switches["testing"] == True:
				date = self.Date.Now()["Formats"]["DD/MM/YYYY"]

			if date != "":
				import re

				if date_type == "end" and re.search("[0-9]{2}\/[0-9]{2}\/[1-9]{1}[0-9]{3}", date) == None:
					date = self.Input.Type(text, next_line = True, accept_enter = False, regex = "[0-9]{2}\/[0-9]{2}\/[1-9]{1}[0-9]{3}; " + self.Date.Now()["Formats"]["DD/MM/YYYY"])

				self.game[date_type.title() + " date"] = date

		# Ask for the original language of the game
		show_text = self.JSON.Language.language_texts["languages, title()"]
		select_text = self.JSON.Language.language_texts["language, title()"]

		languages = list(self.languages["full"].values())
		languages.append("[" + self.JSON.Language.language_texts["empty, title()"] + "]")

		if self.switches["testing"] == False:
			language = self.Input.Select(show_text = show_text, select_text = select_text, options = languages)["option"]

		if self.switches["testing"] == True:
			language = "[" + self.JSON.Language.language_texts["empty, title()"] + "]"

		if language != "[" + self.JSON.Language.language_texts["empty, title()"] + "]":
			self.game["Language"] = language

		# Ask for the game platform
		show_text = self.JSON.Language.language_texts["platforms, title()"]
		select_text = self.JSON.Language.language_texts["platform, title()"]

		if self.switches["testing"] == False:
			platform = self.Input.Select(show_text = show_text, select_text = select_text, options = self.game_types["Platforms"][self.user_language])["option"]

		if self.switches["testing"] == True:
			platform = self.game_types["Platforms"][self.user_language][0]

		if "Platform" not in self.game:
			self.game["Platform"] = platform

		# Ask for the game developers, publishers, and distributors
		for key in ["developers", "publishers", "distributors"]:
			text = self.JSON.Language.language_texts[key + ", title()"]

			if self.switches["testing"] == False:
				self.game[key.capitalize()] = self.Input.Type(text + ":", next_line = True, accept_enter = False)

			if self.switches["testing"] == True:
				self.game[key.capitalize()] = text

		# Ask for the game status
		show_text = self.JSON.Language.language_texts["statuses, title()"]
		select_text = self.JSON.Language.language_texts["status, title()"]

		if self.switches["testing"] == False:
			status = self.Input.Select(show_text = show_text, select_text = select_text, options = self.language_texts["statuses, type: list"])["option"]

		if self.switches["testing"] == True:
			status = self.language_texts["statuses, type: list"][0]

		if "Status" not in self.game:
			self.game["Status"] = status

	def Create_Details(self):
		self.game["Details"] = {
			self.JSON.Language.language_texts["title, title()"]: self.game["Title"]
		}

		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language][self.user_language]

			key = self.JSON.Language.language_texts["title_in_{}"].format(translated_language) 

			if language in self.game["Titles"]:
				self.game["Details"][key] = self.game["Titles"][language]

		if "Romanized" in self.game["Titles"]:
			key = self.JSON.Language.language_texts["romanized_title"]

			self.game["Details"][key] = self.game["Titles"]["Romanized"]

		self.game["Details"][self.Date.language_texts["year, title()"]] = self.game["Year"]

		if "Start date" in self.game:
			self.game["Details"][self.Date.language_texts["start_date"]] = self.game["Start date"]

		if "End date" in self.game:
			self.game["Details"][self.Date.language_texts["end_date"]] = self.game["End date"]

		if "Language" in self.game:
			self.game["Details"][self.JSON.Language.language_texts["original_language"]] = self.game["Language"]

		self.game["Details"][self.JSON.Language.language_texts["platform, title()"]] = self.game["Platform"]

		for key in ["developers", "publishers", "distributors"]:
			text_key = key

			if ", " not in self.game[key.capitalize()]:
				text_key = text_key[:-1]

			text_key = self.JSON.Language.language_texts[text_key + ", title()"]

			self.game["Details"][text_key] = self.game[key.capitalize()]

		if self.game["Status"] != self.JSON.Language.language_texts["remote, title()"]:
			self.game["Details"][self.JSON.Language.language_texts["status, title()"]] = self.game["Status"]

		# Create the game folders
		self.game["folders"] = {
			"root": self.dictionary["Type"]["Folders"]["information"]["root"] + self.Sanitize(self.game["Title"], restricted_characters = True) + "/"
		}

		self.Folder.Create(self.game["folders"]["root"])

		# Create the game details file
		self.game["folders"]["details"] = self.game["folders"]["root"] + self.JSON.Language.language_texts["details, title()"] + ".txt"
		self.File.Create(self.game["folders"]["details"])

		# Write into the game details file
		self.File.Edit(self.game["folders"]["details"], self.Text.From_Dictionary(self.game["Details"]), "w")

		# Remove the "folders" dictionary to let "Select_Data" create it
		self.game.pop("folders")

	def Add_To_The_Database(self):
		self.dictionary["Type"]["JSON"] = self.JSON.To_Python(self.dictionary["Type"]["Folders"]["information"]["info"])

		# Add to the titles list
		self.dictionary["Type"]["JSON"]["Titles"].append(self.game["Title"])

		# Add to the status titles list
		english_status = self.Get_Language_Status(self.game["Status"])

		self.dictionary["Type"]["JSON"]["Status"][english_status].append(self.game["Title"])

		# Update the number of game inside the json dictionary
		self.dictionary["Type"]["JSON"]["Number"] = len(self.dictionary["Type"]["JSON"]["Titles"])

		# Edit the "Info.json" file with the new dictionary
		self.JSON.Edit(self.dictionary["Type"]["Folders"]["information"]["info"], self.dictionary["Type"]["JSON"])