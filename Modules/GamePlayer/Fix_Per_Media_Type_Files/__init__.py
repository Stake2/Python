# Fix_Per_Media_Type_Files.py

from Script_Helper import *

from GamePlayer.GamePlayer import GamePlayer as GamePlayer

class Fix_Per_Media_Type_Files(GamePlayer):
	def __init__(self):
		super().__init__()

		for game_type in Create_Array_Of_File(self.game_types_file):
			self.media_type_files_folder = self.per_media_type_files_folder + game_type + "/"
			self.media_type_folders_folder = self.per_media_type_folders_folder + game_type + "/"
			self.all_files_folder = self.media_type_folders_folder + "All Files/"

			self.games_file = self.media_type_files_folder + "Games" + self.dot_text
			self.times_file = self.media_type_files_folder + "Times" + self.dot_text

			Create_Text_File(self.games_file, self.global_switches)
			Create_Text_File(self.times_file, self.global_switches)

			self.games = Create_Array_Of_File(self.games_file)
			self.times = Create_Array_Of_File(self.times_file)

			i = 0
			for game in self.games:
				time = self.times[i]
				replaced_time = time.replace(":", ";").replace("/", "-")

				self.all_files_file = self.all_files_folder + Remove_Non_File_Characters(game) + " " + replaced_time + self.dot_text
				Create_Text_File(self.all_files_file, self.global_switches)

				self.game_folder = self.media_type_folders_folder + Remove_Non_File_Characters(game) + "/"
				self.game_folder_file = self.game_folder + replaced_time + self.dot_text
				Create_Text_File(self.game_folder_file, self.global_switches)

				print()
				print(game)
				print(time)
				print(Remove_Non_File_Characters(game) + " " + replaced_time)
				print(i)

				file_text = Create_Array_Of_File(self.all_files_file)
				file_text[3] = str(i + 1)

				print()
				print("---")
				print(Create_Array_Of_File(self.all_files_file))
				print(file_text)
				print("---")

				text_to_write = Stringfy_Array(file_text, add_line_break = True)
				Write_To_File(self.all_files_file, text_to_write, self.global_switches)
				Write_To_File(self.game_folder_file, text_to_write, self.global_switches)

				i += 1