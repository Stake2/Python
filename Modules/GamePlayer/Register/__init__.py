# Register.py

from GamePlayer.GamePlayer import GamePlayer as GamePlayer

class Register(GamePlayer):
	def __init__(self, dictionary = {}):
		super().__init__()

		self.dictionary = dictionary

		# Ask for the entry information
		if self.dictionary == {}:
			self.Type_Entry_Information()

		self.dictionary["Entry"].update({
			"Times": {
				"UTC": self.Date.To_String(self.dictionary["Entry"]["Time"]["utc"]),
				"Timezone": self.Date.Now(self.dictionary["Entry"]["Time"]["date"].astimezone())["hh:mm DD/MM/YYYY"]
			},
			"Diary Slim": {
				"Text": "",
				"Clean text": ""
			},
			"States": {
				"Post on the Social Networks": False
			}
		})

		# Define the media variable to make typing the media dictionary easier
		self.game = self.dictionary["Game"]

		#self.Check_Game_Status()

		#if self.game["States"]["Re-playing"] == False and self.game["States"]["Completed game"] == True:
		#	self.Check_Game_Dates()

		# Database related methods
		self.Register_In_JSON()
		self.Create_Entry_File()
		self.Add_Entry_File_To_Year_Folder()

		self.Define_Diary_Slim_Text()

		self.Post_On_Social_Networks()

		self.Write_On_Diary_Slim()

		self.Show_Information(self.dictionary)

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

		# Define session and time related keys inside the dictionary
		self.Play.Register_The_Session()

		# Get the dictionary from the "Play" class with the session and time related keys
		self.dictionary = self.Play.dictionary

	def Register_In_JSON(self):
		self.game_type = self.dictionary["Type"]["Type"]["en"]

		dicts = [
			self.dictionaries["Sessions"],
			self.dictionaries["Game type"][self.game_type],
			self.dictionaries["Played"]
		]

		# Add one to the entry, game type entry, and root game type entry numbers
		for dict_ in dicts:
			dict_["Numbers"]["Total"] += 1

			if "Per Game Type" in dict_["Numbers"]:
				dict_["Numbers"]["Per Game Type"][self.game_type] += 1

		# Define sanitized version of entry name for files
		self.dictionary["Entry"]["Name"] = {
			"Normal": str(self.dictionaries["Sessions"]["Numbers"]["Total"]) + ". " + self.game_type + " (" + self.dictionary["Entry"]["Times"]["Timezone"] + ")",
			"Sanitized": ""
		}

		self.dictionary["Entry"]["Name"]["Sanitized"] = self.dictionary["Entry"]["Name"]["Normal"].replace(":", ";").replace("/", "-")

		# Add to the "Entries" lists
		for dict_ in dicts:
			if self.dictionary["Entry"]["Name"]["Normal"] not in dict_["Entries"]:
				dict_["Entries"].append(self.dictionary["Entry"]["Name"]["Normal"])

		# Define local game titles to remove some keys from them
		game_titles = self.game["Titles"].copy()
		game_titles.pop("Language")

		for key in ["ja", "Sanitized"]:
			if key in game_titles:
				game_titles.pop(key)

		for language in self.languages["small"]:
			if language in game_titles and game_titles["Original"] == game_titles[language]:
				game_titles.pop(language)

		self.key = self.dictionary["Entry"]["Name"]["Normal"]

		self.dictionaries["Sessions"]["Dictionary"][self.key] = {
			"Number": self.dictionaries["Sessions"]["Numbers"]["Total"],
			"Type number": self.dictionaries["Game type"][self.game_type]["Numbers"]["Total"],
			"Entry": self.dictionary["Entry"]["Name"]["Normal"],
			"Titles": game_titles,
			"Type": self.game_type,
			"Time": self.dictionary["Entry"]["Times"]["UTC"],
			"Session duration": self.dictionary["Entry"]["Session duration"]["Difference"]["Difference"]
		}

		self.dictionaries["Sessions"]["Dictionary"][self.key]["Session duration"]["Text"] = self.dictionary["Entry"]["Session duration"]["Difference"]["Text"]["en"]

		# Get the States dictionary
		self.dictionary["States"] = self.Define_States_Dictionary(self.dictionary)

		if self.dictionary["States"]["States"] != {}:
			self.dictionaries["Sessions"]["Dictionary"][self.key]["States"] = self.dictionary["States"]["States"]

		# Add entry dictionary to type and Registered entry dictionaries
		for dict_ in dicts:
			if dict_ != self.dictionaries["Sessions"]:
				dict_["Dictionary"][self.key] = self.dictionaries["Sessions"]["Dictionary"][self.key].copy()

		# Update the "Entries.json" file
		self.JSON.Edit(self.folders["play_history"]["current_year"]["sessions"], self.dictionaries["Sessions"])

		# Update the type "Entries.json" file
		self.JSON.Edit(self.dictionary["Type"]["Folders"]["per_game_type"]["sessions"], self.dictionaries["Game type"][self.game_type])

		# Update the game "Played.json" file
		self.JSON.Edit(self.game["folders"]["played"]["entries"], self.dictionaries["Played"])

		# Add to the root and type "Entry list.txt" file
		self.File.Edit(self.folders["play_history"]["current_year"]["entry_list"], self.dictionary["Entry"]["Name"]["Normal"], "a")
		self.File.Edit(self.dictionary["Type"]["Folders"]["per_game_type"]["entry_list"], self.dictionary["Entry"]["Name"]["Normal"], "a")

	def Create_Entry_File(self):
		# Number: [entry number]
		# Type number: [Type number]
		# 
		# Title:
		# [Title]
		# 
		# Type:
		# [Type]
		#
		# Times:
		# [Entry times]
		# 
		# Session duration:
		# [Session duration]
		# 
		# File name:
		# [Number. Type (Time)]

		# Define the entry file
		folder = self.dictionary["Type"]["Folders"]["per_game_type"]["files"]["root"]
		file = folder + self.dictionary["Entry"]["Name"]["Sanitized"] + ".txt"
		self.File.Create(file)

		self.dictionary["Entry"]["Text"] = {
			"General": self.Define_File_Text("General")
		}

		for language in self.languages["small"]:
			self.dictionary["Entry"]["Text"][language] = self.Define_File_Text(language)

		# Write the entry text into the entry file
		self.File.Edit(file, self.dictionary["Entry"]["Text"]["General"], "w")

		# Write the entry text into the "Played" entry file
		file = self.game["folders"]["played"]["files"]["root"] + self.dictionary["Entry"]["Name"]["Sanitized"] + ".txt"

		self.File.Create(file)
		self.File.Edit(file, self.dictionary["Entry"]["Text"][self.user_language], "w")

	def Define_File_Text(self, language_parameter = None):
		if language_parameter != "General":
			language = language_parameter

		if language_parameter == "General":
			language = self.user_language

		full_language = self.languages["full"][language]

		# Define entry text lines
		lines = [
			self.JSON.Language.texts["number, title()"][language] + ": " + str(self.dictionaries["Sessions"]["Numbers"]["Total"]),
			self.JSON.Language.texts["type_number"][language] + ": " + str(self.dictionaries["Game type"][self.game_type]["Numbers"]["Total"])
		]

		# Add entry title lines
		if language_parameter != "General":
			text = self.JSON.Language.texts["title, title()"][language]

		if language_parameter == "General":
			text = self.JSON.Language.texts["titles, title()"][language]

		lines.append("\n" + text + ":" + "\n" + "{}")

		lines.extend([
			self.JSON.Language.texts["type, title()"][language] + ":" + "\n" + self.dictionary["Type"]["Type"][language] + "\n",
			self.Date.texts["times, title()"][language] + ":" + "\n" + "{}",
			self.JSON.Language.texts["session_duration"][language] + ":" + "\n" + "{}",
			self.JSON.Language.texts["entry, title()"][language] + ":" + "\n" + self.dictionary["Entry"]["Name"]["Normal"]
		])

		# Add states texts lines
		if self.dictionary["States"]["Texts"] != {}:
			text = "\n" + self.JSON.Language.texts["states, title()"][language] + ":" + "\n"

			for key in self.dictionary["States"]["Texts"]:
				language_text = self.dictionary["States"]["Texts"][key][language]

				text += language_text

				if key != list(self.dictionary["States"]["Texts"].keys())[-1]:
					text += "\n"

			lines.append(text)

		# Define items to be added to file text format
		items = []

		# Add entry titles to items list
		titles = []

		key = "Original"

		if "Romanized" in self.game["Titles"]:
			key = "Romanized"

		titles.append(self.game["Titles"][key])

		if self.game["Titles"]["Language"] != self.game["Titles"][key]:
			titles.append("\n" + self.game["Titles"]["Language"])

		i = 0
		for line in lines:
			if self.JSON.Language.texts["titles, title()"][language] in line:
				line = line.replace(self.JSON.Language.texts["titles, title()"][language], self.JSON.Language.texts["title, title()"][language])

				lines[i] = line

			i += 1

		items.append(self.Text.From_List(titles) + "\n")

		# Add times to items list
		times = ""

		for key in ["UTC", "Timezone"]:
			time = self.dictionary["Entry"]["Times"][key]

			times += time + "\n"

		items.append(times)

		# Add session duration to items list
		session_duration = self.dictionary["Entry"]["Session duration"]["Text"][language] + "\n"

		if language_parameter != "General":
			session_duration = self.dictionary["Entry"]["Session duration"]["Text"][language] + "\n"

		if language_parameter == "General":
			session_duration = ""

			for language in self.languages["small"]:
				text = self.dictionary["Entry"]["Session duration"]["Text"][language] + "\n"

				if text not in session_duration:
					session_duration += text

		items.append(session_duration)

		# Define language entry text
		file_text = self.Text.From_List(lines)

		return file_text.format(*items)

	def Add_Entry_File_To_Year_Folder(self):
		# Create folders
		for language in self.languages["small"]:
			full_language = self.languages["full"][language]

			# Folder names
			root_folder = self.texts["game_sessions"][language]
			type_folder = self.dictionary["Type"]["Type"][language]

			# Entries folder
			folder = self.current_year["folders"][full_language]["root"]

			self.current_year["folders"][full_language][root_folder] = {
				"root": folder + root_folder + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][root_folder]["root"])

			# Game type folder
			folder = self.current_year["folders"][full_language][root_folder]["root"]

			self.current_year["folders"][full_language][root_folder][type_folder] = {
				"root": folder + type_folder + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][root_folder][type_folder]["root"])

			# Session file
			folder = self.current_year["folders"][full_language][root_folder][type_folder]["root"]
			file_name = self.dictionary["Entry"]["Name"]["Sanitized"]
			self.current_year["folders"][full_language][root_folder][type_folder][file_name] = folder + file_name + ".txt"

			self.File.Create(self.current_year["folders"][full_language][root_folder][type_folder][file_name])

			self.File.Edit(self.current_year["folders"][full_language][root_folder][type_folder][file_name], self.dictionary["Entry"]["Text"][language], "w")

			# Firsts Of The Year subfolder folder
			firsts_of_the_year_text = self.JSON.Language.texts["firsts_of_the_year"][language]
			subfolder_name = self.texts["game_sessions"][language]

			folder = self.current_year["folders"][full_language][firsts_of_the_year_text]["root"]

			self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name] = {
				"root": folder + subfolder_name + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name]["root"])

			# Firsts Of The Year game type folder
			folder = self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name]["root"]
			type_folder = self.dictionary["Type"]["Type"][language]

			self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder] = {
				"root": folder + type_folder + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder]["root"])

			# First game type session in year file
			if self.game["States"]["First game type session in year"] == True:
				folder = self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder]["root"]

				self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name] = folder + file_name + ".txt"
				self.File.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name])

				self.File.Edit(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name], self.dictionary["Entry"]["Text"][language], "w")

	def Define_Diary_Slim_Text(self):
		items = [
			self.game_type,
			self.game["Titles"]["Language"],
			self.dictionary["Entry"]["Session duration"]["Text"][self.user_language]
		]

		template = self.language_texts["i_played_the_{}_game_called_{}_for_{}"] + "."

		self.dictionary["Entry"]["Diary Slim"]["Text"] = template.format(*items)

		self.dictionary["Entry"]["Diary Slim"]["Clean text"] = self.dictionary["Entry"]["Diary Slim"]["Text"]

		# If there are states, add the texts to the Diary Slim text
		if self.dictionary["States"]["States"] != {}:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.JSON.Language.language_texts["states, title()"] + ":" + "\n"

			for key in self.dictionary["States"]["Texts"]:
				self.dictionary["Entry"]["Diary Slim"]["Text"] += self.dictionary["States"]["Texts"][key][self.user_language]

				if key != list(self.dictionary["States"]["Texts"].keys())[-1]:
					self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n"

	def Post_On_Social_Networks(self):
		self.social_networks = [
			"WhatsApp",
			"Instagram",
			"Facebook",
			"Twitter",
		]

		self.social_networks_string = self.Text.From_List(self.social_networks, break_line = False, separator = ", ")
		self.first_three_social_networks = ""

		for social_network in self.social_networks:
			if social_network != self.social_networks[-1]:
				self.first_three_social_networks += social_network

				if social_network != "Facebook":
					self.first_three_social_networks += ", "

		self.twitter_social_network = self.social_networks[-1]

		self.posted_on_social_networks_text_template = self.language_texts["i_posted_the_text_of_the_played_game_and_a_screenshot_on_the_status_of_{}_and_tweet_on_{}"] + "."

		self.dictionary["Entry"]["Diary Slim"]["Posted on the Social Networks text"] = self.posted_on_social_networks_text_template.format(self.first_three_social_networks, self.twitter_social_network)

		text = self.language_texts["post_on_the_social_networks"] + " (" + self.social_networks_string + ")"

		self.dictionary["Entry"]["States"]["Post on the Social Networks"] = self.Input.Yes_Or_No(text)

		if self.dictionary["Entry"]["States"]["Post on the Social Networks"] == True:
			from Social_Networks.Open_Social_Network import Open_Social_Network as Open_Social_Network

			Open_Social_Network(option_info = {"type": "profile"}, social_network_parameter = "WhatsApp", first_space = False, second_space = False)

			self.Input.Type(self.language_texts["press_enter_to_copy_the_text_of_the_played_game"])

			self.Text.Copy(self.dictionary["Entry"]["Times"]["Timezone"] + ":\n" + self.dictionary["Entry"]["Diary Slim"]["Clean text"])

		print()
		print("-----")
		print()

	def Write_On_Diary_Slim(self):
		# Add "Posted on Social Networks" text if the user wanted to post the entry text on the Social Networks
		if self.dictionary["Entry"]["States"]["Post on the Social Networks"] == True:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.dictionary["Entry"]["Diary Slim"]["Posted on the Social Networks text"]

		from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

		Write_On_Diary_Slim_Module(self.dictionary["Entry"]["Diary Slim"]["Text"], self.dictionary["Entry"]["Times"]["Timezone"], add_dot = False)