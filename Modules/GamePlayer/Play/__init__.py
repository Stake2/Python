# Play.py

from GamePlayer.GamePlayer import GamePlayer as GamePlayer

from GamePlayer.Register_Playing_Time import Register_Playing_Time as Register_Playing_Time

class Play(GamePlayer):
	def __init__(self):
		super().__init__()

		self.Choose_Game()

		self.Define_Game_Dictionary()
		self.Show_Game_Information(self.game_dictionary)
		self.Open_Game()

		self.start_counting_time = False

		if self.start_counting_time == False:
			i = 0
			while self.start_counting_time == False:
				self.start_counting_time = self.Input.Yes_Or_No(self.language_texts["start_counting_playing_time"])

				i += 1

		print()
		print("-----")

		try:
			self.Count()

		except KeyboardInterrupt:
			self.File.Delete(self.played_time_backup_file)

			self.game_dictionary["texts"] = {
				"Games": self.game["name"],
				"Number": int(self.File.Contents(self.game_played_files["Number"])["lines"][0]) + 1,
				"Game categories": self.game["category"]["name"],
				"Times": self.Date.Now()["%H:%M %d/%m/%Y"],
				"Time spent": self.game_dictionary["time_list"]["en"] + " - " + self.game_dictionary["time_list"]["pt"],
			}

			for language in self.small_languages:
				translated_language = self.translated_languages[language]["en"]
				text = self.texts["i_played_the_{}_game_called_{}_for_{}_current_time_{}"][language]

				self.game_dictionary["texts"][translated_language + " played time"] = text.format(self.game["category"]["names"][language], self.game["name"], self.game_dictionary["time_list"][language], self.now_time)

			Register_Playing_Time(self.game_dictionary)

	def Choose_Game(self):
		# Select a game folder
		if len(self.games["folder"]["list"]) != 1:
			show_text = self.language_texts["game_folders"]
			select_text = self.language_texts["select_a_game_folder"]

			self.option_info = self.Input.Select(self.games["folder"]["list"], language_options = self.games["folder"]["list_with_numbers"], show_text = show_text, select_text = select_text)

		if len(self.games["folder"]["list"]) == 1:
			self.option_info = {
				"option": self.games["folder"]["list"][0],
				"number": 0,
			}

		self.game = {
			"category": {
				"name": self.games["folder"]["names"][self.option_info["number"]],
			}
		}

		self.game["category"]["names"] = {}

		for language in self.small_languages:
			self.game["category"]["names"][language] = self.games["Folder names"][language][self.option_info["number"]]

		self.game["category"]["folder"] = self.option_info["option"]

		dict_ = self.games["files"][self.game["category"]["name"]]

		self.game["category"]["file"] = {
			"list": dict_["list"],
			"names": dict_["names"],
		}

		# Define media type files folder and folders folder
		self.game["category"]["media_type_files_folder"] = self.per_media_type_files_folder + self.game["category"]["name"] + "/"
		self.Folder.Create(self.game["category"]["media_type_files_folder"])

		self.game["category"]["media_type_folders_folder"] = self.per_media_type_folders_folder + self.game["category"]["name"] + "/"
		self.Folder.Create(self.game["category"]["media_type_folders_folder"])

		# Select a game
		options = self.game["category"]["file"]["names"]
		show_text = self.language_texts["games, title()"]
		select_text = self.language_texts["select_a_game"]

		self.option_info = self.Input.Select(options, show_text = show_text, select_text = select_text)

		self.game["name"] = self.option_info["option"]
		self.game["sanitized_name"] = self.Sanitize(self.game["name"], restricted_characters = True)

		self.game["file"] = self.game["category"]["file"]["list"][self.option_info["number"]]

		if self.File.Exist(self.apps_folders["shortcuts"]["root"] + self.game["name"] + ".lnk") == True:
			self.game["python_module_link"] = self.apps_folders["shortcuts"]["root"] + self.game["name"] + ".lnk"

	def Define_Game_Dictionary(self):
		self.game_dictionary = {}
		self.game_dictionary["game"] = self.game
		self.game_dictionary["show_text"] = self.language_texts["opening_this_game"]

	def Open_Game(self):
		if self.global_switches["testing"] == False:
			if "python_module_link" in self.game:
				self.File.Open(self.game["python_module_link"])

				self.Input.Type(self.language_texts["press_enter_when_you_finish_using_the_python_module_of_the_game"])

			self.File.Open(self.game["file"])

	def Count(self):
		self.played_time_backup_file = self.current_year_played_folder + "Played time backup.txt"
		self.File.Create(self.played_time_backup_file)

		self.has_hours = False

		self.hours = 0
		self.hour_texts = {}

		self.minutes = 0

		self.time_to_wait = 59

		self.game_dictionary["played_texts"] = {}

		if self.global_switches["testing"] == True:
			self.time_to_wait = 0.1

		while self.hours <= 54000:
			self.now_time = self.Date.Now()["%H:%M %d/%m/%Y"]

			self.hours_text = str(self.hours)

			if self.hours == 0:
				self.hours_text = "0"

			self.minutes_text = str(self.minutes)

			if self.minutes == 0:
				self.minutes_text = "00"

			self.time_text = {}

			for language in self.small_languages:
				self.time_text[language] = self.Date.Time_Text(self.hours_text + ":" + self.minutes_text, language, add_original_time = False)

			self.has_minutes = False

			if self.hours > 0:
				for language in self.small_languages:
					self.hour_texts[language] = self.time_text[language]

				self.game_dictionary["time_list"] = self.hour_texts

				self.has_minutes = True
				self.has_hours = True

			if self.hours == 0 and self.minutes != 0:
				self.minute_texts = {}

				for language in self.small_languages:
					self.minute_texts[language] = self.time_text[language]

				self.game_dictionary["time_list"] = self.minute_texts

				self.has_minutes = True

			if self.has_minutes == True:
				for language in self.small_languages:
					self.game_dictionary["played_texts"][language] = self.texts["i_am_playing_the_{}_game_called_{}_for_{}_current_time_{}"][language].format(self.game["category"]["names"][language], self.game["name"], self.game_dictionary["time_list"][language], self.now_time)

				print()
				print(self.game_dictionary["played_texts"][self.user_language])

			if self.minutes == 59:
				self.minutes = 0
				self.hours += 1

			if self.has_minutes == True:
				text_to_write = self.game_dictionary["played_texts"][self.user_language] + "\n"

				for language in self.small_languages:
					if language != self.user_language:
						text_to_write += self.game_dictionary["played_texts"][language]

						if language != self.small_languages[-1]:
							text_to_write += "\n"

				text_to_write += "\n\n"

				if self.has_hours == True:
					for language in self.small_languages:
						text_to_write += str(self.hour_texts[language])

						if language != self.small_languages[-1]:
							text_to_write += "\n"

					text_to_write += "\n\n"

				for language in self.small_languages:
					text_to_write += str(self.minute_texts[language])

					if language != self.small_languages[-1]:
						text_to_write += "\n"

				self.File.Edit(self.played_time_backup_file, text_to_write, "w")

			self.minutes += 1

			self.Date.Sleep(self.time_to_wait)