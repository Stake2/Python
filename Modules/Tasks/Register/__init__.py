# Register.py

from Tasks.Tasks import Tasks as Tasks

from copy import deepcopy

class Register(Tasks):
	def __init__(self, dictionary_parameter = {}, show_text = True):
		super().__init__()

		# Define the root dictionary on this class as the parameter dictionary
		self.dictionary = {
			"Type": {},
			"Questions": {
				"Questions": {},
				"Has questions": False
			},
			"Task": {
				"Name": {},
				"Titles": {},
				"Descriptions": {},
				"States": {
					"First task in year": False,
					"First task type task in year": False
				}
			},
			"Entry": {
				"Times": {}
			}
		}

		# ---------- #

		# Register the completed task time in the "Times" dictionary
		time_key = "Completed task"
		self.dictionary["Entry"]["Times"][time_key] = self.Date.Now()

		# Register the completed task time in the UTC time
		self.dictionary["Entry"]["Times"][time_key + " (UTC)"] = self.dictionary["Entry"]["Times"][time_key]

		# ---------- #

		# Define the states dictionary
		self.states = {
			"Used as module": False,
			# Indicates if the module is being used as a dependency in another place

			"Five dash space": True,
			# Indicates if the module should show a five dash space after showing the information about the registered task

			"Ask for input": True,
			# Ask for input after showing the information about the registered task

			"Register task": True
			# A state defining if the task is going to be registered
		}

		# If the parameter dictionary is not empty
		if dictionary_parameter != {}:
			# Define the "Used as module" state as True
			self.states["Used as module"] = True

		# If the "Register task" key is inside the parameter dictionary
		if "Register task" in dictionary_parameter:
			# Update the state inside the root states dictionary
			self.states["Register task"] = dictionary_parameter["Register task"]

		# ---------- #

		# Update the root dictionary with the parameter dictionary
		self.dictionary.update(dictionary_parameter)

		# ---------- #

		# If the type of the task type dictionary is a string
		if isinstance(self.dictionary["Type"], str):
			# Transform it into a task type dictionary, using the string as a key
			self.dictionary["Type"] = self.tasks["Types"]["Dictionary"][self.dictionary["Type"]]

		# Define the grammatical number key
		self.dictionary["Task"]["Grammatical number"] = "Singular"

		# ---------- #

		# If the task type dictionary is empty
		if self.dictionary["Type"] == {}:
			# Ask the user to select the task type
			self.Select_Task_Type()

		# ---------- #

		# If the task "Descriptions" dictionary is empty
		if self.dictionary["Task"]["Descriptions"] == {}:
			# Ask the user to type the task information
			self.Ask_For_Task_Information()

			# Ask the user to type the task descriptions
			self.Ask_For_Task_Descriptions()

		# ---------- #

		# Define a shortcut for the task dictionary
		self.task = self.dictionary["Task"]

		# If the "Descriptions" key is not inside the task dictionary
		if "Descriptions" not in self.task:
			# Define the descriptions dictionary as the titles dictionary
			self.task["Descriptions"] = self.task["Titles"]

		# ---------- #

		# Add the "Diary Slim" dictionary to the "Entry" dictionary
		self.dictionary["Entry"]["Diary Slim"] = {
			"Text": ""
		}

		# If the "States" key is not inside the root dictionary
		if "States" not in self.dictionary:
			# Add the key
			self.dictionary["States"] = {
				"States": {},
				"Texts": {}
			}

		# If the "Register task" state is True
		if self.states["Register task"] == True:
			# Save the entry to the database in the JSON format
			self.Register_In_JSON()

			# Create the individual entry file for the watched media
			self.Create_Entry_File()

			# Create the entry files inside their corresponding year folders
			self.Add_Entry_File_To_Year_Folder()

		# Write the task description in the user language on the current iary Slim
		self.Write_On_Diary_Slim()

		# Show information about the registered task
		# Passing the root dictionary and the states dictionary as parameters
		self.Show_Information(self.dictionary, self.states)

	def Select_Task_Type(self):
		# Define the list of options and language options
		options = self.tasks["Types"]["Lists"]["Plural"]["en"]
		language_options = self.tasks["Types"]["Lists"]["Plural"][self.language["Small"]]

		# Define the "t" variable for task type number
		type_number = 0

		# Iterate through the keys inside the task "Types" dictionary
		for task_type in self.tasks["Types"]["Dictionary"].values():
			# If the "Module-only" key is inside the task type dictionary
			if "Module-only" in task_type:
				# Remove the task type from the lists above
				options.pop(type_number)
				language_options.pop(type_number)

			# Add to the "type number" number
			type_number += 1

		# Define the show and select texts
		show_text = self.language_texts["task_types"]
		select_text = self.language_texts["select_a_task_type"]

		# Ask for the user to select a task type
		option = self.Input.Select(options, language_options = language_options, show_text = show_text, select_text = select_text)["Option"]["Original"]

		# Get the task type dictionary for the selected task type
		self.dictionary["Type"] = self.tasks["Types"]["Dictionary"][option]

	def Ask_For_Task_Information(self):
		# Iterate through the list of small languages
		for language in self.languages["Small"]:
			# Get the translated language in the user language
			translated_language = self.languages["Full (translated)"][language][self.language["Small"]]

			# Define the task text
			task_text = self.dictionary["Type"]["Task texts"]

			# If the "Register task" state is False
			if self.states["Register task"] == False:
				# Change the task text to the "Task progress text"
				task_text = self.dictionary["Type"]["Task progress text"]

			# Define the task title in the current language
			self.dictionary["Task"]["Titles"][language] = task_text[language]

		# If the class is being used as a module by another Python module
		if self.states["Used as module"] == True:
			# Show a five dash space separator
			print()
			print(self.separators["5"])

			# Show the "Class being executed" and the name of the module and class
			# So the user is sure that this is the Tasks module, not another one
			# "Tasks.Register()" (in the user language)
			print()
			print(self.Language.language_texts["class_being_executed"] + ":")
			print("\t" + self.language_texts["Tasks.Register"])

			# Show the task type
			print()
			print(self.language_texts["task_type"] + ":")
			print("\t" + self.dictionary["Type"]["Names"]["Plural"][self.language["Small"]])

		# If the "Register task" state is True
		if self.states["Register task"] == True:
			# Ask the questions to the user, getting the questions dictionary back
			# (Only if there are questions)
			self.dictionary["Questions"]["Questions"] = self.Ask_Questions(self.dictionary["Type"])

	def Ask_Questions(self, dictionary):
		# Define the default questions dictionary
		questions = {}

		# If there is only one question
		if "Question" in dictionary:
			# Define the first question as the only question that exists
			questions["1"] = {
				"Key": "1",
				**dictionary["Question"]
			}

			# Change the "Has questions" state to True
			self.dictionary["Questions"]["Has questions"] = True

		# If there are more questions
		if "Questions" in dictionary:
			# Re-define the questions dictionary as the one already inside the text dictionary
			questions = dictionary["Questions"]

			# Iterate through the questions inside the dictionary of questions, getting the key and question dictionary
			for key in questions:
				# Update the question dictionary inside the root questions dictionary
				questions[key] = {
					"Key": key,
					**questions[key]
				}

			# Change the "Has questions" state to True
			self.dictionary["Questions"]["Has questions"] = True

		# ---------- #

		# Iterate through the questions inside the dictionary, getting the key and question dictionary
		for key, question in questions.items():
			# If the question type is "Type"
			if question["Question type"] == "Type":
				# Get the input text
				question["Text"] = self.Define_Input_Text(question)

				# Define the response as an empty dictionary
				questions[key]["Response"] = {}

				# Iterate through the list of small languages
				for language in self.languages["Small"]:
					# Get the translated language in the user language
					translated_language = self.languages["Full (translated)"][language][self.language["Small"]]

					# Change the input text to add the current language
					question["Text"] = self.Define_Input_Text(question)

					# Add the "in" text
					question["Text"] += " " + self.Language.language_texts["in"] + " "

					# Add the current language but translated to the user language
					question["Text"] += translated_language

					# Ask for the response in the current language
					questions[key]["Response"][language] = self.Verify_Input(question)

			# ----- #

			# If the question type is "Select"
			if question["Question type"] == "Select":
				# Create the local texts dictionary with the show and select texts
				texts = {
					"Show": question["Show text"],
					"Select": question["Select text"]
				}

				# Iterate through the texts inside the dictionary above
				for item, value in texts.items():
					# Define the local language texts dictionary
					language_texts = self.Language.language_texts

					# If the value (text key) is inside the language texts dictionary of this module
					if value in self.language_texts:
						# Define the local language texts dictionary as that one
						language_texts = self.language_texts

					# If the value (text key) is inside the local list of language texts
					if value in language_texts:
						# Get the language text for the current value (text key)
						texts[item] = language_texts[value]

				# Get the user response
				questions[key]["Response"] = self.Input.Select(question["List"], show_text = texts["Show"], select_text = texts["Select"])["Option"]["Original"]

			# ----- #

			# Define the default value for the "Grammatical number" key on the "Task" dictionary
			self.dictionary["Task"]["Grammatical number"] = "Singular"

			# If the "Grammatical numbers" key is inside the question dictionary
			if "Grammatical numbers" in question:
				# Get the grammatical numbers for easier typing
				grammatical_numbers = question["Grammatical numbers"]

				# Split the response into a list
				items = question["Response"]["en"].split(", ")

				# Make a text from a list
				text = self.Text.From_List(items)

				# Get the number
				number = len(items)

				# Get the singular text key
				singular = grammatical_numbers["Singular"]

				# If the plural text is not inside the grammatical numbers dictionary
				if "Plural" not in grammatical_numbers:
					grammatical_numbers["Plural"] = singular + "s"

				# Get the plural text key
				plural = grammatical_numbers["Plural"]

				# Get the correct grammatical text key
				text_key = self.Text.By_Number(number, singular, plural)

				# Iterate through the list of small languages
				for language in self.languages["Small"]:
					# Transform the list of typed items into a text
					items = questions[key]["Response"][language].split(", ")

					typed_items = self.Text.From_List(items, language = language)

					# Get the language text
					text = self.texts[text_key][language]

					# Add the text to the response in the current language
					# 
					# Example:
					# Singular: "programming my module" + " " + [typed module]
					# Plural: "programming my modules" + " " + [typed modules]
					questions[key]["Response"][language] = text + " " + typed_items

				# If the number is greater than one
				if number > 1:
					# Define the grammatical number as plural
					self.dictionary["Task"]["Grammatical number"] = "Plural"

			# ----- #

			# If the "Format" key is inside the question dictionary
			if "Format" in question:
				# Iterate through the list of small languages
				for language in self.languages["Small"]:
					# Get the response
					response = questions[key]["Response"]

					# If the response is a dictionary
					if isinstance(response, dict):
						# Get the response in the current language
						response = response[language]

					# Define the task title
					task_title = self.dictionary["Task"]["Titles"][language]

					# If the format character "{}" is present in the task title in the current language
					if "{}" in task_title:
						# Format the task title
						task_title = task_title.format(response)

					# Update it in the root titles dictionary
					self.dictionary["Task"]["Titles"][language] = task_title

		# Return the questions
		return questions

	def Define_Input_Text(self, question):
		# Define the default value of the input text as the question
		input_text = question

		# If the "Input text" key is inside the question dictionary
		if "Input text" in question:
			# Define the input text
			input_text = question["Input text"]

		# If the input text is a string
		if isinstance(input_text, str) == True:
			# If the input text is a key inside the root texts dictionary of this module
			if input_text in self.texts:
				# Define the dictionary of texts as that one
				texts_dictionary = self.texts

			# Else, define it as the dictionary of the "Language" module
			else:
				texts_dictionary = self.Language.texts

			# If the input text is inside the local texts dictionary
			if input_text in texts_dictionary:
				# Get the correct text dictionary from the text key
				input_text = texts_dictionary[input_text]

			# If the user language key is inside the input text dictionary
			if self.language["Small"] in input_text:
				# Get the user language version of the input text
				input_text = input_text[self.language["Small"]]

			# If the format character is inside the input text
			if "{}" in input_text:
				# Define the item as the singular version of the task type name in the user language
				item = self.dictionary["Type"]["Names"]["Singular"][self.language["Small"]]

				# Format the input text with the item
				input_text = input_text.format(item)

		# Return the language input text
		return input_text

	def Verify_Input(self, dictionary):
		# Define the default regex
		regex = None

		# If the "Type" key is inside the dictionary
		# And its value is "Number"
		if (
			"Type" in dictionary and
			dictionary["Type"] == "Number"
		):
			regex = r"\b[1-9][0-9]*\b; 10"

		# Ask the user to type the information with the input text
		text = self.Input.Type(dictionary["Text"], accept_enter = False, next_line = True, tab = "\t", regex = regex)

		return text

	def Ask_For_Task_Descriptions(self):
		# Show a five dash space separator
		print()
		print(self.separators["5"])

		# Show the explanation text about opening the task description files for the user to type on them
		print()
		print(self.language_texts["opening_the_task_description_files_for_you_to_type_on_them, type: explanation"])

		# ---------- #

		# Define the dictionary of files
		files = {}

		# Get the grammatical number
		grammatical_number = self.dictionary["Task"]["Grammatical number"]

		# Define the text key for the explanation text with the grammatical number
		text_key = "say_what_you_did_on_the_{}_in_{}" + ", " + grammatical_number.lower()

		# Define the list of languages to use
		languages = self.languages["Small"]

		# Iterate through the list of languages
		for language in languages:
			# Define the task title
			task_title = self.dictionary["Task"]["Titles"][language]

			# Define the task description as the task title in the current language
			self.dictionary["Task"]["Descriptions"][language] = task_title

		# If the "Register task" state is False
		if self.states["Register task"] == False:
			# Define the list of languages as just the user language
			languages = [
				self.language["Small"]
			]

		# Iterate through the small languages list
		for language in languages:
			# Get the full language
			full_language = self.languages["Full"][language]

			# Get the translated language in the user language
			translated_language = self.languages["Full (translated)"][language][self.language["Small"]]

			# Define the item of the task type
			texts = self.dictionary["Type"]["Names"]["Singular"]

			# If the "Grammatical item text" key is inside the task type dictionary
			if "Grammatical item text" in self.dictionary["Type"]:
				# Get the grammatical item text dictionary
				dictionary = self.dictionary["Type"]["Grammatical item text"]

				# If the "Number" key is inside the dictionary
				if "Number" in dictionary:
					grammatical_number = dictionary["Number"]

					# Update the text key to be in the selected grammatical number
					text_key = "say_what_you_did_on_the_{}_in_{}" + ", " + grammatical_number.lower()

				# Get the grammatical item text with the current grammatical number
				item = dictionary[grammatical_number]

				# Define the texts dictionary
				texts = self.Language.texts[item]

			# Get the text for the item in the current language
			item_text = texts[self.language["Small"]]

			# If the "No lowercase" key is not inside the task type dictionary
			if "No lowercase" not in self.dictionary["Type"]:
				item_text = item_text.lower()

			# Define the list of items to use to format the explanation text template
			items = [
				item_text,
				translated_language
			]

			# Format the explanation text with the item of the text
			explanation_text = self.texts[text_key][self.language["Small"]].format(*items)

			# Show a three dash space separator
			print()
			print(self.separators["3"])

			# Show the explanation text of the text (task)
			print()
			print(explanation_text + ".")

			# Define the task description file in the current language
			files[language] = self.tasks["Folders"]["root"] + full_language + ".txt"

			# Create the file
			self.File.Create(files[language])

			# Open the file
			self.System.Open(files[language])

			# If the "Testing" switch is False
			if self.switches["Testing"] == False:
				# Wait for the user to finish writing the task description
				self.Input.Type(self.language_texts["press_enter_when_you_finish_writing_and_saving_the_description_in_{}"].format(translated_language))

		# Define and create the backup file
		files["Backup"] = self.tasks["Folders"]["root"] + "Backup of the descriptions.txt"
		self.File.Create(files["Backup"])

		# ---------- #

		# Iterate through the small languages list
		for language in languages:
			# Define the task title
			task_title = self.dictionary["Task"]["Titles"][language]

			# Define the task description in the current language as the task title with a period and two line breaks
			self.dictionary["Task"]["Descriptions"][language] = task_title + "." + "\n\n"

			# If the "Testing" switch is False
			if self.switches["Testing"] == False:
				# Add the contents of the description file in the current language to the task description
				self.dictionary["Task"]["Descriptions"][language] += self.File.Contents(files[language])["string"]

			# If the "Testing" switch is True
			else:
				# Define the "[Description]" text in the current language
				description_text = "[" + self.Language.texts["description, title()"][language] + "]"

				# Add the text to the task description
				self.dictionary["Task"]["Descriptions"][language] += description_text

			# Define the text to add to the backup file as the task description in the current language
			text = self.dictionary["Task"]["Descriptions"][language]

			# If the language is not the last one, add two line breaks to the text
			if language != languages[-1]:
				text += "\n\n"

			# Add the current task description to the backup file
			self.File.Edit(files["Backup"], text, "a", next_line = False)

			# Delete the description file in the current language
			self.File.Delete(files[language])

		# Delete the task description backup file	
		self.File.Delete(files["Backup"])

	def Register_In_JSON(self):
		# Define a shortcut for the task type dictionary
		self.task_type = self.dictionary["Type"]["Names"]["Plural"]["en"]

		# ---------- #

		# Re-read the "Tasks.json" and media type "Tasks.json" files to retrieve the most up-to-date data
		self.dictionaries["Tasks"] = self.JSON.To_Python(self.tasks["Folders"]["Task History"]["Current year"]["Tasks"])
		self.dictionaries["Task type"][self.task_type] = self.JSON.To_Python(self.dictionary["Type"]["Folders"]["By task type"]["Tasks"])

		# ---------- #

		# Create a local list of dictionaries to update
		dictionaries_to_update = [
			self.dictionaries["Tasks"],
			self.dictionaries["Task type"][self.task_type]
		]

		# Increment the total count for entries and task type entries
		for current_dict in dictionaries_to_update:
			current_dict["Numbers"]["Total"] += 1

			# If the "By task type" key exists, increment the count for the specific task type
			if "By task type" in current_dict["Numbers"]:
				current_dict["Numbers"]["By task type"][self.task_type] += 1

		# ---------- #

		# If the "States" dictionary is not inside the task dictionary
		if "States" not in self.task:
			# Define it with the two default states as False
			self.task["States"] = {
				"First task in year": False,
				"First task type task in year": False
			}

		# If the root task number is one
		if self.dictionaries["Tasks"]["Numbers"]["Total"] == 1:
			# Define the "First task in year" state as True
			self.task["States"]["First task in year"] = True

		# If the task type task number is one
		if self.dictionaries["Task type"][self.task_type]["Numbers"]["Total"] == 1:
			# Define the "First task type task in year" state as True
			self.task["States"]["First task type task in year"] = True

		# ---------- #

		# Define shortcuts for the total entries number and the entry times 
		entries_number = self.dictionaries["Tasks"]["Numbers"]["Total"]
		entry_time = self.dictionary["Entry"]["Times"]["Completed task"]["Formats"]["HH:MM DD/MM/YYYY"]

		# Define the entry "Name" dictionary
		self.task["Name"] = {}

		# Define the template for the entry name
		template = "{}. {} ({})"

		# Iterate through the list of small languages
		for language in self.languages["Small"]:
			# Get the language task type
			language_task_type = self.dictionary["Type"]["Names"]["Plural"][language]

			# Define the list of items to use to format the template
			items = [
				entries_number,
				language_task_type,
				entry_time
			]

			# Format the template with the list of items, making the entry name
			entry_name = template.format(*items)

			# Create the language entry name dictionary
			dictionary = {
				"Normal": entry_name,
				"Sanitized": entry_name.replace(":", ";").replace("/", "-")
			}

			# Add the dictionary to the "Languages" dictionary
			self.task["Name"][language] = dictionary

		# Add the entry name to the "Entries" lists in each dictionary
		for current_dict in dictionaries_to_update:
			if self.task["Name"]["en"]["Normal"] not in current_dict["Entries"]:
				current_dict["Entries"].append(self.task["Name"]["en"]["Normal"])

		# ---------- #

		# Get the normal entry name from the dictionary
		self.entry_name = self.task["Name"]["en"]["Normal"]

		# Add the "Entry" dictionary to the "Dictionary" dictionary
		self.dictionaries["Tasks"]["Dictionary"][self.entry_name] = {
			"Number": self.dictionaries["Tasks"]["Numbers"]["Total"],
			"Type number": self.dictionaries["Task type"][self.task_type]["Numbers"]["Total"],
			"Entry": self.task["Name"]["en"]["Normal"],
			"Titles": self.task["Titles"],
			"Type": self.task_type,
			"Times": deepcopy(self.dictionary["Entry"]["Times"]),
			"Lines": len(self.task["Descriptions"]["en"].splitlines())
		}

		# Define a shortcut for the entry dictionary
		self.entry_dictionary = self.dictionaries["Tasks"]["Dictionary"][self.entry_name]

		# ---------- #

		# Define a list of time keys
		time_keys = [
			"Completed task",
			"Completed task (UTC)"
		]

		# Iterate through the list of time types
		for time_key in time_keys:
			# Define the timezone key as "Timezone"
			timezone_key = "Timezone"

			# Define the format as the timezone one
			format = "HH:MM DD/MM/YYYY"

			# If the "UTC" text is inside the time key
			if "UTC" in time_key:
				# Update the timezone key to be the UTC one
				timezone_key = "UTC"

				# Define the format as the UTC one
				format = "YYYY-MM-DDTHH:MM:SSZ"

			# Get the time for the current time type, timezone, and format
			time = self.entry_dictionary["Times"][time_key][timezone_key]["DateTime"]["Formats"][format]

			# Update the entry dictionary with the obtained time
			self.entry_dictionary["Times"][time_key] = time

		# ---------- #

		# Get the "States" dictionary
		self.dictionary["States"] = self.Define_States_Dictionary(self.dictionary)

		# If the "States" dictionary is not empty
		if self.dictionary["States"]["States"] != {}:
			# Define the states in the JSON task dictionary
			self.dictionaries["Tasks"]["Dictionary"][self.entry_name]["States"] = self.dictionary["States"]["States"]

			# If the "First task type task in year" state is True
			# And the "Custom task item" key is present in the "Task" dictionary
			if (
				self.task["States"]["First task type task in year"] == True and
				"Custom task item" in self.dictionary["Task"]
			):
				# Define the state key
				key = "First task type task in year"

				# Iterate through the list of small languages
				for language in self.languages["Small"]:
					# Get the state text in the current language
					language_text = self.dictionary["States"]["Texts"][key][language]

					# If the task item is inside the language text
					if self.dictionary["Type"]["Item"][language] in language_text:
						# Get the task item in the current language
						task_item = self.dictionary["Type"]["Item"][language]

						# Get the custom task item to replace
						to_replace = self.dictionary["Task"]["Custom task item"][language]

						# Replace the task item with the task item and the custom task item
						language_text = language_text.replace(task_item, task_item + " " + to_replace)

					# Update the state text in the "States" dictionary in the current language
					self.dictionary["States"]["Texts"][key][language] = language_text

		# ---------- #

		# Add the task dictionary to the task type tasks dictionary
		self.dictionaries["Task type"][self.task_type]["Dictionary"][self.entry_name] = self.dictionaries["Tasks"]["Dictionary"][self.entry_name].copy()

		# ---------- #

		# Update the root current year "Tasks.json" file
		self.JSON.Edit(self.tasks["Folders"]["Task History"]["Current year"]["Tasks"], self.dictionaries["Tasks"])

		# Update the task type current year "Tasks.json" file
		self.JSON.Edit(self.dictionary["Type"]["Folders"]["By task type"]["Tasks"], self.dictionaries["Task type"][self.task_type])

		# ---------- #

		# Make a list of "Entry list.txt" files to add to
		files = [
			self.tasks["Folders"]["Task History"]["Current year"]["Entry list"],
			self.dictionary["Type"]["Folders"]["By task type"]["Entry list"]
		]

		# Iterate through those files
		for file in files:
			# Get the lines of the file
			lines = self.File.Contents(file)["Lines"]

			# If the entry name is not inside the text file, add it
			if self.entry_name not in lines:
				self.File.Edit(file, self.entry_name, "a")

	def Create_Entry_File(self):
		# This is a template for organizing task information in a text file
		# Each section contains placeholders that should be replaced with actual data
		# The structure includes details about the task, task type, task times and states
		# Optional values are indicated in parentheses

		# Task number:
		# [Task number]
		# 
		# Task number by task type:
		# [Task number by task type]
		# 
		# Task titles:
		# [Portuguese title]
		# [English title]
		# 
		# Task type:
		# [Task type]
		# 
		# When I completed the task:
		# [Completed task time in the local timezone]
		# 
		# When I completed the task (UTC):
		# [Completed task time in the UTC time]
		# 
		# Entry:
		# [Number. Type (Time)]
		# (
		# States:
		# [Task states]
		# )
		# Task descriptions:
		# 
		# Português:
		# [Portuguese task description]
		# 
		# -
		# 
		# English:
		# [English task description]

		# Define the task folder, file name, and file by task type
		by_task_type_folder = self.tasks["Folders"]["Task History"]["Current year"]["By task type"][self.task_type]["Files"]["root"]
		file_name = self.task["Name"]["en"]["Sanitized"]
		file = by_task_type_folder + file_name + ".txt"

		# Create the task file inside the "By task type" folder
		self.File.Create(file)

		# ---------- #

		# Define the dictionary for the task texts
		self.dictionary["Text"] = {
			"General": self.Define_File_Text("General")
		}

		# Fill the entry "Text" dictionary with the entry texts of each language
		for language in self.languages["Small"]:
			self.dictionary["Text"][language] = self.Define_File_Text(language)

		# ---------- #

		# Write the general task text into the general task file
		self.File.Edit(file, self.dictionary["Text"]["General"], "w")

	# Define the task file text by language
	def Define_File_Text(self, language_parameter = None):
		# If the language parameter is not general
		if language_parameter != "General":
			# Define the local language as the language parameter
			language = language_parameter

		# If it is, define the local language as the user language
		else:
			language = self.language["Small"]

		# Define the full language based on the local language
		full_language = self.languages["Full"][language]

		# ---------- #

		# Define the list of lines for the task text
		# Starting with the total number of tasks and the task number by task type
		lines = [
			self.texts["task_number"][language] + ":" + "\n" + str(self.dictionaries["Tasks"]["Numbers"]["Total"]) + "\n",
			self.texts["task_number_by_task_type"][language] + ":" + "\n" + str(self.dictionaries["Task type"][self.task_type]["Numbers"]["Total"])
		]

		# ---------- #

		# Define the "Title(s)" text based on the language (singular or plural)
		if language_parameter != "General":
			text = self.texts["task_title"][language]

		else:
			text = self.texts["task_titles"][language]

		# Add that text to the list of lines with a format character
		lines.append("\n" + text + ":" + "\n" + "{}")

		# ---------- #

		# Add the task type to the list of lines
		lines.append(self.texts["task_type"][language] + ":" + "\n" + self.dictionary["Type"]["Names"]["Plural"][language] + "\n")

		# ---------- #

		# Add the "When I completed the task" (local timezone) title and format string
		completed_task_timezone_text = self.texts["when_i_completed_the_task"][language] + ":" + "\n" + "{}"
		lines.append(completed_task_timezone_text)

		# Add the "When I completed the task (UTC)" title and format string
		completed_task_utc_text = self.texts["when_i_completed_the_task"][language] + " (" + self.Date.texts["utc"][language] + ")" + ":" + "\n" + "{}"
		lines.append(completed_task_utc_text)

		# ---------- #

		# Add the entry text and the entry name
		lines.append(self.Language.texts["entry, title()"][language] + ":" + "\n" + self.task["Name"]["en"]["Normal"])

		# ---------- #

		# Add the state texts if there are states
		if self.dictionary["States"]["Texts"] != {}:
			# Define the text variable
			text = "\n" + self.Language.texts["states, title()"][language] + ":" + "\n"

			# Add the state texts
			for key in self.dictionary["States"]["Texts"]:
				language_text = self.dictionary["States"]["Texts"][key][language]

				text += language_text

				if key != list(self.dictionary["States"]["Texts"].keys())[-1]:
					text += "\n"

			# Add the text to the list of lines
			lines.append(text)

		# ---------- #

		# If the language parameter is not "General"
		if language_parameter != "General":
			# Define the task description text as the singular one
			text = self.texts["task_description"][language]
			line_break = "\n"

		# If the language parameter is "General"
		else:
			# Define the task description text as the plural one
			text = self.texts["task_descriptions"][language]
			line_break = "\n\n"

		# If the description of the task is not the same as the task title
		if self.dictionary["Task"]["Titles"]["en"] != self.dictionary["Task"]["Descriptions"]["en"]:
			# Add the task description text and the line break(s) with a format character
			lines.append("\n" + text + ":" + line_break + "{}")

		# ---------- #

		# Define the list of items to be used to format the task text template
		items = []

		# ---------- #

		# Add the task titles to the list of itens
		titles = ""

		# Define the "Title(s)" text based on the language (singular or plural)
		if language_parameter != "General":
			titles = self.task["Titles"][language] + "\n"

		else:
			for language in self.languages["Small"]:
				titles += self.task["Titles"][language] + "\n"

		# Add the task titles to the list of items
		items.append(titles)

		# ---------- #

		# Iterate over the relevant keys to obtain the times
		for time_key in ["Completed task", "Completed task (UTC)"]:
			# Check if the key exists
			if time_key in self.dictionary["Entry"]["Times"]:
				# Define the timezone key as "Timezone"
				timezone_key = "Timezone"

				# Define the format as the timezone one
				format = "HH:MM DD/MM/YYYY"

				# If the "UTC" text is inside the time key
				if "UTC" in time_key:
					# Update the timezone key to be the UTC one
					timezone_key = "UTC"

					# Define the format as the UTC one
					format = "YYYY-MM-DDTHH:MM:SSZ"

				# Retrieve the formatted datetime string from the "Times" dictionary,
				# using the specified time key (e.g., "Completed task"), timezone key (e.g., "UTC"),
				# and format (e.g., "YYYY-MM-DDTHH:MM:SSZ")
				time = self.dictionary["Entry"]["Times"][time_key][timezone_key]["DateTime"]["Formats"][format]

				# Append the times to the items list
				items.append(time + "\n")

		# ---------- #

		# Define an empty string to add the descriptions to
		descriptions = ""

		# Define the task description to be added based on the language
		# Only the description for the current language
		if language_parameter != "General":
			descriptions = self.task["Descriptions"][language]

		# Or all language descriptions
		else:
			# Iterate through the list of small languages
			for local_language in self.languages["Small"]:
				# Get the full language
				full_language = self.languages["Full"][local_language]

				# Add the full language and the language description to the root descriptions text
				descriptions += full_language + ":" + "\n" + self.task["Descriptions"][local_language]

				# If the local language is not the last language in the list
				if local_language != self.languages["Small"][-1]:
					descriptions += "\n\n"

		# If the description of the task is not the same as the task title
		if self.dictionary["Task"]["Titles"]["en"] != self.dictionary["Task"]["Descriptions"]["en"]:
			# Add the descriptions to the list of items
			items.append(descriptions)

		# ---------- #

		# Transform the list of lines into a text with the next line
		file_text = self.Text.From_List(lines, next_line = True)

		# Return the file text template formatted with the list of items
		return file_text.format(*items)

	def Add_Entry_File_To_Year_Folder(self):
		# Iterate through the list of small languages
		for language in self.languages["Small"]:
			# Get the full language
			full_language = self.languages["Full"][language]

			# Define shortcuts for the root and type folders
			root_folder = self.Language.texts["completed_tasks"][language]
			type_folder = self.dictionary["Type"]["Names"]["Plural"][language]

			# Define and create the "Completed tasks" folder
			folder = self.current_year["Folders"][language]["root"]

			self.current_year["Folders"][language]["Completed tasks"] = {
				"root": folder + root_folder + "/"
			}

			self.Folder.Create(self.current_year["Folders"][language]["Completed tasks"]["root"])

			# Define and create the task type folder
			folder = self.current_year["Folders"][language]["Completed tasks"]["root"]

			self.current_year["Folders"][language]["Completed tasks"][type_folder] = {
				"root": folder + type_folder + "/"
			}

			self.Folder.Create(self.current_year["Folders"][language]["Completed tasks"][type_folder]["root"])

			# Define and create the "Completed tasks" file
			folder = self.current_year["Folders"][language]["Completed tasks"][type_folder]["root"]
			file_name = self.task["Name"][language]["Sanitized"]
			self.current_year["Folders"][language]["Completed tasks"][type_folder][file_name] = folder + file_name + ".txt"

			self.File.Create(self.current_year["Folders"][language]["Completed tasks"][type_folder][file_name])

			# Write the task text in the current language to the "Completed tasks" file
			self.File.Edit(self.current_year["Folders"][language]["Completed tasks"][type_folder][file_name], self.dictionary["Text"][language], "w")

			# Define and create the "Firsts Of The Year" subfolder folder
			subfolder_name = self.dictionary["Type"]["Type folder"][language]

			folder = self.current_year["Folders"][language]["Firsts of the Year"]["root"]

			self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name] = {
				"root": folder + subfolder_name + "/"
			}

			self.Folder.Create(self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name]["root"])

			# Define and create the "First task type task in year" file
			if self.task["States"]["First task type task in year"] == True:
				folder = self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name]["root"]

				self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name][file_name] = folder + file_name + ".txt"
				self.File.Create(self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name][file_name])

				self.File.Edit(self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name][file_name], self.dictionary["Text"][language], "w")

	def Write_On_Diary_Slim(self):
		# Define the Diary Slim text as the task description in the user language
		self.dictionary["Entry"]["Diary Slim"]["Text"] = self.task["Descriptions"][self.language["Small"]]

		# If the description of the task in English is the same as the English task title
		# And there is no dot at the end of the Diary Slim text
		if (
			self.dictionary["Task"]["Titles"]["en"] == self.dictionary["Task"]["Descriptions"]["en"] and
			self.dictionary["Entry"]["Diary Slim"]["Text"][-1] != "."
		):
			# Add a dot to the Diary Slim text
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "."

		# If the "Register task" state is True
		# And there are states, add the state texts to the Diary Slim text
		if (
			self.states["Register task"] == False and
			self.dictionary["States"]["States"] != {}
		):
			# Add two new lines, the "States" text in the user language, a colon, and a new line
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.Language.language_texts["states, title()"] + ":" + "\n"

			# Iterate through the state keys inside the states dictionary
			for key in self.dictionary["States"]["Texts"]:
				# Get the state text in the user language
				language_text = self.dictionary["States"]["Texts"][key][self.language["Small"]]

				# Add the language state text to the Diary Slim text
				self.dictionary["Entry"]["Diary Slim"]["Text"] += language_text

				# If the key is not the last one in the list, add a new line
				if key != list(self.dictionary["States"]["Texts"].keys())[-1]:
					self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n"

		# Import the "Write_On_Diary_Slim_Module" module from the "Diary_Slim" module
		from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

		# Define the "Write on Diary Slim" dictionary
		# With the Diary Slim text, time, not adding a dot, and not showing the text
		dictionary = {
			"Text": self.dictionary["Entry"]["Diary Slim"]["Text"],
			"Time": self.dictionary["Entry"]["Times"]["Completed task"]["Formats"]["HH:MM DD/MM/YYYY"],
			"Add": {
				"Dot": False
			},
			"Show text": False
		}

		# Write the entry text on the current Diary Slim
		# Getting back the current Diary Slim dictionary
		self.dictionary["Diary Slim"] = Write_On_Diary_Slim_Module.Return(dictionary)