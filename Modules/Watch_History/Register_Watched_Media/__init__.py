# Register_Watched_Media.py

# Script Helper importer
from Script_Helper import *

from Watch_History.Watch_History import Watch_History as Watch_History
from Watch_History.Media_Manager import Select_Media_Type as Select_Media_Type

from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

from Block_Websites.Unblock import Unblock as Unblock

import re

# Class to register watched media
class Register_Watched_Media(Watch_History):
	def __init__(self, run_as_module = False, media_dict = None):
		super().__init__()

		self.run_as_module = run_as_module
		self.media_dict = media_dict

		if self.run_as_module == False:
			self.Ask_For_Media_Info()

		self.Define_Media_Variables()

		self.Define_Diary_Slim_Watched_Text()
		self.Ask_For_Food_And_Drink()

		self.Add_To_Watched_Numbers()

		self.Add_Watched_Media_To_Text_Files()
		self.Create_Watched_Media_Text_Files()

		self.Check_First_Watched_In_Year()

		self.Fetch_Next_Episode()

		self.Post_On_Social_Networks()

		self.Write_On_Diary_Slim()

		if self.global_switches["verbose"] == True:
			print()
			print(self.large_bar)
			print()
			print("Register_Watched_Media:")

		self.Show_Watched_Media_Info()

	def Ask_For_Media_Info(self):
		# To-Do: Make this method

		self.media_dict = {}

	def Define_Media_Variables(self):
		self.media_title = self.media_dict["media_title"]
		self.media_title_file_safe = self.media_dict["media_title_file_safe"]

		self.portuguese_media_title = self.media_dict["portuguese_media_title"]

		self.language_media_title = Language_Item_Definer(self.media_title, self.portuguese_media_title)

		self.media_folder = self.media_dict["media_folder"]
		self.media_details = self.media_dict["media_details"]
		self.media_details_file = self.media_dict["media_details_file"]

		self.media_episode_titles = self.media_dict["media_episode_titles"]

		self.media_episode = self.media_dict["media_episode"]
		self.media_episode_file_safe = self.media_dict["media_episode_file_safe"]

		self.started_watching_time = self.media_dict["started_watching_time"]
		self.finished_watching_time = self.media_dict["finished_watching_time"]

		self.english_media_type = self.media_dict["english_media_type"]
		self.portuguese_media_type = self.media_dict["portuguese_media_type"]
		self.mixed_media_type = self.media_dict["mixed_media_type"]
		self.language_singular_media_type = self.media_dict["language_singular_media_type"]

		self.origin_type = self.media_dict["origin_type"]

		self.per_media_type_files_folder = self.media_dict["per_media_type_files_folder"]
		self.per_media_type_episodes_file = self.media_dict["per_media_type_episodes_file"]
		self.per_media_type_times_file = self.media_dict["per_media_type_times_file"]

		self.is_remote = self.media_dict["is_remote"]
		self.is_local = self.media_dict["is_local"]
		self.is_hybrid = self.media_dict["is_hybrid"]

		self.is_series_media = self.media_dict["is_series_media"]
		self.is_video_series_media = self.media_dict["is_video_series_media"]

		if self.is_series_media == True:
			self.media_episode_number = self.media_dict["media_episode_number"]

		self.re_watching = self.media_dict["re_watching"]

		self.no_media_list = self.media_dict["no_media_list"]

		self.media_item = self.media_dict["media_item"]
		self.media_item_file_safe = self.media_dict["media_item_file_safe"]
		self.media_item_episode = self.media_dict["media_item_episode"]
		self.media_item_episode_with_title = self.media_dict["media_item_episode_with_title"]
		self.media_item_folder = self.media_dict["media_item_folder"]
		self.current_media_item_file = self.media_dict["current_media_item_file"]

		if self.no_media_list == False:
			self.media_item_details = self.media_dict["media_item_details"]
			self.media_item_details_file = self.media_dict["media_item_details_file"]
			self.media_list_item_names = self.media_dict["media_list_item_names"]

		self.youtube_video_id = ""

		if self.is_video_series_media == True:
			self.youtube_video_id = self.media_dict["youtube_video_id"]

		if self.english_media_type == self.anime_media_type_english_plural and "dubbed_media_text" in self.media_dict:
			self.dubbed_media_text = self.media_dict["dubbed_media_text"]

		if self.english_media_type == self.video_media_type_english_plural:
			self.is_video_series_media = True

		if self.is_series_media == True and self.is_video_series_media == True:
			self.youtube_ids_file = self.media_item_folder + self.youtube_ids_english_text + self.dot_text
			Create_Text_File(self.youtube_ids_file)

			text_to_append = self.youtube_video_id
			Append_To_File(self.youtube_ids_file, text_to_append, self.global_switches, check_file_length = True)

	def Define_Diary_Slim_Watched_Text(self):
		self.finished_watching_episode_text_template = 'Acabei de assistir {}'

		self.the_text = self.gender_the_texts[self.mixed_media_type]["the"]
		self.this_text = self.gender_the_texts[self.mixed_media_type]["this"]

		if self.is_series_media == True:
			self.finished_watching_episode_text_template += ' "{}"'

			self.watched_item_text = "esse episódio d" + self.the_text

			if self.re_watching == True:
				self.finished_watching_episode_text_template = self.finished_watching_episode_text_template.replace("assistir", "re-assistir")

			self.local_media_title = self.media_title

			if self.portuguese_media_title != None:
				self.local_media_title = self.portuguese_media_title

			if self.media_episode == self.media_episode_titles[-1]:
				self.watched_item_text = self.watched_item_text.replace("esse", "o último")

			self.watched_media_item_name = Language_Item_Definer("season", "da temporada")

			self.watched_media_container_type = self.language_singular_media_type.lower()

			if self.is_video_series_media == True:
				self.watched_media_item_name = Language_Item_Definer("of the " + self.youtube_name + " video series", "da série de vídeos do " + self.youtube_name)
				self.watched_media_container_type = Language_Item_Definer("channel", "canal")
				self.the_text = self.gender_the_texts[self.mixed_media_type]["feminine"]["the"]

			if self.no_media_list == False and self.media_item != self.media_title:
				self.watched_item_text = self.watched_item_text.replace("episódio", "episódio {}".format(self.watched_media_item_name + ' "{}"'.format(self.media_item)))

			if self.is_video_series_media == True:
				self.watched_media_item_name = Language_Item_Definer(self.youtube_name + " video series", "série de vídeos do " + self.youtube_name)

			self.watched_item_text += " " + self.watched_media_container_type

			self.finished_watching_episode_text = self.finished_watching_episode_text_template.format(self.watched_item_text, self.local_media_title)

		if self.is_series_media == False:
			self.finished_watching_episode_text = self.finished_watching_episode_text_template.format(self.this_text + " " + self.language_singular_media_type.lower())

		media_episode = self.media_episode

		for i in range(0, 11):
			media_episode = media_episode.replace("Rewatched {}x - ".format(i), "")

		if self.english_media_type == self.anime_media_type_english_plural and "dubbed_media_text" in self.media_dict:
			self.finished_watching_episode_text += dubbed_portuguese_text

		self.finished_watching_episode_text += ":\n" + media_episode

		self.finished_watching_episode_time_text = self.finished_watching_time + ":\n" + self.finished_watching_episode_text

	def Ask_For_Food_And_Drink(self):
		self.ask_for_food_and_drink = False

		self.food_and_drink_text = ""

		self.ate_food = False
		self.food = ""

		if self.ask_for_food_and_drink == True:
			self.ate_food = Yes_Or_No_Definer(Language_Item_Definer("Watched while eating", "Assistiu enquanto comia"), second_space = False)	

			if self.ate_food == True:
				self.food = Select_Choice(Language_Item_Definer("Type the food that you ate", "Digite a comida que você comeu"), second_space = False)

		self.drank_drink = False
		self.drink = ""

		if self.ask_for_food_and_drink == True:
			self.drank_drink = Yes_Or_No_Definer(Language_Item_Definer("Watched while drinking", "Assistiu enquanto bebia"), second_space = False)

			if self.drank_drink == True:
				self.drink = Select_Choice(Language_Item_Definer("Type the drink that you drank", "Digite a bebida que você bebeu"), second_space = False)

		if self.ate_food == True:
			self.food_and_drink_text += " enquanto comia " + self.food

		if self.ate_food == True and self.drank_drink == True:
			self.food_and_drink_text += " e "

		else:
			if self.drank_drink == True:
				self.food_and_drink_text += " enquanto "

		if self.drank_drink == True:
			self.food_and_drink_text += "bebia " + self.drink

		self.finished_watching_episode_text_with_food_and_drink = self.finished_watching_episode_text.replace('":', '"{}:')

		self.finished_watching_episode_text_with_food_and_drink = self.finished_watching_episode_text_with_food_and_drink.format(self.food_and_drink_text)

		if self.ate_food == True or self.drank_drink == True:
			self.ate_and_drank_text = ""

		if self.ate_food == True:
			self.ate_and_drank_text += "\n\n" + "Food - Comida" + ": " + self.food

		if self.ate_food == True and self.drank_drink == True:
			self.ate_and_drank_text += "\n"

		if self.drank_drink == True:
			if self.ate_food == False:
				self.ate_and_drank_text += "\n\n"

			self.ate_and_drank_text += "Drink - Bebida" + ": " + self.drink

	def Add_To_Watched_Numbers(self):
		self.media_type_watched_number_file = self.per_media_type_number_files[self.english_media_type]

		# Movies Folder (Appends)
			# Number.txt (Writes)

		# Current Year Watched Media Folder >

			# Per Media Type >
				# Files (Writes) > 
					# [Media Type] >
						# Number.txt

			# Writes:
				# Number.txt

		self.total_watched_number = Change_Number(Create_Array_Of_File(self.total_watched_number_current_year_file)[0], "more", 1)
		self.media_type_watched_number = Change_Number(Create_Array_Of_File(self.media_type_watched_number_file)[0], "more", 1)

		# Number.txt
		text_to_write = self.total_watched_number
		Write_To_File(self.total_watched_number_current_year_file, text_to_write, self.global_switches)

		# Files (Writes) > [Media Type] > Number.txt
		text_to_write = self.media_type_watched_number
		Write_To_File(self.media_type_watched_number_file, text_to_write, self.global_switches)

		self.watched_movie_number_file = self.movies_folder + self.number_english_text + self.dot_text

		if self.is_series_media == False:
			# Movies Folder (Appends) > Number.txt (Writes)
			text_to_write = Change_Number(Create_Array_Of_File(self.watched_movie_number_file)[0], "more", 1)
			Write_To_File(self.watched_movie_number_file, text_to_write, self.global_switches)

	def Add_Watched_Media_To_Text_Files(self):
		# Current Year Watched Media Folder >

			# Appends:
				# Episodes.txt
				# Media Types.txt
				# Times.txt
				# YouTude IDs.txt

		self.youtube_ids_file = self.current_year_watched_media_folder + self.youtube_ids_english_text + self.dot_text
		Create_Text_File(self.youtube_ids_file, self.global_switches)

		# Episodes.txt
		text_to_append = self.media_item_episode_with_title
		Append_To_File(self.watched_files[self.episodes_english_text], text_to_append, self.global_switches, check_file_length = True)

		# Media Types.txt
		text_to_append = self.mixed_media_type
		Append_To_File(self.watched_files[self.media_types_english_text], text_to_append, self.global_switches, check_file_length = True)

		# Times.txt
		text_to_append = self.finished_watching_time
		Append_To_File(self.watched_files[self.times_english_text], text_to_append, self.global_switches, check_file_length = True)

		# YouTube IDs.txt
		text_to_append = " "

		if self.is_video_series_media == True:
			text_to_append = self.youtube_video_id

		Append_To_File(self.youtube_ids_file, text_to_append, self.global_switches, check_file_length = True)

		# ------------------ #

		# Current Year Watched Media Folder >

			# Per Media Type >
				# Files (Appends) > 
					# [Media Type] >
						# Episodes.txt, Times.txt, YouTude IDs.txt

		# Files (Appends) > [Media Type] > Episodes.txt
		text_to_append = self.media_item_episode_with_title
		Append_To_File(self.per_media_type_episodes_file, text_to_append, self.global_switches, check_file_length = True)

		# Files (Appends) > [Media Type] > Times.txt
		text_to_append = self.finished_watching_time
		Append_To_File(self.per_media_type_times_file, text_to_append, self.global_switches, check_file_length = True)
		
		# Files (Appends) > [Media Type] > (YouTube IDs.txt)
		if self.is_video_series_media == True:
			self.youtube_ids_file = self.per_media_type_files_folder + self.youtube_ids_english_text + self.dot_text
			Create_Text_File(self.youtube_ids_file, self.global_switches)

			text_to_append = self.youtube_video_id
			Append_To_File(self.youtube_ids_file, text_to_append, self.global_switches, check_file_length = True)

		# ------------------ #

		# Movies Folder (Appends)
			# Names.txt
			# Times.txt

		if self.is_series_media == False:
			self.watched_movie_names_file = self.movies_folder + self.names_english_text + self.dot_text
			self.watched_movie_times_file = self.movies_folder + self.times_english_text + self.dot_text

			# Movies Folder (Appends) > Names.txt
			text_to_append = self.media_item_episode_with_title
			Append_To_File(self.watched_movie_names_file, text_to_append, self.global_switches, check_file_length = True)

			# Movies Folder (Appends) > Times.txt
			text_to_append = self.finished_watching_time
			Append_To_File(self.watched_movie_times_file, text_to_append, self.global_switches, check_file_length = True)

		# Movies Folder (Appends)
			# Names.txt
			# Number.txt (Writes)
			# Times.txt

		# Current Year Watched Media Folder >
			# All Watched Files (Creates) >
				# [Watched number]. [Media name] [Media episode title].txt
					# Contents:
					# [Full Media episode title]
					# [Watched time]
					# [Media type]

			# Per Media Type >
				# Files (Appends) > 
					# [Media Type] >
						# Episodes.txt, Times.txt, Number.txt

				# Folders >
					# [Media Type] (Creates) >
						# All Files >
							# [Media name] [Media episode title].txt
								# Contents:
								# [Full Media episode title]
								# [Watched time]

						# [Media name] >
							# [Media episode title without media name].txt
								# Contents:
								# [Full Media episode title]
								# [Watched time]

			# Appends:
				# Episodes.txt
				# Media Types.txt
				# Times.txt
				# Number.txt
				# YouTube IDs.txt

		# ------------------ #

		variable = ""

	def Create_Watched_Media_Text_Files(self):
		# Current Year Watched Media Folder >

			# All Watched Files (Creates) >
				# [Watched number]. [Media name] [Media episode title].txt
					# Contents:
						# [All watched number], [Media type watched number]
						# [Watched media name]
						# [Full Media episode title]
						#
						# [Watched media type]
						# [Mixed watched media type]
						#
						# [Watched time]
						# ([YouTube ID])

		self.media_item_episode_with_title_file = Remove_Non_File_Characters(self.media_item_episode_with_title)

		self.media_item_episode_with_title_file = re.sub(self.mixed_rewatched_regex_text, "", self.media_item_episode_with_title_file)

		# [Watched number]. [Media name] [Media episode title].txt
		self.current_episode_file = self.all_watched_files_current_year_folder + str(self.total_watched_number) + ". " + self.media_item_episode_with_title_file + self.dot_text

		Create_Text_File(self.current_episode_file, self.global_switches)

		self.full_watched_media_file_text = self.total_watched_number + ", " + self.media_type_watched_number + "\n\n"

		if self.is_series_media == True:
			self.full_watched_media_file_text += self.media_title + "\n"

		self.full_watched_media_file_text += self.media_item_episode_with_title + "\n\n" + self.language_singular_media_type + "\n" + self.mixed_media_type + "\n\n" + self.finished_watching_time

		if self.is_video_series_media == True:
			self.full_watched_media_file_text += "\n" + self.youtube_video_id

		if self.ate_food == True or self.drank_drink == True:
			self.full_watched_media_file_text += self.ate_and_drank_text

		Write_To_File(self.current_episode_file, self.full_watched_media_file_text, self.global_switches)

		# ------------------ #

		# Current Year Watched Media Folder >

			# Per Media Type >
				# Folders >
					# [Media Type] (Creates) >
						# [Media name] >
							# [Media episode title without media name].txt
								# [All watched number], [Media type watched number]
								# [Watched media name]
								# [Full Media episode title]
								#
								# [Watched media type]
								# [Mixed watched media type]
								#
								# [Watched time]
								# ([YouTube ID])

		self.per_media_type_folder = self.per_media_type_folder_folders_dict[self.english_media_type]

		self.watched_media_folder = self.per_media_type_folder + Remove_Non_File_Characters(self.media_title) + "/"
		Create_Folder(self.watched_media_folder, self.global_switches)

		if self.no_media_list == False:
			self.watched_media_folder = self.watched_media_folder + self.media_item_file_safe + "/"
			Create_Folder(self.watched_media_folder, self.global_switches)

		self.media_item_episode_file = Remove_Non_File_Characters(self.media_episode_file_safe)

		self.media_item_episode_file = re.sub(self.mixed_rewatched_regex_text, "", self.media_item_episode_file)

		# Per Media Type watched media name file
		self.per_media_type_media_episode_file = self.watched_media_folder

		if self.is_series_media == True:
			self.per_media_type_media_episode_file += self.media_item_episode_file

			if len(self.per_media_type_media_episode_file) > 255:
				while len(self.per_media_type_media_episode_file) > 255:
					self.per_media_type_media_episode_file = self.per_media_type_media_episode_file[:-1]

		if self.is_series_media == False:
			self.per_media_type_media_episode_file += "Movie - Filme"

		if " " in self.per_media_type_media_episode_file[-1]:
			self.per_media_type_media_episode_file[:-1]

		self.per_media_type_media_episode_file += self.dot_text

		if " " in self.per_media_type_media_episode_file[0]:
			self.per_media_type_media_episode_file[1:]

		Create_Text_File(self.per_media_type_media_episode_file, self.global_switches)

		Write_To_File(self.per_media_type_media_episode_file, self.full_watched_media_file_text, self.global_switches)

		# ------------------ #

		# Current Year Experienced Media Folder >
			# [Mixed Media Type] (Creates) >
				# [Watched media name] >
					# [Media episode title].txt
						# Contents:
						# [All watched number], [Media type watched number]
						# [Watched media name]
						# [Full Media episode title]
						#
						# [Watched media type]
						# [Mixed watched media type]
						#
						# [Watched time]
						# ([YouTube ID])

		self.current_year_experienced_media_folder = current_year_experienced_media_folder + self.mixed_media_type + "/"
		Create_Folder(self.current_year_experienced_media_folder, self.global_switches)

		# Experienced Media Watched Media Folder
		self.current_year_experienced_media_name_folder = self.current_year_experienced_media_folder + Remove_Non_File_Characters(self.media_title) + "/"
		Create_Folder(self.current_year_experienced_media_name_folder, self.global_switches)

		if self.no_media_list == False:
			self.current_year_experienced_media_name_folder = self.current_year_experienced_media_name_folder + self.media_item_file_safe + "/"
			Create_Folder(self.current_year_experienced_media_name_folder, self.global_switches)

		self.current_year_experienced_media_name_file = self.current_year_experienced_media_name_folder + self.media_episode_file_safe + self.dot_text
		Create_Text_File(self.current_year_experienced_media_name_file, self.global_switches)

		Write_To_File(self.current_year_experienced_media_name_file, self.full_watched_media_file_text, self.global_switches)

		# ------------------ #

		variable = ""

	def Check_First_Watched_In_Year(self):
		self.firsts_of_the_year_language_texts = {
			full_language_en: "Firsts Of The Year",
			full_language_pt: "Primeiros Do Ano",
		}

		self.media_language_texts = {
			full_language_en: "Media",
			full_language_pt: "Mídia",
		}

		self.firsts_of_the_year_folders = {}
		self.firsts_of_the_year_media_folders = {}
		self.firsts_of_the_year_media_type_folders = {}

		for full_language in full_languages_not_none:
			self.firsts_of_the_year_folders[full_language] = current_notepad_year_folder + full_language + "/" + self.firsts_of_the_year_language_texts[full_language] + "/"
			self.firsts_of_the_year_media_folders[full_language] = self.firsts_of_the_year_folders[full_language] + self.media_language_texts[full_language] + "/"
			self.firsts_of_the_year_media_type_folders[full_language] = self.firsts_of_the_year_media_folders[full_language] + self.language_singular_media_type + "/"

			Create_Folder(self.firsts_of_the_year_folders[full_language], self.global_switches)
			Create_Folder(self.firsts_of_the_year_media_folders[full_language], self.global_switches)
			Create_Folder(self.firsts_of_the_year_media_type_folders[full_language], self.global_switches)

		self.first_watched_media_file_name = self.total_watched_number + ". " + Remove_Non_File_Characters(self.media_item_episode_with_title) + " " + Text_Replacer(Text_Replacer(self.finished_watching_time, ":", ";"), "/", "-")

		local_full_episode = "\n" + self.media_item_episode_with_title

		if self.is_series_media == False:
			local_full_episode = ""

		self.is_first_watched_media_per_type = False

		if len(Create_Array_Of_File(self.per_media_type_episodes_file)) == 0:
			self.is_first_watched_media_per_type = True

		if self.is_first_watched_media_per_type == True:
			for full_language in full_languages_not_none:
				media_type_folder = self.firsts_of_the_year_media_type_folders[full_language]
				self.first_watched_media_file = media_type_folder + self.first_watched_media_file_name + self.dot_text
				Create_Text_File(self.first_watched_media_file, self.global_switches)

				text_to_write = self.total_watched_number + ", " + self.media_type_watched_number + "\n\n" + self.media_title + local_full_episode + "\n\n" + self.language_singular_media_type + "\n" + self.english_media_type + "\n\n" + self.finished_watching_time

				if self.ate_food == True or self.drank_drink == True:
					text_to_write += "\n\n" + self.ate_and_drank_text

				Write_To_File(self.first_watched_media_file, text_to_write, self.global_switches)

	def Fetch_Next_Episode(self):
		self.completed_media = False
		self.completed_media_item = False

		if self.is_series_media == True:
			if self.no_media_list == False:
				i = 0
				for media_list_item in self.media_list_item_names:
					if self.media_item in media_list_item:
						self.current_media_item_number = i

					i += 1

				if self.media_episode == self.media_episode_titles[-1]:
					if self.is_video_series_media == False and self.media_item == self.media_list_item_names[-1]:
						self.completed_media = True

					if self.is_video_series_media == False and self.media_item != self.media_list_item_names[-1]:
						self.next_media_item = self.media_list_item_names[self.current_media_item_number]

						if Read_String(self.current_media_item_file) != self.next_media_item:
							Write_To_File(self.current_media_item_file, self.next_media_item, self.global_switches)

					self.completed_media_item = True

		if self.is_series_media == False:
			self.completed_media = True

		if self.completed_media == False and self.completed_media_item == False:
			self.next_episode = self.media_episode_titles[int(self.media_episode_number) + 1]

			if self.is_hybrid == True:
				self.next_episode += self.origin_type

			if "Episode" in self.media_details:
				self.media_details["Episode"] = self.next_episode

			if self.no_media_list == False:
				self.media_item_details["Episode"] = self.next_episode

				if "Episode" in self.media_item_details:
					self.media_item_details["Episode"] = self.next_episode

				if Read_String(self.media_item_details_file) != Stringfy_Dict(self.media_item_details) and self.no_media_list == False:
					Write_To_File(self.media_item_details_file, Stringfy_Dict(self.media_item_details), self.global_switches)

		if self.completed_media == True:
			self.media_details["Status"] = self.completed_english_text

			# Defines the new watching status as "Completed"
			self.completed_text = Language_Item_Definer(self.completed_english_text, self.completed_portuguese_text)

		if Read_String(self.media_details_file) != Stringfy_Dict(self.media_details):
			Write_To_File(self.media_details_file, Stringfy_Dict(self.media_details), self.global_switches)

		# ------------------ #

		# Completed media part of the method

		if self.completed_media == True:
			self.watching_media_file = self.media_info_media_watching_status_files[self.english_media_type][self.watching_english_text]
			self.completed_media_file = self.media_info_media_watching_status_files[self.english_media_type][self.completed_english_text]

			self.watching_media_list = Create_Array_Of_File(self.watching_media_file)
			self.completed_media_list = Create_Array_Of_File(self.completed_media_file)

			if self.media_title_file_safe in self.watching_media_list:
				self.watching_media_list.remove(self.media_title_file_safe)

			self.completed_media_list.append(self.media_title_file_safe)

			self.watching_media_list = Stringfy_Array(sorted(self.watching_media_list), add_line_break = True)
			text_to_write = self.watching_media_list
			Write_To_File(self.watching_media_file, text_to_write, self.global_switches)

			# ----- #

			self.completed_media_list = Stringfy_Array(sorted(self.completed_media_list), add_line_break = True)

			text_to_write = self.completed_media_list
			Write_To_File(self.completed_media_file, text_to_write, self.global_switches)

		# ------------------ #

		# Completed media time and date part of the method

		# Gets the date that the user started and finished watching the media and writes it to the media watched dates text file
		if self.completed_media == True or self.is_video_series_media == True and self.completed_media_item == True:
			# Defines the media started and finished watching dates text file
			self.media_dates_file = self.media_item_folder + self.mixed_dates_text + self.dot_text

			# Defines the day that the user finished watching the media
			self.finished_watching_day = self.finished_watching_time

			if self.is_series_media == True:
				# Creates a text array of the media watched dates text file
				self.media_dates = Create_Array_Of_File(self.media_dates_file)

				# Defines the day that the user started watching the media
				self.started_watching_media_day = self.media_dates[1].split("/")

				# Defines the time (hours and minutes) that the user started watching the media
				self.time_and_day = self.started_watching_media_day[0].split(" ")

				self.time = self.time_and_day[0]

				# Splits the time and day that the user started watching the media by day, month, and year
				self.day = self.time_and_day[1]
				self.month = self.started_watching_media_day[1]
				self.year = self.started_watching_media_day[2]

				# Makes a datetime object of the time that the user started watching the media
				self.started_watching_media_day = "{} {}/{}/{}"
				self.started_watching_media_day = self.started_watching_media_day.format(self.time, self.day, self.month, self.year)
				self.format = "%H:%M %d/%m/%Y"
				self.day_that_started_watching_datetime = datetime.datetime.strptime(self.started_watching_media_day, self.format)

				# Defines the day that the user started watching the media
				self.day_that_finished_watching_string = self.finished_watching_day.split("/")

				# Defines the time (hours and minutes) that the user started watching the media
				self.time_and_day = self.day_that_finished_watching_string[0].split(" ")

				self.time = self.time_and_day[0]

				# Splits the time and day that the user started watching the media by day, month, and year
				self.day = self.time_and_day[1]
				self.month = self.day_that_finished_watching_string[1]
				self.year = self.day_that_finished_watching_string[2]

				self.day_that_finished_watching_string = "{} {}/{}/{}"
				self.day_that_finished_watching_string = self.day_that_finished_watching_string.format(self.time, self.day, self.month, self.year)

				# Makes a datetime object of the time that the user started watching the media
				self.day_that_finished_watching_datetime = datetime.datetime.strptime(self.day_that_finished_watching_string, self.format)

				self.has_years = False
				self.has_months = False

				# Defines the time spent watching the whole media (difference of started and finished watching datetime objects)
				self.time_spent_watching_media = str(self.day_that_finished_watching_datetime - self.day_that_started_watching_datetime)

				if " days" in self.time_spent_watching_media:
					# Gets the number of days spent wathing from the time_spent_watching_media string
					if re.search("[0-9][0-9][0-9] days", self.time_spent_watching_media) != None:
						self.days_spent_watching_media = int(re.search("[0-9][0-9][0-9] days", self.time_spent_watching_media).group().replace(" days", ""))

					else:
						if re.search("[0-9][0-9] days", self.time_spent_watching_media) != None:
							self.days_spent_watching_media = int(re.search("[0-9][0-9] days", self.time_spent_watching_media).group().replace(" days", ""))

					# Gets the time spent watching media from the time_spent_watching_media string
					self.hours_spent_watching_media = self.time_spent_watching_media.split(", ")[1]

					# If the days are equal to 365, say that it has years and defines the year text as singular
					if self.days_spent_watching_media == 365:
						self.years = "1"

						self.year_text = Language_Item_Definer("year", "ano")

						self.has_years = True

					# If the days are less than 365, say that it has months
					if self.days_spent_watching_media < 365 and self.days_spent_watching_media >= 30:
						# If the days spent watching are greater or equal to 60, then it defines the months text as plural
						if self.days_spent_watching_media >= 60:
							self.months_text = Language_Item_Definer("months", "meses")

						# If the days spent watching are equal to 30, then it defines the months text as singular
						if self.days_spent_watching_media <= 30 or self.days_spent_watching_media <= 59:
							self.months_text = Language_Item_Definer("month", "mês")

						# Splits the days by 30 to get month number
						self.months = str(round(self.days_spent_watching_media / 30))

						self.has_months = True

					# If the days are greater than 365, say that it has years, months, and defines the year text as plural
					if self.days_spent_watching_media > 365:
						self.divided_by_years = str(self.days_spent_watching_media / 365)

						# If a dot is in the year number (float), then it splits the string by the dot to get year and month number
						if "." in self.divided_by_years:
							# Defines the year number
							self.years = int(self.divided_by_years[0])

							self.months = round(float(self.divided_by_years), 2)

							# Defines the month number by getting the number after the dot on the float and gets the first number of it
							self.months = str(self.months).split(".")[1][0]

							# If the days spent watching are greater or equal to 60, then it defines the months text as plural
							if self.days_spent_watching_media >= 60:
								self.months_text = Language_Item_Definer("months", "meses")

							# If the days spent watching are equal to 30, then it defines the months text as singular
							if self.days_spent_watching_media <= 30:
								self.months_text = Language_Item_Definer("month", "mês")

							if self.days_spent_watching_media <= 30 or self.days_spent_watching_media <= 59:
								self.months_text = Language_Item_Definer("months", "meses")

							# If the years spent watching are equal to 1, then it defines the years text as singular
							if self.years == 1:
								self.years_text = Language_Item_Definer("year", "ano")

							# If the years spent watching are greater 1, then it defines the years text as plural
							if self.years > 1:
								self.years_text = Language_Item_Definer("years", "anos")

							self.has_months = True

						# If there is no dot on the year number (float), then it just uses the year number
						else:
							self.years = self.divided_by_years[0]

							self.years_text = Language_Item_Definer("year", "ano")

						self.has_years = True

					# If there are no years or months, just days, then it defines the days text
					if self.has_years == False and self.has_months == False:
						# If the days spent watching are lesser or equal to 1, then it defines the days text as singular
						if self.days_spent_watching_media <= 1:
							self.days_text = Language_Item_Definer("day", "dia")

						# If the days spent watching are greater than 1, then it defines the days text as plural
						if self.days_spent_watching_media > 1:
							self.days_text = Language_Item_Definer("days", "dias")

					self.time_spent_watching_media = ""

					# If the time spent watching the media has years, it adds the years number and text to the time_spent_watching_media string
					if self.has_years == True:
						self.years = str(self.years)
						self.time_spent_watching_media += self.years + " " + self.years_text

					# If the time spent watching the media has years and monts, it adds a comma to separate year and month numbers
					if self.has_years == True and self.has_months == True:
						self.time_spent_watching_media += ", "

					# If the time spent watching the media has months, it adds the months number and text to the time_spent_watching_media string
					if self.has_months == True:
						self.time_spent_watching_media += self.months + " " + self.months_text

					# If there are no years or months, just days, then it adds the days number and text to the time_spent_watching_media string
					if self.has_years == False and self.has_months == False:
						self.days = self.days_spent_watching_media

						self.time_spent_watching_media += self.days + " " + self.days_text

					# Splits the time that the user started watching the media by hours and minutes
					self.numeral_time_spent_watching_media = self.hours_spent_watching_media.split(":")

					self.hours = int(self.numeral_time_spent_watching_media[0])

					self.has_hours = False

					# If the hours text is not 00, then it defines the hour texts and the full hour text, which is hour number plus hour text
					# It also says that the time has hours
					if self.hours != 00:
						self.hour_text = Language_Item_Definer("hour", "hora")
						self.hours_text = Language_Item_Definer("hours", "horas")
						self.hours_text = self.hours_text if self.hours >= 2 else self.hour_text
						self.hours = str(self.hours) + " " + self.hours_text

						self.has_hours = True

					self.minutes = int(self.numeral_time_spent_watching_media[1])

					self.has_minutes = False

					# If the minutes text is not 00, then it defines the minute texts and the full minute text, which is minute number plus hour text
					# It also says that the time has minutes
					if self.minutes != 00:
						self.minute_text = Language_Item_Definer("minute", "minuto")
						self.minutes_text = Language_Item_Definer("minutes", "minutos")
						self.minutes_text = self.minutes_text if self.minutes >= 2 else self.minute_text
						self.minutes = str(self.minutes) + " " + self.minutes_text

						self.has_minutes = True

					# Creates the full numeral time spent watching media which may have hours and minutes, and maybe only one of the two
					self.numeral_time_spent_watching_media = ""

					# Adds the hours to the full numeral time spent watching string if the time has hours
					if self.has_hours == True:
						self.numeral_time_spent_watching_media += self.hours

					# Adds the "and" text per language to the full numeral time spent watching string if the time has both hours and minutes
					if self.has_hours == True and self.has_minutes == True:
						self.numeral_time_spent_watching_media += " " + self.and_text_lower + " "

					# Adds the minutes to the full numeral time spent string if the time has minutes
					if self.has_minutes == True:
						self.numeral_time_spent_watching_media += self.minutes

					# Adds a comma and the full numeral time spent watching text to the time spent watching media string
					self.time_spent_watching_media += ", " + self.numeral_time_spent_watching_media

			if self.is_series_media == False:
				self.started_watching_media_day = self.started_watching_time

			#################

			# Creates a text array of the media watched dates text file
			self.media_dates = Create_Array_Of_File(self.media_dates_file)

			self.media_dates.append("")

			# Appends the finished watching media date to the above array
			self.media_dates.append("Finished watching in - Terminei de assistir em:")
			self.media_dates.append(self.finished_watching_day)

			if self.is_series_media == True:
				# Appends the time spent watching media to the array of the media watched dates text file
				self.media_dates.append("")
				self.media_dates.append("Time spent watching the media - Tempo gasto assistindo a mídia:")
				self.media_dates.append(self.time_spent_watching_media)

			# Transforms the media watched dates text array in a string with line breaks
			self.media_dates = Stringfy_Array(self.media_dates, add_line_break = True)

			# Writes the new media watched dates text to the media watched dates text file
			text_to_write = self.media_dates
			Write_To_File(self.media_dates_file, text_to_write, self.global_switches)

			self.finished_watching_episode_time_text += "\n\n" + "De: " + self.started_watching_media_day + "\n" + "Até: " + self.finished_watching_day

			if self.is_series_media == True:
				self.finished_watching_episode_time_text += "\n" + "Duração: " + self.time_spent_watching_media

	def Post_On_Social_Networks(self):
		self.social_networks = [
			"WhatsApp",
			"Instagram",
			"Facebook",
			"Twitter",
		]

		self.social_networks_string = Stringfy_Array(self.social_networks, custom_separator = ", ")

		self.posted_on_social_networks_text = self.posted_on_social_networks_text_template.format("episódio")

		if self.is_series_media == False:
			self.posted_on_social_networks_text = self.posted_on_social_networks_text_template.format("filme")

		if self.is_video_series_media == True:
			self.posted_on_social_networks_text = self.posted_on_social_networks_text_template.format("episódio com legendas")

		if self.media_title in ["The Walking Dead", "Yuru Camp"]:
			self.posted_on_social_networks_text = self.posted_on_social_networks_text.replace("uma print", "um vídeo resumo")

		self.post_on_social_networks_text = Language_Item_Definer("Post on the Social Networks", "Postar nas Redes Sociais") + " (" + self.social_networks_string + ")"

		self.post_on_social_networks = Yes_Or_No_Definer(self.post_on_social_networks_text, second_space = False)

		print()

		if self.post_on_social_networks == True:
			if self.global_switches["testing_script"] == False:
				Unblock(True, "WhatsApp")

				Open_Link(self.social_networks_links[self.whatsapp])

			Select_Choice(Language_Item_Definer("Press Enter to copy watched text", "Pressione Enter para copiar texto de assistido"), enter_equals_empty = True, first_space = False)

			Copy_Text(self.finished_watching_episode_time_text)

		print("-----")
		print()

	def Write_On_Diary_Slim(self):
		diary_slim_watched_text = self.finished_watching_episode_time_text + "\n\n" + self.posted_on_social_networks_text
		Write_On_Diary_Slim_Module(diary_slim_watched_text, self.finished_watching_time, self.global_switches, add_dot = False, add_time = False)

	def Show_Watched_Media_Info(self):
		print()
		print(self.large_bar)
		print()

		print(Language_Item_Definer("Watched media info", "Informações da mídia assistida") + ": ")
		print()

		self.local_language_singular_media_type = self.language_singular_media_type

		if self.is_video_series_media == True:
			self.local_language_singular_media_type = Language_Item_Definer("{} channel", "Canal do {}").format(self.youtube_name)

		print(self.local_language_singular_media_type + ":")
		print(self.language_media_title)
		print()

		self.the_text = self.gender_the_texts[self.mixed_media_type]["the"]

		if self.is_video_series_media == True:
			self.the_text = self.gender_the_texts[self.mixed_media_type]["feminine"]["the"]
			self.watched_media_container_type = Language_Item_Definer(self.youtube_name + " video series", "série de vídeos do " + self.youtube_name)

		if self.is_series_media == True:
			self.media_episode_text = Language_Item_Definer("{} episode", "Episódio d{}".format(self.the_text) + " {}").format(self.watched_media_container_type)

			self.watched_media_item_name = self.watched_media_container_type

			if self.is_video_series_media == False:
				self.watched_media_container_type = Language_Item_Definer("season", "temporada")

			if self.is_video_series_media == True:
				self.watched_media_container_type = Language_Item_Definer("channel", "canal")

			print(self.media_episode_text + ":")
			print(self.media_episode)
			print()

			if self.no_media_list == False:
				print(self.media_episode_text + " " + Language_Item_Definer("with {}", "com {}").format(self.watched_media_container_type) + ":")

				media_item_episode = self.media_item_episode

				if ": " in self.media_item_episode and self.is_video_series_media == False:
					media_item_episode = self.media_item_episode.replace(": ", "")

				print(media_item_episode)
				print()

			if self.is_video_series_media == False:
				self.text_to_show = self.media_episode_text + " " + Language_Item_Definer("with {} {} title", "com título d{} {}").format(self.the_text, self.watched_media_item_name)

				if self.no_media_list == False:
					self.text_to_show += Language_Item_Definer(" and {}", " e {}").format(self.watched_media_container_type)

				print(self.text_to_show + ":")
				print(self.media_item_episode_with_title)
				print()

		# Show media type
		print(Language_Item_Definer("Media type", "Tipo de mídia") + ":")
		print(Language_Item_Definer(self.english_media_type, self.portuguese_media_type))

		# Show mixed media type
		if self.english_media_type != self.anime_media_type_english_plural:
			print()
			print(Language_Item_Definer("Mixed media type", "Tipo de mídia misturado") + ":")
			print(self.mixed_media_type)

		if self.is_first_watched_media_per_type == True:
			self.english_first_watched_in_year_text = Language_Item_Definer("This is {}".format(self.the_text) + " first {} that you watch in {}")
			self.portuguese_first_watched_in_year_text = Language_Item_Definer("Ess{} é {} primeir{}".format(self.the_text, self.the_text, self.the_text) + " {} que você assiste em {}")

			if self.is_series_media == True:
				self.english_first_watched_in_year_text = self.english_first_watched_in_year_text.replace("first {}", "first {} episode")
				self.portuguese_first_watched_in_year_text = self.portuguese_first_watched_in_year_text.replace("primeir{}", "primeir{} episódio de")

				if self.is_video_series_media == True:
					self.english_first_watched_in_year_text = self.english_first_watched_in_year_text.replace("episode", "YouTube video")
					self.portuguese_first_watched_in_year_text = self.portuguese_first_watched_in_year_text.replace("episódio", "vídeo do YouTube")

			self.first_watched_in_year_text = Language_Item_Definer(self.english_first_watched_in_year_text, self.portuguese_first_watched_in_year_text).format(self.language_singular_media_type, current_year) + "."

			print()
			print(self.first_watched_in_year_text)

		self.finished_watching_text = Language_Item_Definer("When I finished watching the", "Quando assisti o") + " "

		if self.is_series_media == True:
			self.finished_watching_text += "episódio"

		if self.is_series_media == False:
			self.finished_watching_text += self.language_singular_media_type

		print()
		print(self.finished_watching_text + ": " + self.finished_watching_time)

		if self.youtube_video_id != "":
			print()
			print(Language_Item_Definer("YouTube ID", "ID do YouTube") + ": " + self.youtube_video_id)

		if self.ate_food != False:
			print()
			print(Language_Item_Definer("Food", "Comida") + ": " + self.food)

		if self.drank_drink != False:
			print()
			print(Language_Item_Definer("Drink", "Bebida") + ": " + self.drink)

		if self.completed_media == False and self.completed_media_item == False and self.is_series_media == True:
			print()
			print(Language_Item_Definer("Next episode to watch", "Próximo episódio para assistir") + ": ")
			print(self.next_episode)

		print()
		print(self.dash_space)

		self.congratulations_text = Language_Item_Definer("Congratulations", "Parabéns") + "! :3"

		if self.completed_media_item == True:
			print()

			print(self.congratulations_text)
			print()

			self.english_finished_watching_media_item_text = 'You just finished watching this {} of {} "{}" {}'.format(self.watched_media_item_name, self.the_text, self.language_media_title, self.watched_media_container_type)

			self.portuguese_finished_watching_media_item_text = 'Você acabou de terminar de assistir essa {} {} {} "{}"'.format(self.watched_media_item_name, self.the_text, self.watched_media_container_type, self.language_media_title)

			print(Language_Item_Definer(self.english_finished_watching_media_item_text, self.portuguese_finished_watching_media_item_text) + ": ")
			print(self.media_item)

			if self.completed_media == False and self.is_video_series_media == False:
				print()
				print(Language_Item_Definer("Next {} to watch", "Próxima {} para assistir").format(self.watched_media_item_name) + ": ")
				print(self.next_media_item)

		if self.completed_media == True:
			print()

			if self.completed_media_item == True:
				print(self.dash_space)
				print()

			self.finished_watching_media_text_template = Language_Item_Definer("You just finished watching {} {}", "Você acabou de terminar de assistir {} {}")

			if self.is_video_series_media == False:
				self.watched_media_container_type = self.language_singular_media_type.lower()

			print(self.congratulations_text)
			print(self.finished_watching_media_text_template.format(self.the_text, self.watched_media_container_type.lower()) + ": ")
			print(self.language_media_title)
			print()

			print(Language_Item_Definer("Finished {} info", "Informações d{}".format(self.the_text) + " {}").format(self.language_singular_media_type.lower()) + ":")
			print()
	
			print(Language_Item_Definer("New watching status", "Novo status de assistindo") + ":")
			print(self.completed_text)
			print()

			self.the_media_text = self.the_text + " " + self.watched_media_container_type.lower()

			self.watching_media_time_text_template = Language_Item_Definer("Time and day that you {} watching", "Hora e dia que você {} assistir") + " " + self.the_media_text

			# Started watching media time text and day
			self.started_watching_media_time_text = self.watching_media_time_text_template.format(Language_Item_Definer("started", "começou a"))

			print(self.started_watching_media_time_text + ":")
			print(self.started_watching_media_day)
			print()

			# Finished watching media time text and day
			self.finished_watching_time_text = self.watching_media_time_text_template.format(Language_Item_Definer("finished", "terminou de"))

			print(self.finished_watching_time_text + ":")
			print(self.finished_watching_day)

			if self.is_series_media == True:
				print()
				print(Language_Item_Definer("This is the time you spent watching", "Este é o tempo que você passou assistindo") + " " + self.the_media_text + ": ")
				print(self.time_spent_watching_media)

			print()
			print(self.large_bar)

		print()

		input(Language_Item_Definer("Press Enter when you finish reading the Info Summary", "Pressione Enter quando terminar de ler o Resumo de Informações") + ": ")