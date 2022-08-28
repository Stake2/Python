# Fill_Play_History_Files.py

from Script_Helper import *

from GamePlayer.GamePlayer import GamePlayer as GamePlayer

class Fill_Play_History_Files(GamePlayer):
	def __init__(self):
		super().__init__()

		self.verbose = True

		self.second_played_folder = self.play_history_folder + "Second Played/"
		self.second_played_folder_current_year = self.second_played_folder + str(current_year) + "/"

		self.game_played_times_file = self.second_played_folder_current_year + "Tempo de Jogatina dos Jogos" + self.dot_text
		self.game_types_file = self.second_played_folder_current_year + "Game Types" + self.dot_text

		self.game_played_times = Create_Array_Of_File(self.game_played_times_file)
		self.game_types = Create_Array_Of_File(self.game_types_file)

		self.game_names = []
		self.played_times = []
		self.when_played_times = []

		self.game_type_numbers = {}

		self.number_counter = 0
		for played_time in self.game_played_times:
			self.game_type = self.game_types[self.number_counter]

			self.game_type_numbers[self.game_type] = 0

			self.number_counter += 1

		self.number_counter = 0
		for played_time in self.game_played_times:
			self.game_type = self.game_types[self.number_counter]

			self.game_type_numbers[self.game_type] += 1

			self.number_counter += 1

		self.number_of_games_played = 1
		self.number_counter = 0
		for played_time in self.game_played_times:
			self.game_name = played_time.split("\"")[1].split("\"")[0]
			self.game_type = self.game_types[self.number_counter]
			self.played_time = played_time.split(" por ")[1].split(", ")[0]
			self.played_time = self.played_time.replace("horas", "hours").replace("minutos", "minutes").replace("segundos", "seconds") + " - " + self.played_time
			self.when_played = played_time.split("horário atual: ")[1]

			self.game_type_number = self.game_type_numbers[self.game_type]

			self.game_names.append(self.game_name)
			self.played_times.append(self.played_time)
			self.when_played_times.append(self.when_played)

			# Write to root text files

			self.texts_to_use = {
			"Games": self.game_name,
			"Number": str(self.number_of_games_played),
			"Game Types": self.game_type,
			"Times": self.when_played,
			"Time Spent": self.played_time,
			"Played Time " + full_language_en: self.playing_texts[full_language_en]["played_the_game_for"].format(self.game_name, self.played_time.split(" - ")[0].replace(" e ", " and "), self.when_played),
			"Played Time " + full_language_pt: self.playing_texts[full_language_pt]["played_the_game_for"].format(self.game_name, self.played_time.split(" - ")[1], self.when_played),
			}

			self.functions_to_use = {}

			for text in self.texts_to_use:
				self.functions_to_use[text] = Append_To_File

				if text == "Number":
					self.functions_to_use[text] = Write_To_File

			print("\n---\n")

			for text in self.texts_to_use:
				file = self.game_played_time_files[text]
				text_to_use = str(self.texts_to_use[text])

				Write_Function = self.functions_to_use[text]

				if Write_Function == Write_To_File:
					Write_Function(file, text_to_use, self.global_switches)

				if Write_Function == Append_To_File:
					Write_Function(file, text_to_use, self.global_switches, check_file_length = True)

				if self.global_switches["verbose"] == True:
					print(self.texts_to_use[text])
					print(file)
					print()

			self.media_type_files_folder = self.per_media_type_files_folder + self.game_type + "/"
			Create_Folder(self.media_type_files_folder, self.global_switches)

			self.media_type_folders_folder = self.per_media_type_folders_folder + self.game_type + "/"
			Create_Folder(self.media_type_folders_folder, self.global_switches)

			# Write to "Per Media Type/Game Files" text file

			self.game_files_file = self.game_files_folder + Remove_Non_File_Characters(self.game_name) + self.dot_text
			Create_Text_File(self.game_files_file, self.global_switches)

			text_to_append = played_time.replace("o jogo \"" + self.game_name + "\" ", "")
			Append_To_File(self.game_files_file, text_to_append, self.global_switches, check_file_length = True)

			if self.global_switches["verbose"] == True:
				print(text_to_append)
				print(self.game_files_file)

			# Write to "Per Media Type/Files" text files

			Append_To_File(self.media_type_files_folder + "Games" + self.dot_text, self.game_name, self.global_switches, check_file_length = True)
			Append_To_File(self.media_type_files_folder + "Times" + self.dot_text, self.when_played, self.global_switches, check_file_length = True)
			Append_To_File(self.media_type_files_folder + "Time Spent" + self.dot_text, self.played_time, self.global_switches, check_file_length = True)

			text_to_write = str(self.game_type_number)
			Write_To_File(self.media_type_files_folder + "Number" + self.dot_text, text_to_write, self.global_switches)

			if self.global_switches["verbose"] == True:
				print()
				print(self.game_name)
				print(self.media_type_files_folder + "Games" + self.dot_text)

				print()
				print(self.when_played)
				print(self.media_type_files_folder + "Times" + self.dot_text)

				print()
				print(self.played_time)
				print(self.media_type_files_folder + "Time Spent" + self.dot_text)

				print()
				print(text_to_write)
				print(self.media_type_files_folder + "Number" + self.dot_text)

			# Create text files in "All Played Files" folder

			self.played_game_file_name = self.when_played.replace(":", ";").replace("/", "-")

			self.all_played_files_file = self.all_played_files_folder + str(self.number_of_games_played) + " " + Remove_Non_File_Characters(self.game_name) + self.dot_text
			Create_Text_File(self.all_played_files_file, self.global_switches)

			text_to_write = self.game_name + "\n" + self.game_type + "\n" + self.when_played + "\n" + self.played_time + "\n" + str(self.number_of_games_played)
			Write_To_File(self.all_played_files_file, text_to_write, self.global_switches)

			if self.global_switches["verbose"] == True:
				print()
				print(text_to_write)
				print(self.all_played_files_file)

			# Create text files in "Per Media Type/Folders" folders

			self.all_files_folder = self.media_type_folders_folder + "All Files/"
			Create_Folder(self.all_files_folder, self.global_switches)

			self.game_media_type_folder = self.media_type_folders_folder + Remove_Non_File_Characters(self.game_name) + "/"
			Create_Folder(self.game_media_type_folder, self.global_switches)

			self.all_files_file = self.all_files_folder + Remove_Non_File_Characters(self.game_name) + " " + self.played_game_file_name + self.dot_text
			Create_Text_File(self.all_files_file, self.global_switches)

			self.game_folder_file = self.game_media_type_folder + self.played_game_file_name + self.dot_text
			Create_Text_File(self.game_folder_file, self.global_switches)

			text_to_write = self.game_name + "\n" + self.when_played + "\n" + self.played_time + "\n" + str(self.game_type_number)
			Write_To_File(self.all_files_file, text_to_write, self.global_switches)

			if self.global_switches["verbose"] == True:
				print()
				print(text_to_write)
				print(self.all_files_file)

			Write_To_File(self.game_folder_file, text_to_write, self.global_switches)

			if self.global_switches["verbose"] == True:
				print()
				print(text_to_write)
				print(self.game_folder_file)

			# ---------- #

			self.number_of_games_played += 1
			self.number_counter += 1