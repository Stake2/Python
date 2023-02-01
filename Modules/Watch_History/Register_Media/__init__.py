# Register_Media.py

from Watch_History.Watch_History import Watch_History as Watch_History

from Social_Networks.Open_Social_Network import Open_Social_Network as Open_Social_Network

from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

import re

class Register_Media(Watch_History):
	def __init__(self, run_as_module = False, media_dictionary = None):
		super().__init__()

		self.run_as_module = run_as_module
		self.media_dictionary = media_dictionary

		if self.run_as_module == False:
			self.Ask_For_Media_Info()

		# Define "register" dictionary (key) inside media dictionary
		self.media_dictionary["register"] = {
			"Diary Slim": {
				"text": ""
			}
		}

		self.Define_Diary_Slim_Text()

		self.Register_In_JSON()
		self.Create_File()

		self.Add_File_To_Year_Folder()

		self.Check_Media_Status()

		if self.media_dictionary["media"]["states"]["completed"] == True or self.media_dictionary["media"]["states"]["completed_item"] == True:
			self.Set_Media_As_Completed()

		self.Post_On_Social_Networks()

		self.Write_On_Diary_Slim()

		if self.global_switches["verbose"] == True:
			print()
			print(self.large_bar)
			print()
			print("Register_Media:")

		self.Show_Information()

	def Ask_For_Media_Info(self):
		# To-Do: Make this method

		self.media_dictionary = {}

	def Define_Diary_Slim_Text(self):
		template = self.language_texts["i_just_finished_watching_{}"]

		if self.media_dictionary["media"]["states"]["series_media"] == True:
			template += ' "{}"'

			text = self.media_dictionary["media_type"]["genders"]["of_the"]

			if self.media_dictionary["media"]["states"]["video"] == True:
				text = self.media_types["genders"]["masculine"]["of_the"]

			# Add unit and "of the" text
			self.watched_item_text = self.language_texts["this_{}_{}"].format(self.media_dictionary["media"]["texts"]["unit"][self.user_language], text)

			# Replaced "watching" with "re-watching" text
			if self.media_dictionary["media"]["states"]["re_watching"] == True:
				template = template.replace(self.language_texts["watching, infinitive"], self.language_texts["re_watching, infinitive"])

				template = template.replace(self.language_texts["re_watching, infinitive"], self.language_texts["re_watching, infinitive"] + " " + self.media_dictionary["media"]["episode"]["re_watched"]["time_text"][self.user_language])

			if self.language_texts["single_unit"] not in self.media_dictionary["media"]["item"]["details"]:
				# Replace "this" text with "the first" if the episode is the first one
				if self.media_dictionary["media"]["episode"]["title"] == self.media_dictionary["media"]["item"]["episodes"]["titles"][self.user_language][0]:
					self.watched_item_text = self.watched_item_text.replace(self.language_texts["this, masculine"], self.language_texts["the_first, masculine"])

				# Replace "this" text with "the last" if the episode is the last one
				if self.media_dictionary["media"]["episode"]["title"] == self.media_dictionary["media"]["item"]["episodes"]["titles"][self.user_language][-1] or len(self.media_dictionary["media"]["item"]["episodes"]["titles"][self.user_language]) == 1:
					self.watched_item_text = self.watched_item_text.replace(self.language_texts["this, masculine"], self.language_texts["the_last, masculine"])

			if "Movie" in self.media_dictionary["media"]["episode"]["titles"][self.user_language]:
				self.watched_item_text = self.watched_item_text.replace(self.language_texts["episode"], self.language_texts["movie"])

			self.of_the_text = self.language_texts["of_the_{}"]

			if self.media_dictionary["media"]["states"]["media_list"] == True and self.media_dictionary["media"]["item"]["title"] != self.media_dictionary["media"]["title"] and self.language_texts["single_unit"] not in self.media_dictionary["media"]["item"]["details"]:
				if self.media_dictionary["media"]["states"]["video"] == False:
					text = ""

					# Replace "of the" text with "of the first" if the media item is the first one
					if self.media_dictionary["media"]["item"]["title"] == self.media_dictionary["media"]["items"]["list"][0]:
						text = " " + self.language_texts["first, feminine"]

					# Replace "of the" text with "of the last" if the media item is the last one
					if self.media_dictionary["media"]["item"]["title"] == self.media_dictionary["media"]["items"]["list"][-1]:
						text = " " + self.language_texts["last, feminine"]

					# Add item text ("season" or "series") to "of the" text
					self.of_the_text = self.of_the_text.format(text + self.media_dictionary["media"]["texts"]["item"][self.user_language])

				if self.media_dictionary["media"]["states"]["video"] == True:
					self.of_the_text = self.of_the_text.format(self.language_texts["video_serie"])

				# Add "of the" text next to unit ("episode" or "video") text
				self.watched_item_text = self.watched_item_text.replace(self.media_dictionary["media"]["texts"]["unit"][self.user_language], self.media_dictionary["media"]["texts"]["unit"][self.user_language] + " {}".format(self.of_the_text))

				# Add media item title to "of the" text
				self.watched_item_text = self.watched_item_text.replace(self.of_the_text, self.of_the_text + ' "' + self.media_dictionary["media"]["item"]["title"] + '"')

				# Replace media title with space in media item if it exists
				if self.media_dictionary["media"]["title"] + " " in self.media_dictionary["media"]["item"]:
					self.watched_item_text = self.watched_item_text.replace(self.media_dictionary["media"]["title"] + " ", "")

			# Add container (media type or "YouTube channel" text for video media type) to watched item text
			self.watched_item_text += " " + self.media_dictionary["media"]["texts"]["container_text"]["container"]

			# Define Diary Slim text as the template formatted with the "watched item text" and the media title per language
			self.media_dictionary["register"]["Diary Slim"]["text"] = template.format(self.watched_item_text, self.media_dictionary["media"]["titles"]["language"])

		# If the media is a movie, only add the "this" text and the media type "movie" text in user language
		if self.media_dictionary["media"]["states"]["series_media"] == False:
			self.media_dictionary["register"]["Diary Slim"]["text"] = template.format(self.media_dictionary["media_type"]["genders"]["this"] + " " + self.media_dictionary["media_type"]["singular"][self.user_language].lower())

		# Add language media episode (or movie title)
		if self.language_texts["single_unit"] not in self.media_dictionary["media"]["item"]["details"]:
			self.media_dictionary["register"]["Diary Slim"]["text"] += ":\n" + self.media_dictionary["media"]["episode"]["titles"][self.user_language]

		if self.language_texts["single_unit"] in self.media_dictionary["media"]["item"]["details"]:
			self.media_dictionary["register"]["Diary Slim"]["text"] += ":\n" + self.media_dictionary["media"]["episode"]["with_title"][self.user_language]

		if self.media_dictionary["media"]["states"]["re_watching"] == True:
			self.media_dictionary["register"]["Diary Slim"]["text"] += self.media_dictionary["media"]["episode"]["re_watched"]["text"]

		# Add YouTube video link for video media
		if self.media_dictionary["media"]["states"]["video"] == True:
			self.media_dictionary["register"]["Diary Slim"]["text"] += "\n\n" + self.remote_origins["YouTube"] + "watch?v=" + self.media_dictionary["media"]["episode"]["youtube_id"]

		self.media_dictionary["register"]["Diary Slim"]["text"] = self.media_dictionary["media"]["finished_watching"]["date_time_format"][self.user_language] + ":\n" + self.media_dictionary["register"]["Diary Slim"]["text"]

	def Register_In_JSON(self):
		self.media_type = self.media_dictionary["media_type"]["plural"]["en"]

		self.watched = self.JSON.To_Python(self.media_dictionary["media"]["item"]["folders"]["watched"]["watched"])

		# Add to episode and media type episode numbers
		self.episodes["Number"] += 1
		self.media_type_episodes[self.media_type]["Number"] += 1

		# Add media title to media titles list
		media_title = self.Get_Media_Title(self.media_dictionary)

		self.episodes["Lists"]["Media"].append(media_title)
		self.media_type_episodes[self.media_type]["Lists"]["Media"].append(media_title)

		self.media_dictionary["register"].update({
			"Episode titles": {}
		})

		for language in self.small_languages:
			# Get media episode
			self.media_dictionary["register"]["Episode titles"][language] = ""

			if self.media_dictionary["media"]["states"]["series_media"] == True:
				self.media_dictionary["register"]["Episode titles"][language] = self.Get_Media_Title(self.media_dictionary, language, episode = True)

			# Add media episode to episode titles list
			self.episodes["Lists"]["Episode titles"][language].append(self.media_dictionary["register"]["Episode titles"][language])

			if self.media_dictionary["media"]["states"]["series_media"] == True:
				# Add media episode to media type episode titles list
				self.media_type_episodes[self.media_type]["Lists"]["Episode titles"][language].append(self.media_dictionary["register"]["Episode titles"][language])

				# Add media episode to media "Watched" episode titles list
				self.watched["Lists"]["Episode titles"][language].append(self.media_dictionary["register"]["Episode titles"][language])

		# Add to media types list
		self.episodes["Lists"]["Media Types"].append(self.media_type)

		# Define media episode times
		self.media_dictionary["register"]["Times"] = {
			"ISO8601": self.media_dictionary["media"]["finished_watching"]["%Y-%m-%d %H:%M:%S"],
			"Language DateTime": {}
		}

		for language in self.small_languages:
			self.media_dictionary["register"]["Times"]["Language DateTime"][language] = self.media_dictionary["media"]["finished_watching"]["date_time_format"][language]

		# Add to episode times, media type episode times, and media "Watched" episode times
		self.episodes["Lists"]["Times"]["ISO8601"].append(self.media_dictionary["register"]["Times"]["ISO8601"])
		self.media_type_episodes[self.media_type]["Lists"]["Times"]["ISO8601"].append(self.media_dictionary["register"]["Times"]["ISO8601"])
		self.watched["Lists"]["Times"]["ISO8601"].append(self.media_dictionary["register"]["Times"]["ISO8601"])

		for language in self.small_languages:
			self.episodes["Lists"]["Times"]["Language DateTime"][language].append(self.media_dictionary["register"]["Times"]["Language DateTime"][language])
			self.media_type_episodes[self.media_type]["Lists"]["Times"]["Language DateTime"][language].append(self.media_dictionary["register"]["Times"]["Language DateTime"][language])
			self.watched["Lists"]["Times"]["Language DateTime"][language].append(self.media_dictionary["register"]["Times"]["Language DateTime"][language])

		youtube_id = ""

		if self.media_dictionary["media"]["states"]["video"] == True:
			youtube_id = self.media_dictionary["media"]["episode"]["youtube_id"]

		# Add empty string or YouTube ID to "YouTube IDs" key
		self.episodes["Lists"]["YouTube IDs"].append(youtube_id)

		if self.media_dictionary["media"]["states"]["video"] == True:
			self.media_type_episodes[self.media_type]["Lists"]["YouTube IDs"].append(youtube_id)

		# Define [Number. Media Type (Time)] and sanitized version for files
		self.media_dictionary["register"]["Number. Media Type (Time)"] = str(self.episodes["Number"]) + ". " + self.media_type + " (" + self.media_dictionary["register"]["Times"]["Language DateTime"][self.user_language] + ")"
		self.media_dictionary["register"]["Number. Media Type (Time) Sanitized"] = self.media_dictionary["register"]["Number. Media Type (Time)"].replace(":", ";").replace("/", "-")

		# Define [Number. Media Type (Time)] sanitized for files per language
		self.media_dictionary["register"]["Number. Media Type (Time) Sanitized Languages"] = {}

		for language in self.small_languages:
			self.media_dictionary["register"]["Number. Media Type (Time) Sanitized Languages"][language] = str(self.episodes["Number"]) + ". " + self.media_type + " (" + self.media_dictionary["register"]["Times"]["Language DateTime"][language].replace(":", ";").replace("/", "-") + ")"

		# Add to [Number. Media Type (Time)] list
		self.episodes["Number. Media Type (Time)"].append(self.media_dictionary["register"]["Number. Media Type (Time)"])
		self.media_type_episodes[self.media_type]["Number. Media Type (Time)"].append(self.media_dictionary["register"]["Number. Media Type (Time)"])

		# Add episode dictionary to episodes dictionary
		media_titles = self.media_dictionary["media"]["titles"].copy()
		item_titles = self.media_dictionary["media"]["item"]["titles"].copy()

		for key in ["jp", "sanitized"]:
			if key in media_titles:
				media_titles.pop(key)

			if key in item_titles:
				item_titles.pop(key)

		if media_titles["language"] == media_titles["original"]:
			media_titles.pop("language")

		if item_titles["language"] == item_titles["original"]:
			item_titles.pop("language")

		for dictionary in [media_titles, item_titles]:
			if "romanized" in dictionary and dictionary["language"] == dictionary["romanized"]:
				dictionary.pop("romanized")

		key = self.media_dictionary["register"]["Number. Media Type (Time)"]

		self.episodes["Dictionary"][key] = {
			"Number": self.episodes["Number"],
			"Media type number": self.media_type_episodes[self.media_type]["Number"],
			"Media": media_titles,
			"Item": item_titles,
			"Episode titles": self.media_dictionary["register"]["Episode titles"],
			"Type": self.media_type,
			"Times": self.media_dictionary["register"]["Times"],
			"File name": self.media_dictionary["register"]["Number. Media Type (Time)"]
		}

		if self.media_dictionary["media"]["states"]["media_list"] == False or self.media_dictionary["media"]["item"]["title"] == self.media_dictionary["media"]["title"] or self.media_dictionary["media"]["states"]["series_media"] == False:
			self.episodes["Dictionary"][key].pop("Item")

		if self.media_dictionary["media"]["states"]["series_media"] == False or self.language_texts["single_unit"] in self.media_dictionary["media"]["item"]["details"]:
			self.episodes["Dictionary"][key].pop("Episode titles")

		if self.media_dictionary["media"]["states"]["video"] == True:
			self.episodes["Dictionary"][key]["YouTube ID"] = youtube_id

		dict_ = self.Define_States_Dictionary(self.media_dictionary)

		key = self.media_dictionary["register"]["Number. Media Type (Time)"]

		if dict_ != {}:
			self.episodes["Dictionary"][key]["States"] = dict_

		# Add episode dictionary to media type episodes dictionary
		self.media_type_episodes[self.media_type]["Dictionary"][key] = self.episodes["Dictionary"][key].copy()

		# Get Comments dictionary from file
		self.comments = self.JSON.To_Python(self.folders["comments"]["comments"])

		# Get year comment number from "Comments.json" file
		self.episodes["Comments"] = self.comments["Year numbers"][str(self.date["year"])]

		# Update "Episodes.json" file
		self.JSON.Edit(self.folders["watch_history"]["current_year"]["episodes"], self.episodes)

		# Get year media type comment number from "Comments.json" file
		self.media_type_episodes[self.media_type]["Comments"] = self.comments["Media type year numbers"][str(self.date["year"])][self.media_type]

		# Update media type "Episodes.json" file
		self.JSON.Edit(self.media_dictionary["media_type"]["folders"]["per_media_type"]["episodes"], self.media_type_episodes[self.media_type])

		# Add to root and media type "File list.txt" file
		self.File.Edit(self.folders["watch_history"]["current_year"]["file_list"], self.media_dictionary["register"]["Number. Media Type (Time)"], "a")
		self.File.Edit(self.media_dictionary["media_type"]["folders"]["per_media_type"]["file_list"], self.media_dictionary["register"]["Number. Media Type (Time)"], "a")

		# ---------------------------- #

		watched_key = "Movie"

		if self.language_texts["single_unit"] in self.media_dictionary["media"]["item"]["details"]:
			watched_key = "Episode"

		# Add episode number to "Episode number" list for series media
		if self.media_dictionary["media"]["states"]["series_media"] == True:
			self.watched["Episode number"].append(self.media_dictionary["media"]["episode"]["number"])

			watched_key = self.media_dictionary["media"]["episode"]["number"]

		if self.media_dictionary["media"]["states"]["re_watching"] == True:
			watched_key += " (" + self.media_dictionary["media"]["episode"]["re_watched"]["text"] + ")"

		# Add episode dictionary to media "Watched" dictionary
		self.watched["Dictionary"][watched_key] = self.media_type_episodes[self.media_type]["Dictionary"][key]

		# Update media "Watched.json" file
		self.JSON.Edit(self.media_dictionary["media"]["item"]["folders"]["watched"]["watched"], self.watched)

	def Create_File(self):
		# Number: [Episode number]
		# Media type number: [Media type number]
		# 
		# Media: [Media titles]
		# (
		# Item: [Item titles]
		# (
		# [Episode/Video] titles: [Episode titles]
		# )
		# Type: [Media type]
		#
		# Times: [Episode times]
		# 
		# File name: [Number. Media Type (Time)]

		# Define episode file
		folder = self.media_dictionary["media_type"]["folders"]["per_media_type"]["files"]["root"]
		file = folder + self.media_dictionary["register"]["Number. Media Type (Time) Sanitized"] + ".txt"
		self.File.Create(file)

		self.media_dictionary["register"]["episode_text"] = {}

		self.media_dictionary["register"]["episode_text"]["general"] = self.Define_Episode_Text("general")

		for language in self.small_languages:
			self.media_dictionary["register"]["episode_text"][language] = self.Define_Episode_Text(language)

		# Write episode text into episode file
		self.File.Edit(file, self.media_dictionary["register"]["episode_text"]["general"], "w")

		# Write episode text into "Watched" episode file
		folder = self.media_dictionary["media"]["item"]["folders"]["watched"]["root"]

		if self.media_dictionary["media"]["states"]["series_media"] == True:
			folder = self.media_dictionary["media"]["item"]["folders"]["watched"]["files"]["root"]
			file_name = str(self.media_dictionary["media"]["episode"]["number"])

		if self.media_dictionary["media"]["states"]["series_media"] == False:
			file_name = "Movie"

		if self.language_texts["single_unit"] in self.media_dictionary["media"]["item"]["details"]:
			file_name = "Episode"

		file = folder + file_name

		if self.media_dictionary["media"]["states"]["re_watching"] == True:
			file += " (" + self.media_dictionary["media"]["episode"]["re_watched"]["text"] + ")"

		file += ".txt"

		self.File.Edit(file, self.media_dictionary["register"]["episode_text"][self.user_language], "w")

	# Define episode text per language
	def Define_Episode_Text(self, language_parameter = None):
		if language_parameter != "general":
			language = language_parameter

		if language_parameter == "general":
			language = "en"

		full_language = self.full_languages[language]

		# Define episode text lines
		lines = [
			self.texts["number, title()"][language] + ": " + str(self.episodes["Number"]),
			self.texts["media_type_number"][language] + ": " + str(self.media_type_episodes[self.media_type]["Number"]),
			"\n" + self.texts["media, title()"][language] + ":" + "\n" + "{}",
		]

		if self.media_dictionary["media"]["states"]["series_media"] == True:
			if self.media_dictionary["media"]["states"]["media_list"] == True and self.media_dictionary["media"]["item"]["title"] != self.media_dictionary["media"]["title"]:
				lines.append(self.texts["item, title()"][language] + ":" + "\n" + "{}")

			if self.language_texts["single_unit"] not in self.media_dictionary["media"]["item"]["details"]:
				text = self.texts["episode_titles"][language]

				if language_parameter != "general":
					text = self.texts["episode_title"][language]

				if self.media_dictionary["media"]["states"]["video"] == True:
					text = self.texts["video_titles"][language]

				lines.append(text + ":" + "\n" + "{}")

		lines.extend([
			self.texts["type, title()"][language] + ": " + self.media_dictionary["media_type"]["plural"]["en"] + "\n",
			self.Date.texts["times, title()"][language] + ":" + "\n" + "{}",
			self.File.texts["file_name"][language] + ": " + self.media_dictionary["register"]["Number. Media Type (Time)"]
		])

		if "States" in self.episodes["Dictionary"][self.media_dictionary["register"]["Number. Media Type (Time)"]]:
			dict_ = self.episodes["Dictionary"][self.media_dictionary["register"]["Number. Media Type (Time)"]]["States"]

			text = "\n" + self.texts["states, title()"][language] + ":" + "\n"

			for key in dict_:
				key = key.lower()

				if key != "re_watched":
					text_key = key

					if "_" not in key:
						text_key += ", title()"

					if key not in ["first_episode_in_year", "first_media_type_episode_in_year"]:
						language_text = self.texts[text_key][language]

					if key == "first_episode_in_year":
						language_text = self.texts["first_in_year"][language]

					if key == "first_media_type_episode_in_year":
						language_text = self.texts["first_{}_in_year"][language].format(self.media_dictionary["media"]["texts"]["container"][language].lower())

					text += language_text

				if key == "re_watched":
					text += self.media_dictionary["media"]["episode"]["re_watched"]["re_watched_text"][language] + " (" + str(self.media_dictionary["media"]["episode"]["re_watched"]["times"]) + "x)"

				if key != list(dict_.keys())[-1].lower():
					text += "\n"

			lines.append(text)

		# Define language episode text
		episode_text = self.Text.From_List(lines)

		# Define items to be added to episode text
		items = []

		titles = ""

		# Add media titles to items list
		key = "original"

		if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"] and "romanized" in self.media_dictionary["media"]["titles"]:
			key = "romanized"

		titles += self.media_dictionary["media"]["titles"][key]

		if self.media_dictionary["media"]["titles"]["language"] != self.media_dictionary["media"]["titles"][key]:
			titles += "\n" + self.media_dictionary["media"]["titles"]["language"]

		items.append(titles + "\n")

		if self.media_dictionary["media"]["states"]["series_media"] == True:
			# Add media item titles to media item titles list
			if self.media_dictionary["media"]["states"]["media_list"] == True and self.media_dictionary["media"]["item"]["title"] != self.media_dictionary["media"]["title"]:
				key = "original"

				if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"] and "romanized" in self.media_dictionary["media"]["item"]["titles"]:
					key = "romanized"

				item_titles = self.media_dictionary["media"]["item"]["titles"][key]

				if self.media_dictionary["media"]["item"]["titles"]["language"] != self.media_dictionary["media"]["item"]["titles"][key]:
					item_titles += "\n" + self.media_dictionary["media"]["item"]["titles"]["language"]

				items.append(item_titles + "\n")

			if self.language_texts["single_unit"] not in self.media_dictionary["media"]["item"]["details"]:
				# Add episode titles to episode titles list
				episode_titles = ""

				if language_parameter != "general":
					episode_title = self.media_dictionary["media"]["episode"]["titles"][language]

					if episode_title == "":
						episode_title = "[" + self.Language.texts["empty, title()"][language] + "]"

					episode_titles = episode_title + "\n"

				if language_parameter == "general":
					line_break = True

					for language in self.small_languages:
						episode_title = self.media_dictionary["media"]["episode"]["titles"][language]

						if episode_title == "":
							episode_title = "[" + self.Language.texts["empty, title()"][language] + "]"

						episode_titles += episode_title + "\n"

				items.append(episode_titles)

		times = ""

		for key in ["ISO8601", "Language DateTime"]:
			time = self.media_dictionary["register"]["Times"][key]

			if key == "ISO8601":
				times += time + "\n"

			if key == "Language DateTime":
				if language_parameter != "general":
					times += time[language] + "\n"

				if language_parameter == "general":
					for language in self.small_languages:
						times += time[language] + "\n"

		items.append(times)

		return episode_text.format(*items)

	def Add_File_To_Year_Folder(self):
		# Create folders
		for language in self.small_languages:
			full_language = self.full_languages[language]

			# Watched media folder
			watched_media = self.texts["watched_media"][language]
			media_type_folder = self.media_dictionary["media_type"]["singular"][language]
			folder = self.current_year["folders"][full_language][watched_media]["root"]

			# Media type folder
			self.current_year["folders"][full_language][watched_media][media_type_folder] = {
				"root": folder + media_type_folder + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][watched_media][media_type_folder]["root"])

			# Type folder
			firsts_of_the_year_text = self.texts["firsts_of_the_year"][language]
			type_folder = self.texts["media, title()"][language]
			folder = self.current_year["folders"][full_language][firsts_of_the_year_text]["root"]

			self.current_year["folders"][full_language][firsts_of_the_year_text][type_folder] = {
				"root": folder + type_folder + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][type_folder]["root"])

			# Media type folder
			folder = self.current_year["folders"][full_language][firsts_of_the_year_text][type_folder]["root"]
			
			self.current_year["folders"][full_language][firsts_of_the_year_text][type_folder][media_type_folder] = {
				"root": folder + media_type_folder + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][type_folder][media_type_folder]["root"])

		for language in self.small_languages:
			full_language = self.full_languages[language]

			# Watched media file
			watched_media = self.texts["watched_media"][language]
			media_type_folder = self.media_dictionary["media_type"]["singular"][language]

			folder = self.current_year["folders"][full_language][watched_media][media_type_folder]["root"]
			file_name = self.media_dictionary["register"]["Number. Media Type (Time) Sanitized Languages"][language]
			self.current_year["folders"][full_language][watched_media][media_type_folder][file_name] = folder + file_name + ".txt"

			self.File.Create(self.current_year["folders"][full_language][watched_media][media_type_folder][file_name])

			self.File.Edit(self.current_year["folders"][full_language][watched_media][media_type_folder][file_name], self.media_dictionary["register"]["episode_text"][language], "w")

			# First episode in year file
			if self.media_dictionary["media"]["states"]["first_media_type_episode_in_year"] == True:
				firsts_of_the_year_text = self.texts["firsts_of_the_year"][language]
				type_folder = self.texts["media, title()"][language]

				folder = self.current_year["folders"][full_language][firsts_of_the_year_text][type_folder][media_type_folder]["root"]

				self.current_year["folders"][full_language][firsts_of_the_year_text][type_folder][media_type_folder][file_name] = folder + file_name + ".txt"
				self.File.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][type_folder][media_type_folder][file_name])

				self.File.Edit(self.current_year["folders"][full_language][firsts_of_the_year_text][type_folder][media_type_folder][file_name], self.media_dictionary["register"]["episode_text"][language], "w")

	def Check_Media_Status(self):
		if self.media_dictionary["media"]["states"]["series_media"] == True:
			# If the media has a media list and the episode title is the last one
			if self.media_dictionary["media"]["states"]["media_list"] == True and self.media_dictionary["media"]["episode"]["title"] == self.media_dictionary["media"]["item"]["episodes"]["titles"][self.user_language][-1]:
				# And the episode is not a video
				if self.media_dictionary["media"]["states"]["video"] == False:
					# If the media item is the last media item, define the media as completed
					if self.media_dictionary["media"]["item"]["title"] == self.media_dictionary["media"]["items"]["list"][-1]:
						self.media_dictionary["media"]["states"]["completed"] = True

					# If the media item is not the last media item (media is not completed), get next media item
					if self.media_dictionary["media"]["item"]["title"] != self.media_dictionary["media"]["items"]["list"][-1]:
						title = self.media_dictionary["media"]["items"]["list"][self.media_dictionary["media"]["item"]["number"] + 1]

						# Define next media item
						self.media_dictionary["media"]["item"]["next"] = {
							"title": title,
							"sanitized": self.Sanitize_Title(title),
							"titles": {},
							"folders": {
								"root": self.media_dictionary["media"]["items"]["folders"]["root"] + self.Sanitize_Title(title) + "/",
								"media": self.media_dictionary["media"]["folders"]["media"] + self.Sanitize_Title(title) + "/",
								"media_type_comments": {
									"root": self.media_dictionary["media"]["folders"]["media_type_comments"]["root"] + self.Sanitize_Title(title) + "/"
								}
							},
							"number": self.media_dictionary["media"]["item"]["number"] + 1
						}

						# Define local media dictionary to update it
						dictionary = {
							"texts": {
								"select": "",
							},
							"media_type": self.media_dictionary["media_type"],
							"media": self.media_dictionary["media"]["item"]["next"]
						}

						# Update the titles and folders of the next media item dictionary
						self.media_dictionary["media"]["item"]["next"] = self.Select_Media(dictionary)["media"]

						# Update current media item file
						self.File.Edit(self.media_dictionary["media"]["items"]["folders"]["current"], self.media_dictionary["media"]["item"]["next"]["title"], "w")

				self.media_dictionary["media"]["states"]["completed_item"] = True

			# If the media has no media list and the episode title is the last one, define the media as completed
			if self.media_dictionary["media"]["states"]["media_list"] == False and self.media_dictionary["media"]["episode"]["title"] == self.media_dictionary["media"]["item"]["episodes"]["titles"][self.user_language][-1]:
				self.media_dictionary["media"]["states"]["completed"] = True

		# If the media is a movie, define it as completed
		if self.media_dictionary["media"]["states"]["series_media"] == False:
			self.media_dictionary["media"]["states"]["completed"] = True

		# If the media and media item are not completed, get next episode number
		if self.media_dictionary["media"]["states"]["completed"] == False and self.media_dictionary["media"]["states"]["completed_item"] == False:
			# Get next episode language title
			self.media_dictionary["media"]["episode"]["next"] = self.media_dictionary["media"]["item"]["episodes"]["titles"][self.user_language][self.media_dictionary["media"]["episode"]["number"]]

			# Add hybrid origin type to episode title
			if self.media_dictionary["media"]["states"]["hybrid"] == True:
				self.media_dictionary["media"]["episode"]["next"] += self.media_dictionary["media"]["episode"]["hybrid_origin_type"]

			# Define current episode to watch as the next episode
			self.media_dictionary["media"]["item"]["details"][self.language_texts["episode, title()"]] = self.media_dictionary["media"]["episode"]["next"]

			# Update media item details file
			self.File.Edit(self.media_dictionary["media"]["item"]["folders"]["details"], self.Text.From_Dictionary(self.media_dictionary["media"]["item"]["details"]), "w")

		# If the media is completed, define its status as completed
		if self.media_dictionary["media"]["states"]["completed"] == True:
			# Update status key in media details
			self.Change_Status(self.media_dictionary, self.language_texts["completed, title()"])

	def Set_Media_As_Completed(self):
		# Completed media and media item time and date part
		template = self.language_texts["when_i_finished_watching"] + " {}:" + "\n" + \
		self.media_dictionary["media"]["finished_watching"]["date_time_format"][self.user_language] + "\n" + \
		"\n" + \
		self.language_texts["duration, title()"] + ":" + "\n" + \
		"{}"

		# Gets the date that the user started and finished watching the media item and writes it into the media item dates file
		if self.media_dictionary["media"]["states"]["completed_item"] == True:
			# Gets the item dates from the item dates file
			self.media_dictionary["media"]["item"]["dates"] = self.File.Dictionary(self.media_dictionary["media"]["item"]["folders"]["dates"], next_line = True)

			if self.language_texts["single_unit"] in self.media_dictionary["media"]["item"]["details"]:
				self.media_dictionary["media"]["item"]["dates"][self.language_texts["when_i_started_to_watch"] + " " + self.media_dictionary["media"]["texts"]["the_item"][self.user_language]] = self.media_dictionary["media"]["finished_watching"]["date_time_format"][self.user_language]

			# Get started watching time
			self.media_dictionary["media"]["item"]["started_watching_item"] = self.media_dictionary["media"]["item"]["dates"][self.language_texts["when_i_started_to_watch"] + " " + self.media_dictionary["media"]["texts"]["the_item"][self.user_language]]

			# Define time spent watching using started watching time and finished watching time
			self.media_dictionary["media"]["item"]["time_spent_watching"] = self.Date.Difference(self.media_dictionary["media"]["item"]["started_watching_item"], self.media_dictionary["media"]["finished_watching"])["difference_strings"][self.user_language]

			# Format the time template
			self.media_dictionary["media"]["item"]["formatted_template"] = "\n\n" + template.format(self.media_dictionary["media"]["texts"]["the_item"][self.user_language], self.media_dictionary["media"]["item"]["time_spent_watching"])

			# Add the time template to the item dates text
			self.media_dictionary["media"]["item"]["finished_watching_text"] = self.File.Contents(self.media_dictionary["media"]["item"]["folders"]["dates"])["string"] + self.media_dictionary["media"]["item"]["formatted_template"]

			# Update item dates text file
			self.File.Edit(self.media_dictionary["media"]["item"]["folders"]["dates"], self.media_dictionary["media"]["item"]["finished_watching_text"], "w")

			# Add the time template to the Diary Slim text if the media is not completed
			if self.media_dictionary["media"]["states"]["completed"] == False and self.language_texts["single_unit"] not in self.media_dictionary["media"]["item"]["details"]:
				self.media_dictionary["register"]["Diary Slim"]["text"] += "\n\n" + self.media_dictionary["media"]["item"]["finished_watching_text"]

		# Gets the date that the user started and finished watching the media and writes it to the media dates text file
		if self.media_dictionary["media"]["states"]["completed"] == True:
			# Gets the media dates from the media dates file
			self.media_dictionary["media"]["dates"] = self.File.Dictionary(self.media_dictionary["media"]["folders"]["dates"], next_line = True)

			# Get started watching time
			self.media_dictionary["media"]["started_watching"] = self.Date.From_String(self.media_dictionary["media"]["dates"][self.language_texts["when_i_started_to_watch"] + " " + self.media_dictionary["media"]["texts"]["container_text"]["the"]])

			# Define time spent watching using started watching time and finished watching time
			self.media_dictionary["media"]["time_spent_watching"] = self.Date.Difference(self.media_dictionary["media"]["started_watching"], self.media_dictionary["media"]["finished_watching"])["difference_strings"][self.user_language]

			# Format the time template
			self.media_dictionary["media"]["item"]["formatted_template"] = "\n\n" + template.format(self.media_dictionary["media"]["texts"]["container_text"]["the"], self.media_dictionary["media"]["time_spent_watching"])

			# Add the time template to the media dates text
			self.media_dictionary["media"]["finished_watching_text"] = self.File.Contents(self.media_dictionary["media"]["folders"]["dates"])["string"] + self.media_dictionary["media"]["item"]["formatted_template"]

			# Update media dates text file
			self.File.Edit(self.media_dictionary["media"]["folders"]["dates"], self.media_dictionary["media"]["finished_watching_text"], "w")

			# Add the time template to the Diary Slim text
			self.media_dictionary["register"]["Diary Slim"]["text"] += "\n\n" + self.media_dictionary["media"]["finished_watching_text"]

			# ---------------------------- #

			# Update media type "Info.json" file

			# Read JSON file
			self.media_type = self.JSON.To_Python(self.media_dictionary["media_type"]["folders"]["media_info"]["info"])

			media_title = self.Get_Media_Title(self.media_dictionary)

			# Remove completed media from the "Watching" media list
			if media_title in self.media_type["Status"][self.texts["watching, title()"]["en"]]:
				self.media_type["Status"][self.texts["watching, title()"]["en"]].remove(media_title)

			# Add completed media to the "Completed" media list
			if media_title not in self.media_type["Status"][self.texts["completed, title()"]["en"]]:
				self.media_type["Status"][self.texts["completed, title()"]["en"]].append(media_title)

			# Sort status media lists
			for item in ["watching", "completed"]:
				text = self.texts[item + ", title()"]["en"]

				self.media_type["Status"][text] = sorted(self.media_type["Status"][text])

			# Update media type json file
			self.JSON.Edit(self.media_dictionary["media_type"]["folders"]["media_info"]["info"], self.media_type)

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

		if self.media_dictionary["media"]["states"]["series_media"] == False:
			text = text.replace(self.language_texts["a_screenshot_of_the_episode"], self.language_texts["movie"])

		if self.media_dictionary["media"]["title"] in ["The Walking Dead", "Yuru Camp"]:
			text = text.replace(self.language_texts["a_screenshot_of_the_episode"], self.language_texts["a_summary_video"])

		self.posted_on_social_networks_text_template = self.language_texts["i_posted_the_watched_text_and_{}_on_the_status_of_{}_and_tweet_on_{}"] + "."

		self.media_dictionary["register"]["Diary Slim"]["posted_on_social_networks"] = self.posted_on_social_networks_text_template.format(text, self.first_three_social_networks, self.twitter_social_network)

		text = self.language_texts["post_on_the_social_networks"] + " (" + self.social_networks_string + ")"

		self.media_dictionary["register"]["post_on_social_networks"] = self.Input.Yes_Or_No(text)

		if self.media_dictionary["register"]["post_on_social_networks"] == True:
			Open_Social_Network(option_info = {"type": "profile"}, social_network_parameter = "WhatsApp", first_space = False, second_space = False)

			self.Input.Type(self.language_texts["press_enter_to_copy_the_watched_text"])

			self.Text.Copy(self.media_dictionary["register"]["Diary Slim"]["text"])

		print()
		print("-----")
		print()

	def Write_On_Diary_Slim(self):
		# Add "Posted on Social Networks" text if the user wanted to post the episode text on the Social Networks
		if self.media_dictionary["register"]["post_on_social_networks"] == True:
			self.media_dictionary["register"]["Diary Slim"]["text"] += "\n\n" + self.media_dictionary["register"]["Diary Slim"]["posted_on_social_networks"]

		Write_On_Diary_Slim_Module(self.media_dictionary["register"]["Diary Slim"]["text"], add_time = False)

	def Show_Information(self):
		self.media_dictionary["header_text"] = self.Text.Capitalize(self.media_dictionary["media"]["texts"]["container_text"]["container"]) + ": "

		if self.media_dictionary["media"]["states"]["completed"] == True:
			text = self.media_dictionary["media"]["texts"]["container_text"]["this"]
			self.media_dictionary["header_text"] = self.language_texts["you_finished_watching_{}"].format(text) + ": "

		self.Show_Media_Information(self.media_dictionary)