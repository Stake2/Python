# Register.py

from Tasks.Tasks import Tasks as Tasks

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
				"Date": self.Date.Now()
			}
		}

		# Define the states dictionary
		self.states = {
			"Used as module": False, # Indicates if the module is being used as a dependency in another place
			"Five dash space": False, # Inditaces if the module should show a five dash space after showing the information about the registered task
			"Ask for input": True # Ask for input after showing the information about the registered task
		}

		# If the parameter dictionary is not empty
		if dictionary_parameter != {}:
			# Define the "Used as module" state as True
			self.states["Used as module"] = True

		# Update the root dictionary with the parameter dictionary
		self.dictionary.update(dictionary_parameter)

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

		# If the parameter dictionary is not empty
		if dictionary_parameter != {}:
			# Define the "Ask for input" state as False
			self.states["Ask for input"] = False

		# ---------- #

		# Define a shortcut for the task dictionary
		self.task = self.dictionary["Task"]

		# If the "Descriptions" key is not inside the task dictionary
		if "Descriptions" not in self.task:
			# Define the descriptions dictionary as the titles dictionary
			self.task["Descriptions"] = self.task["Titles"]

		# ---------- #

		# Update the task entry dictionary to add the "Dates" and "Diary Slim" dictionaries
		self.dictionary["Entry"].update({
			"Dates": {
				"UTC": self.dictionary["Entry"]["Date"]["UTC"]["DateTime"]["Formats"]["YYYY-MM-DDTHH:MM:SSZ"],
				"Timezone": self.dictionary["Entry"]["Date"]["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"]
			},
			"Diary Slim": {
				"Text": ""
			}
		})

		# Database related methods to register the task entry
		self.Register_In_JSON()
		self.Create_Entry_File()
		self.Add_Entry_File_To_Year_Folder()

		# Write the task description in the user language on the current iary Slim
		self.Write_On_Diary_Slim()

		# Show information about the registered task
		# Passing the root dictionary and the states dictionary as parameters
		self.Show_Information(self.dictionary, self.states)

	def Select_Task_Type(self):
		# Define the list of options and language options
		options = self.tasks["Types"]["Lists"]["Plural"]["en"]
		language_options = self.tasks["Types"]["Lists"]["Plural"][self.user_language]

		# Define the "t" variable for task type number
		t = 0

		# Iterate through the keys inside the task "Types" dictionary
		for task_type in self.tasks["Types"]["Dictionary"].values():
			# If the "Module-only" key is inside the task type dictionary
			if "Module-only" in task_type:
				# Remove the task type from the lists above
				options.pop(t)
				language_options.pop(t)

			# Add to the "t" number variable
			t += 1

		# Define the show and select texts
		show_text = self.language_texts["task_types"]
		select_text = self.language_texts["select_a_task_type"]

		# Ask for the user to select a task type
		option = self.Input.Select(options, language_options = language_options, show_text = show_text, select_text = select_text)["Option"]["Original"]

		# Get the task type dictionary for the selected task type
		self.dictionary["Type"] = self.tasks["Types"]["Dictionary"][option]

	def Ask_For_Task_Information(self):
		# Iterate through the list of small languages
		for language in self.languages["small"]:
			# Get the translated language in the user language
			translated_language = self.languages["full_translated"][language][self.user_language]

			# Define the task title in the current language
			self.dictionary["Task"]["Titles"][language] = self.dictionary["Type"]["Task texts"][language]

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
			print("\t" + self.dictionary["Type"]["Names"]["Plural"][self.user_language])

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
				for language in self.languages["small"]:
					# Get the translated language in the user language
					translated_language = self.languages["full_translated"][language][self.user_language]

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
				for language in self.languages["small"]:
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
				for language in self.languages["small"]:
					# Get the response
					response = questions[key]["Response"]

					# If the response is a dictionary
					if isinstance(response, dict):
						# Get the response in the current language
						response = response[language]

					# Format the task title
					title = self.dictionary["Task"]["Titles"][language].format(response)

					# Update it in the root titles dictionary
					self.dictionary["Task"]["Titles"][language] = title

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
			if self.user_language in input_text:
				# Get the user language version of the input text
				input_text = input_text[self.user_language]

			# If the format character is inside the input text
			if "{}" in input_text:
				# Define the item as the singular version of the task type name in the user language
				item = self.dictionary["Type"]["Names"]["Singular"][self.user_language]

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

		# Iterate through the small languages list
		for language in self.languages["small"]:
			# Get the full language
			full_language = self.languages["full"][language]

			# Get the translated language in the user language
			translated_language = self.languages["full_translated"][language][self.user_language]

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
			item_text = texts[self.user_language]

			# If the "No lowercase" key is not inside the task type dictionary
			if "No lowercase" not in self.dictionary["Type"]:
				item_text = item_text.lower()

			# Define the list of items to use to format the explanation text template
			items = [
				item_text,
				translated_language
			]

			# Format the explanation text with the item of the text
			explanation_text = self.texts[text_key][self.user_language].format(*items)

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

			# Wait for the user to finish writing the task description
			self.Input.Type(self.language_texts["press_enter_when_you_finish_writing_and_saving_the_description_in_{}"].format(translated_language))

		# Define and create the backup file
		files["Backup"] = self.tasks["Folders"]["root"] + "Backup of the descriptions.txt"
		self.File.Create(files["Backup"])

		# ---------- #

		# Iterate through the small languages list
		for language in self.languages["small"]:
			# Define the task description in the current language as the task title with a period and two line breaks
			self.dictionary["Task"]["Descriptions"][language] = self.dictionary["Task"]["Titles"][language] + "." + "\n\n"

			# If the "Testing" switch is False
			if self.switches["Testing"] == False:
				# Add the contents of the description file in the current language to the task description
				self.dictionary["Task"]["Descriptions"][language] += self.File.Contents(files[language])["string"]

			# If the "Testing" switch is True
			else:
				# Add the "[Description]" text in the current language to the task description
				self.dictionary["Task"]["Descriptions"][language] += "[" + self.Language.texts["description, title()"][language] + "]"

			# Define the text to add to the backup file as the task description in the current language
			text = self.dictionary["Task"]["Descriptions"][language]

			# If the language is not the last one, add two line breaks to the text
			if language != self.languages["small"][-1]:
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

		# Define a list of dicts to add to
		dicts = [
			self.dictionaries["Tasks"],
			self.dictionaries["Task type"][self.task_type]
		]

		# Add one to the root and task type entry numbers
		for dict_ in dicts:
			dict_["Numbers"]["Total"] += 1

			if "Per Task Type" in dict_["Numbers"]:
				dict_["Numbers"]["Per Task Type"][self.task_type] += 1

		# If the root task number is one
		if self.dictionaries["Tasks"]["Numbers"]["Total"] == 1:
			# Define the "First task in year" state as True
			self.task["States"]["First task in year"] = True

		# If the task type task number is one
		if self.dictionaries["Task type"][self.task_type]["Numbers"]["Total"] == 1:
			# Define the "First task type task in year" state as True
			self.task["States"]["First task type task in year"] = True

		# Define the normal and sanitized version of the task name for file names
		self.task["Name"] = {
			"Normal": str(self.dictionaries["Tasks"]["Numbers"]["Total"]) + ". " + self.task_type + " (" + self.dictionary["Entry"]["Dates"]["Timezone"] + ")",
			"Sanitized": ""
		}

		# Replace colons and slashes on the sanitized task name
		self.task["Name"]["Sanitized"] = self.task["Name"]["Normal"].replace(":", ";").replace("/", "-")

		# Add to the "Tasks" lists
		for dict_ in dicts:
			if self.task["Name"]["Normal"] not in dict_["Entries"]:
				dict_["Entries"].append(self.task["Name"]["Normal"])

		# Define a shortcut for the task name text
		self.key = self.task["Name"]["Normal"]

		# Define the task entry JSON dictionary
		self.dictionaries["Tasks"]["Dictionary"][self.key] = {
			"Number": self.dictionaries["Tasks"]["Numbers"]["Total"],
			"Type number": self.dictionaries["Task type"][self.task_type]["Numbers"]["Total"],
			"Entry": self.task["Name"]["Normal"],
			"Titles": self.task["Titles"],
			"Type": self.task_type,
			"Date": self.dictionary["Entry"]["Dates"]["UTC"],
			"Lines": len(self.task["Descriptions"]["en"].splitlines())
		}

		# If the "States" dictionary is not inside the task dictionary
		if "States" not in self.task:
			# Define it with the two default states as False
			self.task["States"] = {
				"First task in year": False,
				"First task type task in year": False
			}

		# Get the "States" dictionary
		self.dictionary["States"] = self.Define_States_Dictionary(self.dictionary)

		# If the "States" dictionary is not empty
		if self.dictionary["States"]["States"] != {}:
			# Define the states in the JSON task dictionary
			self.dictionaries["Tasks"]["Dictionary"][self.key]["States"] = self.dictionary["States"]["States"]

			# If the "First task type task in year" state is True
			# And the "Custom task item" key is present in the "Task" dictionary
			if (
				self.task["States"]["First task type task in year"] == True and
				"Custom task item" in self.dictionary["Task"]
			):
				# Define the state key
				key = "First task type task in year"

				# Iterate through the list of small languages
				for language in self.languages["small"]:
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

		# Add the task dictionary to the task type tasks dictionary
		self.dictionaries["Task type"][self.task_type]["Dictionary"][self.key] = self.dictionaries["Tasks"]["Dictionary"][self.key].copy()

		# Update the root current year "Tasks.json" file
		self.JSON.Edit(self.tasks["Folders"]["Task History"]["Current year"]["Tasks"], self.dictionaries["Tasks"])

		# Update the task type current year "Tasks.json" file
		self.JSON.Edit(self.dictionary["Type"]["Folders"]["Per Task Type"]["Tasks"], self.dictionaries["Task type"][self.task_type])

		# Add to the root and task type "Entry list.txt" file
		self.File.Edit(self.tasks["Folders"]["Task History"]["Current year"]["Entry list"], self.task["Name"]["Normal"], "a")
		self.File.Edit(self.dictionary["Type"]["Folders"]["Per Task Type"]["Entry list"], self.task["Name"]["Normal"], "a")

	def Create_Entry_File(self):
		# Number: [Task number]
		# Task type number: [Task type number]
		# 
		# Titles:
		# [Portuguese title]
		# [English title]
		# 
		# Type:
		# [Task type]
		# 
		# Dates:
		# [Task dates]
		# 
		# File name:
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

		# Define and create the the task file in the "Per Task Type" folder
		folder = self.tasks["Folders"]["Task History"]["Current year"]["Per Task Type"][self.task_type]["Files"]["root"]
		file = folder + self.task["Name"]["Sanitized"] + ".txt"
		self.File.Create(file)

		# Define the dictionary of the task texts
		self.dictionary["Text"] = {
			"General": self.Define_File_Text("General")
		}

		# Iterate through the list of small languages
		for language in self.languages["small"]:
			# Define the task text for each language
			self.dictionary["Text"][language] = self.Define_File_Text(language)

		# Write the general task text into the general task file
		self.File.Edit(file, self.dictionary["Text"]["General"], "w")

	# Define the task text per language
	def Define_File_Text(self, language_parameter = None):
		# If the language parameter is not general
		if language_parameter != "General":
			# Define the local language as the language parameter
			language = language_parameter

		# If it is, define the local language as the user language
		else:
			language = self.user_language

		# Define the full language based on the local language
		full_language = self.languages["full"][language]

		# Define the list of lines for the task text
		# Starting with the total number of tasks and the task number per task type
		lines = [
			self.texts["number, title()"][language] + ": " + str(self.dictionaries["Tasks"]["Numbers"]["Total"]),
			self.texts["task_type_number"][language] + ": " + str(self.dictionaries["Task type"][self.task_type]["Numbers"]["Total"])
		]

		# Define the "Title(s)" text based on the language (singular or plural)
		if language_parameter != "General":
			text = self.Language.texts["title, title()"][language]

		else:
			text = self.Language.texts["titles, title()"][language]

		# Add that text to the list of lines with a format character
		lines.append("\n" + text + ":" + "\n" + "{}")

		# Extend the list of lines with the task type, times, and file name lines, some of them already containing the values (task type name and file name)
		lines.extend([
			self.Language.texts["type, title()"][language] + ":" + "\n" + self.dictionary["Type"]["Names"]["Plural"][language] + "\n",
			self.Date.texts["times, title()"][language] + ":" + "\n" + "{}",
			self.File.texts["file_name"][language] + ":" + "\n" + self.task["Name"]["Normal"]
		])

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

		# Define the "Task description(s)" text based on the language (singular or plural)
		if language_parameter != "General":
			text = self.texts["task_description"][language]
			line_break = "\n"

		else:
			text = self.texts["task_descriptions"][language]
			line_break = "\n\n"

		# If the description of the task is not the same as the task title
		if self.dictionary["Task"]["Titles"]["en"] != self.dictionary["Task"]["Descriptions"]["en"]:
			# Add the task description text and the line break(s) with a format character
			lines.append("\n" + text + ":" + line_break + "{}")

		# Define the list of items to be used to format the task text template
		items = []

		# Add the task titles to the list of itens
		titles = ""

		# Define the "Title(s)" text based on the language (singular or plural)
		if language_parameter != "General":
			titles = self.task["Titles"][language] + "\n"

		else:
			for language in self.languages["small"]:
				titles += self.task["Titles"][language] + "\n"

		# Add the task titles to the list of items
		items.append(titles)

		# Define the times to be added to the list of items
		times = ""

		# (Add UTC and Timezone itimes)
		for key in ["UTC", "Timezone"]:
			time = self.dictionary["Entry"]["Dates"][key]

			times += time + "\n"

		# Add the times to the list of items
		items.append(times)

		# Define the task descriptions to be added to the list of items
		descriptions = ""

		# Define the task description to be added based on the language
		# (Only the task description for the current language, or all task descriptions)
		if language_parameter != "General":
			descriptions = self.task["Descriptions"][language]

		else:
			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				descriptions += full_language + ":" + "\n" + self.task["Descriptions"][language]

				if language != self.languages["small"][-1]:
					descriptions += "\n\n"

		# If the description of the task is not the same as the task title
		if self.dictionary["Task"]["Titles"]["en"] != self.dictionary["Task"]["Descriptions"]["en"]:
			# Add the descriptions to the list of items
			items.append(descriptions)

		# Transform the list of lines into a text with the next line
		file_text = self.Text.From_List(lines, next_line = True)

		# Return the file text template formatted with the list of items
		return file_text.format(*items)

	def Add_Entry_File_To_Year_Folder(self):
		# Iterate through the list of small languages
		for language in self.languages["small"]:
			# Get the full language
			full_language = self.languages["full"][language]

			# Define shortcuts for the root and type folders
			root_folder = self.Language.texts["done_tasks"][language]
			type_folder = self.dictionary["Type"]["Names"]["Plural"][language]

			# Define and create the "Done tasks" folder
			folder = self.current_year["Folders"][language]["root"]

			self.current_year["Folders"][language]["Done tasks"] = {
				"root": folder + root_folder + "/"
			}

			self.Folder.Create(self.current_year["Folders"][language]["Done tasks"]["root"])

			# Define and create the task type folder
			folder = self.current_year["Folders"][language]["Done tasks"]["root"]

			self.current_year["Folders"][language]["Done tasks"][type_folder] = {
				"root": folder + type_folder + "/"
			}

			self.Folder.Create(self.current_year["Folders"][language]["Done tasks"][type_folder]["root"])

			# Define and create the "Done tasks" file
			folder = self.current_year["Folders"][language]["Done tasks"][type_folder]["root"]
			file_name = self.task["Name"]["Sanitized"]
			self.current_year["Folders"][language]["Done tasks"][type_folder][file_name] = folder + file_name + ".txt"

			self.File.Create(self.current_year["Folders"][language]["Done tasks"][type_folder][file_name])

			# Write the task text in the current language to the "Done tasks" file
			self.File.Edit(self.current_year["Folders"][language]["Done tasks"][type_folder][file_name], self.dictionary["Text"][language], "w")

			# Define and create the "Firsts Of The Year" subfolder folder
			subfolder_name = self.dictionary["Type"]["Type folder"][language]

			folder = self.current_year["Folders"][language]["Firsts of the Year"]["root"]

			self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name] = {
				"root": folder + subfolder_name + "/"
			}

			self.Folder.Create(self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name]["root"])

			# Define and create the "Firsts Of The Year" task type folder
			item_folder = self.dictionary["Type"]["Item"][language]

			folder = self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name]["root"]
			
			self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name][item_folder] = {
				"root": folder + item_folder + "/"
			}

			self.Folder.Create(self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name][item_folder]["root"])

			# Define and create the "First task type task in year" file
			if self.task["States"]["First task type task in year"] == True:
				folder = self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name][item_folder]["root"]

				self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name][item_folder][file_name] = folder + file_name + ".txt"
				self.File.Create(self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name][item_folder][file_name])

				self.File.Edit(self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name][item_folder][file_name], self.dictionary["Text"][language], "w")

	def Write_On_Diary_Slim(self):
		# Define the Diary Slim text as the task description in the user language
		self.dictionary["Entry"]["Diary Slim"]["Text"] = self.task["Descriptions"][self.user_language]

		# If the description of the task in English is the same as the English task title
		if self.dictionary["Task"]["Titles"]["en"] == self.dictionary["Task"]["Descriptions"]["en"]:
			# Add a dot to the Diary Slim text
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "."

		# If there are states, add the state texts to the Diary Slim text
		if self.dictionary["States"]["States"] != {}:
			# Add two new lines, the "States" text in the user language, a colon, and a new line
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.Language.language_texts["states, title()"] + ":" + "\n"

			# Iterate through the state keys inside the states dictionary
			for key in self.dictionary["States"]["Texts"]:
				# Get the state text in the user language
				language_text = self.dictionary["States"]["Texts"][key][self.user_language]

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
			"Time": self.dictionary["Entry"]["Dates"]["Timezone"],
			"Add": {
				"Dot": False
			},
			"Show text": False
		}

		# Write the entry text on the current Diary Slim
		# Getting back the current Diary Slim dictionary
		self.dictionary["Diary Slim"] = Write_On_Diary_Slim_Module.Return(dictionary)