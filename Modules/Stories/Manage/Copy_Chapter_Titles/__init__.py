# Copy_Chapter_Titles.py

from Stories.Stories import Stories as Stories

class Copy_Chapter_Titles(Stories):
	def __init__(self, story = None):
		super().__init__(story = story)

		# Select the language
		show_text = self.JSON.Language.language_texts["languages, title()"]
		select_text = self.JSON.Language.language_texts["language, title()"]

		translated_languages = []

		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language][self.user_language]

			translated_languages.append(translated_language)

		language = self.Input.Select(self.languages["small"], language_options = translated_languages, show_text = show_text, select_text = select_text)["option"]

		# Get the translated language
		translated_language = self.languages["full_translated"][language][self.user_language]

		# Show the translated language
		print()
		print(self.large_bar)
		print()
		print(translated_language + ":")
		print()

		# Get the chapter titles list
		chapter_titles = self.story["Information"]["Chapter titles"][language]

		# Iterate through the chapter titles list
		i = 1
		for title in chapter_titles:
			# Add the chapter number and separator to the chapter title
			title = str(i) + " - " + title

			# Show the chapter number and title
			print("-")
			print()
			print(str(i) + "/" + str(len(chapter_titles)) + ":")
			print("[" + title + "]")

			# Copy the chapter title with the chapter number
			self.Text.Copy(title, verbose = False)

			input()

			i += 1

		print(self.large_bar)
		print()
		print(self.language_texts["you_finished_copying_the_chapter_titles_of_this_story"] + ":")
		print(self.story["Titles"][self.user_language])