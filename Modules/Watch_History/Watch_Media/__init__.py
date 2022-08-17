# Watch_Media.py

# Script Helper importer
from Script_Helper import *

from Watch_History.Watch_History import Watch_History as Watch_History

from Watch_History.Register_Watched_Media import Register_Watched_Media as Register_Watched_Media
from Watch_History.Select_Media_Type_And_Media import Select_Media_Type_And_Media as Select_Media_Type_And_Media
from Watch_History.Comment_Writer import Write_Comment as Write_Comment
from Watch_History.Media_Manager import *

import re
from os.path import expanduser

# Class to watch media that has a "To_Watch" status
class Watch_Media(Watch_History):
	def __init__(self, run_as_module = False, open_media = True, media_list = None, status_text = None, choice_info = None):
		super().__init__()

		self.run_as_module = run_as_module
		self.open_media = open_media
		self.media_list = media_list

		self.status_text = status_text

		if self.status_text == None:
			self.status_text = self.watching_english_text

		self.Select_Media_Type_And_Media()
		self.Define_Media_Variables()
		self.Define_Media_Episode_Variables()
		self.Define_Media_Dict()

		if self.open_media == True:
			self.Define_Media_Episode_Unit()
			self.Show_Opening_Media_Info()
			self.Open_Media_Unit()
			self.Make_Discord_Status()
			self.Comment_On_Media()
			self.Register_Media()

	def Select_Media_Type_And_Media(self):
		if self.run_as_module == False:
			self.lists_dict = {}

			self.lists_dict["media_list"] = self.media_list

			self.choice_info = Select_Media_Type_And_Media(self.lists_dict, status_text = self.status_text)

		if self.run_as_module == True:
			self.choice_info = choice_info

		# Media Type variables definition
		self.english_media_type = self.choice_info.english_media_type
		self.portuguese_media_type = self.choice_info.portuguese_media_type
		self.language_singular_media_type = self.choice_info.language_singular_media_type
		self.mixed_media_type = self.choice_info.mixed_media_type

		# Watching Status files and media
		self.watching_status_files = self.choice_info.watching_status_files
		self.watching_status_media = self.choice_info.watching_status_media

		# Per Media Type files folder, times file, and episodes file
		self.per_media_type_files_folder = self.per_media_type_files_folders[self.english_media_type]
		self.per_media_type_times_file = self.per_media_type_time_files[self.english_media_type]
		self.per_media_type_episodes_file = self.per_media_type_episode_files[self.english_media_type]

		# Media variables definition (name, folder, and details)
		self.media_folder = self.choice_info.media_folder
		self.media_details = self.choice_info.media_details
		self.media_details_file = self.choice_info.media_details_file

		if self.global_switches["verbose"] == True:
			print("media_folder:")
			print(self.media_folder)

			print()
			print("media_details:")
			Dict_Print(self.media_details)

			print("media_details_file:")
			print(self.media_details_file)
			print()

	def Define_Media_Variables(self):
		# Media title and Portuguese media title variables
		self.media_title = self.media_details["Original Name"]
		self.media_title_file_safe = Remove_Non_File_Characters(self.media_title)

		self.portuguese_media_title = self.media_title

		if "Portuguese Name" in self.media_details:
			self.portuguese_media_title = self.media_details["Portuguese Name"]

		self.media_watching_status = self.media_details["Status"]

		self.origin_type = self.media_details["Origin Type"]

		# Media origin type default variables
		self.is_remote = False
		self.is_local = False
		self.is_hybrid = False
		self.is_local_episode = False
		self.is_remote_episode = False

		self.is_series_media = True
		self.is_video_series_media = False

		self.re_watching = False

		# Series media, video series media, and re-watching variables definition
		if self.english_media_type == self.movie_media_type_english_plural:
			self.is_series_media = False

		if self.english_media_type == self.video_media_type_english_plural:
			self.is_video_series_media = True

		if self.media_watching_status == self.rewatching_english_text:
			self.re_watching = True

		self.no_media_list = False

		self.current_media_item_file = None

		# Media list definition for series media
		if self.is_series_media == True:
			self.media_list_text = self.media_type_sub_folders[self.mixed_media_type]["media_list_text"]
			self.singular_media_list_text = self.media_type_sub_folders[self.mixed_media_type]["english_singular_media_list_text"]
			self.current_media_item_text = "Current " + self.singular_media_list_text

			self.media_list_folder = self.media_folder + self.media_list_text + "/"

			# Media list folder exists
			if is_a_folder(self.media_list_folder) == True:
				# "Seasons - Temporadas.txt" or "Series - Séries.txt"
				self.media_list_file = self.media_list_folder + self.media_list_text + self.dot_text
				Create_Text_File(self.media_list_file, self.global_switches["create_files"])

				# "Current Season.txt" or "Current Series.txt"
				self.current_media_item_file = self.media_list_folder + self.current_media_item_text + self.dot_text
				Create_Text_File(self.current_media_item_file, self.global_switches["create_files"])

				self.media_list_item_names = Create_Array_Of_File(self.media_list_file)

				for media_list_item in self.media_list_item_names:
					media_list_item_folder = self.media_list_folder + Remove_Non_File_Characters(media_list_item) + "/"
					Create_Folder(media_list_item_folder, self.global_switches["create_folders"])

			# Media list folder does not exists
			else:
				self.no_media_list = True

		# No media list for non-series media
		if self.is_series_media == False:
			self.no_media_list = True

		self.media_item = self.media_title
		self.media_item_folder = self.media_folder

		# Media item definition for series media with media list
		if self.is_series_media == True and self.no_media_list == False and self.is_video_series_media == False:
			self.media_item = Create_Array_Of_File(self.current_media_item_file)[0]

		# Media item selection and definition for video series media
		if self.is_video_series_media == True:
			if len(self.media_list_item_names) >= 2:
				self.choice_text = Language_Item_Definer("Select a {} video series", "Selecione uma série de vídeos do {}").format(self.youtube_name)

				self.media_item = Select_Choice_From_List(self.media_list_item_names, alternative_choice_text = self.choice_text, return_first_item = True, add_none = True, first_space = True, second_space = True)

		self.media_item_file_safe = self.media_item

		if self.media_item_file_safe[0] + self.media_item_file_safe[1] == ": ":
			self.media_item_file_safe = self.media_item_file_safe.replace(": ", "")

		self.media_item_file_safe = Remove_Non_File_Characters(self.media_item_file_safe)

		# Media item folder definition for series media with media list
		if self.is_series_media == True and self.no_media_list == False:
			self.media_item_folder = self.media_list_folder + self.media_item_file_safe + "/"
			Create_Folder(self.media_item_folder, self.global_switches["create_folders"])

		# Media item details file and dict definition, is the same as "media_details" if the media has no media list
		self.media_item_details_file = self.media_item_folder + "Media Details" + self.dot_text
		self.media_item_details = Make_Setting_Dictionary(self.media_item_details_file, read_file = True)

		# Titles folder, episode titles files, and commentes folder definition for series media
		if self.is_series_media == True:
			self.titles_folder = self.media_item_folder + self.mixed_titles_text + "/"
			Create_Folder(self.titles_folder, self.global_switches["create_folders"])

			self.english_titles_file = self.titles_folder + full_language_en + self.dot_text
			Create_Text_File(self.english_titles_file, self.global_switches["create_files"])

			self.portuguese_titles_file = self.titles_folder + full_language_pt + self.dot_text
			Create_Text_File(self.portuguese_titles_file, self.global_switches["create_files"])

			self.english_titles = Create_Array_Of_File(self.english_titles_file, add_none = True)
			self.portuguese_titles = Create_Array_Of_File(self.portuguese_titles_file, add_none = True)
			self.media_episode_titles = Language_Item_Definer(self.english_titles, self.portuguese_titles)

			self.comments_folder = self.media_item_folder + self.mixed_comments_text + "/"
			Create_Folder(self.comments_folder, self.global_switches["create_folders"])

		self.has_dub = False

		# Has Dub definition
		if "Has Dub" in self.media_details:
			self.has_dub = Define_Yes_Or_No(self.media_details["Has Dub"])

			if "Watch Dubbed" in self.media_details:
				self.watch_dubbed = Define_Yes_Or_No(self.media_details["Watch Dubbed"])

			if "Watch Dubbed" not in self.media_details:
				self.watch_dubbed = Yes_Or_No_Definer(Language_Item_Definer("Watch dubbed episode", "Assistir episódio dublado"), first_space = False, second_space = False)

		if "Has Dub" not in self.media_details:
			self.watch_dubbed = False

		# Origin Type variables definition for local medias
		if self.origin_type == self.local_english_text:
			self.is_local = True
			self.is_local_episode = True

		# Origin Type variables definition for remote medias
		if self.origin_type == self.remote_english_text:
			self.is_remote = True
			self.is_remote_episode = True

	def Define_Media_Episode_Variables(self):
		# Definition of episode to watch if the media is not series media
		self.media_episode = self.media_details["Original Name"]

		# Definition of episode to watch if the media is series media
		if self.is_series_media == True:
			if self.media_item_details["Episode"] == "None":
				self.first_episode_title = self.portuguese_titles[0]

				self.media_item_details["Episode"] = self.first_episode_title

				if Read_String(self.media_item_details_file) != Stringfy_Dict(self.media_item_details, add_line_break = True):
					Write_To_File(self.media_item_details_file, Stringfy_Dict(self.media_item_details, add_line_break = True), self.global_switches)

			self.media_episode = self.media_item_details["Episode"]

		self.hybrid_origin_type = ""

		# Origin Type variables definition for hybrid medias, getting origin type by each episode name
		if self.origin_type == self.hybrid_english_text:
			self.is_hybrid = True

			# Local episode
			if self.local_english_text in self.media_episode:
				self.media_episode = self.media_episode.split(", " + self.local_english_text)[0]

				self.hybrid_origin_type = ", " + self.local_english_text

				self.is_local_episode = True

			# Remote episode
			if self.remote_english_text in self.media_episode:
				self.media_episode = self.media_episode.split(", " + self.remote_english_text)[0]

				self.hybrid_origin_type = ", " + self.remote_english_text

				self.is_remote_episode = True

		# Remote or hybrid remote media origin, code, and link
		if self.origin_type == self.remote_english_text or self.is_remote_episode == True:
			self.media_remote_origin_name = self.media_item_details["Remote Origin"]
			self.media_remote_origin_code = self.media_item_details["Origin Location"]
			self.media_remote_origin = self.remote_origin_links[self.media_remote_origin_name]

		# Media episode number definition by episode titles file line
		if self.is_series_media == True:
			self.ep_in_episode = False
			self.alternative_episode_type = False

			i = 0
			for line in self.portuguese_titles:
				if line == re.sub(self.mixed_rewatched_regex_text, "", self.media_episode):
					self.media_episode_number = i

				i += 1

			self.media_episode_number_text = str(Add_Leading_Zeros(self.media_episode_number))
			self.media_episode_number_text_backup = self.media_episode_number_text

			one_episode_number = re.findall(self.one_episode_number_regex, self.media_episode)
			one_episode_number_and_bracket = re.findall(self.episode_and_bracket_number, self.media_episode)
			two_episode_numbers = re.findall(self.two_episode_numbers_regex, self.media_episode)

			if self.global_switches["verbose"] == True:
				print()
				print("Backup: " + self.media_episode_number_text_backup)
				print(one_episode_number)
				print(one_episode_number_and_bracket)
				print(two_episode_numbers)

			if one_episode_number != [] and str(one_episode_number[0]) != self.media_episode_number_text_backup:
				self.media_episode_number_text = one_episode_number[0]

			if one_episode_number_and_bracket != [] and one_episode_number_and_bracket[0].split("(")[0] != self.media_episode_number_text_backup:
				self.media_episode_number_text = one_episode_number_and_bracket[0]

			if one_episode_number_and_bracket != [] and one_episode_number_and_bracket[0].split("(")[0] == self.media_episode_number_text_backup:
				self.media_episode_number_text = one_episode_number_and_bracket[0].split(" ")[0].split("(")[1].split(")")[0]

			if two_episode_numbers != []:
				self.media_episode_number_text = two_episode_numbers[0]

			if self.global_switches["verbose"] == True:
				print("Regex: " + self.media_episode_number_text)

			if self.media_episode_number_text !=  self.media_episode_number_text_backup:
				self.media_episode_number_text = self.media_episode_number_text_backup + " (" + self.media_episode_number_text + ")"

			else:
				self.media_episode_number_text = self.media_episode_number_text_backup

			if self.global_switches["verbose"] == True:
				print("With brackets added: " + self.media_episode_number_text)
				print()

		# Adding "Rewatched ?x - Reassistido ?x" text to media episode
		if self.re_watching == True:
			self.media_episode += " " + self.mixed_rewatched_format_text.format("1", "1")

		# Defining the local media folder to use in local or hybrid local media
		if self.is_hybrid == True or self.is_local == True:
			self.local_media_folder = self.local_medias_folder + self.media_title_file_safe + "/"

			if self.no_media_list == False and self.media_item != self.media_title:
				self.local_media_folder += self.media_item_file_safe + "/"

			Create_Folder(self.local_media_folder, self.global_switches["create_folders"])

		self.media_episode_file_safe = Remove_Non_File_Characters(self.media_episode)

		# Define the media item episode as the same as media episode
		self.media_item_episode = self.media_episode

		# Change the media item episode to add media item if media has media list
		if self.no_media_list == False and self.is_video_series_media == False and self.media_item != self.media_title:
			season_text = re.findall(r"^S[0-9][0-9]", self.media_item)

			self.media_item_episode = self.media_item + self.media_episode
			self.media_item_episode_with_title = self.media_title

			if season_text == []:
				self.media_item_episode = self.media_item + " " + self.media_episode

			if ":" not in self.media_item_episode:
				self.media_item_episode_with_title += " "

			self.media_item_episode_with_title += self.media_item_episode

		# Adding channel name to video series media item episode
		if self.no_media_list == False and self.is_video_series_media == True:
			self.media_item_episode = self.media_title + ": " + self.media_episode
			self.media_item_episode_with_title = self.media_title + ": " + self.media_episode

		# Adding media title to media item episode with title
		if self.no_media_list == True and self.is_video_series_media == False:
			self.media_item_episode_with_title = self.media_title + " " + self.media_item_episode

		# Creating dubbed media text and adding dubbed text to media item episode if media is anime and is defined to watch it dubbed
		if self.is_series_media == True and self.english_media_type == self.anime_media_type_english_plural and self.watch_dubbed == True:
			self.dubbed_text_to_title = False

			if "Dubbed To Title" in self.media_details:
				if self.media_details["Dubbed To Title"] == "Yes":
					self.dubbed_text_to_title = True

			if "Dubbed To Title" not in self.media_details:
				self.dubbed_text_to_title = True

			if self.dubbed_text_to_title == True:
				self.dubbed_media_text = ""
				self.dubbed_media_text += " " + self.dubbed_portuguese_text
				self.media_item_episode_with_title = self.media_item_episode_with_title.replace(self.media_title, self.media_title + " " + self.dubbed_portuguese_text)

	def Define_Media_Dict(self):
		self.started_watching_time = time.strftime("%H:%M %d/%m/%Y")

		self.media_dict = {
			"media_title": self.media_title,
			"media_title_file_safe": self.media_title_file_safe,

			"portuguese_media_title": self.portuguese_media_title,

			"media_folder": self.media_folder,
			"media_details": Make_Setting_Dictionary(self.media_details_file, read_file = True),
			"media_details_file": self.media_details_file,

			"media_episode_titles": self.media_episode_titles,

			"media_episode": self.media_episode,
			"media_episode_file_safe": self.media_episode_file_safe,

			"english_media_type": self.english_media_type,
			"portuguese_media_type": self.portuguese_media_type,
			"mixed_media_type": self.mixed_media_type,
			"language_singular_media_type": self.language_singular_media_type,

			"origin_type": self.hybrid_origin_type,

			"per_media_type_files_folder": self.per_media_type_files_folder,
			"per_media_type_episodes_file": self.per_media_type_episodes_file,
			"per_media_type_times_file": self.per_media_type_times_file,

			"is_remote": self.is_remote,
			"is_local": self.is_local,
			"is_hybrid": self.is_hybrid,

			"is_series_media": self.is_series_media,
			"is_video_series_media": self.is_video_series_media,

			"re_watching": self.re_watching,
			"no_media_list": self.no_media_list,
		}

		if self.is_series_media == True:
			self.media_dict["media_episode_number"] = self.media_episode_number
			self.media_dict["media_episode_number_text"] = self.media_episode_number_text
			self.media_dict["comments_folder"] = self.comments_folder

		self.media_dict["media_item"] = self.media_item
		self.media_dict["media_item_file_safe"] = self.media_item_file_safe
		self.media_dict["media_item_episode_with_title"] = self.media_item_episode_with_title
		self.media_dict["media_item_episode"] = self.media_item_episode
		self.media_dict["media_item_folder"] = self.media_item_folder
		self.media_dict["current_media_item_file"] = self.current_media_item_file

		if self.is_series_media == True and self.no_media_list == False:
			self.media_dict["media_item_details"] = self.media_item_details
			self.media_dict["media_item_details_file"] = self.media_item_details_file
			self.media_dict["media_list_item_names"] = self.media_list_item_names

		if self.english_media_type == self.anime_media_type_english_plural and self.watch_dubbed == True:
			self.media_dict["dubbed_media_text"] = self.dubbed_media_text

	def Define_Media_Episode_Unit(self):
		# Remote media episode link definition
		if self.is_remote_episode == True:
			self.media_episode_link = self.media_remote_origin

			# Media episode link definition for Animes Vision website
			if self.media_remote_origin_name == self.animes_vision_name:
				# Add Portuguese media type and origin code (media title) to media episode link
				self.media_episode_link += self.portuguese_media_type.lower() + "/" + self.media_remote_origin_code

				# Add dubbed text
				if self.has_dub == True and self.watch_dubbed == True:
					self.media_episode_link += "-" + self.dubbed_portuguese_text.lower()

				self.media_episode_link += "/"

				# Add episode number
				self.media_episode_link += "episodio-" + self.media_episode_number_text + "/"

			# Media episode link definition for YouTube website
			if self.media_remote_origin_name == self.youtube_name:
				# Add watch and video id to media episode link if it is in the remote origin code
				if "v=" in self.media_remote_origin_code:
					self.media_episode_link += "watch?" + self.media_remote_origin_code

				# Else, add playlist id which is in the remote origin code
				else:
					self.media_episode_link += "playlist?list=" + self.media_remote_origin_code

			self.Media_Unit = self.media_episode_link

			Executor = Open_Link

		# Local media episode file definition
		if self.is_local_episode == True:
			if self.is_series_media == True and self.is_video_series_media == False:
				# Add "Português" text to local media folder if media has dub and watch dubbed is true
				if self.has_dub == True and self.watch_dubbed == True:
					self.local_media_folder += full_language_pt + "/"

			Create_Folder(self.local_media_folder, self.global_switches["create_files"])

			# Remove re-watched text from media episode
			self.media_episode_no_rewatched = re.sub(self.mixed_rewatched_regex_text, "", Remove_Non_File_Characters(self.media_episode))

			# Add media episode to local media folder
			self.media_episode_file = self.local_media_folder + self.media_episode_no_rewatched

			self.file_does_exist = False

			# Check if a media episode file with one of the accepted extensions exist
			for extension in self.accepted_file_extensions:
				file = self.media_episode_file + "." + extension

				if is_a_file(file) == True:
					self.media_episode_file = file

					self.file_does_exist = True

			# If it does not, then, ask if the user wants to move the file from somewhere to the correct folder
			if self.file_does_exist == False:
				print()
				print(self.media_episode_file)
				print()
				print(Language_Item_Definer("The media file does not exist", "O arquivo de mídia não existe") + ".")

				print()

				self.ask_text = Language_Item_Definer("Do you want to bring it from another folder", "Você quer trazer ele de outra pasta")

				self.bring_file = Yes_Or_No_Definer(self.ask_text, first_space = False)

				if self.bring_file == True:
					self.media_episode_file = self.Find_Media_file(self.media_episode)

				if self.bring_file == False:
					quit(Language_Item_Definer("Alright", "Tudo bem") + ".")

			self.Media_Unit = "file:///" + self.media_episode_file

			self.Executor = Open_Video

	def Show_Opening_Media_Info(self):
		# This text defined by language and word gender (this, esse) for non-series, and (this, essa) for series
		self.this_text = self.gender_the_texts[self.mixed_media_type]["this"]

		# The text defined by language and word gender (the, o) for non-series, and (the, a) for series
		self.the_text = self.gender_the_texts[self.mixed_media_type]["the"]

		self.opening_media_text = Language_Item_Definer("Opening {} to watch", "Abrindo {} para assistir").format(self.this_text + " " + self.language_singular_media_type.lower())

		# Show opening this media text
		print(self.opening_media_text + ":")

		# Show media title if the media is not a video series
		if self.is_video_series_media == False:
			print(Language_Item_Definer(self.media_title, self.portuguese_media_title))

		# Show media title if the media is a video series, with channel name (media_title) and video series (media_item)
		if self.is_video_series_media == True:
			print(self.media_title + self.media_type_separator + self.media_item)

		# Show media episode if the media is series media (not a movie)
		if self.is_series_media == True:
			self.watched_media_container_type = Language_Item_Definer("season", "temporada")

			if self.is_video_series_media == True:
				self.watched_media_container_type = Language_Item_Definer("{} channel", "canal do {}").format(self.youtube_name)

			print()
			print(Language_Item_Definer("And this episode", "E esse episódio") + ":")
			print(self.media_episode)
			print()

			# Show media item episode (media episode with media item) if the media has a media list
			if self.no_media_list == False:
				print(Language_Item_Definer("Episode with {}", "Episódio com {}").format(self.watched_media_container_type) + ": ")

				media_item_episode = self.media_item_episode

				if ": " in self.media_item_episode:
					media_item_episode = self.media_item_episode.replace(": ", "")

				print(media_item_episode)
				print()

		# Show media type
		print(Language_Item_Definer("Media type", "Tipo de mídia") + ":")
		print(Language_Item_Definer(self.english_media_type, self.portuguese_media_type))
		print()

		# Show mixed media type
		if self.english_media_type != self.anime_media_type_english_plural:
			print(Language_Item_Definer("Mixed media type", "Tipo de mídia misturado") + ":")
			print(self.mixed_media_type)
			print()

		self.media_unit_text = Language_Item_Definer("Media Unit", "Unidade de Mídia") + ":"

		# Show media unit text and Media_Unit
		print(self.media_unit_text)
		print(self.Media_Unit)

	def Open_Media_Unit(self):
		# Open media unit with its executor
		if self.global_switches["testing_script"] == False:
			self.Executor(self.Media_Unit)

	# Make Custom Discord Status for the media episode that is going to be watched and copy  it
	def Make_Discord_Status(self):
		self.discord_status_text_template = "Assistindo {}: {}"

		self.discord_status = self.discord_status_text_template.format(self.language_singular_media_type, self.media_item_episode_with_title)

		Copy_Text(self.discord_status)

	def Comment_On_Media(self):
		# Ask to comment on media (inside Write_Comment class)
		Write_Comment(self.media_dict)

	def Register_Media(self):
		self.finished_watching_media_text_template = Language_Item_Definer("Press Enter when you finish watching the {}", "Pressione Enter quando você terminar de assistir {}")

		# Text to show in the input when the user finishes watching the media (pressing Enter)
		self.finished_watching_media_text = self.finished_watching_media_text_template.format(self.the_text + " " + self.language_singular_media_type)

		self.finished_watching = Select_Choice(self.finished_watching_media_text, accept_enter = True, enter_equals_empty = True, second_space = False)

		# Register finished watching time
		self.finished_watching_time = time.strftime("%H:%M %d/%m/%Y")

		self.media_dict["started_watching_time"] = self.started_watching_time
		self.media_dict["finished_watching_time"] = self.finished_watching_time

		# Ask for YouTube Video ID to user
		if self.is_video_series_media == True:
			self.youtube_video_id = Select_Choice(Language_Item_Definer("Paste the YouTube Video URL", "Cole o link do vídeo do YouTube"), second_space = False)
			self.youtube_video_id = self.youtube_video_id.split("watch?v=")[1].split("&list=")[0]

			self.media_dict["youtube_video_id"] = self.youtube_video_id

		# Use "Register_Watched_Media" class to register watched media, running it as a module, and giving the media_dict to it
		Register_Watched_Media(run_as_module = True, media_dict = self.media_dict)

	def Find_Media_file(self, episode_file_name):
		self.episode_file_name = episode_file_name

		self.downloads_folder = Sanitize_File_Path(expanduser("~")) + "Downloads/"
		self.downloads_videos_folder = self.downloads_folder + "Videos/"
		self.mega_downloads_folder = self.downloads_folder + "Mega/"

		self.frequently_used_folders = [
			self.downloads_folder,
			self.downloads_videos_folder,
			self.mega_downloads_folder,
		]

		self.old_file = Select_Folder_And_Media_File(self.frequently_used_folders)

		self.moved_succesfully = False

		if self.old_file.split(".")[1] not in self.accepted_file_extensions:
			while self.old_file.split(".")[1] not in self.accepted_file_extensions:
				print()
				print(Language_Item_Definer("Please select a file that is either MP4 or MKV", "Selecione um arquivo que seja MP4 ou MKV") + ".")

				self.old_file = Select_Folder_And_Media_File(self.frequently_used_folders)

				self.new_file = self.local_media_folder + self.episode_file_name + "." + "{}"

		if self.media_file.split(".")[1] in self.accepted_file_extensions:
			Move_Media_File(self.old_file, self.new_file)

		if self.moved_succesfully == True:
			self.Media_Unit = self.new_file

			return self.Media_Unit

		if self.moved_succesfully == False:
			quit()

	def Select_Folder_And_Media_File(self, folders):
		self.search_folder_text = Language_Item_Definer("Select one folder to search for the file", "Selecione uma pasta para procurar pelo arquivo")

		self.media_file_location = Select_Choice_From_List(folders, local_script_name, self.search_folder_text, return_first_item = True, first_space = False)

		self.files_on_folder = List_Files(self.media_file_location, add_none = False)

		self.select_media_file_text = Language_Item_Definer("Select the media file", "Selecione o arquivo da mídia")

		return Select_Choice_From_List(self.files_on_folder, local_script_name, self.select_media_file_text, return_first_item = True, first_space = False, second_space = False, add_none = True)

	def Move_Media_File(self, old_file, new_file):
		self.old_file = old_file
		self.new_file = new_file

		for extension in self.accepted_file_extensions:
			if extension in file:
				self.extension = extension

		self.new_file = self.new_file.format(self.extension)

		Move_File(self.old_file, self.new_file)

		self.moved_succesfully = True