# Watch_Media.py

from Watch_History.Watch_History import Watch_History as Watch_History

import re

# A class to Watch media that has the "Watching" or "Re-watching" Watching Status
class Watch_Media(Watch_History):
	def __init__(self, dictionary = {}, run_as_module = False, open_media = True):
		super().__init__()

		import importlib

		classes = [
			"Comment_Writer",
			"Register"
		]

		for title in classes:
			class_ = getattr(importlib.import_module("."  + title, "Watch_History"), title)
			setattr(self, title, class_)

		self.dictionary = dictionary
		self.run_as_module = run_as_module
		self.open_media = open_media

		self.Define_Media_Dictionary()
		self.Define_Episode_Variables()

		if self.media["States"]["Open media"] == True:
			self.Define_Episode_Unit()
			self.Show_Information()
			self.Open_Episode_Unit()
			self.Create_Discord_Status()
			self.Comment_On_Media()
			self.Register_The_Media()

	def Define_Media_Dictionary(self):
		# Select the media type and the media if the dictionary is empty
		if self.dictionary == {}:
			# Ask the user to select a media type and media
			self.dictionary = self.Select_Media_Type_And_Media(watch = True)

		self.media = self.dictionary["Media"]

		self.media["States"]["Open media"] = self.open_media

		# Define the status list for "Plan to watch" related statuses
		status_list = [
			self.texts["plan_to_watch, title()"][self.user_language],
			self.JSON.Language.texts["on_hold, title()"][self.user_language]
		]

		# If the media watching status is inside the status list
		if self.media["Details"][self.JSON.Language.language_texts["status, title()"]] in status_list:
			# If the media "Dates.txt" file is empty
			if self.File.Contents(self.media["folders"]["dates"])["lines"] == []:
				# Get the first watching time where the user started watching the media
				self.media["Started watching time"] = self.Date.Now()["Formats"]["HH:MM DD/MM/YYYY"]

				# Create the Dates text
				self.media["Dates"] = self.language_texts["when_i_started_to_watch"] + ":\n"
				self.media["Dates"] += self.media["Started watching time"]

				self.File.Edit(self.media["folders"]["dates"], self.media["Dates"], "w")

			# If the media has a media item list
			if self.media["States"]["Media item list"] == True:
				# And the media item "Dates.txt" file is empty
				if self.File.Contents(self.media["Item"]["folders"]["dates"])["lines"] == []:
					# Gets the first watching time where the user started watching the media
					self.media["Item"]["Started watching time"] = self.Date.Now()["Formats"]["HH:MM DD/MM/YYYY"]

					# Create the Dates text
					self.media["Item"]["Dates"] = self.language_texts["when_i_started_to_watch"] + ":\n"
					self.media["Item"]["Dates"] += self.media["Item"]["Started watching time"]

					self.File.Edit(self.media["Item"]["folders"]["dates"], self.media["Item"]["Dates"], "w")

			# Change the watching status to "Watching"
			self.Change_Status(self.dictionary, self.language_texts["watching, title()"])

		# Define dubbing for the media
		if self.JSON.Language.language_texts["dubbing, title()"] in self.media["Details"]:
			self.media["States"]["Dubbing"]["Has dubbing"] = True

			self.found_watch_dubbed_setting = False

			details_list = [
				self.media["Details"],
				self.media["Item"]["Details"]
			]

			for details in details_list:
				if self.language_texts["watch_dubbed"] in details:
					self.media["States"]["Dubbing"]["Watch dubbed"] = self.Input.Define_Yes_Or_No(details[self.language_texts["watch_dubbed"]])

					self.found_watch_dubbed_setting = True

		if self.JSON.Language.language_texts["origin_type"] not in self.media["Details"]:
			self.media["States"]["Remote"] = True

			self.media["Details"][self.JSON.Language.language_texts["origin_type"]] = self.JSON.Language.language_texts["remote, title()"]

		# Define remote origin for animes or videos media type
		if self.JSON.Language.language_texts["remote_origin"] not in self.media["Details"]:
			remote_origin = "None"

			if self.dictionary["Media type"]["Plural"]["en"] == self.texts["animes, title()"]["en"]:
				remote_origin = "Animes Vision"

			if self.dictionary["Media type"]["Plural"]["en"] == self.texts["videos, title()"]["en"]:
				remote_origin = "YouTube"

			if remote_origin != "None":
				self.media["Details"][self.JSON.Language.language_texts["remote_origin"]] = remote_origin

	def Define_Episode_Variables(self):
		from copy import deepcopy

		# Definition of episode to watch if the media is not series media
		self.media["Episode"].update({
			"Title": self.media["Titles"]["Original"],
			"Titles": deepcopy(self.media["Titles"]),
			"Sanitized": self.Sanitize(self.media["Titles"]["Original"], restricted_characters = True),
			"Separator": self.media["Episode"]["Separator"]
		})

		# Definition of episode to watch if the media is series media
		if self.media["States"]["Series media"] == True:
			if self.media["States"]["Single unit"] == True:
				for language in self.languages["small"]:
					if language not in self.media["Episode"]["Titles"] or language in self.media["Titles"] and self.media["Episode"]["Titles"][language] == self.media["Titles"][language]:
						self.media["Episode"]["Titles"][language] = self.Get_Media_Title(self.dictionary, language = language, item = True)

					self.media["Item"]["Episodes"]["Titles"][language] = [
						self.media["Episode"]["Titles"][language]
					]

			# If the media language key exists inside the episode titles dictionary
			# Define the episode title as the title in the media language
			if self.media["Language"] in self.media["Item"]["Episodes"]["Titles"]:
				language_titles = self.media["Item"]["Episodes"]["Titles"][self.media["Language"]]

			# Else, define the episode title as the title in the user language and change the media language
			else:
				language_titles = self.media["Item"]["Episodes"]["Titles"][self.user_language]

				self.media["Language"] = self.user_language

			after_key = self.language_texts["episodes, title()"]

			if after_key not in self.media["Item"]["Details"]:
				after_key = self.Date.language_texts["end_date"]

			if after_key not in self.media["Item"]["Details"]:
				after_key = self.Date.language_texts["start_date"]

			# If "Episode" key is not present in media item details, define it as the first episode
			if self.JSON.Language.language_texts["episode, title()"] not in self.media["Item"]["Details"] or self.media["Item"]["Details"][self.JSON.Language.language_texts["episode, title()"]] == "None":
				first_episode_title = ""

				if language_titles != []:
					first_episode_title = language_titles[0]

				episode_title = first_episode_title

				# Add the episode key after the "Episodes" key or update it
				key_value = {
					"key": self.JSON.Language.language_texts["episode, title()"],
					"value": episode_title
				}

				self.media["Item"]["Details"] = self.JSON.Add_Key_After_Key(self.media["Item"]["Details"], key_value, after_key)

				if self.media["States"]["Single unit"] == False:
					# Update media item details file
					self.File.Edit(self.media["Item"]["folders"]["details"], self.Text.From_Dictionary(self.media["Item"]["Details"]), "w")

			# Define media episode dictionary
			self.media["Episode"].update({
				"Title": self.media["Item"]["Details"][self.JSON.Language.language_texts["episode, title()"]],
				"Titles": {},
				"Sanitized": self.Sanitize_Title(self.media["Item"]["Details"][self.JSON.Language.language_texts["episode, title()"]])
			})

			for alternative_episode_type in self.alternative_episode_types:
				if alternative_episode_type in self.media["Episode"]["Title"]:
					self.media["Episode"]["Separator"] = alternative_episode_type

			if self.media["States"]["Single unit"] == True:
				self.media["Episode"]["Number"] = 1

			if self.media["States"]["Single unit"] == False:
				# Get episode number
				i = 1
				for episode_title in language_titles:
					# If the separator is not empty and present in the episode title
					if self.media["Episode"]["Separator"] != "" and self.media["Episode"]["Separator"] in episode_title:
						# Remove the separator and number
						episode_title = re.sub(self.media["Episode"]["Separator"] + "[0-9]{1,3} ", "", episode_title)

						# Define the expression as "current episode title" inside the episode title (not an exact match)
						expression = episode_title in self.media["Episode"]["Title"]

					# If the separator is not empty and does not exist inside the episode title
					# Or the media type is "Videos" (episodic is False for video media, exact match is used)
					# Or the media is non-episodic (exact match is also used for non-episodic media)
					elif (
						self.media["Episode"]["Separator"] != "" and self.media["Episode"]["Separator"] not in episode_title or
						self.media["States"]["Video"] == True or
						self.media["States"]["Episodic"] == False
					):
						# Define the expression as "current episode title" equal to the episode title
						expression = episode_title == self.media["Episode"]["Title"]

					# If the expression is True, define the episode number as the current one
					if expression == True:
						self.media["Episode"]["Number"] = i

					i += 1

			# Define the episode titles per language
			for language in self.languages["small"]:
				episode_titles = self.media["Item"]["Episodes"]["Titles"][language]

				episode_title = ""

				# If the episode titles list is not empty, get the language episode title using the episode number
				if episode_titles != []:
					episode_title = episode_titles[self.media["Episode"]["Number"] - 1]

				self.media["Episode"]["Titles"][language] = episode_title

			# Get YouTube ID for video series media
			if self.media["States"]["Video"] == True:
				self.media["Episode"]["ID"] = self.media["Item"]["Episodes"]["Titles"]["IDs"][self.media["Episode"]["Number"] - 1]

		# Remote media origin, code, and link
		if self.media["States"]["Remote"] == True or self.JSON.Language.language_texts["remote_origin"] in self.media["Details"]:
			# Get remote origin title from media details
			if self.JSON.Language.language_texts["remote_origin"] in self.media["Details"]:
				self.media["Episode"]["Remote"]["Title"] = self.media["Details"][self.JSON.Language.language_texts["remote_origin"]]

			self.media["Episode"]["Remote"]["Link"] = self.remote_origins[self.media["Episode"]["Remote"]["Title"]]

			# Define origin location
			for key in ["origin_location"]:
				text = self.JSON.Language.language_texts[key]

				self.media["Episode"]["Remote"][key] = ""

				if text in self.media["Details"]:
					self.media["Episode"]["Remote"][key] = self.media["Details"][text]

				if text in self.media["Item"]["Details"]:
					self.media["Episode"]["Remote"][key] = self.media["Item"]["Details"][text]

			# Define remote link for the "YouTube" remote
			if self.media["Episode"]["Remote"]["Title"] == "YouTube":
				if "v=" not in self.media["Episode"]["Remote"]["origin_location"]:
					self.media["Episode"]["Remote"]["Link"] += "watch?v=" + self.media["Episode"]["ID"]

					# Add Playlist ID to link if the media has a media item list
					if self.media["States"]["Media item list"] == True:
						self.media["Episode"]["Remote"]["Link"] += "&list=" + self.media["Episode"]["Remote"]["origin_location"]

						# Add the index (number of video on playlist) if the media is episodic
						if self.media["States"]["Episodic"] == True:
							self.media["Episode"]["Remote"]["Link"] += "&index=" + str(self.media["Episode"]["Number"] + 1)

				if "v=" in self.media["Episode"]["Remote"]["origin_location"]:
					self.media["Episode"]["Remote"]["Link"] += "watch?" + self.media["Episode"]["Remote"]["origin_location"]

			# Define remote link for the "Animes Vision" remote
			if self.media["Episode"]["Remote"]["Title"] == "Animes Vision":
				if self.media["Episode"]["Remote"]["origin_location"] == "":
					self.media["Episode"]["Remote"]["origin_location"] = self.media["Titles"]["Sanitized"].lower()

					if self.media["States"]["Replace title"] == True:
						self.media["Episode"]["Remote"]["origin_location"] = self.media["Item"]["Titles"]["Sanitized"].lower()

					# Replace spaces by dashes
					self.media["Episode"]["Remote"]["origin_location"] = self.media["Episode"]["Remote"]["origin_location"].replace(" ", "-")

					# Remove restricted characters for Animes URL
					for text in ["!", ",", ".", "△"]:
						self.media["Episode"]["Remote"]["origin_location"] = self.media["Episode"]["Remote"]["origin_location"].replace(text, "")

				# Add code to link
				self.media["Episode"]["Remote"]["Link"] += self.dictionary["Media type"]["Plural"]["pt"].lower() + "/" + self.media["Episode"]["Remote"]["origin_location"] + "/"

				# Add dubbed text
				if self.media["States"]["Dubbing"]["Has dubbing"] == True and self.media["States"]["Dubbing"]["Watch dubbed"] == True:
					self.media["Episode"]["Remote"]["Link"] = self.media["Episode"]["Remote"]["Link"].replace(self.media["Episode"]["Remote"]["origin_location"], self.media["Episode"]["Remote"]["origin_location"] + "-" + self.JSON.Language.texts["dubbed"]["pt"].lower())

				# Add episode number
				self.media["Episode"]["Remote"]["Link"] += "episodio-" + str(self.Text.Add_Leading_Zeroes(self.media["Episode"]["Number"])) + "/"

				# Add dubbed text to media link if the media has a dub in the user language and user wants to watch it dubbed
				if self.media["States"]["Dubbing"]["Has dubbing"] == True and self.media["States"]["Dubbing"]["Watch dubbed"] == True:
					self.media["Episode"]["Remote"]["Link"] += self.JSON.Language.texts["dubbed, title()"]["pt"].lower()

				# Add subbed text to media link if there is no dub for the media or the user wants to watch it subbed
				if self.media["States"]["Dubbing"]["Has dubbing"] == False or self.media["States"]["Dubbing"]["Watch dubbed"] == False:
					self.media["Episode"]["Remote"]["Link"] += self.JSON.Language.texts["subbed, title()"]["pt"].lower()

			self.media["Episode"]["unit"] = self.media["Episode"]["Remote"]["Link"]

		# Media episode number text definition by episode title and episode separator
		if self.media["States"]["Series media"] == True:
			media_episode = self.media["Episode"]["Title"]

			regex = {
				"one": r"[0-9]{2,4}",
				"two": r"[0-9]{2,4}\-[0-9]{2,4}",
				"episode_and_parenthesis": r"[0-9]{2,4}\([0-9]{2,4}\)"
			}

			results = {}

			for key in regex:
				results[key] = re.findall(regex[key], media_episode)

			self.media["Episode"]["Number text"] = str(self.Text.Add_Leading_Zeroes(self.media["Episode"]["Number"]))

			number = ""

			if results["one"] != [] and str(results["one"][0]) != self.media["Episode"]["Number text"]:
				number = results["one"][0]

			if results["episode_and_parenthesis"] != []:
				number = results["episode_and_parenthesis"][0]

			if results["two"] != []:
				number = self.media["Episode"]["Number text"] + " (" + results["two"][0] + ")"

			if (
				number == self.media["Episode"]["Number text"] or 
				number == "" or
				self.media["States"]["Episodic"] == False
			):
				self.media["Episode"].pop("Number text")

			if "Number text" in self.media["Episode"] and number != self.media["Episode"]["Number text"]:
				self.media["Episode"]["Number text"] = number

		# Defining re_watched times and text
		if self.media["States"]["Re-watching"] == True:
			self.media["Episode"]["re_watched"] = {
				"times": 0,
				"text": "",
				"re_watched_text": {},
				"time_text": {}
			}

			if self.run_as_module == False:
				watched_times = ""

				print()
				print(self.media["Titles"]["Language"] + " " + self.media["Episode"]["Title"])

				while not isinstance(watched_times, int):
					watched_times = self.Input.Type(self.language_texts["type_the_number_of_times_that_you_watched"])

					try:
						watched_times = int(watched_times)

					except ValueError:
						watched_times = 0

			if self.run_as_module == True:
				watched_times = 1

			if watched_times != 0:
				if watched_times != 1:
					self.media["Episode"]["re_watched"]["times"] = watched_times + 1

				else:
					self.media["Episode"]["re_watched"]["times"] = watched_times

				self.media["Episode"]["re_watched"]["text"] = " (" + self.language_texts["re_watched, capitalize()"] + " " + str(self.media["Episode"]["re_watched"]["times"]) + "x)"

				number = self.media["Episode"]["re_watched"]["times"]

				for language in self.languages["small"]:
					text = self.Text.By_Number(number, self.JSON.Language.texts["{}_time"][language], self.JSON.Language.texts["{}_times"][language])

					self.media["Episode"]["re_watched"]["time_text"][language] = text.format(self.Date.texts["number_names_feminine, type: list"][language][number])

					self.media["Episode"]["re_watched"]["re_watched_text"][language] = self.texts["re_watched, capitalize()"][language] + " " + self.media["Episode"]["re_watched"]["time_text"][language]

			if watched_times == 0:
				self.media["States"]["Re-watching"] = False

		# Define media episode with item if media has media item list
		if self.media["States"]["Series media"] == True:
			self.media["separators"] = {
				"title": " ",
				"episode": " "
			}

			for item_type in ["title", "episode"]:
				text = self.JSON.Language.language_texts[item_type + "_separator"]

				if text in self.media["Details"]:
					self.media["separators"][item_type] = self.media["Details"][text]

				elif self.media["States"]["Video"] == True:
					self.media["separators"][item_type] = ": "

				# If the item is the title and the ": " is inside the item title
				# Or the item is the episode and the "S[Any number two times]" is found on the item title
				if (
					item_type == "title" and self.media["Item"]["Title"][0] + self.media["Item"]["Title"][1] == ": " or
					item_type == "episode" and re.findall(r"S[0-9]{2}", self.media["Item"]["Title"]) != []
				):
					# The item or episode separator is defined as an empty string
					self.media["separators"][item_type] = ""

			media_title = self.Get_Media_Title(self.dictionary)

			self.media["Episode"].update({
				"with_title_default": "",
				"with_title": {}
			})

			# Define episode with item and episode with title and item keys
			if self.media["States"]["Media item list"] == True and self.media["Item"]["Title"] != self.media["Title"] and self.media["States"]["Single unit"] == False:
				self.media["Episode"].update({
					"with_item": {},
					"with_title_and_item": {}
				})

				# Define the episode with item as the media item + the episode separator and episode title
				self.media["Episode"]["with_item"]["Original"] = self.media["Item"]["Title"] + self.media["separators"]["episode"] + self.media["Episode"]["Title"]

				self.media["Episode"]["with_title_and_item"]["Original"] = ""

				# Add original media title if it is not present in the item title
				if media_title not in self.media["Item"]["Title"]:
					self.media["Episode"]["with_title_and_item"]["Original"] += media_title + self.media["separators"]["title"]

				# Add media title separator and title
				self.media["Episode"]["with_title_and_item"]["Original"] += self.media["Item"]["Title"]

				# Add episode separator and title
				self.media["Episode"]["with_title_and_item"]["Original"] += self.media["separators"]["episode"] + self.media["Episode"]["Title"]

				# Define episode with item and episode with title and item texts per language
				for language in self.languages["small"]:
					media_title = self.Get_Media_Title(self.dictionary, language = language)

					# Define the media item title as the original one
					item_title = self.Get_Media_Title(self.dictionary, language = language, item = True)

					# Define the episode with item as the language media item + the episode separator and language episode title
					self.media["Episode"]["with_item"][language] = item_title + self.media["separators"]["episode"] + self.media["Episode"]["Titles"][language]

					self.media["Episode"]["with_title_and_item"][language] = media_title + self.media["separators"]["title"]

					if self.media["States"]["Replace title"] == False:
						# Add item title to text if "replace title" is False
						self.media["Episode"]["with_title_and_item"][language] += item_title + self.media["separators"]["episode"]

					if self.media["States"]["Replace title"] == True:
						self.media["Episode"]["with_title_and_item"][language] = item_title + self.media["separators"]["episode"]

					self.media["Episode"]["with_title_and_item"][language] += self.media["Episode"]["Titles"][language]

				self.media["Episode"]["with_title_default"] = self.media["Episode"]["with_title_and_item"][self.user_language]

			self.media["Episode"]["with_title"]["Original"] = media_title + self.media["separators"]["title"] + self.media["Episode"]["Title"]

			# Define the episode with title texts per language
			for language in self.languages["small"]:
				media_title = self.Get_Media_Title(self.dictionary, language = language)

				# Replace media title with media item title if "replace title" setting exists inside media details
				if self.media["States"]["Replace title"] == True:
					if language in self.media["Item"]["Titles"]:
						media_title = self.media["Item"]["Titles"][language]

					else:
						media_title = self.media["Item"]["Titles"]["Original"]

				self.media["Episode"]["with_title"][language] = media_title + self.media["separators"]["title"] + self.media["Episode"]["Titles"][language]

			if self.media["States"]["Media item list"] == False or self.media["Item"]["Title"] == self.media["Title"] or self.media["States"]["Single unit"] == True:
				self.media["Episode"]["with_title_default"] = self.media["Episode"]["with_title"][self.user_language]

		# Defining dubbed media text and add it to the media episode if the media is "Animes", has dubbing, and is set to be watched dubbed
		if self.dictionary["Media type"]["Plural"]["en"] == self.texts["animes, title()"]["en"] and self.media["States"]["Dubbing"]["Watch dubbed"] == True:
			self.media["States"]["Dubbing"]["Dubbed to the media title"] = False

			if self.language_texts["dubbed_to_the_media_title"] in self.media["Details"] and self.media["Details"][self.language_texts["dubbed_to_the_media_title"]] == self.Input.language_texts["yes, title()"]:
				self.media["States"]["Dubbing"]["Dubbed to the media title"] = True

			if self.language_texts["dubbed_to_the_media_title"] not in self.media["Details"]:
				self.media["States"]["Dubbing"]["Dubbed to the media title"] = True

			if self.media["States"]["Dubbing"]["Dubbed to the media title"] == True:
				self.media["Episode"]["Dubbing"] = {
					"Text": " " + self.JSON.Language.language_texts["dubbed, title()"]
				}

		# Define accepted file extensions
		self.dictionary["File extensions"] = [
			"mp4",
			"mkv",
			"webm"
		]

		container = self.media["texts"]["container"][self.user_language]

		if self.media["States"]["Video"] == False:
			container = container.lower()

		# Add "dubbed" text to media container text
		if "Dubbing" in self.media["Episode"] and "Text" in self.media["Episode"]["Dubbing"]:
			container = self.JSON.Language.texts["dubbed_{}"][self.user_language].format(container)

		self.media["texts"]["container_text"] = {
			"container": container,
			"this": self.media["texts"]["genders"][self.user_language]["this"] + " " + container,
			"the": self.media["texts"]["genders"][self.user_language]["the"] + " " + container,
			"of_the": self.media["texts"]["genders"][self.user_language]["of_the"] + " " + container
		}

		# Define the header text to be used on the "Show_Media_Information" root method
		self.dictionary["header_text"] = self.language_texts["opening_{}_to_watch"].format(self.media["texts"]["container_text"]["this"]) + ":"

		if self.media["States"]["Re-watching"] == True:
			self.dictionary["header_text"] = self.dictionary["header_text"].replace(self.language_texts["watch"], self.language_texts["re_watch"])

	def Define_Episode_Unit(self):
		# Local media episode file definition
		if self.media["States"]["Local"] == True:
			if self.media["States"]["Video"] == False:
				if self.media["States"]["Dubbing"]["Has dubbing"] == True:
					# Add dubbed text to the media folder if there is dub for the media and user wants to watch it dubbed
					if self.media["States"]["Dubbing"]["Watch dubbed"] == True:
						self.media["Item"]["folders"]["media"]["root"] += self.JSON.Language.texts["dubbed, title()"][self.user_language] + "/"

					if self.File_Exists(self.media["Item"]["folders"]["media"]["root"] + self.media["Episode"]["Sanitized"]) == True:
						self.media["States"]["Dubbing"]["Watch dubbed"] = self.Input.Yes_Or_No(self.language_texts["watch_dubbed"])

			self.Folder.Create(self.media["Item"]["folders"]["media"]["root"])

			# Add media episode to local media folder
			self.media["Episode"]["unit"] = self.media["Item"]["folders"]["media"]["root"] + self.media["Episode"]["Sanitized"]

			file_exists = self.File_Exists(self.media["Episode"]["unit"])

			# If the media has dubbing and no "Watch dubbed" setting was found
			if self.JSON.Language.language_texts["dubbing, title()"] in self.media["Details"] and self.found_watch_dubbed_setting == False:
				# If the file exists and the "Dubbed" text is inside the file, define the "Watch dubbed" state as True
				if file_exists == True and self.JSON.Language.texts["dubbed, title()"][self.user_language] in self.media["Episode"]["unit"]:
					self.media["States"]["Dubbing"]["Watch dubbed"] = True

				# If the user language episode file does not exist
				if file_exists == False:
					# Define the "Watch dubbed" state as False
					self.media["States"]["Dubbing"]["Watch dubbed"] = False

					# Iterate through small languages list
					for language in self.languages["small"]:
						# If the language is not the user language
						# (Exclude the user language because the episode file in the user language was not found)
						if language != self.user_language:
							# Define the full language
							full_language = self.languages["full"][language]

							# Sanitize the language episode title to get the file name
							file_name = self.Sanitize_Title(self.media["Episode"]["Titles"][language])

							# Define the root episode file
							self.media["Episode"]["unit"] = self.media["Item"]["folders"]["media"]["root"].replace(self.full_user_language + "/", "")

							# If the language is not equal to the media language, add the full language folder to the episode unit
							# (Episode units of media on their native language are not placed inside a full language folder)
							if language != self.media["Language"]:
								self.media["Episode"]["unit"] = self.media["Episode"]["unit"] + full_language + "/"
								self.Folder.Create(self.media["Episode"]["unit"])

							# Add the language episode file name to the episode unit
							self.media["Episode"]["unit"] += file_name

							# Check if the language episode file with one of the accepted extensions exist
							for extension in self.dictionary["File extensions"]:
								file = self.media["Episode"]["unit"] + "." + extension

								if self.File.Exist(file) == True:
									self.media["Episode"]["unit"] = file

			# If it does not, then, ask if the user wants to move the file from somewhere to the correct folder
			if file_exists == False:
				print()
				print(self.File.language_texts["file, title()"] + ":")
				print("\t" + self.media["Episode"]["unit"] + "." + str(self.dictionary["File extensions"]).replace("'", "").replace(", ", "/"))
				print()
				print(self.language_texts["the_media_file_does_not_exist"] + ".")
				print()

				question = self.language_texts["do_you_want_to_bring_it_from_another_folder"]

				bring_file = self.Input.Yes_Or_No(question, first_space = False)

				if bring_file == True:
					self.media["Episode"]["unit"] = self.Find_Media_file(self.media["Episode"]["Sanitized"])

				if bring_file == False:
					print()
					quit(self.JSON.Language.language_texts["alright"] + ".")

	def File_Exists(self, file):
		file_exists = False

		# Check if an episode file with one of the accepted extensions exist
		for extension in self.dictionary["File extensions"]:
			if "." + extension not in file:
				file += "." + extension

			if self.File.Exist(file) == True:
				file_exists = True

				self.media["Episode"]["unit"] = file

		return file_exists

	def Show_Information(self):
		self.Show_Media_Information(self.dictionary)

	def Open_Episode_Unit(self):
		# Open media unit with its executor
		self.File.Open(self.media["Episode"]["unit"])

	# Make Discord Custom Status for the media or media episode that is going to be watched and copy it
	def Create_Discord_Status(self):
		template = self.language_texts["watching, title()"]

		key = "with_title"

		if self.media["States"]["Media item list"] == True and self.media["Item"]["Title"] != self.media["Title"] and self.media["States"]["Video"] == False and self.media["States"]["Single unit"] == False:
			key = "with_title_and_item"

		self.dictionary["discord_status"] = template + " " + self.dictionary["Media type"]["Singular"][self.user_language] + ": " + self.media["Episode"][key][self.user_language]

		self.Text.Copy(self.dictionary["discord_status"])

	def Comment_On_Media(self):
		# Ask to comment on media (using Comment_Writer class)
		self.dictionary = self.Comment_Writer(self.dictionary).dictionary

	def Register_The_Media(self):
		text = self.language_texts["press_enter_when_you_finish_watching"]

		# Text to show in the input when the user finishes watching the media (pressing Enter)
		text = text + " " + self.media["texts"]["the_unit"][self.user_language]

		self.media["States"]["Finished watching"] = self.Input.Type(text)
		self.media["States"]["Finished watching"] = True

		# Register the finished watching time
		self.dictionary["Entry"] = {
			"Date": self.Date.Now()
		}

		# Use the "Register" class to register the watched media, and giving the dictionary to it
		self.Register(self.dictionary)

	def Find_Media_file(self, file_name):
		self.frequently_used_folders = [
			self.Folder.folders["user"]["downloads"]["root"],
			self.Folder.folders["user"]["downloads"]["videos"]["root"],
			self.Folder.folders["user"]["downloads"]["mega"]["root"]
		]

		old_file = self.Select_Folder_And_Media_File(self.frequently_used_folders)

		new_file = self.media["Item"]["folders"]["media"]["root"] + self.Sanitize(file_name, restricted_characters = True) + "."

		text = self.language_texts["please_select_a_file_that_is_in_the_format"] + " "

		for extension in self.dictionary["File extensions"]:
			if extension == self.dictionary["File extensions"][-1]:
				text += self.JSON.Language.language_texts["genders, type: dict, masculine"]["or"] + " "

			text += extension.upper()

			if extension != self.dictionary["File extensions"][-1]:
				text += ", "

		if old_file.split(".")[-1] not in self.dictionary["File extensions"]:
			while old_file.split(".")[-1] not in self.dictionary["File extensions"]:
				print()
				print(text + ".")

				old_file = self.Select_Folder_And_Media_File(self.frequently_used_folders)

				new_file = self.media["Item"]["folders"]["media"]["root"] + file_name + "."

		self.moved_succesfully = False

		if old_file.split(".")[-1] in self.dictionary["File extensions"]:
			self.moved_succesfully = self.Move_Media_File(old_file, new_file)

		if self.moved_succesfully == True:
			unit = new_file

			print()
			print("-----")
			print()

			return unit

		if self.moved_succesfully == False:
			quit()

	def Select_Folder_And_Media_File(self, folders):
		show_text = self.Folder.language_texts["folders, title()"]
		select_text = self.language_texts["select_one_folder_to_search_for_the_file"]

		location = self.Input.Select(folders, show_text = show_text, select_text = select_text)["option"]

		files = self.Folder.Contents(location, add_sub_folders = False)["file"]["list"]

		select_text = self.language_texts["select_the_media_file"]

		return self.Input.Select(files, select_text = select_text)["option"]

	def Move_Media_File(self, old_file, new_file):
		for extension in self.dictionary["File extensions"]:
			if extension in old_file:
				new_file = new_file + extension

		return self.File.Move(old_file, new_file)