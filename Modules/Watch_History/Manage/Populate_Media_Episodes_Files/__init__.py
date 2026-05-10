# Populate_Media_Episodes_Files.py

# Import the root "Watch_History" class
from Watch_History.Watch_History import Watch_History as Watch_History

# Import the "deepcopy" module from the "copy" module
from copy import deepcopy

class Populate_Media_Episodes_Files(Watch_History):
	def __init__(self):
		super().__init__()

		# Define the root "populate" dictionary
		self.populate = {
			"Methods": {
				"List": [
					"Populate episode titles files",
					"Add to the list of videos"
				],
				"Dictionary": {
					"Populate episode titles files": {
						"Name": "Populate episode titles files",
						"Language name": self.language_texts["populate_the_episode_titles_files"],
						"Object": self.Populate_Episode_Titles_Files
					},
					"Add to the list of videos": {
						"Name": "Add to the list of videos",
						"Language name": self.language_texts["add_to_the_list_of_videos"],
						"Object": self.Add_To_The_List_Of_Videos
					}
				}
			},
			"Episodes": {}
		}

		# ---------- #

		# Define the root dictionary
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

		# Create a shortcut to the "Media" dictionary
		self.media = self.dictionary["Media"]

		# ---------- #

		# Update the "Episodes" dictionary of the root "populate" dictionary
		self.populate["Episodes"] = {
			"Numbers": {
				"Total episodes of the media item": 1,
				"Total episodes of all media items up to the current one": 1
			},
			**self.media["Item"]["Episodes"]
		}

		# Create a root shortcut to the "Episodes" dictionary
		self.episodes = self.populate["Episodes"]

		# ---------- #

		# Define the method name initially as "Populate episode titles files"
		method_name = "Populate episode titles files"

		# If the media is a video channel
		if self.media["States"]["Video"] == True:
			# Define the list of options as the list of methods
			options = self.populate["Methods"]["List"]

			# Define the list of language options as an empty list
			language_options = []

			# Iterate through the methods
			for method in self.populate["Methods"]["Dictionary"].values():
				# Add the method language name to the list of language options
				language_options.append(method["Language name"])

			# Define the show text as the "Methods of the {} class to run" and format it with the class name
			show_text = self.Language.language_texts["methods_of_the_{}_class_to_run"].format(self.language_texts["populate_media_episodes_files"])

			# Define the select text as "Select one method to run"
			select_text = self.Language.language_texts["select_one_method_to_run"]

			# Ask the user to select a method from the list of methods using the parameters defined above
			method_name = self.Input.Select(options, language_options = language_options, show_text = show_text, select_text = select_text)["Option"]["Original"]

		# Get the method dictionary using its name
		method = self.populate["Methods"]["Dictionary"][method_name]

		# Define the root selected method as the local one
		self.selected_method = method

		# Run the selected class method
		self.selected_method["Object"]()

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

		# Iterate through the language keys and dictionaries
		for small_language, language in self.languages["Dictionary"].items():
			# Get the current language translated to the user language
			translated_language = language["Translated"][self.language["Small"]]

			# Format the "Episode titles file in {}" text with the translated language
			text = self.language_text["episode_titles_file_in_{}"].format(translated_language)

			# Create a shortcut to the file
			file = self.populate["Episodes"]["Titles"]["Files"][small_language]

			# Show the text and the file in the current language
			print()
			print(text + ":")
			print("\t" + file)

		# ---------- #

		# If the media is not a video channel
		if self.media["States"]["Video"] == False:
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

			# Create a shortcut to a text telling the user that they finished populating the episode titles files
			text = self.language_texts["you_finished_populating_the_episode_titles_files"]

		# ---------- #

		# If the media is a video channel
		if self.media["States"]["Video"] == True:
			# Show the IDs file
			print()
			print(self.Language.language_texts["ids_file"] + ":")
			print("\t" + self.media["Item"]["Folders"]["Titles"]["IDs"])

			# Create a shortcut to a text telling the user that they finished populating the episode titles and IDs files
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
		# If the media is a video channel
		# And the selected method is "Populate episode titles files"
		if (
			self.media["States"]["Video"] == True and
			self.selected_method["Name"] == "Populate episode titles files"
		):
			# Get the videos dictionary for the media (item)
			self.videos = self.Get_Videos()

		# If the selected method is "Populate episode titles files"
		if self.selected_method["Name"] == "Populate episode titles files":
			# If the media is a video channel
			if self.media["States"]["Video"] == True:
				# Update the number of episodes of the current media item to be the number of videos
				self.episodes["Numbers"]["Total episodes of the media item"] = self.videos["Numbers"]["Total"]

			# ---------- #

			# Create a shortcut to the number of episodes of the current media item
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
				# Create a shortcut to the number of episodes up to (and including) the current media item
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

				# Iterate through the language keys and dictionaries
				for small_language, language in self.languages["Dictionary"].items():
					# Create a shortcut to the full language
					full_language = language["Full"]

					# Get the current language translated to the user language
					translated_language = language["Translated"][self.language["Small"]]

					# If the current language list is not inside the "Titles" dictionary
					if small_language not in self.episodes["Titles"]:
						# Add it
						self.episodes["Titles"][small_language] = []

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
						if small_language == self.languages["Small"][0]:
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
							episode_title_text = self.texts["episode_title"][small_language]

							# Get the "in [language]" text in the current language
							# Examples:
							# ["en"]["en"]: "in English"
							# ["pt"]["en"]: "in Portuguese"
							# ["pt"]["pt"]: "em Português"
							# ["en"]["pt"]: "em Inglês"
							in_language_text = self.Language.texts["in_[language]"][small_language][small_language]

							# Define the episode title as the "Episode title in [language]" text
							title = episode_title_text + " " + in_language_text

						# Add a space to the end of the episode title
						episode_title += " "

					# ---------- #

					# If the media is a video channel
					if self.media["States"]["Video"] == True:
						# Get the list of video titles for the current language
						video_titles = self.videos["Titles"][small_language]

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
							video_title = self.Translate_Title(small_language, translated_language, video_title)

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
					self.episodes["Titles"][small_language].append(episode_title)

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

		# Define the writing mode as "write" by default
		writing_mode = "w"

		# If the selected method is "Add to the list of videos"
		if self.selected_method["Name"] == "Add to the list of videos":
			# Change the writing mode to "append"
			writing_mode = "a"

		# Iterate through the language keys and dictionaries
		for small_language, language in self.languages["Dictionary"].items():
			# Get the episode titles file in the current language
			file = self.episodes["Titles"]["Files"][small_language]

			# Get the current language translated to the user language
			translated_language = language["Translated"][self.language["Small"]]

			# If the selected method is "Populate episode titles files"
			if self.selected_method["Name"] == "Populate episode titles files":
				# Define the local dictionary of episode titles as the "episodes" one
				episode_titles = self.episodes["Titles"]

				# Show the translated language
				print()
				print(translated_language + ":")

				# Show the language titles
				for title in episode_titles[small_language]:
					print("\t" + title)

				# Transform the list of episode titles into a text string
				text = self.Text.From_List(episode_titles[small_language])

			# If the selected method is "Add to the list of videos"
			if self.selected_method["Name"] == "Add to the list of videos":
				# Define the local dictionary of episode titles as the "videos" one
				episode_titles = self.videos["Titles"]

				# Define the text as the last title (which was added)
				text = episode_titles[small_language][-1]

			# Write the list of episode titles or new episode title into the language episode titles file
			self.File.Edit(file, text, writing_mode)

		# ---------- #

		# If the media is a video channel
		if self.media["States"]["Video"] == True:
			# Create a shortcut to the "IDs.txt" file
			file = self.media["Item"]["Folders"]["Titles"]["IDs"]

			# If the selected method is "Populate episode titles files"
			if self.selected_method["Name"] == "Populate episode titles files":
				# Define the text as the list of video IDs transformed into a text string
				text = self.Text.From_List(self.videos["IDs"])

			# If the selected method is "Add to the list of videos"
			if self.selected_method["Name"] == "Add to the list of videos":
				# Define the text as the last ID (which was added)
				text = self.videos["IDs"][-1]

			# Write the ID or IDs into the "IDs.txt" file using the defined writing mode
			self.File.Edit(file, text, writing_mode)

			# ----- #

			# Create a shortcut to the "Dates.txt" file
			file = self.media["Item"]["Folders"]["Titles"]["Dates"]

			# If the selected method is "Populate episode titles files"
			if self.selected_method["Name"] == "Populate episode titles files":
				# Define the text as the list of video dates transformed into a text string
				text = self.Text.From_List(self.videos["Dates"])

			# If the selected method is "Add to the list of videos"
			if self.selected_method["Name"] == "Add to the list of videos":
				# Define the text as the last date (which was added)
				text = self.videos["Dates"][-1]

			# Write the date or dates into the "Dates.txt" file using the defined writing mode
			self.File.Edit(file, text, writing_mode)

	def Get_Videos(self, new_video = None):
		# Define a root videos dictionary
		videos = {
			"Numbers": {
				"Total": 0
			},
			"Titles": {},
			"IDs": [],
			"Dates": [],
			"Dictionary": {}
		}

		# Iterate through the list of small languages
		for small_language in self.languages["Small"]:
			# Create the language titles list
			videos["Titles"][small_language] = []

		# Create a shortcut to the dictionary of video titles
		video_titles = self.media["Item"]["Episodes"]["Titles"]

		# Create a shortcut to the list of video IDs
		video_ids = self.media["Item"]["Episodes"]["Titles"]["IDs"]

		# Create a shortcut to the list of video dates
		video_dates = self.media["Item"]["Episodes"]["Titles"]["Dates"]

		# If the "new video" parameter is not None
		if new_video != None:
			# Iterate through the list of small languages
			for small_language in self.languages["Small"]:
				# Add the video title in the current language to the dictionary of video titles
				video_titles[small_language].append(new_video["Titles"][small_language])

			# Add the video ID
			video_ids.append(new_video["ID"])

			# Add the video date
			video_dates.append(new_video["Date"])

		# If the list of video IDs is empty
		if video_ids == []:
			# Get the playlist ID from the media item details dictionary
			playlist_id = self.media["Item"]["Details"][self.Language.language_texts["origin_location"]]

			# Get the videos dictionary from the defined playlist using the root "Get_YouTube_Information" method
			videos["Dictionary"] = self.Get_YouTube_Information("Playlist videos", playlist_id)["Videos"]

		# If the list of video IDs is not empty
		if video_ids != []:
			# Define a local video number
			video_number = 0

			# Iterate through the video IDs in the list of video IDs
			for id in video_ids:
				# Create a local video dictionary
				video = {
					"Titles": {},
					"ID": id,
					"Date": ""
				}

				# If the video number is in the range of the list of video dates
				if video_number <= len(video_dates) - 1:
					# Define the video date as the one in the video number
					video["Date"] = video_dates[video_number]

				# Iterate through the list of small languages
				for small_language in self.languages["Small"]:
					# Add the video title in the current language
					video["Titles"][small_language] = video_titles[small_language][video_number]

				# If the video number is not in the range of the list of video dates
				if video_number > len(video_dates) - 1:
					# Tell the user that the video date was not found
					print()
					print(self.separators["5"])
					print()
					print("Video date not found:")
					print()
					print("ID:")
					print(id)
					print()
					print("Video title:")
					print(video["Titles"][self.language["Small"]])

					# Pause the for loop so the user reads the message
					input()

				# Add the local video dictionary to the local videos dictionary using the video ID as a key
				videos["Dictionary"][id] = video

				# Add one to the video number
				video_number += 1

		# ---------- #

		# Iterate through the videos inside the videos "Dictionary"
		for id, video in videos["Dictionary"].items():
			# Iterate through the list of small languages
			for small_language in self.languages["Small"]:
				# Add the video title in the current language
				videos["Titles"][small_language].append(video["Titles"][small_language])

			# Add the video ID to the "IDs" list
			videos["IDs"].append(video["ID"])

			# Add the video date to the "Dates" list
			videos["Dates"].append(video["Date"])

		# ---------- #

		# Update the total number of videos
		videos["Numbers"]["Total"] = len(videos["IDs"])

		# ---------- #

		# Return the videos dictionary
		return videos

	def Add_To_The_List_Of_Videos(self):
		# Show a five dash space separator
		print()
		print(self.separators["5"])

		# Define an empty video dictionary
		video = {
			"Titles": {},
			"ID": "",
			"Date": ""
		}

		# Iterate through the list of small languages
		for small_language in self.languages["Small"]:
			# Create the language titles list
			video["Titles"][small_language] = []

		# ---------- #

		# Define the input text as "Paste the link of the video on YouTube"
		input_text = self.language_texts["paste_the_link_of_the_video_on_youtube"]

		# Get the video ID from the video link
		video["ID"] = self.Get_ID_From_Link(input_text, "Video")

		# ---------- #

		# Show a space
		print()

		# ---------- #

		# Get the video information dictionary
		video_information = self.Get_YouTube_Information("Video", video["ID"])

		# Update the video "Date" key
		video["Date"] = video_information["Times"]["Timezone"]

		# ---------- #

		# Iterate through the language keys and dictionaries
		for small_language, language in self.languages["Dictionary"].items():
			# Get the current language translated to the user language
			translated_language = language["Translated"][self.language["Small"]]

			# Ask the user to translate the video title (only if the title in the current language does not exist)
			title = self.Translate_Title(small_language, translated_language, video_information["Title"])

			# Add the language title to the correct language key
			video["Titles"][small_language] = title

		# Get the videos dictionary for the media item, passing the local video dictionary to it
		self.videos = self.Get_Videos(new_video = video)

		# ---------- #

		# Add the "End date" key after the "Start date" key or update it
		key_value = {
			"key": self.Date.language_texts["end_date"],
			"value": video["Date"]
		}

		# Define the after key as the "Start date" one
		after_key = self.Date.language_texts["start_date"]

		self.media["Item"]["Details"] = self.JSON.Add_Key_After_Key(self.media["Item"]["Details"], key_value, after_key = after_key)

		# ---------- #

		# Create a shortcut to the media item "Episode" key
		media_item_episode = self.media["Item"]["Details"][self.Language.language_texts["episode, title()"]]

		# Create a shortcut to the last episode
		last_episode = self.media["Item"]["Episodes"]["Titles"][self.media["Language"]][-1]

		# If the media item episode is the last episode
		if media_item_episode == last_episode:
			# Update the "Episode" key of the media item details to change it to the new episode
			key_value = {
				"key": self.Language.language_texts["episode, title()"],
				"value": video["Titles"][self.media["Language"]]
			}

			# Define the after key as the "Episodes" one
			after_key = self.language_texts["episodes, title()"]

			self.media["Item"]["Details"] = self.JSON.Add_Key_After_Key(self.media["Item"]["Details"], key_value, after_key = after_key)

		# Update the "Episodes" key of the media item details to change it to the new number of episodes
		key = self.language_texts["episodes, title()"]

		self.media["Item"]["Details"][key] = self.videos["Numbers"]["Total"]

		# Transform the media item details dictionary into a text string
		media_item_details = self.Text.From_Dictionary(self.media["Item"]["Details"])

		# Update the media item "Details.txt" file with the updated media item details dictionary
		self.File.Edit(self.media["Item"]["Folders"]["details"], media_item_details, "w")

		# ---------- #

		# Populate the media (item) episode files
		self.Populate_The_Files()

		# ---------- #

		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Show the YouTube channel name
		print(self.Text.Capitalize(self.language_texts["youtube_channel"]) + ":")
		print("[" + self.media["Title"] + "]")
		print()

		# If the media item title is not the same as the media title
		if self.media["Item"]["Title"] != self.media["Title"]:
			# Show the video series text
			text = self.language_texts["video_series, type: singular, capitalize()"]

			# Show the video series title
			print(text + ":")
			print("[" + self.media["Item"]["Title"] + "]")
			print()

		# Iterate through the language keys and dictionaries
		for small_language, language in self.languages["Dictionary"].items():
			# Get the current language translated to the user language
			translated_language = language["Translated"][self.language["Small"]]

			# Define the translated language text as "Title of the video in {}" formatted with the translated language
			translated_language_text = self.Language.language_texts["title_of_the_video_in_{}"].format(translated_language)

			# Show the the translated language text
			print(translated_language_text + ":")

			# Show the video title in the current language
			print("[" + video["Titles"][small_language] + "]")
			print()

		# Show the video ID
		print(self.language_texts["video_id"] + ":")
		print("[" + video["ID"] + "]")
		print()

		# Show the video date
		print(self.language_texts["video_date"] + ":")
		print("[" + video["Date"] + "]")