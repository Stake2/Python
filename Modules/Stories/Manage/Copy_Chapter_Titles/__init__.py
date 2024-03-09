# Copy_Chapter_Titles.py

from Stories.Stories import Stories as Stories

class Copy_Chapter_Titles(Stories):
	def __init__(self):
		super().__init__()

		# Define the States dictionary
		self.states = {
			"Select language": False
		}

		print(self.separators["5"])

		# Ask the user if it wants to select a language
		type_text = self.JSON.Language.language_texts["select_a_language, type: question"]

		self.states["Select language"] = self.Input.Yes_Or_No(type_text)

		translated_language = ""

		if self.states["Select language"] == True:
			# Define the show and select texts
			show_text = self.JSON.Language.language_texts["languages, title()"]
			select_text = self.JSON.Language.language_texts["language, title()"]

			# Create the translated languages list
			translated_languages = []

			for language in self.languages["small"]:
				translated_language = self.languages["full_translated"][language][self.user_language]

				translated_languages.append(translated_language)

			# Ask the user to select the language
			language = self.Input.Select(self.languages["small"], language_options = translated_languages, show_text = show_text, select_text = select_text)["option"]

			# Get the translated language
			translated_language = self.languages["full_translated"][language][self.user_language]

			# Show the translated language
			print()
			print(self.separators["5"])
			print()
			print(translated_language + ":")
			print()

		# Define the list of languages
		languages = []

		# Add the correct languages
		if translated_language == "":
			languages = self.languages["small"]

		else:
			languages.append(language)

		# Get the chapter titles dictionary
		chapter_titles = self.story["Information"]["Chapters"]["Titles"]

		# Iterate through the English chapter titles list
		i = 1
		for title in chapter_titles["en"]:
			# Show the chapter number
			print("---")
			print()
			print(self.language_texts["chapter_number"] + ":")
			print("[" + str(i) + "/" + str(len(chapter_titles["en"])) + "]")
			print()

			# Iterate through the small languages list
			for language in languages:
				# Get the chapter title in the current language
				title = chapter_titles[language][i - 1]

				# Add the chapter number and separator to the chapter title
				edited_title = str(i) + " - " + title

				# Show the chapter title
				print(self.JSON.Language.texts["title_in_language"][language][self.user_language] + ":")
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

		# Show the finish text with the story title
		print(self.separators["5"])
		print()
		print(self.language_texts["you_finished_copying_the_chapter_titles_of_this_story"] + ":")
		print(self.story["Titles"][self.user_language])
		print()
		print(self.separators["5"])