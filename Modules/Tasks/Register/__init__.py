# Register.py

from Tasks.Tasks import Tasks as Tasks

from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

class Register(Tasks):
	def __init__(self, task = {}, show_text = True):
		super().__init__()

		self.dictionaries["Task"] = task

		if self.dictionaries["Task"] == {}:
			self.Select_Task_Type()
			self.Type_Task_Information()

		if self.dictionaries["Task"] != {}:
			self.dictionaries["Task"]["large_bar"] = False
			self.dictionaries["Task"]["input"] = False

			if "Descriptions" not in self.dictionaries["Task"]:
				self.dictionaries["Task"]["Descriptions"] = self.dictionaries["Task"]["Titles"]

		self.dictionaries["Task"].update({
			"Times": {
				"UTC": self.Date.To_String(self.dictionaries["Task"]["Time"]["utc"]),
				"Timezone": self.dictionaries["Task"]["Time"]["hh:mm DD/MM/YYYY"]
			},
			"States": {
				"First Task In Year": False,
				"First Task Type Task In Year": False
			}
		})

		# Database related methods
		self.Register_In_JSON()
		self.Create_Entry_File()
		self.Add_Entry_File_To_Year_Folder()

		# Write on Diary Slim
		Write_On_Diary_Slim_Module(self.dictionaries["Task"]["Descriptions"][self.user_language], self.dictionaries["Task"]["Times"]["Timezone"], show_text = False)

		self.Show_Information()

		if self.dictionaries["Task"]["large_bar"] == True:
			print()
			print(self.large_bar)

		if self.dictionaries["Task"]["input"] == True:
			self.Input.Type(self.JSON.Language.language_texts["press_enter_when_you_finish_reading_the_info_summary"])

	def Select_Task_Type(self):
		options = self.task_types["plural"]["en"]
		language_options = self.task_types["plural"][self.user_language]

		show_text = self.language_texts["task_types"]
		select_text = self.language_texts["select_a_task_type"]

		dictionary = self.Input.Select(options, language_options = language_options, show_text = show_text, select_text = select_text)

		self.dictionaries["Task"] = {
			"Name": {},
			"Titles": {},
			"Descriptions": {},
			"Type": self.task_types[dictionary["option"]],
			"Time": self.Date.Now(),
			"large_bar": True,
			"input": True
		}

	def Type_Task_Information(self):
		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language][self.user_language]

			type_text = self.language_texts["describe_the_task_in"] + " " + translated_language

			self.dictionaries["Task"]["Titles"][language] = self.task_types["task_texts, type: dict"][language][self.dictionaries["Task"]["Type"]["plural"]["en"]] + "."

			self.dictionaries["Task"]["Descriptions"][language] = self.dictionaries["Task"]["Titles"][language] + "\n\n"

			self.dictionaries["Task"]["Descriptions"][language] += self.Input.Lines(type_text)["string"]
			print(self.dictionaries["Task"]["Descriptions"][language])

	def Register_In_JSON(self):
		self.task_type = self.dictionaries["Task"]["Type"]["plural"]["en"]

		# Add to task and task type task number
		self.dictionaries["Tasks"]["Numbers"]["Total"] += 1
		self.dictionaries["Task Type"][self.task_type]["Numbers"]["Total"] += 1

		if self.dictionaries["Tasks"]["Numbers"]["Total"] == 1:
			self.dictionaries["Task"]["States"]["First Task In Year"] = True

		if self.dictionaries["Task Type"][self.task_type]["Numbers"]["Total"] == 1:
			self.dictionaries["Task"]["States"]["First Task Type Task In Year"] = True

		# Define sanitized version of entry name for files
		self.dictionaries["Task"]["Name"] = {
			"Normal": str(self.dictionaries["Tasks"]["Numbers"]["Total"]) + ". " + self.task_type + " (" + self.dictionaries["Task"]["Times"]["Timezone"] + ")",
			"Sanitized": ""
		}

		self.dictionaries["Task"]["Name"]["Sanitized"] = self.dictionaries["Task"]["Name"]["Normal"].replace(":", ";").replace("/", "-")

		# Add to [Entries] list
		self.dictionaries["Tasks"]["Entries"].append(self.dictionaries["Task"]["Name"]["Normal"])
		self.dictionaries["Task Type"][self.task_type]["Entries"].append(self.dictionaries["Task"]["Name"]["Normal"])

		self.key = self.dictionaries["Task"]["Name"]["Normal"]

		self.dictionaries["Tasks"]["Dictionary"][self.key] = {
			"Number": self.dictionaries["Tasks"]["Numbers"]["Total"],
			"Type number": self.dictionaries["Task Type"][self.task_type]["Numbers"]["Total"],
			"Entry": self.dictionaries["Task"]["Name"]["Normal"],
			"Titles": self.dictionaries["Task"]["Titles"],
			"Type": self.task_type,
			"Time": self.dictionaries["Task"]["Times"]["UTC"]
		}

		# Get States dictionary
		dict_ = self.Define_States_Dictionary(self.dictionaries["Task"])

		if dict_ != {}:
			self.dictionaries["Tasks"]["Dictionary"][self.key]["States"] = dict_

		# Add task dictionary to task type tasks dictionary
		self.dictionaries["Task Type"][self.task_type]["Dictionary"][self.key] = self.dictionaries["Tasks"]["Dictionary"][self.key].copy()

		# Update "Tasks.json" file
		self.JSON.Edit(self.folders["task_history"]["current_year"]["tasks"], self.dictionaries["Tasks"])

		# Update task type "Tasks.json" file
		self.JSON.Edit(self.dictionaries["Task"]["Type"]["folders"]["per_task_type"]["tasks"], self.dictionaries["Task Type"][self.task_type])

		# Add to root and task type "Entry list.txt" file
		self.File.Edit(self.folders["task_history"]["current_year"]["entry_list"], self.dictionaries["Task"]["Name"]["Normal"], "a")
		self.File.Edit(self.dictionaries["Task"]["Type"]["folders"]["per_task_type"]["entry_list"], self.dictionaries["Task"]["Name"]["Normal"], "a")

	def Create_Entry_File(self):
		# Number: [Task number]
		# Task type number: [Task type number]
		# 
		# Titles:
		# [English title]
		# [Portuguese title]
		# 
		# Type: [Task type]
		# 
		# Times:
		# [Task times]
		# 
		# File name: [Entries]
		# (
		# States:
		# [Task states]
		# )
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
		folder = self.folders["task_history"]["current_year"]["per_task_type"][self.task_type.lower()]["files"]["root"]
		file = folder + self.dictionaries["Task"]["Name"]["Sanitized"] + ".txt"
		self.File.Create(file)

		self.dictionaries["Task"]["Text"] = {
			"General": self.Define_File_Text("General")
		}

		for language in self.languages["small"]:
			self.dictionaries["Task"]["Text"][language] = self.Define_File_Text(language)

		# Write task text into task file
		self.File.Edit(file, self.dictionaries["Task"]["Text"]["General"], "w")

	# Define task text per language
	def Define_File_Text(self, language_parameter = None):
		if language_parameter != "General":
			language = language_parameter

		if language_parameter == "General":
			language = "en"

		full_language = self.languages["full"][language]

		# Define task text lines
		lines = [
			self.texts["number, title()"][language] + ": " + str(self.dictionaries["Tasks"]["Numbers"]["Total"]),
			self.texts["task_type_number"][language] + ": " + str(self.dictionaries["Task Type"][self.task_type]["Numbers"]["Total"])
		]

		# Add task title lines
		if language_parameter != "General":
			text = self.JSON.Language.texts["title, title()"][language]

		if language_parameter == "General":
			text = self.JSON.Language.texts["titles, title()"][language]

		lines.append("\n" + text + ":" + "\n" + "{}")

		lines.extend([
			self.JSON.Language.texts["type, title()"][language] + ": " + self.task_type + "\n",
			self.Date.texts["times, title()"][language] + ":" + "\n" + "{}",
			self.File.texts["file_name"][language] + ": " + self.dictionaries["Task"]["Name"]["Normal"]
		])

		# Add states texts lines
		if "States" in self.dictionaries["Tasks"]["Dictionary"][self.dictionaries["Task"]["Name"]["Normal"]]:
			dict_ = self.dictionaries["Tasks"]["Dictionary"][self.dictionaries["Task"]["Name"]["Normal"]]["States"]

			text = "\n" + self.JSON.Language.texts["states, title()"][language] + ":" + "\n"

			for key in dict_:
				key = key.lower()

				text_key = key

				if key != "First Task Type Task In Year":
					language_text = self.texts[text_key][language]

				if key == "First Task Type Task In Year":
					task_type = self.task_types["items, type: dict"][language][self.task_type]

					if self.task_type in ["Python", "PHP"]:
						task_type = self.texts["{}_task"][language].format(self.task_types["items, type: dict"][language][self.task_type])

					language_text = self.texts["first_{}_in_year"][language].format(task_type)

				text += language_text

				if key != list(dict_.keys())[-1].lower():
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

		# Define items to be added to task text format
		items = []

		# Add task titles to items list
		titles = ""

		if language_parameter != "General":
			titles = self.dictionaries["Task"]["Titles"][language] + "\n"

		if language_parameter == "General":
			for language in self.languages["small"]:
				titles += self.dictionaries["Task"]["Titles"][language] + "\n"

		items.append(titles)

		# Add times to items list
		times = ""

		for key in ["UTC", "Timezone"]:
			time = self.dictionaries["Task"]["Times"][key]

			times += time + "\n"

		items.append(times)

		# Add task descriptions to items list
		descriptions = ""

		if language_parameter != "General":
			descriptions = self.dictionaries["Task"]["Descriptions"][language]

		if language_parameter == "General":
			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				descriptions += full_language + ":" + "\n" + self.dictionaries["Task"]["Descriptions"][language]

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
			type_folder = self.dictionaries["Task"]["Type"]["plural"][language]

			# Done tasks folder
			folder = self.current_year["folders"][full_language]["root"]

			self.current_year["folders"][full_language][root_folder] = {
				"root": folder + root_folder + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][root_folder]["root"])

			# Task type folder
			folder = self.current_year["folders"][full_language][root_folder]["root"]

			self.current_year["folders"][full_language][root_folder][type_folder] = {
				"root": folder + type_folder + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][root_folder][type_folder]["root"])

			# Done tasks file
			folder = self.current_year["folders"][full_language][root_folder][type_folder]["root"]
			file_name = self.dictionaries["Task"]["Name"]["Sanitized"]
			self.current_year["folders"][full_language][root_folder][type_folder][file_name] = folder + file_name + ".txt"

			self.File.Create(self.current_year["folders"][full_language][root_folder][type_folder][file_name])

			self.File.Edit(self.current_year["folders"][full_language][root_folder][type_folder][file_name], self.dictionaries["Task"]["Text"][language], "w")

			# Firsts Of The Year subfolder folder
			firsts_of_the_year_text = self.JSON.Language.texts["firsts_of_the_year"][language]
			type_folder = self.task_types["items, type: dict"][language][self.task_type]
			subfolder_name = self.dictionaries["Task"]["Type"]["subfolders"][language]

			folder = self.current_year["folders"][full_language][firsts_of_the_year_text]["root"]

			self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name] = {
				"root": folder + subfolder_name + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name]["root"])

			# Firsts Of The Year media type folder
			type_folder = self.task_types["type_folders, type: dict"][self.task_type]

			folder = self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name]["root"]
			
			self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder] = {
				"root": folder + type_folder + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder]["root"])

			# First task type task in year file
			if self.dictionaries["Task"]["States"]["First Task In Year"] == True:
				folder = self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder]["root"]

				self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name] = folder + file_name + ".txt"
				self.File.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name])

				self.File.Edit(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name], self.dictionaries["Task"]["Text"][language], "w")

	def Show_Information(self):
		print()
		print(self.large_bar)
		print()

		print(self.language_texts["this_task_was_registered"] + ":")

		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language][self.user_language]

			print("\t" + translated_language + ":")
			print("\t" + self.dictionaries["Task"]["Titles"][language])
			print()

		print(self.JSON.Language.language_texts["type, title()"] + ":")

		text = self.dictionaries["Task"]["Type"]["plural"]["en"]

		if self.dictionaries["Task"]["Type"]["plural"][self.user_language] != self.dictionaries["Task"]["Type"]["plural"]["en"]:
			text = "\t" + text + "\n"
			text += "\t" + self.dictionaries["Task"]["Types"][self.user_language]

		print(text)
		print()

		print(self.JSON.Language.language_texts["when, title()"] + ":")
		print(self.dictionaries["Task"]["Times"]["Timezone"])

		show_task_description = self.Input.Yes_Or_No(self.language_texts["show_task_description"] + "?" + " (" + self.language_texts["can_be_long"] + ")")

		if show_task_description == True:
			print()
			print(self.language_texts["task_description_in"] + " " + self.full_user_language + ":")
			print("[" + self.dictionaries["Task"]["Descriptions"][self.user_language] + "]")