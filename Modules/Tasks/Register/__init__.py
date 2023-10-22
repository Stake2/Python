# Register.py

from Tasks.Tasks import Tasks as Tasks

class Register(Tasks):
	def __init__(self, dictionary = {}, show_text = True):
		super().__init__()

		self.dictionary = dictionary

		# Ask for the task information
		if self.dictionary == {}:
			self.Select_Task_Type()
			self.Type_Task_Information()

		if self.dictionary != {}:
			self.dictionary["large_bar"] = False
			self.dictionary["input"] = False

		# Define the task variable to make typing the task dictionary easier
		self.task = self.dictionary["Task"]

		if "Descriptions" not in self.task:
			self.task["Descriptions"] = self.task["Titles"]

		if "States" not in self.task:
			self.task["States"] = {
				"First task in year": False,
				"First task type task in year": False
			}

		if type(self.dictionary["Type"]) == str:
			self.dictionary["Type"] = self.task_types[self.dictionary["Type"]]

		self.dictionary["Entry"].update({
			"Dates": {
				"UTC": self.dictionary["Entry"]["Date"]["UTC"]["DateTime"]["Formats"]["YYYY-MM-DDTHH:MM:SSZ"],
				"Timezone": self.dictionary["Entry"]["Date"]["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"]
			},
			"Diary Slim": {
				"Text": ""
			}
		})

		# Database related methods
		self.Register_In_JSON()
		self.Create_Entry_File()
		self.Add_Entry_File_To_Year_Folder()

		self.Write_On_Diary_Slim()

		self.Show_Information(self.dictionary)

		# Re-initiate the root class to update files
		super().__init__()

	def Select_Task_Type(self):
		options = self.task_types["Plural"]["en"]
		language_options = self.task_types["Plural"][self.user_language]

		show_text = self.language_texts["task_types"]
		select_text = self.language_texts["select_a_task_type"]

		dictionary = self.Input.Select(options, language_options = language_options, show_text = show_text, select_text = select_text)

		self.dictionary = {
			"Type": self.task_types[dictionary["option"]],
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
			"large_bar": True,
			"input": True
		}

	def Type_Task_Information(self):
		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language][self.user_language]

			type_text = self.language_texts["describe_the_task_in"] + " " + translated_language

			self.dictionary["Task"]["Titles"][language] = self.dictionary["Type"]["Texts"][language]

			# Ask for the task item if it is present in the task text
			if "{" in self.dictionary["Task"]["Titles"][language]:
				if hasattr(self, "re") == False:
					import re

					self.re = re

				print()
				print(self.dictionary["Task"]["Titles"][language])

				# List the text format templates of the task items
				items = self.re.findall("\{[(\w+\s)]+\}", self.dictionary["Task"]["Titles"][language])

				for item in items:
					# Remove the braces of the task item
					item_text = item.replace("{", "").replace("}", "")

					# Ask for the task item
					task_item = self.Input.Type(item_text.capitalize())

					# If there is the "(s)" plural prototype text on the task title template
					if "(s)" in self.dictionary["Task"]["Titles"][language]:
						# Determine if the typed task item has commas
						has_comma = False

						if "," in task_item or ", " in task_item:
							has_comma = True

							for list_item in [",", ", "]:
								if list_item in task_item:
									comma = list_item

						# If it has, split each item of the task item into a list of sub items
						if has_comma == True:
							sub_items = task_item.split(comma)

							# Reset the task item string into an empty string
							task_item = ""

							# Iterate through the sub items list
							for sub_item in sub_items:
								# If the sub item is not the first one and the list has only two items
								if sub_item != sub_items[0] and len(sub_items) == 2:
									# Add a space before the second item
									task_item += " "

								# If the sub item is equal to the last item, add the "and" text and a space
								if sub_item == sub_items[-1]:
									task_item += self.JSON.Language.texts["and"][language] + " "

								task_item += sub_item

								# If the sub item is equal to the last one and the list has more than two items, add a comma and a space
								if sub_item != sub_items[-1] and len(sub_items) != 2:
									task_item += ", "

							# Replace the parenthesis of the task title template
							self.dictionary["Task"]["Titles"][language] = self.dictionary["Task"]["Titles"][language].replace("(s)", "s")

						# Else, remove the "(s)" plural prototype text
						else:
							self.dictionary["Task"]["Titles"][language] = self.dictionary["Task"]["Titles"][language].replace("(s)", "")

					# Replace the text format template with the typed task item
					self.dictionary["Task"]["Titles"][language] = self.dictionary["Task"]["Titles"][language].replace(item, task_item)

			# Define the task description as the task title plus two new lines
			self.dictionary["Task"]["Descriptions"][language] = self.dictionary["Task"]["Titles"][language] + "." + "\n\n"

			# Ask for the task description
			self.dictionary["Task"]["Descriptions"][language] += self.Input.Lines(type_text)["string"]

	def Register_In_JSON(self):
		self.task_type = self.dictionary["Type"]["Plural"]["en"]

		dicts = [
			self.dictionaries["Tasks"],
			self.dictionaries["Task type"][self.task_type]
		]

		# Add one to the entry, task type entry, and root task type entry numbers
		for dict_ in dicts:
			dict_["Numbers"]["Total"] += 1

			if "Per Task Type" in dict_["Numbers"]:
				dict_["Numbers"]["Per Task Type"][self.task_type] += 1

		if self.dictionaries["Tasks"]["Numbers"]["Total"] == 1:
			self.task["States"]["First task in year"] = True

		if self.dictionaries["Task type"][self.task_type]["Numbers"]["Total"] == 1:
			self.task["States"]["First task type task in year"] = True

		# Define sanitized version of entry name for files
		self.task["Name"] = {
			"Normal": str(self.dictionaries["Tasks"]["Numbers"]["Total"]) + ". " + self.task_type + " (" + self.dictionary["Entry"]["Dates"]["Timezone"] + ")",
			"Sanitized": ""
		}

		self.task["Name"]["Sanitized"] = self.task["Name"]["Normal"].replace(":", ";").replace("/", "-")

		# Add to the "Tasks" lists
		for dict_ in dicts:
			if self.task["Name"]["Normal"] not in dict_["Entries"]:
				dict_["Entries"].append(self.task["Name"]["Normal"])

		self.key = self.task["Name"]["Normal"]

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

		# Add task dictionary to task type tasks dictionary
		self.dictionaries["Task type"][self.task_type]["Dictionary"][self.key] = self.dictionaries["Tasks"]["Dictionary"][self.key].copy()

		# Update the "Tasks.json" file
		self.JSON.Edit(self.folders["task_history"]["current_year"]["tasks"], self.dictionaries["Tasks"])

		# Update the task type "Tasks.json" file
		self.JSON.Edit(self.dictionary["Type"]["Folders"]["per_task_type"]["tasks"], self.dictionaries["Task type"][self.task_type])

		# Add to the root and task type "Entry list.txt" file
		self.File.Edit(self.folders["task_history"]["current_year"]["entry_list"], self.task["Name"]["Normal"], "a")
		self.File.Edit(self.dictionary["Type"]["Folders"]["per_task_type"]["entry_list"], self.task["Name"]["Normal"], "a")

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
		folder = self.folders["task_history"]["current_year"]["per_task_type"][self.task_type.lower()]["files"]["root"]
		file = folder + self.task["Name"]["Sanitized"] + ".txt"
		self.File.Create(file)

		self.dictionary["Text"] = {
			"General": self.Define_File_Text("General")
		}

		for language in self.languages["small"]:
			self.dictionary["Text"][language] = self.Define_File_Text(language)

		# Write the task text into the task file
		self.File.Edit(file, self.dictionary["Text"]["General"], "w")

	# Define task text per language
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
			text = self.JSON.Language.texts["title, title()"][language]

		if language_parameter == "General":
			text = self.JSON.Language.texts["titles, title()"][language]

		lines.append("\n" + text + ":" + "\n" + "{}")

		lines.extend([
			self.JSON.Language.texts["type, title()"][language] + ":" + "\n" + self.dictionary["Type"]["Plural"][language] + "\n",
			self.Date.texts["times, title()"][language] + ":" + "\n" + "{}",
			self.File.texts["file_name"][language] + ":" + "\n" + self.task["Name"]["Normal"]
		])

		# Add states texts lines
		if self.dictionary["States"]["Texts"] != {}:
			text = "\n" + self.JSON.Language.texts["states, title()"][language] + ":" + "\n"

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

		items.append(descriptions)

		# Define language task text
		file_text = self.Text.From_List(lines)

		return file_text.format(*items)

	def Add_Entry_File_To_Year_Folder(self):
		# Create folders
		for language in self.languages["small"]:
			full_language = self.languages["full"][language]

			# Folder names
			root_folder = self.texts["done_tasks"][language]
			type_folder = self.dictionary["Type"]["Plural"][language]

			# Done tasks folder
			folder = self.current_year["Folders"][full_language]["root"]

			self.current_year["Folders"][full_language][root_folder] = {
				"root": folder + root_folder + "/"
			}

			self.Folder.Create(self.current_year["Folders"][full_language][root_folder]["root"])

			# Task type folder
			folder = self.current_year["Folders"][full_language][root_folder]["root"]

			self.current_year["Folders"][full_language][root_folder][type_folder] = {
				"root": folder + type_folder + "/"
			}

			self.Folder.Create(self.current_year["Folders"][full_language][root_folder][type_folder]["root"])

			# Done tasks file
			folder = self.current_year["Folders"][full_language][root_folder][type_folder]["root"]
			file_name = self.task["Name"]["Sanitized"]
			self.current_year["Folders"][full_language][root_folder][type_folder][file_name] = folder + file_name + ".txt"

			self.File.Create(self.current_year["Folders"][full_language][root_folder][type_folder][file_name])

			self.File.Edit(self.current_year["Folders"][full_language][root_folder][type_folder][file_name], self.dictionary["Text"][language], "w")

			# Firsts Of The Year subfolder folder
			firsts_of_the_year_text = self.JSON.Language.texts["firsts_of_the_year"][language]
			subfolder_name = self.dictionary["Type"]["Subfolders"][language]

			folder = self.current_year["Folders"][full_language][firsts_of_the_year_text]["root"]

			self.current_year["Folders"][full_language][firsts_of_the_year_text][subfolder_name] = {
				"root": folder + subfolder_name + "/"
			}

			self.Folder.Create(self.current_year["Folders"][full_language][firsts_of_the_year_text][subfolder_name]["root"])

			# Firsts Of The Year task type folder
			item_folder = self.dictionary["Type"]["Items"][language]

			folder = self.current_year["Folders"][full_language][firsts_of_the_year_text][subfolder_name]["root"]
			
			self.current_year["Folders"][full_language][firsts_of_the_year_text][subfolder_name][item_folder] = {
				"root": folder + item_folder + "/"
			}

			self.Folder.Create(self.current_year["Folders"][full_language][firsts_of_the_year_text][subfolder_name][item_folder]["root"])

			# First task type task in year file
			if self.task["States"]["First task type task in year"] == True:
				folder = self.current_year["Folders"][full_language][firsts_of_the_year_text][subfolder_name][item_folder]["root"]

				self.current_year["Folders"][full_language][firsts_of_the_year_text][subfolder_name][item_folder][file_name] = folder + file_name + ".txt"
				self.File.Create(self.current_year["Folders"][full_language][firsts_of_the_year_text][subfolder_name][item_folder][file_name])

				self.File.Edit(self.current_year["Folders"][full_language][firsts_of_the_year_text][subfolder_name][item_folder][file_name], self.dictionary["Text"][language], "w")

	def Write_On_Diary_Slim(self):
		self.dictionary["Entry"]["Diary Slim"]["Text"] = self.task["Descriptions"][self.user_language]

		# If there are states, add the texts to the Diary Slim text
		if self.dictionary["States"]["States"] != {}:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.JSON.Language.language_texts["states, title()"] + ":" + "\n"

			for key in self.dictionary["States"]["Texts"]:
				self.dictionary["Entry"]["Diary Slim"]["Text"] += self.dictionary["States"]["Texts"][key][self.user_language]

				if key != list(self.dictionary["States"]["Texts"].keys())[-1]:
					self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n"

		from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

		# Write on Diary Slim
		Write_On_Diary_Slim_Module(self.dictionary["Entry"]["Diary Slim"]["Text"], self.dictionary["Entry"]["Dates"]["Timezone"], add_dot = False, show_text = False)