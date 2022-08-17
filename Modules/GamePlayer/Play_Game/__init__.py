# Play_Game.py

from Script_Helper import *

from GamePlayer.GamePlayer import GamePlayer as GamePlayer

from GamePlayer.Register_Played_Time import Register_Played_Time as Register_Played_Time

class Play_Game(GamePlayer):
	def __init__(self):
		super().__init__()

		self.Choose_Game()
		self.Open_Game()

		self.start_counting_time = Yes_Or_No_Definer(Language_Item_Definer("Start counting time", "Começar a contar o tempo"))

		if self.start_counting_time == False:
			i = 0
			while self.start_counting_time == False:
				text = Language_Item_Definer("Start counting time (Answer: No", "Começar a contar o tempo (Resposta: Não") + " {}x)".format(i)
				self.start_counting_time = Yes_Or_No_Definer(text, first_space = False)

				i += 1

		print("-----")

		try:
			self.Count_Played_Time()

		except KeyboardInterrupt:
			Remove_File(self.played_time_backup_file)

			self.texts_to_use = {
			"Games": self.choosen_game,
			"Number": int(Create_Array_Of_File(self.game_played_time_files["Number"])[0]) + 1,
			"Game Types": self.game_type,
			"Times": time.strftime("%H:%M %d/%m/%Y"),
			"Time Spent": self.array_to_use[full_language_en] + " - " + self.array_to_use[full_language_pt],
			"Played Time " + full_language_en: self.playing_texts[full_language_en]["played_the_game_for"].format(self.game_genre, self.choosen_game, self.array_to_use[full_language_en], self.now_time),
			"Played Time " + full_language_pt: self.playing_texts[full_language_pt]["played_the_game_for"].format(self.game_genre, self.choosen_game, self.array_to_use[full_language_pt], self.now_time),
			}

			self.when_played = self.texts_to_use["Times"]
			self.time_spent = self.texts_to_use["Time Spent"]

			self.variables_dict = {
			"game_files_folder": self.game_files_folder,
			"media_type_files_folder": self.media_type_files_folder,
			"media_type_folders_folder": self.media_type_folders_folder,
			"choosen_game": self.choosen_game,
			"game_type": self.game_type,
			"game_genre": self.game_genre,
			"game_name": self.choosen_game,
			"array_to_use": self.array_to_use,
			}

			Register_Played_Time(self.texts_to_use, self.variables_dict)

	def Choose_Game(self):
		self.add_more_folders_text = "[" + self.game_folder_texts_language["add_game_shortcut_folder"] + "]"
		self.game_folder_names.append(self.add_more_folders_text)
		self.game_folders.append(self.add_more_folders_text)

		self.games_text = Define_Text_By_Number(self.all_games_number, self.singular_games_text, self.plural_games_text)

		self.choice_text = self.game_folder_texts_language["select_folder_to_list"] + " ({} ".format(str(self.all_games_number)) + self.games_text + ")"
		self.selected_folder = Select_Choice_From_List(self.game_folder_names, local_script_name, self.choice_text, second_choices_list = self.game_folders, add_none = True, return_second_item_parameter = True, return_first_and_second_item = True, return_number = True, second_space = False)

		self.game_type = self.selected_folder[0].split(" (")[0].replace(" - ", ", ")
		self.game_genre = self.game_type

		if ", " in self.game_genre:
			self.game_genre = self.game_genre.split(", ")[Language_Item_Definer(0, 1)]

		self.choosen_game_folder = self.selected_folder[1]

		self.media_type_files_folder = self.per_media_type_files_folder + self.game_type + "/"
		Create_Folder(self.media_type_files_folder, self.global_switches["create_folders"])

		self.media_type_folders_folder = self.per_media_type_folders_folder + self.game_type + "/"
		Create_Folder(self.media_type_folders_folder, self.global_switches["create_folders"])

		if self.selected_folder[0] == self.add_more_folders_text:
			self.game_folder_names.pop(-1)
			self.game_folders.pop(-1)

			Add_New_Game_Folder()

			self.game_folder_names.append(self.add_more_folders_text)
			self.game_folders.append(self.add_more_folders_text)

			self.selected_folder = Select_Choice_From_List(game_folder_names, local_script_name, self.choice_text, second_choices_list = game_folders, add_none = True, return_second_item_parameter = True, return_first_and_second_item = True, return_number = True, second_space = False)

		self.game_folder = self.selected_folder[1]

		self.current_game_names = List_Filenames(self.game_folder, add_none = False)
		self.current_game_files = List_Files(self.game_folder, add_none = False)

		if len(self.current_game_names) != 0:
			self.game_names_dict[self.game_folder] = self.current_game_names

			Add_To_Dict_With_Key(self.game_files_names_dict, self.current_game_names, self.current_game_files)

		self.game_list_to_use = self.game_names_dict[self.game_folder], ""

		if self.has_multiple_game_folders == False:
			self.game_list_to_use = self.game_names, self.game_files

		self.game_names = self.game_list_to_use[0]

		self.choice_text = self.global_texts_language["select_game_from_list"]

		self.choice_info = Select_Choice_From_List(self.game_names, local_script_name, self.choice_text, second_choices_list = self.game_names, add_none = True, return_second_item_parameter = True, return_first_and_second_item = True, return_number = True)
		self.choosen_game = self.choice_info[0]
		self.choosen_game_file = self.game_files_names_dict[self.choosen_game]
		self.python_game_module_link = self.game_script_shortcuts_folder + self.choosen_game + self.dot_lnk

		print("-----")
		print()
		print(self.global_texts_language["opening_this_game"] + ":")
		print(self.choosen_game)
		print()
		print(self.global_texts_language["opening_this_game_file"] + ":")
		print(self.choosen_game_file)
		print()
		print(self.global_texts_language["in_this_game_folder"] + ":")
		print(self.choosen_game_folder)
		print()
		print(self.global_texts_language["game_genre"] + ":")
		print(self.game_genre)
		print()
		print("-----")

	def Open_Game(self):
		if self.global_switches["open_game"] == True:
			if is_a_file(self.python_game_module_link) == True:
				self.Choose_Function_To_Open_Game(self.python_game_module_link)
				print()
				input(Language_Item_Definer("Press Enter when you finish using the Python Game Module", "Pressione Enter quando você terminar de usar o Módulo de Python do Jogo") + ": ")

			self.Choose_Function_To_Open_Game(self.choosen_game_file)

	def Choose_Function_To_Open_Game(self, choosen_game_file):
		self.extension_functions = {
		"url": Open_Link,
		"lnk": Open_Link,
		"exe": Open_File,
		"bat": Open_File,
		}

		self.alternative_extension_functions = {
		"zip": "",
		"n64": "",
		"z64": "",
		"swf": "",
		"smc": "",
		}

		self.extension_found = False

		for extension in self.extensions_dict.values():
			replaced_extension = extension.replace(".", "")

			if replaced_extension in choosen_game_file or replaced_extension.upper() in choosen_game_file:
				if replaced_extension in self.extension_functions:
					self.extension_functions[replaced_extension](choosen_game_file)

					self.extension_found = True

		if self.extension_found == False:
			for extension in self.alternative_extension_functions:
				if extension in self.choosen_game_file:
					if extension == "n64" or extension == "N64":
						Open_File_With_Program(project_64, self.choosen_game_file)

					if extension == "zip" or extension == "smc":
						Open_File_With_Program(snes9x, self.choosen_game_file)

					if extension == "swf":
						Open_File_With_Program(adobe_flash_player, self.choosen_game_file)

	def Count_Played_Time(self):
		self.played_time_backup_file = self.current_year_played_folder + "Played Time Backup" + self.dot_text
		Create_Text_File(self.played_time_backup_file, self.global_switches["create_files"])

		self.has_hours = False

		self.played_times = {}

		self.hours = 0
		self.minutes = 0

		if self.global_switches["testing_script"] == True:
			self.time_to_wait = 1

		else:
			self.time_to_wait = 60

		while self.hours <= 54000:
			self.now_time = time.strftime("%H:%M %d/%m/%Y")

			self.minutes_array = Define_Text_By_Number(self.minutes, 
			{full_language_en: self.time_texts[full_language_en]["minute"], full_language_pt: self.time_texts[full_language_pt]["minute"]},
			{full_language_en: self.time_texts[full_language_en]["minutes"], full_language_pt: self.time_texts[full_language_pt]["minutes"]})

			if self.hours <= 1:
				self.hours_array = {
				full_language_en: self.time_texts[full_language_en]["hour"],
				full_language_pt: self.time_texts[full_language_pt]["hour"],
				}

			if self.hours > 2:
				self.hours_array = {
				full_language_en: self.time_texts[full_language_en]["hours"],
				full_language_pt: self.time_texts[full_language_pt]["hours"],
				}

			self.hours_text = str(self.hours)

			if self.hours == 0:
				self.hours_text = "0"

			self.minutes_text = str(self.minutes)

			if self.minutes == 0:
				self.minutes_text = "00"

			self.time_text = {}

			self.time_text[full_language_en] = Make_Time_Text(self.hours_text + ":" + self.minutes_text + ":00", full_language_en, add_original_time = False)
			self.time_text[full_language_pt] = Make_Time_Text(self.hours_text + ":" + self.minutes_text + ":00", full_language_pt, add_original_time = False)

			self.has_minutes = False

			if self.hours > 0:
				self.hours_texts = {}

				for language in full_languages_not_none:
					self.hours_texts[language] = self.time_text[language]

				self.array_to_use = self.hours_texts

				self.has_minutes = True
				self.has_hours = True

			else:
				if self.minutes != 0:
					self.minutes_texts = {}

					for language in full_languages_not_none:
						self.minutes_texts[language] = self.time_text[language]

					self.array_to_use = self.minutes_texts

					self.has_minutes = True

			if self.has_minutes == True:
				self.played_time = self.playing_texts_language["playing_the_game_for"].format(self.game_genre, self.choosen_game, self.array_to_use[Language_Item_Definer(full_language_en, full_language_pt)], self.now_time)

				for language in full_languages_not_none:
					self.played_times[language] = self.playing_texts[language]["playing_the_game_for"].format(self.game_genre, self.choosen_game, self.array_to_use[language], self.now_time)

				print()
				print(self.played_time)

			if self.global_switches["verbose"] == True:
				print(self.minutes, self.hours)

			if self.minutes == 60:
				self.minutes = 0
				self.hours += 1

			if self.has_minutes == True:
				text_to_write = self.played_time + "\n" + self.played_times[full_language_en] + "\n" + self.played_times[full_language_pt] + "\n"

				if self.has_hours == True:
					text_to_write += str(self.hours_texts[full_language_en]) + "\n" + str(self.hours_texts[full_language_pt])

				if self.has_hours == False:
					text_to_write += str(self.minutes_texts[full_language_en]) + "\n" + str(self.minutes_texts[full_language_pt])

				Write_To_File(self.played_time_backup_file, text_to_write, self.global_switches)

			self.minutes += 1

			time.sleep(self.time_to_wait)