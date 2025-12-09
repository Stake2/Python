# Verify_Current_Year.py

# Import the root class
from Years.Years import Years as Years

# Import some useful modules
from copy import deepcopy

class Verify_Current_Year(Years):
	def __init__(self):
		# Run the root class to import its methods and variables
		super().__init__()

		# Define the files dictionary
		self.Define_Files()

		# Verify the current year
		self.Verify_Current_Year()

	def Define_Files(self):
		# Create a shortcut to the "Text" folder of the current year
		text_folder = self.years["Current year"]["Folders"]["Text"]

		# Define the files dictionary with its keys, text keys, and files
		self.files = {
			"Created in": {
				"Text key": "created_in",
				self.language["Small"]: text_folder["root"] + self.Language.language_texts["created_in"] + ".txt"
			},
			"Edited in": {
				"Text key": "edited_in",
				self.language["Small"]: text_folder["root"] + self.Language.language_texts["edited_in"] + ".txt"
			},
			"Yearly statistics": {
				"Text key": "yearly_statistics",
				"Template": {}
			},
			"This Year I (post)": {
				"Text key": "this_year_i_post",
				"Template": {}
			},
			"This Year I (personal version)": {
				"Text key": "this_year_i_personal_version"
			},
			"FutureMe": {
				"Text": "FutureMe"
			},
			"Christmas": {
				"Show text": self.Language.language_texts["merry_christmas"],
				"Text key": "texts, title()",
				self.language["Small"]: text_folder["Christmas"]["Merry Christmas"]["root"] + self.Language.language_texts["texts, title()"] + ".txt",
				"Template": {
					self.language["Small"]: self.years["Texts"]["Files"]["Christmas"]["Merry Christmas"]["Texts"]
				}
			},
			"New Year": {
				"Show text": self.Language.language_texts["happy_new_year"],
				"Text key": "texts, title()",
				self.language["Small"]: self.years["Current year"]["Folders"]["New Year"]["root"] + self.Language.language_texts["texts, title()"] + ".txt",
				"Template": {
					self.language["Small"]: self.years["Texts"]["Files"]["New Year"]["Texts"]
				}
			}
		}

		# Define some language files related to the "This Year I" text
		for language in self.languages["Small"]:
			# Create a shortcut for the folders dictionary
			folders = self.years["Current year"]["Folders"][language]

			# Define the "This Year I (post)" file
			self.files["This Year I (post)"][language] = folders[self.Language.texts["this_year_i_post"]["en"]]

			# Define the "This Year I (post)" template file
			self.files["This Year I (post)"]["Template"][language] = folders[self.Language.texts["this_year_i_post"]["en"]]

			# Define the "This Year I (personal version)" file
			self.files["This Year I (personal version)"][language] = folders[self.Language.texts["this_year_i_post"]["en"]]

			# If the "FutureMe" key is inside the folders dictionary
			if "FutureMe" in folders:
				# Define the "FutureMe" file
				self.files["FutureMe"][language] = folders["FutureMe"]

		# If the current year did not existed in the years folder
		if self.years["States"]["Current year folder exists"] == False:
			# Iterate through the keys and files inside the files dictionary
			for key, files in self.files.items():
				# Define the local list of small languages as the root one
				languages = self.languages["Small"]

				# If the key is not "This Year I (post)"
				if key != "This Year I (post)":
					# Define the local list of languages as only the user language
					languages = [
						self.language["Small"]
					]

				# Iterate through the local list of small languages
				for language in languages:
					# If the language is inside the list of files
					if language in files:
						# Get the file in the current language
						file = files[language]

					# Else, get the file from the text "Files" dictionary of the current year
					else:
						file = self.years["Current year"]["Files"]["Text"][language][key]

					# Define the file to be read
					file_to_read = file

					# If the file has a template file
					if "Template" in files:
						# If the language is inside the "Template" dictionary
						if language in files["Template"]:
							# Update the file to read to be the template one
							file_to_read = files["Template"][language]

						# Else, get the file template from the "Texts" files dictionary
						else:
							file_to_read = self.years["Texts"]["Files"][language][key]

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

						# Get the user timezone datetime format
						date = date["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"]

						# Define the text to write as the date string
						text_to_write = date

					# Create the file
					self.File.Create(file)

					# Write the text to write inside the file
					self.File.Edit(file, text_to_write, "w")

			# Define the local list of social networks
			social_networks_list = [
				"Discord",
				"Instagram {} Facebook",
				"Twitter, Bluesky, {} Threads",
				"WhatsApp"
			]

			# Iterate through the local list of social networks
			# To create and write into the social network posts files inside the "Summary" folder
			for social_network in social_networks_list:
				# If the "{}" format string is present inside the social network
				if "{}" in social_network:
					# Format the social network with the "and" text in the user language
					social_network = social_network.format(self.Language.language_texts["and"])

				# Define the social network file inside the "Summary" folder
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

				# Write the text to write inside the file
				self.File.Edit(file, text_to_write, "w")

			# Define a new list of social networks
			social_networks_list = [
				"Discord",
				"Instagram {} Facebook",
				"Twitter",
				"Bluesky {} Threads",
				"WhatsApp",
				"Wattpad"
			]

			# Iterate through the local list of social networks
			# To create and write into the social network posts files inside the "New Year" folder
			for social_network in social_networks_list:
				# If the "{}" format string is present inside the social network
				if "{}" in social_network:
					# Format the social network with the "and" text
					social_network = social_network.format("and")

				# Define the social network file
				file = self.years["Current year"]["Files"]["Text"]["New Year"]["Social networks"][social_network]

				# Define the template file
				template_file = self.years["Texts"]["Files"]["New Year"]["Social networks"][social_network]

				# Read the template file
				text_to_write = self.File.Contents(template_file)["string"]

				# Define the "[Year type]" texts dictionary
				texts = {
					"Current year": {
						# The year number
						"Item": str(self.date["Units"]["Year"]),

						# The list of texts to replace with the year number with
						"List": [
							"{current_year}",
							"[" + self.Language.language_texts["current_year"] + "]"
						]
					},
					"Next year": {
						# The year number
						"Item": str(self.date["Units"]["Year"] + 1),

						# The list of texts to replace with the year number with
						"List": [
							"{next_year}",
							"[" + self.Language.language_texts["next_year"] + "]"
						]
					}
				}

				# Iterate through the year types and dictionaries inside the texts dictionary
				for year_type, dictionary in texts.items():
					# Iterate through the list of texts to search for
					for text in dictionary["List"]:
						# If the text is inside the text to write
						if text in text_to_write:
							# Replace the "[Year type]" text with the [year_type] number on the text to write
							# Example: "{current_year}" and "[Current year]" would both become "2025"
							text_to_write = text_to_write.replace(text, dictionary["Item"])

				# Create the file
				self.File.Create(file)

				# Write the text to write inside the file
				self.File.Edit(file, text_to_write, "w")

			# List the folders inside the current year image folder
			folders = self.Folder.Contents(self.years["Current year"]["Folders"]["Image"]["root"])

			# Define a "copy image folder" switch as False
			copy_image_folder = False

			# If the local "copy image folder" switch is True
			if copy_image_folder == True:
				# Copy the year images folder to the current year image folder
				self.Folder.Copy(self.folders["Image"]["Years"]["Images"]["root"], self.years["Current year"]["Folders"]["Image"]["root"])

	def Verify_Current_Year(self):
		# Show a ten dash space separator
		print()
		print(self.separators["10"])
		print()

		# Define the tab variable as only one tab
		tab = "\t"

		# Show the "Current year" text in the user language and the current year number with the tab
		print(self.Language.language_texts["current_year"] + ":")
		print(tab + str(self.date["Units"]["Year"]))
		print()

		# Define the text to show initially as the text which says the current year already exists in the years folder
		text_to_show = self.language_texts["the_current_year_already_exists_in_the_years_folder"]

		# If the current year did not existed in the years folder
		if self.years["States"]["Current year folder exists"] == False:
			# Change the text to show to the text which says the current year did not existed in the years folder
			text_to_show = self.language_texts["the_current_year_did_not_existed_in_the_years_folder"]

		# Show the "Status of the year folder" text in the user language and the text to show with the tab
		print(self.language_texts["status_of_the_year_folder"] + ":")
		print(tab + text_to_show)
		print()

		# Define the text to show initially as the text which talks about the year folder
		text_to_show = self.language_texts["this_is_its_year_folder"]

		# If the current year did not existed in the years folder
		if self.years["States"]["Current year folder exists"] == False:
			# Change the text to show to the text which says the year folder was created
			text_to_show = self.language_texts["its_year_folder_was_created"]

		# Show the text above and the current year folder
		print(text_to_show + ":")
		print(tab + self.years["Current year"]["Folders"]["Text"]["root"])
		print()

		# Show the "Image folder of the year" and the year image folder
		print(self.language_texts["image_folder_of_the_year"] + ":")
		print(tab + self.years["Current year"]["Folders"]["Image"]["root"])

		# If the current year did not existed in the years folder
		if self.years["States"]["Current year folder exists"] == False:
			# Show the "Texts" text in the user language
			print()
			print(self.Language.language_texts["texts, title()"] + ":")

			# Define the double tab variable as two tabs
			double_tab = "\t\t"

			# Iterate through the keys and files inside the files dictionary
			for key, files in self.files.items():
				# Define the local list of small languages as the root one
				languages = self.languages["Small"]

				# If the key is not "This Year I (post)"
				# Or is inside the defined list
				if (
					key != "This Year I (post)" or
					key in ["Yearly statistics", "FutureMe"]
				):
					# Define the local list of languages as only the user language
					languages = [
						self.language["Small"]
					]

				# Iterate through the local list of small languages
				for language in languages:
					# If the language is inside the list of files
					if language in files:
						# Get the file in the current language
						file = files[language]

					# Else, get the file from the text "Files" dictionary of the current year
					else:
						file = self.years["Current year"]["Files"]["Text"][language][key]

					# If the "Text key" key is inside the files dictionary
					if "Text key" in files:
						# Create a shortcut to that key
						text_key = files["Text key"]

						# Define the language text
						language_text = self.Language.texts[text_key][language]

					# If the "Text" key is inside the files dictionary
					if "Text" in files:
						# Define the language text as that key
						language_text = files["Text"]

					# Read the file to get its lines
					lines = self.File.Contents(file)["Lines"]

					# If the list of lines is not empty
					if lines != []:
						# If the "Show text" is inside the files dictionary
						if "Show text" in files:
							# Change the language text to that text
							language_text = files["Show text"]

						# Show the language text with a tab
						print(tab + '"' + language_text + '":')

						# If the list of lines has only one line
						if len(lines) == 1:
							# Define the text template to show only one line
							text_template = double_tab + "{}"

							# Define the text as the first line
							text = lines[0] + "\n"

						# If the list of lines has multiple lines
						if len(lines) > 1:
							# Define the text template to show multiple lines
							text_template = tab + "[" + "\n" + \
							"{}" + \
							"\n" + \
							tab + "]" + "\n"

							# Define a local line number
							line_number = 0

							# Iterate through the list of file lines
							for line in lines:
								# Update them to add the double tab and the pipe
								lines[line_number] = double_tab + "| " + line

								# Add one to the local line number
								line_number += 1

							# Define the text as the list of lines converted into a text
							text = self.Text.From_List(lines)

						# Format the text template with the text
						text = text_template.format(text)

						# Show the text
						print(text)

		# If the current year already existed in the years folder
		else:
			# Show a space separator
			print()

		# Show a ten dash space separator
		print(self.separators["10"])

		# If the current year did not existed in the years folder
		if self.years["States"]["Current year folder exists"] == False:
			# Re-initiate the root class to update the year files
			super().__init__()