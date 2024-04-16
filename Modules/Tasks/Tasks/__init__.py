# Tasks.py

# Import the "importlib" module
import importlib

class Tasks(object):
	def __init__(self):
		# Define the module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Import classes method
		self.Import_Classes()

		# Folders and files method
		self.Define_Folders_And_Files()

		# Class methods
		self.Define_Types()
		self.Define_Registry_Format()

	def Define_Basic_Variables(self):
		from copy import deepcopy

		# Import the JSON module
		from Utility.JSON import JSON as JSON

		self.JSON = JSON()

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

		# Get the modules list
		self.modules = self.JSON.To_Python(self.folders["apps"]["modules"]["modules"])

		# Create a list of the modules that will not be imported
		remove_list = [
			"Define_Folders",
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

		# Make a backup of the module folders
		self.module_folders = {}

		for item in ["modules", "module_files"]:
			self.module_folders[item] = deepcopy(self.folders["apps"][item][self.module["key"]])

		# Define the local folders dictionary as the Folder folders dictionary
		self.folders = self.Folder.folders

		# Restore the backup of the module folders
		for item in ["modules", "module_files"]:
			self.folders["apps"][item][self.module["key"]] = self.module_folders[item]

		# Get the switches dictionary from the "Global Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# Get the Languages dictionary
		self.languages = self.JSON.Language.languages

		# Get the user language and full user language
		self.user_language = self.JSON.Language.user_language
		self.full_user_language = self.JSON.Language.full_user_language

		# Get the Sanitize method of the File class
		self.Sanitize = self.File.Sanitize

		# Get the current date from the Date module
		self.date = self.Date.date

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

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

	def Import_Classes(self):
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
		self.current_year = self.Years.years["Current year"]

		# Replace the "self.folders" folder dictionary with the "Productivity" network folder dictionary
		self.folders = self.folders["Notepad"]["Data Networks"]["Productivity"]

		self.folders["Task History"]["Current year"] = self.folders["Task History"][str(self.date["Units"]["Year"])]

		# Define the "History" dictionary
		self.history = {
			"Key": "",
			"Numbers": {
				"Productive things": ""
			},
			"Folder": self.folders["Task History"]["root"]
		}

	def Define_Types(self):
		self.task_types = self.JSON.To_Python(self.folders["Data"]["Types"])

		# Iterate through the English plural task types list
		i = 0
		for plural_task_type in self.task_types["Plural"]["en"]:
			# Create task type dictionary
			self.task_types[plural_task_type] = {
				"Singular": {},
				"Plural": {},
				"Folders": {},
				"Subfolders": {},
				"Items": {},
				"Texts": {}
			}

			# Define singular and plural types
			for language in self.languages["small"]:
				for item in ["Singular", "Plural"]:
					self.task_types[plural_task_type][item][language] = self.task_types[item][language][i]

			# Create "Per Task Type" task type folder
			self.folders["Task History"]["Current year"]["Per Task Type"][plural_task_type] = {
				"root": self.folders["Task History"]["Current year"]["Per Task Type"]["root"] + plural_task_type + "/"
			}

			self.Folder.Create(self.folders["Task History"]["Current year"]["Per Task Type"][plural_task_type]["root"])

			# Create "Tasks.json" file in "Per Task Type" task type folder
			self.folders["Task History"]["Current year"]["Per Task Type"][plural_task_type]["Tasks"] = self.folders["Task History"]["Current year"]["Per Task Type"][plural_task_type]["root"] + "Tasks.json"
			self.File.Create(self.folders["Task History"]["Current year"]["Per Task Type"][plural_task_type]["Tasks"])

			# Create "Entry list.txt" file in "Per Task Type" task type folder
			self.folders["Task History"]["Current year"]["Per Task Type"][plural_task_type]["Entry list"] = self.folders["Task History"]["Current year"]["Per Task Type"][plural_task_type]["root"] + "Entry list.txt"
			self.File.Create(self.folders["Task History"]["Current year"]["Per Task Type"][plural_task_type]["Entry list"])

			# Create "Files" folder on "Per Task Type" task type folder
			self.folders["Task History"]["Current year"]["Per Task Type"][plural_task_type]["Files"] = {
				"root": self.folders["Task History"]["Current year"]["Per Task Type"][plural_task_type]["root"] + "Files/"
			}

			self.Folder.Create(self.folders["Task History"]["Current year"]["Per Task Type"][plural_task_type]["Files"]["root"])

			# Define type folders and files
			self.task_types[plural_task_type]["Folders"] = {
				"Per Task Type": self.folders["Task History"]["Current year"]["Per Task Type"][plural_task_type]
			}

			# Define the task type subfolders and item
			for language in self.languages["small"]:
				for item in ["Art", "Programming"]:
					if plural_task_type in self.task_types["subfolders, type: dict"][item]:
						self.task_types[plural_task_type]["Subfolders"][language] = self.Language.texts[item.lower() + ", title()"][language]

				# Define the task item
				self.task_types[plural_task_type]["Items"][language] = self.task_types["items, type: dict"][plural_task_type][language]

				# Define the task texts
				self.task_types[plural_task_type]["Texts"][language] = self.task_types["task_texts, type: dict"][plural_task_type][language]

			i += 1

		# Write the types dictionary into the "Types.json" file
		self.JSON.Edit(self.folders["Data"]["Types"], self.task_types)

	def Define_Registry_Format(self):
		from copy import deepcopy

		# Define default Tasks dictionary template
		self.template = {
			"Numbers": {
				"Total": 0,
			},
			"Entries": [],
			"Dictionary": {}
		}

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

		if (
			self.File.Contents(self.folders["Task History"]["History"])["lines"] != [] and
			self.JSON.To_Python(self.folders["Task History"]["History"])["Years"] != []
		):
			# Get the History dictionary from file
			self.dictionaries["History"] = self.JSON.To_Python(self.folders["Task History"]["History"])

		# If the current year is not inside the "History" years list, add it to the list
		if self.current_year["Number"] not in self.dictionaries["History"]["Years"]:
			self.dictionaries["History"]["Years"].append(self.current_year["Number"])

		tasks = 0

		# Update the number of entries of all years
		for year in self.Date.Create_Years_List(function = str):
			# Get the year folder and the entries file
			year_folder = self.folders["Task History"]["root"] + year + "/"
			entries_file = year_folder + "Tasks.json"

			# If the file exists and it is not empty
			if (
				self.File.Exist(entries_file) == True and
				self.File.Contents(entries_file)["lines"] != []
			):
				# Add the number of lines of the file to the local number of entries
				tasks += self.JSON.To_Python(entries_file)["Numbers"]["Total"]

			# Add the year to the Years list if it is not inside it
			if year not in self.dictionaries["History"]["Years"]:
				self.dictionaries["History"]["Years"].append(year)

		# Sort the Years list
		self.dictionaries["History"]["Years"] = sorted(self.dictionaries["History"]["Years"], key = str.lower)

		# Update the number of years with the length of the years list
		self.dictionaries["History"]["Numbers"]["Years"] = len(self.dictionaries["History"]["Years"])

		# Define the number of Entries of all years as the local number of entries
		self.dictionaries["History"]["Numbers"]["Tasks"] = tasks

		# Update the "History.json" file with the updated "History" dictionary
		self.JSON.Edit(self.folders["Task History"]["History"], self.dictionaries["History"])

		# Create the "Per Task Type" key inside the "Numbers" dictionary of the "Tasks" dictionary
		self.dictionaries["Tasks"]["Numbers"]["Per Task Type"] = {}

		# If the "Tasks.json" is not empty, get the Tasks dictionary from it
		if (
			self.File.Contents(self.folders["Task History"]["Current year"]["Tasks"])["lines"] != [] and
			self.JSON.To_Python(self.folders["Task History"]["Current year"]["Tasks"])["Entries"] != []
		):
			self.dictionaries["Tasks"] = self.JSON.To_Python(self.folders["Task History"]["Current year"]["Tasks"])

		# Iterate through the English plural task types list
		for plural_task_type in self.task_types["Plural"]["en"]:
			key = plural_task_type.lower().replace(" ", "_")

			# Define default task type dictionary
			self.dictionaries["Task type"][plural_task_type] = deepcopy(self.template)

			# If the task type "Tasks.json" is not empty, get the task type Tasks dictionary from it
			if (
				self.File.Contents(self.folders["Task History"]["Current year"]["Per Task Type"][plural_task_type]["Tasks"])["lines"] != [] and
				self.JSON.To_Python(self.folders["Task History"]["Current year"]["Per Task Type"][plural_task_type]["Tasks"])["Entries"] != []
			):
				self.dictionaries["Task type"][plural_task_type] = self.JSON.To_Python(self.folders["Task History"]["Current year"]["Per Task Type"][plural_task_type]["Tasks"])

			# Add the task type number to the root numbers per task type if it does not exist in there
			if plural_task_type not in self.dictionaries["Tasks"]["Numbers"]["Per Task Type"]:
				self.dictionaries["Tasks"]["Numbers"]["Per Task Type"][plural_task_type] = 0

			# Else, define the root total number per task type as the number inside the Tasks dictionary per task type
			if plural_task_type in self.dictionaries["Tasks"]["Numbers"]["Per Task Type"]:
				self.dictionaries["Tasks"]["Numbers"]["Per Task Type"][plural_task_type] = self.dictionaries["Task type"][plural_task_type]["Numbers"]["Total"]

			# Update the per task type "Tasks.json" file with the updated per type Tasks dictionary
			self.JSON.Edit(self.folders["Task History"]["Current year"]["Per Task Type"][plural_task_type]["Tasks"], self.dictionaries["Task type"][plural_task_type])

		# Update the "Tasks.json" file with the updated Tasks dictionary
		self.JSON.Edit(self.folders["Task History"]["Current year"]["Tasks"], self.dictionaries["Tasks"])

	def Define_States_Dictionary(self, dictionary):
		states_dictionary = {
			"States": {},
			"Texts": {}
		}

		# Define keys for the states
		keys = [
			"First task in year",
			"First task type task in year"
		]

		# Iterate through the states keys
		for key in keys:
			# If the state is True
			if dictionary["Task"]["States"][key] == True:
				state = True

				# Define the state dictionary
				states_dictionary["States"][key] = state

				# Define the state texts of the current state dictionary
				states_dictionary["Texts"][key] = {}

				for language in self.languages["small"]:
					text = ""

					if key != "First task type task in year":
						text_key = key.lower().replace(" ", "_")

						if text_key in self.Language.texts:
							text = self.Language.texts[text_key][language]

						else:
							text = self.texts[text_key][language]

					if key == "First task type task in year":
						task_item = dictionary["Type"]["Items"][language]

						if self.task_type not in ["Python", "PHP"]:
							text_key = "first_{}_in_year"
							task_item = task_item.lower()

						if self.task_type in ["Python", "PHP"]:
							text_key = "first_{}_in_year, feminine"
							task_item = self.texts["{}_task"][language].format(task_item)

						text = self.Language.texts[text_key][language].format(task_item)

					states_dictionary["Texts"][key][language] = text

		return states_dictionary

	def Define_Year_Summary_Data(self, entry, language):
		# Get the entry title
		item = entry["Titles"][language]

		return item

	def Show_Information(self, dictionary):
		task = dictionary["Task"]

		print()
		print(self.separators["5"])
		print()

		print(self.language_texts["this_task_was_registered"] + ":")

		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language][self.user_language]

			print("\t" + translated_language + ":")
			print("\t" + task["Titles"][language])
			print()

		print(self.Language.language_texts["type, title()"] + ":")

		types = []

		for language in self.languages["small"]:
			text = "\t" + dictionary["Type"]["Plural"][language]

			if text not in types:
				types.append(text)

		for item in types:
			print(item)

		print()

		print(self.Language.language_texts["when, title()"] + ":")
		print("\t" + dictionary["Entry"]["Dates"]["Timezone"])

		# If there are states, show them
		if (
			"States" in dictionary and
			dictionary["States"]["Texts"] != {}
		):
			print()
			print(self.Language.language_texts["states, title()"] + ":")

			for key in dictionary["States"]["Texts"]:
				print("\t" + dictionary["States"]["Texts"][key][self.user_language])

		show_task_description = self.Input.Yes_Or_No(self.language_texts["show_task_description"] + "?" + " (" + self.Language.language_texts["can_be_long, feminine"] + ")")

		if show_task_description == True:
			print()
			print(self.language_texts["task_description_in"] + " " + self.full_user_language + ":")
			print("[" + task["Descriptions"][self.user_language] + "]")

		if dictionary["large_bar"] == True:
			print()
			print(self.separators["5"])

		# If the user finished reading the information summary, ask for input before ending execution
		if dictionary["input"] == True:
			self.Input.Type(self.Language.language_texts["press_enter_when_you_finish_reading_the_info_summary"])