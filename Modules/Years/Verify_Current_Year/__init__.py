# Verify_Current_Year.py

# Import the root class
from Years.Years import Years as Years

# Import some useful modules
import collections

class Verify_Current_Year(Years):
	def __init__(self):
		# Run the root class to import its methods and variables
		super().__init__()

		# Define the root "verify" dictionary
		self.verify = {
			# Define the empty "Files" dictionary which will be filled later
			"Files": {},

			# Define the empty "Social network files" dictionary which will be filled later
			"Social network files": {},

			# Define the empty "Format strings" which will be filled later
			"Format strings": {},

			# Define the "States" dictionary as a copy of the root "States" dictionary plus the "Copy image folders" state
			"States": {
				**self.years["States"],
				"Copy image folders": False
			}
		}

		# Define the text "Files" dictionary
		self.Define_Text_Files()

		# Define the "Social network files" dictionary
		self.Define_Social_Network_Files()

		# If the "Testing" switch is True
		if self.switches["Testing"] == True:
			# Change the "Current year folder exists" state to False
			self.verify["States"]["Current year folder exists"] = False

		# If "Current year folder exists" state is False
		# (The current year did not existed in the years folder)
		if self.verify["States"]["Current year folder exists"] == False:
			# Write to the year files
			self.Write_To_Files()

			# Update the image folder of the year
			self.Update_Image_Folder()

		# Show information about the verification of the current year and the current year information
		self.Show_Information()

	def Define_Text_Files(self):
		# Create a shortcut to the current year "Text" files dictionary
		current_year_files = self.years["Current year"]["Files"]

		# Update the root "Files" dictionary
		self.verify["Files"] = {
			"Numbers": {
				"Total": 0
			},
			"List": [
				"Created in",
				"Edited in",
				"Christmas",
				"Yearly statistics",
				"This Year I",
				"This Year I (personal version)",
				"This Year I (post)",
				"FutureMe",
				"New Year"
			],
			"Dictionary": {
				"Created in": {
					"User language file": True,
					"Use current date": True
				},
				"Edited in": {
					"User language file": True,
					"Use current date": True
				},
				"Christmas": {
					"Texts": self.Language.texts["merry_christmas"],
					"File": current_year_files["Christmas"]["Merry Christmas"]["Texts"],
					"Template file": self.years["Texts"]["Files"]["Christmas"]["Merry Christmas"]["Texts"],
					"User language file": True
				},
				"Yearly statistics": {
					"User language file": True,
					"Use template": True
				},
				"This Year I": {
					"Use template": True
				},
				"This Year I (personal version)": {
					"Use template": True
				},
				"This Year I (post)": {
					"Use template": True
				},
				"FutureMe": {
					"User language file": True
				},
				"New Year": {
					"Texts": self.Language.texts["happy_new_year"],
					"File": current_year_files["New Year"]["Texts"],
					"Template file": self.years["Texts"]["Files"]["New Year"]["Texts"],
					"User language file": True
				}
			}
		}

		# Update the total number of files
		self.verify["Files"]["Numbers"]["Total"] = len(self.verify["Files"]["List"])

		# Create a shortcut to the current year "Files" dictionary
		current_year_files = self.years["Current year"]["Files"]

		# Create a shortcut to the "Files" dictionary of the "Texts" dictionary
		texts_files = self.years["Texts"]["Files"]

		# Iterate through the list of file keys inside the root "Files" dictionary
		for key in self.verify["Files"]["List"]:
			# Define the file dictionary
			dictionary = {
				"Key": key,
				"Files": {}
			}

			# If the dictionary already existed in the root "Dictionary"
			if key in self.verify["Files"]["Dictionary"]:
				# Update the local dictionary with the root one
				dictionary.update(self.verify["Files"]["Dictionary"][key])

			# Create a list of keys to define
			to_define = [
				"User language file",
				"Use template",
				"Use current date"
			]

			# Iterate through the list of keys
			for key_to_define in to_define:
				# If the key is not present
				if key_to_define not in dictionary:
					# Define it as False
					dictionary[key_to_define] = False

			# Define the local list of small languages as the root one
			languages = self.languages["Small"]

			# If the "User language file" switch is True
			if dictionary["User language file"] == True:
				# Define the local list of languages as only the user language
				languages = [
					self.language["Small"]
				]

			# Iterate through the local list of small languages
			for language in languages:
				# If the "Use template" switch is True
				# Or the "Template file" key is inside the local dictionary
				if (
					dictionary["Use template"] == True or
					"Template file" in dictionary
				):
					# If the "Template files" dictionary is not present
					if "Template files" not in dictionary:
						# Create it
						dictionary["Template files"] = {}

				# If the "File" key is not inside the local dictionary
				if "File" not in dictionary:
					# Define the local list of dictionaries to iterate through
					dictionaries = [
						current_year_files,
						current_year_files[language]
					]

					# Iterate through the list of dictionaries
					for file_dictionary in dictionaries:
						# If the key is inside that dictionary
						if key in file_dictionary:
							# Update the local language files dictionary to be the current one
							language_files = file_dictionary

					# If the file key is inside that dictionary
					if key in language_files:
						# Get the file
						file = language_files[key]

						# Add it to the "Files" dictionary in the language key
						dictionary["Files"][language] = file

					# If the "Template file" key is not inside the local dictionary
					# And the "Use template" switch is True
					if (
						"Template file" not in dictionary and
						dictionary["Use template"] == True
					):
						# Define the local list of dictionaries to iterate through
						dictionaries = [
							texts_files,
							texts_files[language]
						]

						# Iterate through the list of dictionaries
						for file_dictionary in dictionaries:
							# If the key is inside that dictionary
							if key in file_dictionary:
								# Update the local language files dictionary to be the current one
								language_files = file_dictionary

						# Define the language template file as the template file inside the "Files" dictionary of the "Texts" dictionary
						dictionary["Template files"][language] = language_files[key]

				# If the "File" key is inside the local dictionary
				if "File" in dictionary:
					# Add it to the "Files" dictionary in the language key
					dictionary["Files"][language] = dictionary["File"]

					# Remove the "File" key
					dictionary.pop("File")

					# If the "Template file" key is inside the local dictionary
					if "Template file" in dictionary:
						# Define the template file in the language key as the root "Template file"
						dictionary["Template files"][language] = dictionary["Template file"]

						# Remove the "Template file" key
						dictionary.pop("Template file")

				# If the "Texts" key is not inside the dictionary
				if "Texts" not in dictionary:
					# Define the text as the key
					text = key

					# Create the text key by converting the key into lowercase and replacing spaces with underscores
					text_key = key.lower().replace(" ", "_")

					# If the underscore character is not inside the text key
					if "_" not in text_key:
						# Add the ", title()" text
						text_key += ", title()"

					# Remove the parentheses from the text key
					text_key = text_key.replace("(", "")
					text_key = text_key.replace(")", "")

					# If the text key is inside the language texts dictionary of the "Language" utility class
					if text_key in self.Language.texts:
						# Define the texts as the text dictionary inside the text key
						texts = self.Language.texts[text_key]

					# Add the local texts to the root "Texts" key
					dictionary["Texts"] = texts

			# ---------- #

			# Define the order to use to sort the keys of the dictionary
			order = [
				"Key",
				"Texts",
				"Files"
			]

			# If the "Template files" key is inside the dictionary
			if "Template files" in dictionary:
				# Add that key too
				order.append("Template files")

			# Add the rest of the keys
			order.extend([
				"User language file",
				"Use template",
				"Use current date"
			])

			# Sort the keys of the dictionary with the defined order
			dictionary = self.JSON.Sort_Item_List(dictionary, order = order)

			# Add the local dictionary to the root "Files" dictionary
			self.verify["Files"]["Dictionary"][key] = dictionary

		# Sort the keys of the "Files" dictionary with the order being the "List" of files
		self.verify["Files"]["Dictionary"] = self.JSON.Sort_Item_List(self.verify["Files"]["Dictionary"], order = self.verify["Files"]["List"])

	def Define_Social_Network_Files(self):
		# Update the root "Social network files" dictionary
		self.verify["Social network files"] = {
			"Numbers": {
				"Total": 0
			},
			"List": [
				"Summary",
				"New Year"
			],
			"Dictionary": {}
		}

		# Update the total number of social network files
		self.verify["Social network files"]["Numbers"]["Total"] = len(self.verify["Social network files"]["List"])

		# Define a list of items to import
		to_import = [
			"Name",
			"Numbers",
			"List"
		]

		# Iterate through the list of social network lists
		for social_network_list in self.verify["Social network files"]["List"]:
			# Define the dictionary
			dictionary = {
				"Name": {},
				"Numbers": {},
				"List": [],
				"Dictionary": {}
			}

			# Get the root dictionary of social networks
			social_networks = self.social_networks["Dictionary"][social_network_list]

			# Iterate through the list of items to import
			for item in to_import:
				# Import the item from the root social networks dictionary
				dictionary[item] = social_networks[item]

			# Iterate through the social network names inside the defined dictionary
			for social_network_name in dictionary["List"]:
				# Define the local social network dictionary
				social_network = {
					"Name": {},
					"File": "",
					"Template file": ""
				}

				# Import the root social network "Name" dictionary
				social_network["Name"] = social_networks["Dictionary"][social_network_name]["Name"]

				# Create a shortcut to the "Files" dictionary
				files = self.years["Current year"]["Files"][social_network_list]

				# Create a shortcut to the template "Files" dictionary
				template_files = self.years["Texts"]["Files"][social_network_list]

				# If the social networks list name is "New Year"
				if social_network_list == "New Year":
					# Get the "Social networks" dictionary from both dictionaries
					files = files["Social networks"]

					# Create a shortcut to the template "Files" dictionary
					template_files = template_files["Social networks"]

				# Get the social network "File" and add it to the social network dictionary
				social_network["File"] = files[social_network_name]

				# Get the social network "Template file" and add it to the social network dictionary
				social_network["Template file"] = template_files[social_network_name]

				# Add the local social network dictionary to the root list "Dictionary"
				dictionary["Dictionary"][social_network_name] = social_network

			# Add the local social networks list dictionary to the root "Dictionary"
			self.verify["Social network files"]["Dictionary"][social_network_list] = dictionary

	def Write_To_Files(self):
		# Iterate through the file keys and dictionaries inside the "Dictionary" of the root "Files" dictionary
		for key, dictionary in self.verify["Files"]["Dictionary"].items():
			# Create the "Text to write" dictionary
			dictionary["Text to write"] = {}

			# List the languages inside the "Files" dictionary
			languages = list(dictionary["Files"].keys())

			# Iterate through the local list of small languages
			for language in languages:
				# Get the file in the current language and define it as the file to write to
				file_to_write = dictionary["Files"][language]

				# Define the file to be read as the file to write
				file_to_read = file_to_write

				# If the "Template files" dictionary is present (the file has a template file)
				if "Template files" in dictionary:
					# Change the file to read as the template file in the current language key
					file_to_read = dictionary["Template files"][language]

				# Define the text to write as the text of the "file to read" as a string
				text_to_write = self.File.Contents(file_to_read)["String"]

				# Replace the format strings inside the text to write
				text_to_write = self.Replace_Year_Format_Strings(text_to_write)

				# If the "Use current date" switch is True
				if dictionary["Use current date"] == True:
					# Get the current date
					date = self.Date.Now()

					# Get the user timezone datetime format of the current date
					date_string = date["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"]

					# Define the text to write as the date string
					text_to_write = date_string

				# Create the file
				self.File.Create(file_to_write)

				# Write the text to write inside the file
				self.File.Edit(file_to_write, text_to_write, "w")

				# Add the text to write to the "Text to write" dictionary in the current language key
				dictionary["Text to write"][language] = text_to_write

			# Update the root dictionary with the local one
			self.verify["Files"]["Dictionary"][key] = dictionary

		# ---------- #

		# Iterate through the keys and dictionaries of the social network lists
		for key, dictionary in self.verify["Social network files"]["Dictionary"].items():
			# Get the dictionary of social networks
			social_networks = dictionary["Dictionary"]

			# Iterate through the social network names and dictionaries inside the defined dictionary
			for social_network_name, social_network in social_networks.items():
				# Read the social network template file
				text_to_write = self.File.Contents(social_network["Template file"])["String"]

				# Replace the format strings inside the text to write
				text_to_write = self.Replace_Year_Format_Strings(text_to_write)

				# Create the social network file
				self.File.Create(social_network["File"])

				# Write the text to write inside the social network file
				self.File.Edit(social_network["File"], text_to_write, "w")

				# Add the text to write to the "Text to write" dictionary
				social_network["Text to write"] = text_to_write

				# Update the root social network dictionary with the local one
				social_networks[social_network_name] = social_network

			# Update the root social network list dictionary with the local one
			self.verify["Social network files"]["Dictionary"][key] = dictionary

	def Update_Image_Folder(self):
		# Define the source folder as the year "Images" folder (it is a template folder for new years)
		source_folder = self.folders["Image"]["Years"]["Images"]["root"]

		# Create a shortcut to the "Folder exists" boolean to call the method only one time
		folder_exists = self.Folder.Exists(source_folder)

		# List the contents of the folder
		folder_contents = self.Folder.Contents(source_folder)

		# If the source folder does not exist
		# Or it exists
		# And it is empty
		if (
			folder_exists == False or
			folder_exists == True and
			folder_contents["Folder"]["List"] == []
		):
			# Change the "Copy image folders" state to True
			self.verify["States"]["Copy image folders"] = True

		# If "Copy image folders" state is True
		if self.verify["States"]["Copy image folders"] == True:
			# Define the destination folder as the current year "Image" folder
			destination_folder = self.years["Current year"]["Folders"]["Image"]["root"]

			# Copy the source folder contents to the destination folder
			self.Folder.Copy(source_folder, destination_folder)

	def Show_Information(self):
		# Show a ten dash space separator
		print()
		print(self.separators["10"])
		print()

		# ---------- #

		# Define the tab variable as only one tab
		tab = "\t"

		# Show the "Current year" text in the user language and the current year number with the tab
		print(self.Language.language_texts["current_year"] + ":")
		print(tab + str(self.date["Units"]["Year"]))
		print()

		# ---------- #

		# Define the text to show initially as the text which says the current year already exists in the years folder
		text_to_show = self.language_texts["the_current_year_already_exists_in_the_years_folder"]

		# If "Current year folder exists" state is False
		# (The current year did not existed in the years folder)
		if self.verify["States"]["Current year folder exists"] == False:
			# Change the text to show to the text which says the current year did not existed in the years folder
			text_to_show = self.language_texts["the_current_year_did_not_existed_in_the_years_folder"]

		# Show the "Status of the year folder" text in the user language and the text to show with the tab
		print(self.language_texts["status_of_the_year_folder"] + ":")
		print(tab + text_to_show)
		print()

		# ---------- #

		# Define the text to show initially as the text which talks about the year folder
		text_to_show = self.language_texts["this_is_its_year_folder"]

		# If "Current year folder exists" state is False
		# (The current year did not existed in the years folder)
		if self.verify["States"]["Current year folder exists"] == False:
			# Change the text to show to the text which says the year folder was created
			text_to_show = self.language_texts["its_year_folder_was_created"]

		# Show the text above and the current year folder
		print(text_to_show + ":")
		print(tab + self.years["Current year"]["Folders"]["Text"]["root"])
		print()

		# ---------- #

		# Show the "Image folder of the year" and the year image folder
		print(self.language_texts["image_folder_of_the_year"] + ":")
		print(tab + self.years["Current year"]["Folders"]["Image"]["root"])

		# ---------- #

		# If "Current year folder exists" state is False
		# (The current year did not existed in the years folder)
		if self.verify["States"]["Current year folder exists"] == False:
			# Show the "Texts" text in the user language
			print()
			print(self.Language.language_texts["texts, title()"] + ":")

			# Define the double tab variable as two tabs
			double_tab = tab + "\t"

			# Iterate through the file keys and dictionaries inside the "Dictionary" of the root "Files" dictionary
			for key, dictionary in self.verify["Files"]["Dictionary"].items():
				# List the languages inside the "Files" dictionary
				languages = list(dictionary["Files"].keys())

				# Iterate through the local list of small languages
				for language in languages:
					# Get the file in the current language
					file = dictionary["Files"][language]

					# Get the text to write in the current language
					text_to_write = dictionary["Text to write"][language]

					# If the text to write is not empty
					if text_to_write != "":
						# Show the dictionary text in the current language with a tab
						print(tab + '"' + dictionary["Texts"][language] + '":')

						# Get the lines of the text to write
						lines = text_to_write.splitlines()

						# Get the number of lines
						number_of_lines = len(lines)

						# If the number of lines inside the text to write is only one
						if number_of_lines == 1:
							# Define the text template to show only one line and a double tab
							text_template = double_tab + "{}"

							# Define the file text as the first line plus a line break
							file_text = lines[0] + "\n"

						# If the number of lines inside the text to write are multiple
						if number_of_lines > 1:
							# Define the text template to show multiple lines with a tab
							text_template = tab + "[" + "\n" + \
							"{}" + \
							"\n" + \
							tab + "]" + "\n"

							# Define a local line number
							line_number = 0

							# Iterate through the list of file lines
							for line in lines:
								# Update the lines to add the double tab and the pipe
								lines[line_number] = double_tab + "| " + line

								# Add one to the local line number
								line_number += 1

							# Define the text as the list of lines converted into a text
							file_text = self.Text.From_List(lines)

						# Format the text template with the text
						file_text = text_template.format(file_text)

						# Show the file text
						print(file_text)

			# ---------- #

			# Define the triple tab variable as three tabs
			triple_tab = double_tab + "\t"

			# Show the "Social networks texts" text in the user language
			print()
			print(self.Language.language_texts["social_networks_texts"] + ":")

			# Iterate through the keys and dictionaries of the social network lists
			for key, dictionary in self.verify["Social network files"]["Dictionary"].items():
				# Show the dictionary name in the user language with a tab
				print(tab + dictionary["Name"][self.language["Small"]] + ":")

				# Get the dictionary of social networks
				social_networks = dictionary["Dictionary"]

				# Iterate through the social network dictionaries inside the defined dictionary
				for social_network in social_networks.values():
					# Get the social network file
					file = social_network["File"]

					# Get the text to write
					text_to_write = social_network["Text to write"]

					# If the list of lines is not empty
					if lines != []:
						# Show the social network name in the user language with a double tab
						print(double_tab + '"' + social_network["Name"][self.language["Small"]] + '":')

						# Get the lines of the text to write
						lines = text_to_write.splitlines()

						# Get the number of lines
						number_of_lines = len(lines)

						# If the number of lines inside the text to write is only one
						if number_of_lines == 1:
							# Define the text template to show only one line and a triple tab
							text_template = triple_tab + "{}"

							# Define the file text as the first line plus a line break
							file_text = lines[0] + "\n"

						# If the number of lines inside the text to write are multiple
						if number_of_lines > 1:
							# Define the text template to show multiple lines with a double tab
							text_template = double_tab + "[" + "\n" + \
							"{}" + \
							"\n" + \
							double_tab + "]" + "\n"

							# Define a local line number
							line_number = 0

							# Iterate through the list of file lines
							for line in lines:
								# Update the lines to add the triple tab and the pipe
								lines[line_number] = triple_tab + "| " + line

								# Add one to the local line number
								line_number += 1

							# Define the text as the list of lines converted into a text
							file_text = self.Text.From_List(lines)

						# Format the text template with the text
						file_text = text_template.format(file_text)

						# Show the file text
						print(file_text)

		# If the current year already existed in the years folder
		else:
			# Show a space separator
			print()

		# ---------- #

		# Show a ten dash space separator
		print(self.separators["10"])

		# If "Current year folder exists" state is False
		# (The current year did not existed in the years folder)
		if self.verify["States"]["Current year folder exists"] == False:
			# Re-initiate the root class to update the year files
			super().__init__()