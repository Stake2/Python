# Watch_Media.py

from Watch_History.Watch_History import Watch_History as Watch_History

from Watch_History.Register_Watched_Media import Register_Watched_Media as Register_Watched_Media
from Watch_History.Comment_Writer import Comment_Writer as Comment_Writer

import re
from urllib.parse import urlparse, parse_qs

# A class to Watch media that has the "Watching" or "Re-Watching" Watching Status
class Watch_Media(Watch_History):
	def __init__(self, media_dictionary = {}, run_as_module = False, open_media = True):
		super().__init__()

		self.media_dictionary = media_dictionary
		self.run_as_module = run_as_module
		self.open_media = open_media

		self.Define_Media_Dictionary()

		if self.media_dictionary["media"]["states"]["open_media"] == False:
			self.Define_Media_Episode_Variables()

		if self.media_dictionary["media"]["states"]["open_media"] == True:
			self.Define_Media_Episode_Variables()
			self.Define_Media_Episode_Unit()
			self.Show_Opening_Media_Info()
			self.Open_Media_Unit()
			self.Make_Discord_Status()
			self.Comment_On_Media()
			self.Register_Media()

	def Define_Media_Dictionary(self):
		# Select media type and media if media dictionary is empty
		if self.media_dictionary == {}:
			options = {
				"media_type": {
					"status": [
						self.texts["watching, title()"]["en"],
						self.texts["re_watching, title()"]["en"],
					],
				}
			}

			self.media_dictionary = self.Define_Options(self.media_dictionary, options)

			self.media_dictionary = self.Select_Media_Type_And_Media(options)

		# Else, only define the options of the filled media dictionary
		if self.media_dictionary != {}:
			self.media_dictionary = self.Define_Options({}, self.media_dictionary)

		# Re-Read of media details file
		self.media_dictionary["media"]["details"] = self.File.Dictionary(self.media_dictionary["media"]["folders"]["details"])

		# Define media states dictionary
		self.media_dictionary["media"]["states"] = {
			"remote": False,
			"local": False,
			"hybrid": False,
			"series_media": True,
			"video": False,
			"re_watching": False,
			"media_list": False,
			"has_dubbing": False,
			"watch_dubbed": False,
			"open_media": self.open_media,
		}

		# Define origin type state
		for item in ["local", "remote", "hybrid"]:
			if self.media_dictionary["media"]["details"][self.language_texts["origin_type"]] == self.language_texts[item + ", title()"]:
				self.media_dictionary["media"]["states"][item] = True

		# Define non-series media state for movies
		if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["movies"]["en"]:
			self.media_dictionary["media"]["states"]["series_media"] = False

		# Define video state for videos
		if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["videos"]["en"]:
			self.media_dictionary["media"]["states"]["video"] = True

		# Define Re-Watching state for Re-Watching status
		if self.media_dictionary["media"]["details"][self.language_texts["status, title()"]] == self.language_texts["re_watching, title()"]:
			self.media_dictionary["media"]["states"]["re_watching"] = True

		# Media list definition for series media
		if self.media_dictionary["media"]["states"]["series_media"] == True:
			self.media_dictionary["media"]["items"] = {
				"folders": {
					"root": self.media_dictionary["media"]["folders"]["root"] + self.media_dictionary["media_type"]["subfolders"]["plural"] + "/",
				}
			}

			for item in ["list", "current"]:
				key = item

				if item == "list":
					key = "plural"

				self.media_dictionary["media"]["items"]["folders"][item] = self.media_dictionary["media"]["items"]["folders"]["root"] + self.media_dictionary["media_type"]["subfolders"][key] + ".txt"
				self.File.Create(self.media_dictionary["media"]["items"]["folders"][item])

				self.media_dictionary["media"]["items"][item] = self.File.Contents(self.media_dictionary["media"]["items"]["folders"][item])["lines"]

				if item == "current":
					self.media_dictionary["media"]["items"][item] = self.media_dictionary["media"]["items"][item][0]

			# Define media item folders
			for item in self.media_dictionary["media"]["items"]["list"]:
				if item[0] + item[1] == ": ":
					item = item[2:]

				self.media_dictionary["media"]["items"]["folders"][item] = self.media_dictionary["media"]["items"]["folders"]["root"] + self.Sanitize(item, restricted_characters = True) + "/"
				self.Folder.Create(self.media_dictionary["media"]["items"]["folders"][item])

			if len(self.media_dictionary["media"]["items"]["list"]) > 1:
				# Has media list
				self.media_dictionary["media"]["states"]["media_list"] = True

			# Define current media item
			title = self.media_dictionary["media"]["items"]["current"]

			# Select video series from channel for video series media
			if self.media_dictionary["media"]["states"]["video"] == True and self.media_dictionary["media"]["states"]["media_list"] == True:
				show_text = self.Text.Capitalize(self.language_texts["youtube_video_series"])
				select_text = self.language_texts["select_a_youtube_video_series"]

				title = self.Input.Select(self.media_dictionary["media"]["items"]["list"], show_text = show_text, select_text = select_text)["option"]

			# Define media item dictionary with titles and folder
			self.media_dictionary["media"]["item"] = {
				"title": title,
				"title_sanitized": title,
				"titles": {},
				"folders": {
					"root": self.media_dictionary["media"]["items"]["folders"]["root"] + self.Sanitize(title, restricted_characters = True) + "/",
					"media": self.media_dictionary["media"]["folders"]["media"] + self.Sanitize(title, restricted_characters = True) + "/",
				}
			}

			# Define media item variables
			self.media_dictionary = self.Select_Media(self.media_dictionary, item = True)

			# Define media item folders
			for item in ["Comments", "Titles"]:
				key = item.lower().replace(" ", "_")
				item = self.language_texts[key + ", title()"]

				self.media_dictionary["media"]["item"]["folders"][key] = {
					"root": self.media_dictionary["media"]["item"]["folders"]["root"] + item + "/",
				}

				self.Folder.Create(self.media_dictionary["media"]["item"]["folders"][key]["root"])

			# Define episodes dictionary
			self.media_dictionary["media"]["item"]["episodes"] = {
				"titles": {
					"files": {},
				}
			}

			# Define episode titles files and lists
			for language in self.small_languages:
				full_language = self.full_languages[language]

				# Define episode titles file
				self.media_dictionary["media"]["item"]["episodes"]["titles"]["files"][language] = self.media_dictionary["media"]["item"]["folders"]["titles"]["root"] + full_language + ".txt"
				self.File.Create(self.media_dictionary["media"]["item"]["episodes"]["titles"]["files"][language])

				# Get language episode titles from file
				self.media_dictionary["media"]["item"]["episodes"]["titles"][language] = self.File.Contents(self.media_dictionary["media"]["item"]["episodes"]["titles"]["files"][language])["lines"]

				# Define episode number text as "EP"
				episode_number_text = "EP"

				# Or custom episode number text
				if self.language_texts["episode_number_name"] in self.media_dictionary["media"]["item"]["details"]:
					episode_number_text = self.media_dictionary["media"]["item"]["details"][self.language_texts["episode_number_name"]]

				# Iterate through episode titles
				i = 1
				for episode_title in self.media_dictionary["media"]["item"]["episodes"]["titles"][language]:
					number = str(self.Text.Add_Leading_Zeros(i))

					# Add episode number text to local episode title
					episode_title = episode_number_text + number + " " + episode_title

					# Add episode number text to episode titles if the number text is not present
					if number not in self.media_dictionary["media"]["item"]["episodes"]["titles"][language][i - 1]:
						self.media_dictionary["media"]["item"]["episodes"]["titles"][language][i - 1] = episode_title

					i += 1

			# Define dubbing
			if self.language_texts["dubbing, title()"] in self.media_dictionary["media"]["details"]:
				self.media_dictionary["media"]["states"]["has_dubbing"] = True

				if self.language_texts["watch_dubbed"] in self.media_dictionary["media"]["details"]:
					self.media_dictionary["media"]["states"]["watch_dubbed"] = self.Input.Define_Yes_Or_No(self.media_dictionary["media"]["details"][self.language_texts["watch_dubbed"]])

				if self.language_texts["watch_dubbed"] not in self.media_dictionary["media"]["details"]:
					if self.media_dictionary["media"]["states"]["open_media"] == True:
						self.media_dictionary["media"]["states"]["watch_dubbed"] = self.Input.Yes_Or_No(self.language_texts["watch_the_dubbed_episode_in_your_language"])

			# Write dictionary into media item "Information.json" file
			self.File.Edit(self.media_dictionary["media"]["item"]["folders"]["information"], self.Language.Python_To_JSON(self.media_dictionary["media"]["item"]), "w")

		dictionary = self.media_dictionary["media"].copy()
		dictionary.pop("select")
		dictionary.pop("list")

		# Write dictionary into media "Information.json" file
		self.File.Edit(self.media_dictionary["media"]["folders"]["information"], self.Language.Python_To_JSON(dictionary), "w")

	def Define_Media_Episode_Variables(self):
		# Definition of episode to watch if the media is not series media
		self.media_dictionary["media"]["episode"] = {
			"title": self.media_dictionary["media"]["titles"]["original"],
			"titles": self.media_dictionary["media"]["titles"],
			"sanitized": self.Sanitize(self.media_dictionary["media"]["titles"]["original"], restricted_characters = True),
			"number": 1
		}

		# Definition of episode to watch if the media is series media
		if self.media_dictionary["media"]["states"]["series_media"] == True:
			language_titles = self.media_dictionary["media"]["item"]["episodes"]["titles"][self.user_language]

			# If "Episode" key is not present in media item details, define it as the first episode
			if self.language_texts["episode, title()"] not in self.media_dictionary["media"]["item"]["details"] or self.media_dictionary["media"]["item"]["details"][self.language_texts["episode, title()"]] == "None":
				if language_titles != []:
					first_episode_title = language_titles[0]

				self.media_dictionary["media"]["item"]["details"][self.language_texts["episode, title()"]] = first_episode_title

				# Update media item details file
				self.File.Edit(self.media_dictionary["media"]["item"]["folders"]["details"], self.Text.From_Dictionary(self.media_dictionary["media"]["item"]["details"]), "w")

				# Update media item "Information.json" file
				self.File.Edit(self.media_dictionary["media"]["item"]["folders"]["information"], self.Language.Python_To_JSON(self.media_dictionary["media"]["item"]), "w")

			# Define media episode dictionary
			self.media_dictionary["media"]["episode"] = {
				"title": self.media_dictionary["media"]["item"]["details"][self.language_texts["episode, title()"]],
				"titles": {},
				"sanitized": self.Sanitize(self.media_dictionary["media"]["item"]["details"][self.language_texts["episode, title()"]], restricted_characters = True),
				"number": 1
			}

			# Get episode number
			i = 1
			for episode_title in language_titles:
				if episode_title in self.media_dictionary["media"]["episode"]["title"]:
					self.media_dictionary["media"]["episode"]["number"] = i

				i += 1

			# Define episode titles per language
			for language in self.small_languages:
				episode_titles = self.media_dictionary["media"]["item"]["episodes"]["titles"][language]

				episode_title = ""

				if episode_titles != []:
					episode_title = episode_titles[self.media_dictionary["media"]["episode"]["number"] - 1]

				self.media_dictionary["media"]["episode"]["titles"][language] = episode_title

		# Origin type variables definition for hybrid medias, getting origin type by the episode title
		if self.media_dictionary["media"]["details"][self.language_texts["origin_type"]] == self.language_texts["hybrid, title()"]:
			self.media_dictionary["media"]["states"]["hybrid"] = True

			# Local episode
			if self.language_texts["local, title()"] in self.media_dictionary["media"]["episode"]["title"]:
				self.media_dictionary["media"]["episode"]["title"] = self.media_dictionary["media"]["episode"]["title"].split(", " + self.language_texts["local, title()"])[0]

				self.media_dictionary["media"]["episode"]["hybrid_origin_type"] = ", " + self.language_texts["local, title()"]

				self.media_dictionary["media"]["states"]["local"] = True

			# Remote episode
			if self.language_texts["remote, title()"] in self.media_dictionary["media"]["episode"]["title"]:
				self.media_dictionary["media"]["episode"]["title"] = self.media_dictionary["media"]["episode"]["title"].split(", " + self.language_texts["remote, title()"])[0]

				self.media_dictionary["media"]["episode"]["hybrid_origin_type"] = ", " + self.language_texts["remote, title()"]

				self.media_dictionary["media"]["states"]["remote"] = True

		self.Text.Copy(self.Language.Python_To_JSON(self.media_dictionary["media"]))

		# Remote or hybrid remote media origin, code, and link
		if self.language_texts["remote_origin, title()"] in self.media_dictionary["media"]["details"] or self.language_texts["remote_origin, title()"] in self.media_dictionary["media"]["item"]["details"]:
			values = {}

			for item in ["remote_origin, title()", "origin_location, title()"]:
				if self.language_texts[item] in self.media_dictionary["media"]["details"]:
					values[item] = self.media_dictionary["media"]["details"][self.language_texts[item]]

				if self.language_texts[item] in self.media_dictionary["media"]["item"]["details"]:
					values[item] = self.media_dictionary["media"]["item"]["details"][self.language_texts[item]]

				if self.language_texts[item] not in self.media_dictionary["media"]["details"] and self.language_texts[item] not in self.media_dictionary["media"]["item"]["details"]:
					values[item] = ""

			self.remote_data = {
				"name": values["remote_origin, title()"],
				"origin_code": values["origin_location, title()"],
			}

			if self.remote_data["origin_code"] == "":
				if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"]:
					self.remote_data["origin_code"] = self.Sanitize(self.media_dictionary["media"]["titles"]["original"].lower(), restricted_characters = True)
					self.remote_data["origin_code"] = self.remote_data["origin_code"].replace(" ", "-")
					self.remote_data["origin_code"] = self.remote_data["origin_code"].replace("!", "")
					self.remote_data["origin_code"] = self.remote_data["origin_code"].replace(",", "")
					self.remote_data["origin_code"] = self.remote_data["origin_code"].replace("△", "")

			self.remote_data["origin"] = self.remote_origins[self.remote_data["name"]]

		self.one_episode_number_regex = r"[0-9][0-9]"
		self.two_episode_numbers_regex = r"[0-9][0-9]\-[0-9][0-9]"
		self.episode_and_bracket_number = r"[0-9][0-9]\([0-9][0-9]\)"

		self.language_media_episode = self.media_dictionary["media"]["episode"]["title"]

		if self.media_dictionary["media"]["states"]["series_media"] == False:
			self.language_media_episode = self.media_dictionary["media"]["titles"]["language"]

		# Media episode number definition by episode titles file line
		if self.media_dictionary["media"]["states"]["series_media"] == True:
			media_episode = self.media_dictionary["media"]["episode"]["title"]

			if re.sub(self.texts["re_watched, type: regex, en - pt"], "", self.media_dictionary["media"]["episode"]["title"]) != None:
				media_episode = re.sub(self.texts["re_watched, type: regex, en - pt"], "", self.media_dictionary["media"]["episode"]["title"])

			self.media_dictionary["episode_number_text"] = str(self.Text.Add_Leading_Zeros(self.media_dictionary["media"]["episode"]["number"]))
			self.media_episode_number_text_backup = self.media_dictionary["episode_number_text"]

			one_episode_number = re.findall(self.one_episode_number_regex, self.media_dictionary["media"]["episode"]["title"])
			one_episode_number_and_bracket = re.findall(self.episode_and_bracket_number, self.media_dictionary["media"]["episode"]["title"])
			two_episode_numbers = re.findall(self.two_episode_numbers_regex, self.media_dictionary["media"]["episode"]["title"])

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

		if self.media_dictionary["media"]["states"]["video"] == True:
			self.youtube_video_ids_file = self.media_dictionary["media"]["item"]["folders"]["root"] + self.texts["youtube_ids"]["en"] + ".txt"
			self.youtube_video_ids = self.File.Contents(self.youtube_video_ids_file)["lines"]

			if self.youtube_video_ids != []:
				self.youtube_video_id = self.youtube_video_ids[self.media_dictionary["media"]["episode"]["number"] - 1]

		self.re_watched_string = ""

		# Adding "Re-Watched ?x - Re-Assistido ?x" text to media episode
		if self.media_dictionary["media"]["states"]["re_watching"] == True:
			if self.run_as_module == False:
				print()
				print(self.media_dictionary["media"]["titles"]["language"] + " " + self.media_dictionary["media"]["episode"]["title"])

				self.watched_times = self.Input.Type(self.language_texts["type_the_number_of_times_that_you_watched"], accept_enter = False)

			if self.run_as_module == True:
				self.watched_times = 1

			if int(self.watched_times) != 0:
				if int(self.watched_times) != 1:
					self.re_watched_times = str(int(self.watched_times) + 1)

				else:
					self.re_watched_times = str(self.watched_times)

				self.re_watched_string = self.texts["re_watched, type: format, en - pt"].format(self.re_watched_times, self.re_watched_times)
				self.media_dictionary["media"]["episode"]["title"] += " " + self.re_watched_string

				self.language_re_watched_string = self.language_texts["re_watched, type: format"].format(self.re_watched_times)
				self.language_media_episode += " " + self.language_re_watched_string

			if int(self.watched_times) == 0:
				self.media_dictionary["media"]["states"]["re_watching"] = False

		# Defining the local media folder to use in local or hybrid local media
		if self.media_dictionary["media"]["states"]["hybrid"] == True or self.media_dictionary["media"]["states"]["local"] == True:
			self.local_media_folder = self.root_folders["media"] + self.media_dictionary["media"]["titles"]["original_file_name"] + "/"

			if self.media_dictionary["media"]["states"]["media_list"] == False and self.media_dictionary["media"]["item"] != self.media_dictionary["media"]["titles"]["original"]:
				self.local_media_folder += self.media_dictionary["media"]["item"]["title_sanitized"] + "/"

			self.Folder.Create(self.local_media_folder)

		# Define the media item episode as the same as media episode
		self.media_item_episode = self.media_dictionary["media"]["episode"]["title"]
		self.media_item_episode_with_title = self.media_item_episode

		# Change the media item episode to add media item if media has media list
		if self.media_dictionary["media"]["states"]["media_list"] == False and self.media_dictionary["media"]["states"]["video"] == False and self.media_dictionary["media"]["states"]["series_media"] == True and self.media_dictionary["media"]["item"] != self.media_dictionary["media"]["titles"]["original"]:
			separators = {
				"title_separator": None,
				"episode_separator": None,
			}

			for item in ["title_separator", "episode_separator"]:
				if self.language_texts[item] in self.media_dictionary["media"]["details"]:
					separators[item] = self.media_dictionary["media"]["details"][self.language_texts[item]]

			season_text = re.findall(r"^S[0-9][0-9]", self.media_dictionary["media"]["item"])

			space = ""

			if season_text == [] or \
			   season_text != [] and "EP" not in self.media_dictionary["media"]["episode"]["title"] and re.findall(r"E[0-9][0-9]", self.media_dictionary["media"]["episode"]["title"]) == []:
				space = " "

			if separators["episode_separator"] != None:
				space = separators["episode_separator"]

			self.media_item_episode = self.media_dictionary["media"]["item"] + space + self.media_dictionary["media"]["episode"]["title"]

			self.media_item_episode_with_title = ""

			if self.media_dictionary["media"]["titles"]["original"] not in self.media_dictionary["media"]["item"]:
				self.media_item_episode_with_title += self.media_dictionary["media"]["titles"]["original"]

			if self.media_dictionary["media"]["titles"]["original"] in self.media_dictionary["media"]["item"]:
				self.media_item_episode_with_title += self.media_dictionary["media"]["item"]

			if ":" not in self.media_item_episode and separators["title_separator"] == None:
				self.media_item_episode_with_title += " "

			if separators["title_separator"] != None:
				self.media_item_episode_with_title += separators["title_separator"]

			if self.media_dictionary["media"]["titles"]["original"] not in self.media_dictionary["media"]["item"]:
				self.media_item_episode_with_title += self.media_dictionary["media"]["item"]

				if separators["episode_separator"] == None and season_text == [] or \
				   season_text != [] and "EP" not in self.media_dictionary["media"]["episode"]["title"] and re.findall(r"E[0-9][0-9]", self.media_dictionary["media"]["episode"]["title"]) == []:
					self.media_item_episode_with_title += " "

				if separators["episode_separator"] != None:
					self.media_item_episode_with_title += separators["episode_separator"]

				self.media_item_episode_with_title += self.media_dictionary["media"]["episode"]["title"]

			if self.media_dictionary["media"]["titles"]["original"] in self.media_dictionary["media"]["item"]:
				self.media_item_episode_with_title += self.media_dictionary["media"]["episode"]["title"]

		if self.media_dictionary["media"]["states"]["series_media"] == True:
			if self.media_dictionary["media"]["states"]["video"] == False and self.media_dictionary["media"]["item"] == self.media_dictionary["media"]["titles"]["original"]:
				self.media_item_episode = self.media_dictionary["media"]["titles"]["original"] + " " + self.media_dictionary["media"]["episode"]["title"]
				self.media_item_episode_with_title = self.media_dictionary["media"]["titles"]["original"] + " " + self.media_dictionary["media"]["episode"]["title"]

			# Adding channel name to video series media item episode
			if self.media_dictionary["media"]["states"]["media_list"] == False and self.media_dictionary["media"]["states"]["video"] == True:
				self.media_item_episode = self.media_dictionary["media"]["titles"]["original"] + ": " + self.media_dictionary["media"]["episode"]["title"]
				self.media_item_episode_with_title = self.media_dictionary["media"]["titles"]["original"] + ": " + self.media_dictionary["media"]["episode"]["title"]

		for language in self.small_languages:
			language_name = self.texts["[language]_name"][language]

			self.language_media_item[language]["episode"] = self.media_item_episode
			self.language_media_item[language]["episode_with_title"] = self.media_item_episode_with_title

			if self.media_dictionary["media"]["titles"]["original"] in self.language_media_item[language]["episode_with_title"] and language in self.media_dictionary["media"]["titles"]:
				self.language_media_item[language]["episode_with_title"] = self.language_media_item[language]["episode_with_title"].replace(self.media_dictionary["media"]["titles"]["original"], self.media_dictionary["media"]["titles"][language])

			if self.media_dictionary["media"]["item"] in self.language_media_item[language]["episode"]:
				self.language_media_item[language]["episode"] = self.language_media_item[language]["episode"].replace(self.media_dictionary["media"]["item"], self.language_media_item[language]["title"])

			if self.media_dictionary["media"]["item"] in self.language_media_item[language]["episode_with_title"]:
				self.language_media_item[language]["episode_with_title"] = self.language_media_item[language]["episode_with_title"].replace(self.media_dictionary["media"]["item"], self.language_media_item[language]["title"])

		self.language_media_item["language"]["episode"] = self.language_media_item[self.user_language]["episode"]
		self.language_media_item["language"]["episode_with_title"] = self.language_media_item[self.user_language]["episode_with_title"]

		# Creating dubbed media text and adding dubbed text to media item episode if media is anime and is defined to watch it dubbed
		if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"] and self.media_dictionary["media"]["states"]["watch_dubbed"] == True:
			self.dubbed_text_to_title = False

			if self.language_texts["dubbed_to_title"] in self.media_dictionary["media"]["details"] and self.media_dictionary["media"]["details"][self.language_texts["dubbed_to_title"]] == "Yes":
				self.dubbed_text_to_title = True

			if self.language_texts["dubbed_to_title"] not in self.media_dictionary["media"]["details"]:
				self.dubbed_text_to_title = True

			if self.dubbed_text_to_title == True:
				self.dubbed_media_text = ""
				self.dubbed_media_text += " " + self.language_texts["dubbed"]
				self.media_item_episode_with_title = self.media_item_episode_with_title.replace(self.media_dictionary["media"]["titles"]["original"], self.media_dictionary["media"]["titles"]["original"] + " " + self.language_texts["dubbed"])

	def Update_Media_Dictionary(self):
		self.media_dictionary.update({
			"language_media_episode": self.language_media_episode,
			"youtube_video_id": self.youtube_video_id,
			"started_watching_time": self.Date.Now()["date_time_format"][self.user_language],
			"per_media_type_files_folder": self.per_media_type_files_folder,
			"per_media_type_episodes_file": self.per_media_type_episodes_file,
			"per_media_type_times_file": self.per_media_type_times_file,

			"re_watched_string": self.re_watched_string,
		})

		self.media_dictionary["the_item_text"] = self.media_dictionary["the_text"]
		self.media_dictionary["the_unit_text"] = self.gender_the_texts[self.media_dictionary["media_type"]["plural"]["en"]]["masculine"]["the"]

		self.media_dictionary["media_container_name"] = self.media_dictionary["media_type"]["singular"]["language"].lower()
		self.media_dictionary["media_item_name"] = self.media_dictionary["media_type"]["singular"]["language"].lower()
		self.media_dictionary["media_unit_name"] = self.media_dictionary["media_type"]["singular"]["language"].lower()

		if self.media_dictionary["media"]["states"]["series_media"] == True:
			self.media_dictionary["the_item_text"] = self.gender_the_texts[self.media_dictionary["media_type"]["plural"]["en"]]["feminine"]["the"]
			self.media_dictionary["media_unit_name"] = self.language_texts["episode"]

			if self.media_dictionary["media"]["states"]["media_list"] == False:
				self.media_dictionary["media_item_name"] = self.language_texts["season"]

			if self.media_dictionary["media"]["states"]["video"] == True:
				self.media_dictionary["media_container_name"] = self.language_texts["youtube_channel"]
				self.media_dictionary["media_item_name"] = self.language_texts["youtube_video_serie"]
				self.media_dictionary["media_unit_name"] = self.language_texts["video"]

		self.media_dictionary["header_text"] = self.language_texts["opening_{}_to_watch"].format(self.media_dictionary["this_text"] + " " + self.media_dictionary["media_container_name"]) + ":"

		if self.media_dictionary["media"]["states"]["series_media"] == True:
			self.media_dictionary["comments_folder"] = self.comments_folder

		if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"] and self.media_dictionary["media"]["states"]["watch_dubbed"] == True:
			self.media_dictionary["dubbed_media_text"] = self.dubbed_media_text

	def Define_Media_Episode_Unit(self):
		self.accepted_file_extensions = [
			"mp4",
			"mkv",
			"webm",
		]

		# Remote media episode link definition
		if self.language_texts["remote_origin, title()"] in self.media_dictionary["media"]["item"]["details"]:
			self.media_dictionary["media_link"] = self.remote_data["origin"]

			# Media episode link definition for Animes Vision website
			if self.remote_data["name"] == "Animes Vision":
				# Add Portuguese media type and origin code (media title) to media episode link
				self.media_dictionary["media_link"] += self.media_dictionary["media_type"]["plural"]["pt"].lower() + "/" + self.remote_data["origin_code"]

				# Add dubbed text
				if self.media_dictionary["media"]["states"]["has_dubbing"] == True and self.media_dictionary["media"]["states"]["watch_dubbed"] == True:
					self.media_dictionary["media_link"] += "-" + self.texts["dubbed"]["pt"].lower()

				self.media_dictionary["media_link"] += "/"

				# Add episode number
				self.media_dictionary["media_link"] += "episodio-" + str(self.Text.Add_Leading_Zeros(self.media_dictionary["media"]["episode"]["number"])) + "/"

				# Add dubbed text to media link if the media has a dub in the user language and user wants to watch it dubbed
				if self.media_dictionary["media"]["states"]["has_dubbing"] == True and self.media_dictionary["media"]["states"]["watch_dubbed"] == True:
					self.media_dictionary["media_link"] += self.texts["dubbed"]["pt"]

				# Add subbed text to media link if there is no dub for the media or the user wants to watch it subbed
				if self.media_dictionary["media"]["states"]["has_dubbing"] == False or self.media_dictionary["media"]["states"]["watch_dubbed"] == False:
					self.media_dictionary["media_link"] += self.texts["subbed"]["pt"]

			# Media episode link definition for YouTube website
			if self.remote_data["name"] == "YouTube":
				# Add watch and video id to media episode link if it is in the remote origin code
				if "v=" not in self.remote_data["origin_code"]:
					self.media_dictionary["media_link"] += "watch?v=" + self.media_dictionary["youtube_video_id"] + "&list=" + self.remote_data["origin_code"] + "&index=" + str(self.media_dictionary["media"]["episode"]["number"])

				if "v=" in self.remote_data["origin_code"]:
					self.media_dictionary["media_link"] += "watch?" + self.remote_data["origin_code"]

			self.media_dictionary["media_unit"] = self.media_dictionary["media_link"]

			if self.is_remote_episode == True:
				self.Executor = self.Text.Open_Link

		# Local media episode file definition
		if self.is_local_episode == True:
			if self.media_dictionary["media"]["states"]["series_media"] == True and self.media_dictionary["media"]["states"]["video"] == False:
				# Add "Português" text to local media folder if media has dub and watch dubbed is true
				if self.media_dictionary["media"]["states"]["has_dubbing"] == True and self.media_dictionary["media"]["states"]["watch_dubbed"] == True:
					self.local_media_folder += self.full_user_language + "/"

			self.Folder.Create(self.local_media_folder)

			# Remove re-watched text from media episode
			self.media_episode_no_re_watched = re.sub(" " + self.texts["re_watched, type: regex, en - pt"], "", self.media_dictionary["media"]["episode"]["sanitized"])

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
					self.media_dictionary["media_file"] = self.Find_Media_file(self.media_dictionary["media"]["episode"]["title"])

				if self.bring_file == False:
					print()
					quit(self.language_texts["alright"] + ".")

			self.media_dictionary["media_unit"] = self.media_dictionary["media_file"]

			self.Executor = self.File.Open

	def Show_Opening_Media_Info(self):
		if self.media_dictionary["media"]["states"]["video"] == False and self.Today_Is_Christmas() == True:
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

		self.discord_status = self.discord_status_text_template + " " + self.media_dictionary["media_type"]["singular"]["language"] + ": " + self.language_media_item["language"]["episode_with_title"]

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
		self.media_dictionary["finished_watching"] = self.Date.Now()["date_time_format"][self.user_language]

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