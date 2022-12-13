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
				self.task_dictionary["descriptions"] = self.task_dictionary["names"]

		self.Add_To_Task_Numbers()
		self.Make_Task_Header()

		self.Add_Task_To_Text_Files()
		self.Create_Task_Text_Files()

		self.Check_First_Task_In_Year()

		self.diary_slim_text = Write_On_Diary_Slim_Module(self.task_dictionary["descriptions"][self.user_language], self.task_dictionary["time"], show_text = False)

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
			"names": {},
			"descriptions": {},
			"type": option_info["option"],
			"time": self.Date.Now()["%H:%M %d/%m/%Y"],
			"large_bar": True,
			"input": True,
		}

	def Type_Task_Information(self):
		for language in self.small_languages:
			translated_language = self.translated_languages[language][self.user_language]

			type_text = self.language_texts["describe_the_task_in"] + " " + translated_language

			self.task_dictionary["descriptions"][language] = self.Input.Lines(type_text)["string"]

			self.task_dictionary["names"][language] = self.task_types["task_texts, type: dict"][language][self.task_dictionary["type"]] + "."

	def Add_To_Task_Numbers(self):
		self.task_type_number_file = self.folders["Task History"][str(self.date["year"])]["Per Task Type"]["Files"][self.task_dictionary["type"]]["Number"]

		# Current Year Task History folder >
			# Per Task Type >
				# Files (Writes) > 
					# [Task Type] >
						# Number.txt

			# Writes:
				# Number.txt

		# Number.txt
		file = self.folders["Task History"][str(self.date["year"])]["Number"]
		self.task_dictionary["number"] = str(int(self.File.Contents(file)["lines"][0]) + 1)

		self.File.Edit(file, self.task_dictionary["number"], "w")

		# Files (Writes) > [Task Type] > Number.txt
		file = self.folders["Task History"][str(self.date["year"])]["Per Task Type"]["Files"][self.task_dictionary["type"]]["Number"]
		self.task_dictionary["task_type_number"] = str(int(self.File.Contents(file)["lines"][0]) + 1)

		self.File.Edit(file, self.task_dictionary["task_type_number"], "w")

	def Make_Task_Header(self):
		i = 0
		for task_type in self.task_types["en"]:
			if task_type == self.task_dictionary["type"]:
				self.task_dictionary["language_type"] = self.task_types[self.user_language][i]

			i += 1

		self.task_dictionary["header"] = self.task_dictionary["number"] + ", " + self.task_dictionary["task_type_number"] + "\n"
		self.task_dictionary["header"] += "\n"
		self.task_dictionary["header"] += self.task_dictionary["type"] + "\n"

		if self.task_dictionary["language_type"] != self.task_dictionary["type"]:
			self.task_dictionary["header"] += self.task_dictionary["language_type"] + "\n"

		self.task_dictionary["header"] += "\n"

		for language in self.small_languages:
			self.task_dictionary["header"] += self.task_dictionary["descriptions"][language]

			if language != self.small_languages[-1]:
				self.task_dictionary["header"] += "\n\n-\n\n"

		self.task_dictionary["time_replaced"] = self.task_dictionary["time"].replace(":", ";").replace("/", "-")

		self.task_dictionary["number_type_and_time"] = self.task_dictionary["number"] + ". " + self.task_dictionary["type"] + " " + self.task_dictionary["time"]

	def Add_Task_To_Text_Files(self):
		# Current Year Task History folder >
			# Appends:
				# Tasks.txt
				# Tasks.json
				# Task Types.txt
				# Times.txt

		folder = self.folders["Task History"][str(self.date["year"])]

		# Tasks.txt
		file = folder["Tasks"]
		text = self.task_dictionary["names"]["en"].replace(".", "")

		self.File.Edit(file, text, "a")

		# Tasks.json
		file = folder["Tasks.json"]
		text = self.Language.JSON_To_Python(file)

		for language in self.small_languages:
			text[language].append(self.task_dictionary["names"][language].replace(".", ""))

		text = self.Language.Python_To_JSON(text)

		self.File.Edit(file, text, "a")

		# Task Types.txt
		file = folder["Task Types"]
		text = self.task_dictionary["type"]

		self.File.Edit(file, text, "a")

		# Times.txt
		file = folder["Times"]
		text = self.task_dictionary["time"]

		self.File.Edit(file, text, "a")

		# ------------------ #

		# Current Year Task History folder >
			# Per Task Type >
				# Files (Appends) > 
					# [Task Type] >
						# Tasks.txt, Tasks.json, Times.txt

		folder = self.folders["Task History"][str(self.date["year"])]["Per Task Type"]["Files"][self.task_dictionary["type"]]

		# Files (Appends) > [Task Type] > Tasks.txt
		file = folder["Tasks"]
		text = self.task_dictionary["names"]["en"].replace(".", "")

		self.File.Edit(file, text, "a")

		# Files (Appends) > [Task Type] > Tasks.json
		file = folder["Tasks.json"]
		text = self.Language.JSON_To_Python(file)

		for language in self.small_languages:
			text[language].append(self.task_dictionary["names"][language].replace(".", ""))

		text = self.Language.Python_To_JSON(text)

		self.File.Edit(file, text, "a")

		# Files (Appends) > [Task Type] > Times.txt
		file = folder["Times"]
		text = self.task_dictionary["time"]

		self.File.Edit(file, text, "a")

	def Create_Task_Text_Files(self):
		# Current Year Task History folder >
			# All Task Files (Creates) >
				# [Task number]. [Task type] [Task time].txt
					# Contents:
					# [All Tasks number], [Task type number]
					# 
					# [Task type]
					# ([Mixed task type])
					# 
					# [Task time]
					# 
					# [Language task descriptions]

		# [Task number]. [Task type] [Task time].txt
		self.task_dictionary["file"] = self.folders["Task History"][str(self.date["year"])]["All Task Files"] + self.task_dictionary["number_type_and_time"] + ".txt"
		self.File.Create(self.task_dictionary["file"])

		text = self.task_dictionary["header"]
		self.File.Edit(self.task_dictionary["file"], text, "w")

		# ------------------ #

		# Current Year Task History folder >
			# Per Task Type >
				# Folders >
					# [Task Type] (Creates) >
						# [Task time].txt
							# Contents:
							# [All Tasks number], [Task type number]
							# 
							# [Task type]
							# ([Mixed task type])
							# 
							# [Task time]
							# 
							# [Language task descriptions]

		folder = self.folders["Task History"][str(self.date["year"])]["Per Task Type"]["Folders"][self.task_dictionary["type"]]["root"]

		self.task_dictionary["task_type_file"] = folder + self.task_dictionary["time_replaced"] + ".txt"
		self.File.Create(self.task_dictionary["task_type_file"])

		text = self.task_dictionary["header"]
		self.File.Edit(self.task_dictionary["task_type_file"], text, "w")

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
			self.firsts_of_the_year_folders["root"][language] = self.notepad_folders["years"]["current"]["root"] + full_language + "/" + self.texts["firsts_of_the_year"][language] + "/"
			self.Folder.Create(self.firsts_of_the_year_folders["root"][language])

			# Subfolders
			self.firsts_of_the_year_folders["sub_folder"][language] = self.firsts_of_the_year_folders["root"][language] + self.task_types["sub_folders, type: dict"][self.task_dictionary["type"]] + "/"
			self.Folder.Create(self.firsts_of_the_year_folders["sub_folder"][language])

			# Task type folders
			self.firsts_of_the_year_folders["type"][language] = self.firsts_of_the_year_folders["sub_folder"][language] + self.task_types["type_folders, type: dict"][self.task_dictionary["type"]] + "/"
			self.Folder.Create(self.firsts_of_the_year_folders["type"][language])

			i += 1

		self.task_dictionary["first_task_in_year"] = False

		file = self.folders["Task History"][str(self.date["year"])]["Per Task Type"]["Files"][self.task_dictionary["type"]]["Tasks"]

		if self.File.Contents(file)["length"] == 0:
			self.task_dictionary["first_task_in_year"] = True

		if self.task_dictionary["first_task_in_year"] == True:
			for language in self.small_languages:
				folder = self.firsts_of_the_year_folders["sub_folder"][language]

				self.task_dictionary["first_task_in_year_file"] = folder + self.task_dictionary["number_type_and_time"] + ".txt"
				self.File.Create(self.task_dictionary["first_task_in_year_file"])

				self.File.Edit(self.task_dictionary["first_task_in_year_file"], self.task_dictionary["header"], "w")

	def Show_Task_Information(self):
		print()
		print(self.large_bar)
		print()

		print(self.language_texts["this_task_was_registered"] + ":")

		for language in self.small_languages:
			translated_language = self.translated_languages[language][self.user_language]

			print("\t" + translated_language + ":")
			print("\t" + self.task_dictionary["names"][language])
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
		print(self.task_dictionary["time"])

		show_task_description = self.Input.Yes_Or_No(self.language_texts["show_task_description"] + "?" + " (" + self.language_texts["can_be_long"] + ")")

		if show_task_description == True:
			print()
			print(self.language_texts["task_description_in"] + " " + self.full_user_language + ":")
			print("[" + self.task_dictionary["descriptions"][self.user_language] + "]")