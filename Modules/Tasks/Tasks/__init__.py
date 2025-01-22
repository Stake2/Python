# Tasks.py

# Import the "importlib" module
import importlib

# Import the "deepcopy" class from the "copy" module
from copy import deepcopy

class Tasks(object):
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.folders = self.Define_Folders(object = self).folders

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Import the usage classes
		self.Import_Usage_Classes()

		# Folders and files method
		self.Define_Folders_And_Files()

		# Class methods
		self.Define_Task_Types()
		self.Define_Registry_Format()

	def Import_Classes(self):
		# Define the list of modules to be imported
		modules = [
			"Define_Folders",
			"JSON"
		]

		# Iterate through the list of modules
		for module_title in modules:
			# Import the module
			module = importlib.import_module("." + module_title, "Utility")

			# Get the sub-class
			sub_class = getattr(module, module_title)

			# If the module title is not "Define_Folders"
			if module_title != "Define_Folders":
				# Run the sub-class to define its variable
				sub_class = sub_class()

			# Add the sub-class to the current module
			setattr(self, module_title, sub_class)

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

	def Define_Basic_Variables(self):
		# Get the modules list
		self.modules = self.JSON.To_Python(self.folders["Apps"]["Modules"]["Modules"])

		# Create a list of the modules that will not be imported
		remove_list = [
			"Define_Folders",
			"Modules",
			"Language",
			"JSON"
		]

		# Iterate through the Utility modules
		for module_title in self.modules["Utility"]["List"]:
			# If the module title is not inside the remove list
			if module_title not in remove_list:
				# Import the module
				module = importlib.import_module("." + module_title, "Utility")

				# Get the sub-class
				sub_class = getattr(module, module_title)

				# Add the sub-class to the current module
				setattr(self, module_title, sub_class())

		# Get the switches dictionary from the "Global Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# Get the Languages dictionary
		self.languages = self.Language.languages

		# Get the user language and full user language
		self.user_language = self.Language.user_language
		self.full_user_language = self.Language.full_user_language

		# Define the local "folders" dictionary as the dictionary inside the "Folder" class
		self.folders = self.Folder.folders

		# Get the Sanitize method of the File class
		self.Sanitize = self.File.Sanitize

		# Get the current date from the Date module
		self.date = self.Date.date

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

		# Define the "Separators" dictionary
		self.separators = {}

		# Create separators from one to ten characters
		for number in range(1, 11):
			# Define the empty string
			string = ""

			# Add separators to it
			while len(string) != number:
				string += "-"

			# Add the string to the Separators dictionary
			self.separators[str(number)] = string

	def Import_Usage_Classes(self):
		# Define the classes to be imported
		classes = [
			"Years"
		]

		# Import them
		for title in classes:
			# Import the module
			module = importlib.import_module("." + title, title)

			# Get the sub-class
			sub_class = getattr(module, title)

			# Add the sub-class to the current module
			setattr(self, title, sub_class())

	def Define_Folders_And_Files(self):
		# Define the current year variable
		self.current_year = self.Years.years["Current year"]

		# Define the root "Tasks" dictionary, with the "Folders" dictionary
		self.tasks = {
			"Module name": self.language_texts["tasks, title()"],
			"Folders": self.folders["Notepad"]["Data Networks"]["Productivity"]
		}

		# Define a shortcut for the current year folder
		self.tasks["Folders"]["Task History"]["Current year"] = self.tasks["Folders"]["Task History"][self.current_year["Number"]]

		# Define the "History" dictionary
		self.history = {
			"Key": "",
			"Numbers": {
				"Productive things": ""
			},
			"Folder": self.tasks["Folders"]["Task History"]["root"]
		}

		# Define and create the "Task types" folder
		self.tasks["Folders"]["Task types"] = {
			"root": self.tasks["Folders"]["root"] + self.language_texts["task_types"] + "/"
		}

		self.Folder.Create(self.tasks["Folders"]["Task types"]["root"])

		# Define and create the "Task types.json" file
		self.tasks["Folders"]["Task types"]["Task types"] = self.tasks["Folders"]["Task types"]["root"] + self.texts["task_types"]["en"] + ".json"

		self.File.Create(self.tasks["Folders"]["Task types"]["Task types"])

	def Define_Task_Types(self):
		# Define the default task types dictionary
		self.tasks["Types"] = {
			"Numbers": {
				"Total": 0
			},
			"List": [],
			"Lists": {
				"Singular": {},
				"Plural": {}
			},
			"Dictionary": {}
		}

		# Iterate through the list of grammatical numbers
		for grammatical_number in self.tasks["Types"]["Lists"]:
			# Iterate through the list of small languages
			for language in self.languages["small"]:
				# Create the language key inside the grammatical number dictionary
				self.tasks["Types"]["Lists"][grammatical_number][language] = []

		# Define the "Task types.json" file variable for easier typing
		file = self.tasks["Folders"]["Task types"]["Task types"]

		# If the "Task types.json" file is not empty
		if self.File.Contents(file)["lines"] != []:
			# Update the root "Task types" dictionary with the dictionary inside the file
			self.tasks["Types"].update(self.JSON.To_Python(file))

		# ---------- #

		# Get the sub-folders of the "Task types" folder
		contents = self.Folder.Contents(self.tasks["Folders"]["Task types"]["root"])

		# Get the task type folders dictionary
		folders = contents["folder"]["dictionary"]

		# ---------- #

		# Get the number of task types
		self.tasks["Types"]["Numbers"]["Total"] = len(contents["folder"]["names"])

		# Define the list of texts
		self.tasks["Types"]["List"] = contents["folder"]["names"]

		# ---------- #

		# Iterate through the task type folders dictionary
		for key, folder in folders.items():
			# Create the "Task type" dictionary
			dictionary = {
				"Key": key,
				"Names": {
					"Singular": {},
					"Plural": {}
				},
				"Folders": {
					"root": folder
				},
				"Files": {},
				"Type folder": {},
				"Item": {},
				"Task texts": {}
			}

			# ----- #

			# Define the task type "Type.json" file
			dictionary["Files"]["Type"] = dictionary["Folders"]["root"] + "Type.json"

			# If the task type "Type.json" file exists and it is not empty
			if (
				self.File.Exist(dictionary["Files"]["Type"]) == True and
				self.File.Contents(dictionary["Files"]["Type"])["lines"] != []
			):
				# Update the local dictionary with the one inside the file
				dictionary.update(self.JSON.To_Python(dictionary["Files"]["Type"]))

			# ----- #

			# Define the names for the task type

			names = {}

			# Iterate through the list of grammatical numbers
			for grammatical_number in self.tasks["Types"]["Lists"]:
				# Get the text key for the grammatical number
				text_key = dictionary["Names"][grammatical_number]

				# Get the names dictionary with all language keys
				names[grammatical_number] = self.Define_Text(dictionary["Names"][grammatical_number], text_key)

				# Iterate through the list of small languages
				for language in self.languages["small"]:
					# Get the name in the current grammatical number and language
					name = names[grammatical_number][language]

					# If the name is not inside the list of tasks
					if name not in self.tasks["Types"]["Lists"][grammatical_number][language]:
						# Add that name to the list of task types in the current grammatical number and language
						self.tasks["Types"]["Lists"][grammatical_number][language].append(name)

			# Define the root "Names" dictionary as the local names dictionary
			dictionary["Names"] = names

			# Get the plural task type
			task_type = dictionary["Names"]["Plural"]["en"]

			# ----- #

			# Define the type folder and item for the task type
			for item in ["Type folder", "Item"]:
				# Get the text key
				text_key = dictionary[item]

				# Get the names dictionary with all language keys
				dictionary[item] = self.Define_Text(text_key, text_key)

			# ----- #

			# Define a shortcut for the per task type folder, to not be ugly and big
			per_task_type_folder = self.tasks["Folders"]["Task History"]["Current year"]["Per Task Type"]

			# Create the "Per Task Type" task type folder for the current year
			per_task_type_folder[task_type] = {
				"root": per_task_type_folder["root"] + task_type + "/"
			}

			self.Folder.Create(per_task_type_folder[task_type]["root"])

			# Create the "Tasks.json" file in the "Per Task Type" task type folder
			per_task_type_folder[task_type]["Tasks"] = per_task_type_folder[task_type]["root"] + "Tasks.json"
			self.File.Create(per_task_type_folder[task_type]["Tasks"])

			# Create the "Entry list.txt" file in the "Per Task Type" task type folder
			per_task_type_folder[task_type]["Entry list"] = per_task_type_folder[task_type]["root"] + "Entry list.txt"
			self.File.Create(per_task_type_folder[task_type]["Entry list"])

			# Create the "Files" folder on the "Per Task Type" task type folder
			per_task_type_folder[task_type]["Files"] = {
				"root": per_task_type_folder[task_type]["root"] + "Files/"
			}

			self.Folder.Create(per_task_type_folder[task_type]["Files"]["root"])

			# Define the per task type folder inside the folders dictionary
			dictionary["Folders"]["Per Task Type"] = per_task_type_folder[task_type]

			# ----- #

			# Add the task type dictionary to the root "Types" dictionary
			self.tasks["Types"]["Dictionary"][key] = dictionary

		# ---------- #

		# Iterate through the keys inside the task "Types" dictionary
		for key in deepcopy(self.tasks["Types"]["Dictionary"]):
			# If the key is not inside the "folders" dictionary
			if key not in folders:
				# Remove the key
				self.tasks["Types"]["Dictionary"].pop(key)

		# ---------- #

		# Iterate through the keys inside the task "Types" dictionary
		for key, dictionary in deepcopy(self.tasks["Types"]["Dictionary"]).items():
			# If the key is not inside the "List" list, remove it
			if key not in self.tasks["Types"]["List"]:
				self.tasks["Types"]["Dictionary"].pop(key)

				# Iterate through the list of grammatical numbers
				for grammatical_number in self.tasks["Types"]["Lists"]:
					# Iterate through the list of small languages
					for language in self.languages["small"]:
						# Get the name
						name = dictionary["Names"][grammatical_number][language]

						# Remove it from the language list in the current grammatical number
						self.tasks["Types"]["Lists"][grammatical_number][language].remove(name)

		# ---------- #

		# Update the "Task types.json" file with the updated task "Types" dictionary
		self.JSON.Edit(self.tasks["Folders"]["Task types"]["Task types"], self.tasks["Types"])

	def Define_Text(self, original_text, text_key = None):
		# Define the default texts dictionary
		texts = original_text

		# If the original text is a string
		if isinstance(original_text, str) == True:
			# If the text key is None
			if text_key == None:
				# Define the text key as the original text
				text_key = original_text

			# Define the empty texts dictionary
			texts = {}

			# If the text key does not contain an underscore
			if "_" not in text_key:
				# Add the ", title()" text
				text_key += ", title()"

			# If the text key is inside the "Texts" dictionary of the "Language" class
			if text_key in self.Language.texts:
				# Define the texts dictionary for the text
				texts = self.Language.texts[text_key]

			else:
				# Iterate through the list of small languages
				for language in self.languages["small"]:
					# Define the text in the current language as the original text, not a text dictionary
					texts[language] = original_text

		return texts

	def Define_Registry_Format(self):
		# Define the default tasks dictionary template
		self.template = {
			"Numbers": {
				"Total": 0,
			},
			"Entries": [],
			"Dictionary": {}
		}

		# Define the root dictionaries
		# With the History, Tasks, Task, and Task type keys
		self.dictionaries = {
			"History": {
				"Numbers": {
					"Years": 0,
					"Tasks": 0
				},
				"Years": []
			},
			"Tasks": deepcopy(self.template),
			"Task": {},
			"Task type": {}
		}

		# ---------- #

		# Define a shortcut for the "History.json" file
		history_file = self.tasks["Folders"]["Task History"]["History"]

		# If the history file is not empty and the list of years is not empty
		if (
			self.File.Contents(history_file)["lines"] != [] and
			self.JSON.To_Python(history_file)["Years"] != []
		):
			# Define the history dictionary as the one inside the file
			self.dictionaries["History"] = self.JSON.To_Python(history_file)

		# If the current year is not inside the list of years, add it to the list
		if self.current_year["Number"] not in self.dictionaries["History"]["Years"]:
			self.dictionaries["History"]["Years"].append(self.current_year["Number"])

		# ---------- #

		# Define the local number of tasks as zero
		tasks = 0

		# Iterate through the list of years from 2018 to the current year
		for year in self.Date.Create_Years_List(function = str):
			# Get the year folder and the tasks file for the current year
			year_folder = self.tasks["Folders"]["Task History"]["root"] + year + "/"
			entries_file = year_folder + "Tasks.json"

			# If the file exists and it is not empty
			if (
				self.File.Exist(entries_file) == True and
				self.File.Contents(entries_file)["lines"] != []
			):
				# Add the number of lines of the file to the local number of tasks
				tasks += self.JSON.To_Python(entries_file)["Numbers"]["Total"]

			# Add the year to the list of years if it is not inside it
			if year not in self.dictionaries["History"]["Years"]:
				self.dictionaries["History"]["Years"].append(year)

		# ---------- #

		# Sort the list of years
		self.dictionaries["History"]["Years"] = sorted(self.dictionaries["History"]["Years"], key = str.lower)

		# Update the number of years with the number of years in the list
		self.dictionaries["History"]["Numbers"]["Years"] = len(self.dictionaries["History"]["Years"])

		# Define the number of tasks on all years as the local number of tasks
		self.dictionaries["History"]["Numbers"]["Tasks"] = tasks

		# Update the "History.json" file with the updated "History" dictionary
		self.JSON.Edit(history_file, self.dictionaries["History"])

		# ---------- #

		# Create the "Per Task Type" key inside the "Numbers" dictionary of the "Tasks" dictionary
		self.dictionaries["Tasks"]["Numbers"]["Per Task Type"] = {}

		# Define a shortcut for the "Tasks.json" file
		tasks_file = self.tasks["Folders"]["Task History"]["Current year"]["Tasks"]

		# If the "Tasks.json" file is not empty and the list of years is not an empty list
		if (
			self.File.Contents(tasks_file)["lines"] != [] and
			self.JSON.To_Python(tasks_file)["Entries"] != []
		):
			# Define the "Tasks" dictionary as the one inside the file
			self.dictionaries["Tasks"] = self.JSON.To_Python(tasks_file)

		# ---------- #

		# Iterate through the task type keys and dictionaries
		for key, task_type in self.tasks["Types"]["Dictionary"].items():
			# Define the default task type dictionary as the template one
			self.dictionaries["Task type"][key] = deepcopy(self.template)

			# Define a shortcut for the file for the "if" not to be ugly and big
			file = task_type["Folders"]["Per Task Type"]["Tasks"]

			# If the task type "Tasks.json" file is not empty and the list of years is not an empty list
			if (
				self.File.Contents(file)["lines"] != [] and
				self.JSON.To_Python(file)["Entries"] != []
			):
				# Define the task type tasks dictionary as the one inside the file
				self.dictionaries["Task type"][key] = self.JSON.To_Python(file)

			# Define the number to use as zero
			number_to_use = 0

			# If the plural task type is inside the "Per Task Type" dictionary of numbers
			if key in self.dictionaries["Tasks"]["Numbers"]["Per Task Type"]:
				# Define the number to use as it
				number_to_use = self.dictionaries["Task type"][key]["Numbers"]["Total"]

			# Define the number inside the task type number key
			self.dictionaries["Tasks"]["Numbers"]["Per Task Type"][key] = number_to_use

			# Update the per task type "Tasks.json" file with the updated per type tasks dictionary
			self.JSON.Edit(file, self.dictionaries["Task type"][key])

		# Update the "Tasks.json" file with the updated "Tasks" dictionary
		self.JSON.Edit(tasks_file, self.dictionaries["Tasks"])

	def Define_States_Dictionary(self, dictionary):
		# Define the default empty states dictionary
		states_dictionary = {
			"States": {},
			"Texts": {}
		}

		# Define the list of keys for the states
		keys = [
			"First task in year",
			"First task type task in year"
		]

		# Iterate through the list of keys
		for key in keys:
			# If the state is True
			if dictionary["Task"]["States"][key] == True:
				# Define the local state as True
				state = True

				# Define the state dictionary
				states_dictionary["States"][key] = state

				# Define the state "Texts" dictionary of the current state
				states_dictionary["Texts"][key] = {}

				# Iterate through the list of small languages
				for language in self.languages["small"]:
					# Define the default empty text
					text = ""

					# If the key is not "First task type task in year"
					if key != "First task type task in year":
						# Define the text key, making it lowercase and replacing spaces with underline
						text_key = key.lower().replace(" ", "_")

						# If the text key is inside the "Texts" dictionary of the "Language" class
						if text_key in self.Language.texts:
							# Get the text in the current language
							text = self.Language.texts[text_key][language]

						# Else, it is inside of the "Texts" dictionary of the "Tasks" class (this one)
						else:
							# Get the text in the current language
							text = self.texts[text_key][language]

					# If the key is "First task type task in year"
					if key == "First task type task in year":
						# Define the task item (the item of the task type) in the current language
						task_item = dictionary["Type"]["Item"][language]

						# If the task type is not "Python" nor "PHP"
						if self.task_type not in ["Python", "PHP"]:
							# Define the text key
							text_key = "first_{}_in_year"

							# Make the task item lowercase
							task_item = task_item.lower()

						# If the task type is "Python" or "PHP"
						if self.task_type in ["Python", "PHP"]:
							# Define the text key
							text_key = "first_{}_in_year, feminine"

							# Define the task item ask the "{}_task" formatted with the task item, in the current language
							task_item = self.texts["{}_task"][language].format(task_item)

						# Define the text as the text of the text key being formatted with the task item, in the current language
						text = self.Language.texts[text_key][language].format(task_item)

					# Add the text to the state "Texts" dictionary with the key, in the current language
					states_dictionary["Texts"][key][language] = text

		# Return the local states dictionary
		return states_dictionary

	def Define_Year_Summary_Data(self, entry, language):
		# Get the entry title
		item = entry["Titles"][language]

		# Return it
		return item

	def Show_Information(self, dictionary, states):
		# Make a shortcut for the "Task" dictionary
		task = dictionary["Task"]

		# Show a five dash space separator
		print()
		print(self.separators["5"])

		# ---------- #

		# If the class is being used as a module by another Python module
		if self.states["Used as module"] == True:
			# Show the "Class being executed" and the name of the module and class
			# So the user is sure that this is the Tasks module, not another one
			# "Tasks.Register()" (in the user language)
			print()
			print(self.Language.language_texts["class_being_executed"] + ":")
			print("\t" + self.language_texts["Tasks.Register"])

		# ---------- #

		# Show the text about the registered task
		print()
		print(self.language_texts["this_task_was_registered"] + ":")

		# Iterate through the list of small languages
		for language in self.languages["small"]:
			# Get the translated language in the user language
			translated_language = self.languages["full_translated"][language][self.user_language]

			# Show the translated language and the task title in the current language
			print("\t" + translated_language + ":")
			print("\t" + task["Titles"][language])
			print()

		# ---------- #

		# Show the "Type" text
		print(self.Language.language_texts["type, title()"] + ":")

		# Define an empty list of texts
		texts = []

		# Iterate through the list of small languages
		for language in self.languages["small"]:
			# Define the type text with a tab and the plural type in the current language
			text = "\t" + dictionary["Type"]["Names"]["Plural"][language]

			# If the text is not inside the list of texts
			if text not in texts:
				# Show the task type in the current language
				print(text)

			# Add the text to the list of texts
			texts.append(text)

		# ---------- #

		# Show the "When" text and the entry date in the user timezone
		print()
		print(self.Language.language_texts["when, title()"] + ":")
		print("\t" + dictionary["Entry"]["Dates"]["Timezone"])

		# ---------- #

		# If there are states, show them
		if (
			"States" in dictionary and
			dictionary["States"]["Texts"] != {}
		):
			# Show the "States" text
			print()
			print(self.Language.language_texts["states, title()"] + ":")

			# Show the state texts in the user language
			for key in dictionary["States"]["Texts"]:
				language_text = dictionary["States"]["Texts"][key][self.user_language]

				print("\t" + language_text)

		# ---------- #

		# Show the task description in the user language
		print()
		print(self.language_texts["task_description_in"] + " " + self.full_user_language + ":")
		print("[" + task["Descriptions"][self.user_language] + "]")

		# Show the text telling the user that the class wrote on the current Diary Slim
		# And the current Diary Slim date
		date = self.dictionary["Diary Slim"]["Date"]["Timezone"]["DateTime"]["Formats"]["[Day name], [Day] [Month name] [Year]"][self.user_language]

		print()
		print(self.language_texts["the_task_description_was_written_on_the_current_diary_slim"] + ":")
		print("\t" + date)

		# If the "Five dash space" state is True
		if states["Five dash space"] == True:
			# Show a five dash space separator
			print()
			print(self.separators["5"])

		# If the user finished reading the information summary
		# And the "Ask for input" state is True
		if states["Ask for input"] == True:
			# Ask for input before ending the execution of the class
			self.Input.Type(self.Language.language_texts["press_enter_when_you_finish_reading_the_information_summary"])