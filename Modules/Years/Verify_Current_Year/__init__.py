# Verify_Current_Year.py

from Years.Years import Years as Years

class Verify_Current_Year(Years):
	def __init__(self):
		super().__init__()

		self.Verify_Current_Year()

	def Verify_Current_Year(self):
		from copy import deepcopy

		print()
		print("-----")
		print()

		# Define the "Files" dictionary
		self.files = {
			"Created in": {
				"Text key": "created_in",
				self.user_language: self.years["Current year"]["Folders"]["Text"]["root"] + self.Language.language_texts["created_in"] + ".txt"
			},
			"Edited in": {
				"Text key": "edited_in",
				self.user_language: self.years["Current year"]["Folders"]["Text"]["root"] + self.Language.language_texts["edited_in"] + ".txt"
			},
			"This Year I (post)": {
				"Text key": "this_year_i_post",
				"Template": {}
			},
			"Christmas": {
				"Text key": "texts, title()",
				self.user_language: self.years["Current year"]["Folders"]["Text"]["Christmas"]["Merry Christmas"]["root"] + self.Language.language_texts["texts, title()"] + ".txt",
				"Template": {
					self.user_language: self.years["Texts"]["Files"]["Christmas"]["Merry Christmas"]["Texts"]
				}
			},
			"New Year": {
				"Text key": "texts, title()",
				self.user_language: self.years["Current year"]["Folders"]["New Year"]["root"] + self.Language.language_texts["texts, title()"] + ".txt",
				"Template": {
					self.user_language: self.years["Texts"]["Files"]["New Year"]["Texts"]
				}
			}
		}

		# Define the language "This Year I (post)" file
		for language in self.languages["small"]:
			# Define the "This Year I (post)" file
			self.files["This Year I (post)"][language] = self.years["Current year"]["Folders"][language][self.Language.texts["this_year_i_post"]["en"]]

			# Define the template file
			self.files["This Year I (post)"]["Template"][language] = self.years["Texts"]["Folders"][language][self.Language.texts["this_year_i_post"]["en"]]

		# If the current year did not existed in the years folder
		# Creates the folders and files of the current year folder
		if self.years["States"]["Current year folder exists"] == False:
			# Iterate through the files in the "Files" dictionary
			for key, files in self.files.items():
				# Define the small languages list
				languages = self.languages["small"]

				if key != "This Year I (post)":
					languages = [
						self.user_language
					]

				# Iterate through the languages list
				for language in languages:
					# Get the file in the current language
					file = files[language]

					# Define the file to be read
					file_to_read = file

					# If the file has a template file
					if "Template" in files:
						# Update the file to read
						file_to_read = files["Template"][language]

					# Define the text to write as the file text as a string
					text_to_write = self.File.Contents(file_to_read)["string"]

					# Replace the current "{current_year}" text with the current year number on the text to write
					if "{current_year}" in text_to_write:
						text_to_write = text_to_write.replace("{current_year}", str(self.date["Units"]["Year"]))

					# Replace the "{next_year}" text with the next year number on the text to write
					if "{next_year}" in text_to_write:
						text_to_write = text_to_write.replace("{next_year}", str(self.date["Units"]["Year"] + 1))

					# If the file is either the "Created in" or "Edited in" file
					if " in" in key:
						# Get the current date
						date = self.Date.Now()

						# Get the correct format
						date = date["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"]

						# Redefine the text to write
						text_to_write = date

					# Create the file
					self.File.Create(file)

					# Update the file with the formatted text
					self.File.Edit(file, text_to_write, "w")

			# Define the list of Social Networks
			social_networks_list = [
				"Discord",
				"Instagram, Facebook",
				"Twitter",
				"WhatsApp"
			]

			# Create and format the files of Social Networks posts for the "Summary" folder
			for social_network in social_networks_list:
				# Define the social network file
				file = self.years["Current year"]["Folders"]["Text"]["Summary"]["root"] + social_network + ".txt"

				# Define the template file
				template_file = self.years["Texts"]["Folders"]["Summary"]["root"] + social_network + ".txt"

				# Read the template file
				text_to_write = self.File.Contents(template_file)["string"]

				# Replace the current "{current_year}" text with the current year number on the text to write
				if "{current_year}" in text_to_write:
					text_to_write = text_to_write.replace("{current_year}", str(self.date["Units"]["Year"]))

				# Create the file
				self.File.Create(file)

				# Update the file with the formatted template
				self.File.Edit(file, text_to_write, "w")

			# Create and format the files of Social Networks posts for the "New Year" folder
			for social_network in social_networks_list:
				# Define the social network file
				file = self.years["Current year"]["Files"]["Text"]["New Year"]["Social Networks"][social_network]

				# Define the template file
				template_file = self.years["Texts"]["Files"]["New Year"]["Social Networks"][social_network]

				# Read the template file
				text_to_write = self.File.Contents(template_file)["string"]

				# Define the "[Year type]" texts dictionary
				texts = {
					"Current year": {
						"Item": str(self.date["Units"]["Year"]),
						"List": [
							"{current_year}",
							"[" + self.Language.language_texts["current_year"] + "]"
						]
					},
					"Next year": {
						"Item": str(self.date["Units"]["Year"] + 1),
						"List": [
							"{next_year}",
							"[" + self.Language.language_texts["next_year"] + "]"
						]
					}
				}

				# Iterate through the keys of the texts dictionary
				for year_type, dictionary in texts.items():
					# Get the list of texts to search for
					for text in dictionary["List"]:
						# Replace the "[Year type]" text with the [year_type] number on the text to write
						if text in text_to_write:
							text_to_write = text_to_write.replace(text, dictionary["Item"])

				# Create the file
				self.File.Create(file)

				# Update the file with the formatted template
				self.File.Edit(file, text_to_write, "w")

			# Copy the Year images folder to the current Year Image folder
			self.Folder.Copy(self.folders["Image"]["Years"]["Images"]["root"], self.years["Current year"]["Folders"]["Image"]["root"])

		# Define the text that says that the current Year already exists in the Years folder
		text_to_show = self.language_texts["the_current_year_already_exists_in_the_years_folder"]

		# Define the text that says that the current Year did not existed in the Years folder
		if self.years["States"]["Current year folder exists"] == False:
			text_to_show = self.language_texts["the_current_year_did_not_existed_in_the_years_folder"]

		tab = "\t"

		# Show the text to show and the current year number
		print(text_to_show + ":")
		print(tab + str(self.date["Units"]["Year"]))
		print()

		# Define the text that is shown when the year folder already existed
		text_to_show = self.language_texts["this_is_its_year_folder"]

		# Define the text that is shown when the year folder did not existed in the folder of years
		if self.years["States"]["Current year folder exists"] == False:
			text_to_show = self.language_texts["its_year_folder_was_created"]

		# Show the text above and the year folder
		print(text_to_show + ":")
		print(tab + self.years["Current year"]["Folders"]["Text"]["root"])
		print()

		# Show the image folder of the year
		print(self.Language.language_texts["image_folder"] + ":")
		print(tab + self.years["Current year"]["Folders"]["Image"]["root"])

		# If the current year did not existed in the years folder
		if self.years["States"]["Current year folder exists"] == False:
			# Show the "Texts" text
			print()
			print(self.Language.language_texts["texts, title()"] + ":")

			tab = "\t"
			double_tab = "\t\t"

			# Iterate through the files in the "Files" dictionary
			for key, files in self.files.items():
				# Define the small languages list
				languages = self.languages["small"]

				if key != "This Year I (post)":
					languages = [
						self.user_language
					]

				# Iterate through the languages list
				for language in languages:
					# Get the file in the current language
					file = files[language]

					# Define the text key
					text_key = files["Text key"]

					# Define the language text
					language_text = self.Language.texts[text_key][language]

					# Read the file and get its lines of text
					lines = self.File.Contents(file)["lines"]

					# Show the language text with a tab
					print(tab + '"' + language_text + '":')

					# Show a separator with a tab
					print(tab + "[")

					# Show the file lines with two tabs
					for line in lines:
						print(double_tab + "| " + line)

					# Show a separator and a space separator with a tab
					print(tab + "]")
					print()

		# If the current year already existed in the years folder
		else:
			# Show a space separator
			print()

		# Show a five dash separator
		print("-----")

		# If the current year did not existed in the years folder
		if self.years["States"]["Current year folder exists"] == False:
			# Re-initiate the root class to update the files
			super().__init__()