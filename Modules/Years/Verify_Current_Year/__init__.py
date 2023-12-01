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

		folder_list = self.Folder.Contents(self.years["Current year"]["Folders"]["Text"]["root"])["folder"]["list"]

		# Creates the new Year text and image folder, copies the Year template files to the text folder, and edits some of them
		if folder_list == []:
			# Copy the Year texts folder to the current Year folder
			self.Folder.Copy(self.years["Texts"]["Folders"]["root"], self.years["Current year"]["Folders"]["Text"]["root"])

			# Copy the Year images folder to the current Year Image folder
			self.Folder.Copy(self.folders["Image"]["Years"]["Images"]["root"], self.years["Current year"]["Folders"]["Image"]["root"])

			# "This Year I (post)" file
			for language in self.languages["small"]:
				self.this_year_i_post_file = self.years["Current year"]["Folders"][language][self.JSON.Language.texts["this_year_i_post"][language]]

				text_to_write = self.File.Contents(self.this_year_i_post_file)["string"]

				if "{current_year}" in text_to_write:
					text_to_write = text_to_write.replace("{current_year}", str(self.date["Units"]["Year"]))

				self.File.Edit(self.this_year_i_post_file, text_to_write, "w")

			self.files = {
				"Christmas": self.years["Current year"]["Folders"]["Text"]["Christmas"]["Merry Christmas"]["root"] + self.JSON.Language.language_texts["texts, title()"] + ".txt",
				"New Year": self.years["Current year"]["Folders"]["New Year"]["root"] + self.JSON.Language.language_texts["texts, title()"] + ".txt"
			}

			# Replace the current "{current_year}" text with current Year number on Christmas Texts file
			text_to_write = self.File.Contents(self.files["Christmas"])["string"]

			if "{current_year}" in text_to_write:
				text_to_write = text_to_write.replace("{current_year}", str(self.date["Units"]["Year"]))

			self.File.Edit(self.files["Christmas"], text_to_write, "w")

			# Replace the "{next_year}" text with the next Year number on the New Year "Texts" file
			text_to_write = self.File.Contents(self.files["New Year"])["string"]

			if "{next_year}" in text_to_write:
				text_to_write = text_to_write.replace("{next_year}", str(self.date["Units"]["Year"] + 1))

			self.File.Edit(self.files["New Year"], text_to_write, "w")

			date = self.Date.Now()

			# "Created In" file
			self.created_in_file = self.years["Current year"]["Folders"]["Text"]["root"] + self.JSON.Language.language_texts["created_in"] + ".txt"
			self.File.Edit(self.created_in_file, date["Timezone"]["Formats"]["HH:MM DD/MM/YYYY"], "w")

			date = self.Date.Now()

			# "Edited In" file
			self.edited_in_file = self.years["Current year"]["Folders"]["Text"]["root"] + self.JSON.Language.language_texts["edited_in"] + ".txt"
			self.File.Edit(self.edited_in_file, date["Timezone"]["Formats"]["HH:MM DD/MM/YYYY"], "w")

			# Social Networks posts files
			for item in ["Instagram, Facebook", "Twitter", "WhatsApp"]:
				file = self.years["Current year"]["Folders"]["Text"]["Summary"]["root"] + item + ".txt"

				text_to_write = self.File.Contents(file)["string"]

				if "{current_year}" in text_to_write:
					text_to_write = text_to_write.replace("{current_year}", str(self.date["Units"]["Year"]))

				self.File.Edit(file, text_to_write, "w")

		# Tells the user that the current Year already exists in the Years folder
		text_to_show = self.language_texts["the_current_year_already_exists_in_the_years_folder"]

		# Tells the user that the current Year did not existed in the Years folder
		if folder_list == []:
			text_to_show = self.language_texts["the_current_year_did_not_existed_in_the_years_folder"]

		tab = "\t"

		print(text_to_show + ":")
		print(tab + str(self.date["Units"]["Year"]))
		print()

		text_to_show = self.language_texts["this_is_its_year_folder"]

		if folder_list == []:
			text_to_show = self.language_texts["its_year_folder_was_created"]

		print(text_to_show + ":")
		print(tab + self.years["Current year"]["Folders"]["Text"]["root"])
		print()

		print(self.JSON.Language.language_texts["image_folder"] + ":")
		print(tab + self.years["Current year"]["Folders"]["Image"]["root"])

		if folder_list == []:
			print()

			for item in self.files:
				file = self.files[item]

				text_key = item.lower().replace(" ", "_")

				if "_" not in text_key:
					text_key += ", title()"

				language_text = self.JSON.Language.language_texts[text_key]

				print(self.language_texts["{}_texts"].format(language_text) + ":")

				print("[")

				for line in self.File.Contents(file)["lines"]:
					print("\t" + line)

				print("]")
				print()

		else:
			print()

		print("-----")