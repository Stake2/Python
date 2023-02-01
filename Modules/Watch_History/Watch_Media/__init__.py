# Watch_Media.py

from Watch_History.Watch_History import Watch_History as Watch_History

from Watch_History.Register_Media import Register_Media as Register_Media
from Watch_History.Comment_Writer import Comment_Writer as Comment_Writer

import re
from copy import deepcopy

# A class to Watch media that has the "Watching" or "Re-Watching" Watching Status
class Watch_Media(Watch_History):
	def __init__(self, media_dictionary = {}, run_as_module = False, open_media = True):
		super().__init__()

		self.media_dictionary = media_dictionary
		self.run_as_module = run_as_module
		self.open_media = open_media

		self.Define_Media_Dictionary()
		self.Define_Episode_Variables()

		if self.media_dictionary["media"]["states"]["open_media"] == True:
			self.Define_Episode_Unit()
			self.Show_Information()
			self.Open_Episode_Unit()
			self.Create_Discord_Status()
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
					]
				}
			}

			# Define options
			self.media_dictionary = self.Define_Options(self.media_dictionary, options)

			# Ask user to select media type and media
			self.media_dictionary = self.Select_Media_Type_And_Media(options, watch = True)

			self.media_dictionary["media"]["states"]["open_media"] = self.open_media

		# Else, only define the options of the filled media dictionary
		if self.media_dictionary != {}:
			self.media_dictionary = self.Define_Options({}, self.media_dictionary)

		# Define dubbing
		if self.language_texts["dubbing, title()"] in self.media_dictionary["media"]["details"]:
			self.media_dictionary["media"]["states"]["has_dubbing"] = True

			found = False

			for details in [self.media_dictionary["media"]["details"], self.media_dictionary["media"]["item"]["details"]]:
				if self.language_texts["watch_dubbed"] in details:
					self.media_dictionary["media"]["states"]["watch_dubbed"] = self.Input.Define_Yes_Or_No(details[self.language_texts["watch_dubbed"]])

					found = True

			if found == False and self.media_dictionary["media"]["states"]["open_media"] == True:
				self.media_dictionary["media"]["states"]["watch_dubbed"] = self.Input.Yes_Or_No(self.language_texts["watch_the_dubbed_episode_in_your_language"])

		# Re-Read of media details file
		self.media_dictionary["media"]["details"] = self.File.Dictionary(self.media_dictionary["media"]["folders"]["details"])

		# Define remote origin for animes or videos media type
		if self.language_texts["remote_origin, title()"] not in self.media_dictionary["media"]["details"]:
			if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"]:
				remote_origin = "Animes Vision"

			if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["videos"]["en"]:
				remote_origin = "YouTube"

			self.media_dictionary["media"]["details"][self.language_texts["remote_origin, title()"]] = remote_origin

	def Define_Episode_Variables(self):
		# Definition of episode to watch if the media is not series media
		self.media_dictionary["media"]["episode"].update({
			"title": self.media_dictionary["media"]["titles"]["original"],
			"titles": deepcopy(self.media_dictionary["media"]["titles"]),
			"sanitized": self.Sanitize(self.media_dictionary["media"]["titles"]["original"], restricted_characters = True),
			"separator": self.media_dictionary["media"]["episode"]["separator"]
		})

		# Definition of episode to watch if the media is series media
		if self.media_dictionary["media"]["states"]["series_media"] == True:
			if self.language_texts["single_unit"] in self.media_dictionary["media"]["item"]["details"]:
				for language in self.small_languages:
					if language not in self.media_dictionary["media"]["episode"]["titles"]:
						self.media_dictionary["media"]["episode"]["titles"][language] = self.Get_Media_Title(self.media_dictionary, item = True)

					self.media_dictionary["media"]["item"]["episodes"]["titles"][language] = [self.media_dictionary["media"]["episode"]["titles"][language]]

			language_titles = self.media_dictionary["media"]["item"]["episodes"]["titles"][self.user_language]

			# If "Episode" key is not present in media item details, define it as the first episode
			if self.language_texts["episode, title()"] not in self.media_dictionary["media"]["item"]["details"] or self.media_dictionary["media"]["item"]["details"][self.language_texts["episode, title()"]] == "None":
				if language_titles != []:
					first_episode_title = language_titles[0]

				self.media_dictionary["media"]["item"]["details"][self.language_texts["episode, title()"]] = first_episode_title

				# Update media item details file
				self.File.Edit(self.media_dictionary["media"]["item"]["folders"]["details"], self.Text.From_Dictionary(self.media_dictionary["media"]["item"]["details"]), "w")

				# Update media item "Information.json" file
				self.JSON.Edit(self.media_dictionary["media"]["item"]["folders"]["information"], self.media_dictionary["media"]["item"])

			# Define media episode dictionary
			self.media_dictionary["media"]["episode"].update({
				"title": self.media_dictionary["media"]["item"]["details"][self.language_texts["episode, title()"]],
				"titles": {},
				"sanitized": self.Sanitize(self.media_dictionary["media"]["item"]["details"][self.language_texts["episode, title()"]], restricted_characters = True)
			})

			for alternative_episode_type in self.alternative_episode_types:
				if alternative_episode_type in self.media_dictionary["media"]["episode"]["title"]:
					self.media_dictionary["media"]["episode"]["separator"] = alternative_episode_type

			if self.language_texts["single_unit"] in self.media_dictionary["media"]["item"]["details"]:
				self.media_dictionary["media"]["episode"]["number"] = 1

			if self.language_texts["single_unit"] not in self.media_dictionary["media"]["item"]["details"]:
				# Get episode number
				i = 1
				for episode_title in language_titles:
					if self.media_dictionary["media"]["episode"]["separator"] in episode_title:
						episode_title = re.sub(self.media_dictionary["media"]["episode"]["separator"] + "[0-9]{1,3} ", "", episode_title)
						expression = episode_title in self.media_dictionary["media"]["episode"]["title"]

					else:
						expression = episode_title == self.media_dictionary["media"]["episode"]["title"]

					if expression:
						self.media_dictionary["media"]["episode"]["number"] = i

					i += 1

			# Define episode titles per language
			for language in self.small_languages:
				episode_titles = self.media_dictionary["media"]["item"]["episodes"]["titles"][language]

				episode_title = ""

				if episode_titles != []:
					episode_title = episode_titles[self.media_dictionary["media"]["episode"]["number"] - 1]

				self.media_dictionary["media"]["episode"]["titles"][language] = episode_title

			# Get YouTube ID for video series media
			if self.media_dictionary["media"]["states"]["video"] == True:
				file = self.media_dictionary["media"]["item"]["folders"]["youtube_ids"]
				ids = self.File.Contents(file)["lines"]

				self.media_dictionary["media"]["episode"]["youtube_id"] = ids[self.media_dictionary["media"]["episode"]["number"] - 1]

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

		# Remote or hybrid remote media origin, code, and link
		if self.media_dictionary["media"]["states"]["remote"] == True or self.language_texts["remote_origin, title()"] in self.media_dictionary["media"]["details"]:
			# Get remote origin title from media details
			if self.language_texts["remote_origin, title()"] in self.media_dictionary["media"]["details"]:
				self.media_dictionary["media"]["episode"]["remote"]["title"] = self.media_dictionary["media"]["details"][self.language_texts["remote_origin, title()"]]

			self.media_dictionary["media"]["episode"]["remote"]["link"] = self.remote_origins[self.media_dictionary["media"]["episode"]["remote"]["title"]]

			# Define origin code
			for item in ["code"]:
				text = self.language_texts["origin_location, title()"]

				self.media_dictionary["media"]["episode"]["remote"][item] = ""

				if text in self.media_dictionary["media"]["details"]:
					self.media_dictionary["media"]["episode"]["remote"][item] = self.media_dictionary["media"]["details"][text]

				if text in self.media_dictionary["media"]["item"]["details"]:
					self.media_dictionary["media"]["episode"]["remote"][item] = self.media_dictionary["media"]["item"]["details"][text]

			# Define link for video media
			if self.media_dictionary["media"]["states"]["video"] == True:
				if "v=" not in self.media_dictionary["media"]["episode"]["remote"]["code"]:
					self.media_dictionary["media"]["episode"]["remote"]["link"] += "watch?v=" + self.media_dictionary["media"]["episode"]["youtube_id"] + "&list=" + self.media_dictionary["media"]["episode"]["remote"]["code"] + "&index=" + str(self.media_dictionary["media"]["episode"]["number"])

				if "v=" in self.media_dictionary["media"]["episode"]["remote"]["code"]:
					self.media_dictionary["media"]["episode"]["remote"]["link"] += "watch?" + self.media_dictionary["media"]["episode"]["remote"]["code"]

			# If origin location is empty, and media type is "Animes", then define it as the lower case original media title with spaces replaced by dashes
			if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"] and self.media_dictionary["media"]["episode"]["remote"]["code"] == "":
				self.media_dictionary["media"]["episode"]["remote"]["code"] = self.media_dictionary["media"]["titles"]["sanitized"].lower()

				# Replace spaces by dashes
				self.media_dictionary["media"]["episode"]["remote"]["code"] = self.media_dictionary["media"]["episode"]["remote"]["code"].replace(" ", "-")

				# Remove restricted characters for Animes URL
				for item in ["!", ",", ".", "△"]:
					self.media_dictionary["media"]["episode"]["remote"]["code"] = self.media_dictionary["media"]["episode"]["remote"]["code"].replace(item, "")

				if self.media_dictionary["media"]["episode"]["remote"]["title"] == "Animes Vision":
					# Add code to link
					self.media_dictionary["media"]["episode"]["remote"]["link"] += self.media_dictionary["media_type"]["plural"]["pt"].lower() + "/" + self.media_dictionary["media"]["episode"]["remote"]["code"] + "/"

		# Media episode number text definition by episode title and episode separator
		if self.media_dictionary["media"]["states"]["series_media"] == True:
			media_episode = self.media_dictionary["media"]["episode"]["title"]

			if re.sub(self.texts["re_watched, type: regex, en - pt"], "", media_episode) != None:
				media_episode = re.sub(self.texts["re_watched, type: regex, en - pt"], "", media_episode)

			regex = {
				"one": r"[0-9][0-9]",
				"two": r"[0-9][0-9]\-[0-9][0-9]",
				"episode_and_parenthesis": r"[0-9][0-9]\([0-9][0-9]\)"
			}

			results = {}

			for key in regex:
				results[key] = re.findall(regex[key], media_episode)

			self.media_dictionary["media"]["episode"]["number_text"] = str(self.Text.Add_Leading_Zeros(self.media_dictionary["media"]["episode"]["number"]))

			number = ""

			if results["one"] != [] and str(results["one"][0]) != self.media_dictionary["media"]["episode"]["number_text"]:
				number = results["one"][0]

			if results["episode_and_parenthesis"] != []:
				number = results["episode_and_parenthesis"][0]

			if results["two"] != []:
				number = self.media_dictionary["media"]["episode"]["number_text"] + " (" + results["two"][0] + ")"

			if number == self.media_dictionary["media"]["episode"]["number_text"] or number == "":
				self.media_dictionary["media"]["episode"].pop("number_text")

			if "number_text" in self.media_dictionary["media"]["episode"] and number != self.media_dictionary["media"]["episode"]["number_text"]:
				self.media_dictionary["media"]["episode"]["number_text"] = number

		# Defining re_watched times and text
		if self.media_dictionary["media"]["states"]["re_watching"] == True:
			self.media_dictionary["media"]["episode"]["re_watched"] = {
				"times": 0,
				"text": "",
				"re_watched_text": {},
				"time_text": {}
			}

			if self.run_as_module == False:
				print()
				print(self.media_dictionary["media"]["titles"]["language"] + " " + self.media_dictionary["media"]["episode"]["title"])

				watched_times = int(self.Input.Type(self.language_texts["type_the_number_of_times_that_you_watched"], accept_enter = False))

			if self.run_as_module == True:
				watched_times = 1

			if watched_times != 0:
				if watched_times != 1:
					self.media_dictionary["media"]["episode"]["re_watched"]["times"] = watched_times + 1

				else:
					self.media_dictionary["media"]["episode"]["re_watched"]["times"] = watched_times

				self.media_dictionary["media"]["episode"]["re_watched"]["text"] = " (" + self.language_texts["re_watched, title()"] + " " + str(self.media_dictionary["media"]["episode"]["re_watched"]["times"]) + "x)"

				number = self.media_dictionary["media"]["episode"]["re_watched"]["times"]

				for language in self.small_languages:
					text = self.Text.By_Number(number, self.Language.texts["{}_time"][language], self.Language.texts["{}_times"][language])

					self.media_dictionary["media"]["episode"]["re_watched"]["time_text"][language] = text.format(self.Date.texts["number_names_feminine, type: list"][language][number])

					self.media_dictionary["media"]["episode"]["re_watched"]["re_watched_text"][language] = self.texts["re_watched, title()"][language] + " " + self.media_dictionary["media"]["episode"]["re_watched"]["time_text"][language]

			if watched_times == 0:
				self.media_dictionary["media"]["states"]["re_watching"] = False

		# Define media episode with item if media has media list
		if self.media_dictionary["media"]["states"]["series_media"] == True:
			self.media_dictionary["media"]["separators"] = {
				"title": " ",
				"episode": " "
			}

			for item in ["title", "episode"]:
				text = self.language_texts[item + "_separator"]

				if text in self.media_dictionary["media"]["details"]:
					self.media_dictionary["media"]["separators"][item] = self.media_dictionary["media"]["details"][text]

				elif self.media_dictionary["media"]["states"]["video"] == True:
					self.media_dictionary["media"]["separators"][item] = ": "

			media_title = self.Get_Media_Title(self.media_dictionary)

			self.media_dictionary["media"]["episode"].update({
				"with_title_default": "",
				"with_title": {}
			})

			# Define episode with item and episode with title and item keys
			if self.media_dictionary["media"]["states"]["media_list"] == True and self.media_dictionary["media"]["item"]["title"] != self.media_dictionary["media"]["title"] and self.language_texts["single_unit"] not in self.media_dictionary["media"]["item"]["details"]:
				self.media_dictionary["media"]["episode"].update({
					"with_item": {},
					"with_title_and_item": {}
				})

				# Define the episode with item as the media item + the episode separator and episode title
				self.media_dictionary["media"]["episode"]["with_item"]["original"] = self.media_dictionary["media"]["item"]["title"] + self.media_dictionary["media"]["separators"]["episode"] + self.media_dictionary["media"]["episode"]["title"]

				self.media_dictionary["media"]["episode"]["with_title_and_item"]["original"] = ""

				# Add original media title if it is not present in the item title
				if media_title not in self.media_dictionary["media"]["item"]["title"]:
					self.media_dictionary["media"]["episode"]["with_title_and_item"]["original"] += media_title

				# Add title separator
				self.media_dictionary["media"]["episode"]["with_title_and_item"]["original"] += self.media_dictionary["media"]["separators"]["title"]

				self.media_dictionary["media"]["episode"]["with_title_and_item"]["original"] += self.media_dictionary["media"]["item"]["title"]

				if media_title not in self.media_dictionary["media"]["item"]["title"]:
					# Add episode separator
					self.media_dictionary["media"]["episode"]["with_title_and_item"]["original"] += self.media_dictionary["media"]["separators"]["episode"]

				self.media_dictionary["media"]["episode"]["with_title_and_item"]["original"] += self.media_dictionary["media"]["episode"]["title"]

				# Define episode with item and episode with title and item texts per language
				for language in self.small_languages:
					# Define the media item title as the original one
					item_title = self.Get_Media_Title(self.media_dictionary, item = True)

					# Define the episode with item as the language media item + the episode separator and language episode title
					self.media_dictionary["media"]["episode"]["with_item"][language] = item_title + self.media_dictionary["media"]["separators"]["episode"] + self.media_dictionary["media"]["episode"]["titles"][language]

					# Define the episode with title and item as the language media item + the episode separator and language episode title
					self.media_dictionary["media"]["episode"]["with_title_and_item"][language] = media_title + self.media_dictionary["media"]["separators"]["title"] + item_title + self.media_dictionary["media"]["separators"]["episode"] + self.media_dictionary["media"]["episode"]["titles"][language]

				self.media_dictionary["media"]["episode"]["with_title_default"] = self.media_dictionary["media"]["episode"]["with_title_and_item"][self.user_language]

			# Define the episode with title as the media title + the episode separator and episode title
			self.media_dictionary["media"]["episode"]["with_title"]["original"] = media_title + self.media_dictionary["media"]["separators"]["title"] + self.media_dictionary["media"]["episode"]["title"]

			# Define the episode with title texts per language
			for language in self.small_languages:
				# Define media title as the original
				media_title = self.media_dictionary["media"]["titles"]["original"]

				# Define media title as the romanized one for Animes media
				if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"]:
					media_title = self.media_dictionary["media"]["titles"]["romanized"]

				# If a language media title exists, define it as the local media title
				if language in self.media_dictionary["media"]["titles"]:
					media_title = self.media_dictionary["media"]["titles"][language]
				print(self.media_dictionary["media"]["titles"])

				self.media_dictionary["media"]["episode"]["with_title"][language] = media_title + self.media_dictionary["media"]["separators"]["title"] + self.media_dictionary["media"]["episode"]["titles"][language]

			if self.media_dictionary["media"]["states"]["media_list"] == False or self.media_dictionary["media"]["item"]["title"] == self.media_dictionary["media"]["title"] or self.language_texts["single_unit"] in self.media_dictionary["media"]["item"]["details"]:
				self.media_dictionary["media"]["episode"]["with_title_default"] = self.media_dictionary["media"]["episode"]["with_title"][self.user_language]

		# Defining dubbed media text and it to the media episode if the media is "Animes", has dubbing, and is set to be watched dubbed
		if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"] and self.media_dictionary["media"]["states"]["watch_dubbed"] == True:
			self.media_dictionary["media"]["states"]["dubbed_to_title"] = False

			if self.language_texts["dubbed_to_title"] in self.media_dictionary["media"]["details"] and self.media_dictionary["media"]["details"][self.language_texts["dubbed_to_title"]] == self.Input.language_texts["yes, title()"]:
				self.media_dictionary["media"]["states"]["dubbed_to_title"] = True

			if self.language_texts["dubbed_to_title"] not in self.media_dictionary["media"]["details"]:
				self.media_dictionary["media"]["states"]["dubbed_to_title"] = True

			if self.media_dictionary["media"]["states"]["dubbed_to_title"] == True:
				self.media_dictionary["media"]["episode"]["dubbed_text"] = " " + self.language_texts["dubbed, title()"]

		# Define accepted file extensions
		self.media_dictionary["file_extensions"] = [
			"mp4",
			"mkv",
			"webm"
		]

		container = self.media_dictionary["media"]["texts"]["container"][self.user_language]

		if self.media_dictionary["media"]["states"]["video"] == False:
			container = container.lower()

		# Add "dubbed" text to media container text
		if "dubbed_text" in self.media_dictionary["media"]["episode"]:
			container = self.texts["dubbed_{}"][self.user_language].format(container)

		self.media_dictionary["media"]["texts"]["container_text"] = {
			"container": container,
			"this": self.media_dictionary["media"]["texts"]["genders"]["this"] + " " + container,
			"the": self.media_dictionary["media"]["texts"]["genders"]["the"] + " " + container,
			"of_the": self.media_dictionary["media"]["texts"]["genders"]["of_the"] + " " + container
		}

		# Define the header text to be used on the "Show_Media_Information" root method
		self.media_dictionary["header_text"] = self.language_texts["opening_{}_to_watch"].format(self.media_dictionary["media"]["texts"]["container_text"]["this"]) + ":"

		if self.media_dictionary["media"]["states"]["re_watching"] == True:
			self.media_dictionary["header_text"] = self.media_dictionary["header_text"].replace(self.language_texts["watch"], self.language_texts["re_watch"])

		dictionary = self.media_dictionary["media"].copy()
		dictionary.pop("select")
		dictionary.pop("list")

		if self.media_dictionary["media"]["states"]["media_list"] == False:
			dictionary.pop("item")

		# Write dictionary into media "Information.json" file
		self.JSON.Edit(self.media_dictionary["media"]["folders"]["information"], dictionary)

	def Define_Episode_Unit(self):
		# Remote media episode link definition
		if self.media_dictionary["media"]["states"]["remote"] == True or self.language_texts["remote_origin, title()"] in self.media_dictionary["media"]["details"]:
			# Media episode link definition for Animes Vision website
			if self.media_dictionary["media"]["episode"]["remote"]["title"] == "Animes Vision":
				# Add dubbed text
				if self.media_dictionary["media"]["states"]["has_dubbing"] == True and self.media_dictionary["media"]["states"]["watch_dubbed"] == True:
					self.media_dictionary["media"]["episode"]["remote"]["link"] = self.media_dictionary["media"]["episode"]["remote"]["link"].replace(self.media_dictionary["media"]["episode"]["remote"]["code"], self.media_dictionary["media"]["episode"]["remote"]["code"] + "-" + self.texts["dubbed"]["pt"].lower())

				# Add episode number
				self.media_dictionary["media"]["episode"]["remote"]["link"] += "episodio-" + str(self.Text.Add_Leading_Zeros(self.media_dictionary["media"]["episode"]["number"])) + "/"

				# Add dubbed text to media link if the media has a dub in the user language and user wants to watch it dubbed
				if self.media_dictionary["media"]["states"]["has_dubbing"] == True and self.media_dictionary["media"]["states"]["watch_dubbed"] == True:
					self.media_dictionary["media"]["episode"]["remote"]["link"] += self.texts["dubbed"]["pt"]

				# Add subbed text to media link if there is no dub for the media or the user wants to watch it subbed
				if self.media_dictionary["media"]["states"]["has_dubbing"] == False or self.media_dictionary["media"]["states"]["watch_dubbed"] == False:
					self.media_dictionary["media"]["episode"]["remote"]["link"] += self.texts["subbed"]["pt"]

			self.media_dictionary["media"]["episode"]["unit"] = self.media_dictionary["media"]["episode"]["remote"]["link"]

		# Local media episode file definition
		if self.media_dictionary["media"]["states"]["local"] == True:
			if self.media_dictionary["media"]["states"]["series_media"] == True and self.media_dictionary["media"]["states"]["video"] == False:
				# Add "Português" text to media item folder if media has dubbing and watch dubbed is true
				if self.media_dictionary["media"]["states"]["has_dubbing"] == True and self.media_dictionary["media"]["states"]["watch_dubbed"] == True:
					self.media_dictionary["media"]["item"]["folders"]["media"] += self.full_user_language + "/"

			self.Folder.Create(self.media_dictionary["media"]["item"]["folders"]["media"])

			# Add media episode to local media folder
			self.media_dictionary["media"]["episode"]["unit"] = "file:///" + self.media_dictionary["media"]["item"]["folders"]["media"] + self.media_dictionary["media"]["episode"]["sanitized"]

			file_exists = False

			# Check if an episode file with one of the accepted extensions exist
			for extension in self.media_dictionary["file_extensions"]:
				file = self.media_dictionary["media"]["episode"]["unit"].replace("file:///", "") + "." + extension

				if self.File.Exist(file) == True:
					self.media_dictionary["media"]["episode"]["unit"] = "file:///" + file

					file_exists = True

			# If it does not, then, ask if the user wants to move the file from somewhere to the correct folder
			if file_exists == False:
				print()
				print(self.media_dictionary["media"]["episode"]["unit"].replace("file:///", "") + "." + str(self.media_dictionary["file_extensions"]).replace("'", "").replace(", ", "/"))
				print()
				print(self.language_texts["the_media_file_does_not_exist"] + ".")
				print()

				question = self.language_texts["do_you_want_to_bring_it_from_another_folder"]

				bring_file = self.Input.Yes_Or_No(question, first_space = False)

				if bring_file == True:
					self.media_dictionary["media"]["episode"]["unit"] = "file:///" + self.Find_Media_file(self.media_dictionary["media"]["episode"]["sanitized"])

				if bring_file == False:
					print()
					quit(self.language_texts["alright"] + ".")

	def Show_Information(self):
		self.Show_Media_Information(self.media_dictionary)

	def Open_Episode_Unit(self):
		# Open media unit with its executor
		if self.media_dictionary["media"]["states"]["remote"] == True:
			self.File.Open(self.media_dictionary["media"]["episode"]["unit"])

		if self.media_dictionary["media"]["states"]["local"] == True and self.global_switches["testing"] == False:
			import subprocess
			subprocess.Popen('"' + self.root_folders["program_files_86"] + 'Mozilla Firefox/Firefox.exe" ' + '"' + self.media_dictionary["media"]["episode"]["unit"] + '"')

	# Make Discord Custom Status for the media or media episode that is going to be watched and copy it
	def Create_Discord_Status(self):
		template = self.language_texts["watching, title()"]

		key = "with_title"

		if self.media_dictionary["media"]["states"]["media_list"] == True and self.media_dictionary["media"]["item"]["title"] != self.media_dictionary["media"]["title"] and self.media_dictionary["media"]["states"]["video"] == False and self.language_texts["single_unit"] not in self.media_dictionary["media"]["item"]["details"]:
			key = "with_title_and_item"

		self.media_dictionary["discord_status"] = template + " " + self.media_dictionary["media_type"]["singular"][self.user_language] + ": " + self.media_dictionary["media"]["episode"][key][self.user_language]

		self.Text.Copy(self.media_dictionary["discord_status"])

	def Comment_On_Media(self):
		# Ask to comment on media (using Comment_Writer class)
		Comment_Writer(self.media_dictionary)

	def Register_Media(self):
		template = self.language_texts["press_enter_when_you_finish_watching_{}"]

		# Text to show in the input when the user finishes watching the media (pressing Enter)
		text = template.format(self.media_dictionary["media"]["texts"]["the_unit"][self.user_language])

		self.media_dictionary["media"]["states"]["finished_watching"] = self.Input.Type(text)
		self.media_dictionary["media"]["states"]["finished_watching"] = True

		# Register finished watching time
		self.media_dictionary["media"]["finished_watching"] = self.Date.Now()

		# Use the "Register_Media" class to register the watched media, running it as a module, and giving the media_dictionary to it
		Register_Media(run_as_module = True, media_dictionary = self.media_dictionary)

	def Find_Media_file(self, file_name):
		self.frequently_used_folders = [
			self.user_folders["downloads"]["root"],
			self.user_folders["downloads"]["videos"],
			self.user_folders["downloads"]["mega"],
		]

		old_file = self.Select_Folder_And_Media_File(self.frequently_used_folders)

		new_file = self.media_dictionary["media"]["item"]["folders"]["media"] + self.Sanitize(file_name, restricted_characters = True) + "."

		if old_file.split(".")[1] not in self.media_dictionary["file_extensions"]:
			while old_file.split(".")[1] not in self.media_dictionary["file_extensions"]:
				print()
				print(self.language_texts["please_select_a_file_that_is_either_mp4_or_mkv"] + ".")

				old_file = self.Select_Folder_And_Media_File(self.frequently_used_folders)

				new_file = self.media_dictionary["media"]["item"]["folders"]["media"] + file_name + "."

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