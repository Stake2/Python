# Show_Story_Information.py

from Stories.Stories import Stories as Stories

class Show_Story_Information(Stories):
	def __init__(self, stories_list = []):
		super().__init__()

		# Define the list of stories in the object of this class
		self.stories_list = stories_list

		# Show information about the stories
		self.Show_Information()

	def Show_Information(self):
		# If the list of stories is empty
		if self.stories_list == []:
			# Ask the user to select the story
			self.story = self.Select_Story()

			# Update the list of stories
			self.stories_list = [
				self.story["Title"]
			]

		# Iterate through the list of stories
		for story_title in self.stories_list:
			# Get the "Story" dictionary
			story = self.stories["Dictionary"][story_title]

			# Show space separators and a dash space separator
			print()
			print(self.separators["5"])
			print()

			# Show the "Story title:" text
			print(self.Language.language_texts["story_title"] + ":")

			# Show the titles of the story in all languages
			for language in self.languages["small"]:
				translated_language = self.languages["full_translated"][language][self.user_language]

				print("\t" + translated_language + ":")
				print("\t" + story["Titles"][language])
				print()

			# Iterate through the information items in the "Information items" dictionary
			for key, information_item in self.stories["Information items"]["Dictionary"].items():
				# Define the text of the information item
				text = information_item["Texts"][self.user_language]

				# Show the text
				print(text + ":")

				# If the information item key is not the "Synopsis" one
				if key != "Synopsis":
					# Get the information inside the "Story" dictionary
					information = story["Information"][key]

					# If the user language is inside the information, get it
					if self.user_language in information:
						information = information[self.user_language]

					# If the type of the information is not a dictionary, show the information with a tab
					if type(information) != dict:
						print("\t" + information)

					# If the type of the information is a dictionary
					if type(information) == dict:
						# Iterater through the values inside the dictionary
						for item in information.values():
							# If the type of the item is a dictionary
							# And the user language is present in that dictionary
							if (
								type(item) == dict and
								self.user_language in item
							):
								# Get the user language value
								item = item[self.user_language]

							# If the information item key not is "Status"
							# Or it is
							# And the type of the item is not a number
							if (
								key != "Status" or
								key == "Status" and
								type(item) != int
							):
								# Show the item with a tab, transforming the item into a text string
								print("\t" + str(item))

				# If the information item key is the "Synopsis" one
				if key == "Synopsis":
					# Show each line of the synopsis of the story in the user language
					for line in story["Information"][key][self.user_language].splitlines():
						print("\t" + line)

				print()

			# Show the folder of the story
			print(self.Folder.language_texts["folder, title()"] + ":")
			print("\t" + story["Folders"]["root"])
			print()

			# Show the website image folder of the story
			print(self.Language.language_texts["website_image_folder"] + ":")
			print("\t" + story["Folders"]["Covers"]["Websites"]["root"])
			print()

			# Show the link of the story
			print(self.Language.language_texts["website_link"] + ":")
			print("\t" + story["Information"]["Website"]["Link"])
			print()

			# If the "Wattpad" dictionary is not empty
			if story["Information"]["Wattpad"] != {}:
				# Show the "Wattpad:" text
				print("Wattpad:")

				# Show the Wattpad information of the story
				for language in story["Information"]["Wattpad"]:
					# Get the translated language
					translated_language = self.languages["full_translated"][language][self.user_language]

					# Get the item (link)
					item = story["Information"]["Wattpad"][language]

					# Show the link in the current language
					# With the translated language
					print("\t" + translated_language + ":")
					print("\t" + item["Link"])

					# If the language is not the last one from the list of Wattpad links
					if language != list(story["Information"]["Wattpad"].keys())[-1]:
						# Show a space separator
						print()

				print()

		# Show a five dash space separator
		print(self.separators["5"])