# Populate_Media_Episodes_Files.py

# Import the root "Watch_History" class
from Watch_History.Watch_History import Watch_History as Watch_History

# Import the "deepcopy" module from the "copy" module
from copy import deepcopy

class Populate_Media_Episodes_Files(Watch_History):
	def __init__(self):
		super().__init__()

		# Define the root dictionary
		self.root_dictionary = {
			"Methods": { # A dictionary of class methods to select from
				"Populate episode titles files": {
					"Name": "Populate episode titles files",
					"Text": self.language_texts["populate_the_episode_titles_files"],
					"Object": self.Populate_Episode_Titles_Files
				}
			}
		}

		# ---------- #

		# Define the media dictionary
		self.dictionary = {
			"Media type": {
				"Status": [
					self.texts["watching, title()"]["en"],
					self.texts["re_watching, title()"]["en"]
				],

				# Remove the "Movies" media type from the media type dictionary, returning a local media types dictionary
				"List": self.Remove_Media_Type("Movies")
			}
		}

		# Ask user to select the media type and the media
		# Passing the "select_media_item" parameter as True to ask for the user to select a media item
		self.dictionary = self.Select_Media_Type_And_Media(self.dictionary, watch = True, select_media_item = True)

		# Define a shortcut to the "Media" dictionary
		self.media = self.dictionary["Media"]

		# ---------- #

		# Define the "Populate episode titles" inside the root dictionary
		self.root_dictionary["Populate episode titles"] = {
			"Episodes": {
				"Numbers": {
					"Total episodes of the media item": 1,
					"Total episodes of all media items up to the current one": 1
				},
				**self.media["Item"]["Episodes"]
			}
		}

		# ---------- #

		# Show a five dash space separator
		print()
		print(self.separators["5"])

		# If the media is a video channel
		if self.media["States"]["Video"] == True:
			# Define the name of the method
			name = "Add to the list of videos"

			# Create the method dictionary of the method
			method = {
				"Name": name,
				"Text": self.language_texts["add_to_the_list_of_videos"],
				"Object": self.Add_To_The_List_Of_Videos
			}

			# Add the method dictionary to the root "Methods" dictionary
			self.root_dictionary["Methods"][name] = method

		# ---------- #

		# Define a shortcut to the methods dictionary
		methods = self.root_dictionary["Methods"]

		# Get the keys
		keys = list(methods.keys())

		# Get the values
		values = list(methods.values())

		# Define the method initially as the "Populate episode titles files" method
		method = "Populate episode titles files"

		# If there is more than one method
		if len(methods) > 1:
			# Define the options and language options based on the dictionary of methods
			options = keys
			language_options = values

			# Define the show and select texts
			show_text = self.Language.language_texts["methods_of_the_{}_class_to_run"]
			select_text = self.Language.language_texts["select_one_method_to_run"]

			# Ask the user to select the method
			method = self.Input.Select(
				options,
				language_options = methods,
				show_text = show_text,
				select_text = select_text
			)["Option"]["Original"]

		# Get the method dictionary
		method = methods[method]

		# Define the selected method as the local one
		self.selected_method = method

		# Run the class method
		method["Object"]()

	def Populate_Episode_Titles_Files(self):
		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Define a text key to tell the user which action the class is doing (populating the episode titles files)
		text_key = "populating_the_episode_titles_files"

		# If the media is a video channel
		if self.media["States"]["Video"] == True:
			# Update the text key to also talk about the IDs files
			text_key = "populating_the_episode_title_and_ids_files"

		# Get the language text for the text key
		language_text = self.language_texts[text_key]

		# Show it
		print(language_text + "...")

		# ---------- #

		# Show the episode titles files by language
		for language in self.languages["Small"]:
			# Get the translated language for the current language
			translated_language = self.languages["Full (translated)"][language][self.language["Small"]]

			# Format the episode titles file text with the translated language
			text = self.language_text["episode_titles_file_in_{}"].format(translated_language)

			# Show the text and the file in the current language
			print()
			print(text + ":")
			print("\t" + self.root_dictionary["Populate episode titles"]["Episodes"]["Titles"]["Files"][language])

		# ---------- #

		# If the media is not a video channel
		if self.media["States"]["Video"] == False:
			# Define a root shortcut to the "Episodes" dictionary
			self.episodes = self.root_dictionary["Populate episode titles"]["Episodes"]

			# Define the error variable as True to make the while loop work
			error = True

			# Prompt repeatedly until the user enters a valid integer
			while error == True:
				# Ask for the total episode number of the media (item)
				number = self.Input.Type(
					self.language_texts["type_the_number_of_episodes"],
					accept_enter = False
				)

				# Convert the input to an integer, if it succeeds, exit the loop
				try:
					# Convert it
					number = int(number)

					# Add the local number to the "Total episodes of the media item" key
					self.episodes["Numbers"]["Total episodes of the media item"] = number

					# Change the error variable to False
					error = False

				# Invalid input, keep asking
				except ValueError:
					pass

			# ---------- #

			# If the media has a list of media items
			# And the media item is not the first one in the list
			if (
				self.media["States"]["Has a list of media items"] == True and
				self.media["Item"]["Title"] != self.media["Items"]["List"][0]
			):
				# Define the error variable as True to make the while loop work
				error = True

				# Prompt repeatedly until the user enters a valid integer
				while error == True:
					# Ask for the total number of episodes up to the current media item
					number = self.Input.Type(
						self.language_texts["type_the_number_of_all_media_episodes"],
						accept_enter = False
					)

					# Convert the input to an integer, if it succeeds, exit the loop
					try:
						number = int(number)

						# Add the local number to the "Total episodes of all media items up to the current one" key
						self.episodes["Numbers"]["Total episodes of all media items up to the current one"] = number

						# Change the error variable to False
						error = False

					# Invalid input, keep asking
					except ValueError:
						pass

				# Add one to the total number of episodes up to the current media item
				self.episodes["Numbers"]["Total episodes of all media items up to the current one"] += 1

			# Define a shortcut to a text telling the user that they finished populating the episode titles files
			text = self.language_texts["you_finished_populating_the_episode_titles_files"]

		# ---------- #

		# If the media is a video channel
		if self.media["States"]["Video"] == True:
			# Show the IDs file
			print()
			print(self.Language.language_texts["ids_file"] + ":")
			print("\t" + self.media["Item"]["Folders"]["Titles"]["IDs"])

			# Get the IDs from the user (or the media item files)
			self.Get_IDs()

			# Define a shortcut to a text telling the user that they finished populating the episode titles and IDs files
			text = self.language_texts["you_finished_populating_the_episode_titles_and_ids_files"]

		# ---------- #

		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Populate the episode titles (and IDs) files
		self.Populate_The_Files()

		# Show the text defined by the non-video or video sections above
		print(text + ".")

	def Replace_Text(self, text):
		# Define a list of items to remove from the text
		items_to_remove = [
			"(",
			")",
			"\t",
			'"'
		]

		# If there is a space at the start of the text, remove it
		if " " in text[0]:
			text = text[:1]

		# If there is one at the end, also remove it
		if " " in text[-1]:
			text = text[:-1]

		# Replace double spaces with only one
		if "  " in text:
			text = text.replace("  ", " ")

		# Remove the items to remove if they are present
		for list_item in items_to_remove:
			if list_item in text:
				text = text.replace(list_item, "")

		# Return the replaced text
		return text

	def Translate_Title(self, language, translated_language, title):
		# If the local language is not the same as the media language
		if language != self.media["Language"]:
			# Define an information text to show to the user asking them to translate the title to the translated language
			text = self.language_texts["please_translate_this_title_to_{}"].format(translated_language)

			# Show the information text about translating the title and the original title
			print(text + ":")
			print("[" + title + "]")

			# Copy the user language title to the user's clipboard
			self.Text.Copy(title)

			# Ask for the user to type or paste the translated title
			title = self.Input.Type(self.Language.language_texts["title, title()"] + ": ", accept_enter = False)

		# Return the translated title
		return title

	def Populate_The_Files(self):
		# Define a local "add to the list of videos" switch as False by default
		add_to_the_list_of_videos = False

		# If the selected method is "Add to the list of videos"
		if self.selected_method["Name"] == "Add to the list of videos":
			# Switch it to True
			add_to_the_list_of_videos = True

		# If the media is a video channel
		if self.media["States"]["Video"] == True:
			# Get the videos dictionary for the media item, passing the "add to the list of videos" switch as a parameter
			self.videos = self.Get_Videos(add_to_the_list_of_videos)

		# If the selected method is not "Add to the list of videos"
		if self.selected_method["Name"] != "Add to the list of videos":
			# If the media is a video channel
			if self.media["States"]["Video"] == True:
				# Update the number of episodes of the current media item to be the number of videos
				self.episodes["Numbers"]["Total episodes of the media item"] = self.videos["Numbers"]["Total"]

			# ---------- #

			# Define a shortcut to the number of episodes of the current media item
			current_media_item_episodes_number = self.episodes["Numbers"]["Total episodes of the media item"]

			# ---------- #

			# If the media is not a video channel
			# And the media has a list of media items
			# And the media item is not the first one in the list
			if (
				self.media["States"]["Video"] == False and
				self.media["States"]["Has a list of media items"] == True and
				self.media["Item"]["Title"] != self.media["Items"]["List"][0]
			):
				# Define a shortcut to the number of episodes up to (and including) the current media item
				media_items_episodes_number = self.episodes[
					"Numbers"
				]["Total episodes of all media items up to the current one"]

				# Define a total number text as the total number of media item episodes and the total number of episodes of all media items up to the current one added together, less one
				total_number_text = (current_media_item_episodes_number + media_items_episodes_number) - 1

				# Convert it to a string
				total_number_text = str(total_number_text)

			# ---------- #

			# Define a local episode number as zero
			episode_number = 0

			# While the local episode number is lesser than or equal to the number of episodes of the current media item
			while episode_number <= self.episodes["Numbers"]["Total episodes of the media item"]:
				# Define the progress text as the "Episode numbers" text
				progress_text = f"""
				{self.language_texts["episode_numbers"]}:
				[{episode_number}/{current_media_item_episodes_number}]
				""".replace("\t", "")

				# If the media is not a video channel
				# And the media has a list of media items
				# And the media item is not the first one in the list
				if (
					self.media["States"]["Video"] == False and
					self.media["States"]["Has a list of media items"] == True and
					self.media["Item"]["Title"] != self.media["Items"]["List"][0]
				):
					# Remove the leading zeroes from the number of episodes up to (and including) the current media item and also convert it into a text string
					number = str(self.Text.Remove_Leading_Zeroes(media_items_episodes_number))

					# Add it to the progress text with parentheses
					progress_text = progress_text.replace("]", " (" + number + ")]")

				# Show the progress text
				print(progress_text)

				# ---------- #

				# Iterate through the list of small languages
				for language in self.languages["Small"]:
					# Get the full language
					full_language = self.languages["Full"][language]

					# Get the translated language for the current language in the user language
					translated_language = self.languages["Full (translated)"][language][self.language["Small"]]

					# If the current language list is not inside the "Titles" dictionary
					if language not in self.episodes["Titles"]:
						# Add it
						self.episodes["Titles"][language] = []

					# ---------- #

					# Define the episode title as an empty string by default
					episode_title = ""

					# If the media is not a video channel
					if self.media["States"]["Video"] == False:
						# Define the full episode title as the "EP" text and the current episode number
						episode_title = "EP" + str(self.Text.Add_Leading_Zeroes(episode_number + 1))

						# If the media has a list of media items
						# And the media item is not the first one in the list
						if (
							self.media["States"]["Has a list of media items"] == True and
							self.media["Item"]["Title"] != self.media["Items"]["List"][0]
						):
							# Add leading zeroes to the number of episodes up to (and including) the current media item
							number = str(self.Text.Add_Leading_Zeroes(media_items_episodes_number))

							# Add the number with parentheses to the episode title
							episode_title += "(" + number + ")"

						# Define the "first space" switch as True by default
						first_space = True

						# If the current language is the first one in the list of small languages
						if language == self.languages["Small"][0]:
							# Switch the "first space" switch to False
							first_space = False

						# If the "Testing" switch is False
						if self.switches["Testing"] == False:
							# Define the input text
							input_text = self.language_texts["paste_the_episode_title_in_{}"]

							# Format it with the translated language
							input_text = input_text.format("[" + translated_language + "]")

							# Ask for the episode title
							title = self.Input.Type(input_text, accept_enter = False, next_line = True, first_space = first_space)

						# If the "Testing" switch is True
						if self.switches["Testing"] == True:
							# Get the episode title text in the current language
							episode_title_text = self.texts["episode_title"][language]

							# Get the "in [language]" text in the current language
							in_language_text = self.Language.texts["in_[language]"][language][language]

							# Define the episode title as the "Episode title in [language]" text
							title = episode_title_text + " " + in_language_text

						# Add a space to the end of the episode title
						episode_title += " "

					# ---------- #

					# If the media is a video channel
					if self.media["States"]["Video"] == True:
						# Get the list of video titles for the current language
						video_titles = self.videos["Lists"][language]

						# If the list of video titles in the current language is not empty
						# And the length of the list is greater than or equal to the episode number less one
						# (That means the video title in the current language exists)
						if (
							video_titles != [] and
							len(video_titles) >= episode_number
						):
							# Get the language video title from the list
							video_title = video_titles[episode_number]

						# Else, ask the user to translate the video title in the media language to the current language
						# (That means the video title in the current language does not exist)
						else:
							video_title = self.Translate_Title(language, translated_language, video_title)

						# Define the video title as the episode title
						title = video_title

					# ---------- #

					# Remove some texts from the typed episode title and add quotes
					title = '"' + self.Replace_Text(title) + '"'

					# Add the episode title to the full episode title
					episode_title += title

					# Show the episode title
					print()
					print([episode_title])

					# Add the episode title to the list of episode titles of the current language
					self.episodes["Titles"][language].append(episode_title)

				# Show a five dash space separator
				print()
				print(self.separators["5"])

				# ---------- #

				# If the media is not a video channel
				# And the media has a list of media items
				# And the media item is not the first one in the list
				if (
					self.media["States"]["Video"] == False and
					self.media["States"]["Has a list of media items"] == True and
					self.media["Item"]["Title"] != self.media["Items"]["List"][0]
				):
					# Add one to the "Total episodes of the media item" number
					self.episodes["Numbers"]["Total episodes of the media item"] += 1

				# ---------- #

				# Add one to the local episode number
				episode_number += 1

		# ---------- #

		# Iterate through the list of small languages
		for language in self.languages["Small"]:
			# Get the translated language for the current language in the user language
			translated_language = self.languages["Full (translated)"][language][self.language["Small"]]

			# Show the translated language
			print()
			print(translated_language + ":")

			# Show the language titles
			for title in self.episodes["Titles"][language]:
				print("\t" + title)

			# Get the language episode titles file
			file = self.episodes["Titles"]["Files"][language]

			# Transform the list of episode titles into a text string
			text = self.Text.From_List(self.episodes["Titles"][language], next_line = True)

			# Write the list of episode titles into the language episode titles file
			self.File.Edit(file, text, "w")

		# ---------- #

		# If the media is a video channel
		if self.media["States"]["Video"] == True:
			# Get the list of video IDs and transform it into a text string
			video_ids = self.Text.From_List(self.videos["Lists"]["IDs"], next_line = True)

			# Define a shortcut to the "IDs.txt" file
			file = self.media["Item"]["Folders"]["Titles"]["IDs"]

			# Write the list of video IDs into the "IDs.txt" file
			self.File.Edit(file, video_ids, "w")

			# ----- #

			# Get the list of video dates and transform it into a text string
			video_dates = self.Text.From_List(self.videos["Lists"]["Dates"], next_line = True)

			# Define a shortcut to the "Dates.txt" file
			file = self.media["Item"]["Folders"]["Titles"]["Dates"]

			# Write the list of video dates into the "Dates.txt" file
			self.File.Edit(file, video_dates, "w")

	def Get_Videos(self, add_to_the_list_of_videos = False):
		# Define a root videos dictionary
		videos = {
			"Numbers": {
				"Total": 0
			},
			"Lists": {
				"IDs": [],
				"Titles": {},
				"Dates": []
			},
			"Dictionary": {}
		}

		# Iterate through the list of small languages
		for language in self.languages["Small"]:
			# Create the language titles list
			videos["Lists"]["Titles"][language] = []

		# ---------- #

		# Define a shortcut to the list of video IDs
		video_ids = self.media["Item"]["Episodes"]["Titles"]["IDs"]

		# ---------- #

		# If the list of video IDs is empty
		if video_ids == []:
			# Get the playlist ID from the media item details dictionary
			playlist_id = self.media["Item"]["Details"][self.Language.language_texts["origin_location"]]

			# Get the videos dictionary from the defined playlist using the root "Get_YouTube_Information" method
			videos["Dictionary"] = self.Get_YouTube_Information("Playlist videos", playlist_id)["Videos"]

		# If it is not empty
		else:
			# Define a shortcut to the list of video titles in the user language
			video_titles = self.media["Item"]["Episodes"]["Titles"][self.language["Small"]]

			# Define a shortcut to the list of video dates
			video_dates = self.media["Item"]["Episodes"]["Titles"]["Dates"]

			# Define a local video number
			video_number = 0

			# Iterate through the video IDs in the list of video IDs
			for id in video_ids:
				# Define the video dictionary with its keys inside the local videos "Dictionary" dictionary
				videos["Dictionary"][id] = {
					"Title": video_titles[i],
					"ID": id,
					"Date": video_dates[i]
				}

				# Add one to the video number
				video_number += 1

		# ---------- #

		# If the "add to the list of videos" switch is True
		if add_to_the_list_of_videos == True:
			# Run the "Add_To_The_List_Of_Videos" method
			self.Add_To_The_List_Of_Videos(videos)

		# ---------- #

		# Iterate through the videos inside the videos "Dictionary"
		for id, video in videos["Dictionary"].items():
			# Add the video ID to the "IDs" list
			videos["Lists"]["IDs"].append(video["ID"])

			# Add the video title to the titles list of the media language
			videos["Lists"]["Titles"][self.media["Language"]].append(video["Title"])

			# Add the video date to the "Dates" list
			videos["Lists"]["Dates"].append(video["Times"]["Timezone"])

		# ---------- #

		# Update the total number of videos
		videos["Numbers"]["Total"] = len(videos["Lists"]["IDs"])

		# ---------- #

		# Return the videos dictionary
		return videos

	def Add_To_The_List_Of_Videos(self, videos):
		# Import the "validators" module
		import validators

		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Define an empty video dictionary
		video = {
			"ID": "",
			"Titles": {},
			"Date": ""
		}

		# Iterate through the list of small languages
		for language in self.languages["Small"]:
			# Create the language titles list
			video["Titles"][language] = []

		# ---------- #

		# Define the video link as an empty string
		video_link = ""

		# Define the input text as "paste_the_link_to_the_video"
		input_text = self.language_texts["paste_the_link_to_the_video"]

		# While the video ID is not a link
		while validators.url(video_link) == False:
			# Ask for the video link
			video_link = self.Input.Type(input_text)

		# Parse the video link to get the ID
		video["ID"] = self.Parse_Link(video_link, "Video")

		# ---------- #

		# Show a space
		print()

		# ---------- #

		# Get the video information dictionary
		video_information = self.Get_YouTube_Information("Video", video["ID"])

		# Update the video "Date" key
		video["Date"] = video_information["Times"]["Timezone"]

		# ---------- #

		# Iterate through the list of small languages
		for language in self.languages["Small"]:
			# Get the translated language for the current language in the user language
			translated_language = self.languages["Full (translated)"][language][self.language["Small"]]

			# Ask the user to translate the video title (only if the title in the current language does not exist)
			title = self.Translate_Title(language, translated_language, video_information["Title"])

			# Add the language title to the correct language titles list
			video["Titles"][language] = title

		# Add the video to the videos dictionary
		self.videos["Dictionary"][video["ID"]] = video

		# ---------- #

		# Add the "End date" key after the "Start date" key or update it
		key_value = {
			"key": self.Date.language_texts["end_date"],
			"value": video["Date"]
		}

		self.media["Item"]["Details"] = self.JSON.Add_Key_After_Key(self.media["Item"]["Details"], key_value, after_key = self.Date.language_texts["start_date"])

		# ---------- #

		# Define a shortcut to the media item "Episode" key
		media_item_episode = self.media["Item"]["Details"][self.Language.language_texts["episode, title()"]]

		# Define a shortcut to the last episode
		last_episode = self.media["Item"]["Episodes"]["Titles"][self.media["Language"]][-1]

		# If the media item episode is the last episode
		if media_item_episode == last_episode:
			# Update the "Episode" key of the media item details to change it to the new episode
			key_value = {
				"key": self.Language.language_texts["episode, title()"],
				"value": video["Titles"][self.media["Language"]]
			}

			self.media["Item"]["Details"] = self.JSON.Add_Key_After_Key(self.media["Item"]["Details"], key_value, after_key = self.language_texts["episodes, title()"])

		# Transform the media item details dictionary into a text string
		media_item_details = self.Text.From_Dictionary(self.media["Item"]["Details"])

		# Update the media item "Details.txt" file with the updated media item details dictionary
		self.File.Edit(self.media["Item"]["Folders"]["details"], media_item_details, "w")

		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Show the YouTube channel
		print(self.Text.Capitalize(self.language_texts["youtube_channel"]) + ":")
		print("[" + self.media["Title"] + "]")
		print()

		# Show the video series
		text = self.language_texts["video_series, type: singular, capitalize()"]

		print(text + ":")
		print("[" + self.media["Item"]["Title"] + "]")
		print()

		# Show the video titles
		for language in self.languages["Small"]:
			# Get the translated language for the current language in the user language
			translated_language = self.languages["Full (translated)"][language][self.language["Small"]]

			# Define the translated language text
			translated_language_text = self.Language.language_texts["title_in_{}"].format(translated_language)

			# Show the translated language text and the title
			print(translated_language_text + ":")
			print("[" + video["Titles"][language] + "]")
			print()

		# Show the video ID
		print(self.language_texts["video_id"] + ":")
		print("\t" + video_id)
		print()

		# Show the video date
		print(self.Date.language_texts["date, title()"] + ":")
		print("\t" + video["Date"])

		# Show a five dash space separator
		print()
		print(self.separators["5"])