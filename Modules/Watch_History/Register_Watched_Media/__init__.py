# Register_Watched_Media.py

from Watch_History.Watch_History import Watch_History as Watch_History

from Social_Networks.Open_Social_Network import Open_Social_Network as Open_Social_Network

from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

import re

class Register_Watched_Media(Watch_History):
	def __init__(self, run_as_module = False, media_dictionary = None):
		super().__init__()

		self.run_as_module = run_as_module
		self.media_dictionary = media_dictionary

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

		self.media_dictionary = {}

	def Define_Media_Variables(self):
		self.media_title = self.media_dictionary["media_title"]
		self.media_titles = self.media_dictionary["media_titles"]
		self.media_title_file_safe = self.media_dictionary["media_title_file_safe"]

		self.language_media_title = self.media_titles["language"]

		self.media_folder = self.media_dictionary["media_folder"]
		self.media_details = self.media_dictionary["media_details"]
		self.media_details_file = self.media_dictionary["media_details_file"]

		self.media_episode = self.media_dictionary["media_episode"]
		self.media_episode_file_safe = self.media_dictionary["media_episode_file_safe"]
		self.language_media_episode = self.media_dictionary["language_media_episode"]

		self.plural_media_types = self.media_dictionary["plural_media_types"]
		self.singular_media_types = self.media_dictionary["singular_media_types"]
		self.mixed_plural_media_type = self.media_dictionary["mixed_plural_media_type"]

		self.origin_type = self.media_dictionary["origin_type"]

		self.per_media_type_files_folder = self.media_dictionary["per_media_type_files_folder"]
		self.per_media_type_episodes_file = self.media_dictionary["per_media_type_episodes_file"]
		self.per_media_type_times_file = self.media_dictionary["per_media_type_times_file"]

		self.is_remote = self.media_dictionary["is_remote"]
		self.is_local = self.media_dictionary["is_local"]
		self.is_hybrid = self.media_dictionary["is_hybrid"]

		self.is_series_media = self.media_dictionary["is_series_media"]
		self.is_video_series_media = self.media_dictionary["is_video_series_media"]

		if self.is_series_media == True:
			self.media_episode_number = self.media_dictionary["media_episode_number"]
			self.episode_titles = self.media_dictionary["episode_titles"]
			self.language_episode_titles = self.media_dictionary["language_episode_titles"]

		self.re_watching = self.media_dictionary["re_watching"]

		self.no_media_list = self.media_dictionary["no_media_list"]

		self.media_item = self.media_dictionary["media_item"]
		self.language_media_item = self.media_dictionary["language_media_item"]
		self.media_item_file_safe = self.media_dictionary["media_item_file_safe"]
		self.media_item_episode = self.media_dictionary["media_item_episode"]
		self.media_item_episode_with_title = self.media_dictionary["media_item_episode_with_title"]
		self.media_item_folder = self.media_dictionary["media_item_folder"]
		self.current_media_item_file = self.media_dictionary["current_media_item_file"]

		if self.no_media_list == False:
			self.media_item_details = self.media_dictionary["media_item_details"]
			self.media_item_details_file = self.media_dictionary["media_item_details_file"]
			self.media_list_item_names = self.media_dictionary["media_list_item_names"]

		if self.is_video_series_media == True:
			self.media_dictionary["youtube_video_id"] = self.media_dictionary["youtube_video_id"]

		if self.plural_media_types["en"] == self.texts["plural_media_types, type: list"]["en"][0] and "dubbed_media_text" in self.media_dictionary:
			self.dubbed_media_text = self.media_dictionary["dubbed_media_text"]

		if self.plural_media_types["en"] == self.texts["plural_media_types, type: list"]["en"][4]:
			self.is_video_series_media = True

	def Define_Diary_Slim_Watched_Text(self):
		template = self.language_texts["i_just_finished_watching_{}"]

		if self.is_series_media == True:
			template += ' "{}"'

			self.watched_item_text = self.language_texts["this_episode_{}"].format(self.media_dictionary["of_the_text"])

			if self.re_watching == True:
				template = template.replace(self.language_texts["watch"], self.language_texts["re_watch"])

			self.media_episode_without_re_watched = re.sub(" " + self.texts["re_watched, type: regex, en - pt"], "", self.media_episode)

			if self.media_episode_without_re_watched == self.language_episode_titles[0]:
				self.watched_item_text = self.watched_item_text.replace(self.language_texts["this, masculine"], self.language_texts["the_first, masculine"])

			if self.media_episode_without_re_watched == self.language_episode_titles[-1] or len(self.language_episode_titles) == 1:
				self.watched_item_text = self.watched_item_text.replace(self.language_texts["this, masculine"], self.language_texts["the_last, masculine"])

			self.watched_item_text = self.watched_item_text.replace(self.language_texts["episode"], self.media_dictionary["media_unit_name"])

			self.of_the_text = self.language_texts["of_the_{}"]

			if self.no_media_list == False and self.is_video_series_media == False:
				if self.media_item == self.media_list_item_names[0]:
					self.of_the_text = self.language_texts["of_the_first_{}"]

				if self.media_item == self.media_list_item_names[-1]:
					self.of_the_text = self.language_texts["of_the_final_{}"]

			self.of_the_text = self.of_the_text.format(self.media_dictionary["media_item_name"])

			self.watched_media_container_type = self.singular_media_types["language"].lower()

			if self.is_video_series_media == True:
				self.watched_media_container_type = self.language_texts["channel"]

			if self.no_media_list == False:
				self.watched_item_text = self.watched_item_text.replace(self.media_dictionary["media_unit_name"], self.media_dictionary["media_unit_name"] + " {}".format(self.of_the_text))

				if self.media_item != self.media_title:
					self.watched_item_text = self.watched_item_text.replace(self.of_the_text, self.of_the_text + ' "' + self.language_media_item[self.user_language]["title"] + '"')

					if self.media_title + " " in self.media_item:
						self.watched_item_text = self.watched_item_text.replace(self.media_title + " ", "")

			self.watched_item_text += " " + self.watched_media_container_type

			self.finished_watching_diary_text = template.format(self.watched_item_text, self.media_titles["language"])

		if self.is_series_media == False:
			self.finished_watching_diary_text = template.format(self.media_dictionary["this_text"] + " " + self.singular_media_types["language"].lower())

		if self.plural_media_types["en"] == self.texts["animes"]["en"] and "dubbed_media_text" in self.media_dictionary:
			self.finished_watching_diary_text += self.language_texts["dubbed"]

		self.finished_watching_diary_text += ":\n" + self.language_media_episode

		if self.is_video_series_media == True:
			self.finished_watching_diary_text += "\n\n" + self.remote_origins["YouTube"] + "watch?v=" + self.media_dictionary["youtube_video_id"]

		self.finished_watching_diary_with_time_text = self.media_dictionary["finished_watching"] + ":\n" + self.finished_watching_diary_text

	def Ask_For_Food_And_Drink(self):
		self.ask_for_food_and_drink = False

		self.food_and_drink_text = ""

		self.ate_food = False
		self.food = ""

		if self.ask_for_food_and_drink == True:
			self.ate_food = self.Input.Yes_Or_No(self.language_texts["did_you_watched_while_you_ate"])

			if self.ate_food == True:
				self.media_dictionary["food"] = self.Input.Type(self.language_texts["type_what_you_ate"])

		self.drank_drink = False
		self.drink = ""

		if self.ask_for_food_and_drink == True:
			self.drank_drink = self.Input.Yes_Or_No(self.language_texts["did_you_watched_while_drinking"])

			if self.drank_drink == True:
				self.media_dictionary["drink"] = self.Input.Type(self.language_texts["type_what_you_drank"])

		if self.ate_food == True:
			self.food_and_drink_text += " " + self.language_texts["while"] + " " + self.language_texts["eating"] + " " + self.food

		if self.ate_food == True and self.drank_drink == True:
			self.food_and_drink_text += " " + self.language_texts["and"] + " "

		else:
			if self.drank_drink == True:
				self.food_and_drink_text += " " + self.language_texts["while"] + " "

		if self.drank_drink == True:
			self.food_and_drink_text += self.language_texts["drinking"] + " " + self.drink

		self.finished_watching_episode_text_with_food_and_drink = self.finished_watching_diary_text.replace('":', '"' + self.food_and_drink_text + ':')

		if self.ate_food == True or self.drank_drink == True:
			self.ate_and_drank_text = ""

		if self.ate_food == True:
			self.ate_and_drank_text += "\n\n" + self.language_texts["food, title(), en - pt"] + ": " + self.food

		if self.ate_food == True and self.drank_drink == True:
			self.ate_and_drank_text += "\n"

		if self.drank_drink == True:
			if self.ate_food == False:
				self.ate_and_drank_text += "\n\n"

			self.ate_and_drank_text += self.language_texts["food, title(), en - pt"] + ": " + self.drink

	def Add_To_Watched_Numbers(self):
		self.media_type_watched_number_file = self.per_media_type_number_files[self.plural_media_types["en"]]

		# Movies Folder (Appends)
			# Number.txt (Writes)

		# Current Year Watched Media Folder >

			# Per Media Type >
				# Files (Writes) > 
					# [Media Type] >
						# Number.txt

			# Writes:
				# Number.txt

		self.total_watched_number = str(int(self.File.Contents(self.total_watched_number_current_year_file)["lines"][0]) + 1)
		self.media_type_watched_number = str(int(self.File.Contents(self.media_type_watched_number_file)["lines"][0]) + 1)

		# Number.txt
		text_to_write = self.total_watched_number
		self.File.Edit(self.total_watched_number_current_year_file, text_to_write, "w")

		# Files (Writes) > [Media Type] > Number.txt
		text_to_write = self.media_type_watched_number
		self.File.Edit(self.media_type_watched_number_file, text_to_write, "w")

		self.watched_movie_number_file = self.movies_folder + "Number.txt"

		if self.is_series_media == False:
			# Movies Folder (Appends) > Number.txt (Writes)
			text_to_write = str(int(self.File.Contents(self.watched_movie_number_file)["lines"][0]) + 1)
			self.File.Edit(self.watched_movie_number_file, text_to_write, "w")

	def Add_Watched_Media_To_Text_Files(self):
		# Current Year Watched Media Folder >

			# Appends:
				# Episodes.txt
				# Media Types.txt
				# Times.txt
				# YouTude IDs.txt

		self.youtube_video_ids_file = self.current_year_watched_media_folder + self.texts["youtube_ids"]["en"] + ".txt"
		self.File.Create(self.youtube_video_ids_file)

		# Episodes.txt
		text_to_append = self.media_item_episode_with_title
		self.File.Edit(self.watched_files["Episodes"], text_to_append, "a")

		# Media Types.txt
		text_to_append = self.mixed_plural_media_type
		self.File.Edit(self.watched_files["Media Types"], text_to_append, "a")

		# Times.txt
		text_to_append = self.media_dictionary["finished_watching"]
		self.File.Edit(self.watched_files["Times"], text_to_append, "a")

		# YouTube IDs.txt
		text_to_append = "None"

		if self.is_video_series_media == True:
			text_to_append = self.media_dictionary["youtube_video_id"]

		self.File.Edit(self.youtube_video_ids_file, text_to_append, "a")

		# ------------------ #

		# Current Year Watched Media Folder >

			# Per Media Type >
				# Files (Appends) > 
					# [Media Type] >
						# Episodes.txt, Times.txt, YouTude IDs.txt

		# Files (Appends) > [Media Type] > Episodes.txt
		text_to_append = self.media_item_episode_with_title
		self.File.Edit(self.per_media_type_episodes_file, text_to_append, "a")

		# Files (Appends) > [Media Type] > Times.txt
		text_to_append = self.media_dictionary["finished_watching"]
		self.File.Edit(self.per_media_type_times_file, text_to_append, "a")
		
		# Files (Appends) > [Media Type] > (YouTube IDs.txt)
		if self.is_video_series_media == True:
			self.youtube_video_ids_file = self.per_media_type_files_folder + self.texts["youtube_ids"]["en"] + ".txt"
			self.File.Create(self.youtube_video_ids_file)

			text_to_append = self.media_dictionary["youtube_video_id"]
			self.File.Edit(self.youtube_video_ids_file, text_to_append, "a")

		# ------------------ #

		# Movies Folder (Appends)
			# Names.txt
			# Times.txt

		if self.is_series_media == False:
			self.watched_movie_names_file = self.movies_folder + "Names.txt"
			self.watched_movie_times_file = self.movies_folder + "Times.txt"

			# Movies Folder (Appends) > Names.txt
			text_to_append = self.media_item_episode_with_title
			self.File.Edit(self.watched_movie_names_file, text_to_append, "a")

			# Movies Folder (Appends) > Times.txt
			text_to_append = self.media_dictionary["finished_watching"]
			self.File.Edit(self.watched_movie_times_file, text_to_append, "a")

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

		self.media_item_episode_with_title_file = self.Sanitize(self.media_item_episode_with_title, restricted_characters = True)

		self.media_item_episode_with_title_file = re.sub(" " + self.texts["re_watched, type: regex, en - pt"], "", self.media_item_episode_with_title_file)

		# [Watched number]. [Media name] [Media episode title].txt
		self.current_episode_file = self.all_watched_files_current_year_folder + str(self.total_watched_number) + ". " + self.media_item_episode_with_title_file + ".txt"

		self.File.Create(self.current_episode_file)

		self.full_watched_media_file_text = self.total_watched_number + ", " + self.media_type_watched_number + "\n\n"

		if self.is_series_media == True:
			self.full_watched_media_file_text += self.media_title + "\n"

		self.full_watched_media_file_text += self.media_item_episode_with_title + "\n\n" + self.singular_media_types["en"] + "\n" + self.mixed_plural_media_type + "\n\n" + self.media_dictionary["finished_watching"]

		if self.is_video_series_media == True:
			self.full_watched_media_file_text += "\n" + self.media_dictionary["youtube_video_id"]

		if self.ate_food == True or self.drank_drink == True:
			self.full_watched_media_file_text += self.ate_and_drank_text

		self.File.Edit(self.current_episode_file, self.full_watched_media_file_text, "w")

		# ------------------ #

		# Current Year Watched Media Folder >
			# Per Media Type >
				# Folders >
					# [Media Type] (Creates) >
						# [Media name] >
							# [Media episode title without media name].txt
								# Contents:
								# [All watched number], [Media type watched number]
								# 
								# [Watched media name]
								# [Full Media episode title]
								#
								# [Watched media type]
								# [Mixed watched media type]
								#
								# [Watched time]
								# ([YouTube ID])

		self.per_media_type_folder = self.per_media_type_folder_folders_dict[self.plural_media_types["en"]]

		self.watched_media_folder = self.per_media_type_folder + self.Sanitize(self.media_title, restricted_characters = True) + "/"
		self.Folder.Create(self.watched_media_folder)

		if self.no_media_list == False and self.media_item != self.media_title:
			self.watched_media_folder = self.watched_media_folder + self.media_item_file_safe + "/"
			self.Folder.Create(self.watched_media_folder)

		self.media_item_episode_file = self.Sanitize(self.media_episode_file_safe, restricted_characters = True)

		# Per Media Type watched media name file
		self.per_media_type_media_episode_file = self.watched_media_folder

		if self.is_series_media == True:
			self.per_media_type_media_episode_file += self.media_item_episode_file

			if len(self.per_media_type_media_episode_file) > 255:
				while len(self.per_media_type_media_episode_file) > 255:
					self.per_media_type_media_episode_file = self.per_media_type_media_episode_file[:-1]

		if self.is_series_media == False:
			self.per_media_type_media_episode_file += self.texts["movie, en - pt"]

		if " " in self.per_media_type_media_episode_file[-1]:
			self.per_media_type_media_episode_file[:-1]

		self.per_media_type_media_episode_file += ".txt"

		if " " in self.per_media_type_media_episode_file[0]:
			self.per_media_type_media_episode_file[1:]

		self.File.Create(self.per_media_type_media_episode_file)

		self.File.Edit(self.per_media_type_media_episode_file, self.full_watched_media_file_text, "w")

		# ------------------ #

		# Current Year Experienced Media Folder >
			# [Mixed Media Type] (Creates) >
				# [Watched media name] >
					# [Media episode title].txt
						# Contents:
						# [All watched number], [Media type watched number]
						# 
						# [Watched media name]
						# [Full Media episode title]
						#
						# [Watched media type]
						# [Mixed watched media type]
						#
						# [Watched time]
						# ([YouTube ID])

		self.current_year_experienced_media_folder = self.notepad_folders["years"]["current"]["experienced_media"] + self.mixed_plural_media_type + "/"
		self.Folder.Create(self.current_year_experienced_media_folder)

		# Experienced Media Watched Media Folder
		self.current_year_experienced_media_name_folder = self.current_year_experienced_media_folder + self.Sanitize(self.media_title, restricted_characters = True) + "/"
		self.Folder.Create(self.current_year_experienced_media_name_folder)

		if self.no_media_list == False and self.media_item != self.media_title:
			self.current_year_experienced_media_name_folder = self.current_year_experienced_media_name_folder + self.media_item_file_safe + "/"
			self.Folder.Create(self.current_year_experienced_media_name_folder)

		self.current_year_experienced_media_name_file = self.current_year_experienced_media_name_folder + self.media_episode_file_safe + ".txt"
		self.File.Create(self.current_year_experienced_media_name_file)

		self.File.Edit(self.current_year_experienced_media_name_file, self.full_watched_media_file_text, "w")

		# ------------------ #

		variable = ""

	def Check_First_Watched_In_Year(self):
		self.firsts_of_the_year_folders = {
			"root": {},
			"subfolder": {},
			"media_type": {},
		}

		i = 0
		for language in self.small_languages:
			full_language = self.full_languages[language]

			self.firsts_of_the_year_folders["root"][language] = self.notepad_folders["years"]["current"]["root"] + full_language + "/" + self.texts["firsts_of_the_year"][language] + "/"
			self.Folder.Create(self.firsts_of_the_year_folders["root"][language])

			self.firsts_of_the_year_folders["subfolder"][language] = self.firsts_of_the_year_folders["root"][language] + self.texts["media"][language] + "/"
			self.Folder.Create(self.firsts_of_the_year_folders["subfolder"][language])

			self.firsts_of_the_year_folders["media_type"][language] = self.firsts_of_the_year_folders["subfolder"][language] + self.singular_media_types[language] + "/"
			self.Folder.Create(self.firsts_of_the_year_folders["media_type"][language])

			i += 1

		self.first_watched_media_file_name = self.total_watched_number + ". " + self.Sanitize(self.media_item_episode_with_title, restricted_characters = True)

		local_full_episode = "\n" + self.media_item_episode_with_title

		if self.is_series_media == False:
			local_full_episode = ""

		self.media_dictionary["first_watched_in_year"] = False

		if self.File.Contents(self.per_media_type_episodes_file)["length"] == 0:
			self.media_dictionary["first_watched_in_year"] = True

		if self.media_dictionary["first_watched_in_year"] == True:
			for language in self.small_languages:
				folder = self.firsts_of_the_year_folders["media_type"][language]

				self.first_watched_media_file = folder + self.first_watched_media_file_name + ".txt"
				self.File.Create(self.first_watched_media_file)

				text = self.total_watched_number + ", " + self.media_type_watched_number + "\n\n" + self.media_title + local_full_episode + "\n\n" + self.singular_media_types["en"] + "\n" + self.plural_media_types["en"] + "\n\n" + self.media_dictionary["finished_watching"]

				if self.ate_food == True or self.drank_drink == True:
					text += "\n\n" + self.ate_and_drank_text

				self.File.Edit(self.first_watched_media_file, text, "w")

	def Fetch_Next_Episode(self):
		self.media_dictionary["completed_media"] = False
		self.media_dictionary["completed_media_item"] = False

		if self.is_series_media == True:
			if self.no_media_list == False:
				i = 0
				for media_list_item in self.media_list_item_names:
					if self.media_item in media_list_item:
						self.current_media_item_number = i

					i += 1

				if self.media_episode == self.language_episode_titles[-1]:
					if self.is_video_series_media == False:
						if self.media_item == self.media_list_item_names[-1]:
							self.media_dictionary["completed_media"] = True

						if self.media_item != self.media_list_item_names[-1]:
							self.media_dictionary["next_media_item"] = self.media_list_item_names[self.current_media_item_number + 1]

							self.File.Edit(self.current_media_item_file, self.media_dictionary["next_media_item"], "w")

							self.media_dictionary["language_next_media_item"] = self.media_dictionary["next_media_item"]

							folder = self.media_dictionary["media_list_folder"] + self.media_dictionary["next_media_item"] + "/"
							dictionary = self.File.Dictionary(folder + "Media details.txt")

							if self.texts["[language]_name"][self.user_language] in dictionary:
								self.media_dictionary["language_next_media_item"] = dictionary[self.texts["[language]_name"][self.user_language]]

					self.media_dictionary["completed_media_item"] = True

			if self.no_media_list == True and self.media_episode == self.language_episode_titles[-1]:
				self.media_dictionary["completed_media"] = True

		if self.is_series_media == False:
			self.media_dictionary["completed_media"] = True

		if self.media_dictionary["completed_media"] == False and self.media_dictionary["completed_media_item"] == False:
			self.media_dictionary["next_episode_to_watch"] = self.language_episode_titles[int(self.media_episode_number)]

			if self.is_hybrid == True:
				self.media_dictionary["next_episode_to_watch"] += self.origin_type

			if self.language_texts["episode, title()"] in self.media_details:
				self.media_details[self.language_texts["episode, title()"]] = self.media_dictionary["next_episode_to_watch"]

			if self.no_media_list == False:
				self.media_item_details[self.language_texts["episode, title()"]] = self.media_dictionary["next_episode_to_watch"]

				if self.language_texts["episode, title()"] in self.media_item_details:
					self.media_item_details[self.language_texts["episode, title()"]] = self.media_dictionary["next_episode_to_watch"]

				if self.no_media_list == False:
					self.File.Edit(self.media_item_details_file, self.Text.From_Dictionary(self.media_item_details), "w")

		if self.media_dictionary["completed_media"] == True:
			self.media_details[self.language_texts["status, title()"]] = self.language_texts["completed, title()"]

			# Defines the new watching status as "Completed"
			self.media_dictionary["completed_text"] = self.language_texts["completed, title()"]

		self.File.Edit(self.media_details_file, self.Text.From_Dictionary(self.media_details), "w")

		# ------------------ #

		# Completed media part

		# Update Watching Status files
		if self.media_dictionary["completed_media"] == True:
			# Watching media list
			self.watching_media_file = self.watching_status_files[self.plural_media_types["en"]][self.language_texts["watching, title()"]]
			self.watching_media_list = self.File.Contents(self.watching_media_file)["lines"]

			# Remove completed media from the Watching media list
			if self.media_title_file_safe in self.watching_media_list:
				self.watching_media_list.remove(self.media_title_file_safe)

			# Update the Watching media list
			self.File.Edit(self.watching_media_file, self.Text.From_List(sorted(self.watching_media_list)), "w")

			# ----- #

			# Completed media list
			self.completed_media_file = self.watching_status_files[self.plural_media_types["en"]][self.language_texts["completed, title()"]]
			self.completed_media_list = self.File.Contents(self.completed_media_file)["lines"]

			# Add completed media to the Completed media list
			self.completed_media_list.append(self.media_title_file_safe)

			# Update the Completed media list
			self.File.Edit(self.completed_media_file, self.Text.From_List(sorted(self.completed_media_list)), "w")

		# Completed media time and date part
		self.media_the_text = self.media_dictionary["the_text"] + " " + self.media_dictionary["media_container_name"]
		self.media_item_the_text = self.media_dictionary["the_item_text"] + " " + self.media_dictionary["media_item_name"]

		# Gets the date that the user started and finished watching the media item and writes it to the media dates text file
		if self.media_dictionary["completed_media_item"] == True:
			# Defines the media started and finished watching dates text file
			self.media_item_dates_file = self.media_item_folder + self.texts["dates, title(), en - pt"] + ".txt"

			self.media_item_dates = self.File.Dictionary(self.media_item_dates_file, next_line = True)

			self.media_dictionary["started_watching_item"] = self.media_item_dates[self.language_texts["when_i_started_to_watch"] + " " + self.media_item_the_text]

			self.media_dictionary["time_spent_watching_item"] = self.Date.Difference(self.media_dictionary["started_watching_item"], self.media_dictionary["finished_watching"])["difference_string"]

			text = self.File.Contents(self.media_item_dates_file)["string"]
			text += "\n\n"
			text += self.language_texts["when_i_finished_watching"] + " " + self.media_item_the_text + ":" + "\n"
			text += self.media_dictionary["finished_watching"]
			text += "\n\n"
			text += self.language_texts["duration, title()"] + ":" + "\n"
			text += self.media_dictionary["time_spent_watching_item"]

			self.File.Edit(self.media_item_dates_file, text, "w")

			self.finished_watching_diary_with_time_text += "\n\n"
			self.finished_watching_diary_with_time_text += self.language_texts["when_i_started_to_watch"] + " " + self.media_item_the_text + ": " + self.media_dictionary["started_watching_item"] + "\n"
			self.finished_watching_diary_with_time_text += self.language_texts["when_i_finished"] + ": " + self.media_dictionary["finished_watching"]
			self.finished_watching_diary_with_time_text += "\n" + self.language_texts["duration, title()"] + ": " + self.media_dictionary["time_spent_watching_item"]

		# Gets the date that the user started and finished watching the media and writes it to the media dates text file
		if self.media_dictionary["completed_media"] == True:
			# Defines the media started and finished watching dates text file
			self.media_dates_file = self.media_folder + self.texts["dates, title(), en - pt"] + ".txt"

			self.media_dates = self.File.Dictionary(self.media_dates_file, next_line = True)

			self.media_dictionary["started_watching"] = self.media_dates[self.language_texts["when_i_started_to_watch"] + " " + self.media_the_text]

			self.media_dictionary["time_spent_watching"] = self.Date.Difference(self.media_dictionary["started_watching"], self.media_dictionary["finished_watching"])["difference_string"]

			text = self.File.Contents(self.media_dates_file)["string"]
			text += "\n\n"
			text += self.language_texts["when_i_finished_watching"] + " " + self.media_the_text + ":" + "\n"
			text += self.media_dictionary["finished_watching"]
			text += "\n\n"
			text += self.language_texts["duration, title()"] + ":" + "\n"
			text += self.media_dictionary["time_spent_watching"]

			self.File.Edit(self.media_dates_file, text, "a")

			self.finished_watching_diary_with_time_text += "\n\n"
			self.finished_watching_diary_with_time_text += self.language_texts["when_i_started_to_watch"] + " " + self.media_the_text + ": " + self.media_dictionary["started_watching"] + "\n"
			self.finished_watching_diary_with_time_text += self.language_texts["when_i_finished"] + ": " + self.media_dictionary["finished_watching"]
			self.finished_watching_diary_with_time_text += "\n" + self.language_texts["duration, title()"] + ": " + self.media_dictionary["time_spent_watching"]

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

		text = self.language_texts["a_screenshot_of_the_episode"]

		if self.is_series_media == False:
			text = text.replace(self.language_texts["a_screenshot_of_the_episode"], self.language_texts["movie"])

		if self.media_title in ["The Walking Dead", "Yuru Camp"]:
			text = text.replace(self.language_texts["a_screenshot_of_the_episode"], self.language_texts["a_summary_video"])

		self.posted_on_social_networks_text_template = self.language_texts["i_posted_the_watched_text_and_{}_on_the_status_of_{}_and_tweet_on_{}"] + "."

		self.posted_on_social_networks_text = self.posted_on_social_networks_text_template.format(text, self.first_three_social_networks, self.twitter_social_network)

		self.post_on_social_networks_text = self.language_texts["post_on_the_social_networks"] + " (" + self.social_networks_string + ")"

		self.post_on_social_networks = self.Input.Yes_Or_No(self.post_on_social_networks_text)

		if self.post_on_social_networks == True:
			Open_Social_Network(option_info = {"type": "profile"}, social_network_parameter = "WhatsApp", first_space = False, second_space = False)

			self.Input.Type(self.language_texts["press_enter_to_copy_the_watched_text"])

			self.Text.Copy(self.finished_watching_diary_with_time_text)

		print()
		print("-----")
		print()

	def Write_On_Diary_Slim(self):
		diary_slim_watched_text = self.finished_watching_diary_with_time_text + "\n\n" + self.posted_on_social_networks_text

		Write_On_Diary_Slim_Module(diary_slim_watched_text, self.media_dictionary["finished_watching"], add_time = False)

	def Show_Watched_Media_Info(self):
		del self.media_dictionary["header_text"], self.media_dictionary["media_unit"]

		self.media_dictionary["header_text"] = self.Text.Capitalize(self.media_dictionary["media_container_name"]) + ": "

		if self.media_dictionary["completed_media"] == True:
			self.media_dictionary["header_text"] = self.language_texts["you_finished_watching_{}"].format(self.media_the_text) + ": "

		self.Show_Media_Information(self.media_dictionary)