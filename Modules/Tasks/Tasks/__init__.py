# Tasks.py

class Tasks(object):
	def __init__(self):
		self.Define_Basic_Variables()

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.Define_Texts()

		# Import the Years class
		from Years.Years import Years as Years
		self.Years = Years()

		self.Define_Folders_And_Files()

		self.Define_Types()
		self.Define_Registry_Format()

	def Define_Basic_Variables(self):
		from Utility.Global_Switches import Global_Switches as Global_Switches

		from Utility.File import File as File
		from Utility.Folder import Folder as Folder
		from Utility.Date import Date as Date
		from Utility.Input import Input as Input
		from Utility.JSON import JSON as JSON
		from Utility.Text import Text as Text

		self.switches = Global_Switches().switches["global"]

		self.File = File()
		self.Folder = Folder()
		self.Date = Date()
		self.Input = Input()
		self.JSON = JSON()
		self.Text = Text()

		self.languages = self.JSON.Language.languages

		self.user_language = self.JSON.Language.user_language
		self.full_user_language = self.JSON.Language.full_user_language

		self.Sanitize = self.File.Sanitize

		self.folders = self.Folder.folders

		self.date = self.Date.date

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.JSON.Language.Item(self.texts)

		self.large_bar = "-----"
		self.dash_space = "-"

	def Define_Folders_And_Files(self):
		self.current_year = self.Years.current_year

		# Folders dictionary
		self.folders = self.Folder.Contents(self.folders["notepad"]["networks"]["productive_network"]["root"], lower_key = True)["dictionary"]

		self.folders["task_history"]["current_year"] = self.folders["task_history"][str(self.date["year"])]

	def Define_Types(self):
		self.task_types = self.JSON.To_Python(self.folders["data"]["types"])

		# Iterate through the English plural task types list
		i = 0
		for plural_task_type in self.task_types["Plural"]["en"]:
			key = plural_task_type.lower().replace(" ", "_")

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
			self.folders["task_history"]["current_year"]["per_task_type"][key] = {
				"root": self.folders["task_history"]["current_year"]["per_task_type"]["root"] + plural_task_type + "/"
			}

			self.Folder.Create(self.folders["task_history"]["current_year"]["per_task_type"][key]["root"])

			# Create "Tasks.json" file in "Per Task Type" task type folder
			self.folders["task_history"]["current_year"]["per_task_type"][key]["tasks"] = self.folders["task_history"]["current_year"]["per_task_type"][key]["root"] + "Tasks.json"
			self.File.Create(self.folders["task_history"]["current_year"]["per_task_type"][key]["tasks"])

			# Create "Entry list.txt" file in "Per Task Type" task type folder
			self.folders["task_history"]["current_year"]["per_task_type"][key]["entry_list"] = self.folders["task_history"]["current_year"]["per_task_type"][key]["root"] + "Entry list.txt"
			self.File.Create(self.folders["task_history"]["current_year"]["per_task_type"][key]["entry_list"])

			# Create "Files" folder on "Per Task Type" task type folder
			self.folders["task_history"]["current_year"]["per_task_type"][key]["files"] = {
				"root": self.folders["task_history"]["current_year"]["per_task_type"][key]["root"] + "Files/"
			}

			self.Folder.Create(self.folders["task_history"]["current_year"]["per_task_type"][key]["files"]["root"])

			# Define type folders and files
			self.task_types[plural_task_type]["Folders"] = {
				"per_task_type": self.folders["task_history"]["current_year"]["per_task_type"][key]
			}

			# Define the task type subfolders and item
			for language in self.languages["small"]:
				for item in ["Art", "Programming"]:
					if plural_task_type in self.task_types["subfolders, type: dict"][item]:
						self.task_types[plural_task_type]["Subfolders"][language] = self.JSON.Language.texts[item.lower() + ", title()"][language]

				# Define the task item
				self.task_types[plural_task_type]["Items"][language] = self.task_types["items, type: dict"][plural_task_type][language]

				# Define the task texts
				self.task_types[plural_task_type]["Texts"][language] = self.task_types["task_texts, type: dict"][plural_task_type][language]

			i += 1

		# Write the types dictionary into the "Types.json" file
		self.JSON.Edit(self.folders["data"]["types"], self.task_types)

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
			"Task Type": {}
		}

		if self.File.Contents(self.folders["task_history"]["history"])["lines"] != [] and self.JSON.To_Python(self.folders["task_history"]["history"])["Years"] != []:
			# Get the History dictionary from file
			self.dictionaries["History"] = self.JSON.To_Python(self.folders["task_history"]["history"])

		# If the current year is not inside the "History" years list, add it to the list
		if self.current_year["Number"] not in self.dictionaries["History"]["Years"]:
			self.dictionaries["History"]["Years"].append(self.current_year["Number"])

		# Update the number of years with the length of the years list
		self.dictionaries["History"]["Numbers"]["Years"] = len(self.dictionaries["History"]["Years"])

		tasks = 0

		# Update the number of entries of all years
		for year in range(self.date["year"], self.date["year"] + 1):
			year = str(year)

			# Get the year folder and the entries file
			year_folder = self.folders["task_history"]["root"] + year + "/"
			entries_file = year_folder + "Tasks.json"

			# If the file exists and it is not empty
			if self.File.Exist(entries_file) == True and self.File.Contents(entries_file)["lines"] != []:
				# Add the number of lines of the file to the local number of entries
				tasks += self.JSON.To_Python(entries_file)["Numbers"]["Total"]

			# Add the year to the Years list if it is not inside it
			if year not in self.dictionaries["History"]["Years"]:
				self.dictionaries["History"]["Years"].append(year)

		# Sort the Years list
		self.dictionaries["History"]["Years"] = sorted(self.dictionaries["History"]["Years"], key = str.lower)

		# Define the number of Entries of all years as the local number of entries
		self.dictionaries["History"]["Numbers"]["Tasks"] = tasks

		# Update the "History.json" file with the new History dictionary
		self.JSON.Edit(self.folders["task_history"]["history"], self.dictionaries["History"])

		# Create the "Per Task Type" key inside the "Numbers" dictionary of the "Tasks" dictionary
		self.dictionaries["Tasks"]["Numbers"]["Per Task Type"] = {}

		# If the "Tasks.json" is not empty, get the Tasks dictionary from it
		if self.File.Contents(self.folders["task_history"]["current_year"]["tasks"])["lines"] != [] and self.JSON.To_Python(self.folders["task_history"]["current_year"]["tasks"])["Entries"] != []:
			self.dictionaries["Tasks"] = self.JSON.To_Python(self.folders["task_history"]["current_year"]["tasks"])

		# Iterate through the English plural task types list
		for plural_task_type in self.task_types["Plural"]["en"]:
			key = plural_task_type.lower().replace(" ", "_")

			# Define default task type dictionary
			self.dictionaries["Task Type"][plural_task_type] = deepcopy(self.template)

			# If the task type "Tasks.json" is not empty, get the task type Tasks dictionary from it
			if self.File.Contents(self.folders["task_history"]["current_year"]["per_task_type"][key]["tasks"])["lines"] != [] and self.JSON.To_Python(self.folders["task_history"]["current_year"]["per_task_type"][key]["tasks"])["Entries"] != []:
				self.dictionaries["Task Type"][plural_task_type] = self.JSON.To_Python(self.folders["task_history"]["current_year"]["per_task_type"][key]["tasks"])

			# Add the task type number to the root numbers per task type if it does not exist in there
			if plural_task_type not in self.dictionaries["Tasks"]["Numbers"]["Per Task Type"]:
				self.dictionaries["Tasks"]["Numbers"]["Per Task Type"][plural_task_type] = 0

			# Else, define the root total number per task type as the number inside the Tasks dictionary per task type
			if plural_task_type in self.dictionaries["Tasks"]["Numbers"]["Per Task Type"]:
				self.dictionaries["Tasks"]["Numbers"]["Per Task Type"][plural_task_type] = self.dictionaries["Task Type"][plural_task_type]["Numbers"]["Total"]

			# Update the per task type "Tasks.json" file with the updated per type Tasks dictionary
			self.JSON.Edit(self.folders["task_history"]["current_year"]["per_task_type"][key]["tasks"], self.dictionaries["Task Type"][plural_task_type])

		# Update the "Tasks.json" file with the updated Tasks dictionary
		self.JSON.Edit(self.folders["task_history"]["current_year"]["tasks"], self.dictionaries["Tasks"])

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

						if text_key in self.JSON.Language.texts:
							text = self.JSON.Language.texts[text_key][language]

						else:
							text = self.texts[text_key][language]

					if key == "First task type task in year":
						task_item = dictionary["Type"]["Items"][language]

						if self.task_type not in ["Python", "PHP"]:
							task_item = task_item.lower()

						if self.task_type in ["Python", "PHP"]:
							task_item = self.texts["{}_task"][language].format(task_item)

						text = self.JSON.Language.texts["first_{}_in_year"][language].format(task_item)

					states_dictionary["Texts"][key][language] = text

		return states_dictionary

	def Show_Information(self, dictionary):
		task = dictionary["Task"]

		print()
		print(self.large_bar)
		print()

		print(self.language_texts["this_task_was_registered"] + ":")

		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language][self.user_language]

			print("\t" + translated_language + ":")
			print("\t" + task["Titles"][language])
			print()

		print(self.JSON.Language.language_texts["type, title()"] + ":")

		types = []

		for language in self.languages["small"]:
			text = "\t" + dictionary["Type"]["Plural"][language]

			if text not in types:
				types.append(text)

		for item in types:
			print(item)

		print()

		print(self.JSON.Language.language_texts["when, title()"] + ":")
		print("\t" + dictionary["Entry"]["Times"]["Timezone"])

		# If there are states, show them
		if "States" in self.dictionary and self.dictionary["States"]["States"] != {}:
			print()
			print(self.JSON.Language.language_texts["states, title()"] + ":")

			for key in self.dictionary["States"]["Texts"]:
				print("\t" + self.dictionary["States"]["Texts"][key][self.user_language])

		show_task_description = self.Input.Yes_Or_No(self.language_texts["show_task_description"] + "?" + " (" + self.language_texts["can_be_long"] + ")")

		if show_task_description == True:
			print()
			print(self.language_texts["task_description_in"] + " " + self.full_user_language + ":")
			print("[" + task["Descriptions"][self.user_language] + "]")

		if dictionary["large_bar"] == True:
			print()
			print(self.large_bar)

		# If the user finished reading the information summary, ask for input before ending execution
		if dictionary["input"] == True:
			self.Input.Type(self.JSON.Language.language_texts["press_enter_when_you_finish_reading_the_info_summary"])