# Verify_Current_Year.py

from Years.Years import Years as Years

class Verify_Current_Year(Years):
	def __init__(self):
		super().__init__(select_year = False)

		self.Verify_Current_Year()

	def Verify_Current_Year(self):
		print()
		print("-----")
		print()

		self.folder_size = self.Folder.Contents(self.current_year["folder"])["size"]

		# Creates the new Year text and image folder, copies the Year template files to the text folder, and edits some of them
		if self.folder_size == 0:
			# Copy "Year Texts" folder to Current Year folder
			self.Folder.Copy(self.year_texts_contents["root"], self.current_year["folder"])

			# Copy "Year Images" folder to Current Year Image folder
			self.Folder.Copy(self.year_images_folder, self.current_year["image_folder"])

			# This Year I (post) file
			for language in self.small_languages:
				full_language = self.full_languages[language]

				self.this_year_i_post_file = self.current_year["folders"][full_language][self.texts["this_year_i_post"][language]]

				text_to_write = self.File.Contents(self.this_year_i_post_file)["string"]

				if "{current_year}" in text_to_write:
					text_to_write = text_to_write.replace("{current_year}", str(self.date["year"]))

				self.File.Edit(self.this_year_i_post_file, text_to_write, "w")

			# Christmas Texts file
			self.christmas_folder = self.current_year["folder"] + self.language_texts["christmas, en - " + self.user_language] + "/"
			self.christmas_texts_file = self.christmas_folder + self.language_texts["texts, en - " + self.user_language] + ".txt"

			text_to_write = self.File.Contents(self.christmas_texts_file)["string"]

			if "{current_year}" in text_to_write:
				text_to_write = text_to_write.replace("{current_year}", str(self.date["year"]))

			self.File.Edit(self.christmas_texts_file, text_to_write, "w")

			# New Year Texts file
			self.new_year_folder = self.current_year["folder"] + self.language_texts["new_year, en - " + self.user_language] + "/"
			self.new_year_texts_file = self.new_year_folder + self.language_texts["texts, en - " + self.user_language] + ".txt"

			text_to_write = self.File.Contents(self.new_year_texts_file)["string"]

			if "{next_year}" in text_to_write:
				text_to_write = text_to_write.replace("{next_year}", str(self.date["year"] + 1))

			self.File.Edit(self.new_year_texts_file, text_to_write, "w")

			# Created In file
			self.created_in_file = self.current_year["folder"] + self.language_texts["created_in, en - " + self.user_language] + ".txt"
			self.File.Edit(self.created_in_file, self.Date.Now()["strftime"], "w")

			# Edited In file
			self.edited_in_file = self.current_year["folder"] + self.language_texts["edited_in, en - " + self.user_language] + ".txt"
			self.File.Edit(self.edited_in_file, self.Date.Now()["strftime"], "w")

			# New Year posts folder
			self.new_year_posts_folder = self.new_year_folder + "Posts/"

			# Twitter posts file
			self.twitter_file = self.new_year_posts_folder + "Twitter.txt"

			text_to_write = self.File.Contents(self.twitter_file)["string"]

			if "{current_year}" in text_to_write:
				text_to_write = text_to_write.replace("{current_year}", str(self.date["year"]))

			self.File.Edit(self.twitter_file, text_to_write, "w")

			# WhatsApp, Instagram, and Facebook posts file
			self.whatsapp_instagram_facebook_file = self.new_year_posts_folder + "WhatsApp, Instagram, Facebook.txt"

			text_to_write = self.File.Contents(self.whatsapp_instagram_facebook_file)["string"]

			if "{current_year}" in text_to_write:
				text_to_write = text_to_write.replace("{current_year}", str(self.date["year"]))

			self.File.Edit(self.whatsapp_instagram_facebook_file, text_to_write, "w")

			self.sub_files = {
				self.language_texts["christmas, title()"]: self.christmas_file,
				self.language_texts["new_year"]: self.new_year_file,
			}

		# Tells the user that the current Year already exists in the Years folder
		text_to_show = self.language_texts["the_current_year_already_exists_in_the_years_folder"]

		# Tells the user that the current Year did not existed in the Years folder
		if self.folder_size == 0:
			text_to_show = self.language_texts["the_current_year_did_not_existed_in_the_years_folder"]

		print(text_to_show + ":")
		print(self.date["year"])
		print()

		text_to_show = self.language_texts["this_is_its_year_folder"]

		if self.folder_size == 0:
			text_to_show = self.language_texts["its_year_folder_was_created"]

		print(text_to_show + ":")
		print(self.current_year["folder"])
		print()

		print(self.language_texts["image_folder"] + ":")
		print(self.current_year["image_folder"])

		if self.folder_size == 0:
			print()

			for language_text in self.sub_files:
				file = self.sub_files[language_text]

				print(self.language_texts["{}_texts"].format(language_text) + ":")

				print("[")

				for line in self.File.Contents(file)["lines"]:
					print("\t" + line)

				print("]")

				if language_text != list(self.sub_files.keys())[-1]:
					print()

		print()
		print("-----")