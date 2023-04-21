# Watch_Media.py

from Watch_History.Watch_History import Watch_History as Watch_History

import re

# A class to Watch media that has the "Watching" or "Re-watching" Watching Status
class Watch_Media(Watch_History):
	def __init__(self, media_dictionary = {}, run_as_module = False, open_media = True):
		super().__init__()

		import importlib

		classes = [
			"Comment_Writer",
			"Register"
		]

		for title in classes:
			class_ = getattr(importlib.import_module("."  + title, "Watch_History"), title)
			setattr(self, title, class_)

		self.media_dictionary = media_dictionary
		self.run_as_module = run_as_module
		self.open_media = open_media

		self.Define_Media_Dictionary()
		self.Define_Episode_Variables()

		if self.media["States"]["open_media"] == True:
			self.Define_Episode_Unit()
			self.Show_Information()
			self.Open_Episode_Unit()
			self.Create_Discord_Status()
			self.Comment_On_Media()
			self.Register_The_Media()

	def Define_Media_Dictionary(self):
		# Select media type and media if media dictionary is empty
		if self.media_dictionary == {}:
			# Define options dictionary, with the media type dictionary containing the status list of the media
			options = {
				"media_type": {
					"status": [
						self.texts["plan_to_watch, title()"]["en"],
						self.texts["watching, title()"]["en"],
						self.texts["re_watching, title()"]["en"],
						self.texts["on_hold, title()"]
					]
				}
			}

			# Define the options for the media dictionary
			self.media_dictionary = self.Define_Options(self.media_dictionary, options)

			# Ask the user to select a media type and media
			self.media_dictionary = self.Select_Media_Type_And_Media(options, watch = True)

		self.media = self.media_dictionary["Media"]

		self.media["States"]["open_media"] = self.open_media

		# Define the status list for "Plan to watch" related media
		status_list = [
			self.texts["plan_to_watch, title()"][self.user_language],
			self.texts["on_hold, title()"][self.user_language]
		]

		# If the media watching status is inside the status list
		if self.media["details"][self.JSON.Language.language_texts["status, title()"]] in status_list and "Old history" not in self.media_dictionary:
			# If the media "Dates.txt" file is empty
			if self.File.Contents(self.media["folders"]["dates"])["lines"] == "":
				# Gets the first watching time where the user started watching the media
				self.media["Started watching time"] = self.Date.Now()["hh:mm DD/MM/YYYY"]

				# Create the Dates text
				self.media["Dates"] = self.language_texts["when_i_started_to_watch"] + ":\n"
				self.media["Dates"] += self.media["Started watching time"]

				self.File.Edit(self.media["folders"]["dates"], self.media["Dates"], "w")

			# If the media has a media item list
			if self.media["States"]["Media item list"] == True:
				# And the media item "Dates.txt" file is empty
				if self.File.Contents(self.media["item"]["folders"]["dates"])["lines"] == "":
					# Gets the first watching time where the user started watching the media
					self.media["item"]["Started watching time"] = self.Date.Now()["hh:mm DD/MM/YYYY"]

					# Create the Dates text
					self.media["item"]["Dates"] = self.language_texts["when_i_started_to_watch"] + ":\n"
					self.media["item"]["Dates"] += self.media["item"]["Started watching time"]

					self.File.Edit(self.media["item"]["folders"]["dates"], self.media["item"]["Dates"], "w")

			# Change the watching status to "Watching"
			self.Change_Status(self.media_dictionary, self.language_texts["watching, title()"])

		# Define dubbing for the media
		if self.language_texts["dubbing, title()"] in self.media["details"]:
			self.media["States"]["Has Dubbing"] = True

			self.found_watch_dubbed_setting = False

			details_list = [
				self.media["details"],
				self.media["item"]["details"]
			]

			for details in details_list:
				if self.language_texts["watch_dubbed"] in details:
					self.media["States"]["Watch dubbed"] = self.Input.Define_Yes_Or_No(details[self.language_texts["watch_dubbed"]])

					self.found_watch_dubbed_setting = True

		if self.language_texts["origin_type"] not in self.media["details"]:
			self.media["States"]["remote"] = True

			self.media["details"][self.language_texts["origin_type"]] = self.language_texts["remote, title()"]

		# Define remote origin for animes or videos media type
		if self.language_texts["remote_origin, title()"] not in self.media["details"]:
			remote_origin = "None"

			if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["animes, title()"]["en"]:
				remote_origin = "Animes Vision"

			if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["videos, title()"]["en"]:
				remote_origin = "YouTube"

			if remote_origin != "None":
				self.media["details"][self.language_texts["remote_origin, title()"]] = remote_origin

	def Define_Episode_Variables(self):
		from copy import deepcopy

		# Definition of episode to watch if the media is not series media
		self.media["episode"].update({
			"title": self.media["Titles"]["Original"],
			"titles": deepcopy(self.media["Titles"]),
			"Sanitized": self.Sanitize(self.media["Titles"]["Original"], restricted_characters = True),
			"separator": self.media["episode"]["separator"]
		})

		# Definition of episode to watch if the media is series media
		if self.media["States"]["series_media"] == True:
			if self.media["States"]["single_unit"] == True:
				for language in self.languages["small"]:
					if language not in self.media["episode"]["titles"] or language in self.media["Titles"] and self.media["episode"]["titles"][language] == self.media["Titles"][language]:
						self.media["episode"]["titles"][language] = self.Get_Media_Title(self.media_dictionary, language = language, item = True)

					self.media["item"]["episodes"]["titles"][language] = [
						self.media["episode"]["titles"][language]
					]

			# If the media language key exists inside the episode titles dictionary
			# Define the episode title as the title in the media language
			if self.media["Language"] in self.media["item"]["episodes"]["titles"]:
				language_titles = self.media["item"]["episodes"]["titles"][self.media["Language"]]

			# Else, define the episode title as the title in the user language and change the media language
			else:
				language_titles = self.media["item"]["episodes"]["titles"][self.user_language]

				self.media["Language"] = self.user_language

			after_key = self.language_texts["episodes, title()"]

			if after_key not in self.media["item"]["details"]:
				after_key = self.Date.language_texts["end_date"]

			if after_key not in self.media["item"]["details"]:
				after_key = self.Date.language_texts["start_date"]

			if "Old history" in self.media_dictionary and "Episode title" in self.media_dictionary["Old history"]:
				# Add the episode key after the "Episodes" key or update it
				key_value = {
					"key": self.language_texts["episode, title()"],
					"value": self.media_dictionary["Old history"]["Episode title"]
				}

				self.media["item"]["details"] = self.JSON.Add_Key_After_Key(self.media["item"]["details"], key_value, after_key)

			# If "Episode" key is not present in media item details, define it as the first episode
			if self.language_texts["episode, title()"] not in self.media["item"]["details"] or self.media["item"]["details"][self.language_texts["episode, title()"]] == "None":
				if language_titles != []:
					first_episode_title = language_titles[0]

				if "Old history" not in self.media_dictionary:
					episode_title = first_episode_title

					# Add the episode key after the "Episodes" key or update it
					key_value = {
						"key": self.language_texts["episode, title()"],
						"value": episode_title
					}

				self.media["item"]["details"] = self.JSON.Add_Key_After_Key(self.media["item"]["details"], key_value, after_key)

				if self.media["States"]["single_unit"] == False:
					# Update media item details file
					self.File.Edit(self.media["item"]["folders"]["details"], self.Text.From_Dictionary(self.media["item"]["details"]), "w")

			# Define media episode dictionary
			self.media["episode"].update({
				"title": self.media["item"]["details"][self.language_texts["episode, title()"]],
				"titles": {},
				"Sanitized": self.Sanitize_Title(self.media["item"]["details"][self.language_texts["episode, title()"]])
			})

			for alternative_episode_type in self.alternative_episode_types:
				if alternative_episode_type in self.media["episode"]["title"]:
					self.media["episode"]["separator"] = alternative_episode_type

			if self.media["States"]["single_unit"] == True:
				self.media["episode"]["number"] = 1

			if self.media["States"]["single_unit"] == False:
				# Get episode number
				i = 1
				for episode_title in language_titles:
					# If the separator is not empty and present in the episode title
					if self.media["episode"]["separator"] != "" and self.media["episode"]["separator"] in episode_title:
						# Remove the separator and number
						episode_title = re.sub(self.media["episode"]["separator"] + "[0-9]{1,3} ", "", episode_title)

						# Define the expression as "current episode title" inside the episode title (not an exact match)
						expression = episode_title in self.media["episode"]["title"]

					# If the separator is not empty and does not exist inside the episode title
					# Or the media type is "Videos" (episodic is False for video media, exact match is used)
					# Or the media is non-episodic (exact match is also used for non-episodic media)
					elif (
						self.media["episode"]["separator"] != "" and self.media["episode"]["separator"] not in episode_title or
						self.media["States"]["video"] == True or
						self.media["States"]["episodic"] == False
					):
						# Define the expression as "current episode title" equal to the episode title
						expression = episode_title == self.media["episode"]["title"]

					# If the expression is True, define the episode number as the current one
					if expression == True:
						self.media["episode"]["number"] = i

					i += 1

			# Define the episode titles per language
			for language in self.languages["small"]:
				episode_titles = self.media["item"]["episodes"]["titles"][language]

				episode_title = ""

				# If the episode titles list is not empty, get the language episode title using the episode number
				if episode_titles != []:
					episode_title = episode_titles[self.media["episode"]["number"] - 1]

				self.media["episode"]["titles"][language] = episode_title

			# Get YouTube ID for video series media
			if self.media["States"]["video"] == True:
				self.media["episode"]["id"] = self.media["item"]["episodes"]["titles"]["ids"][self.media["episode"]["number"] - 1]

		# Remote media origin, code, and link
		if self.media["States"]["remote"] == True or self.language_texts["remote_origin, title()"] in self.media["details"]:
			# Get remote origin title from media details
			if self.language_texts["remote_origin, title()"] in self.media["details"]:
				self.media["episode"]["remote"]["title"] = self.media["details"][self.language_texts["remote_origin, title()"]]

			self.media["episode"]["remote"]["link"] = self.remote_origins[self.media["episode"]["remote"]["title"]]

			# Define origin location
			for key in ["origin_location"]:
				text = self.language_texts[key + ", title()"]

				self.media["episode"]["remote"][key] = ""

				if text in self.media["details"]:
					self.media["episode"]["remote"][key] = self.media["details"][text]

				if text in self.media["item"]["details"]:
					self.media["episode"]["remote"][key] = self.media["item"]["details"][text]

			# Define remote link for the "YouTube" remote
			if self.media["episode"]["remote"]["title"] == "YouTube":
				if "v=" not in self.media["episode"]["remote"]["origin_location"]:
					self.media["episode"]["remote"]["link"] += "watch?v=" + self.media["episode"]["id"]

					# Add Playlist ID to link if the media has a media item list
					if self.media["States"]["Media item list"] == True:
						self.media["episode"]["remote"]["link"] += "&list=" + self.media["episode"]["remote"]["origin_location"]

						# Add the index (number of video on playlist) if the media is episodic
						if self.media["States"]["episodic"] == True:
							self.media["episode"]["remote"]["link"] += "&index=" + str(self.media["episode"]["number"] + 1)

				if "v=" in self.media["episode"]["remote"]["origin_location"]:
					self.media["episode"]["remote"]["link"] += "watch?" + self.media["episode"]["remote"]["origin_location"]

			# Define remote link for the "Animes Vision" remote
			if self.media["episode"]["remote"]["title"] == "Animes Vision":
				if self.media["episode"]["remote"]["origin_location"] == "":
					self.media["episode"]["remote"]["origin_location"] = self.media["Titles"]["Sanitized"].lower()

					if self.media["States"]["Replace title"] == True:
						self.media["episode"]["remote"]["origin_location"] = self.media["item"]["Titles"]["Sanitized"].lower()

					# Replace spaces by dashes
					self.media["episode"]["remote"]["origin_location"] = self.media["episode"]["remote"]["origin_location"].replace(" ", "-")

					# Remove restricted characters for Animes URL
					for text in ["!", ",", ".", "△"]:
						self.media["episode"]["remote"]["origin_location"] = self.media["episode"]["remote"]["origin_location"].replace(text, "")

				# Add code to link
				self.media["episode"]["remote"]["link"] += self.media_dictionary["media_type"]["plural"]["pt"].lower() + "/" + self.media["episode"]["remote"]["origin_location"] + "/"

				# Add dubbed text
				if self.media["States"]["Has Dubbing"] == True and self.media["States"]["Watch dubbed"] == True:
					self.media["episode"]["remote"]["link"] = self.media["episode"]["remote"]["link"].replace(self.media["episode"]["remote"]["origin_location"], self.media["episode"]["remote"]["origin_location"] + "-" + self.texts["dubbed"]["pt"].lower())

				# Add episode number
				self.media["episode"]["remote"]["link"] += "episodio-" + str(self.Text.Add_Leading_Zeroes(self.media["episode"]["number"])) + "/"

				# Add dubbed text to media link if the media has a dub in the user language and user wants to watch it dubbed
				if self.media["States"]["Has Dubbing"] == True and self.media["States"]["Watch dubbed"] == True:
					self.media["episode"]["remote"]["link"] += self.texts["dubbed"]["pt"]

				# Add subbed text to media link if there is no dub for the media or the user wants to watch it subbed
				if self.media["States"]["Has Dubbing"] == False or self.media["States"]["Watch dubbed"] == False:
					self.media["episode"]["remote"]["link"] += self.texts["subbed"]["pt"]

			self.media["episode"]["unit"] = self.media["episode"]["remote"]["link"]

		# Media episode number text definition by episode title and episode separator
		if self.media["States"]["series_media"] == True:
			media_episode = self.media["episode"]["title"]

			regex = {
				"one": r"[0-9]{2,4}",
				"two": r"[0-9]{2,4}\-[0-9]{2,4}",
				"episode_and_parenthesis": r"[0-9]{2,4}\([0-9]{2,4}\)"
			}

			results = {}

			for key in regex:
				results[key] = re.findall(regex[key], media_episode)

			self.media["episode"]["number_text"] = str(self.Text.Add_Leading_Zeroes(self.media["episode"]["number"]))

			number = ""

			if results["one"] != [] and str(results["one"][0]) != self.media["episode"]["number_text"]:
				number = results["one"][0]

			if results["episode_and_parenthesis"] != []:
				number = results["episode_and_parenthesis"][0]

			if results["two"] != []:
				number = self.media["episode"]["number_text"] + " (" + results["two"][0] + ")"

			if (
				number == self.media["episode"]["number_text"] or 
				number == "" or
				self.media["States"]["episodic"] == False
			):
				self.media["episode"].pop("number_text")

			if "number_text" in self.media["episode"] and number != self.media["episode"]["number_text"]:
				self.media["episode"]["number_text"] = number

		# Defining re_watched times and text
		if self.media["States"]["Re-watching"] == True:
			self.media["episode"]["re_watched"] = {
				"times": 0,
				"text": "",
				"re_watched_text": {},
				"time_text": {}
			}

			if self.run_as_module == False:
				watched_times = ""

				if "Old history" in self.media_dictionary:
					watched_times = 0

					if "re_watched" in self.media_dictionary["Old history"]:
						watched_times = self.media_dictionary["Old history"]["re_watched"]["times"]

				else:
					print()
					print(self.media["Titles"]["Language"] + " " + self.media["episode"]["title"])

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
					self.media["episode"]["re_watched"]["times"] = watched_times + 1

				else:
					self.media["episode"]["re_watched"]["times"] = watched_times

				self.media["episode"]["re_watched"]["text"] = " (" + self.language_texts["re_watched, capitalize()"] + " " + str(self.media["episode"]["re_watched"]["times"]) + "x)"

				number = self.media["episode"]["re_watched"]["times"]

				for language in self.languages["small"]:
					text = self.Text.By_Number(number, self.JSON.Language.texts["{}_time"][language], self.JSON.Language.texts["{}_times"][language])

					self.media["episode"]["re_watched"]["time_text"][language] = text.format(self.Date.texts["number_names_feminine, type: list"][language][number])

					self.media["episode"]["re_watched"]["re_watched_text"][language] = self.texts["re_watched, capitalize()"][language] + " " + self.media["episode"]["re_watched"]["time_text"][language]

			if watched_times == 0:
				self.media["States"]["Re-watching"] = False

		# Define media episode with item if media has media item list
		if self.media["States"]["series_media"] == True:
			self.media["separators"] = {
				"title": " ",
				"episode": " "
			}

			for item_type in ["title", "episode"]:
				text = self.language_texts[item_type + "_separator"]

				if text in self.media["details"]:
					self.media["separators"][item_type] = self.media["details"][text]

				elif self.media["States"]["video"] == True:
					self.media["separators"][item_type] = ": "

				# If the item is the title and the ": " is inside the item title
				# Or the item is the episode and the "S[Any number two times]" is found on the item title
				if (
					item_type == "title" and ": " in self.media["item"]["title"] or
					item_type == "episode" and re.findall(r"S[0-9]{2}", self.media["item"]["title"]) != []
				):
					# The item or episode separator is defined as an empty string
					self.media["separators"][item_type] = ""

			media_title = self.Get_Media_Title(self.media_dictionary)

			self.media["episode"].update({
				"with_title_default": "",
				"with_title": {}
			})

			# Define episode with item and episode with title and item keys
			if self.media["States"]["Media item list"] == True and self.media["item"]["title"] != self.media["title"] and self.media["States"]["single_unit"] == False:
				self.media["episode"].update({
					"with_item": {},
					"with_title_and_item": {}
				})

				# Define the episode with item as the media item + the episode separator and episode title
				self.media["episode"]["with_item"]["Original"] = self.media["item"]["title"] + self.media["separators"]["episode"] + self.media["episode"]["title"]

				self.media["episode"]["with_title_and_item"]["Original"] = ""

				# Add original media title if it is not present in the item title
				if media_title not in self.media["item"]["title"]:
					self.media["episode"]["with_title_and_item"]["Original"] += media_title + self.media["separators"]["title"]

				# Add media title separator and title
				self.media["episode"]["with_title_and_item"]["Original"] += self.media["item"]["title"]

				# Add episode separator and title
				self.media["episode"]["with_title_and_item"]["Original"] += self.media["separators"]["episode"] + self.media["episode"]["title"]

				# Define episode with item and episode with title and item texts per language
				for language in self.languages["small"]:
					media_title = self.Get_Media_Title(self.media_dictionary, language = language)

					# Define the media item title as the original one
					item_title = self.Get_Media_Title(self.media_dictionary, language = language, item = True)

					# Define the episode with item as the language media item + the episode separator and language episode title
					self.media["episode"]["with_item"][language] = item_title + self.media["separators"]["episode"] + self.media["episode"]["titles"][language]

					self.media["episode"]["with_title_and_item"][language] = media_title + self.media["separators"]["title"]

					if self.media["States"]["Replace title"] == False:
						# Add item title to text if "replace title" is False
						self.media["episode"]["with_title_and_item"][language] += item_title + self.media["separators"]["episode"]

					if self.media["States"]["Replace title"] == True:
						self.media["episode"]["with_title_and_item"][language] = item_title + self.media["separators"]["episode"]

					self.media["episode"]["with_title_and_item"][language] += self.media["episode"]["titles"][language]

				self.media["episode"]["with_title_default"] = self.media["episode"]["with_title_and_item"][self.user_language]

			self.media["episode"]["with_title"]["Original"] = media_title + self.media["separators"]["title"] + self.media["episode"]["title"]

			# Define the episode with title texts per language
			for language in self.languages["small"]:
				media_title = self.Get_Media_Title(self.media_dictionary, language = language)

				# Replace media title with media item title if "replace title" setting exists inside media details
				if self.media["States"]["Replace title"] == True:
					if language in self.media["item"]["Titles"]:
						media_title = self.media["item"]["Titles"][language]

					else:
						media_title = self.media["item"]["Titles"]["Original"]

				self.media["episode"]["with_title"][language] = media_title + self.media["separators"]["title"] + self.media["episode"]["titles"][language]

			if self.media["States"]["Media item list"] == False or self.media["item"]["title"] == self.media["title"] or self.media["States"]["single_unit"] == True:
				self.media["episode"]["with_title_default"] = self.media["episode"]["with_title"][self.user_language]

		# Defining dubbed media text and it to the media episode if the media is "Animes", has dubbing, and is set to be watched dubbed
		if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["animes, title()"]["en"] and self.media["States"]["Watch dubbed"] == True:
			self.media["States"]["dubbed_to_title"] = False

			if self.language_texts["dubbed_to_title"] in self.media["details"] and self.media["details"][self.language_texts["dubbed_to_title"]] == self.Input.language_texts["yes, title()"]:
				self.media["States"]["dubbed_to_title"] = True

			if self.language_texts["dubbed_to_title"] not in self.media["details"]:
				self.media["States"]["dubbed_to_title"] = True

			if self.media["States"]["dubbed_to_title"] == True:
				self.media["episode"]["dubbed_text"] = " " + self.language_texts["dubbed, title()"]

		# Define accepted file extensions
		self.media_dictionary["file_extensions"] = [
			"mp4",
			"mkv",
			"webm"
		]

		container = self.media["texts"]["container"][self.user_language]

		if self.media["States"]["video"] == False:
			container = container.lower()

		# Add "dubbed" text to media container text
		if "dubbed_text" in self.media["episode"]:
			container = self.texts["dubbed_{}"][self.user_language].format(container)

		self.media["texts"]["container_text"] = {
			"container": container,
			"this": self.media["texts"]["genders"][self.user_language]["this"] + " " + container,
			"the": self.media["texts"]["genders"][self.user_language]["the"] + " " + container,
			"of_the": self.media["texts"]["genders"][self.user_language]["of_the"] + " " + container
		}

		# Define the header text to be used on the "Show_Media_Information" root method
		self.media_dictionary["header_text"] = self.language_texts["opening_{}_to_watch"].format(self.media["texts"]["container_text"]["this"]) + ":"

		if self.media["States"]["Re-watching"] == True:
			self.media_dictionary["header_text"] = self.media_dictionary["header_text"].replace(self.language_texts["watch"], self.language_texts["re_watch"])

	def Define_Episode_Unit(self):
		# Local media episode file definition
		if self.media["States"]["local"] == True:
			if self.media["States"]["series_media"] == True and self.media["States"]["video"] == False:
				# Add "Português" text to media item folder if media has dubbing and watch dubbed is true
				if self.media["States"]["Has Dubbing"] == True and self.media["States"]["Watch dubbed"] == True:
					self.media["item"]["folders"]["media"]["root"] += self.full_user_language + "/"

			self.Folder.Create(self.media["item"]["folders"]["media"]["root"])

			# Add media episode to local media folder
			self.media["episode"]["unit"] = self.media["item"]["folders"]["media"]["root"] + self.media["episode"]["Sanitized"]

			file_exists = self.File_Exists(self.media["episode"]["unit"])

			# If the media has dubbing and no "Watch dubbed" setting was found
			if self.language_texts["dubbing, title()"] in self.media["details"] and self.found_watch_dubbed_setting == False:
				# If the user language episode file exists, ask for the user if it wants to watch the episode dubbed
				if file_exists == True:
					self.media["States"]["Watch dubbed"] = True

				# If the user language episode file does not exist
				if file_exists == False:
					# Define the "Watch dubbed" state as False
					self.media["States"]["Watch dubbed"] = False

					# Iterate through small languages list
					for language in self.languages["small"]:
						# If the language is not the user language
						# (Exclude the user language because the episode file in the user language was not found)
						if language != self.user_language:
							# Define the full language
							full_language = self.languages["full"][language]

							# Sanitize the language episode title to get the file name
							file_name = self.Sanitize_Title(self.media["episode"]["titles"][language])

							# Define the root episode file
							self.media["episode"]["unit"] = self.media["item"]["folders"]["media"]["root"].replace(self.full_user_language + "/", "")

							# If the language is not equal to the media language, add the full language folder to the episode unit
							# (Episode units of media on their native language are not placed inside a full language folder)
							if language != self.media["Language"]:
								self.media["episode"]["unit"] = self.media["episode"]["unit"] + full_language + "/"
								self.Folder.Create(self.media["episode"]["unit"])

							# Add the language episode file name to the episode unit
							self.media["episode"]["unit"] += file_name

							# Check if the language episode file with one of the accepted extensions exist
							for extension in self.media_dictionary["file_extensions"]:
								file = self.media["episode"]["unit"] + "." + extension

								if self.File.Exist(file) == True:
									self.media["episode"]["unit"] = file

			# If it does not, then, ask if the user wants to move the file from somewhere to the correct folder
			if file_exists == False:
				print()
				print(self.media["episode"]["unit"] + "." + str(self.media_dictionary["file_extensions"]).replace("'", "").replace(", ", "/"))
				print()
				print(self.language_texts["the_media_file_does_not_exist"] + ".")
				print()

				question = self.language_texts["do_you_want_to_bring_it_from_another_folder"]

				bring_file = self.Input.Yes_Or_No(question, first_space = False)

				if bring_file == True:
					self.media["episode"]["unit"] = self.Find_Media_file(self.media["episode"]["Sanitized"])

				if bring_file == False:
					print()
					quit(self.language_texts["alright"] + ".")

	def File_Exists(self, file):
		file_exists = False

		# Check if an episode file with one of the accepted extensions exist
		for extension in self.media_dictionary["file_extensions"]:
			if "." + extension not in file:
				file += "." + extension

			if self.File.Exist(file) == True:
				file_exists = True

				self.media["episode"]["unit"] = file

		return file_exists

	def Show_Information(self):
		self.Show_Media_Information(self.media_dictionary)

	def Open_Episode_Unit(self):
		# Open media unit with its executor
		self.File.Open(self.media["episode"]["unit"])

	# Make Discord Custom Status for the media or media episode that is going to be watched and copy it
	def Create_Discord_Status(self):
		template = self.language_texts["watching, title()"]

		key = "with_title"

		if self.media["States"]["Media item list"] == True and self.media["item"]["title"] != self.media["title"] and self.media["States"]["video"] == False and self.media["States"]["single_unit"] == False:
			key = "with_title_and_item"

		self.media_dictionary["discord_status"] = template + " " + self.media_dictionary["media_type"]["singular"][self.user_language] + ": " + self.media["episode"][key][self.user_language]

		self.Text.Copy(self.media_dictionary["discord_status"])

	def Comment_On_Media(self):
		# Ask to comment on media (using Comment_Writer class)
		self.media_dictionary = self.Comment_Writer(self.media_dictionary).dictionary

	def Register_The_Media(self):
		template = self.language_texts["press_enter_when_you_finish_watching_{}"]

		# Text to show in the input when the user finishes watching the media (pressing Enter)
		text = template.format(self.media["texts"]["the_unit"][self.user_language])

		self.media["States"]["finished_watching"] = self.Input.Type(text)
		self.media["States"]["finished_watching"] = True

		# Register finished watching time
		self.media_dictionary["Entry"] = {
			"Time": self.Date.Now()
		}

		# Use the "Register" class to register the watched media, running it as a module, and giving the media_dictionary to it
		self.Register(dictionary = self.media_dictionary, run_as_module = True)

	def Find_Media_file(self, file_name):
		self.frequently_used_folders = [
			self.Folder.folders["user"]["downloads"]["root"],
			self.Folder.folders["user"]["downloads"]["videos"],
			self.Folder.folders["user"]["downloads"]["mega"]
		]

		old_file = self.Select_Folder_And_Media_File(self.frequently_used_folders)

		new_file = self.media["item"]["folders"]["media"]["root"] + self.Sanitize(file_name, restricted_characters = True) + "."

		if old_file.split(".")[1] not in self.media_dictionary["file_extensions"]:
			while old_file.split(".")[1] not in self.media_dictionary["file_extensions"]:
				print()
				print(self.language_texts["please_select_a_file_that_is_either_mp4_or_mkv"] + ".")

				old_file = self.Select_Folder_And_Media_File(self.frequently_used_folders)

				new_file = self.media["item"]["folders"]["media"]["root"] + file_name + "."

		self.moved_succesfully = False

		if old_file.split(".")[1] in self.media_dictionary["file_extensions"]:
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
		show_text = self.language_texts["folders, title()"]
		select_text = self.language_texts["select_one_folder_to_search_for_the_file"]

		location = self.Input.Select(folders, show_text = show_text, select_text = select_text)["option"]

		files = self.Folder.Contents(location, add_sub_folders = False)["file"]["list"]

		select_text = self.language_texts["select_the_media_file"]

		return self.Input.Select(files, select_text = select_text)["option"]

	def Move_Media_File(self, old_file, new_file):
		for extension in self.media_dictionary["file_extensions"]:
			if extension in old_file:
				extension = extension

		new_file = new_file + self.extension

		return self.File.Move(old_file, new_file)