# Watch_Media.py

from Watch_History.Watch_History import Watch_History as Watch_History

import re

# A class to Watch media that has the "Watching" or "Re-watching" Watching Status
class Watch_Media(Watch_History):
	def __init__(self, dictionary = {}, run_as_module = False, open_media = True):
		super().__init__()

		# Import sub-classes method
		self.Import_Sub_Classes()

		# Import the parameters to the class object
		self.dictionary = dictionary
		self.run_as_module = run_as_module
		self.open_media = open_media

		# Define the media dictionary
		self.Define_Media_Dictionary()

		# Define the episode variables and dictionary
		self.Define_Episode_Variables()

		# If the "Open media" state is True
		if self.media["States"]["Open media"] == True:
			# If the media is a local one (watching the media locally on the computer)
			if self.media["States"]["Local"] == True:
				# Define the media unit
				self.Define_Media_Unit()

			# Show information about the media that is going to be watched
			self.Show_Information()

			# If the "Defined title" key is not inside the root dictionary
			if "Defined title" not in self.dictionary:
				# Open the media unit for the user to watch
				self.Open_Media_Unit()

				# Create the Discord status text for the user to set on their Discord profile
				self.Create_Discord_Status()

				# Start watching the media
				self.Start_Watching_Media()

				# Ask if the user wants to comment on the media
				self.Comment_On_Media()

				# Register the watched media
				self.Register_Watched_Media()

	def Import_Sub_Classes(self):
		# Import the "importlib" module
		import importlib

		# Define the classes to be imported
		classes = [
			"Comment_Writer",
			"Register"
		]

		# Import them
		for title in classes:
			# Import the module
			module = importlib.import_module("." + title, self.__module__.split(".")[0])

			# Get the sub-class
			sub_class = getattr(module, title)

			# Add the sub-class to the current module
			setattr(self, title, sub_class)

	def Select_The_Media(self):
		# Define the list of watching statuses to use
		# With the "Watching" and "Re-watching" statuses
		watching_statuses = [
			self.texts["watching, title()"]["en"],
			self.texts["re_watching, title()"]["en"]
		]

		# Define the default root dictionary with the "Media type" dictionary containing the watching statuses
		# And also add the "Add status options" switch to the "Media" dictionary
		self.dictionary = {
			"Media type": {
				"Status": watching_statuses
			},
			"Media": {
				"Add status options": True
			}
		}

		# Ask the user to select a media type and media
		self.dictionary = self.Select_Media_Type_And_Media(options = self.dictionary, watch = True)

	def Define_Media_Dictionary(self):
		# Select the media type and the media if the dictionary is empty
		if self.dictionary == {}:
			# Ask the user to select the media to be watched
			self.Select_The_Media()

		# Define a shortcut for the media dictionary
		self.media = self.dictionary["Media"]

		# Define the open media variable inside the states dictionary of the media
		self.media["States"]["Open media"] = self.open_media

		# Define a shortcut for the media status
		media_watching_status = self.media["Details"][self.Language.language_texts["status, title()"]]

		# If the media watching status is equal to "Completed"
		if media_watching_status == self.Language.texts["completed, title()"][self.language["Small"]]:
			# Define the new status as "Re-watching"
			self.media["Status change"] = {
				"Old": media_watching_status,
				"New": self.language_texts["re_watching, title()"]
			}

			# Define the "Re-watching" state as "True"
			self.media["States"]["Re-watching"] = True

		# If the media is a series media (not a movie)
		# And the "Select episode" key is inside the root dictionary
		# And it is True
		if (
			self.media["States"]["Series media"] == True and
			"Select episode" in self.dictionary and
			self.dictionary["Select episode"] == True
		):
			# Get the episode titles
			titles = self.media["Item"]["Episodes"]["Titles"][self.language["Small"]]	

			# Ask the user to select an episode
			show_text = self.language_texts["episodes, title()"]
			select_text = self.language_texts["episode, title()"]

			episode = self.Input.Select(titles, show_text = show_text, select_text = select_text)["option"]

			# Define the episode in the media (item) details
			self.media["Item"]["Details"][self.language_texts["episode"].title()] = episode

			# Update the media (item) "Details.txt" file
			self.File.Edit(self.media["Item"]["Folders"]["details"], self.Text.From_Dictionary(self.media["Item"]["Details"]), "w")

		# Define the status list for the "Plan to watch" related statuses
		plan_to_watch_status_list = [
			self.texts["plan_to_watch, title()"][self.language["Small"]],
			self.Language.texts["on_hold, title()"][self.language["Small"]]
		]

		# If the media watching status is inside the "Plan to watch" status list
		# Or the media "Dates.txt" file is empty
		# Or the media has a media item list and the media item "Dates.txt" file is empty
		if (
			media_watching_status in plan_to_watch_status_list or
			self.File.Contents(self.media["Folders"]["dates"])["lines"] == [] or
			self.media["States"]["Has a list of media items"] == True and
			self.File.Contents(self.media["Item"]["Folders"]["dates"])["lines"] == []
		):
			# If the media "Dates.txt" file is empty
			# And the user is not re-watching the media
			if (
				self.File.Contents(self.media["Folders"]["dates"])["lines"] == [] and
				self.media["States"]["Re-watching"] == False
			):
				# Get the first watching time where the user started watching the media (now)
				self.media["Started watching time"] = self.Date.Now()["Formats"]["HH:MM DD/MM/YYYY"]

				# Create the "Dates" text to add that time and the time text
				self.media["Dates"] = self.language_texts["when_i_started_watching"] + ":\n"
				self.media["Dates"] += self.media["Started watching time"]

				# Update the "Dates.txt" file of the media
				self.File.Edit(self.media["Folders"]["dates"], self.media["Dates"], "w")

			# If the media has a media item list
			# And the media item "Dates.txt" file is empty
			# And the user is not re-watching the media
			if (
				self.media["States"]["Has a list of media items"] == True and
				self.File.Contents(self.media["Item"]["Folders"]["dates"])["lines"] == [] and
				self.media["States"]["Re-watching"] == False
			):
				# Get the first watching time where the user started watching the media item (now)
				self.media["Item"]["Started watching time"] = self.Date.Now()["Formats"]["HH:MM DD/MM/YYYY"]

				# Create the "Dates" text to add that time and the time text
				self.media["Item"]["Dates"] = self.language_texts["when_i_started_watching"] + ":\n"
				self.media["Item"]["Dates"] += self.media["Item"]["Started watching time"]

				# Update the "Dates.txt" file of the media item
				self.File.Edit(self.media["Item"]["Folders"]["dates"], self.media["Item"]["Dates"], "w")

			# If the media watching status is inside the "Plan to watch" status list
			if media_watching_status in plan_to_watch_status_list:
				# Define the new status as "Watching"
				self.media["Status change"] = {
					"Old": media_watching_status,
					"New": self.language_texts["watching, title()"]
				}

		# If there is a new watching status inside the media dictionary, change the current watching status to it
		if "Status change" in self.media:
			self.media["Details"] = self.Change_Status(self.dictionary, self.media["Status change"]["New"])

		# If the "Dubbing" key is inside the media details dictionary
		if self.Language.language_texts["dubbing, title()"] in self.media["Details"]:
			# Define the "Has dubbing" media state as True
			self.media["States"]["Dubbing"]["Has dubbing"] = True

			# Define the "Found watch dubbed setting" switch as False
			self.found_watch_dubbed_setting = False

			# Define the list of detail dictionaries
			details_list = [
				self.media["Details"],
				self.media["Item"]["Details"]
			]

			# Iterate through the list
			for details in details_list:
				# If the "Watch dubbed" key is inside the current details dictionary
				if self.language_texts["watch_dubbed"] in details:
					# Define the "Watch dubbed" media state as the detail value
					self.media["States"]["Dubbing"]["Watch dubbed"] = self.Input.Define_Yes_Or_No(details[self.language_texts["watch_dubbed"]])

					# Switch the "Found watch dubbed setting" switch to True
					self.found_watch_dubbed_setting = True

		# If the "Origin type" key is not inside the media details dictionary
		if self.Language.language_texts["origin_type"] not in self.media["Details"]:
			# Define the "Remote" media state as True
			self.media["States"]["Remote"] = True

			# Define the "Origin type" key inside the media details as the remote one
			self.media["Details"][self.Language.language_texts["origin_type"]] = self.Language.language_texts["remote, title()"]

		# If the "Remote origin" key is not inside the media details dictionary
		if self.Language.language_texts["remote_origin"] not in self.media["Details"]:
			# Define a local "remote origin" variable as None
			remote_origin = "None"

			# If the media type is "Animes"
			if self.dictionary["Media type"]["Plural"]["en"] == self.texts["animes, title()"]["en"]:
				# Define the local remote origin as "Animes Vision"
				remote_origin = "Animes Vision"

			# If the media type is "Videos"
			if self.dictionary["Media type"]["Plural"]["en"] == self.texts["videos, title()"]["en"]:
				# Define the local remote origin as "YouTube"
				remote_origin = "YouTube"

			# If the local remote origin is not None
			if remote_origin != "None":
				# Define the "Remote origin" key inside the media details as the local remote origin
				self.media["Details"][self.Language.language_texts["remote_origin"]] = remote_origin

	def Define_Episode_Variables(self):
		# Import the "deepcopy" module from the "copy" module
		from copy import deepcopy

		# The original media "Episode" dictionary is this one:
		# Defined by the root method "Select_Media"
		"""
		self.media["Episode"] = {
			"Title": "",
			"Titles": {},
			"Sanitized": "",
			"Number": 1,
			"Number text": "1",
			"Separator": ""
		}
		"""

		# Update the media "Episode" dictionary to update the "Title", "Titles", and "Sanitized" keys
		# Defining those keys as the root media keys
		self.media["Episode"].update({
			"Title": self.media["Titles"]["Original"],
			"Titles": deepcopy(self.media["Titles"]),
			"Sanitized": self.Sanitize_Title(self.media["Titles"]["Original"], remove_dot = False),
		})

		# If the media is a series media (with media items or seasons)
		if self.media["States"]["Series media"] == True:
			# If the media item is a single unit one
			if self.media["States"]["Single unit"] == True:
				# Iterate through the list of small languages
				for language in self.languages["small"]:
					# If the language is not inside the media episode titles dictionary
					# Or the media is inside the root media titles dictionary
					# And the media episode title is the same as the media title
					if (
						language not in self.media["Episode"]["Titles"] or
						language in self.media["Titles"] and
						self.media["Episode"]["Titles"][language] == self.media["Titles"][language]
					):
						# Get the title for the media item in the current language
						# Thus defining the episode title for that language as the media item title
						self.media["Episode"]["Titles"][language] = self.Get_Media_Title(self.dictionary, language = language, item = True)

					# Define the list of episode titles for the media item in the current language as a list with only the language episode title
					self.media["Item"]["Episodes"]["Titles"][language] = [
						self.media["Episode"]["Titles"][language]
					]

			# Create a local "language titles list" dictionary
			language_titles = {}

			# Iterate through the list of small languages
			for language in self.languages["small"]:
				# Add the language list of titles to the local language titles dictionary
				language_titles[language] = self.media["Item"]["Episodes"]["Titles"][language]

			# If the media language key does not exist inside the episode titles dictionary
			if self.media["Language"] not in self.media["Item"]["Episodes"]["Titles"]:
				# Change the media language to the user language
				self.media["Language"] = self.language["Small"]

			# Define the after key used to find the "Episode" key, to define the current episode to watch (episode number and title)
			# Be it "Episodes", "End date", or "Start date"
			after_key = self.language_texts["episodes, title()"]

			if after_key not in self.media["Item"]["Details"]:
				after_key = self.Date.language_texts["end_date"]

			if after_key not in self.media["Item"]["Details"]:
				after_key = self.Date.language_texts["start_date"]

			# Define the default episode variable as an empty string
			episode = ""

			# If the "Episode" key is present inside the media item details
			if self.Language.language_texts["episode, title()"] in self.media["Item"]["Details"]:
				# Define it as the current episode to watch
				episode = self.media["Item"]["Details"][self.Language.language_texts["episode, title()"]]

			# If the "Episode" key is not present inside media item details
			# Or the key is present and its value is "None"
			if (
				self.Language.language_texts["episode, title()"] not in self.media["Item"]["Details"] or
				self.media["Item"]["Details"][self.Language.language_texts["episode, title()"]] == "None"
			):
				# Define the first episode title as an empty string
				first_episode_title = ""

				# If the list of media language titles is not empty
				if language_titles[self.media["Language"]] != []:
					# Define the first episode title as the first one on the media language list
					first_episode_title = language_titles[self.media["Language"]][0]

				# Define the local episode variable as the first episode
				episode = first_episode_title

				# Add the episode key after the "Episodes" key or update it
				key_value = {
					"key": self.Language.language_texts["episode, title()"],
					"value": episode
				}

				# If the media item is not a single unit (that means it has episodes)
				if self.media["States"]["Single unit"] == False:
					# Add the "Episode" key after the defined "after key"
					self.media["Item"]["Details"] = self.JSON.Add_Key_After_Key(self.media["Item"]["Details"], key_value, after_key)

					# Update the media item "Details.txt" file
					self.File.Edit(self.media["Item"]["Folders"]["details"], self.Text.From_Dictionary(self.media["Item"]["Details"]), "w")

			# Update the media "Episode" dictionary to add the normal and sanitized episode title
			self.media["Episode"].update({
				"Title": episode,
				"Titles": {},
				"Sanitized": self.Sanitize_Title(episode, remove_dot = False)
			})

			# If the "Defined title" key is inside the root dictionary
			if "Defined title" in self.dictionary:
				# Update the normal and sanitized episode titles to be the defined title
				self.media["Episode"]["Title"] = self.dictionary["Defined title"]
				self.media["Episode"]["Sanitized"] = self.Sanitize_Title(self.media["Episode"]["Title"], remove_dot = False)

			# Iterate through the list of alternative episode types
			# alternative_episode_types = ["OVA", "ONA", "Special", "Especial", "Shorts", "Curtas"]
			for alternative_episode_type in self.alternative_episode_types:
				# If the episode type is inside the media episode title
				if alternative_episode_type in self.media["Episode"]["Title"]:
					# Define the episode separator as the current episode type
					self.media["Episode"]["Separator"] = alternative_episode_type

			# If the media item is a single unit
			if self.media["States"]["Single unit"] == True:
				# Define the episode number as one
				self.media["Episode"]["Number"] = 1

			# If the media item is not a single unit (that means it has episodes)
			if self.media["States"]["Single unit"] == False:
				# Iterate through the episode titles inside the media language list of episode titles
				# To find the current episode number
				i = 1
				for episode_title in language_titles[self.media["Language"]]:
					# If the separator is not an empty string and is present in the current episode title
					if (
						self.media["Episode"]["Separator"] != "" and
						self.media["Episode"]["Separator"] in episode_title
					):
						# Define the language title as the root episode title
						language_title = self.media["Episode"]["Title"]

						# Remove the separator and episode number from the episode title
						episode_title = re.sub(self.media["Episode"]["Separator"] + "[0-9]{1,3} ", "", episode_title)

						# Define the expression as "current episode title is inside the media episode title" (not an exact match)
						# We remove the episode number from the current episode title to be easier to match it with the correct episode title (the one inside the "Episode" dictionary)
						expression = episode_title in language_title

					# If the separator is not an empty string and is not present in the current episode title
					# Or the media type is "Videos", and the media is a video channel
					# (Video media is not episodic, that means they do not follow a specific order, so exact match is used)
					# Or the media is non-episodic (exact match is also used for non-episodic media)
					# Or the separator is empty
					elif (
						self.media["Episode"]["Separator"] != "" and
						self.media["Episode"]["Separator"] not in episode_title or
						self.media["States"]["Video"] == True or
						self.media["States"]["Episodic"] == False or 
						self.media["Episode"]["Separator"] == ""
					):
						# Define the language title as the root episode title
						language_title = self.media["Episode"]["Title"]

						# Define the expression as "current episode title is equal to the language episode title" (an exact match)
						# For example, the current "episode title" is (EP12 "The Big Flowers")
						# This expression checks if the current episode title is equal to the current language title (the one inside the "i" line number inside the list of language episode titles)
						expression = episode_title == language_title

					# If the defined expression is True, define the episode number as the current "i" number
					if expression == True:
						self.media["Episode"]["Number"] = i

					# Add one to the "i" number
					i += 1

				# Iterate through the list of small languages
				for language in self.languages["small"]:
					# Get the list of episode titles in the current language
					episode_titles = self.media["Item"]["Episodes"]["Titles"][language]

					# Define the local episode title as an empty string
					episode_title = ""

					# If the list of episode titles is not empty
					if episode_titles != []:
						# Define the line number to use to find the episode title
						line_number = self.media["Episode"]["Number"] - 1

						# Get the language episode title using the defined line number
						# (Less one because lists in Python starts in zero, and the episode number starts in one)
						episode_title = episode_titles[line_number]

					# Define the episode title in the current language as the local episode title, inside the "Titles" key
					self.media["Episode"]["Titles"][language] = episode_title

			# For the video media type, when the media is a video channel
			# Get the episode ID from the "IDs.txt" file using the episode number
			if self.media["States"]["Video"] == True:
				self.media["Episode"]["ID"] = self.media["Item"]["Episodes"]["Titles"]["IDs"][self.media["Episode"]["Number"] - 1]

		# If the media is not a series media (without media items or seasons)
		# That means it is a movie
		if self.media["States"]["Series media"] == False:
			# Sanitize the media title to get the sanitized title
			self.media["Episode"]["Sanitized"] = self.Sanitize_Title(self.media["Titles"][self.media["Language"]], remove_dot = False)

			# Update the sanitized title to be the previous title but with the year of the movie added with parenthesis
			self.media["Episode"]["Sanitized"] = self.media["Episode"]["Sanitized"] + " (" + self.media["Titles"]["Original"].split("(")[1]

		# If the media is a remote one
		# Or the "Remote origin" key is present inside the media details dictionary
		if (
			self.media["States"]["Remote"] == True or
			self.Language.language_texts["remote_origin"] in self.media["Details"]
		):
			# If the "Remote origin" key is present
			if self.Language.language_texts["remote_origin"] in self.media["Details"]:
				# Get the remote origin title from the key
				self.media["Episode"]["Remote"]["Title"] = self.media["Details"][self.Language.language_texts["remote_origin"]]

			# Make a shortcut for the remote title
			remote_title = self.media["Episode"]["Remote"]["Title"]

			# Get the remote origin dictionary
			remote_origin = self.remote_origins[remote_title]

			# Define the remote link as the link inside the "remote origin" dictionary
			# Links = {"Animes Vision": "https://animes.vision/", "YouTube": "https://www.youtube.com/"}
			self.media["Episode"]["Remote"]["Link"] = remote_origin["Link"]

			# Define a local key as "origin_location"
			key = "origin_location"

			# Get the text for the "Origin location" key
			text = self.Language.language_texts[key]

			# Define the origin location key as an empty string
			self.media["Episode"]["Remote"][key] = ""

			# If the text is inside the media details dictionary
			if text in self.media["Details"]:
				# Define the origin location key as the value inside that dictionary
				self.media["Episode"]["Remote"][key] = self.media["Details"][text]

			# If the text is inside the media item details dictionary
			if text in self.media["Item"]["Details"]:
				# Define the origin location key as the value inside that dictionary
				self.media["Episode"]["Remote"][key] = self.media["Item"]["Details"][text]

			# Define the remote origin link for the "Animes Vision" remote origin
			if self.media["Episode"]["Remote"]["Title"] == "Animes Vision":
				# If the origin location is empty
				if self.media["Episode"]["Remote"]["origin_location"] == "":
					# Define the origin location as the lowercase version of the sanitized media title
					# For example:
					# title of the anime
					self.media["Episode"]["Remote"]["origin_location"] = self.media["Titles"]["Sanitized"].lower()

					# If the "Replace title" is True
					if self.media["States"]["Replace title"] == True:
						# Replace the media title with the media item title, but the sanitized version
						# For example:
						# title of the anime season
						self.media["Episode"]["Remote"]["origin_location"] = self.media["Item"]["Titles"]["Sanitized"].lower()

					# Replace spaces by dashes on the origin location
					# For example:
					# title-of-the-anime
					self.media["Episode"]["Remote"]["origin_location"] = self.media["Episode"]["Remote"]["origin_location"].replace(" ", "-")

					# Remove restricted characters from the origin location
					for text in ["!", ",", ".", "△"]:
						self.media["Episode"]["Remote"]["origin_location"] = self.media["Episode"]["Remote"]["origin_location"].replace(text, "")

				# Add the media type code to the remote origin link
				# For example:
				# https://animes.vision/animes/title-of-the-anime/
				# The media type code is "animes"
				self.media["Episode"]["Remote"]["Link"] += self.dictionary["Media type"]["Plural"][self.language["Small"]].lower() + "/" + self.media["Episode"]["Remote"]["origin_location"] + "/"

				# Add the "Dubbed" text to the episode link
				# If the "Has dubbing" and "Watch dubbed" media states are True
				# (That means the user wants to watch the media dubbed)
				if (
					self.media["States"]["Dubbing"]["Has dubbing"] == True and
					self.media["States"]["Dubbing"]["Watch dubbed"] == True
				):
					# Define a shortcut for the origin location
					origin_location = self.media["Episode"]["Remote"]["origin_location"]

					# Add the "dubbed" text to the origin location 
					# For example:
					# title-of-the-anime-dubbed ("-dubbed" is added)
					dubbed_origin_location = self.media["Episode"]["Remote"]["origin_location"] + "-" + self.Language.texts["dubbed, title()"][self.language["Small"]].lower()

					# Replace the original origin location with the dubbed version of it
					# For example:
					# "title-of-the-anime" becomes "title-of-the-anime-dubbed"
					self.media["Episode"]["Remote"]["Link"] = self.media["Episode"]["Remote"]["Link"].replace(origin_location, dubbed_origin_location)

				# Add the episode number to the remote origin link
				# With the "episodio" code ("episodio" means "episode")
				# For example:
				# https://animes.vision/animes/title-of-the-anime/episodio-12/
				self.media["Episode"]["Remote"]["Link"] += "episodio-" + str(self.Text.Add_Leading_Zeroes(self.media["Episode"]["Number"])) + "/"

				# Add the "Dubbed" text in the user language to the remote origin link
				# If the "Has dubbing" and "Watch dubbed" media states are True
				# (That means the user wants to watch the media dubbed)
				if (
					self.media["States"]["Dubbing"]["Has dubbing"] == True and
					self.media["States"]["Dubbing"]["Watch dubbed"] == True
				):
					# For example:
					# https://animes.vision/animes/title-of-the-anime/episodio-12/dublado
					# "dublado" means "dubbed"
					self.media["Episode"]["Remote"]["Link"] += self.Language.texts["dubbed, title()"][self.language["Small"]].lower()

				# Add the "Subbed" text in the user language to the remote origin link
				# If the "Has dubbing" or "Watch dubbed" media states are False
				# (That means the user does not want to watch the media dubbed)
				if (
					self.media["States"]["Dubbing"]["Has dubbing"] == False or
					self.media["States"]["Dubbing"]["Watch dubbed"] == False
				):
					# For example:
					# https://animes.vision/animes/title-of-the-anime/episodio-12/legendado
					# "legendado" means "subbed"
					self.media["Episode"]["Remote"]["Link"] += self.Language.texts["subbed, title()"][self.language["Small"]].lower()

			# Define the remote origin link for the "YouTube" remote origin
			if self.media["Episode"]["Remote"]["Title"] == "YouTube":
				# Define a local link as the "Video" link template
				link = remote_origin["Link templates"]["Video"]

				# If the media has a media item list (seasons or video series)
				if self.media["States"]["Has a list of media items"] == True:
					# Update the link to the "Video and playlist" link template
					link = remote_origin["Link templates"]["Video and playlist"]

				# Add the video ID
				link = link.replace("{Video}", self.media["Episode"]["ID"])

				# If the media has a media item list (seasons or video series)
				if self.media["States"]["Has a list of media items"] == True:
					# Add the playlist ID
					link = link.replace("{Playlist}", self.media["Episode"]["Remote"]["origin_location"])

				# If the media has a media item list (seasons or video series)
				# And the media is an episodic one
				# (Video channels can be episodic if the "Episodic" key is present inside the media (item) details)
				if (
					self.media["States"]["Has a list of media items"] == True and
					self.media["States"]["Episodic"] == True
				):
					# Add the "index" (playlist video number) parameter and the episode number plus one
					# This is to tell the index of the video inside the playlist to YouTube
					link += "&index=" + str(self.media["Episode"]["Number"] + 1)

				# Define the remote link as the local link
				self.media["Episode"]["Remote"]["Link"] = link

			# Define the media episode unit as the remote origin link
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

		# Define the media title and episode separators
		if self.media["States"]["Series media"] == True:
			self.media["Separators"] = {
				"Title": " ",
				"Episode": " "
			}

			for item_type in ["Title", "Episode"]:
				text = self.Language.language_texts[item_type.lower() + "_separator"]

				if text in self.media["Details"]:
					self.media["Separators"][item_type] = self.media["Details"][text]

				elif self.media["States"]["Video"] == True:
					self.media["Separators"][item_type] = ": "

				# If the item is the title and the ": " is inside the item title
				# Or the item is the episode and the "S[Any number two times]" is found on the item title
				if (
					item_type == "Title" and
					self.media["Item"]["Title"][0] + self.media["Item"]["Title"][1] == ": " or
					item_type == "Episode" and
					re.findall(r"S[0-9]{2}", self.media["Item"]["Title"]) != [] and
					"Language" not in self.media["Item"]["Titles"]
				):
					# Define the item or episode separator is as an empty string
					self.media["Separators"][item_type] = ""

		# Define the media episode with the media item if the media has a media item list
		if self.media["States"]["Series media"] == True:
			# Get the correct media title
			media_title = self.Get_Media_Title(self.dictionary)

			self.media["Episode"].update({
				"with_title_default": "",
				"with_title": {}
			})

			# Define episode with item and episode with title and item keys
			if (
				self.media["States"]["Has a list of media items"] == True and
				self.media["Item"]["Title"] != self.media["Title"] and
				self.media["States"]["Single unit"] == False
			):
				self.media["Episode"].update({
					"with_item": {},
					"with_title_and_item": {}
				})

				# Get the correct media item title in the current language
				item_title = self.Get_Media_Title(self.dictionary, language = language, item = True)

				# Define the episode with item as the media item + the episode separator and episode title
				self.media["Episode"]["with_item"]["Original"] = item_title + self.media["Separators"]["Episode"] + self.media["Episode"]["Title"]

				self.media["Episode"]["with_title_and_item"]["Original"] = ""

				# Add the original media title if it is not present in the item title
				if media_title not in item_title:
					self.media["Episode"]["with_title_and_item"]["Original"] += media_title + self.media["Separators"]["Title"]

				# Add media title separator and title
				self.media["Episode"]["with_title_and_item"]["Original"] += item_title

				# Add episode separator and title
				self.media["Episode"]["with_title_and_item"]["Original"] += self.media["Separators"]["Episode"] + self.media["Episode"]["Title"]

				# Define episode with item and episode with title and item texts by language
				for language in self.languages["small"]:
					# Get the media title in the current language
					media_title = self.Get_Media_Title(self.dictionary, language = language)

					# Get the correct media item title in the current language
					item_title = self.Get_Media_Title(self.dictionary, language = language, item = True)

					# Define the episode with item as the language media item + the episode separator and language episode title
					self.media["Episode"]["with_item"][language] = item_title + self.media["Separators"]["Episode"] + self.media["Episode"]["Titles"][language]

					self.media["Episode"]["with_title_and_item"][language] = media_title + self.media["Separators"]["Title"]

					if self.media["States"]["Replace title"] == False:
						# Add item title to text if "replace title" is False
						self.media["Episode"]["with_title_and_item"][language] += item_title + self.media["Separators"]["Episode"]

					if self.media["States"]["Replace title"] == True:
						self.media["Episode"]["with_title_and_item"][language] = item_title + self.media["Separators"]["Episode"]

					self.media["Episode"]["with_title_and_item"][language] += self.media["Episode"]["Titles"][language]

				self.media["Episode"]["with_title_default"] = self.media["Episode"]["with_title_and_item"][self.language["Small"]]

			# Get the correct media title
			media_title = self.Get_Media_Title(self.dictionary)

			# Replace media title with media item title if "replace title" setting exists inside media details
			if self.media["States"]["Replace title"] == True:
				if language in self.media["Item"]["Titles"]:
					media_title = self.media["Item"]["Titles"][language]

				else:
					media_title = self.media["Item"]["Titles"]["Original"]

					if "Romanized" in self.media["Item"]["Titles"]:
						media_title = self.media["Item"]["Titles"]["Romanized"]

			self.media["Episode"]["with_title"]["Original"] = media_title + self.media["Separators"]["Title"] + self.media["Episode"]["Title"]

			# Define the episode with title texts by language
			for language in self.languages["small"]:
				media_title = self.Get_Media_Title(self.dictionary, language = language)

				# Replace media title with media item title if "replace title" setting exists inside media details
				if self.media["States"]["Replace title"] == True:
					if language in self.media["Item"]["Titles"]:
						media_title = self.media["Item"]["Titles"][language]

					else:
						media_title = self.media["Item"]["Titles"]["Original"]

						if "Romanized" in self.media["Item"]["Titles"]:
							media_title = self.media["Item"]["Titles"]["Romanized"]

				self.media["Episode"]["with_title"][language] = media_title + self.media["Separators"]["Title"] + self.media["Episode"]["Titles"][language]

			if (
				self.media["States"]["Has a list of media items"] == False or
				self.media["Item"]["Title"] == self.media["Title"] or
				self.media["States"]["Single unit"] == True
			):
				self.media["Episode"]["with_title_default"] = self.media["Episode"]["with_title"][self.language["Small"]]

		# Defining dubbed media text and add it to the media episode if the media is "Animes", has dubbing, and is set to be watched dubbed
		if (
			self.dictionary["Media type"]["Plural"]["en"] == self.texts["animes, title()"]["en"] and
			self.media["States"]["Dubbing"]["Watch dubbed"] == True
		):
			self.media["States"]["Dubbing"]["Dubbed to the media title"] = False

			if (
				self.language_texts["dubbed_to_the_media_title"] in self.media["Details"] and
				self.media["Details"][self.language_texts["dubbed_to_the_media_title"]] == self.Input.language_texts["yes, title()"]
			):
				self.media["States"]["Dubbing"]["Dubbed to the media title"] = True

			if self.language_texts["dubbed_to_the_media_title"] not in self.media["Details"]:
				self.media["States"]["Dubbing"]["Dubbed to the media title"] = True

			if self.media["States"]["Dubbing"]["Dubbed to the media title"] == True:
				self.media["Episode"]["Dubbing"] = {
					"Text": " " + self.Language.language_texts["dubbed, title()"]
				}

		# Define the accepted file extensions for the media unit
		self.dictionary["File extensions"] = [
			"mp4",
			"mkv",
			"webm"
		]

		# Get the container for the media
		container = self.media["Texts"]["container"][self.language["Small"]]

		# Transform the container into lowercase if the media is not a video channel
		if self.media["States"]["Video"] == False:
			container = container.lower()

		# Make a backup of the original container
		original_container = container

		# Add the "dubbed" text to media container text if the media has dubbing
		if (
			"Dubbing" in self.media["Episode"] and
			"Text" in self.media["Episode"]["Dubbing"]
		):
			container = self.Language.texts["dubbed_{}"][self.language["Small"]].format(container)

		# Define the container text dictionary with its keys
		self.media["Texts"]["container_text"] = {
			"container": container,
			"this": self.media["Texts"]["genders"][self.language["Small"]]["this"] + " " + container,
			"the": self.media["Texts"]["genders"][self.language["Small"]]["the"] + " " + container,
			"the (original)": self.media["Texts"]["genders"][self.language["Small"]]["the"] + " " + original_container,
			"of_the": self.media["Texts"]["genders"][self.language["Small"]]["of_the"] + " " + container
		}

		# If the user is re-watching the media
		if self.media["States"]["Re-watching"] == True:
			# Define the "Re-watched" dictionary
			self.Define_Re_Watching()

		# Define the "Watching" text for the media
		self.media["Texts"]["Watching"] = {}

		# Iterate through the list of small languages
		for language in self.languages["small"]:
			# Define the default watching text as "watching"
			watching_text = self.texts["watching, infinitive"][language]

			# If the user is re-watching the media
			if self.media["States"]["Re-watching"] == True:
				# Change the watching text to "re-watching"
				watching_text = self.texts["re_watching, infinitive"][language]

			# Add the watching text to the "Watching" text key, in the current language
			self.media["Texts"]["Watching"][language] = watching_text

		# Define the header text to be used on the "Show_Media_Information" root method
		self.dictionary["Header text"] = self.language_texts["opening_{}_to_watch"].format(self.media["Texts"]["container_text"]["this"]) + ":"

		# If the user is re-watching the media
		if self.media["States"]["Re-watching"] == True:
			# Replace the "watch" text with the "re-watch" text
			self.dictionary["Header text"] = self.dictionary["Header text"].replace(self.language_texts["watch"], self.language_texts["re_watch"])

	def Define_Re_Watching(self):
		# Define the default re-watching dictionary
		self.media["Episode"]["Re-watching"] = {
			"Times": "",
			"Number name": {},
			"Texts": {
				"Number": {},
				"Number name": {},
				"Times": {}
			}
		}

		# If there is a re-watching dictionary inside the root dictionary
		if "Re-watching" in self.dictionary:
			# Define the times on the local re-watching dictionary as the one on the root dictionary
			self.media["Episode"]["Re-watching"]["Times"] = self.dictionary["Re-watching"]["Times"]

		# If the "Run as module" switch is False
		if self.run_as_module == False:
			# Define the default watched times as an empty string
			watched_times = ""

			# If the times inside the root dictionary is not an empty string (the default value)
			if self.media["Episode"]["Re-watching"]["Times"] != "":
				# Update the local watched times with that value
				watched_times = self.media["Episode"]["Re-watching"]["Times"]

			# Show a five dash space separator
			print(self.separators["5"])

			# Show the title text
			print()
			print(self.Language.language_texts["title, title()"] + ":")

			# Show the default "with media title" version of the episode
			print("\t" + self.media["Episode"]["with_title_default"])

			# While the watched times variable is not an integer
			while not isinstance(watched_times, int):
				# Define the type text
				type_text = self.language_texts["type_the_number_of_times_that_you_watched"]

				# Add the lowercase "the unit" text to the type text
				# (Animes, series, and cartoons: "the episode"
				# Videos: "the video"
				# Movies: "the movie")
				type_text += " " + self.media["Texts"]["the_unit"][self.language["Small"]].lower()

				# ----- #

				# If the "Testing" switch is False
				if self.switches["Testing"] == False:
					# Ask for the number of times the user watched the media unit (episode, single unit, or movie)
					watched_times = self.Input.Type(type_text)

				else:
					# Define it as one
					watched_times = 1

					# Show the type text and number of watched times
					print()
					print(type_text + ": " + str(1))

				# Try to transform the input into an integer
				try:
					watched_times = int(watched_times)

				# Except a ValueError, define the watched time as an empty string
				except ValueError:
					watched_times = ""

		# If the "Run as module" switch is True
		if self.run_as_module == True:
			# Define the watched times as one
			watched_times = 1

		# If the watched times is not zero
		if watched_times != 0:
			# Define the watched times in the dictionary as the local watched times
			self.media["Episode"]["Re-watching"]["Times"] = watched_times

			# Iterate through the list of small languages
			for language in self.languages["small"]:
				# Define the number name
				self.media["Episode"]["Re-watching"]["Number name"][language] = self.Date.texts["number_names_feminine, type: list"][language][watched_times]

				# Define the "number" re-watched text as the " (Re-watched [watched times]x)" text
				# 
				# Examples:
				# " (Re-watched 1x)"
				# " (Re-watched 2x)"
				self.media["Episode"]["Re-watching"]["Texts"]["Number"][language] = " (" + self.language_texts["re_watched, capitalize()"] + " " + str(self.media["Episode"]["Re-watching"]["Times"]) + "x)"

				# ---------- #

				# Define the text template for the number of watched times
				# (Singular or plural)
				text = self.Text.By_Number(watched_times, self.Language.texts["{}_time"][language], self.Language.texts["{}_times"][language])

				# Format the text template with the name of the number of watched times
				# Examples: one time, two times
				text = text.format(self.media["Episode"]["Re-watching"]["Number name"][language])

				# Define the times text above inside the root times dictionary on the texts dictionary
				self.media["Episode"]["Re-watching"]["Texts"]["Times"][language] = text

				# Define the number name re-watched text as the "Re-watched [watched times]" text
				# 
				# Examples:
				# Re-watched one time
				# Re-watched two times
				self.media["Episode"]["Re-watching"]["Texts"]["Number name"][language] = self.texts["re_watched, capitalize()"][language] + " " + text

		# If the number of watched times is zero
		# (The user never watched the media episode or unit)
		if watched_times == 0:
			# Turn off the re-watching state
			self.media["States"]["Re-watching"] = False

	def Define_Media_Unit(self):
		# Define a list of tried files that were not found
		tried_files = []

		# If the media is not a video channel
		# And the media has dubbing
		if (
			self.media["States"]["Video"] == False and
			self.media["States"]["Dubbing"]["Has dubbing"] == True
		):
			# Define the local dubbed (always user language) folder
			folder = self.media["Item"]["Folders"]["Media"]["root"] + self.language["Full"] + "/"

			# If the user wants to watch the media dubbed (user language)
			# Or the dubbed (user language) folder exists
			if (
				self.media["States"]["Dubbing"]["Watch dubbed"] == True or
				self.Folder.Exists(folder) == True
			):
				# Define the root media folder as the dubbed (user language) folder
				self.media["Item"]["Folders"]["Media"]["root"] = folder

		# Create the root media folder
		self.Folder.Create(self.media["Item"]["Folders"]["Media"]["root"])

		# Add the media episode title to the local media folder, to create the media unit
		self.media["Episode"]["unit"] = self.media["Item"]["Folders"]["Media"]["root"] + self.media["Episode"]["Sanitized"]

		# Add the media unit to the list of tried files
		tried_files.append(self.media["Episode"]["unit"])

		# Define the "file exists" check
		file_exists = self.File_Exists(self.media["Episode"]["unit"])

		# If the media has dubbing
		# And no "Watch dubbed" setting was found
		# Or the user language episode file does not exist
		if (
			self.Language.language_texts["dubbing, title()"] in self.media["Details"] and
			self.found_watch_dubbed_setting == False or
			file_exists == False
		):
			# If the user language episode file does exist
			# And the "Dubbed" text is inside the file, define the "Watch dubbed" state as True
			if (
				file_exists == True and
				self.Language.texts["dubbed, title()"][self.language["Small"]] in self.media["Episode"]["unit"]
			):
				self.media["States"]["Dubbing"]["Watch dubbed"] = True

			# If the user language episode file does not exist
			if file_exists == False:
				# Define the "Watch dubbed" state as False
				self.media["States"]["Dubbing"]["Watch dubbed"] = False

				# Make a list of languages to iterate through
				languages = self.languages["small"].copy()

				# Remove the user language
				# (Since the user language episode was not found, so we have to use another language to try to find the media unit (episode file))
				languages.remove(self.language["Small"])

				# Iterate through the local list of small languages
				for language in languages:
					# Define the full language
					full_language = self.languages["full"][language]

					# Sanitize the language episode title to get the file name
					file_name = self.Sanitize_Title(self.media["Episode"]["Titles"][language])

					# Define the root episode file
					self.media["Episode"]["unit"] = self.media["Item"]["Folders"]["Media"]["root"].replace(self.language["Full"] + "/", "")

					# If the language is not equal to the media language, add the full language folder to the episode unit
					# (Episode units of media on their native language are not placed inside a full language folder)
					if language != self.media["Language"]:
						self.media["Episode"]["unit"] = self.media["Episode"]["unit"] + full_language + "/"
						self.Folder.Create(self.media["Episode"]["unit"])

					# Add the language episode file name to the episode unit
					self.media["Episode"]["unit"] += file_name

					# Add the file to the list of tried files
					tried_files.append(self.media["Episode"]["unit"])

					# Iterate through the accepted file extensions
					for extension in self.dictionary["File extensions"]:
						# Define the local media file with the current extension
						file = self.media["Episode"]["unit"] + "." + extension

						# If the file exists
						if self.File.Exists(file) == True:
							# Define the media unit as the local file
							self.media["Episode"]["unit"] = file

							# Say that the file exists
							file_exists = True

		# If it does not, then, ask if the user wants to move the file from somewhere to the correct folder
		if file_exists == False:
			# Show the "Files" text
			print()
			print(self.File.language_texts["files, title()"] + ":")

			# Show the list of tried files
			for file in tried_files:
				print("\t" + file + "." + str(self.dictionary["File extensions"]).replace("'", "").replace(", ", "/"))

			# Tell the user that the media file does not exist
			print()
			print(self.language_texts["the_media_file_does_not_exist"] + ".")
			print()

			# Define the question asking the user if they want to bring the file from another folder
			question = self.language_texts["do_you_want_to_bring_it_from_another_folder"]

			# Ask the question
			bring_file = self.Input.Yes_Or_No(question, first_space = False)

			# If the answer is "Yes", use the "Find_Media_File" method to find and move the file
			if bring_file == True:
				self.media["Episode"]["unit"] = self.Find_Media_File(self.media["Episode"]["Sanitized"])

			# Else, finish the program execution
			if bring_file == False:
				print()
				quit(self.Language.language_texts["alright"] + ".")

	def File_Exists(self, file):
		# Define the "file exists" switch as False by default
		file_exists = False

		# Iterate through the accepted file extensions
		for extension in self.dictionary["File extensions"]:
			# Define the new file as a copy of the file
			new_file = file

			# If the extension is not inside the file path
			if "." + extension not in new_file:
				# Add it
				new_file += "." + extension

			# If the file exists
			if self.File.Exists(new_file) == True:
				# Switch the "file exists" switch to True
				file_exists = True

				# Update the media unit file
				self.media["Episode"]["unit"] = new_file

		# Return the "file exists" switch
		return file_exists

	def Show_Information(self):
		self.Show_Media_Information(self.dictionary)

	def Open_Media_Unit(self):
		# Open media unit with its executor
		self.System.Open(self.media["Episode"]["unit"])
	
	def Create_Discord_Status(self):
		# Make a custom status of the media to put on the Discord custom status, with the media and episode title

		# Define the status
		status = self.media["Details"][self.Language.language_texts["status, title()"]]

		# Define the key for the episode title
		key = "with_title"

		# If the media has a list of media
		# And the media item is not the media
		# And the media is not a video channel
		# And the media item is not single unit
		# And the "Replace title" state is deactivated
		if (
			self.media["States"]["Has a list of media items"] == True and
			self.media["States"]["The media item is the root media"] == False and
			self.media["States"]["Video"] == False and
			self.language_texts["single_unit"] not in self.media["Item"]["Details"] and
			self.media["States"]["Replace title"] == False
		):
			key = "with_title_and_item"

		# If the key is present in the "Episode" dictionary
		if key in self.media["Episode"]:
			# Define the title using the key
			title = self.media["Episode"][key][self.language["Small"]]

		# Define the title using the key
		#title = self.media["Episode"]["with_title_default"]

		# If the media is not a series media
		if self.media["States"]["Series media"] == False:
			# Define the title as the episode title in the user language, plus the original title of the episode
			title = self.media["Episode"]["Titles"][self.media["Language"]] + " (" + self.media["Episode"]["Titles"]["Original"].split("(")[1]

		# Define the "Discord" dictionary and the status
		self.dictionary["Discord"] = {
			"Status": ""
		}

		# Define the status, adding the media item status, media type, and media title + episode title
		self.dictionary["Discord"]["Status"] = status + " " + self.dictionary["Media type"]["Singular"][self.language["Small"]] + ": " + title

		# Copy the status
		self.Text.Copy(self.dictionary["Discord"]["Status"])

	def Start_Watching_Media(self):
		# Create the "Entry" dictionary inside the root dictionary, with its default keys
		self.dictionary["Entry"] = {
			"Times": {
				"Started watching": {},
				"Finished watching": {},
				"Finished watching (UTC)": {},
				"Watching session duration": {}
			}
		}

		# Define the text that asks the user to press Enter when they start watching the media
		text = self.Language.language_texts["press_enter_when_you_start"]

		# Define a local (re)watching text
		watching_text = " " + self.media["Texts"]["Watching"][self.language["Small"]]

		# Define a local "the unit" text
		the_unit_text = " " + self.media["Texts"]["the_unit"][self.language["Small"]]

		# Add the " (re)watching" and "the unit" texts
		text += watching_text
		text += the_unit_text

		# Show a five dash space separator
		print()
		print(self.separators["5"])

		# If the "Testing" switch is False
		if self.switches["Testing"] == False:
			# Ask the user to press Enter when they start watching
			# (This pauses the execution and waits for the user to press Enter to proceed)
			self.Input.Type(text)

		# Otherwise, the "Testing" mode is active, so no user input is requested
		else:
			print()
			print(text + ":")

		# Register the started watching time in the "Times" dictionary
		time_key = "Started watching"
		self.dictionary["Entry"]["Times"][time_key] = self.Date.Now()

		# Define the text to be shown
		text = self.Language.language_texts["when_you_started"] + watching_text + the_unit_text

		# Show the time when the user started watching the media
		print()
		print(text + ":")
		print("\t" + self.dictionary["Entry"]["Times"][time_key]["Formats"]["HH:MM DD/MM/YYYY"])

		# Show a five dash space separator
		print()
		print(self.separators["5"])

	def Comment_On_Media(self):
		# Ask if the user wants to comment on the media being watched (using the "Comment_Writer" class)
		# And getting the updated root dictionary from it
		self.dictionary = self.Comment_Writer(self.dictionary).dictionary

	def Register_Watched_Media(self):
		# Define the text that asks the user to press Enter when they finish watching the media
		text = self.Language.language_texts["press_enter_when_you_finish"]

		# Define a local (re)watching text
		watching_text = " " + self.media["Texts"]["Watching"][self.language["Small"]]

		# Define a local "the unit" text
		the_unit_text = " " + self.media["Texts"]["the_unit"][self.language["Small"]]

		# Add the " (re)watching" and "the unit" texts
		text += watching_text
		text += the_unit_text

		# Show a five dash space separator
		print()
		print(self.separators["5"])

		# If the "Testing" switch is False
		if self.switches["Testing"] == False:
			# Ask the user to press Enter when they finish watching
			# (This pauses the execution and waits for the user to press Enter to proceed)
			self.Input.Type(text)

		# Otherwise, the "Testing" mode is active, so no user input is requested
		else:
			print()
			print(text + ":")

		# Register the finished watching time in the "Times" dictionary
		time_key = "Finished watching"
		self.dictionary["Entry"]["Times"][time_key] = self.Date.Now()

		# Register the finished watching time in the UTC time
		self.dictionary["Entry"]["Times"][time_key + " (UTC)"] = self.dictionary["Entry"]["Times"][time_key]

		# If the "Testing" switch is active
		if self.switches["Testing"] == True:
			# Retrieve the current time object for the session
			current_time_object = self.dictionary["Entry"]["Times"][time_key]["Object"]

			# Add 31 minutes and 28 seconds to the finished watching time for testing purposes
			# This ensures there is a time difference for the "Date.Difference" method to calculate
			# Preventing errors when no real time has passed in testing mode
			self.dictionary["Entry"]["Times"][time_key] = self.Date.Now(
				current_time_object + self.Date.Relativedelta(minutes = 31, seconds = 28)
			)

		# Define the text to be shown
		text = self.Language.language_texts["when_you_finished"] + watching_text + the_unit_text

		# Show the time when the user finished watching the media
		print()
		print(text + ":")
		print("\t" + self.dictionary["Entry"]["Times"][time_key]["Formats"]["HH:MM DD/MM/YYYY"])

		# Define the "Date" key to be the finished watching time date object
		self.dictionary["Entry"]["Date"] = self.dictionary["Entry"]["Times"][time_key]

		# Set the "Finished watching" state to True
		self.media["States"]["Finished watching"] = True

		# Define shortcuts for the start and finish times
		start_time = self.dictionary["Entry"]["Times"]["Started watching"]
		finish_time = self.dictionary["Entry"]["Times"]["Finished watching"]

		# Calculate the time difference between the start and finish times
		self.dictionary["Entry"]["Times"]["Watching session duration"] = self.Date.Difference(start_time, finish_time)

		# Show the watching session duration text in the user language
		print()
		print(self.language_texts["watching_session_duration"] + ":")
		print("\t" + self.dictionary["Entry"]["Times"]["Watching session duration"]["Text"][self.language["Small"]])

		# Use the "Register" class to register the watched media, by giving the root dictionary to it
		self.Register(self.dictionary)

	def Find_Media_File(self, file_name):
		self.frequently_used_folders = [
			self.Folder.folders["User"]["downloads"]["root"],
			self.Folder.folders["User"]["downloads"]["videos"]["root"],
			self.Folder.folders["User"]["downloads"]["mega"]["root"]
		]

		old_file = self.Select_Folder_And_Media_File(self.frequently_used_folders)

		new_file = self.media["Item"]["Folders"]["Media"]["root"] + self.Sanitize(file_name, restricted_characters = True) + "."

		text = self.language_texts["please_select_a_file_that_is_in_the_format"] + " "

		# Iterate through the accepted file extensions
		for extension in self.dictionary["File extensions"]:
			if extension == self.dictionary["File extensions"][-1]:
				text += self.Language.language_texts["genders, type: dictionary, masculine"]["or"] + " "

			text += extension.upper()

			if extension != self.dictionary["File extensions"][-1]:
				text += ", "

		if old_file.split(".")[-1] not in self.dictionary["File extensions"]:
			while old_file.split(".")[-1] not in self.dictionary["File extensions"]:
				print()
				print(text + ".")

				old_file = self.Select_Folder_And_Media_File(self.frequently_used_folders)

				new_file = self.media["Item"]["Folders"]["Media"]["root"] + file_name + "."

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
		# Iterate through the accepted file extensions
		for extension in self.dictionary["File extensions"]:
			if extension in old_file:
				new_file = new_file + extension

		return self.File.Move(old_file, new_file)