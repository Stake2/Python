# Copy_Chapter_Titles.py

from Stories.Stories import Stories as Stories

class Copy_Chapter_Titles(Stories):
	def __init__(self):
		# Run the root class to import its methods and variables
		super().__init__()

		# If there is no selected story in the current class
		if hasattr(self, "story") == False:
			# Select the story
			self.story = self.Select_Story()

		# Define the root "copy" dictionary
		self.copy = {
			"Languages": [],
			"Chapter titles": self.story["Chapters"]["Lists"]["Titles"]
		}

		# Define the states dictionary
		self.states = {
			"Select language": False
		}

		# Select a language
		self.Select_Language()

		# Copy the chapter titles
		self.Copy_Titles()

	def Select_Language(self):
		# Show a five dash space separator
		print()
		print(self.separators["5"])

		# Ask the user if it wants to select a language
		type_text = self.Language.language_texts["select_a_language, type: question"]

		self.states["Select language"] = self.Input.Yes_Or_No(type_text)

		# Define the translated language for the chapter titles
		translated_language = ""

		# If the user did not selected a custom language
		if self.states["Select language"] == False:
			# Define the list of languages as the root list of small languages
			self.copy["Languages"] = self.languages["Small"]

		# If the user wants to select a language
		if self.states["Select language"] == True:
			# Define the show and select texts
			show_text = self.Language.language_texts["languages, title()"]
			select_text = self.Language.language_texts["language, title()"]

			# Create the list of translated languages in the user language
			translated_languages = []

			# Iterate through the language keys and dictionaries
			for small_language, language in self.languages["Dictionary"].items():
				# Get the current language translated to the user language
				translated_language = language["Translated"][self.language["Small"]]

				# Add it to the list
				translated_languages.append(translated_language)

			# Ask the user to select the small language
			small_language = self.Input.Select(self.languages["Small"], language_options = translated_languages, show_text = show_text, select_text = select_text)["Option"]["Original"]

			# Add the small language to the languages list
			self.copy["Languages"].append(small_language)

			# Get the language dictionary
			language = self.languages["Dictionary"][small_language]

			# Get the translated language
			translated_language = language["Translated"][self.language["Small"]]

			# Show some space separators and a five dash space separator
			print()
			print(self.separators["5"])
			print()

			# Show the translated language selected
			print(translated_language + ":")
			print()

	def Copy_Titles(self):
		# Define a shortcut to the total chapters number
		total_chapters_number = self.story["Chapters"]["Numbers"]["Total"]

		# Iterate through the English chapter titles list
		for chapter_number, english_chapter_title in enumerate(self.copy["Chapter titles"]["en"], start = 1):
			# Show a three dash space separator
			print(self.separators["3"])
			print()

			# Show the current and total chapter numbers
			print(self.language_texts["chapter_number"] + ":")
			print("[" + str(chapter_number) + "/" + str(total_chapters_number) + "]")
			print()

			# Iterate through the local list of small languages
			for language in self.copy["Languages"]:
				# Get the chapter title in the current language
				language_chapter_title = self.copy["Chapter titles"][language][chapter_number - 1]

				# Create the chapter title with number
				chapter_title_with_number = str(chapter_number) + " - " + language_chapter_title

				# Show the chapter title in the current language
				print(self.Language.texts["title_in_language"][language][self.language["Small"]] + ":")
				print("[" + chapter_title_with_number + "]")

				# Copy the chapter title with the number
				self.Text.Copy(chapter_title_with_number, verbose = False)

				# Ask for user input on chapter titles that are not the last one
				if english_chapter_title != self.copy["Chapter titles"]["en"][-1]:
					self.Input.Type(self.Language.language_texts["continue, title()"])

					print()

				# Show a space separator if the chapter title is the last one
				if english_chapter_title == self.copy["Chapter titles"]["en"][-1]:
					print()

		# Show a five dash space separator and a space separator
		print(self.separators["5"])
		print()

		# Show the information text with the story title in the user language
		print(self.language_texts["you_finished_copying_the_chapter_titles_of_this_story"] + ":")
		print(self.story["Titles"][self.language["Small"]])
		print()

		# Show a five dash space separator
		print(self.separators["5"])