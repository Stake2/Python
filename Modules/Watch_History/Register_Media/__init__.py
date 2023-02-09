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
		self.media_dictionary["Register"] = {
			"Diary Slim": {
				"text": ""
			},
			"Times": {
				"UTC": self.media_dictionary["media"]["finished_watching"]["utc"],
				"date_time_format": self.media_dictionary["media"]["finished_watching"]["date_time_format"]
			}
		}

		self.Define_Diary_Slim_Text()

		self.Register_In_JSON()
		self.Create_File()

		self.Add_File_To_Year_Folder()

		self.Check_Media_Status()

		if self.media_dictionary["media"]["States"]["completed"] == True or self.media_dictionary["media"]["States"]["completed_item"] == True:
			self.Set_Media_As_Completed()

		self.Post_On_Social_Networks()

		self.Write_On_Diary_Slim()

		if self.switches["verbose"] == True:
			print()
			print(self.large_bar)
			print()
			print("Register_Media:")

		self.Show_Information()

	def Ask_For_Media_Info(self):
		# To-Do: Make this method
		pass

	def Define_Diary_Slim_Text(self):
		template = self.language_texts["i_just_finished_watching_{}"]

		if self.media_dictionary["media"]["States"]["series_media"] == True:
			template += ' "{}"'

			text = self.media_dictionary["media_type"]["genders"]["of_the"]

			if self.media_dictionary["media"]["States"]["video"] == True:
				text = self.media_types["genders"][self.user_language]["masculine"]["of_the"]

			# Add unit and "of the" text
			self.watched_item_text = self.language_texts["this_{}_{}"].format(self.media_dictionary["media"]["texts"]["unit"][self.user_language], text)

			# Replaced "watching" with "re-watching" text
			if self.media_dictionary["media"]["States"]["re_watching"] == True:
				template = template.replace(self.language_texts["watching, infinitive"], self.language_texts["re_watching, infinitive"])

				template = template.replace(self.language_texts["re_watching, infinitive"], self.language_texts["re_watching, infinitive"] + " " + self.media_dictionary["media"]["episode"]["re_watched"]["time_text"][self.user_language])

			if self.media_dictionary["media"]["States"]["single_unit"] == False:
				# Replace "this" text with "the first" if the episode is the first one
				if self.media_dictionary["media"]["episode"]["title"] == self.media_dictionary["media"]["item"]["episodes"]["titles"][self.user_language][0]:
					self.watched_item_text = self.watched_item_text.replace(self.language_texts["this, masculine"], self.language_texts["the_first, masculine"])

				# Replace "this" text with "the last" if the episode is the last one
				if self.media_dictionary["media"]["episode"]["title"] == self.media_dictionary["media"]["item"]["episodes"]["titles"][self.user_language][-1] or len(self.media_dictionary["media"]["item"]["episodes"]["titles"][self.user_language]) == 1:
					self.watched_item_text = self.watched_item_text.replace(self.language_texts["this, masculine"], self.language_texts["the_last, masculine"])

			if "Movie" in self.media_dictionary["media"]["episode"]["titles"][self.user_language]:
				self.watched_item_text = self.watched_item_text.replace(self.language_texts["episode"], self.language_texts["movie"])

			self.of_the_text = self.language_texts["of_the_{}"]

			if self.media_dictionary["media"]["States"]["media_list"] == True and self.media_dictionary["media"]["item"]["title"] != self.media_dictionary["media"]["title"] and self.media_dictionary["media"]["States"]["single_unit"] == False:
				if self.media_dictionary["media"]["States"]["video"] == False:
					text = ""

					# Replace "of the" text with "of the first" if the media item is the first one
					if self.media_dictionary["media"]["item"]["title"] == self.media_dictionary["media"]["items"]["list"][0]:
						text = " " + self.language_texts["first, feminine"]

					# Replace "of the" text with "of the last" if the media item is the last one
					if self.media_dictionary["media"]["item"]["title"] == self.media_dictionary["media"]["items"]["list"][-1]:
						text = " " + self.language_texts["last, feminine"]

					# Add item text ("season" or "series") to "of the" text
					self.of_the_text = self.of_the_text.format(text + self.media_dictionary["media"]["texts"]["item"][self.user_language])

				if self.media_dictionary["media"]["States"]["video"] == True:
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
			self.media_dictionary["Register"]["Diary Slim"]["text"] = template.format(self.watched_item_text, self.media_dictionary["media"]["titles"]["language"])

		# If the media is a movie, only add the "this" text and the media type "movie" text in user language
		if self.media_dictionary["media"]["States"]["series_media"] == False:
			self.media_dictionary["Register"]["Diary Slim"]["text"] = template.format(self.media_dictionary["media_type"]["genders"]["this"] + " " + self.media_dictionary["media_type"]["singular"][self.user_language].lower())

		# Add language media episode (or movie title)
		if self.media_dictionary["media"]["States"]["single_unit"] == False:
			self.media_dictionary["Register"]["Diary Slim"]["text"] += ":\n" + self.media_dictionary["media"]["episode"]["titles"][self.user_language]

		if self.media_dictionary["media"]["States"]["single_unit"] == True:
			self.media_dictionary["Register"]["Diary Slim"]["text"] += ":\n" + self.media_dictionary["media"]["episode"]["with_title"][self.user_language]

		if self.media_dictionary["media"]["States"]["re_watching"] == True:
			self.media_dictionary["Register"]["Diary Slim"]["text"] += self.media_dictionary["media"]["episode"]["re_watched"]["text"]

		# Add YouTube video link for video media
		if self.media_dictionary["media"]["States"]["video"] == True:
			self.media_dictionary["Register"]["Diary Slim"]["text"] += "\n\n" + self.media_dictionary["media"]["episode"]["remote"]["link"]

		self.media_dictionary["Register"]["Diary Slim"]["text"] = self.media_dictionary["media"]["finished_watching"]["date_time_format"][self.user_language] + ":\n" + self.media_dictionary["Register"]["Diary Slim"]["text"]

	def Register_In_JSON(self):
		self.media_type = self.media_dictionary["media_type"]["plural"]["en"]

		self.watched = self.JSON.To_Python(self.media_dictionary["media"]["item"]["folders"]["watched"]["watched"])

		# Add to watched episode, root episode and media type episode numbers
		self.episodes["Number"] += 1
		self.watched["Number"] += 1
		self.media_type_episodes[self.media_type]["Number"] += 1

		self.media_dictionary["Register"].update({
			"Episode titles": {}
		})

		# Define sanitized version of entry name for files
		self.media_dictionary["Register"]["Entries"] = {
			"normal": str(self.episodes["Number"]) + ". " + self.media_type + " (" + self.media_dictionary["Register"]["Times"]["date_time_format"][self.user_language] + ")",
			"sanitized": {}
		}

		# Define sanitized version of entry name for files (per language)
		for language in self.languages["small"]:
			self.media_dictionary["Register"]["Entries"]["sanitized"][language] = str(self.episodes["Number"]) + ". " + self.media_type + " (" + self.media_dictionary["Register"]["Times"]["date_time_format"][language].replace(":", ";").replace("/", "-") + ")"

		# Add to "Entries" list
		self.episodes["Entries"].append(self.media_dictionary["Register"]["Entries"]["normal"])
		self.media_type_episodes[self.media_type]["Entries"].append(self.media_dictionary["Register"]["Entries"]["normal"])
		self.watched["Entries"].append(self.media_dictionary["Register"]["Entries"]["normal"])

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

		key = self.media_dictionary["Register"]["Entries"]["normal"]

		self.episodes["Dictionary"][key] = {
			"Number": self.episodes["Number"],
			"Type number": self.media_type_episodes[self.media_type]["Number"],
			"Entry": self.media_dictionary["Register"]["Entries"]["normal"],
			"Media": media_titles,
			"Item": item_titles,
			"Episode titles": self.media_dictionary["Register"]["Episode titles"],
			"Episode number": "",
			"Type": self.media_type,
			"Time": self.media_dictionary["Register"]["Times"]["UTC"]
		}

		if self.media_dictionary["media"]["States"]["media_list"] == False or self.media_dictionary["media"]["item"]["title"] == self.media_dictionary["media"]["title"] or self.media_dictionary["media"]["States"]["series_media"] == False:
			self.episodes["Dictionary"][key].pop("Item")

		# Remove episode titles and number keys of dictionary if media is non-series media or single unit
		if self.media_dictionary["media"]["States"]["series_media"] == False or self.media_dictionary["media"]["States"]["single_unit"] == True or self.media_dictionary["media"]["States"]["episodic"] == False:
			self.episodes["Dictionary"][key].pop("Episode titles")
			self.episodes["Dictionary"][key].pop("Episode number")

		# Define episode number on dictionary if media is series media and not single unit
		if self.media_dictionary["media"]["States"]["series_media"] == True and self.media_dictionary["media"]["States"]["single_unit"] == False and self.media_dictionary["media"]["States"]["episodic"] == True:
			self.episodes["Dictionary"][key]["Episode number"] = self.media_dictionary["media"]["episode"]["number"]

		# Add episode ID if the key is present inside the episode dictionary
		if "id" in self.media_dictionary["media"]["episode"]:
			self.episodes["Dictionary"][key]["ID"] = self.media_dictionary["media"]["episode"]["id"]

		dict_ = self.Define_States_Dictionary(self.media_dictionary)

		key = self.media_dictionary["Register"]["Entries"]["normal"]

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

		# Add to root and media type "Entry list.txt" file
		self.File.Edit(self.folders["watch_history"]["current_year"]["entry_list"], self.media_dictionary["Register"]["Entries"]["normal"], "a")
		self.File.Edit(self.media_dictionary["media_type"]["folders"]["per_media_type"]["entry_list"], self.media_dictionary["Register"]["Entries"]["normal"], "a")

		# ---------------------------- #

		if self.media_dictionary["comment_writer"]["States"]["write"] == True:
			self.watched["Comments"] += 1

		# Add episode number to "Episode number" list for series media
		if self.media_dictionary["media"]["States"]["series_media"] == True and self.media_dictionary["media"]["States"]["single_unit"] == False:
			self.media_dictionary["Register"]["entry"] = str(self.media_dictionary["media"]["episode"]["number"])

			# Add episode title if media is non-episodic
			if self.media_dictionary["media"]["States"]["episodic"] == False:
				self.media_dictionary["Register"]["entry"] = self.media_dictionary["media"]["episode"]["title"]

		# If media is not a series media or media item is a single unit
		if self.media_dictionary["media"]["States"]["series_media"] == False or self.media_dictionary["media"]["States"]["single_unit"] == True:
			# Define the "Entry" string as the entry
			self.watched["Entry"] = self.media_dictionary["Register"]["entry"]

		# If media is a series media and media item is not single unit
		if self.media_dictionary["media"]["States"]["series_media"] == True and self.media_dictionary["media"]["States"]["single_unit"] == False:
			# Add the entry to the entries list
			self.watched["Entry"].append(self.media_dictionary["Register"]["entry"])

		# Define "Watched" entry dictionary as media type entry dictionary
		self.watched["Dictionary"][self.media_dictionary["Register"]["entry"]] = self.media_type_episodes[self.media_type]["Dictionary"][key]

		# Update media "Watched.json" file
		self.JSON.Edit(self.media_dictionary["media"]["item"]["folders"]["watched"]["watched"], self.watched)

	def Create_File(self):
		# Number: [Episode number]
		# Type number: [Type number]
		# 
		# Media:
		# [Media titles]
		# (
		# Item:
		# [Item titles]
		# 
		# [Episode/Video] titles:
		# [Episode titles]
		# )
		# Type: [Media type]
		#
		# Times:
		# [Episode times]
		# 
		# File name: [Number. Type (Time)]

		# Define episode file
		folder = self.media_dictionary["media_type"]["folders"]["per_media_type"]["files"]["root"]
		file = folder + self.media_dictionary["Register"]["Entries"]["sanitized"][self.user_language] + ".txt"
		self.File.Create(file)

		self.media_dictionary["Register"]["file_text"] = {}

		self.media_dictionary["Register"]["file_text"]["general"] = self.Define_File_Text("general")

		for language in self.languages["small"]:
			self.media_dictionary["Register"]["file_text"][language] = self.Define_File_Text(language)

		# Write episode text into episode file
		self.File.Edit(file, self.media_dictionary["Register"]["file_text"]["general"], "w")

		# Write episode text into "Watched" episode file
		folder = self.media_dictionary["media"]["item"]["folders"]["watched"]["root"]

		if self.media_dictionary["media"]["States"]["series_media"] == True:
			folder = self.media_dictionary["media"]["item"]["folders"]["watched"]["files"]["root"]

		file = folder + self.media_dictionary["Register"]["entry"]

		if self.media_dictionary["media"]["States"]["re_watching"] == True:
			file += " (" + self.media_dictionary["media"]["episode"]["re_watched"]["text"] + ")"

		file += ".txt"

		self.File.Create(file)
		self.File.Edit(file, self.media_dictionary["Register"]["file_text"][self.user_language], "w")

	def Define_File_Text(self, language_parameter = None):
		if language_parameter != "general":
			language = language_parameter

		if language_parameter == "general":
			language = "en"

		full_language = self.languages["full"][language]

		# Define episode text lines
		lines = [
			self.Language.texts["number, title()"][language] + ": " + str(self.episodes["Number"]),
			self.texts["media_type_number"][language] + ": " + str(self.media_type_episodes[self.media_type]["Number"]),
			"\n" + self.texts["media, title()"][language] + ":" + "\n" + "{}"
		]

		# Add item and episode titles lines
		if self.media_dictionary["media"]["States"]["series_media"] == True:
			if self.media_dictionary["media"]["States"]["media_list"] == True and self.media_dictionary["media"]["item"]["title"] != self.media_dictionary["media"]["title"]:
				lines.append(self.texts["item, title()"][language] + ":" + "\n" + "{}")

			if self.media_dictionary["media"]["States"]["single_unit"] == False:
				text = self.texts["episode_titles"][language]

				if language_parameter != "general":
					text = self.texts["episode_title"][language]

				if self.media_dictionary["media"]["States"]["video"] == True:
					text = self.texts["video_titles"][language]

				lines.append(text + ":" + "\n" + "{}")

		lines.extend([
			self.Language.texts["type, title()"][language] + ": " + self.media_dictionary["media_type"]["plural"]["en"] + "\n",
			self.Date.texts["times, title()"][language] + ":" + "\n" + "{}",
			self.File.texts["file_name"][language] + ": " + self.media_dictionary["Register"]["Entries"]["normal"]
		])

		# Add states texts lines
		if "States" in self.episodes["Dictionary"][self.media_dictionary["Register"]["Entries"]["normal"]]:
			dict_ = self.episodes["Dictionary"][self.media_dictionary["Register"]["Entries"]["normal"]]["States"]

			text = "\n" + self.Language.texts["states, title()"][language] + ":" + "\n"

			for key in dict_:
				key = key.lower()

				if key != "re_watched":
					text_key = key

					if "_" not in key:
						text_key += ", title()"

					if key != "first_media_type_episode_in_year":
						language_text = self.texts[text_key][language]

					if key == "first_media_type_episode_in_year":
						container = self.media_dictionary["media"]["texts"]["container"][language].lower()

						if self.media_dictionary["media"]["States"]["video"] == True:
							container = self.media_dictionary["media"]["texts"]["unit"][language]

						language_text = self.texts["first_{}_in_year"][language].format(container)

					text += language_text

				if key == "re_watched":
					text += self.media_dictionary["media"]["episode"]["re_watched"]["re_watched_text"][language] + " (" + str(self.media_dictionary["media"]["episode"]["re_watched"]["times"]) + "x)"

				if key != list(dict_.keys())[-1].lower():
					text += "\n"

			lines.append(text)

		# Define language episode text
		file_text = self.Text.From_List(lines)

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

		if self.media_dictionary["media"]["States"]["series_media"] == True:
			# Add media item titles to media item titles list
			if self.media_dictionary["media"]["States"]["media_list"] == True and self.media_dictionary["media"]["item"]["title"] != self.media_dictionary["media"]["title"]:
				key = "original"

				if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"] and "romanized" in self.media_dictionary["media"]["item"]["titles"]:
					key = "romanized"

				item_titles = self.media_dictionary["media"]["item"]["titles"][key]

				if self.media_dictionary["media"]["item"]["titles"]["language"] != self.media_dictionary["media"]["item"]["titles"][key]:
					item_titles += "\n" + self.media_dictionary["media"]["item"]["titles"]["language"]

				items.append(item_titles + "\n")

			if self.media_dictionary["media"]["States"]["single_unit"] == False:
				# Add episode titles to episode titles list
				episode_titles = ""

				if language_parameter != "general":
					episode_title = self.media_dictionary["media"]["episode"]["titles"][language]

					if episode_title == "":
						episode_title = "[" + self.Language.texts["empty, title()"][language] + "]"

					episode_titles = episode_title + "\n"

				if language_parameter == "general":
					for language in self.languages["small"]:
						episode_title = self.media_dictionary["media"]["episode"]["titles"][language]

						if episode_title == "":
							episode_title = "[" + self.Language.texts["empty, title()"][language] + "]"

						episode_titles += episode_title + "\n"

				items.append(episode_titles)

		# Add times to items list
		times = ""

		for key in ["UTC", "date_time_format"]:
			time = self.media_dictionary["Register"]["Times"][key]

			if key == "UTC":
				times += time + "\n"

			if key == "date_time_format":
				if language_parameter != "general":
					times += time[language] + "\n"

				if language_parameter == "general":
					for language in self.languages["small"]:
						times += time[language] + "\n"

		items.append(times)

		return file_text.format(*items)

	def Add_File_To_Year_Folder(self):
		# Create folders
		for language in self.languages["small"]:
			full_language = self.languages["full"][language]

			# Folder names
			root_folder = self.texts["watched_media"][language]
			type_folder = self.media_dictionary["media_type"]["singular"][language]

			# Watched media folder
			folder = self.current_year["folders"][full_language]["root"]

			self.current_year["folders"][full_language][root_folder] = {
				"root": folder + root_folder + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][root_folder]["root"])

			# Media type folder
			folder = self.current_year["folders"][full_language][root_folder]["root"]

			self.current_year["folders"][full_language][root_folder][type_folder] = {
				"root": folder + type_folder + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][root_folder][type_folder]["root"])

			# Firsts Of The Year subfolder folder
			firsts_of_the_year_text = self.Language.texts["firsts_of_the_year"][language]
			subfolder_name = self.texts["media, title()"][language]

			folder = self.current_year["folders"][full_language][firsts_of_the_year_text]["root"]

			self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name] = {
				"root": folder + subfolder_name + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name]["root"])

			# Firsts Of The Year media type folder
			folder = self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name]["root"]
			
			self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder] = {
				"root": folder + type_folder + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder]["root"])

			# Watched media file
			folder = self.current_year["folders"][full_language][root_folder][type_folder]["root"]
			file_name = self.media_dictionary["Register"]["Entries"]["sanitized"][language]
			self.current_year["folders"][full_language][root_folder][type_folder][file_name] = folder + file_name + ".txt"

			self.File.Create(self.current_year["folders"][full_language][root_folder][type_folder][file_name])

			self.File.Edit(self.current_year["folders"][full_language][root_folder][type_folder][file_name], self.media_dictionary["Register"]["file_text"][language], "w")

			# First media type episode in year file
			if self.media_dictionary["media"]["States"]["first_media_type_episode_in_year"] == True:
				folder = self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder]["root"]

				self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name] = folder + file_name + ".txt"
				self.File.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name])

				self.File.Edit(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name], self.media_dictionary["Register"]["file_text"][language], "w")

	def Check_Media_Status(self):
		if self.media_dictionary["media"]["States"]["series_media"] == True:
			# If the media has a media list and the episode title is the last one
			if self.media_dictionary["media"]["States"]["media_list"] == True and self.media_dictionary["media"]["episode"]["title"] == self.media_dictionary["media"]["item"]["episodes"]["titles"][self.user_language][-1]:
				# And the episode is not a video
				if self.media_dictionary["media"]["States"]["video"] == False:
					# If the media item is the last media item, define the media as completed
					if self.media_dictionary["media"]["item"]["title"] == self.media_dictionary["media"]["items"]["list"][-1]:
						self.media_dictionary["media"]["States"]["completed"] = True

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
								"media": self.media_dictionary["media"]["folders"]["media"]["root"] + self.Sanitize_Title(title) + "/",
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

				self.media_dictionary["media"]["States"]["completed_item"] = True

			# If the media has no media list and the episode title is the last one, define the media as completed
			if self.media_dictionary["media"]["States"]["media_list"] == False and self.media_dictionary["media"]["episode"]["title"] == self.media_dictionary["media"]["item"]["episodes"]["titles"][self.user_language][-1]:
				self.media_dictionary["media"]["States"]["completed"] = True

		# If the media is a movie, define it as completed
		if self.media_dictionary["media"]["States"]["series_media"] == False:
			self.media_dictionary["media"]["States"]["completed"] = True

		# If the media and media item are not completed, get next episode number
		if self.media_dictionary["media"]["States"]["completed"] == False and self.media_dictionary["media"]["States"]["completed_item"] == False:
			# Get next episode language title
			self.media_dictionary["media"]["episode"]["next"] = self.media_dictionary["media"]["item"]["episodes"]["titles"][self.user_language][self.media_dictionary["media"]["episode"]["number"]]

			# Add hybrid origin type to episode title
			if self.media_dictionary["media"]["States"]["hybrid"] == True:
				self.media_dictionary["media"]["episode"]["next"] += self.media_dictionary["media"]["episode"]["hybrid_origin_type"]

			# Define current episode to watch as the next episode
			self.media_dictionary["media"]["item"]["details"][self.language_texts["episode, title()"]] = self.media_dictionary["media"]["episode"]["next"]

			# Update media item details file
			self.File.Edit(self.media_dictionary["media"]["item"]["folders"]["details"], self.Text.From_Dictionary(self.media_dictionary["media"]["item"]["details"]), "w")

		# If the media is completed, define its status as completed
		if self.media_dictionary["media"]["States"]["completed"] == True:
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
		if self.media_dictionary["media"]["States"]["completed_item"] == True:
			# Gets the item dates from the item dates file
			self.media_dictionary["media"]["item"]["dates"] = self.File.Dictionary(self.media_dictionary["media"]["item"]["folders"]["dates"], next_line = True)

			if self.media_dictionary["media"]["States"]["single_unit"] == True:
				self.media_dictionary["media"]["item"]["dates"][self.language_texts["when_i_started_to_watch"] + " " + self.media_dictionary["media"]["texts"]["the_item"][self.user_language]] = self.media_dictionary["media"]["finished_watching"]["date_time_format"][self.user_language]

			# Get started watching time
			self.media_dictionary["media"]["item"]["started_watching_item"] = self.media_dictionary["media"]["item"]["dates"][self.language_texts["when_i_started_to_watch"] + " " + self.media_dictionary["media"]["texts"]["the_item"][self.user_language]]

			# Define time spent watching using started watching time and finished watching time
			self.media_dictionary["media"]["item"]["time_spent_watching"] = self.Date.Difference(self.media_dictionary["media"]["item"]["started_watching_item"], self.media_dictionary["media"]["finished_watching"])["difference_strings"][self.user_language]

			if self.media_dictionary["media"]["item"]["time_spent_watching"][0] + self.media_dictionary["media"]["item"]["time_spent_watching"][1] == ", ":
				self.media_dictionary["media"]["item"]["time_spent_watching"] = self.media_dictionary["media"]["item"]["time_spent_watching"][2:]

			# Format the time template
			self.media_dictionary["media"]["item"]["formatted_template"] = "\n\n" + template.format(self.media_dictionary["media"]["texts"]["the_item"][self.user_language], self.media_dictionary["media"]["item"]["time_spent_watching"])

			# Add the time template to the item dates text
			self.media_dictionary["media"]["item"]["finished_watching_text"] = self.File.Contents(self.media_dictionary["media"]["item"]["folders"]["dates"])["string"] + self.media_dictionary["media"]["item"]["formatted_template"]

			# Update item dates text file
			self.File.Edit(self.media_dictionary["media"]["item"]["folders"]["dates"], self.media_dictionary["media"]["item"]["finished_watching_text"], "w")

			text = self.media_dictionary["media"]["item"]["finished_watching_text"]
			text = text.replace(self.language_texts["when_i_started_to_watch"] + " " + self.media_dictionary["media"]["texts"]["the_item"][self.user_language], self.language_texts["when_i_started_to_watch"])
			text = text.replace(self.language_texts["when_i_finished_watching"] + " " + self.media_dictionary["media"]["texts"]["the_item"][self.user_language], self.language_texts["when_i_finished_watching"])

			# Add the time template to the Diary Slim text if the media is not completed
			if self.media_dictionary["media"]["States"]["completed"] == False and self.media_dictionary["media"]["States"]["single_unit"] == False:
				self.media_dictionary["Register"]["Diary Slim"]["text"] += "\n\n" + text

		# Gets the date that the user started and finished watching the media and writes it to the media dates text file
		if self.media_dictionary["media"]["States"]["completed"] == True:
			# Gets the media dates from the media dates file
			self.media_dictionary["media"]["dates"] = self.File.Dictionary(self.media_dictionary["media"]["folders"]["dates"], next_line = True)

			# Get started watching time
			self.media_dictionary["media"]["started_watching"] = self.Date.From_String(self.media_dictionary["media"]["dates"][self.language_texts["when_i_started_to_watch"] + " " + self.media_dictionary["media"]["texts"]["container_text"]["the"]])

			# Define time spent watching using started watching time and finished watching time
			self.media_dictionary["media"]["time_spent_watching"] = self.Date.Difference(self.media_dictionary["media"]["started_watching"], self.media_dictionary["media"]["finished_watching"])["difference_strings"][self.user_language]

			if self.media_dictionary["media"]["time_spent_watching"][0] + self.media_dictionary["media"]["time_spent_watching"][1] == ", ":
				self.media_dictionary["media"]["time_spent_watching"] = self.media_dictionary["media"]["time_spent_watching"][2:]

			# Format the time template
			self.media_dictionary["media"]["item"]["formatted_template"] = "\n\n" + template.format(self.media_dictionary["media"]["texts"]["container_text"]["the"], self.media_dictionary["media"]["time_spent_watching"])

			# Add the time template to the media dates text
			self.media_dictionary["media"]["finished_watching_text"] = self.File.Contents(self.media_dictionary["media"]["folders"]["dates"])["string"] + self.media_dictionary["media"]["item"]["formatted_template"]

			# Update media dates text file
			self.File.Edit(self.media_dictionary["media"]["folders"]["dates"], self.media_dictionary["media"]["finished_watching_text"], "w")

			text = self.media_dictionary["media"]["finished_watching_text"]
			text = text.replace(self.language_texts["when_i_started_to_watch"] + " " + self.media_dictionary["media"]["texts"]["container_text"]["the"], self.language_texts["when_i_started_to_watch"])
			text = text.replace(self.language_texts["when_i_finished_watching"] + " " + self.media_dictionary["media"]["texts"]["container_text"]["the"], self.language_texts["when_i_finished_watching"])

			# Add the time template to the Diary Slim text
			self.media_dictionary["Register"]["Diary Slim"]["text"] += "\n\n" + text

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

		if self.media_dictionary["media"]["States"]["series_media"] == False:
			text = text.replace(self.language_texts["a_screenshot_of_the_episode"], self.language_texts["movie"])

		if self.media_dictionary["media"]["title"] in ["The Walking Dead", "Yuru Camp"]:
			text = text.replace(self.language_texts["a_screenshot_of_the_episode"], self.language_texts["a_summary_video"])

		self.posted_on_social_networks_text_template = self.language_texts["i_posted_the_watched_text_and_{}_on_the_status_of_{}_and_tweet_on_{}"] + "."

		self.media_dictionary["Register"]["Diary Slim"]["posted_on_social_networks"] = self.posted_on_social_networks_text_template.format(text, self.first_three_social_networks, self.twitter_social_network)

		text = self.language_texts["post_on_the_social_networks"] + " (" + self.social_networks_string + ")"

		self.media_dictionary["Register"]["post_on_social_networks"] = self.Input.Yes_Or_No(text)

		if self.media_dictionary["Register"]["post_on_social_networks"] == True:
			Open_Social_Network(option_info = {"type": "profile"}, social_network_parameter = "WhatsApp", first_space = False, second_space = False)

			self.Input.Type(self.language_texts["press_enter_to_copy_the_watched_text"])

			self.Text.Copy(self.media_dictionary["Register"]["Diary Slim"]["text"])

		print()
		print("-----")
		print()

	def Write_On_Diary_Slim(self):
		# Add "Posted on Social Networks" text if the user wanted to post the episode text on the Social Networks
		if self.media_dictionary["Register"]["post_on_social_networks"] == True:
			self.media_dictionary["Register"]["Diary Slim"]["text"] += "\n\n" + self.media_dictionary["Register"]["Diary Slim"]["posted_on_social_networks"]

		add_dot = True

		if self.media_dictionary["Register"]["post_on_social_networks"] == False and self.media_dictionary["media"]["States"]["video"] == True:
			add_dot = False

		Write_On_Diary_Slim_Module(self.media_dictionary["Register"]["Diary Slim"]["text"], add_time = False, add_dot = add_dot)

	def Show_Information(self):
		self.media_dictionary["header_text"] = self.Text.Capitalize(self.media_dictionary["media"]["texts"]["container_text"]["container"]) + ": "

		if self.media_dictionary["media"]["States"]["completed"] == True:
			text = self.media_dictionary["media"]["texts"]["container_text"]["this"]
			self.media_dictionary["header_text"] = self.language_texts["you_finished_watching_{}"].format(text) + ": "

		self.Show_Media_Information(self.media_dictionary)