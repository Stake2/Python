# Write_On_Diary_Slim.py

from Diary_Slim.Diary_Slim import Diary_Slim as Diary_Slim

from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

class Write_On_Diary_Slim(Diary_Slim):
	def __init__(self):
		super().__init__()

		# Define the root dictionary
		self.dictionary = {
			"Text": {},
			"Text to write": ""
		}

		# Define the States dictionary
		self.states = {
			"Multi-selection": False
		}

		# Select the Diary Slim text
		self.Select_The_Text()

		# If the "Item" key is inside the text dictionary
		if "Item" in self.dictionary["Text"]:
			# Define the text item variables
			self.Define_Item_Variables()

		# If the text key is inside the root "Statistics" dictionary
		if self.dictionary["Text"]["Key"] in self.statistics["Dictionary"]:
			# Run the method to manage statistics
			self.Manage_Statistic()

		# Write the Diary Slim text
		self.Write()

	def Select_The_Text(self):
		from copy import deepcopy

		global parameters

		# Define the parameters dictionary to use inside the "Select" method of the "Input" utility module
		parameters = {
			"options": deepcopy(self.diary_slim["Texts"]["Options"]["Keys"]),
			"language_options": deepcopy(self.diary_slim["Texts"]["Options"][self.user_language]),
			"show_text": self.language_texts["texts_to_write"],
			"select_text": self.language_texts["select_a_text_to_write"]
		}

		# Change the index of the Diary Slim Texts dictionary if the text has a custom index
		for key in self.diary_slim["Texts"]["Options"]["Keys"]:
			# Get the Text dictionary
			dictionary = self.diary_slim["Texts"]["Dictionary"][key]

			# Get the user language text
			text = dictionary["Texts"][self.user_language]

			# If the "Index" key is inside the dictionary
			if "Index" in dictionary:
				# Get the correct index
				index = dictionary["Index"] - 1

				# If the index is "-1", use the last index (the text will be the last one)
				if index == -1:
					index = len(options) - 1

				# Remove the key and insert it at the correct index
				parameters["options"].remove(key)
				parameters["options"].insert(index, key)

				# Remove the language text and insert it at the correct index
				parameters["language_options"].remove(text)
				parameters["language_options"].insert(index, text)

			# Remove the option if the "Multi-selection" mode is activated
			# And the "Item" key is present inside the Text dictionary
			if (
				self.states["Multi-selection"] == True and
				"Item" in dictionary
			):
				parameters["options"].remove(key)
				parameters["language_options"].remove(text)

		# Add the "[Multi-selection]" option if its mode is deactivated
		if self.states["Multi-selection"] == False:
			# Add the "[Multi-selection]" text to the list of options
			parameters["options"].append("[Multi-selection]")

			# Get the language text
			language_text = "[" + self.Language.language_texts["multi_selection"] + "]"

			# Add the "[Multi-selection]" text in the user language to the list of language options
			parameters["language_options"].append(language_text)

		# If the "Multi-selection" mode is activated
		# And the Diary Slim text is not a statistic
		if (
			self.states["Multi-selection"] == True and
			self.dictionary["Text"]["Is statistic"] == True
		):
			# Run the "Multi_Selection" method
			self.Multi_Selection()

		# If the "Multi-selection" mode is deactivated
		if self.states["Multi-selection"] == False:
			# Ask the user to select the Diary Slim text
			option = self.Input.Select(**parameters)["option"]

			# If the option is not "[Multi-selection]" one
			if option != "[Multi-selection]":
				# Define the "Text" dictionary inside the root dictionary
				self.dictionary["Text"] = self.diary_slim["Texts"]["Dictionary"][option]

				# Define the "Text to write" as the language text
				self.dictionary["Text to write"] = self.dictionary["Text"]["Texts"][self.user_language]

				# If the "States" key is inside the "Text" dictionary
				if "States" in self.dictionary["Text"]:
					# Get the current state
					self.dictionary["Text to write"] = self.dictionary["Text"]["States"]["Current state"][self.user_language]

			# If the option is the "[Multi-selection]" one
			if option == "[Multi-selection]":
				# Change the "Multi-selection" mode to activated
				self.states["Multi-selection"] = True

				# Run this method again to run it with the "Multi-selection" mode activated
				self.Select_The_Text()

		# If the "Multi-selection" mode is deactivated
		if self.states["Multi-selection"] == False:
			# If the "States" key is inside the "Text" dictionary
			if "States" in self.dictionary["Text"]:
				# Change the current state to the next state
				self.Next_State(self.dictionary["Text"])

			# If the "Additional information" key is inside the "Text" dictionary
			if "Additional information" in self.dictionary["Text"]:
				# Define the additional information and update the text to write
				self.dictionary["Text to write"] = self.Define_Additional_Information(self.dictionary)["Text"]

	def Multi_Selection(self):
		# Add the "[Finish selection]" text to the list of options
		parameters["options"].append("[Finish selection]")

		# Define the language texxt
		language_text = "[" + self.Language.language_texts["finish_selection"] + "]"

		# Add the "[Finish selection]" text in the user language to the list of language options
		parameters["language_options"].append(language_text)

		# Define the option as an empty string
		option = ""

		# Define the empty texts list
		texts = []

		# Define the "finish selection" variable for easier typing
		finish_selection = "[Finish selection]"

		# While the option is not the "[Finish selection]" text
		while option != finish_selection:
			# Show a five dash space separator
			print()
			print(self.separators["5"])

			# If the list of texts is not empty
			if texts != []:
				# Show the "List:" text
				print()
				print(self.Language.language_texts["list, title()"] + ":")

				# Show the list of texts
				print("[")

				# Iterate through the texts in the list
				for text in texts:
					# Make a backup of the text
					text_backup = text

					# Add one tab to the text
					text = text.replace("\n", "\n\t")

					# Show the text with a tab and quotes around it
					print("\t" + '"' + text + '"')

					# If the text backup is not the last one, show a space separator
					if text_backup != texts[-1]:
						print()

				# Show the end of the list
				print("]")

			# Ask the user to select the Diary Slim text
			option = self.Input.Select(**parameters)["option"]

			# If the option is not the "[Finish selection]" text
			if option != finish_selection:
				# Define the "Text" dictionary inside the root dictionary
				self.dictionary["Text"] = self.diary_slim["Texts"]["Dictionary"][option]

				# Remove the selected text from the parameters dictionary
				parameters["options"].remove(option)
				parameters["language_options"].remove(self.dictionary["Text"]["Texts"][self.user_language])

				# Add two line breaks if the text is not the first one
				if texts != []:
					self.dictionary["Text to write"] += "\n\n"

				# Define the language text
				language_text = self.dictionary["Text"]["Texts"][self.user_language]

				# If the "States" key is inside the "Text" dictionary
				if "States" in self.dictionary["Text"]:
					# Get the current state
					language_text = self.dictionary["Text"]["States"]["Current state"][self.user_language]

					# Change the current state to the next state
					self.Next_State(self.dictionary["Text"])

				# If the "Additional information" key is inside the "Text" dictionary
				if "Additional information" in self.dictionary["Text"]:
					# Define the additional information and update the text to write
					language_text = self.Define_Additional_Information(self.dictionary, language_text)["Text"]

				# Add the language text to the "Text to write" string
				self.dictionary["Text to write"] += language_text

				# Add a period to the end of the text if it is not present
				if "." not in self.dictionary["Text to write"][-1]:
					self.dictionary["Text to write"] += "."

				# Replace the line break characters (\n) inside the language text with real line breaks
				language_text = language_text.replace("\n", "\n")

				# Add the language text to the texts list
				texts.append(language_text)

	def Define_Item_Variables(self):
		# Remove the "..." (three dots) text if it is present inside the text
		if "..." in self.dictionary["Text"]["Texts"][self.user_language]:
			for language in self.languages["small"]:
				self.dictionary["Text"]["Texts"][language] = self.dictionary["Text"]["Texts"][language].replace("...", "")

		# Ask for the text data if the text has a type text
		if "Type text" in self.dictionary["Text"]:
			# Show a five dash space separator
			print()
			print(self.separators["5"])

			# Show the text in the user language
			print()
			print(self.dictionary["Text"]["Texts"][self.user_language] + ":")

			# Define the "Data" dictionary
			self.dictionary["Text"]["Data"] = {}

			# If the "Options" key is not inside the Text dictionary
			# That means the user must type the data (string)
			# And not select it (from a list of options)
			if "Options" not in self.dictionary["Text"]:
				# Iterate through the small languages list
				for language in self.languages["small"]:
					# Get the translated language in the user language
					translated_language = self.languages["full_translated"][language][self.user_language]

					# Define the type text
					type_text = self.language_texts[self.dictionary["Text"]["Type text"]] + " " + self.Language.language_texts["genders, type: dict"]["in"] + " " + translated_language

					# Ask the user to type the data in each language
					self.dictionary["Text"]["Data"][language] = self.Input.Type(type_text)

			# If the "Options" key is inside the Text dictionary
			# That means the user must select the data from a list of options
			if "Options" in self.dictionary["Text"]:
				# Define the list of options
				options = self.dictionary["Text"]["Options"]

				# Define the text key variable
				text_key = options["Show text"]

				# Add the ", title()" text if the text key does not contain underscores
				if "_" not in text_key:
					text_key += ", title()"

				# Get the show text using the text key
				show_text = self.Language.language_texts[text_key]

				# Ask the user to select an option from the list of options
				self.dictionary["Text"]["Data"][self.user_language] = self.Input.Select(options["List"], show_text = show_text)["option"]

				# If the "Format" key is inside the "Options" dictionary
				if "Format" in options:
					# Define the item key
					item_key = "{" + self.dictionary["Text"]["Item"] + "}"

					# If the "Genders" key exist inside the "Format" dictionary
					if "Genders" in options["Format"]:
						# Iterate through the text keys inside the list of keys
						for text_key in options["Format"]["Keys"]:
							# Get the text from the text key and add curly brackets
							text = "{" + self.Language.language_texts[text_key] + "}"

							# If the item text is not inside the key
							if self.dictionary["Text"]["Item"] not in text_key:
								# Define that key as the gender text key
								gender_text_key = text

							# If the text is inside the Diary Slim text
							if text in self.dictionary["Text"]["Texts"][self.user_language]:
								# Define the item key as the text key
								item_key = text

					# Define the data
					data = self.dictionary["Text"]["Data"][self.user_language]

					# Replace the key with the selected data
					self.dictionary["Text"]["Texts"][self.user_language] = self.dictionary["Text"]["Texts"][self.user_language].replace(item_key, data)

					# If the "Gender text" key is inside the text
					if gender_text_key in self.dictionary["Text"]["Texts"][self.user_language]:
						# Iterate through the list of genders
						for gender in ["Masculine", "Feminine"]:
							# If the data is inside the gender list of the current gender
							if data in options[gender]:
								# Get the gender text key from the "Format" dictionary, for the current gender
								text_key = options["Format"]["Genders"][gender.lower()]

								# Get the text
								text = self.Language.language_texts[text_key]

								# Replace the gender text template inside the text with the correct gender text
								self.dictionary["Text"]["Texts"][self.user_language] = self.dictionary["Text"]["Texts"][self.user_language].replace(gender_text_key, text)

					# Update the text to write
					self.dictionary["Text to write"] = self.dictionary["Text"]["Texts"][self.user_language]

			# Iterate through the small languages list
			for language in self.languages["small"]:
				# If the language is not inside the "Data" dictionary
				if language not in self.dictionary["Text"]["Data"]:
					# Define it as the data in the user language
					self.dictionary["Text"]["Data"][language] = self.dictionary["Text"]["Data"][self.user_language]

			# Split the text data items into a list if the data contains a comma and a space
			# Add commas between the items, and add the "and " text before the last item
			if ", " in self.dictionary["Text"]["Data"][self.user_language]:
				# Iterate through the small languages list
				for language in self.languages["small"]:
					# Split the text data with a comma and a space
					split = self.dictionary["Text"]["Data"][language].split(", ")

					# Define the text data as an empty string in the current language
					self.dictionary["Text"]["Data"][language] = ""

					# Iterate through the list of items of the text data
					for item in split:
						# If the item is not the first one
						# And the number of items is two
						if (
							item != split[0] and
							len(split) == 2
						):
							# Add a space to separate items
							self.dictionary["Text"]["Data"][language] += " "

						# If the item is the last one
						if item == split[-1]:
							# Add the "and " text before the last item
							self.dictionary["Text"]["Data"][language] += self.Language.texts["and"][language] + " "

						# Add the item
						self.dictionary["Text"]["Data"][language] += item

						# If the item is not the last one
						# And the number of items is not two
						if (
							item != split[-1] and
							len(split) != 2
						):
							# Add a comma and a space to separate the items
							self.dictionary["Text"]["Data"][language] += ", "

					# Replace the singular name with the plural name on the text
					if "Plural" in self.dictionary["Text"]["Descriptions"]:
						# Define the variables for easier typing
						singular = self.dictionary["Text"]["Descriptions"]["Singular"]
						plural = self.dictionary["Text"]["Descriptions"]["Plural"]

						replace_ = self.texts[singular][language]
						with_ = self.texts[plural][language]

						# Replace singular with plural
						self.dictionary["Text"]["Texts"][language] = self.dictionary["Text"]["Texts"][language].replace(replace_, with_)

				# Replace the "Explanation text" with the plural version
				self.dictionary["Text"]["Explanation text"] = "say_what_you_did_on_the_{}, plural"

				# Define the text item as the plural item
				self.dictionary["Text"]["Item"] = self.dictionary["Text"]["Items"]["Plural"]

			# If the text does not use a simple format (has task registration)
			if "Simple format" not in self.dictionary["Text"]:
				# If the text data does not contain a comma and a space
				if ", " not in self.dictionary["Text"]["Data"][self.user_language]:
					# If the "Quotes" setting is True
					if self.dictionary["Text"]["Quotes"] == True:
						# Iterate through the small languages list
						for language in self.languages["small"]:
							# Add quotes to the text data
							self.dictionary["Text"]["Data"][language] = '"' + self.dictionary["Text"]["Data"][language] + '"'

				# Iterate through the small languages list
				for language in self.languages["small"]:
					# Add a space and the text data to the texts dictionary
					self.dictionary["Text"]["Texts"][language] += " " + self.dictionary["Text"]["Data"][language]

		# If the text does not use a simple format (has task registration)
		if "Simple format" not in self.dictionary["Text"]:
			# Show a three dash space separator
			print()
			print(self.separators["3"])

			# Ask for the user to type the task descriptions
			# It is because all Diary Slim texts that contain the "Item" key are also tasks that can be registered
			# They can be registered using the "Tasks" Python module, and its "Register" sub-class
			self.Type_Task_Descriptions()

	def Type_Task_Descriptions(self):
		# Define the Task dictionary
		# With the task type, titles, descriptions, entry date, and files
		self.task_dictionary = {
			"Type": self.dictionary["Text"]["Key"],
			"Task": {
				"Titles": {},
				"Descriptions": {}
			},
			"Entry": {
				"Date": self.Date.Now()
			},
			"Files": {}
		}

		# Show the explanation text about opening the description files for the user to type on them
		print()
		print(self.language_texts["opening_the_description_files_for_you_to_type_on_them, type: explanation"])

		# Define the explanation text of the task
		explanation_text = self.language_texts[self.dictionary["Text"]["Explanation text"]]

		# Format it with the item of the text
		explanation_text = explanation_text.format(self.language_texts[self.dictionary["Text"]["Item"]])

		# Show the explanation text of the text (task)
		print()
		print(explanation_text + ".")

		# Iterate through the small languages list
		for language in self.languages["small"]:
			# Get the full language
			full_language = self.languages["full"][language]

			# Define the task description file in the current language
			self.task_dictionary["Files"][language] = self.folders["Notepad"]["Diary Slim"]["root"] + full_language + ".txt"

			# Create the file
			self.File.Create(self.task_dictionary["Files"][language])

		# Define the empty languages text
		languages_text = ""

		# Define the translated languages list
		translated_languages = []

		# Iterate through the small languages list
		for language in self.languages["small"]:
			# Get the translated language in the user language
			translated_language = self.languages["full_translated"][language][self.user_language]

			# Add the translated language to the list
			translated_languages.append(translated_language)

		# Create the translated languages text
		languages_text = self.Text.From_List(translated_languages)

		# Iterate through the small languages list
		for language in self.languages["small"]:
			# Open the task description file in the current language
			self.System.Open(self.task_dictionary["Files"][language])

		# Wait for the user to finish writing the task descriptions
		self.Input.Type(self.language_texts["press_enter_when_you_finish_writing_and_saving_the_description_in_{}"].format(languages_text))

		# Define and create the backup file
		self.task_dictionary["Files"]["Backup"] = self.folders["Notepad"]["Diary Slim"]["root"] + "Descriptions backup.txt"
		self.File.Create(self.task_dictionary["Files"]["Backup"])

		# Iterate through the small languages list
		for language in self.languages["small"]:
			# Define the task title in the current language as the Diary Slim text
			self.task_dictionary["Task"]["Titles"][language] = self.dictionary["Text"]["Texts"][language]

			# Define the task description in the current language as the task title with a period and two line breaks
			self.task_dictionary["Task"]["Descriptions"][language] = self.task_dictionary["Task"]["Titles"][language] + "." + "\n\n"

			# If the "testing" switch is False
			if self.switches["Testing"] == False:
				# Add the contents of the description file in the current language to the task description
				self.task_dictionary["Task"]["Descriptions"][language] += self.File.Contents(self.task_dictionary["Files"][language])["string"]

			# If the "testing" switch is True
			else:
				# Add the "[Description]" text in the current language to the task description
				self.task_dictionary["Task"]["Descriptions"][language] += "[" + self.Language.texts["description, title()"][language] + "]"

			# Define the text to add to the backup file as the task description in the current language
			text = self.task_dictionary["Task"]["Descriptions"][language]

			# If the language is not the last one, add two line breaks to the text
			if language != self.languages["small"][-1]:
				text += "\n\n"

			# Make the backup of the task description
			self.File.Edit(self.task_dictionary["Files"]["Backup"], text, "a", next_line = False)

			# Delete the description file in the current language
			self.File.Delete(self.task_dictionary["Files"][language])

	def Manage_Statistic(self):
		# Define the key
		text_key = self.dictionary["Text"]["Key"]

		# Get the statistic
		statistic = self.statistics["Dictionary"][text_key]

		# Define the information dictionary
		information = statistic

		# If the "Question" key is inside the statistic dictionary
		if "Question" in statistic:
			# Define the information about the statistic
			information = self.Define_Additional_Information(statistic, is_statistic = True)["Statistic"]

		# Get the statistic dictionary of the Diary Slim text, in the current year
		current_year_statistics = self.diary_slim["Current year"]["Statistics"][text_key]

		# ---------- #

		# Define the statistic text key
		statistic_text_key = statistic["Key"].replace(" ", "_").lower()

		# Define the statistic text if the key exists inside the language texts dictionary of the "Language" class
		if statistic_text_key in self.Language.language_texts:
			text = self.Language.language_texts[statistic_text_key]

		else:
			text = statistic["Key"]

		# If the "Data" is inside the Diary Slim text dictionary
		if "Data" in self.dictionary["Text"]:
			# Get the text from it
			text = self.dictionary["Text"]["Data"][self.user_language]

		# If the "Statistic text" is inside the Diary Slim text dictionary
		if "Statistic text" in self.dictionary["Text"]:
			text = self.dictionary["Text"]["Statistic text"][self.user_language]

		# Add to the statistic numbers of the current year

		# If the text key is inside the statistics dictionary of the current year
		if text_key in self.diary_slim["Current year"]["Statistics"]:
			# Define the statistic key as the key inside the statistic dictionary
			statistic_key = statistic["Key"]

		# If the "Data" key is inside the Diary Slim text dictionary
		if "Data" in self.dictionary["Text"]:
			# Get the data to use as a key
			data_key = self.dictionary["Text"]["Data"][self.user_language]

			# Define the statistic key
			statistic_key = data_key

		# Define the "Statistics" dictionary inside the Diary Slim text dictionary
		self.dictionary["Text"]["Statistics"] = {
			"Number": 0,
			"Dictionary": {
				statistic["Key"]: {
					"Text": text,
					"Old number": current_year_statistics[statistic_key],
					"Number": current_year_statistics[statistic_key]
				}
			},
			"Changed statistic": False
		}

		# Define the number to add as one
		number = 1

		# If the "Question" key is inside the statistic dictionary
		if "Question" in statistic:
			# Get the response
			response = information["Response"]

			# If the response is a number
			if response.isdigit() == True:
				# Define the number to add as the response
				number = int(response)

			# If the response is "No" or "0"
			if response in ["No", 0, "0"]:
				# Define the number as zero
				number = 0

			# If the "Questions" key is inside the statistic dictionary
			if "Questions" in statistic:
				# Iterate through the responses
				for key, answer in response.items():
					# Save the old number
					old_number = current_year_statistics[key]

					# Add the answer to the statistic using the response/question key
					current_year_statistics[key] += answer

					# Add the key to the statistic dictionary inside the Diary Slim dictionary
					self.dictionary["Text"]["Statistics"]["Dictionary"][key] = {
						"Text": self.language_texts[key.replace(" ", "_").lower()],
						"Old number": old_number,
						"Number": current_year_statistics[key]
					}

		# Update the number of statistics
		self.dictionary["Text"]["Statistics"]["Number"] = len(list(self.dictionary["Text"]["Statistics"]["Dictionary"].keys()))

		# Add the defined number to the defined statistic key
		current_year_statistics[statistic_key] += number

		# Update the number inside the statistics dictionary inside the Diary Slim text dictionary
		self.dictionary["Text"]["Statistics"]["Dictionary"][statistic["Key"]]["Number"] = current_year_statistics[statistic_key]

		# If the old number is not the same as the new number
		old_number = self.dictionary["Text"]["Statistics"]["Dictionary"][statistic["Key"]]["Old number"]
		new_number = self.dictionary["Text"]["Statistics"]["Dictionary"][statistic["Key"]]["Number"]

		if old_number != new_number:
			# Change the "Changed statistic" to True
			self.dictionary["Text"]["Statistics"]["Changed statistic"] = True

		# If the "Text decorator" is inside the Diary Slim text dictionary
		if "Text decorator" in self.dictionary["Text"]:
			# Define a shortcut for the text decorator
			text_decorator = self.dictionary["Text"]["Text decorator"]

			# Get the decorator key and text
			key = text_decorator["Key"]
			decorator_text = self.Language.language_texts[key]

			# Format the text

			# Replace the text template
			text = text_decorator["Format"].replace("{text}", decorator_text)

			# Replace the data template
			text = text.replace("{data}", self.dictionary["Text"]["Data"][self.user_language])

			# Update the statistic text to be the local text
			self.dictionary["Text"]["Statistics"]["Dictionary"][statistic["Key"]]["Text"] = text

		# Update the statistics of the current year
		self.Update_Current_Year_Statistics(self.diary_slim["Current year"]["Statistics"])

	def Write(self):
		# If the "Item" key is inside the text dictionary
		# And the "Simple format" key is not inside it
		if (
			"Item" in self.dictionary["Text"] and
			"Simple format" not in self.dictionary["Text"]
		):
			# Import the "Register" class of the "Tasks" module
			from Tasks.Register import Register as Register

			# Run the "Register" class with the local Task dictionary
			Register(self.task_dictionary)

			# Delete the task description backup file
			self.File.Delete(self.task_dictionary["Files"]["Backup"])

		# If the "Item" key is not inside the text dictionary
		# (That means the "Register" sub-class of the "Tasks" class was not executed and did not wrote on Diary Slim
		# So this class needs to write on it)
		# Or the "Item" key is inside the text dictionary
		# And the "Simple format" key is inside it
		if (
			"Item" not in self.dictionary["Text"] or
			"Item" in self.dictionary["Text"] and
			"Simple format" in self.dictionary["Text"]
		):
			# Add a period to the end of the text if it is not present
			if "." not in self.dictionary["Text to write"][-1]:
				self.dictionary["Text to write"] += "."

			# Show a space separator
			print()

			# Define the "Write on Diary Slim" dictionary
			dictionary = {
				"Text": self.dictionary["Text to write"]
			}

			# Write the text on Diary Slim
			Write_On_Diary_Slim_Module(dictionary)

		# If the "Is statistic" state is True
		# And the "Changed statistic" is True
		if (
			self.dictionary["Text"]["Is statistic"] == True and
			self.dictionary["Text"]["Statistics"]["Changed statistic"] == True
		):
			# Define the statistic text to show as singular or plural depending on the number
			number = self.dictionary["Text"]["Statistics"]["Number"]
			singular = self.Language.language_texts["updated_statistic"]
			plural = self.Language.language_texts["updated_statistics"]

			show_text = self.Text.By_Number(number, singular, plural)

			# Show the text
			print()
			print(show_text + ":")

			# Iterate through the dictionary of statistics
			for statistic in self.dictionary["Text"]["Statistics"]["Dictionary"].values():
				# Define the text with the statistic text and colon
				text = statistic["Text"]

				# Add the "in [year]" text
				text += " " + self.Language.language_texts["in"] + " " + str(self.diary_slim["Current year"]["Number"])

				# Add a colon
				text += ": "

				# Add the current number of the statistic
				text += str(statistic["Number"])

				# Add the old number with the "before" text
				text += " (" + self.Language.language_texts["before, title()"].lower() + ": " + str(statistic["Old number"]) + ")"

				# Show the text and number with a tab
				print("\t" + text)

		# Open the current Diary Slim file
		self.System.Open(self.diary_slim["Current year"]["Current Diary Slim file"], verbose = False)

		# Show a five dash space separator
		print()
		print(self.separators["5"])