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

		if self.media_dictionary["Media"]["States"]["open_media"] == True:
			self.Define_Episode_Unit()
			self.Show_Information()
			self.Open_Episode_Unit()
			self.Create_Discord_Status()
			self.Comment_On_Media()
			self.Register_The_Media()

	def Define_Media_Dictionary(self):
		# Select media type and media if media dictionary is empty
		if self.media_dictionary == {}:
			options = {
				"media_type": {
					"status": [
						self.texts["watching, title()"]["en"],
						self.texts["re_watching, title()"]["en"],
					]
				}
			}

			# Define options
			self.media_dictionary = self.Define_Options(self.media_dictionary, options)

			# Ask user to select media type and media
			self.media_dictionary = self.Select_Media_Type_And_Media(options, watch = True)

		self.media_dictionary["Media"]["States"]["open_media"] = self.open_media

		# Define dubbing
		if self.language_texts["dubbing, title()"] in self.media_dictionary["Media"]["details"]:
			self.media_dictionary["Media"]["States"]["Has Dubbing"] = True

			if self.media_dictionary["media_type"]["plural"]["en"] not in [self.texts["movies"]["en"], self.texts["videos"]["en"]]:
				self.media_dictionary["Media"]["States"]["Watch dubbed"] = True

			found = False

			for details in [self.media_dictionary["Media"]["details"], self.media_dictionary["Media"]["item"]["details"]]:
				if self.language_texts["watch_dubbed"] in details:
					self.media_dictionary["Media"]["States"]["Watch dubbed"] = self.Input.Define_Yes_Or_No(details[self.language_texts["watch_dubbed"]])

					found = True

			if found == False and self.media_dictionary["Media"]["States"]["open_media"] == True:
				self.media_dictionary["Media"]["States"]["Watch dubbed"] = self.Input.Yes_Or_No(self.language_texts["watch_the_dubbed_episode_in_your_language"])

		if self.language_texts["origin_type"] not in self.media_dictionary["Media"]["details"]:
			self.media_dictionary["Media"]["States"]["remote"] = True

			self.media_dictionary["Media"]["details"][self.language_texts["origin_type"]] = self.language_texts["remote, title()"]

		# Define remote origin for animes or videos media type
		if self.language_texts["remote_origin, title()"] not in self.media_dictionary["Media"]["details"]:
			remote_origin = "None"

			if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"]:
				remote_origin = "Animes Vision"

			if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["videos"]["en"]:
				remote_origin = "YouTube"

			self.media_dictionary["Media"]["details"][self.language_texts["remote_origin, title()"]] = remote_origin

	def Define_Episode_Variables(self):
		from copy import deepcopy

		# Definition of episode to watch if the media is not series media
		self.media_dictionary["Media"]["episode"].update({
			"title": self.media_dictionary["Media"]["titles"]["original"],
			"titles": deepcopy(self.media_dictionary["Media"]["titles"]),
			"sanitized": self.Sanitize(self.media_dictionary["Media"]["titles"]["original"], restricted_characters = True),
			"separator": self.media_dictionary["Media"]["episode"]["separator"]
		})

		# Definition of episode to watch if the media is series media
		if self.media_dictionary["Media"]["States"]["series_media"] == True:
			if self.media_dictionary["Media"]["States"]["single_unit"] == True:
				for language in self.languages["small"]:
					if language not in self.media_dictionary["Media"]["episode"]["titles"]:
						self.media_dictionary["Media"]["episode"]["titles"][language] = self.Get_Media_Title(self.media_dictionary, item = True)

					self.media_dictionary["Media"]["item"]["episodes"]["titles"][language] = [self.media_dictionary["Media"]["episode"]["titles"][language]]

			language_titles = self.media_dictionary["Media"]["item"]["episodes"]["titles"][self.media_dictionary["Media"]["Language"]]

			# If "Episode" key is not present in media item details, define it as the first episode
			if self.language_texts["episode, title()"] not in self.media_dictionary["Media"]["item"]["details"] or self.media_dictionary["Media"]["item"]["details"][self.language_texts["episode, title()"]] == "None":
				if language_titles != []:
					first_episode_title = language_titles[0]

				self.media_dictionary["Media"]["item"]["details"][self.language_texts["episode, title()"]] = first_episode_title

				# Update media item details file
				self.File.Edit(self.media_dictionary["Media"]["item"]["folders"]["details"], self.Text.From_Dictionary(self.media_dictionary["Media"]["item"]["details"]), "w")

			# Define media episode dictionary
			self.media_dictionary["Media"]["episode"].update({
				"title": self.media_dictionary["Media"]["item"]["details"][self.language_texts["episode, title()"]],
				"titles": {},
				"sanitized": self.Sanitize(self.media_dictionary["Media"]["item"]["details"][self.language_texts["episode, title()"]], restricted_characters = True)
			})

			for alternative_episode_type in self.alternative_episode_types:
				if alternative_episode_type in self.media_dictionary["Media"]["episode"]["title"]:
					self.media_dictionary["Media"]["episode"]["separator"] = alternative_episode_type

			if self.media_dictionary["Media"]["States"]["single_unit"] == True:
				self.media_dictionary["Media"]["episode"]["number"] = 1

			if self.media_dictionary["Media"]["States"]["single_unit"] == False:
				# Get episode number
				i = 1
				for episode_title in language_titles:
					if self.media_dictionary["Media"]["episode"]["separator"] != "" and self.media_dictionary["Media"]["episode"]["separator"] in episode_title:
						episode_title = re.sub(self.media_dictionary["Media"]["episode"]["separator"] + "[0-9]{1,3} ", "", episode_title)
						expression = episode_title in self.media_dictionary["Media"]["episode"]["title"]

					if (
						self.media_dictionary["Media"]["episode"]["separator"] != "" and self.media_dictionary["Media"]["episode"]["separator"] not in episode_title or
						self.media_dictionary["Media"]["States"]["video"] == True or
						self.media_dictionary["Media"]["States"]["episodic"] == False
					):
						expression = episode_title == self.media_dictionary["Media"]["episode"]["title"]

					if expression:
						self.media_dictionary["Media"]["episode"]["number"] = i

					i += 1

			# Define episode titles per language
			for language in self.languages["small"]:
				episode_titles = self.media_dictionary["Media"]["item"]["episodes"]["titles"][language]

				episode_title = ""

				if episode_titles != []:
					episode_title = episode_titles[self.media_dictionary["Media"]["episode"]["number"] - 1]

				self.media_dictionary["Media"]["episode"]["titles"][language] = episode_title

			# Get YouTube ID for video series media
			if self.media_dictionary["Media"]["States"]["video"] == True:
				file = self.media_dictionary["Media"]["item"]["folders"]["titles"]["ids"]
				ids = self.File.Contents(file)["lines"]

				self.media_dictionary["Media"]["episode"]["id"] = ids[self.media_dictionary["Media"]["episode"]["number"] - 1]

		# Origin type variables definition for hybrid medias, getting origin type by the episode title
		if self.media_dictionary["Media"]["details"][self.language_texts["origin_type"]] == self.language_texts["hybrid, title()"]:
			self.media_dictionary["Media"]["States"]["hybrid"] = True

			# Local episode
			if self.language_texts["local, title()"] in self.media_dictionary["Media"]["episode"]["title"]:
				self.media_dictionary["Media"]["episode"]["title"] = self.media_dictionary["Media"]["episode"]["title"].split(", " + self.language_texts["local, title()"])[0]

				self.media_dictionary["Media"]["States"]["local"] = True

			# Remote episode
			if self.language_texts["remote, title()"] in self.media_dictionary["Media"]["episode"]["title"]:
				self.media_dictionary["Media"]["episode"]["title"] = self.media_dictionary["Media"]["episode"]["title"].split(", " + self.language_texts["remote, title()"])[0]

				self.media_dictionary["Media"]["States"]["remote"] = True

		# Remote or hybrid remote media origin, code, and link
		if self.media_dictionary["Media"]["States"]["remote"] == True or self.language_texts["remote_origin, title()"] in self.media_dictionary["Media"]["details"]:
			# Get remote origin title from media details
			if self.language_texts["remote_origin, title()"] in self.media_dictionary["Media"]["details"]:
				self.media_dictionary["Media"]["episode"]["remote"]["title"] = self.media_dictionary["Media"]["details"][self.language_texts["remote_origin, title()"]]

			self.media_dictionary["Media"]["episode"]["remote"]["link"] = self.remote_origins[self.media_dictionary["Media"]["episode"]["remote"]["title"]]

			# Define origin location
			for key in ["origin_location"]:
				text = self.language_texts[key + ", title()"]

				self.media_dictionary["Media"]["episode"]["remote"][key] = ""

				if text in self.media_dictionary["Media"]["details"]:
					self.media_dictionary["Media"]["episode"]["remote"][key] = self.media_dictionary["Media"]["details"][text]

				if text in self.media_dictionary["Media"]["item"]["details"]:
					self.media_dictionary["Media"]["episode"]["remote"][key] = self.media_dictionary["Media"]["item"]["details"][text]

			# Define link for video media
			if self.media_dictionary["Media"]["States"]["video"] == True or self.media_dictionary["Media"]["episode"]["remote"]["title"] == "YouTube":
				if "v=" not in self.media_dictionary["Media"]["episode"]["remote"]["origin_location"]:
					self.media_dictionary["Media"]["episode"]["remote"]["link"] += "watch?v=" + self.media_dictionary["Media"]["episode"]["id"] + "&list=" + self.media_dictionary["Media"]["episode"]["remote"]["origin_location"] + "&index=" + str(self.media_dictionary["Media"]["episode"]["number"])

				if "v=" in self.media_dictionary["Media"]["episode"]["remote"]["origin_location"]:
					self.media_dictionary["Media"]["episode"]["remote"]["link"] += "watch?" + self.media_dictionary["Media"]["episode"]["remote"]["origin_location"]

			# If origin location is empty, and media type is "Animes", then define it as the lower case original media title with spaces replaced by dashes
			if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"] and self.media_dictionary["Media"]["episode"]["remote"]["origin_location"] == "":
				self.media_dictionary["Media"]["episode"]["remote"]["origin_location"] = self.media_dictionary["Media"]["titles"]["sanitized"].lower()

				if self.media_dictionary["Media"]["States"]["Replace Title"] == True:
					self.media_dictionary["Media"]["episode"]["remote"]["origin_location"] = self.media_dictionary["Media"]["item"]["titles"]["sanitized"].lower()

				# Replace spaces by dashes
				self.media_dictionary["Media"]["episode"]["remote"]["origin_location"] = self.media_dictionary["Media"]["episode"]["remote"]["origin_location"].replace(" ", "-")

				# Remove restricted characters for Animes URL
				for item in ["!", ",", ".", "△"]:
					self.media_dictionary["Media"]["episode"]["remote"]["origin_location"] = self.media_dictionary["Media"]["episode"]["remote"]["origin_location"].replace(item, "")

				# Media episode link definition for Animes Vision website
				if self.media_dictionary["Media"]["episode"]["remote"]["title"] == "Animes Vision":
					# Add code to link
					self.media_dictionary["Media"]["episode"]["remote"]["link"] += self.media_dictionary["media_type"]["plural"]["pt"].lower() + "/" + self.media_dictionary["Media"]["episode"]["remote"]["origin_location"] + "/"

				# Add dubbed text
				if self.media_dictionary["Media"]["States"]["Has Dubbing"] == True and self.media_dictionary["Media"]["States"]["Watch dubbed"] == True:
					self.media_dictionary["Media"]["episode"]["remote"]["link"] = self.media_dictionary["Media"]["episode"]["remote"]["link"].replace(self.media_dictionary["Media"]["episode"]["remote"]["origin_location"], self.media_dictionary["Media"]["episode"]["remote"]["origin_location"] + "-" + self.texts["dubbed"]["pt"].lower())

				# Add episode number
				self.media_dictionary["Media"]["episode"]["remote"]["link"] += "episodio-" + str(self.Text.Add_Leading_Zeroes(self.media_dictionary["Media"]["episode"]["number"])) + "/"

				# Add dubbed text to media link if the media has a dub in the user language and user wants to watch it dubbed
				if self.media_dictionary["Media"]["States"]["Has Dubbing"] == True and self.media_dictionary["Media"]["States"]["Watch dubbed"] == True:
					self.media_dictionary["Media"]["episode"]["remote"]["link"] += self.texts["dubbed"]["pt"]

				# Add subbed text to media link if there is no dub for the media or the user wants to watch it subbed
				if self.media_dictionary["Media"]["States"]["Has Dubbing"] == False or self.media_dictionary["Media"]["States"]["Watch dubbed"] == False:
					self.media_dictionary["Media"]["episode"]["remote"]["link"] += self.texts["subbed"]["pt"]

			self.media_dictionary["Media"]["episode"]["unit"] = self.media_dictionary["Media"]["episode"]["remote"]["link"]

		# Media episode number text definition by episode title and episode separator
		if self.media_dictionary["Media"]["States"]["series_media"] == True:
			media_episode = self.media_dictionary["Media"]["episode"]["title"]

			regex = {
				"one": r"[0-9]{2,4}",
				"two": r"[0-9]{2,4}\-[0-9]{2,4}",
				"episode_and_parenthesis": r"[0-9]{2,4}\([0-9]{2,4}\)"
			}

			results = {}

			for key in regex:
				results[key] = re.findall(regex[key], media_episode)

			self.media_dictionary["Media"]["episode"]["number_text"] = str(self.Text.Add_Leading_Zeroes(self.media_dictionary["Media"]["episode"]["number"]))

			number = ""

			if results["one"] != [] and str(results["one"][0]) != self.media_dictionary["Media"]["episode"]["number_text"]:
				number = results["one"][0]

			if results["episode_and_parenthesis"] != []:
				number = results["episode_and_parenthesis"][0]

			if results["two"] != []:
				number = self.media_dictionary["Media"]["episode"]["number_text"] + " (" + results["two"][0] + ")"

			if (
				number == self.media_dictionary["Media"]["episode"]["number_text"] or 
				number == "" or
				self.media_dictionary["Media"]["States"]["episodic"] == False
			):
				self.media_dictionary["Media"]["episode"].pop("number_text")

			if "number_text" in self.media_dictionary["Media"]["episode"] and number != self.media_dictionary["Media"]["episode"]["number_text"]:
				self.media_dictionary["Media"]["episode"]["number_text"] = number

		# Defining re_watched times and text
		if self.media_dictionary["Media"]["States"]["Re-watching"] == True:
			self.media_dictionary["Media"]["episode"]["re_watched"] = {
				"times": 0,
				"text": "",
				"re_watched_text": {},
				"time_text": {}
			}

			if self.run_as_module == False:
				print()
				print(self.media_dictionary["Media"]["titles"]["language"] + " " + self.media_dictionary["Media"]["episode"]["title"])

				watched_times = ""

				while not isinstance(watched_times, int):
					watched_times = self.Input.Type(self.language_texts["type_the_number_of_times_that_you_watched"], accept_enter = False)

					try:
						watched_times = int(watched_times)
						break

					except ValueError:
						continue

			if self.run_as_module == True:
				watched_times = 1

			if watched_times != 0:
				if watched_times != 1:
					self.media_dictionary["Media"]["episode"]["re_watched"]["times"] = watched_times + 1

				else:
					self.media_dictionary["Media"]["episode"]["re_watched"]["times"] = watched_times

				self.media_dictionary["Media"]["episode"]["re_watched"]["text"] = " (" + self.language_texts["re_watched, capitalize()"] + " " + str(self.media_dictionary["Media"]["episode"]["re_watched"]["times"]) + "x)"

				number = self.media_dictionary["Media"]["episode"]["re_watched"]["times"]

				for language in self.languages["small"]:
					text = self.Text.By_Number(number, self.JSON.Language.texts["{}_time"][language], self.JSON.Language.texts["{}_times"][language])

					self.media_dictionary["Media"]["episode"]["re_watched"]["time_text"][language] = text.format(self.Date.texts["number_names_feminine, type: list"][language][number])

					self.media_dictionary["Media"]["episode"]["re_watched"]["re_watched_text"][language] = self.texts["re_watched, capitalize()"][language] + " " + self.media_dictionary["Media"]["episode"]["re_watched"]["time_text"][language]

			if watched_times == 0:
				self.media_dictionary["Media"]["States"]["Re-watching"] = False

		# Define media episode with item if media has media item list
		if self.media_dictionary["Media"]["States"]["series_media"] == True:
			self.media_dictionary["Media"]["separators"] = {
				"title": " ",
				"episode": " "
			}

			for item in ["title", "episode"]:
				text = self.language_texts[item + "_separator"]

				if text in self.media_dictionary["Media"]["details"]:
					self.media_dictionary["Media"]["separators"][item] = self.media_dictionary["Media"]["details"][text]

				elif self.media_dictionary["Media"]["States"]["video"] == True:
					self.media_dictionary["Media"]["separators"][item] = ": "

			media_title = self.Get_Media_Title(self.media_dictionary)

			# Replace media title with media item title if "replace title" setting exists inside media details
			if self.media_dictionary["Media"]["States"]["Replace Title"] == True:
				media_title = self.media_dictionary["Media"]["item"]["title"]

			self.media_dictionary["Media"]["episode"].update({
				"with_title_default": "",
				"with_title": {}
			})

			# Define episode with item and episode with title and item keys
			if self.media_dictionary["Media"]["States"]["Media item list"] == True and self.media_dictionary["Media"]["item"]["title"] != self.media_dictionary["Media"]["title"] and self.media_dictionary["Media"]["States"]["single_unit"] == False:
				self.media_dictionary["Media"]["episode"].update({
					"with_item": {},
					"with_title_and_item": {}
				})

				# Define the episode with item as the media item + the episode separator and episode title
				self.media_dictionary["Media"]["episode"]["with_item"]["original"] = self.media_dictionary["Media"]["item"]["title"] + self.media_dictionary["Media"]["separators"]["episode"] + self.media_dictionary["Media"]["episode"]["title"]

				self.media_dictionary["Media"]["episode"]["with_title_and_item"]["original"] = ""

				# Add original media title if it is not present in the item title
				if media_title not in self.media_dictionary["Media"]["item"]["title"]:
					self.media_dictionary["Media"]["episode"]["with_title_and_item"]["original"] += media_title + self.media_dictionary["Media"]["separators"]["title"]

				# Add media title separator and title
				self.media_dictionary["Media"]["episode"]["with_title_and_item"]["original"] += self.media_dictionary["Media"]["item"]["title"]

				# Add episode separator and title
				self.media_dictionary["Media"]["episode"]["with_title_and_item"]["original"] += self.media_dictionary["Media"]["separators"]["episode"] + self.media_dictionary["Media"]["episode"]["title"]

				# Define episode with item and episode with title and item texts per language
				for language in self.languages["small"]:
					# Define the media item title as the original one
					item_title = self.Get_Media_Title(self.media_dictionary, item = True)

					# Define the episode with item as the language media item + the episode separator and language episode title
					self.media_dictionary["Media"]["episode"]["with_item"][language] = item_title + self.media_dictionary["Media"]["separators"]["episode"] + self.media_dictionary["Media"]["episode"]["titles"][language]

					self.media_dictionary["Media"]["episode"]["with_title_and_item"][language] = media_title + self.media_dictionary["Media"]["separators"]["title"]

					if self.media_dictionary["Media"]["States"]["Replace Title"] == False:
						# Add item title to text if "replace title" is false
						self.media_dictionary["Media"]["episode"]["with_title_and_item"][language] += item_title + self.media_dictionary["Media"]["separators"]["episode"]

					self.media_dictionary["Media"]["episode"]["with_title_and_item"][language] += self.media_dictionary["Media"]["episode"]["titles"][language]

				self.media_dictionary["Media"]["episode"]["with_title_default"] = self.media_dictionary["Media"]["episode"]["with_title_and_item"][self.user_language]

			self.media_dictionary["Media"]["episode"]["with_title"]["original"] = media_title + self.media_dictionary["Media"]["separators"]["title"]

			# Add episode title
			self.media_dictionary["Media"]["episode"]["with_title"]["original"] += self.media_dictionary["Media"]["episode"]["title"]

			# Define the episode with title texts per language
			for language in self.languages["small"]:
				self.media_dictionary["Media"]["episode"]["with_title"][language] = media_title + self.media_dictionary["Media"]["separators"]["title"] + self.media_dictionary["Media"]["episode"]["titles"][language]

			if self.media_dictionary["Media"]["States"]["Media item list"] == False or self.media_dictionary["Media"]["item"]["title"] == self.media_dictionary["Media"]["title"] or self.media_dictionary["Media"]["States"]["single_unit"] == True:
				self.media_dictionary["Media"]["episode"]["with_title_default"] = self.media_dictionary["Media"]["episode"]["with_title"][self.user_language]

		# Defining dubbed media text and it to the media episode if the media is "Animes", has dubbing, and is set to be watched dubbed
		if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"] and self.media_dictionary["Media"]["States"]["Watch dubbed"] == True:
			self.media_dictionary["Media"]["States"]["dubbed_to_title"] = False

			if self.language_texts["dubbed_to_title"] in self.media_dictionary["Media"]["details"] and self.media_dictionary["Media"]["details"][self.language_texts["dubbed_to_title"]] == self.Input.language_texts["yes, title()"]:
				self.media_dictionary["Media"]["States"]["dubbed_to_title"] = True

			if self.language_texts["dubbed_to_title"] not in self.media_dictionary["Media"]["details"]:
				self.media_dictionary["Media"]["States"]["dubbed_to_title"] = True

			if self.media_dictionary["Media"]["States"]["dubbed_to_title"] == True:
				self.media_dictionary["Media"]["episode"]["dubbed_text"] = " " + self.language_texts["dubbed, title()"]

		# Define accepted file extensions
		self.media_dictionary["file_extensions"] = [
			"mp4",
			"mkv",
			"webm"
		]

		container = self.media_dictionary["Media"]["texts"]["container"][self.user_language]

		if self.media_dictionary["Media"]["States"]["video"] == False:
			container = container.lower()

		# Add "dubbed" text to media container text
		if "dubbed_text" in self.media_dictionary["Media"]["episode"]:
			container = self.texts["dubbed_{}"][self.user_language].format(container)

		self.media_dictionary["Media"]["texts"]["container_text"] = {
			"container": container,
			"this": self.media_dictionary["Media"]["texts"]["genders"][self.user_language]["this"] + " " + container,
			"the": self.media_dictionary["Media"]["texts"]["genders"][self.user_language]["the"] + " " + container,
			"of_the": self.media_dictionary["Media"]["texts"]["genders"][self.user_language]["of_the"] + " " + container
		}

		# Define the header text to be used on the "Show_Media_Information" root method
		self.media_dictionary["header_text"] = self.language_texts["opening_{}_to_watch"].format(self.media_dictionary["Media"]["texts"]["container_text"]["this"]) + ":"

		if self.media_dictionary["Media"]["States"]["Re-watching"] == True:
			self.media_dictionary["header_text"] = self.media_dictionary["header_text"].replace(self.language_texts["watch"], self.language_texts["re_watch"])

	def Define_Episode_Unit(self):
		# Local media episode file definition
		if self.media_dictionary["Media"]["States"]["local"] == True:
			if self.media_dictionary["Media"]["States"]["series_media"] == True and self.media_dictionary["Media"]["States"]["video"] == False:
				# Add "Português" text to media item folder if media has dubbing and watch dubbed is true
				if self.media_dictionary["Media"]["States"]["Has Dubbing"] == True and self.media_dictionary["Media"]["States"]["Watch dubbed"] == True:
					self.media_dictionary["Media"]["item"]["folders"]["media"]["root"] += self.full_user_language + "/"

			self.Folder.Create(self.media_dictionary["Media"]["item"]["folders"]["media"]["root"])

			# Add media episode to local media folder
			self.media_dictionary["Media"]["episode"]["unit"] = "file:///" + self.media_dictionary["Media"]["item"]["folders"]["media"]["root"] + self.media_dictionary["Media"]["episode"]["sanitized"]

			file_exists = False

			# Check if an episode file with one of the accepted extensions exist
			for extension in self.media_dictionary["file_extensions"]:
				file = self.media_dictionary["Media"]["episode"]["unit"].replace("file:///", "") + "." + extension

				if self.File.Exist(file) == True:
					self.media_dictionary["Media"]["episode"]["unit"] = "file:///" + file

					file_exists = True

			# If it does not, then, ask if the user wants to move the file from somewhere to the correct folder
			if file_exists == False:
				print()
				print(self.media_dictionary["Media"]["episode"]["unit"].replace("file:///", "") + "." + str(self.media_dictionary["file_extensions"]).replace("'", "").replace(", ", "/"))
				print()
				print(self.language_texts["the_media_file_does_not_exist"] + ".")
				print()

				question = self.language_texts["do_you_want_to_bring_it_from_another_folder"]

				bring_file = self.Input.Yes_Or_No(question, first_space = False)

				if bring_file == True:
					self.media_dictionary["Media"]["episode"]["unit"] = "file:///" + self.Find_Media_file(self.media_dictionary["Media"]["episode"]["sanitized"])

				if bring_file == False:
					print()
					quit(self.language_texts["alright"] + ".")

	def Show_Information(self):
		self.Show_Media_Information(self.media_dictionary)

	def Open_Episode_Unit(self):
		# Open media unit with its executor
		if self.media_dictionary["Media"]["States"]["remote"] == True:
			self.File.Open(self.media_dictionary["Media"]["episode"]["unit"])

		if self.media_dictionary["Media"]["States"]["local"] == True and self.switches["testing"] == False:
			import subprocess
			subprocess.Popen('"' + self.folders["root"]["program_files_86"] + 'Mozilla Firefox/Firefox.exe" ' + '"' + self.media_dictionary["Media"]["episode"]["unit"] + '"')

	# Make Discord Custom Status for the media or media episode that is going to be watched and copy it
	def Create_Discord_Status(self):
		template = self.language_texts["watching, title()"]

		key = "with_title"

		if self.media_dictionary["Media"]["States"]["Media item list"] == True and self.media_dictionary["Media"]["item"]["title"] != self.media_dictionary["Media"]["title"] and self.media_dictionary["Media"]["States"]["video"] == False and self.media_dictionary["Media"]["States"]["single_unit"] == False:
			key = "with_title_and_item"

		self.media_dictionary["discord_status"] = template + " " + self.media_dictionary["media_type"]["singular"][self.user_language] + ": " + self.media_dictionary["Media"]["episode"][key][self.user_language]

		self.Text.Copy(self.media_dictionary["discord_status"])

	def Comment_On_Media(self):
		# Ask to comment on media (using Comment_Writer class)
		self.media_dictionary = self.Comment_Writer(self.media_dictionary).media_dictionary

	def Register_The_Media(self):
		template = self.language_texts["press_enter_when_you_finish_watching_{}"]

		# Text to show in the input when the user finishes watching the media (pressing Enter)
		text = template.format(self.media_dictionary["Media"]["texts"]["the_unit"][self.user_language])

		self.media_dictionary["Media"]["States"]["finished_watching"] = self.Input.Type(text)
		self.media_dictionary["Media"]["States"]["finished_watching"] = True

		# Register finished watching time
		self.media_dictionary["Entry"] = {
			"Time": self.Date.Now()
		}

		# Use the "Register" class to register the watched media, running it as a module, and giving the media_dictionary to it
		self.Register(run_as_module = True, media_dictionary = self.media_dictionary)

	def Find_Media_file(self, file_name):
		self.frequently_used_folders = [
			self.Folder.folders["user"]["downloads"]["root"],
			self.Folder.folders["user"]["downloads"]["videos"],
			self.Folder.folders["user"]["downloads"]["mega"]
		]

		old_file = self.Select_Folder_And_Media_File(self.frequently_used_folders)

		new_file = self.media_dictionary["Media"]["item"]["folders"]["media"]["root"] + self.Sanitize(file_name, restricted_characters = True) + "."

		if old_file.split(".")[1] not in self.media_dictionary["file_extensions"]:
			while old_file.split(".")[1] not in self.media_dictionary["file_extensions"]:
				print()
				print(self.language_texts["please_select_a_file_that_is_either_mp4_or_mkv"] + ".")

				old_file = self.Select_Folder_And_Media_File(self.frequently_used_folders)

				new_file = self.media_dictionary["Media"]["item"]["folders"]["media"]["root"] + file_name + "."

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