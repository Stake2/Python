# Show_Year_Information.py

# Import the root class
from Years.Years import Years as Years

# Import some useful modules
from copy import deepcopy

class Show_Year_Information(Years):
	def __init__(self):
		# Run the root class to import its methods and variables
		super().__init__()

		# Ask the user to select the year to show its information
		self.Select_The_Year()

		# Show information about the year
		self.Show_Information()

	def Select_The_Year(self):
		# Show a ten dash space separator
		print()
		print(self.separators["10"])

		# Define the select text as "Select a year to show its information" in the user language
		select_text = self.language_texts["select_a_year_to_show_its_information"]

		# Ask the user to select a year
		self.year = self.Select_Year(select_text = select_text)

	def Define_Text(self, key, language = None, folder_item_names = None, sub_key = None):
		# Define the text as the key
		text = key

		# If the key is inside the list of full languages
		if key in self.languages["Full"]:
			# Define the text as the full language
			text = self.languages["Full"][key]

		# If the "language" parameter is None
		if language == None:
			# Define the language as the user language
			language = self.language["Small"]

		# Create the text key for the key
		text_key = key.lower().replace(" ", "_")

		# If the underscore character is not inside the text key
		if "_" not in text_key:
			# Add the ", title()" text
			text_key += ", title()"

		# If the text key is inside the "texts" dictionary of the "Language" utility class
		if text_key in self.Language.texts:
			# Define the text as the text inside that key and the language key
			text = self.Language.texts[text_key][language]

		# If the "folder item names" parameter is not None
		# And the sub-key is inside that dictionary
		if (
			folder_item_names != None and
			sub_key in folder_item_names
		):
			# Define the text as the sub-key and user language key inside that dictionary
			text = folder_item_names[sub_key][language]

		# If the sub-key is not None
		if sub_key != None:
			# Define a dictionary of folder keys to iterate through
			folder_keys = {
				"Root": [
					"Root",
					"Language",
					"Christmas",
					"New Year"
				],
				"Additional items": [
					"Planning",
					"Merry Christmas"
				]
			}

			# Iterate through the folder key dictionaries
			for folder_key, items in folder_keys.items():
				# Iterate through the items inside the dictionary
				for item in items:
					# If the folder key is "Root", then create a shortcut to the root "Folder item names" dictionary
					if folder_key == "Root":
						folder_item_names = self.years["Folder item names"][item]["Files"]["Dictionary"]

					# If the folder key is "Additional items", then create a shortcut to the "Additional items" dictionary of the "Folder item names" dictionary
					if folder_key == "Additional items":
						folder_item_names = self.years["Folder item names"]["Additional items"]["Christmas"][item]["Files"]["Dictionary"]

					# If the sub-key is inside the local "Folder item names" dictionary
					if sub_key in folder_item_names:
						# Define the text as the sub-key and user language key inside that dictionary
						text = folder_item_names[sub_key][language]

		# Return the defined text
		return text

	def Show_Text(self, text, text_type, tab = ""):
		# Define the text to show as the tab
		text_to_show = tab

		# Add the text
		text_to_show += text

		# Get the text key from the text type
		text_key = text_type.lower().replace(" ", "_")

		# If the text type is not "File"
		if text_type != "File":
			# Add the " ([text_type])" text
			text_to_show += " (" + self.Language.language_texts[text_key] + ")"

		# If the text type is "File"
		if text_type == "File":
			# Add the ".txt" text
			text_to_show += ".txt"

		# Show the text to show
		print(text_to_show + ":")

	def Show_File_Text(self, text, file, file_tab = "\t", text_tab = "\t", define_text = True):
		# If the "define text" parameter is True
		if define_text == True:
			# Define the text
			text = self.Define_Text(text)

		# Show the "File" text
		self.Show_Text(text, "File", text_tab)

		# Get the lines of the file
		lines = self.File.Contents(file)["Lines"]

		# Define the separator text as tab and a pipe
		separator_text = file_tab + "| "

		# If the list of lines is not empty
		if lines != []:
			# Iterate through the list of lines
			for line in lines:
				# Show the separator text and the line
				print(separator_text + line)

		# If the list of lines is empty
		if lines == []:
			# Show the "[Empty]" text in the user language
			print(file_tab + "[" + self.Language.language_texts["empty, title()"] + "]")

	def Show_Information(self):
		# Show a ten dash space separator
		print()
		print(self.separators["10"])
		print()

		# Define the text template as the "Information about the year of {}" text in the user language
		text_template = self.language_texts["information_about_the_year_of_{}"]

		# Format it with the year number to create the text
		text = text_template.format(self.year["Number"])

		# Show the text
		print(text + ":")
		print()

		# Get the list the file keys
		file_keys = list(self.year["Files"].keys())

		# Define a list of keys to keep
		keys_to_keep = [
			"Text",
			"Created in",
			"Edited in"
		]

		# Iterate through the copy of the list of file keys
		for key in file_keys.copy():
			# If the key is not "Text"
			if key not in keys_to_keep:
				# Remove the key
				file_keys.remove(key)

		# Iterate through the list of file keys
		for key in file_keys:
			# Get the value
			value = self.year["Files"][key]

			# If the value is a string
			# And it exists as a file
			if (
				type(value) == str and
				self.File.Exists(value) == True
			):
				# If the key is the last one
				if key == file_keys[-1]:
					# Show a space separator
					print()

				# Show the "[text].txt" text and the file text
				self.Show_File_Text(key, value, file_tab = "", text_tab = "")

			# Define the sub-dictionary initially as None
			sub_dictionary = None

			# If the value is a dictionary
			if type(value) == dict:
				# Update the sub-dictionary to be the value
				sub_dictionary = value

				# If the sub-dictionary is a dictionary
				if type(sub_dictionary) == dict:
					# List the sub-dictionary keys
					sub_dictionary_keys = list(sub_dictionary.keys())

				# Iterate through the sub-keys and sub-dictionaries inside the value dictionary
				for sub_key, sub_dictionary in deepcopy(sub_dictionary).items():
					# Update the sub-dictionary to be the value in the sub-key
					sub_dictionary = value[sub_key]

					# If the sub-dictionary is a string
					# And it exists as a file
					# And the sub-key is not inside the list of sub-keys to keep
					# (That list contains files that are going to be show outside of this loop)
					if (
						type(sub_dictionary) == str and
						self.File.Exists(sub_dictionary) == True and
						sub_key not in keys_to_keep
					):
						# Create a shortcut to the "Folder item names" dictionary
						folder_item_names = self.years["Folder item names"]["Root"]["Files"]["Dictionary"]

						# Define the local language initally as None
						language = None

						# If the sub-key is inside the list of small languages
						if sub_key in self.languages["Small"]:
							# Define the local language as the sub-key
							language = sub_key

						# Define the text
						text = self.Define_Text(sub_key, language, folder_item_names)

						# Show the "[text].txt" text and the file text with two tabs before each line
						self.Show_File_Text(text, sub_dictionary, "\t\t", define_text = False)

						# If the sub-key is not the last one
						if sub_key != sub_dictionary_keys[-1]:
							# Show a space separator
							print()

					# If the sub-dictionary is a string
					# And the number of keys is not one
					if (
						type(sub_dictionary) == dict and
						len(sub_dictionary_keys) != 1
					):
						# Define the text
						text = self.Define_Text(sub_key, language = self.language["Small"])

						# Show the "[text] (primary folder)" text
						self.Show_Text(text, "Primary folder")

						# Iterate through the sub-sub-keys and sub-values inside the sub-dictionary
						for sub_sub_key, sub_value in sub_dictionary.items():
							# If the sub-value is a string
							# And it exists as a file
							if (
								type(sub_value) == str and
								self.File.Exists(sub_value) == True
							):
								# Define the local language initally as None
								language = None

								# If the sub-key is inside the list of small languages
								if sub_key in self.languages["Small"]:
									# Define the local language as the sub-key
									language = sub_key

								# If the key is inside the list of full languages
								if key in self.languages["Full"].values():
									# Find the key (small language) of the full language and define it as the language
									language = self.JSON.Find_Key(self.languages["Full"])

								# Define the text
								text = self.Define_Text(sub_sub_key, language, sub_key = sub_sub_key)

								# Show the "[text].txt" text and the file text with two tabs before each line
								self.Show_File_Text(text, sub_value, file_tab = "\t\t", define_text = False)

								# If the sub-sub-key is not the last one
								if sub_sub_key != sub_dictionary_keys[-1]:
									# Show a space separator
									print()

							# If the sub-value is a dictionary
							if type(sub_value) == dict:
								# Define the text
								text = self.Define_Text(sub_sub_key)

								# Show the "[text] (secondary folder)" text with a tab
								self.Show_Text(text, "Secondary folder", "\t")

								# List the sub-value keys
								sub_value_keys = list(sub_value.keys())

								# Iterate through the sub-sub-sub-keys and files inside the dictionary
								for sub_sub_sub_key, file in sub_value.items():
									# Define the local language initally as None
									language = None

									# If the sub-sub-sub-key is inside the list of small languages
									if sub_sub_sub_key in self.languages["Small"]:
										# Define the local language as the sub-sub-sub-key
										language = sub_sub_sub_key

									# Define the text
									text = self.Define_Text(sub_sub_sub_key, language, sub_key = sub_sub_sub_key)

									# Show the "[text] (file)" text and the file text with three tabs before each line
									self.Show_File_Text(text, file, file_tab = "\t\t\t", text_tab = "\t\t", define_text = False)

									# If the sub-sub-sub-key is not the last one
									# Or it is
									# And the sub-sub-key is not the last one
									if (
										sub_sub_sub_key != sub_value_keys[-1] or
										sub_sub_sub_key == sub_value_keys[-1] and
										sub_sub_key != sub_dictionary_keys[-1]
									):
										# Show a space separator
										print()