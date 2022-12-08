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
			self.Folder.Copy(self.year_texts_folder, self.current_year["folder"])

			# Copy "Year Images" folder to Current Year Image folder
			self.Folder.Copy(self.year_images_folder, self.current_year["image_folder"])

			# Christmas Texts file
			self.christmas_folder = self.current_year["folder"] + self.mixed_christmas_text + "/"
			self.christmas_file = self.christmas_folder + self.mixed_texts_text + ".txt"

			text_to_write = self.File.Contents(self.christmas_file)["string"]

			if "{current_year}" in text_to_write:
				text_to_write = text_to_write.replace("{current_year}", self.date["year"])

			self.File.Edit(self.christmas_file, text_to_write, "w")

			# New Year Texts file
			self.new_year_folder = self.current_year["folder"] + self.mixed_new_year_text + "/"
			self.new_year_file = self.new_year_folder + self.mixed_texts_text + ".txt"

			text_to_write = self.File.Contents(self.new_year_file)["string"]

			if "{next_year}" in text_to_write:
				text_to_write = text_to_write.replace("{next_year}", self.next_year)

			self.File.Edit(self.new_year_file, text_to_write, "w")

			# Created In file
			self.created_in_file = self.current_year["folder"] + self.mixed_created_in_text + ".txt"
			self.File.Edit(self.created_in_file, self.Date.Now()["strftime"], "w")

			# Edited In file
			self.edited_in_file = self.current_year["folder"] + self.mixed_edited_in_text + ".txt"
			self.File.Edit(self.edited_in_file, self.Date.Now()["strftime"], "w")

			self.sub_files = {
				self.language_christmas_text: self.christmas_file,
				self.language_new_year_text: self.new_year_file,
			}

		# Tells the user that the current Year already exists in the Years folder
		text_to_show = self.language_texts["the_current_year_already_exists_in_the_years_folder"]

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
			for self.language_text in self.sub_files:
				file = self.sub_files[self.language_text]

				print(self.language_texts["{}_texts"] + ":")

				print("[")

				for line in self.File.Contents(file)["lines"]:
					print("\t" + line)

				print("]")

				if language_text != list(self.sub_files.keys())[-1]:
					print()

		print()
		print("-----")