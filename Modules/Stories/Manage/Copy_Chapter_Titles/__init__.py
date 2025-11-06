# Copy_Chapter_Titles.py

from Stories.Stories import Stories as Stories

class Copy_Chapter_Titles(Stories):
	def __init__(self):
		super().__init__()

		# Define the states dictionary
		self.states = {
			"Select language": False
		}

		# Show a five dash space separator
		print(self.separators["5"])

		# Ask the user if it wants to select a language
		type_text = self.Language.language_texts["select_a_language, type: question"]

		self.states["Select language"] = self.Input.Yes_Or_No(type_text)

		# Define the translated language for the chapter titles
		translated_language = ""

		# Define a local list of languages
		languages = []

		# If the user did not selected a custom language
		if self.states["Select language"] == False:
			# Define the local list of languages as the root list of small languages
			languages = self.languages["Small"]

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
			small_language = self.Input.Select(self.languages["Small"], language_options = translated_languages, show_text = show_text, select_text = select_text)["Option"]["Normal"]

			# Add the small language to the languages list
			languages.append(small_language)

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

		# Get the chapter "Titles" dictionary
		chapter_titles = self.story["Information"]["Chapters"]["Titles"]

		# Iterate through the English chapter titles list
		i = 1
		for title in chapter_titles["en"]:
			# Show a three dash space separator
			print(self.separators["3"])
			print()

			# Show the current and total chapter numbers
			print(self.language_texts["chapter_number"] + ":")
			print("[" + str(i) + "/" + str(len(chapter_titles["en"])) + "]")
			print()

			# Iterate through the small languages list
			for language in languages:
				# Get the chapter title in the current language
				title = chapter_titles[language][i - 1]

				# Add the chapter number and separator to the chapter title
				edited_title = str(i) + " - " + title

				# Show the chapter title in the current language
				print(self.Language.texts["title_in_language"][language][self.language["Small"]] + ":")
				print("[" + edited_title + "]")

				# Copy the chapter title with the chapter number
				self.Text.Copy(edited_title, verbose = False)

				# Ask for user input on chapter titles that are not the last one
				if title != chapter_titles["en"][-1]:
					input()

				# Show a space separator if the chapter title is the last one
				if title == chapter_titles["en"][-1]:
					print()

			i += 1

		# Show a five dash space separator and a space separator
		print(self.separators["5"])
		print()

		# Show the information text with the story title in the user language
		print(self.language_texts["you_finished_copying_the_chapter_titles_of_this_story"] + ":")
		print(self.story["Titles"][self.language["Small"]])
		print()

		# Show a five dash space separator
		print(self.separators["5"])