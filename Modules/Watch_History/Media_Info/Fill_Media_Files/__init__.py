# Fill_Media_Files.py

from Watch_History.Watch_History import Watch_History as Watch_History

from Watch_History.Watch_Media import Watch_Media

class Fill_Media_Files(Watch_History):
	def __init__(self, option_info = None):
		super().__init__()

		options = {
			"media_type": {
				"status": self.texts["watching_statuses, type: list"]["en"],
				"list": {}
			}
		}

		# Remove the "Movies" media type from the media type dictionary, returning a local media types dictionary
		options["media_type"]["list"] = self.Remove_Media_Type(self.texts["movies, title()"]["en"])["list"]

		# Ask user to select media type and media
		self.dictionary = self.Select_Media_Type_And_Media(options, watch = True, select_media_item = True)

		# Define the "Fill episode titles" dictionary
		self.dictionary["Fill episode titles"] = {
			"Episodes": {
				"Numbers": {
					"Total": 0
				},
				**self.dictionary["Media"]["item"]["episodes"],
				"Titles": {}
			}
		}

		print()
		print("-----")

		self.Define_Variables()
		self.Fill_Files()

		if self.dictionary["Media"]["States"]["video"] == True and self.dictionary["Media"]["States"]["Media item list"] == True:
			self.Get_YouTube_IDs()

	def Define_Variables(self):
		print()

		key = "filling_the_episode_titles_files"

		if self.dictionary["Media"]["States"]["video"] == True and self.dictionary["Media"]["States"]["Media item list"] == True:
			key = "filling_the_files_of_episode_titles_and_youtube_ids"

		print(self.language_texts[key] + "...")

		key = "episode_titles_file_in_{}"

		if self.dictionary["Media"]["States"]["video"] == True and self.dictionary["Media"]["States"]["Media item list"] == True:
			key = "video_titles_file_in_{}"

		# Show episode titles' files per language
		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language][self.user_language]

			print()
			print(self.language_texts[key].format(translated_language) + ":")
			print(self.dictionary["Fill episode titles"]["Episodes"]["titles"]["files"][language])

		if self.dictionary["Media"]["States"]["video"] == True and self.dictionary["Media"]["States"]["Media item list"] == True:
			print()
			print(self.JSON.Language.language_texts["ids_file"] + ":")
			print(self.dictionary["Media"]["item"]["folders"]["titles"]["ids"])

		if self.dictionary["Media"]["States"]["video"] == False:
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

			# If the media has a media list and the media item is not the first one in the list
			if self.dictionary["Media"]["States"]["Media item list"] == True and self.dictionary["Media"]["item"]["title"] != self.dictionary["Media"]["items"]["list"][0]:
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

	def Replace_Text(self, text):
		items_to_remove = [
			"(",
			")",
			"\t",
			'"',
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
		if self.dictionary["Media"]["States"]["Media item list"] == True and self.dictionary["Media"]["item"]["title"] != self.dictionary["Media"]["items"]["list"][0]:
			total_number_text = str(self.dictionary["Fill episode titles"]["Episodes"]["Numbers"]["Total of all media episodes"] + self.dictionary["Fill episode titles"]["Episodes"]["Numbers"]["Total"] - 1)

		i = 1
		while i <= self.dictionary["Fill episode titles"]["Episodes"]["Numbers"]["Total"]:
			progress = str(i) + "/" + str(self.dictionary["Fill episode titles"]["Episodes"]["Numbers"]["Total"])

			# Add total episode number of all media items
			if self.dictionary["Media"]["States"]["Media item list"] == True and self.dictionary["Media"]["item"]["title"] != self.dictionary["Media"]["items"]["list"][0]:
				progress += " (" + str(self.Text.Add_Leading_Zeroes(self.dictionary["Fill episode titles"]["Episodes"]["Numbers"]["Total of all media episodes"]))

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
				if self.dictionary["Media"]["States"]["Media item list"] == True and self.dictionary["Media"]["item"]["title"] != self.dictionary["Media"]["items"]["list"][0]:
					episode_title += "(" + str(self.Text.Add_Leading_Zeroes(self.dictionary["Fill episode titles"]["Episodes"]["Numbers"]["Total of all media episodes"])) + ")"

				first_space = True

				if language == self.languages["small"][0]:
					first_space = False

				if self.switches["testing"] == False:
					# Ask for the episode title
					typed_text = self.Input.Type(self.language_texts["paste_the_episode_title_in_{}"].format("[" + translated_language + "]"), accept_enter = False, next_line = True, first_space = first_space)

				if self.switches["testing"] == True:
					typed_text = self.texts["episode_title"][language] + " " + full_language

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

			if self.dictionary["Media"]["States"]["Media item list"] == True and self.dictionary["Media"]["item"]["title"] != self.dictionary["Media"]["items"]["list"][0]:
				self.dictionary["Fill episode titles"]["Episodes"]["Numbers"]["Total of all media episodes"] += 1

			i += 1

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
			file = self.dictionary["Fill episode titles"]["Episodes"]["titles"]["files"][language]

			# Write the episode titles to the episode titles file
			text = self.Text.From_List(self.dictionary["Fill episode titles"]["Episodes"]["Titles"][language])

			self.File.Edit(file, text, "w")

		print(self.language_texts["finished_filling_episode_titles_files"] + ".")

	def Get_YouTube_IDs(self):
		# Define empty IDs list
		self.dictionary["Media"]["item"]["episodes"]["ids"] = []

		# Define API dictionary
		youtube = {
			"item": "playlistItems",
			"id": self.dictionary["Media"]["item"]["details"][self.language_texts["origin_location"]]
		}

		# Get videos dictionary from playlist
		videos = self.Get_YouTube_Information(youtube)

		print()

		# Remove private videos
		i = 1
		for id in videos.copy():
			video = videos[id]

			if video["Title"] == "Private video":
				videos.pop(id)

		i = 1
		for id in videos:
			video = videos[id]

			# Add ID to IDs list
			self.dictionary["Media"]["item"]["episodes"]["ids"].append(id)

			# Show video number and progress
			print(str(i) + "/" + str(len(list(videos.keys()))) + ":")
			print()

			# Add to language episode titles list
			for language in self.languages["small"]:
				# Define the translated language
				translated_language = self.languages["full_translated"][language][self.user_language]

				if language not in self.dictionary["Fill episode titles"]["Episodes"]["Titles"]:
					self.dictionary["Fill episode titles"]["Episodes"]["Titles"][language] = []

				if language != self.dictionary["Media"]["Language"]:
					print(self.language_texts["please_translate_this_title_to_{}"].format(translated_language) + ":")
					print(video["Title"])
					self.Text.Copy(video["Title"])

					video["Title"] = self.Input.Type(self.JSON.Language.language_texts["title, title()"] + ": ")

					if id != list(videos.keys())[-1]:
						print()
						print("---")
						print()

				self.dictionary["Fill episode titles"]["Episodes"]["Titles"][language].append(video["Title"])

				i += 1

		# Write into language titles file
		for language in self.languages["small"]:
			# Define the translated language
			translated_language = self.languages["full_translated"][language][self.user_language]

			text = self.Text.From_List(self.dictionary["Fill episode titles"]["Episodes"]["Titles"][language])

			self.File.Edit(self.dictionary["Media"]["item"]["episodes"]["titles"]["files"][language], text)

			# Show titles
			print(self.language_texts["video_titles_in_{}"].format(translated_language) + ":")

			for title in self.dictionary["Fill episode titles"]["Episodes"]["Titles"][language]:
				print("\t" + title)

			print()

		# Write into "IDs.txt" file
		text = self.Text.From_List(self.dictionary["Media"]["item"]["episodes"]["ids"])

		self.File.Edit(self.dictionary["Media"]["item"]["folders"]["titles"]["ids"], text)

		# Show IDs
		print(self.JSON.Language.language_texts["ids, title()"] + ":")

		for id in self.dictionary["Media"]["item"]["episodes"]["ids"]:
			print("\t" + id)

		print()
		print(self.language_texts["finished_filling_the_files_of_episode_titles_and_youtube_ids"] + ".")