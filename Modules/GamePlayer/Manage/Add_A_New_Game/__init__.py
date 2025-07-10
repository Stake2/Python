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

		if "Update" not in self.dictionary:
			# Select the game to define its variables
			self.Select_Game(self.dictionary)

			# Add the game to the Game Information GamePlayer
			self.Add_To_The_Database()

			# Instantiate the root class to update the database files
			super().__init__()

	def Type_Game_Information(self):
		print()
		print(self.separators["5"])
		print()
		print(self.language_texts["type_the_game_information_(some_items_can_be_left_empty_by_pressing_enter)"] + ":")

		# Ask for the game titles
		if "Original" not in self.game["Titles"]:
			if self.switches["Testing"] == False:
				title = self.Input.Type(self.Language.language_texts["original_title"], next_line = True, accept_enter = False)

			if self.switches["Testing"] == True:
				title = self.Language.language_texts["title, title()"] + " (" + self.dictionary["Type"]["Type"][self.language["Small"]] + ")"

				if self.game["Title"] == "":
					self.game["Title"] = title

				self.game["Titles"]["Original"] = self.game["Title"]

			for language in self.languages["small"]:
				translated_language = self.languages["full_translated"][language][self.language["Small"]]

				title = ""

				if self.switches["Testing"] == False:
					title = self.Input.Type(self.Language.language_texts["title_in_{}"].format(translated_language), next_line = True)

				if title != "":
					self.game["Titles"][language] = title

			title = ""

			if self.switches["Testing"] == False:
				title = self.Input.Type(self.Language.language_texts["romanized_title"], next_line = True)

			if title != "":
				self.game["Titles"]["Romanized"] = title

		# Ask for the game year and dates
		text = self.Date.language_texts["year, title()"] + " (" + self.Language.language_texts["format"] + ": " + str(self.Date.Now()["Units"]["Year"]) + ")"

		if self.switches["Testing"] == False:
			year = self.Input.Type(text, next_line = True, regex = "^[1-9]{1}[0-9]{3}; " + str(self.Date.Now()["Units"]["Year"]), accept_enter = False)

		if self.switches["Testing"] == True:
			year = self.Date.Now()["Units"]["Year"]

		self.game["Year"] = year

		for date_type in ["start", "end"]:
			text = self.Date.language_texts[date_type + "_date"] + " (" + self.Language.language_texts["format"] + ": " + self.Date.Now()["Formats"]["DD/MM/YYYY"] + ")"

			accept_enter = False
			regex = None

			if date_type == "end":
				accept_enter = True

			if self.switches["Testing"] == False:
				date = self.Input.Type(text, next_line = True, accept_enter = accept_enter, regex = "[0-9]{2}\/[0-9]{2}\/[1-9]{1}[0-9]{3}; " + self.Date.Now()["Formats"]["DD/MM/YYYY"])

			if self.switches["Testing"] == True:
				date = self.Date.Now()["Formats"]["DD/MM/YYYY"]

			if date != "":
				import re

				if (
					date_type == "end" and
					re.search("[0-9]{2}\/[0-9]{2}\/[1-9]{1}[0-9]{3}", date) == None
				):
					date = self.Input.Type(text, next_line = True, accept_enter = False, regex = "[0-9]{2}\/[0-9]{2}\/[1-9]{1}[0-9]{3}; " + self.Date.Now()["Formats"]["DD/MM/YYYY"])

				self.game[date_type.title() + " date"] = date

		# Ask for the original language of the game
		self.game["Language"] = "[" + self.Language.language_texts["empty, title()"] + "]"

		if "Update" not in self.dictionary:
			show_text = self.Language.language_texts["languages, title()"]
			select_text = self.Language.language_texts["language, title()"]

			languages = list(self.languages["full"].values())
			languages.append("[" + self.Language.language_texts["empty, title()"] + "]")

			if self.switches["Testing"] == False:
				language = self.Input.Select(show_text = show_text, select_text = select_text, options = languages)["option"]

			if self.switches["Testing"] == True:
				language = "[" + self.Language.language_texts["empty, title()"] + "]"

			if language != "[" + self.Language.language_texts["empty, title()"] + "]":
				self.game["Language"] = language

			# Ask for the game platform
			show_text = self.Language.language_texts["platforms, title()"]
			select_text = self.Language.language_texts["platform, title()"]

			if self.switches["Testing"] == False:
				platform = self.Input.Select(show_text = show_text, select_text = select_text, options = self.game_types["Platforms"][self.language["Small"]])["option"]

			if self.switches["Testing"] == True:
				platform = self.game_types["Platforms"][self.language["Small"]][0]

			if "Platform" not in self.game:
				self.game["Platform"] = platform

		# Ask for the game developers, publishers, and distributors
		for key in ["developers", "publishers", "distributors"]:
			text = self.Language.language_texts[key + ", title()"]

			if self.switches["Testing"] == False:
				accept_enter = False

				if key == "publishers":
					accept_enter = True

				self.game[key.capitalize()] = self.Input.Type(text + ":", next_line = True, accept_enter = accept_enter)

				if self.game[key.capitalize()] == "":
					self.game.pop(key.capitalize())

			if self.switches["Testing"] == True:
				self.game[key.capitalize()] = text

		# Ask for the game status
		if "Update" not in self.dictionary:
			show_text = self.Language.language_texts["statuses, title()"]
			select_text = self.Language.language_texts["status, title()"]

			if self.switches["Testing"] == False:
				status = self.Input.Select(show_text = show_text, select_text = select_text, options = self.language_texts["statuses, type: list"])["option"]

			if self.switches["Testing"] == True:
				status = self.language_texts["statuses, type: list"][0]

			if "Status" not in self.game:
				self.game["Status"] = status

	def Create_Details(self):
		if "Details" not in self.game:
			self.game["Details"] = {
				self.Language.language_texts["title, title()"]: self.game["Title"]
			}

		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language][self.language["Small"]]

			key = self.Language.language_texts["title_in_{}"].format(translated_language) 

			if language in self.game["Titles"]:
				self.game["Details"][key] = self.game["Titles"][language]

		if "Romanized" in self.game["Titles"]:
			key = self.Language.language_texts["romanized_title"]

			self.game["Details"][key] = self.game["Titles"]["Romanized"]

		self.game["Details"][self.Date.language_texts["year, title()"]] = self.game["Year"]

		if "Start date" in self.game:
			self.game["Details"][self.Date.language_texts["start_date"]] = self.game["Start date"]

		if "End date" in self.game:
			self.game["Details"][self.Date.language_texts["end_date"]] = self.game["End date"]

		if (
			"Update" not in self.dictionary and
			"Language" in self.game and
			self.game["Language"] != "[" + self.Language.language_texts["empty, title()"] + "]"
		):
			self.game["Details"][self.Language.language_texts["original_language"]] = self.game["Language"]

		self.game["Details"][self.Language.language_texts["platform, title()"]] = self.game["Platform"][self.language["Small"]]

		for key in ["developers", "publishers", "distributors"]:
			text_key = key

			if key.capitalize() in self.game:
				if ", " not in self.game[key.capitalize()]:
					text_key = text_key[:-1]

				text_key = self.Language.language_texts[text_key + ", title()"]

				self.game["Details"][text_key] = self.game[key.capitalize()]

		if "Status" in self.game:
			self.game["Details"][self.Language.language_texts["status, title()"]] = self.game["Status"]

		# Create the game folders
		self.game["Folders"] = {
			"root": self.dictionary["Type"]["Folders"]["Game information"]["root"] + self.Sanitize_Title(self.game["Title"]) + "/"
		}

		self.Folder.Create(self.game["Folders"]["root"])

		# Create the game details file
		self.game["Folders"]["details"] = self.game["Folders"]["root"] + self.Language.language_texts["details, title()"] + ".txt"
		self.File.Create(self.game["Folders"]["details"])

		# Write into the game details file
		self.File.Edit(self.game["Folders"]["details"], self.Text.From_Dictionary(self.game["Details"]), "w")

		# Remove the "folders" dictionary to let "Select_Data" create it
		self.game.pop("folders")

	def Add_To_The_Database(self):
		# Get the JSON dictionary of the game type
		self.dictionary["Type"]["JSON"] = self.JSON.To_Python(self.dictionary["Type"]["Folders"]["Game information"]["Information"])

		# Add the game title to the list of titles
		self.dictionary["Type"]["JSON"]["Titles"].append(self.game["Title"])

		# Add the game status to the list of statuses
		english_status = self.Get_Language_Status(self.game["Status"])

		self.dictionary["Type"]["JSON"]["Status"][english_status].append(self.game["Title"])

		# Update the number of games inside the JSON dictionary
		self.dictionary["Type"]["JSON"]["Number"] = len(self.dictionary["Type"]["JSON"]["Titles"])

		# Edit the "Information.json" file with the updated "Information" dictionary
		self.JSON.Edit(self.dictionary["Type"]["Folders"]["Game information"]["Information"], self.dictionary["Type"]["JSON"])