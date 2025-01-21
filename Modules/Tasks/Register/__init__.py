# Register.py

from Tasks.Tasks import Tasks as Tasks

class Register(Tasks):
	def __init__(self, dictionary = {}, show_text = True):
		super().__init__()

		# Define the root dictionary on this class as the parameter dictionary
		self.dictionary = dictionary

		# If the root dictionary is empty
		if self.dictionary == {}:
			# Ask the user to select the task type
			self.Select_Task_Type()

		# If the type of the task type dictionary is a string
		if isinstance(self.dictionary["Type"], str):
			# Transform it into a task type dictionary, using the string as a key
			self.dictionary["Type"] = self.tasks["Types"]["Dictionary"][self.dictionary["Type"]]

		# If the task "Descriptions" dictionary is empty
		if self.dictionary["Task"]["Descriptions"] == {}:
			# Ask the user to type the task information
			self.Type_Task_Information()

		# If the root dictionary is not empty
		if self.dictionary != {}:
			# If the "Final separator" key is not inside the root dictionary
			if "Final separator" not in self.dictionary:
				# Define the "Five dash space" switch as False
				self.dictionary["Five dash space"] = False

			# Define the "Input" switch as False
			self.dictionary["Input"] = False

		# Define a shortcut for the task dictionary
		self.task = self.dictionary["Task"]

		# If the "Descriptions" key is not inside the task dictionary
		if "Descriptions" not in self.task:
			# Define the descriptions dictionary as the titles dictionary
			self.task["Descriptions"] = self.task["Titles"]

		# If the "States" dictionary is not inside the task dictionary
		if "States" not in self.task:
			# Define it with the two default states as False
			self.task["States"] = {
				"First task in year": False,
				"First task type task in year": False
			}

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
		self.Show_Information(self.dictionary)

	def Select_Task_Type(self):
		# Define the list of options and language options
		options = self.tasks["Types"]["Lists"]["Plural"]["en"]
		language_options = self.tasks["Types"]["Lists"]["Plural"][self.user_language]

		# Define the show and select texts
		show_text = self.language_texts["task_types"]
		select_text = self.language_texts["select_a_task_type"]

		# Ask for the user to select a task type
		dictionary = self.Input.Select(options, language_options = language_options, show_text = show_text, select_text = select_text)

		# Redefine the root dictionary to add the type, task, and entry dictionaries, and also some states
		self.dictionary = {
			"Type": self.tasks["Types"]["Dictionary"][dictionary["option"]],
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
			},
			"Five dash space": False,
			"Input": True
		}

	def Type_Task_Information(self):
		# Iterate through the list of small languages
		for language in self.languages["small"]:
			# Get the translated language in the user language
			translated_language = self.languages["full_translated"][language][self.user_language]

			# Define the task title in the current language
			self.JSON.Show(self.dictionary["Type"])
			self.dictionary["Task"]["Titles"][language] = self.dictionary["Type"]["Task texts"][language]

			# If the "{" character is inside the task title in the current language
			# That means the task contains an item
			if "{" in self.dictionary["Task"]["Titles"][language]:
				# If the "re" (regex) module is not present in this class
				# Import it and define it inside the class
				if hasattr(self, "re") == False:
					import re

					self.re = re

				# If the language is not the first one in the list, show a five dash space separator
				if language != self.languages["small"][0]:
					print()
					print(self.separators["5"])

				# Show the "task title" text and the task title
				print()
				print(self.language_texts["task_title"] + ":")
				print("\t" + self.dictionary["Task"]["Titles"][language])

				# List the text format templates of the task items
				items = self.re.findall("\{[(\w+\s)]+\}", self.dictionary["Task"]["Titles"][language])

				# Iterate through the list of items
				for item in items:
					# Remove the braces of the task item
					item_text = item.replace("{", "").replace("}", "")

					# Ask for the task item
					task_item = self.Input.Type(item_text.capitalize())

					# If there is the "(s)" plural prototype text on the task title template
					if "(s)" in self.dictionary["Task"]["Titles"][language]:
						# Determine if the typed task item has commas
						has_comma = False

						# If there are commas in the task item
						if (
							"," in task_item or
							", " in task_item
						):
							# Define the state as True, and get the type of comma (with or without space)
							has_comma = True

							for list_item in [",", ", "]:
								if list_item in task_item:
									comma = list_item

						# If it has, split each item of the task item into a list of sub items
						if has_comma == True:
							# Get the sub-items on the task item based on the comma
							sub_items = task_item.split(comma)

							# Reset the task item string into an empty string
							task_item = ""

							# Iterate through the list of sub items
							for sub_item in sub_items:
								# If the sub item is not the first one
								# And the list has only two items
								if (
									sub_item != sub_items[0] and
									len(sub_items) == 2
								):
									# Add a space before the second item
									task_item += " "

								# If the sub item is equal to the last item, add the "and" text in the current language and a space
								if sub_item == sub_items[-1]:
									task_item += self.Language.texts["and"][language] + " "

								# Add the sub item
								task_item += sub_item

								# If the sub item is equal to the last one
								# And the list has more than two items, add a comma and a space
								if (
									sub_item != sub_items[-1] and
									len(sub_items) != 2
								):
									task_item += ", "

							# Remove the parenthesis of the task title template
							self.dictionary["Task"]["Titles"][language] = self.dictionary["Task"]["Titles"][language].replace("(s)", "s")

						# Else, remove the "(s)" plural prototype text
						else:
							self.dictionary["Task"]["Titles"][language] = self.dictionary["Task"]["Titles"][language].replace("(s)", "")

					# Replace the text format template with the typed task item
					self.dictionary["Task"]["Titles"][language] = self.dictionary["Task"]["Titles"][language].replace(item, task_item)

			# Define the task description as the task title plus two new lines
			self.dictionary["Task"]["Descriptions"][language] = self.dictionary["Task"]["Titles"][language] + "." + "\n\n"

			# Show a five dash space separator
			print()
			print(self.separators["5"])

			# Define the type text to show to the user
			type_text = self.language_texts["describe_the_task_in"] + " " + translated_language + ":\n"

			# Ask for the user to write the task description in various lines
			self.dictionary["Task"]["Descriptions"][language] += self.Input.Lines(type_text)["string"]

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

		# Get the States dictionary
		self.dictionary["States"] = self.Define_States_Dictionary(self.dictionary)

		if self.dictionary["States"]["States"] != {}:
			self.dictionaries["Tasks"]["Dictionary"][self.key]["States"] = self.dictionary["States"]["States"]

			# If the "First task type task in year" state is True
			# And the "Custom task item" key is present in the "Task" dictionary
			if (
				self.task["States"]["First task type task in year"] == True and
				"Custom task item" in self.dictionary["Task"]
			):
				# Define the key
				key = "First task type task in year"

				# Iterate through the list of small languages
				for language in self.languages["small"]:
					# Get the state text in the current language
					language_text = self.dictionary["States"]["Texts"][key][language]

					# If the task item is inside the language text
					if self.dictionary["Type"]["Item"][language] in language_text:
						task_item = self.dictionary["Type"]["Item"][language]

						to_replace = self.dictionary["Task"]["Custom task item"][language]

						language_text = language_text.replace(task_item, task_item + " " + to_replace)

					# Update the state text in the "States" dictionary in the current language
					self.dictionary["States"]["Texts"][key][language] = language_text

		# Add task dictionary to task type tasks dictionary
		self.dictionaries["Task type"][self.task_type]["Dictionary"][self.key] = self.dictionaries["Tasks"]["Dictionary"][self.key].copy()

		# Update the "Tasks.json" file
		self.JSON.Edit(self.tasks["Folders"]["Task History"]["Current year"]["Tasks"], self.dictionaries["Tasks"])

		# Update the task type "Tasks.json" file
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

		# Define the task file
		folder = self.tasks["Folders"]["Task History"]["Current year"]["Per Task Type"][self.task_type]["Files"]["root"]
		file = folder + self.task["Name"]["Sanitized"] + ".txt"
		self.File.Create(file)

		self.dictionary["Text"] = {
			"General": self.Define_File_Text("General")
		}

		for language in self.languages["small"]:
			self.dictionary["Text"][language] = self.Define_File_Text(language)

		# Write the task text into the task file
		self.File.Edit(file, self.dictionary["Text"]["General"], "w")

	# Define the task text per language
	def Define_File_Text(self, language_parameter = None):
		if language_parameter != "General":
			language = language_parameter

		if language_parameter == "General":
			language = self.user_language

		full_language = self.languages["full"][language]

		# Define task text lines
		lines = [
			self.texts["number, title()"][language] + ": " + str(self.dictionaries["Tasks"]["Numbers"]["Total"]),
			self.texts["task_type_number"][language] + ": " + str(self.dictionaries["Task type"][self.task_type]["Numbers"]["Total"])
		]

		# Add task title lines
		if language_parameter != "General":
			text = self.Language.texts["title, title()"][language]

		if language_parameter == "General":
			text = self.Language.texts["titles, title()"][language]

		lines.append("\n" + text + ":" + "\n" + "{}")

		lines.extend([
			self.Language.texts["type, title()"][language] + ":" + "\n" + self.dictionary["Type"]["Names"]["Plural"][language] + "\n",
			self.Date.texts["times, title()"][language] + ":" + "\n" + "{}",
			self.File.texts["file_name"][language] + ":" + "\n" + self.task["Name"]["Normal"]
		])

		# Add states texts lines
		if self.dictionary["States"]["Texts"] != {}:
			text = "\n" + self.Language.texts["states, title()"][language] + ":" + "\n"

			for key in self.dictionary["States"]["Texts"]:
				language_text = self.dictionary["States"]["Texts"][key][language]

				text += language_text

				if key != list(self.dictionary["States"]["Texts"].keys())[-1]:
					text += "\n"

			lines.append(text)

		# Add task description lines
		if language_parameter != "General":
			text = self.texts["task_description"][language]
			line_break = "\n"

		if language_parameter == "General":
			text = self.texts["task_descriptions"][language]
			line_break = "\n\n"

		# If the description of the task is not the same as the task title
		if self.dictionary["Task"]["Titles"]["en"] != self.dictionary["Task"]["Descriptions"]["en"]:
			lines.append("\n" + text + ":" + line_break + "{}")

		# Define items to be added to file text format
		items = []

		# Add task titles to items list
		titles = ""

		if language_parameter != "General":
			titles = self.task["Titles"][language] + "\n"

		if language_parameter == "General":
			for language in self.languages["small"]:
				titles += self.task["Titles"][language] + "\n"

		items.append(titles)

		# Add times to items list
		times = ""

		for key in ["UTC", "Timezone"]:
			time = self.dictionary["Entry"]["Dates"][key]

			times += time + "\n"

		items.append(times)

		# Add task descriptions to items list
		descriptions = ""

		if language_parameter != "General":
			descriptions = self.task["Descriptions"][language]

		if language_parameter == "General":
			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				descriptions += full_language + ":" + "\n" + self.task["Descriptions"][language]

				if language != self.languages["small"][-1]:
					descriptions += "\n\n"

		# If the description of the task is not the same as the task title
		if self.dictionary["Task"]["Titles"]["en"] != self.dictionary["Task"]["Descriptions"]["en"]:
			items.append(descriptions)

		# Define language task text
		file_text = self.Text.From_List(lines, next_line = True)

		return file_text.format(*items)

	def Add_Entry_File_To_Year_Folder(self):
		# Create the folders
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

		# If there are states, add the texts to the Diary Slim text
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
		Write_On_Diary_Slim_Module(dictionary)