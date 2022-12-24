# Watch_Media.py

from Watch_History.Watch_History import Watch_History as Watch_History

from Watch_History.Register_Watched_Media import Register_Watched_Media as Register_Watched_Media
from Watch_History.Comment_Writer import Comment_Writer as Comment_Writer

import re
from urllib.parse import urlparse, parse_qs

# A class to Watch media that has the "Watching" or "Re-Watching" Watching Status
class Watch_Media(Watch_History):
	def __init__(self, run_as_module = False, open_media = True, media_list = None, status_text = None, option_info_parameter = None):
		super().__init__()

		self.run_as_module = run_as_module
		self.open_media = open_media
		self.media_list = media_list
		self.status_text = status_text

		self.option_info_parameter = option_info_parameter

		if self.option_info_parameter != None:
			self.option_info = self.option_info_parameter

		self.Define_Media_Type_Variables()

		self.media_dictionary = {}

		self.Define_Media_Variables()

		if self.open_media == False:
			self.Define_Media_Episode_Variables()
			self.Define_Media_Dictionary()

		if self.open_media == True:
			self.Define_Media_Episode_Variables()
			self.Define_Media_Dictionary()
			self.Define_Media_Episode_Unit()
			self.Show_Opening_Media_Info()
			self.Open_Media_Unit()
			self.Make_Discord_Status()
			self.Comment_On_Media()
			self.Register_Media()

	def Define_Media_Type_Variables(self):
		if self.option_info == None:
			self.lists_dict = {}

			self.lists_dict["media_list"] = self.media_list

			if self.status_text == None:
				self.status_text = [
					self.language_texts["watching, title()"],
					self.language_texts["re_watching, title()"],
				]

			self.option_info = self.Select_Media_Type_And_Media(self.lists_dict, status_text = self.status_text)

		# Media Type variables definition
		self.plural_media_types = self.option_info["plural_media_type"]
		self.singular_media_types = self.option_info["singular_media_type"]
		self.mixed_plural_media_type = self.option_info["mixed_plural_media_type"]

		# Per Media Type files folder, times file, and episodes file
		self.per_media_type_files_folder = self.per_media_type_files_folders[self.plural_media_types["en"]]
		self.per_media_type_times_file = self.per_media_type_time_files[self.plural_media_types["en"]]
		self.per_media_type_episodes_file = self.per_media_type_episode_files[self.plural_media_types["en"]]

		watching_status_files = self.option_info["watching_status_files"]
		watching_status_media = self.option_info["watching_status_media"]

	def Define_Media_Variables(self):
		# Media variables definition (folder, details file, and details)
		self.media_folder = self.option_info["media_folder"]
		self.media_details_file = self.option_info["media_details_file"]
		self.media_details = self.File.Dictionary(self.media_details_file)
		self.media_titles_list = self.option_info["media_titles"]

		if self.global_switches["verbose"] == True and self.open_media == True:
			print()
			print(self.language_texts["media_folder"] + ":")
			print(self.media_folder)
			print()

			print(self.language_texts["media_details"] + ":")
			print(self.Language.Python_To_JSON(self.media_details))

			print()
			print(self.language_texts["media_details_file"] + ":")
			print(self.media_details_file)

		# Media title and Portuguese media title variables
		self.media_title = self.media_titles_list["original"]

		if self.plural_media_types["en"] == self.texts["animes"]["en"]:
			self.media_title = self.media_titles_list["romanized"]

		if " (" in self.media_titles_list["original"] and " (" not in self.media_titles_list["language"]:
			self.media_titles_list["language"] = self.media_titles_list["language"] + " (" + self.media_titles_list["original"].split(" (")[-1]

			if self.user_language in self.media_titles_list:
				self.media_titles_list[self.user_language] = self.media_titles_list[self.user_language] + " (" + self.media_titles_list["original"].split(" (")[-1]

		self.media_title_file_safe = self.Sanitize(self.media_title, restricted_characters = True)

		self.media_watching_status = self.media_details[self.language_texts["status, title()"]]

		self.origin_type = self.media_details[self.language_texts["origin_type"]]

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
		if self.plural_media_types["en"] == self.texts["plural_media_types, type: list"]["en"][3]:
			self.is_series_media = False

		if self.plural_media_types["en"] == self.texts["plural_media_types, type: list"]["en"][4]:
			self.is_video_series_media = True

		if self.media_watching_status == self.language_texts["re_watching, title()"]:
			self.re_watching = True

		self.no_media_list = False

		self.current_media_item_file = None

		if self.is_series_media == False:
			self.movie_details_file = self.option_info["movie_details_file"]
			self.movie_details = self.option_info["movie_details"]

		# Media list definition for series media
		if self.is_series_media == True:
			self.media_list_text = self.media_type_sub_folders[self.plural_media_types["en"]]["media_list_text"]
			self.singular_media_list_text = self.media_type_sub_folders[self.plural_media_types["en"]]["english_singular_media_list_text"]
			self.current_media_item_text = "Current " + self.singular_media_list_text

			self.media_list_folder = self.media_folder + self.media_list_text + "/"

			# Media list folder exists
			if self.Folder.Exist(self.media_list_folder) == True:
				# "Seasons - Temporadas.txt" or "Series - Séries.txt"
				self.media_list_file = self.media_list_folder + self.media_list_text + ".txt"
				self.File.Create(self.media_list_file)

				# "Current season.txt" or "Current series.txt"
				self.current_media_item_file = self.media_list_folder + self.current_media_item_text + ".txt"
				self.File.Create(self.current_media_item_file)

				self.media_list_item_names = self.File.Contents(self.media_list_file)["lines"]

				for media_list_item in self.media_list_item_names:
					if media_list_item[0] + media_list_item[1] == ": ":
						media_list_item = media_list_item[2:]

					media_list_item_folder = self.media_list_folder + self.Sanitize(media_list_item, restricted_characters = True) + "/"
					self.Folder.Create(media_list_item_folder)

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
			self.media_item = self.File.Contents(self.current_media_item_file)["lines"][0]

		# Select video series from channel for video series media
		if self.is_video_series_media == True and len(self.media_list_item_names) >= 2:
			self.show_text = self.Text.Capitalize(self.language_texts["youtube_video_series"])
			self.select_text = self.language_texts["select_a_youtube_video_series"]

			if self.option_info_parameter == False:
				self.media_item = self.Input.Select(self.media_list_item_names, show_text = self.show_text, select_text = self.select_text)["option"]

			if self.option_info_parameter == True:
				self.media_item = self.media_list_item_names[0]

		self.media_item_file_safe = self.media_item

		if self.media_item_file_safe[0] + self.media_item_file_safe[1] == ": ":
			self.media_item_file_safe = self.media_item_file_safe[2:]

		self.media_item_file_safe = self.Sanitize(self.media_item_file_safe, restricted_characters = True)

		# Media item folder definition for series media with media list
		if self.is_series_media == True and self.no_media_list == False:
			self.media_item_folder = self.media_list_folder + self.media_item_file_safe + "/"
			self.Folder.Create(self.media_item_folder)

		# Media item details file and dict definition, is the same as "media_details" if the media has no media list
		self.media_item_details_file = self.media_item_folder + "Media details.txt"
		self.media_item_details = self.File.Dictionary(self.media_item_details_file)

		self.media_dates_file = self.media_item_folder + self.texts["dates, title(), en - pt"] + ".txt"

		dict_ = {
			"media_details_file": self.media_item_details_file,
			"plural_media_types": self.plural_media_types,
		}

		self.language_media_item = self.Define_Media_Titles(dict_)["media_titles"]

		for language in self.small_languages:
			string = self.language_media_item["original"]

			if self.plural_media_types["en"] == self.texts["animes"]["en"]:
				if "romanized" in self.language_media_item:
					string = self.language_media_item["romanized"]

			if language in self.language_media_item:
				string = self.language_media_item[language]

			self.language_media_item[language] = {
				"title": string,
			}				

		self.language_media_item["language"] = self.language_media_item[self.user_language]

		self.language_episode_titles = None

		# Titles folder, episode titles files, and commentes folder definition for series media
		if self.is_series_media == True:
			self.titles_folder = self.media_item_folder + self.texts["titles, title(), en - pt"] + "/"
			self.Folder.Create(self.titles_folder)

			self.episode_titles_files = {}
			self.episode_titles = {}

			for language in self.small_languages:
				full_language = self.full_languages[language]

				self.episode_titles_files[language] = self.titles_folder + full_language + ".txt"
				self.File.Create(self.episode_titles_files[language])

				self.episode_titles[language] = self.File.Contents(self.episode_titles_files[language])["lines"]

			self.language_episode_titles = self.Language.Item(self.episode_titles)

			self.comments_folder = self.media_item_folder + self.texts["comments, title(), en - pt"] + "/"
			self.Folder.Create(self.comments_folder)

		self.has_dub = False

		# Has dub definition
		if self.language_texts["has_dub"] in self.media_details:
			self.has_dub = self.Input.Define_Yes_Or_No(self.media_details[self.language_texts["has_dub"]])

			if self.language_texts["watch_dubbed"] in self.media_details:
				self.watch_dubbed = self.Input.Define_Yes_Or_No(self.media_details[self.language_texts["watch_dubbed"]])

			if self.language_texts["watch_dubbed"] not in self.media_details:
				if self.open_media == True:
					self.watch_dubbed = self.Input.Yes_Or_No(self.language_texts["watch_the_dubbed_episode_in_your_language"])

				if self.open_media == False:
					self.watch_dubbed = False

		if self.language_texts["has_dub"] not in self.media_details:
			self.watch_dubbed = False

		# Origin type variables definition for local medias
		if self.origin_type == self.texts["local, title()"]["en"]:
			self.is_local = True
			self.is_local_episode = True

		# Origin type variables definition for remote medias
		if self.origin_type == self.texts["remote, title()"]["en"]:
			self.is_remote = True
			self.is_remote_episode = True

	def Define_Media_Episode_Variables(self):
		# Definition of episode to watch if the media is not series media
		self.media_episode = self.media_details[self.language_texts["original_name"]]

		# Definition of episode to watch if the media is series media
		if self.is_series_media == True:
			if self.media_item_details[self.language_texts["episode, title()"]] == "None" or self.media_item_details[self.language_texts["episode, title()"]] == None:
				self.first_episode_title = self.Language.Item(self.episode_titles)

				if self.first_episode_title != []:
					self.first_episode_title = self.first_episode_title[0]

				self.media_item_details[self.language_texts["episode, title()"]] = self.first_episode_title

				self.File.Edit(self.media_item_details_file, self.Text.From_Dictionary(self.media_item_details), "w")

			self.media_episode = self.media_item_details[self.language_texts["episode, title()"]]

		self.hybrid_origin_type = ""

		# Origin type variables definition for hybrid medias, getting origin type by each episode name
		if self.origin_type == self.texts["hybrid, title()"]["en"]:
			self.is_hybrid = True

			# Local episode
			if self.texts["local, title()"]["en"] in self.media_episode:
				self.media_episode = self.media_episode.split(", " + self.texts["local, title()"]["en"])[0]

				self.hybrid_origin_type = ", " + self.texts["local, title()"]["en"]

				self.is_local_episode = True

			# Remote episode
			if self.texts["remote, title()"]["en"] in self.media_episode:
				self.media_episode = self.media_episode.split(", " + self.texts["remote, title()"]["en"])[0]

				self.hybrid_origin_type = ", " + self.texts["remote, title()"]["en"]

				self.is_remote_episode = True

		# Remote or hybrid remote media origin, code, and link
		if self.language_texts["remote_origin, title()"] in self.media_details or self.language_texts["remote_origin, title()"] in self.media_item_details:
			values = {}

			for item in ["remote_origin, title()", "origin_location, title()"]:
				if self.language_texts[item] in self.media_details:
					values[item] = self.media_details[self.language_texts[item]]

				if self.language_texts[item] in self.media_item_details:
					values[item] = self.media_item_details[self.language_texts[item]]

				if self.language_texts[item] not in self.media_details and self.language_texts[item] not in self.media_item_details:
					values[item] = ""

			self.remote_data = {
				"name": values["remote_origin, title()"],
				"origin_code": values["origin_location, title()"],
			}

			if self.remote_data["origin_code"] == "":
				if self.plural_media_types["en"] == self.texts["animes"]["en"]:
					self.remote_data["origin_code"] = self.Sanitize(self.media_title.lower(), restricted_characters = True)
					self.remote_data["origin_code"] = self.remote_data["origin_code"].replace(" ", "-")
					self.remote_data["origin_code"] = self.remote_data["origin_code"].replace("!", "")
					self.remote_data["origin_code"] = self.remote_data["origin_code"].replace(",", "")
					self.remote_data["origin_code"] = self.remote_data["origin_code"].replace("△", "")

			self.remote_data["origin"] = self.remote_origins[self.remote_data["name"]]

		self.one_episode_number_regex = r"[0-9][0-9]"
		self.two_episode_numbers_regex = r"[0-9][0-9]\-[0-9][0-9]"
		self.episode_and_bracket_number = r"[0-9][0-9]\([0-9][0-9]\)"

		self.language_media_episode = self.media_episode

		if self.is_series_media == False:
			self.language_media_episode = self.media_titles_list["language"]

		# Media episode number definition by episode titles file line
		if self.is_series_media == True:
			media_episode = self.media_episode

			if re.sub(self.texts["re_watched, type: regex, en - pt"], "", self.media_episode) != None:
				media_episode = re.sub(self.texts["re_watched, type: regex, en - pt"], "", self.media_episode)

			i = 1
			for line in self.language_episode_titles:
				if line in media_episode:
					self.media_dictionary["episode_number"] = i

				i += 1

			self.media_dictionary["episode_number_text"] = str(self.Text.Add_Leading_Zeros(self.media_dictionary["episode_number"]))
			self.media_episode_number_text_backup = self.media_dictionary["episode_number_text"]

			one_episode_number = re.findall(self.one_episode_number_regex, self.media_episode)
			one_episode_number_and_bracket = re.findall(self.episode_and_bracket_number, self.media_episode)
			two_episode_numbers = re.findall(self.two_episode_numbers_regex, self.media_episode)

			if one_episode_number != [] and str(one_episode_number[0]) != self.media_episode_number_text_backup:
				self.media_dictionary["episode_number_text"] = one_episode_number[0]

			if one_episode_number_and_bracket != [] and one_episode_number_and_bracket[0].split("(")[0] != self.media_episode_number_text_backup:
				self.media_dictionary["episode_number_text"] = one_episode_number_and_bracket[0]

			if one_episode_number_and_bracket != [] and one_episode_number_and_bracket[0].split("(")[0] == self.media_episode_number_text_backup:
				self.media_dictionary["episode_number_text"] = one_episode_number_and_bracket[0].split(" ")[0].split("(")[1].split(")")[0]

			if two_episode_numbers != []:
				self.media_dictionary["episode_number_text"] = two_episode_numbers[0]

			if self.media_dictionary["episode_number_text"] != self.media_episode_number_text_backup:
				self.media_dictionary["episode_number_text"] = self.media_episode_number_text_backup + " (" + self.media_dictionary["episode_number_text"] + ")"

		self.youtube_video_id = None

		if self.is_video_series_media == True:
			self.youtube_video_ids_file = self.media_item_folder + self.texts["youtube_ids"]["en"] + ".txt"
			self.youtube_video_ids = self.File.Contents(self.youtube_video_ids_file)["lines"]

			if self.youtube_video_ids != []:
				self.youtube_video_id = self.youtube_video_ids[self.media_dictionary["episode_number"] - 1]

		self.re_watched_string = ""

		# Adding "Re-Watched ?x - Re-Assistido ?x" text to media episode
		if self.re_watching == True:
			if self.run_as_module == False:
				print()
				print(self.media_titles_list["language"] + " " + self.media_episode)

				self.watched_times = self.Input.Type(self.language_texts["type_the_number_of_times_that_you_watched"], accept_enter = False)

			if self.run_as_module == True:
				self.watched_times = 1

			if int(self.watched_times) != 0:
				if int(self.watched_times) != 1:
					self.re_watched_times = str(int(self.watched_times) + 1)

				else:
					self.re_watched_times = str(self.watched_times)

				self.re_watched_string = self.texts["re_watched, type: format, en - pt"].format(self.re_watched_times, self.re_watched_times)
				self.media_episode += " " + self.re_watched_string

				self.language_re_watched_string = self.language_texts["re_watched, type: format"].format(self.re_watched_times)
				self.language_media_episode += " " + self.language_re_watched_string

			if int(self.watched_times) == 0:
				self.re_watching = False

		# Defining the local media folder to use in local or hybrid local media
		if self.is_hybrid == True or self.is_local == True:
			self.local_media_folder = self.root_folders["media"] + self.media_title_file_safe + "/"

			if self.no_media_list == False and self.media_item != self.media_title:
				self.local_media_folder += self.media_item_file_safe + "/"

			self.Folder.Create(self.local_media_folder)

		self.media_episode_file_safe = self.Sanitize(self.media_episode, restricted_characters = True)

		# Define the media item episode as the same as media episode
		self.media_item_episode = self.media_episode
		self.media_item_episode_with_title = self.media_item_episode

		# Change the media item episode to add media item if media has media list
		if self.no_media_list == False and self.is_video_series_media == False and self.is_series_media == True and self.media_item != self.media_title:
			separators = {
				"title_separator": None,
				"episode_separator": None,
			}

			for item in ["title_separator", "episode_separator"]:
				if self.language_texts[item] in self.media_details:
					separators[item] = self.media_details[self.language_texts[item]]

			season_text = re.findall(r"^S[0-9][0-9]", self.media_item)

			space = ""

			if season_text == [] or \
			   season_text != [] and "EP" not in self.media_episode and re.findall(r"E[0-9][0-9]", self.media_episode) == []:
				space = " "

			if separators["episode_separator"] != None:
				space = separators["episode_separator"]

			self.media_item_episode = self.media_item + space + self.media_episode

			self.media_item_episode_with_title = ""

			if self.media_title not in self.media_item:
				self.media_item_episode_with_title += self.media_title

			if self.media_title in self.media_item:
				self.media_item_episode_with_title += self.media_item

			if ":" not in self.media_item_episode and separators["title_separator"] == None:
				self.media_item_episode_with_title += " "

			if separators["title_separator"] != None:
				self.media_item_episode_with_title += separators["title_separator"]

			if self.media_title not in self.media_item:
				self.media_item_episode_with_title += self.media_item

				if separators["episode_separator"] == None and season_text == [] or \
				   season_text != [] and "EP" not in self.media_episode and re.findall(r"E[0-9][0-9]", self.media_episode) == []:
					self.media_item_episode_with_title += " "

				if separators["episode_separator"] != None:
					self.media_item_episode_with_title += separators["episode_separator"]

				self.media_item_episode_with_title += self.media_episode

			if self.media_title in self.media_item:
				self.media_item_episode_with_title += self.media_episode

		if self.is_series_media == True:
			if self.is_video_series_media == False and self.media_item == self.media_title:
				self.media_item_episode = self.media_title + " " + self.media_episode
				self.media_item_episode_with_title = self.media_title + " " + self.media_episode

			# Adding channel name to video series media item episode
			if self.no_media_list == False and self.is_video_series_media == True:
				self.media_item_episode = self.media_title + ": " + self.media_episode
				self.media_item_episode_with_title = self.media_title + ": " + self.media_episode

		for language in self.small_languages:
			language_name = self.texts["[language]_name"][language]

			self.language_media_item[language]["episode"] = self.media_item_episode
			self.language_media_item[language]["episode_with_title"] = self.media_item_episode_with_title

			if self.media_title in self.language_media_item[language]["episode_with_title"] and language in self.media_titles_list:
				self.language_media_item[language]["episode_with_title"] = self.language_media_item[language]["episode_with_title"].replace(self.media_title, self.media_titles_list[language])

			if self.media_item in self.language_media_item[language]["episode"]:
				self.language_media_item[language]["episode"] = self.language_media_item[language]["episode"].replace(self.media_item, self.language_media_item[language]["title"])

			if self.media_item in self.language_media_item[language]["episode_with_title"]:
				self.language_media_item[language]["episode_with_title"] = self.language_media_item[language]["episode_with_title"].replace(self.media_item, self.language_media_item[language]["title"])

		self.language_media_item["language"]["episode"] = self.language_media_item[self.user_language]["episode"]
		self.language_media_item["language"]["episode_with_title"] = self.language_media_item[self.user_language]["episode_with_title"]

		# Creating dubbed media text and adding dubbed text to media item episode if media is anime and is defined to watch it dubbed
		if self.plural_media_types["en"] == self.texts["animes"]["en"] and self.watch_dubbed == True:
			self.dubbed_text_to_title = False

			if self.language_texts["dubbed_to_title"] in self.media_details and self.media_details[self.language_texts["dubbed_to_title"]] == "Yes":
				self.dubbed_text_to_title = True

			if self.language_texts["dubbed_to_title"] not in self.media_details:
				self.dubbed_text_to_title = True

			if self.dubbed_text_to_title == True:
				self.dubbed_media_text = ""
				self.dubbed_media_text += " " + self.language_texts["dubbed"]
				self.media_item_episode_with_title = self.media_item_episode_with_title.replace(self.media_title, self.media_title + " " + self.language_texts["dubbed"])

	def Define_Media_Dictionary(self):
		self.media_dictionary.update({
			"media_title": self.media_title,
			"media_titles": self.media_titles_list,
			"media_title_file_safe": self.media_title_file_safe,

			"media_folder": self.media_folder,
			"media_details": self.File.Dictionary(self.media_details_file),
			"media_details_file": self.media_details_file,

			"media_episode": self.media_episode,
			"media_episode_file_safe": self.media_episode_file_safe,
			"language_media_episode": self.language_media_episode,
			"youtube_video_id": self.youtube_video_id,
			"started_watching_time": self.Date.Now()["strftime"],

			"plural_media_types": self.plural_media_types,
			"singular_media_types": self.singular_media_types,
			"mixed_plural_media_type": self.mixed_plural_media_type,

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
			"re_watched_string": self.re_watched_string,
			"no_media_list": self.no_media_list,
		})

		self.media_dictionary["the_text"], self.media_dictionary["this_text"], self.media_dictionary["of_text"], self.media_dictionary["of_the_text"] = self.Define_The_Text(self.plural_media_types)
		self.media_dictionary["the_item_text"] = self.media_dictionary["the_text"]
		self.media_dictionary["the_unit_text"] = self.gender_the_texts[self.plural_media_types["en"]]["masculine"]["the"]

		self.media_dictionary["media_container_name"] = self.singular_media_types["language"].lower()
		self.media_dictionary["media_item_name"] = self.singular_media_types["language"].lower()
		self.media_dictionary["media_unit_name"] = self.singular_media_types["language"].lower()

		if self.is_series_media == True:
			self.media_dictionary["the_item_text"] = self.gender_the_texts[self.plural_media_types["en"]]["feminine"]["the"]
			self.media_dictionary["media_unit_name"] = self.language_texts["episode"]

			if self.no_media_list == False:
				self.media_dictionary["media_item_name"] = self.language_texts["season"]

			if self.is_video_series_media == True:
				self.media_dictionary["media_container_name"] = self.language_texts["youtube_channel"]
				self.media_dictionary["media_item_name"] = self.language_texts["youtube_video_serie"]
				self.media_dictionary["media_unit_name"] = self.language_texts["video"]

		self.media_dictionary["header_text"] = self.language_texts["opening_{}_to_watch"].format(self.media_dictionary["this_text"] + " " + self.media_dictionary["media_container_name"]) + ":"

		if self.is_series_media == True:
			self.media_dictionary["episode_titles_files"] = self.episode_titles_files
			self.media_dictionary["episode_titles"] = self.episode_titles
			self.media_dictionary["language_episode_titles"] = self.language_episode_titles
			self.media_dictionary["comments_folder"] = self.comments_folder

		self.media_dictionary["media_item"] = self.media_item
		self.media_dictionary["language_media_item"] = self.language_media_item
		self.media_dictionary["media_item_file_safe"] = self.media_item_file_safe
		self.media_dictionary["media_item_episode_with_title"] = self.media_item_episode_with_title
		self.media_dictionary["media_item_episode"] = self.media_item_episode
		self.media_dictionary["media_item_folder"] = self.media_item_folder
		self.media_dictionary["current_media_item_file"] = self.current_media_item_file

		if self.is_series_media == True and self.no_media_list == False:
			self.media_dictionary["media_item_details"] = self.media_item_details
			self.media_dictionary["media_item_details_file"] = self.media_item_details_file
			self.media_dictionary["media_list_item_names"] = self.media_list_item_names
			self.media_dictionary["media_list_folder"] = self.media_list_folder

		if self.plural_media_types["en"] == self.texts["animes"]["en"] and self.watch_dubbed == True:
			self.media_dictionary["dubbed_media_text"] = self.dubbed_media_text

	def Define_Media_Episode_Unit(self):
		self.accepted_file_extensions = [
			"mp4",
			"mkv",
			"webm",
		]

		# Remote media episode link definition
		if self.language_texts["remote_origin, title()"] in self.media_item_details:
			self.media_dictionary["media_link"] = self.remote_data["origin"]

			# Media episode link definition for Animes Vision website
			if self.remote_data["name"] == "Animes Vision":
				# Add Portuguese media type and origin code (media title) to media episode link
				self.media_dictionary["media_link"] += self.plural_media_types["pt"].lower() + "/" + self.remote_data["origin_code"]

				# Add dubbed text
				if self.has_dub == True and self.watch_dubbed == True:
					self.media_dictionary["media_link"] += "-" + self.texts["dubbed"]["pt"].lower()

				self.media_dictionary["media_link"] += "/"

				# Add episode number
				self.media_dictionary["media_link"] += "episodio-" + str(self.Text.Add_Leading_Zeros(self.media_dictionary["episode_number"])) + "/"

				# Add dubbed text to media link if the media has a dub in the user language and user wants to watch it dubbed
				if self.has_dub == True and self.watch_dubbed == True:
					self.media_dictionary["media_link"] += self.texts["dubbed"]["pt"]

				# Add subbed text to media link if there is no dub for the media or the user wants to watch it subbed
				if self.has_dub == False or self.watch_dubbed == False:
					self.media_dictionary["media_link"] += self.texts["subbed"]["pt"]

			# Media episode link definition for YouTube website
			if self.remote_data["name"] == "YouTube":
				# Add watch and video id to media episode link if it is in the remote origin code
				if "v=" not in self.media_remote_origin_code:
					self.media_dictionary["media_link"] += "watch?v=" + self.media_dictionary["youtube_video_id"] + "&list=" + self.remote_data["origin_code"] + "&index=" + str(self.media_dictionary["episode_number"])

				if "v=" in self.remote_data["origin_code"]:
					self.media_dictionary["media_link"] += "watch?" + self.remote_data["origin_code"]

			self.media_dictionary["media_unit"] = self.media_dictionary["media_link"]

			if self.is_remote_episode == True:
				self.Executor = self.Text.Open_Link

		# Local media episode file definition
		if self.is_local_episode == True:
			if self.is_series_media == True and self.is_video_series_media == False:
				# Add "Português" text to local media folder if media has dub and watch dubbed is true
				if self.has_dub == True and self.watch_dubbed == True:
					self.local_media_folder += self.full_user_language + "/"

			self.Folder.Create(self.local_media_folder)

			# Remove re-watched text from media episode
			self.media_episode_no_re_watched = re.sub(" " + self.texts["re_watched, type: regex, en - pt"], "", self.media_episode_file_safe)

			# Add media episode to local media folder
			self.media_dictionary["media_file"] = "file:///" + self.local_media_folder + self.media_episode_no_re_watched

			self.file_does_exist = False

			# Check if a media episode file with one of the accepted extensions exist
			for extension in self.accepted_file_extensions:
				file = self.media_dictionary["media_file"] + "." + extension

				if self.File.Exist(file.replace("file:///", "")) == True:
					self.media_dictionary["media_file"] = file

					self.file_does_exist = True

			# If it does not, then, ask if the user wants to move the file from somewhere to the correct folder
			if self.file_does_exist == False:
				print()
				print(self.media_dictionary["media_file"])
				print()
				print(self.language_texts["the_media_file_does_not_exist"] + ".")
				print()

				self.ask_text = self.language_texts["do_you_want_to_bring_it_from_another_folder"]

				self.bring_file = self.Input.Yes_Or_No(self.ask_text, first_space = False)

				if self.bring_file == True:
					self.media_dictionary["media_file"] = self.Find_Media_file(self.media_episode)

				if self.bring_file == False:
					print()
					quit(self.language_texts["alright"] + ".")

			self.media_dictionary["media_unit"] = self.media_dictionary["media_file"]

			self.Executor = self.File.Open

	def Show_Opening_Media_Info(self):
		if self.is_video_series_media == False and self.Today_Is_Christmas() == True:
			self.media_dictionary["media_unit_name"] = self.language_texts["christmas_special_{}"].format(self.media_dictionary["media_unit_name"])

		self.Show_Media_Information(self.media_dictionary)

	def Open_Media_Unit(self):
		# Open media unit with its executor
		if self.global_switches["testing"] == False:
			if self.is_remote_episode == True:
				self.Executor(self.media_dictionary["media_unit"])

			if self.is_local_episode == True:
				import subprocess
				subprocess.Popen('"C:\Program Files (x86)\Mozilla Firefox\Firefox.exe" ' + '"' + self.media_dictionary["media_unit"] + '"')

	# Make Custom Discord Status for the media episode that is going to be watched and copy  it
	def Make_Discord_Status(self):
		self.discord_status_text_template = self.language_texts["watching, title()"]

		self.discord_status = self.discord_status_text_template + " " + self.singular_media_types["language"] + ": " + self.language_media_item["language"]["episode_with_title"]

		self.Text.Copy(self.discord_status)

	def Comment_On_Media(self):
		# Ask to comment on media (using Comment_Writer class)
		Comment_Writer(self.media_dictionary)

	def Register_Media(self):
		self.finished_watching_media_text_template = self.language_texts["press_enter_when_you_finish_watching_the_{}"]

		# Text to show in the input when the user finishes watching the media (pressing Enter)
		self.finished_watching_media_text = self.finished_watching_media_text_template.format(self.media_dictionary["the_unit_text"] + " " + self.media_dictionary["media_unit_name"])

		self.finished_watching = self.Input.Type(self.finished_watching_media_text)

		# Register finished watching time
		self.media_dictionary["finished_watching"] = self.Date.Now()["strftime"]

		# Use "Register_Watched_Media" class to register watched media, running it as a module, and giving the media_dictionary to it
		Register_Watched_Media(run_as_module = True, media_dictionary = self.media_dictionary)

	def Find_Media_file(self, episode_file_name):
		self.episode_file_name = episode_file_name

		self.frequently_used_folders = [
			self.user_folders["downloads"]["root"],
			self.user_folders["downloads"]["videos"],
			self.user_folders["downloads"]["mega"],
		]

		self.old_file = self.Select_Folder_And_Media_File(self.frequently_used_folders)

		self.new_file = self.local_media_folder + self.Sanitize(self.episode_file_name, restricted_characters = True) + "."

		if self.old_file.split(".")[1] not in self.accepted_file_extensions:
			while self.old_file.split(".")[1] not in self.accepted_file_extensions:
				print()
				print(self.language_texts["please_select_a_file_that_is_either_mp4_or_mkv"] + ".")

				self.old_file = self.Select_Folder_And_Media_File(self.frequently_used_folders)

				self.new_file = self.local_media_folder + self.episode_file_name + "."

		self.moved_succesfully = False

		if self.old_file.split(".")[1] in self.accepted_file_extensions:
			self.Move_Media_File(self.old_file, self.new_file)

		if self.moved_succesfully == True:
			self.Media_Unit = self.new_file

			print()
			print("-----")
			print()

			return self.Media_Unit

		if self.moved_succesfully == False:
			quit()

	def Select_Folder_And_Media_File(self, folders):
		self.show_text = self.language_texts["folders, title()"]
		self.select_text = self.language_texts["select_one_folder_to_search_for_the_file"]

		self.media_file_location = self.Input.Select(folders, show_text = self.show_text, select_text = self.select_text)["option"]

		self.files_on_folder = self.Folder.Contents(self.media_file_location, add_sub_folders = False)["file"]["list"]

		self.select_text = self.language_texts["select_the_media_file"]

		return self.Input.Select(self.files_on_folder, select_text = self.select_text)["option"]

	def Move_Media_File(self, old_file, new_file):
		self.old_file = old_file
		self.new_file = new_file

		for extension in self.accepted_file_extensions:
			if extension in old_file:
				self.extension = extension

		self.new_file = self.new_file + self.extension

		self.moved_succesfully = self.File.Move(self.old_file, self.new_file)