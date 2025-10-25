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
			for language in self.languages["Small"]:
				translated_language = self.languages["Full (translated)"][language][self.language["Small"]]

				print("\t" + translated_language + ":")
				print("\t" + story["Titles"][language])
				print()

			# Iterate through the information items in the "Information items" dictionary
			for key, information_item in self.stories["Information items"]["Dictionary"].items():
				# Define the text dictionary of the information item
				text = information_item["Texts"]

				# If the information item is "Author"
				# And the number of authors is more than one
				if (
					key == "Author" and
					len(story["Information"]["Authors"]) > 1
				):
					# Use the "Plural texts" as a text dictionary
					text = information_item["Plural texts"]

				# Get the text in the user language
				text = text[self.language["Small"]]

				# Show the text
				print(text + ":")

				# If the information item key is not the "Synopsis" one
				if key != "Synopsis":
					# Get the information inside the "Story" dictionary
					information = story["Information"][key]

					# If the key is "Author"
					if key == "Author":
						# Define the information as the "Authors" key
						information = story["Information"]["Authors"]

					# If the user language is inside the information, get it
					if self.language["Small"] in information:
						information = information[self.language["Small"]]

					# If the type of the information is not a dictionary
					if type(information) != dict:
						# If the type of the information is not a list
						if type(information) != list:
							# Show the information with a tab
							print("\t" + information)

						# If the type of the information is a list
						if type(information) == list:
							# Iterate through the items in the list
							for item in information:
								# Show the item with a tab
								print("\t" + item)

					# If the type of the information is a dictionary
					if type(information) == dict:
						# Iterater through the values inside the dictionary
						for item in information.values():
							# If the type of the item is a dictionary
							# And the user language is present in that dictionary
							if (
								type(item) == dict and
								self.language["Small"] in item
							):
								# Get the user language value
								item = item[self.language["Small"]]

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
					for line in story["Information"][key][self.language["Small"]].splitlines():
						print("\t" + line)

				print()

			# Show the chapters of the story if they exist
			if story["Information"]["Chapters"]["Numbers"]["Total"] != 0:
				print(self.Language.language_texts["chapters, title()"] + ":")

				# Show the number of chapters
				print("\t" + self.Language.language_texts["number, title()"] + ":")
				print("\t\t" + str(story["Information"]["Chapters"]["Numbers"]["Total"]))
				print()

				# Show the titles of the chapters in the user language with their numbers
				print("\t" + self.Language.language_texts["titles, title()"] + ":")

				t = 1
				for title in story["Information"]["Chapters"]["Titles"][self.language["Small"]]:
					print("\t\t" + str(t) + " - " + title)

					t += 1

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
			print("\t" + story["Information"]["Links"]["Website"]["Link"])
			print()

			# Iterate through the list of story websites
			for key in self.stories["Story websites"]["List"]:
				# If the story website IDs dictionary is not empty
				if story["Information"]["Links"][key]["IDs"] != {}:
					# Show the name of the story website
					print(key + ":")

					# Show the story website information of the story
					for language in self.languages["Small"]:
						# Get the translated language
						translated_language = self.languages["Full (translated)"][language][self.language["Small"]]

						# Get the item (link)
						item = story["Information"]["Links"][key]

						# Define the sub-key
						sub_key = "Links"

						# If the story website is "Wattpad"
						if key == "Wattpad":
							sub_key = "Read story"

						# Get the language link
						item = item[sub_key][language]

						# Show the link in the current language
						# With the translated language
						print("\t" + translated_language + ":")
						print("\t" + item)

						# If the language is not the last one
						if language != self.languages["Small"][-1]:
							# Show a space separator
							print()

					print()

		# Show a five dash space separator
		print(self.separators["5"])