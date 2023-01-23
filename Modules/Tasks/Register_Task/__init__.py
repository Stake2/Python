# Register_Task.py

from Tasks.Tasks import Tasks as Tasks

from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

class Register_Task(Tasks):
	def __init__(self, task_dictionary = {}, show_text = True):
		super().__init__()

		self.task_dictionary = task_dictionary

		if self.task_dictionary == {}:
			self.Select_Task_Type()
			self.Type_Task_Information()

		if self.task_dictionary != {}:
			self.task_dictionary["large_bar"] = False
			self.task_dictionary["input"] = False

			if "descriptions" not in self.task_dictionary:
				self.task_dictionary["descriptions"] = self.task_dictionary["titles"]

		self.task_dictionary["language_type"] = self.task_dictionary["type"]

		i = 0
		for task_type in self.task_types["en"]:
			if task_type == self.task_dictionary["language_type"] and self.task_types[self.user_language][i] != self.task_dictionary["type"]:
				self.task_dictionary["language_type"] = self.task_types[self.user_language][i]

			i += 1

		self.Register_Task_In_JSON()
		self.Create_Task_File()

		self.Check_First_Task_In_Year()

		# Write on Diary Slim
		Write_On_Diary_Slim_Module(self.task_dictionary["descriptions"][self.user_language], self.task_dictionary["Times"]["Language DateTime"][self.user_language], show_text = False)

		self.Show_Task_Information()

		if self.task_dictionary["large_bar"] == True:
			print()
			print(self.large_bar)

		if self.task_dictionary["input"] == True:
			self.Input.Type(self.Language.language_texts["press_enter_when_you_finish_reading_the_info_summary"])

	def Select_Task_Type(self):
		options = self.task_types["en"]
		language_options = self.task_types[self.user_language]

		show_text = self.language_texts["task_types"]
		select_text = self.language_texts["select_a_task_type"]

		option_info = self.Input.Select(options, language_options = language_options, show_text = show_text, select_text = select_text)

		self.task_dictionary = {
			"titles": {},
			"descriptions": {},
			"type": option_info["option"],
			"time": self.Date.Now(),
			"large_bar": True,
			"input": True,
		}

	def Type_Task_Information(self):
		for language in self.small_languages:
			translated_language = self.translated_languages[language][self.user_language]

			type_text = self.language_texts["describe_the_task_in"] + " " + translated_language

			self.task_dictionary["descriptions"][language] = self.Input.Lines(type_text)["string"]

			self.task_dictionary["titles"][language] = self.task_types["task_texts, type: dict"][language][self.task_dictionary["type"]] + "."

	def Register_Task_In_JSON(self):
		self.task_dictionary["Times"] = {
			"ISO8601": self.task_dictionary["time"]["%Y-%m-%d %H:%M:%S"],
			"Language DateTime": {}
		}

		for language in self.small_languages:
			self.task_dictionary["Times"]["Language DateTime"][language] = self.task_dictionary["time"]["date_time_format"][language]

		self.task_type = self.task_dictionary["type"]

		# Add to number
		self.tasks["Number"] += 1

		# Add to types list
		self.tasks["Types"].append(self.task_type)

		# Add to titles list
		for language in self.small_languages:
			self.tasks["Titles"][language].append(self.task_dictionary["titles"][language])

		# Add to times dictionary
		self.tasks["Times"]["ISO8601"].append(self.task_dictionary["Times"]["ISO8601"])

		for language in self.small_languages:
			self.tasks["Times"]["Language DateTime"][language].append(self.task_dictionary["Times"]["Language DateTime"][language])

		# Define [Number. Task Type (Time)] and sanitized version for files
		self.task_dictionary["Number. Task Type (Time)"] = str(self.tasks["Number"]) + ". " + self.task_type + " (" + self.task_dictionary["Times"]["Language DateTime"][self.user_language] + ")"
		self.task_dictionary["Number. Task Type (Time) Sanitized"] = self.task_dictionary["Number. Task Type (Time)"].replace(":", ";").replace("/", "-")

		# Define [Number. Task Type (Time)] sanitized for files per language
		self.task_dictionary["Number. Task Type (Time) Sanitized Languages"] = {}

		for language in self.small_languages:
			self.task_dictionary["Number. Task Type (Time) Sanitized Languages"][language] = str(self.tasks["Number"]) + ". " + self.task_type + " (" + self.task_dictionary["Times"]["Language DateTime"][language].replace(":", ";").replace("/", "-") + ")"

		# Add to [Number. Task Type (Time)] list
		self.tasks["Number. Task Type (Time)"].append(self.task_dictionary["Number. Task Type (Time)"])

		# Update "Tasks.json" file to add new Tasks JSON dictionary
		self.JSON.Edit(self.folders["task_history"]["current_year"]["tasks"], self.tasks)

		# Add [Number. Task Type (Time)] to "File list.txt" file
		self.File.Edit(self.folders["task_history"]["current_year"]["file_list"], self.task_dictionary["Number. Task Type (Time)"], "a")

		# ----------------------------------------- #

		self.Add_Task_Types_To_Tasks()

		# Add to task type number
		self.tasks[self.task_type]["Number"] += 1

		# Add to titles list and add Language DateTime
		for language in self.small_languages:
			self.tasks[self.task_type]["Titles"][language].append(self.task_dictionary["titles"][language])

			self.tasks[self.task_type]["Times"]["Language DateTime"][language].append(self.task_dictionary["Times"]["Language DateTime"][language])

		self.tasks[self.task_type]["Number. Task Type (Time)"].append(self.task_dictionary["Number. Task Type (Time)"])

		self.tasks[self.task_type]["Times"]["ISO8601"].append(self.task_dictionary["Times"]["ISO8601"])

		# Update task type "Tasks.json" file to add new task type Tasks JSON dictionary
		self.JSON.Edit(self.folders["task_history"]["current_year"]["per_task_type"][self.task_type]["tasks"], self.tasks[self.task_type])

		# Add [Number. Task Type (Time)] to task type "Task list.txt" file
		self.File.Edit(self.folders["task_history"]["current_year"]["per_task_type"][self.task_type]["file_list"], self.task_dictionary["Number. Task Type (Time)"], "a")

	def Create_Task_File(self):
		# Number: [Task number]
		# Task type number: [Task type number]
		# Type: [Task type]
		# Time: [Task times]
		# 
		# File name: [Number. Task Type (Time)]
		# 
		# English title:
		# Portuguese title:
		# 
		# Task descriptions:
		# 
		# English:
		# [English task description]
		# 
		# -
		# 
		# Português:
		# [Portuguese task description]

		# Define task file
		folder = self.folders["task_history"]["current_year"]["per_task_type"][self.task_type]["files"]["root"]
		file = folder + self.task_dictionary["Number. Task Type (Time) Sanitized"] + ".txt"
		self.File.Create(file)

		self.task_dictionary["task_text"] = {}

		# Define task text per language
		for language in self.small_languages:
			full_language = self.full_languages[language]

			self.task_dictionary["task_text"][language] = self.texts["task_text_template"][language]

			# Define items to be added to task text template
			items = [
				self.tasks["Number"],
				self.tasks[self.task_type]["Number"],
				self.task_type,
				self.task_dictionary["Times"]["ISO8601"] + "\n" + self.task_dictionary["Times"]["Language DateTime"][language] + "\n",
				self.task_dictionary["Number. Task Type (Time)"],
			]

			self.task_dictionary["task_text"][language] = self.task_dictionary["task_text"][language].format(*items)

			# Define task title
			self.task_dictionary["task_text"][language] += "\n\n" + self.texts["[language]_title"][language] + ":" + "\n" + self.task_dictionary["titles"][language]

			# Define task description
			self.task_dictionary["task_text"][language] += "\n\n" + self.texts["task_description"][language] + ":" + "\n" + self.task_dictionary["descriptions"][language]

		# Define general task text
		self.task_dictionary["task_text"]["general"] = self.texts["task_text_template"][language]

		# Define items to be added to template
		items = [
			self.tasks["Number"],
			self.tasks[self.task_type]["Number"],
			self.task_type,
			self.task_dictionary["Times"]["ISO8601"],
			self.task_dictionary["Number. Task Type (Time)"],
		]

		for language in self.small_languages:
			# Add to task time
			items[3] += "\n" + self.task_dictionary["Times"]["Language DateTime"][language]

			if language == self.small_languages[-1]:
				items[3] += "\n"

		self.task_dictionary["task_text"]["general"] = self.task_dictionary["task_text"]["general"].format(*items)

		self.task_dictionary["task_text"]["general"] += "\n\n"

		for language in self.small_languages:
			# Define task titles per language
			self.task_dictionary["task_text"]["general"] += self.texts["[language]_title"][language] + ":" + "\n" + self.task_dictionary["titles"][language]

			if language != self.small_languages[-1]:
				self.task_dictionary["task_text"]["general"] += "\n\n"

		self.task_dictionary["task_text"]["general"] += "\n\n" + self.texts["task_descriptions"]["en"] + ":" + "\n\n"

		for language in self.small_languages:
			full_language = self.full_languages[language]

			# Define task descriptions per language
			self.task_dictionary["task_text"]["general"] += full_language + ":" + "\n" + self.task_dictionary["descriptions"][language]

			if language != self.small_languages[-1]:
				self.task_dictionary["task_text"]["general"] += "\n\n"

		# Write task text into task file
		self.File.Edit(file, self.task_dictionary["task_text"]["general"], "w")

	def Check_First_Task_In_Year(self):
		self.firsts_of_the_year_folders = {
			"root": {},
			"sub_folder": {},
			"type": {},
		}

		i = 0
		# Create folders
		for language in self.small_languages:
			full_language = self.full_languages[language]

			# Root folders
			self.firsts_of_the_year_folders["root"][language] = self.notepad_folders["years"]["current_year"]["root"] + full_language + "/" + self.texts["firsts_of_the_year"][language] + "/"
			self.Folder.Create(self.firsts_of_the_year_folders["root"][language])

			# Subfolders
			self.firsts_of_the_year_folders["sub_folder"][language] = self.firsts_of_the_year_folders["root"][language] + self.task_types["sub_folders, type: dict"][self.task_type][language] + "/"
			self.Folder.Create(self.firsts_of_the_year_folders["sub_folder"][language])

			# Task type folder
			self.firsts_of_the_year_folders["type"][language] = self.firsts_of_the_year_folders["sub_folder"][language] + self.task_dictionary["language_type"] + "/"
			self.Folder.Create(self.firsts_of_the_year_folders["type"][language])

			i += 1

		self.task_dictionary["first_task_in_year"] = False

		if self.tasks["Number"] == 1:
			self.task_dictionary["first_task_in_year"] = True

		if self.task_dictionary["first_task_in_year"] == True:
			for language in self.small_languages:
				folder = self.firsts_of_the_year_folders["type"][language]

				self.task_dictionary["first_task_in_year_file"] = folder + self.task_dictionary["Number. Task Type (Time) Sanitized Languages"][language] + ".txt"
				self.File.Create(self.task_dictionary["first_task_in_year_file"])

				self.File.Edit(self.task_dictionary["first_task_in_year_file"], self.task_dictionary["task_text"][language], "w")

	def Show_Task_Information(self):
		print()
		print(self.large_bar)
		print()

		print(self.language_texts["this_task_was_registered"] + ":")

		for language in self.small_languages:
			translated_language = self.translated_languages[language][self.user_language]

			print("\t" + translated_language + ":")
			print("\t" + self.task_dictionary["titles"][language])
			print()

		print(self.language_texts["type, title()"] + ":")

		text = self.task_dictionary["type"]

		if self.task_dictionary["language_type"] != self.task_dictionary["type"]:
			text = "\t" + self.task_dictionary["type"]

		print(text)

		if self.task_dictionary["language_type"] != self.task_dictionary["type"]:
			print("\t" + self.task_dictionary["language_type"])

		print()

		print(self.language_texts["when, title()"] + ":")
		print(self.task_dictionary["Times"]["Language DateTime"][self.user_language])

		show_task_description = self.Input.Yes_Or_No(self.language_texts["show_task_description"] + "?" + " (" + self.language_texts["can_be_long"] + ")")

		if show_task_description == True:
			print()
			print(self.language_texts["task_description_in"] + " " + self.full_user_language + ":")
			print("[" + self.task_dictionary["descriptions"][self.user_language] + "]")