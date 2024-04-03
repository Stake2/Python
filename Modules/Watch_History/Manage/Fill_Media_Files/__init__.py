# Fill_Media_Files.py

from Watch_History.Watch_History import Watch_History as Watch_History

from Watch_History.Watch_Media import Watch_Media

class Fill_Media_Files(Watch_History):
	def __init__(self, dictionary = None):
		super().__init__()

		self.dictionary = dictionary

		options = {
			"Media type": {
				"Status": self.texts["statuses, type: list"]["en"],

				# Remove the "Movies" media type from the media type dictionary, returning a local media types dictionary
				"List": self.Remove_Media_Type(self.texts["movies, title()"]["en"])
			}
		}

		self.dictionary_is_none = False

		if self.dictionary == None:
			# Ask user to select media type and media
			self.dictionary = self.Select_Media_Type_And_Media(options, watch = True, select_media_item = True)

			self.dictionary_is_none = True

		self.media = self.dictionary["Media"]

		# Define the "Fill episode titles" dictionary
		self.dictionary["Fill episode titles"] = {
			"Episodes": {
				"Numbers": {
					"Total": 0
				},
				**self.media["Item"]["Episodes"]
			}
		}

		print()
		print("-----")

		methods = {
			"Fill_Files": self.language_texts["fill_titles_files"]
		}

		if self.media["States"]["Video"] == True:
			methods["Add_To_Videos_List"] = self.language_texts["add_to_videos_list"]

			# Get the keys and values
			for name in ["keys", "values"]:
				methods[name] = list(getattr(methods, name)())

			# Add methods to method keys
			for method in methods.copy():
				if method not in ["keys", "values"]:
					methods[method] = getattr(self, method)

			if self.dictionary_is_none == True:
				# Select the method
				selected_method = self.Input.Select(methods["keys"], language_options = methods["values"])["option"]

				method = methods[selected_method]

				if selected_method == "Fill_Files":
					self.Define_Variables()

				method()

		if self.media["States"]["Video"] == False:
			if (
				list(methods.keys()) == ["Fill_Files"] or
				"Added media" in self.dictionary
			):
				self.Define_Variables()

		# Select the media again to update the media files
		self.dictionary = self.Select_Media(self.dictionary)
		self.media = self.dictionary["Media"]

		from copy import deepcopy

		# Select the media item again to update the media item files
		self.dictionary.update(self.Define_Media_Item(deepcopy(self.dictionary), media_item = self.media["Item"]["Title"]))

	def Define_Variables(self):
		print()
		print(self.separators["5"])
		print()

		key = "filling_the_titles_files"

		if (
			self.media["States"]["Video"] == True and
			self.media["States"]["Media item list"] == True
		):
			key = "filling_the_files_of_titles_and_youtube_ids"

		print(self.language_texts[key] + "...")

		# Show the files of episode titles per language
		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language][self.user_language]

			print()
			print(self.JSON.Language.language_texts["titles_file_in_{}"].format(translated_language) + ":")
			print("\t" + self.dictionary["Fill episode titles"]["Episodes"]["Titles"]["Files"][language])

		if (
			self.media["States"]["Video"] == True and
			self.media["States"]["Media item list"] == True
		):
			print()
			print(self.JSON.Language.language_texts["ids_file"] + ":")
			print("\t" + self.media["Item"]["Folders"]["titles"]["ids"])

		if self.media["States"]["Video"] == False:
			self.dictionary["Fill episode titles"]["Episodes"]["Numbers"]["Total"] = ""

			# Define the error variable so the "while" works
			error = True

			# Try to ask for the total episode number of all media items
			while error == True:
				# Ask for the total number of media item episodes
				self.dictionary["Fill episode titles"]["Episodes"]["Numbers"]["Total"] = self.Input.Type(self.language_texts["type_the_number_of_episodes"], accept_enter = False)

				# Try to convert input into integer, if it works, there is no error
				try:
					self.dictionary["Fill episode titles"]["Episodes"]["Numbers"]["Total"] = int(self.dictionary["Fill episode titles"]["Episodes"]["Numbers"]["Total"])

					error = False

				except ValueError:
					pass

			# -------------------------------------------------------------- #

			# If the media has a media list
			# And the media item is not the first one in the list
			if (
				self.media["States"]["Media item list"] == True and
				self.media["Item"]["Title"] != self.media["Items"]["List"][0]
			):
				self.dictionary["Fill episode titles"]["Episodes"]["Numbers"]["Total of all media episodes"] = ""

				# Define the error variable so the "while" works
				error = True

				# Try to ask for the total episode number of all media items
				while error == True:
					# Ask for the number of all media episodes
					self.dictionary["Fill episode titles"]["Episodes"]["Numbers"]["Total of all media episodes"] = self.Input.Type(self.language_texts["type_the_number_of_all_media_episodes"], accept_enter = False)

					# Try to convert input into integer, if it works, there is no error
					try:
						self.dictionary["Fill episode titles"]["Episodes"]["Numbers"]["Total of all media episodes"] = int(self.dictionary["Fill episode titles"]["Episodes"]["Numbers"]["Total of all media episodes"])

						error = False

					except ValueError:
						pass

				# Add one to the total episode number of all media items
				self.dictionary["Fill episode titles"]["Episodes"]["Numbers"]["Total of all media episodes"] += 1

			print()
			print("---")
			print()

			self.Fill_Files()

			print(self.language_texts["you_finished_filling_the_files_of_titles"] + ".")

		if (
			self.media["States"]["Video"] == True and
			self.media["States"]["Media item list"] == True
		):
			self.Get_YouTube_IDs()

			print()
			print(self.language_texts["you_finished_filling_the_files_of_titles_and_youtube_ids"] + ".")

	def Replace_Text(self, text):
		items_to_remove = [
			"(",
			")",
			"\t",
			'"'
		]

		if " " in text[0]:
			text = text[:1]

		if " " in text[-1]:
			text = text[:-1]

		if "  " in text:
			text = text.replace("  ", " ")

		for list_item in items_to_remove:
			if list_item in text:
				text = text.replace(list_item, "")

		return text

	def Fill_Files(self):
		if (
			self.media["States"]["Media item list"] == True and
			self.media["Item"]["Title"] != self.media["Items"]["List"][0]
		):
			total_number_text = str(self.dictionary["Fill episode titles"]["Episodes"]["Numbers"]["Total of all media episodes"] + self.dictionary["Fill episode titles"]["Episodes"]["Numbers"]["Total"] - 1)

		i = 1
		while i <= self.dictionary["Fill episode titles"]["Episodes"]["Numbers"]["Total"]:
			progress = str(i) + "/" + str(self.dictionary["Fill episode titles"]["Episodes"]["Numbers"]["Total"])

			# Add total episode number of all media items
			if (
				self.media["States"]["Media item list"] == True and
				self.media["Item"]["Title"] != self.media["Items"]["List"][0]
			):
				progress += " (" + str(self.Text.Remove_Leading_Zeroes(self.dictionary["Fill episode titles"]["Episodes"]["Numbers"]["Total of all media episodes"]))

				progress += "/" + total_number_text + ")"

			progress += ":"

			# Show episode number and progress
			print(progress)
			print()

			# Ask for episode titles per language
			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				# Define the translated language
				translated_language = self.languages["full_translated"][language][self.user_language]

				if language not in self.dictionary["Fill episode titles"]["Episodes"]["Titles"]:
					# Create episode titles language list
					self.dictionary["Fill episode titles"]["Episodes"]["Titles"][language] = []

				# Define the full episode title as the "EP" text and the current episode number
				episode_title = "EP" + str(self.Text.Add_Leading_Zeroes(i))

				# Also add the total episode number of all media items if the media has a media item list
				if (
					self.media["States"]["Media item list"] == True and
					self.media["Item"]["Title"] != self.media["Items"]["List"][0]
				):
					episode_title += "(" + str(self.Text.Add_Leading_Zeroes(self.dictionary["Fill episode titles"]["Episodes"]["Numbers"]["Total of all media episodes"])) + ")"

				first_space = True

				if language == self.languages["small"][0]:
					first_space = False

				if self.switches["testing"] == False:
					# Ask for the episode title
					typed_text = self.Input.Type(self.language_texts["paste_the_episode_title_in_{}"].format("[" + translated_language + "]"), accept_enter = False, next_line = True, first_space = first_space)

				if self.switches["testing"] == True:
					typed_text = self.texts["episode_title"][language] + " " + self.JSON.Language.language_texts["genders, type: dict"]["in"] + " " + full_language

				# Remove some texts from the episode title and add quotes
				typed_text = '"' + self.Replace_Text(typed_text) + '"'

				# Add the episode title to the full episode title
				episode_title = episode_title + " " + typed_text

				print()
				print([episode_title])

				self.dictionary["Fill episode titles"]["Episodes"]["Titles"][language].append(episode_title)

				if language == self.languages["small"][-1]:
					print()

			print("---")
			print()

			if (
				self.media["States"]["Media item list"] == True and
				self.media["Item"]["Title"] != self.media["Items"]["List"][0]
			):
				self.dictionary["Fill episode titles"]["Episodes"]["Numbers"]["Total of all media episodes"] += 1

			i += 1

		if self.media["States"]["Video"] == False:
			for language in self.languages["small"]:
				# Define the translated language
				translated_language = self.languages["full_translated"][language][self.user_language]

				# Show language and episode titles
				if language != self.languages["small"][0]:
					print()

				print(translated_language + ":")

				for title in self.dictionary["Fill episode titles"]["Episodes"]["Titles"][language]:
					print("\t" + title)

				if language == self.languages["small"][-1]:
					print()

				# Define the episode titles file
				file = self.dictionary["Fill episode titles"]["Episodes"]["Titles"]["Files"][language]

				# Write the episode titles to the episode titles file
				text = self.Text.From_List(self.dictionary["Fill episode titles"]["Episodes"]["Titles"][language])

				self.File.Edit(file, text, "w")

	def Get_YouTube_IDs(self):
		# If the IDs list is empty, get the video IDs and titles from the playlist
		if self.media["Item"]["Episodes"]["Titles"]["IDs"] == []:
			# Define the API dictionary
			youtube = {
				"item": "playlistItems",
				"id": self.media["Item"]["Details"][self.JSON.Language.language_texts["origin_location"]]
			}

			# Get the videos dictionary from the playlist
			videos = self.Get_YouTube_Information(youtube)

		# Else, make a video dictionary with the existing IDs and titles
		else:
			videos = {}

			i = 0
			for id in self.media["Item"]["Episodes"]["Titles"]["IDs"]:
				videos[id] = {
					"Title": self.media["Item"]["Episodes"]["Titles"][self.user_language][i],
					"ID": id
				}

				i += 1

		# Remove the private videos
		i = 1
		for id in videos.copy():
			video = videos[id]

			if video["Title"] == "Private video":
				videos.pop(id)

		# Write the IDs into the IDs file
		file = self.media["Item"]["Folders"]["titles"]["ids"]

		self.File.Edit(file, self.Text.From_List(videos.keys()), "w")

		# Get all video titles in the user language
		titles = []

		for id in videos:
			video = videos[id]

			titles.append(video["Title"])

		self.dictionary["Fill episode titles"]["Episodes"]["Titles"][self.user_language] = titles

		# Write the user language video title into the user language file
		file = self.media["Item"]["Folders"]["titles"][self.user_language]

		self.File.Edit(file, self.Text.From_List(titles), "w")

		i = 1
		keys = list(videos.keys())

		for id in videos:
			video = videos[id]

			# Add the video id to the IDs list
			if id not in self.media["Item"]["Episodes"]["Titles"]["IDs"]:
				self.media["Item"]["Episodes"]["Titles"]["IDs"].append(id)

			print()
			print(self.separators["5"])
			print()

			# Show video number and progress
			print(self.JSON.Language.language_texts["number, title()"] + ":")
			print("[" + str(i) + "/" + str(len(keys)) + "]")
			print()

			# Add to the language episode titles list
			for language in self.languages["small"]:
				# If the language is not the user language
				if language != self.user_language:
					# If the language title was not translated already
					if len(self.dictionary["Fill episode titles"]["Episodes"]["Titles"][language]) < i:
						# Define the translated language
						translated_language = self.languages["full_translated"][language][self.user_language]

						video["Title"] = self.Add_Missing_Titles(language, self.dictionary["Fill episode titles"]["Episodes"]["Titles"], video["Title"])

						self.dictionary["Fill episode titles"]["Episodes"]["Titles"][language].append(video["Title"])

						# Write the language video title into the language file
						file = self.media["Item"]["Folders"]["titles"][language]

						self.File.Edit(file, video["Title"], "a")

					# If it was translated, skip it
					else:
						print(self.JSON.Language.language_texts["title, title()"] + ":")
						print("[" + video["Title"] + "]")
						print("[" + self.dictionary["Fill episode titles"]["Episodes"]["Titles"][language][i - 1] + "]")
						print()

						print(self.language_texts["skipping_this_title_as_it_was_already_translated"] + ".")

			i += 1

		print()
		print(self.separators["5"])		

		# Show the language titles
		if len(self.dictionary["Fill episode titles"]["Episodes"]["Titles"][self.user_language]) < 10:
			print()

			for language in self.languages["small"]:
				# Define the translated language
				translated_language = self.languages["full_translated"][language][self.user_language]

				# Show the titles
				print(self.JSON.Language.language_texts["titles_in_{}"].format(translated_language) + ":")

				for title in self.dictionary["Fill episode titles"]["Episodes"]["Titles"][language]:
					print("\t" + title)

				print()

			# Show the IDs
			print(self.JSON.Language.language_texts["ids, title()"] + ":")

			for id in self.media["Item"]["Episodes"]["Titles"]["IDs"]:
				print("\t" + id)

	def Add_To_Videos_List(self):
		video_id = self.Input.Type(self.JSON.Language.language_texts["id, upper()"])

		import validators

		while validators.url(video_id) != True:
			video_id = self.Input.Type(self.JSON.Language.language_texts["id, upper()"])

		print()

		if "youtube" in video_id:
			from urllib.parse import urlparse, parse_qs

			link = urlparse(video_id)
			query = link.query
			parameters = parse_qs(query)
			video_id = parameters["v"][0]

		# Define the API dictionary
		youtube = {
			"item": "video",
			"id": video_id
		}

		# Get the video dictionary
		video = self.Get_YouTube_Information(youtube, remove_unused_keys = False)

		# Define language episode titles
		for language in self.languages["small"]:
			video["Title"] = self.Add_Missing_Titles(language, self.dictionary["Fill episode titles"]["Episodes"]["Titles"], video["Title"])

			self.dictionary["Fill episode titles"]["Episodes"]["Titles"][language] = video["Title"]

		# Add the video ID to the IDs list
		self.File.Edit(self.media["Item"]["Folders"]["titles"]["ids"], video_id, "a")

		# Write into language titles file
		for language in self.languages["small"]:
			title = self.dictionary["Fill episode titles"]["Episodes"]["Titles"][language]

			self.File.Edit(self.media["Item"]["Episodes"]["Titles"]["Files"][language], title, "a")

		video["Date"] = self.Date.From_String(video["Date"])["Formats"]["HH:MM DD/MM/YYYY"]

		# Add the "End date" key after the "Start date" key or update it
		key_value = {
			"key": self.Date.language_texts["end_date"],
			"value": video["Date"]
		}

		self.media["Item"]["Details"] = self.JSON.Add_Key_After_Key(self.media["Item"]["Details"], key_value, after_key = self.Date.language_texts["start_date"])

		if self.media["Item"]["Details"][self.JSON.Language.language_texts["episode, title()"]] == self.media["Item"]["Episodes"]["Titles"][self.media["Language"]][-1]:
			# Update the "Episode" key of the media item details
			key_value = {
				"key": self.JSON.Language.language_texts["episode, title()"],
				"value": self.dictionary["Fill episode titles"]["Episodes"]["Titles"][self.media["Language"]]
			}

			self.media["Item"]["Details"] = self.JSON.Add_Key_After_Key(self.media["Item"]["Details"], key_value, after_key = self.language_texts["episodes, title()"])

		# Update the media item details file
		self.File.Edit(self.media["Item"]["Folders"]["details"], self.Text.From_Dictionary(self.media["Item"]["Details"]), "w")

		print()
		print("-----")
		print()
		print(self.Text.Capitalize(self.language_texts["youtube_channel"]) + ":")
		print("\t" + self.media["Title"])
		print()
		print(self.Text.Capitalize(self.language_texts["video_serie"]) + ":")
		print("\t" + self.media["Item"]["Title"])
		print()

		# Show the video titles
		for language in self.languages["small"]:
			# Define the translated language
			translated_language = self.languages["full_translated"][language][self.user_language]

			print(self.JSON.Language.language_texts["title_in_{}"].format(translated_language) + ":")
			print("\t" + self.dictionary["Fill episode titles"]["Episodes"]["Titles"][language])
			print()

		# Show the video ID
		print(self.JSON.Language.language_texts["id, upper()"] + ":")
		print("\t" + video_id)
		print()

		# Show the video date
		print(self.Date.language_texts["date, title()"] + ":")
		print("\t" + video["Date"])

		print()
		print("-----")

	def Add_Missing_Titles(self, language, titles, title):
		# Define the translated language
		translated_language = self.languages["full_translated"][language][self.user_language]

		if language not in titles:
			titles[language] = ""

		if language != self.media["Language"]:
			# Show the information text about translating the title
			print(self.language_texts["please_translate_this_title_to_{}"].format(translated_language) + ":")
			print("[" + title + "]")

			# Copy the user language title
			self.Text.Copy(title)

			# Ask for the user to type or paste the translated title
			title = self.Input.Type(self.JSON.Language.language_texts["title, title()"] + ": ", accept_enter = False)

		return title