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

		folder_list = self.Folder.Contents(self.current_year["Folder"])["folder"]["list"]

		# Creates the new Year text and image folder, copies the Year template files to the text folder, and edits some of them
		if folder_list == []:
			# Copy "Year Texts" folder to Current Year folder
			self.Folder.Copy(self.years["year_texts"]["root"], self.current_year["Folder"])

			# Copy "Year Images" folder to Current Year Image folder
			self.Folder.Copy(self.year_images_folder, self.current_year["image_folder"])

			# Re-define folders (re-read directory)
			self.current_year["folders"] = self.Folder.Contents(self.current_year["Folder"])["dictionary"]

			# This Year I (post) file
			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				self.this_year_i_post_file = self.current_year["folders"][full_language][self.texts["this_year_i_post"][language]]

				text_to_write = self.File.Contents(self.this_year_i_post_file)["string"]

				if "{current_year}" in text_to_write:
					text_to_write = text_to_write.replace("{current_year}", str(self.date["year"]))

				self.File.Edit(self.this_year_i_post_file, text_to_write, "w")

			self.files = {
				"christmas, title()": self.current_year["folders"][self.language_texts["christmas, en - " + self.user_language]]["root"] + self.language_texts["texts, en - " + self.user_language] + ".txt",
				"new_year": self.current_year["folders"][self.language_texts["new_year, en - " + self.user_language]]["root"] + self.language_texts["texts, en - " + self.user_language] + ".txt",
			}

			# Replace "{current_year}" with current Year number on Christmas Texts file
			text_to_write = self.File.Contents(self.files["christmas, title()"])["string"]

			if "{current_year}" in text_to_write:
				text_to_write = text_to_write.replace("{current_year}", str(self.date["year"]))

			self.File.Edit(self.files["christmas, title()"], text_to_write, "w")

			# Replace "{current_year}" with current Year number on New Year Texts file
			text_to_write = self.File.Contents(self.files["new_year"])["string"]

			if "{next_year}" in text_to_write:
				text_to_write = text_to_write.replace("{next_year}", str(self.date["year"] + 1))

			self.File.Edit(self.files["new_year"], text_to_write, "w")

			# Created In file
			self.created_in_file = self.current_year["Folder"] + self.language_texts["created_in, en - " + self.user_language] + ".txt"
			self.File.Edit(self.created_in_file, self.Date.Now()["strftime"], "w")

			# Edited In file
			self.edited_in_file = self.current_year["Folder"] + self.language_texts["edited_in, en - " + self.user_language] + ".txt"
			self.File.Edit(self.edited_in_file, self.Date.Now()["strftime"], "w")

			# New Year posts folder
			self.new_year_posts_folder = self.current_year["folders"][self.language_texts["new_year, en - " + self.user_language]]["root"] + "Posts/"

			# Social Networks posts files
			for item in ["Instagram, Facebook", "Twitter", "WhatsApp"]:
				file = self.new_year_posts_folder + item + ".txt"

				text_to_write = self.File.Contents(file)["string"]

				if "{current_year}" in text_to_write:
					text_to_write = text_to_write.replace("{current_year}", str(self.date["year"]))

				self.File.Edit(file, text_to_write, "w")

		# Tells the user that the current Year already exists in the Years folder
		text_to_show = self.language_texts["the_current_year_already_exists_in_the_years_folder"]

		# Tells the user that the current Year did not existed in the Years folder
		if folder_list == []:
			text_to_show = self.language_texts["the_current_year_did_not_existed_in_the_years_folder"]

		print(text_to_show + ":")
		print(self.date["year"])
		print()

		text_to_show = self.language_texts["this_is_its_year_folder"]

		if folder_list == []:
			text_to_show = self.language_texts["its_year_folder_was_created"]

		print(text_to_show + ":")
		print(self.current_year["Folder"])
		print()

		print(self.language_texts["image_folder"] + ":")
		print(self.current_year["image_folder"])

		if folder_list == []:
			print()

			for item in self.files:
				file = self.files[item]

				language_text = self.language_texts[item]

				print(self.language_texts["{}_texts"].format(language_text) + ":")

				print("[")

				for line in self.File.Contents(file)["lines"]:
					print("\t" + line)

				print("]")
				print()

		else:
			print()

		print("-----")