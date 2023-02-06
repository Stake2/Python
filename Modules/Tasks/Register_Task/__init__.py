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

		self.task_type = self.task_dictionary["types"]["en"]

		# Define "register" dictionary (key) inside task dictionary
		self.task_dictionary.update({
			"register": {
				"states": {
					"first_task_in_year": False,
					"first_task_type_task_in_year": False
				}
			}
		})

		self.Register_In_JSON()
		self.Create_File()

		self.Add_File_To_Year_Folder()

		# Write on Diary Slim
		Write_On_Diary_Slim_Module(self.task_dictionary["descriptions"][self.user_language], self.task_dictionary["register"]["Times"]["Language DateTime"][self.user_language], show_text = False)

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
			"types": {},
			"time": self.Date.Now(),
			"large_bar": True,
			"input": True,
		}

		i = 0
		for task_type in self.task_types["en"]:
			if self.task_dictionary["type"] == self.task_types["en"][i]:
				for language in self.languages["small"]:
					self.task_dictionary["types"][language] = self.task_types[language][i]

			i += 1

	def Type_Task_Information(self):
		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language][self.user_language]

			type_text = self.language_texts["describe_the_task_in"] + " " + translated_language

			self.task_dictionary["descriptions"][language] = self.Input.Lines(type_text)["string"]

			self.task_dictionary["titles"][language] = self.task_types["task_texts, type: dict"][language][self.task_dictionary["type"]] + "."

	def Register_In_JSON(self):
		# Add to task and task type task number
		self.tasks["Number"] += 1
		self.task_type_tasks[self.task_type]["Number"] += 1

		if self.tasks["Number"] == 1:
			self.task_dictionary["register"]["states"]["first_task_in_year"] = True

		if self.task_type_tasks[self.task_type]["Number"] == 1:
			self.task_dictionary["register"]["states"]["first_task_type_task_in_year"] = True

		# Add to titles list
		for language in self.languages["small"]:
			self.tasks["Lists"]["Titles"][language].append(self.task_dictionary["titles"][language])
			self.task_type_tasks[self.task_type]["Lists"]["Titles"][language].append(self.task_dictionary["titles"][language])

		# Add to types list
		self.tasks["Lists"]["Types"].append(self.task_type)

		# Define task times
		self.task_dictionary["register"]["Times"] = {
			"ISO8601": self.task_dictionary["time"]["%Y-%m-%d %H:%M:%S"],
			"Language DateTime": {}
		}

		for language in self.languages["small"]:
			self.task_dictionary["register"]["Times"]["Language DateTime"][language] = self.task_dictionary["time"]["date_time_format"][language]

		# Add to taskss and task type times
		self.tasks["Lists"]["Times"]["ISO8601"].append(self.task_dictionary["register"]["Times"]["ISO8601"])
		self.task_type_tasks[self.task_type]["Lists"]["Times"]["ISO8601"].append(self.task_dictionary["register"]["Times"]["ISO8601"])

		for language in self.languages["small"]:
			self.tasks["Lists"]["Times"]["Language DateTime"][language].append(self.task_dictionary["register"]["Times"]["Language DateTime"][language])
			self.task_type_tasks[self.task_type]["Lists"]["Times"]["Language DateTime"][language].append(self.task_dictionary["register"]["Times"]["Language DateTime"][language])

		# Define [Number. Task Type (Time)] and sanitized version for files
		self.task_dictionary["register"]["Number. Task Type (Time)"] = {
			"normal": str(self.tasks["Number"]) + ". " + self.task_type + " (" + self.task_dictionary["register"]["Times"]["Language DateTime"][self.user_language] + ")",
			"sanitized": {}
		}

		# Define [Number. Task Type (Time)] sanitized for files per language
		for language in self.languages["small"]:
			self.task_dictionary["register"]["Number. Task Type (Time)"]["sanitized"][language] = str(self.tasks["Number"]) + ". " + self.task_type + " (" + self.task_dictionary["register"]["Times"]["Language DateTime"][language].replace(":", ";").replace("/", "-") + ")"

		# Add to [Number. Task Type (Time)] list
		self.tasks["Number. Task Type (Time)"].append(self.task_dictionary["register"]["Number. Task Type (Time)"]["normal"])
		self.task_type_tasks[self.task_type]["Number. Task Type (Time)"].append(self.task_dictionary["register"]["Number. Task Type (Time)"]["normal"])

		key = self.task_dictionary["register"]["Number. Task Type (Time)"]["normal"]

		self.tasks["Dictionary"][key] = {
			"Number": self.tasks["Number"],
			"Task type number": self.task_type_tasks[self.task_type]["Number"],
			"File name": self.task_dictionary["register"]["Number. Task Type (Time)"]["normal"],
			"Titles": self.task_dictionary["titles"],
			"Type": self.task_type,
			"Times": self.task_dictionary["register"]["Times"]
		}

		dict_ = self.Define_States_Dictionary(self.task_dictionary)

		key = self.task_dictionary["register"]["Number. Task Type (Time)"]["normal"]

		if dict_ != {}:
			self.tasks["Dictionary"][key]["States"] = dict_

		# Add task dictionary to task type tasks dictionary
		self.task_type_tasks[self.task_type]["Dictionary"][key] = self.tasks["Dictionary"][key].copy()

		# Update "Tasks.json" file
		self.JSON.Edit(self.folders["task_history"]["current_year"]["tasks"], self.tasks)

		key = self.task_type.lower().replace(" ", "_")

		# Update task type "Tasks.json" file
		self.JSON.Edit(self.folders["task_history"]["current_year"]["per_task_type"][key]["tasks"], self.task_type_tasks[self.task_type])

		# Add to root and task type "File list.txt" file
		self.File.Edit(self.folders["task_history"]["current_year"]["file_list"], self.task_dictionary["register"]["Number. Task Type (Time)"]["normal"], "a")
		self.File.Edit(self.folders["task_history"]["current_year"]["per_task_type"][key]["file_list"], self.task_dictionary["register"]["Number. Task Type (Time)"]["normal"], "a")

	def Create_File(self):
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
		# File name: [Number. Task Type (Time)]
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

		key = self.task_type.lower().replace(" ", "_")

		# Define task file
		folder = self.folders["task_history"]["current_year"]["per_task_type"][key]["files"]["root"]
		file = folder + self.task_dictionary["register"]["Number. Task Type (Time)"]["sanitized"][self.user_language] + ".txt"
		self.File.Create(file)

		self.task_dictionary["register"]["file_text"] = {}

		self.task_dictionary["register"]["file_text"]["general"] = self.Define_File_Text("general")

		for language in self.languages["small"]:
			self.task_dictionary["register"]["file_text"][language] = self.Define_File_Text(language)

		# Write task text into task file
		self.File.Edit(file, self.task_dictionary["register"]["file_text"]["general"], "w")

	# Define task text per language
	def Define_File_Text(self, language_parameter = None):
		if language_parameter != "general":
			language = language_parameter

		if language_parameter == "general":
			language = "en"

		full_language = self.languages["full"][language]

		# Define task text lines
		lines = [
			self.texts["number, title()"][language] + ": " + str(self.tasks["Number"]),
			self.texts["task_type_number"][language] + ": " + str(self.task_type_tasks[self.task_type]["Number"])
		]

		# Add task title lines
		if language_parameter != "general":
			text = self.Language.texts["title, title()"][language]

		if language_parameter == "general":
			text = self.Language.texts["titles, title()"][language]

		lines.append("\n" + text + ":" + "\n" + "{}")

		lines.extend([
			self.Language.texts["type, title()"][language] + ": " + self.task_type + "\n",
			self.Date.texts["times, title()"][language] + ":" + "\n" + "{}",
			self.File.texts["file_name"][language] + ": " + self.task_dictionary["register"]["Number. Task Type (Time)"]["normal"]
		])

		# Add states texts lines
		if "States" in self.tasks["Dictionary"][self.task_dictionary["register"]["Number. Task Type (Time)"]["normal"]]:
			dict_ = self.tasks["Dictionary"][self.task_dictionary["register"]["Number. Task Type (Time)"]["normal"]]["States"]

			text = "\n" + self.Language.texts["states, title()"][language] + ":" + "\n"

			for key in dict_:
				key = key.lower()

				text_key = key

				if key != "first_task_type_task_in_year":
					language_text = self.texts[text_key][language]

				if key == "first_task_type_task_in_year":
					task_type = self.task_types["items, type: dict"][language][self.task_type]

					if self.task_type in ["Python", "PHP"]:
						task_type = self.texts["{}_task"][language].format(self.task_types["items, type: dict"][language][self.task_type])

					language_text = self.texts["first_{}_in_year"][language].format(task_type)

				text += language_text

				if key != list(dict_.keys())[-1].lower():
					text += "\n"

			lines.append(text)

		# Add task description lines
		if language_parameter != "general":
			text = self.texts["task_description"][language]
			line_break = "\n"

		if language_parameter == "general":
			text = self.texts["task_descriptions"][language]
			line_break = "\n\n"

		lines.append("\n" + text + ":" + line_break + "{}")

		# Define items to be added to task text format
		items = []

		# Add task titles to items list
		titles = ""

		if language_parameter != "general":
			titles = self.task_dictionary["titles"][language] + "\n"

		if language_parameter == "general":
			for language in self.languages["small"]:
				titles += self.task_dictionary["titles"][language] + "\n"

		items.append(titles)

		# Add times to items list
		times = ""

		for key in ["ISO8601", "Language DateTime"]:
			time = self.task_dictionary["register"]["Times"][key]

			if key == "ISO8601":
				times += time + "\n"

			if key == "Language DateTime":
				if language_parameter != "general":
					times += time[language] + "\n"

				if language_parameter == "general":
					for language in self.languages["small"]:
						times += time[language] + "\n"

		items.append(times)

		# Add task descriptions to items list
		descriptions = ""

		if language_parameter != "general":
			descriptions = self.task_dictionary["descriptions"][language]

		if language_parameter == "general":
			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				descriptions += full_language + ":" + "\n" + self.task_dictionary["descriptions"][language]

				if language != self.languages["small"][-1]:
					descriptions += "\n\n"

		items.append(descriptions)

		# Define language task text
		file_text = self.Text.From_List(lines)

		return file_text.format(*items)

	def Add_File_To_Year_Folder(self):
		# Create folders
		for language in self.languages["small"]:
			full_language = self.languages["full"][language]

			# Folder names
			root_folder = self.texts["done_tasks"][language]
			type_folder = self.task_dictionary["types"][language]

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
			file_name = self.task_dictionary["register"]["Number. Task Type (Time)"]["sanitized"][language]
			self.current_year["folders"][full_language][root_folder][type_folder][file_name] = folder + file_name + ".txt"

			self.File.Create(self.current_year["folders"][full_language][root_folder][type_folder][file_name])

			self.File.Edit(self.current_year["folders"][full_language][root_folder][type_folder][file_name], self.task_dictionary["register"]["file_text"][language], "w")

			# Firsts Of The Year subfolder folder
			firsts_of_the_year_text = self.Language.texts["firsts_of_the_year"][language]
			subfolder_name = self.task_types["sub_folders, type: dict"][self.task_type][language]

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
			if self.task_dictionary["register"]["states"]["first_task_in_year"] == True:
				folder = self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder]["root"]

				self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name] = folder + file_name + ".txt"
				self.File.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name])

				self.File.Edit(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name], self.task_dictionary["register"]["file_text"][language], "w")

	def Show_Task_Information(self):
		print()
		print(self.large_bar)
		print()

		print(self.language_texts["this_task_was_registered"] + ":")

		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language][self.user_language]

			print("\t" + translated_language + ":")
			print("\t" + self.task_dictionary["titles"][language])
			print()

		print(self.language_texts["type, title()"] + ":")

		text = self.task_dictionary["types"]["en"]

		if self.task_dictionary["types"][self.user_language] != self.task_dictionary["types"]["en"]:
			text = "\t" + text

		print(text)

		if self.task_dictionary["types"][self.user_language] != self.task_dictionary["types"]["en"]:
			print("\t" + self.task_dictionary["types"][self.user_language])

		print()

		print(self.language_texts["when, title()"] + ":")
		print(self.task_dictionary["register"]["Times"]["Language DateTime"][self.user_language])

		show_task_description = self.Input.Yes_Or_No(self.language_texts["show_task_description"] + "?" + " (" + self.language_texts["can_be_long"] + ")")

		if show_task_description == True:
			print()
			print(self.language_texts["task_description_in"] + " " + self.full_user_language + ":")
			print("[" + self.task_dictionary["descriptions"][self.user_language] + "]")