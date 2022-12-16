# Write_On_Diary_Slim.py

from Diary_Slim.Diary_Slim import Diary_Slim as Diary_Slim

from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

class Write_On_Diary_Slim(Diary_Slim):
	def __init__(self, option_info = None):
		super().__init__()

		self.option_info = option_info

		self.Define_Slim_Texts()
		self.Select()
		self.Define_Text_Variables()
		self.Write()

		print()
		print(self.large_bar)

	def Define_Slim_Texts(self):
		self.date = self.Date.Now()

		# Get slim texts
		self.slim_texts = self.Language.JSON_To_Python(self.slim_texts_file)

		# Get today task done text using weekday
		self.today_task_done_text = self.File.Contents(self.things_done_texts_file)["lines"][self.date["weekday"]]

		for language in self.small_languages:
			# Iterate through state names
			for state in self.states["names"]:
				state = self.states[state]
				state_texts = state["texts"]
				state_name = state["names"][self.user_language]

				order = "first"

				# If the current order text is first order, define the order as "second"
				if state_texts["current"] != [] and state_texts["current"][0] == state_texts["first"][self.user_language]:
					order = "second"

				# Define "first" or "second" order text in language
				text = self.texts[order][language]

				# If the current order text is the second order text, remove the order from slim texts
				if state_texts["current"] != [] and state_texts["current"][0] == state_texts["second"][self.user_language] and state_name in self.slim_texts:
					self.slim_texts[language].pop(state_name)

				# If the current order text is empty, or the current order is not equal to the second order text, add state name to slim texts
				if state_texts["current"] == [] or state_texts["current"] != [] and state_texts["current"][0] != state_texts["second"][self.user_language]:
					self.slim_texts[language][state_name] = state_name + " (" + text + " " + self.language_texts["state"] + ")"

			# Add today done task to slim texts
			if self.today_task_done_text != "":
				if ", " not in self.today_task_done_text:
					self.slim_texts[language]["Today task"] = self.today_task_done_text

				if ", " in self.today_task_done_text:
					self.slim_texts[language]["First today task"] = self.today_task_done_text.split(", ")[0]
					self.slim_texts[language]["Second today task"] = self.today_task_done_text.split(", ")[1]

	def Remove_State_Text(self, text):
		for state in self.states["names"]:
			items_to_remove = [
				" (" + self.language_texts["first"] + " " + self.language_texts["state"] + ")",
				" (" + self.language_texts["second"] + " " + self.language_texts["state"] + ")",
			]

			for item in items_to_remove:
				if item in text:
					text = text.replace(item, "")

		return text

	def Select(self):
		self.text = {}

		if self.option_info == None:
			show_text = self.language_texts["texts_to_write"]
			select_text = self.language_texts["select_a_text_to_write"]

			# Ask for text
			option_info = self.Input.Select(list(self.slim_texts[self.user_language].keys()), language_options = list(self.slim_texts[self.user_language].values()), show_text = show_text, select_text = select_text)

		if self.option_info != None:
			print("---")
			print()
			print(self.language_texts["you_selected_this_option"] + ":")
			print(self.option_info["option"])

		if self.option_info == None:
			self.option_info = option_info

	def Define_Text_Variables(self):
		self.text["key"] = self.option_info["option"]

		# Define language texts to write
		self.text["texts"] = {}

		for language in self.small_languages:
			self.text["texts"][language] = self.slim_texts[language][self.text["key"]].replace("...", "")

		# If key in slim texts, ask for description of text
		if self.text["key"] in self.slim_texts:
			self.text_dictionary = self.slim_texts[self.text["key"]]

			# Define explain_text if it is not present
			if "explain_text" not in self.text_dictionary:
				self.text_dictionary["explain_text"] = "say_what_you_did_on_the_{}"

			# Ask for text data if type_text is present on text dictionary
			if "type_text" in self.text_dictionary:
				self.text["data"] = {
					self.user_language: self.Input.Type(self.language_texts[self.text_dictionary["type_text"]]),
				}

				for language in self.small_languages:
					if language not in self.text["data"]:
						self.text["data"][language] = self.text["data"][self.user_language]

				# Split text data items, add commas between them, and add "and" text before the last item
				if ", " in self.text["data"][self.user_language]:
					for language in self.small_languages:
						split = self.text["data"][language].split(", ")

						self.text["data"][language] = ""

						for item in split:
							if item == split[-1]:
								self.text["data"][language] += self.texts["and"][language] + " "

							self.text["data"][language] += item

							if item != split[-1]:
								self.text["data"][language] += ", "

						# Replace singular name with plural name on text
						if "plural_item" in self.text_dictionary:
							self.text["texts"][language] = self.text["texts"][language].replace(self.texts[self.text_dictionary["singular_name"]][language], self.texts[self.text_dictionary["plural_name"]][language])

					self.text_dictionary["explain_text"] = "say_what_you_did_on_the_{}, plural"
					self.text_dictionary["item"] = self.text_dictionary["plural_item"]

				# Add quotes to text data
				else:
					for language in self.small_languages:
						self.text["data"][language] = '"' + self.text["data"][language] + '"'

				# Add text data to text
				for language in self.small_languages:
					self.text["texts"][language] += " " + self.text["data"][language]

			# Type task descriptions for the task
			self.Type_Task_Descriptions()

	def Type_Task_Descriptions(self):
		# Define task dictionary with names, descriptions, type, time, and files
		self.task_dictionary = {
			"names": {},
			"descriptions": {},
			"type": self.text["key"],
			"time": self.Date.Now()["%H:%M %d/%m/%Y"],
			"files": {},
		}

		print()
		print(self.language_texts["opening_the_description_files_for_you_to_type_on_them, type: explanation"])
		print()
		print(self.language_texts[self.text_dictionary["explain_text"]].format(self.language_texts[self.text_dictionary["item"]]) + ".")

		# Add files to dictionary, create and open them
		for language in self.small_languages:
			full_language = self.full_languages[language]

			self.task_dictionary["files"][language] = self.mega_folders["notepad"]["effort"]["diary_slim"]["root"] + full_language + ".txt"
			self.File.Create(self.task_dictionary["files"][language])

			if self.File.Exist(self.task_dictionary["files"][language]) == True:
				self.File.Open(self.task_dictionary["files"][language])

		# Create text with all languages translated to user language
		languages_text = ""

		for language in self.small_languages:
			translated_language = self.translated_languages[language][self.user_language]

			if len(self.small_languages) == 2 and language != self.small_languages[0]:
				languages_text += " "

			if language == self.small_languages[-1]:
				languages_text += self.language_texts["and"] + " "

			languages_text += translated_language

			if len(self.small_languages) != 2 and language != self.small_languages[-1]:
				languages_text += ", "

		# Wait for user to finish writing task descriptions
		self.Input.Type(self.language_texts["press_enter_when_you_finish_writing_and_saving_the_description_in_{}"].format(languages_text))

		# Create backup file
		self.backup_file = self.mega_folders["notepad"]["effort"]["diary_slim"]["root"] + "Descriptions backup.txt"
		self.File.Create(self.backup_file)

		# Define task descriptions and make a backup of them
		for language in self.small_languages:
			self.task_dictionary["names"][language] = self.text["texts"][language] + "."

			self.task_dictionary["descriptions"][language] = self.task_dictionary["names"][language] + "\n\n"
			self.task_dictionary["descriptions"][language] += self.File.Contents(self.task_dictionary["files"][language])["string"]

			text = self.task_dictionary["descriptions"][language]

			if language != self.small_languages[-1]:
				text += "\n\n"

			# Make backup
			self.File.Edit(self.backup_file, text, "a", next_line = False)

			self.File.Delete(self.task_dictionary["files"][language])

	def Write(self):
		text_to_write = self.text["texts"][self.user_language]

		# Register task and delete backup file if text key is in slim texts
		if self.text["key"] in self.slim_texts:
			from Tasks.Register_Task import Register_Task as Register_Task

			Register_Task(self.task_dictionary)

			if self.global_switches["verbose"] == True:
				print(self.Language.Python_To_JSON(self.task_dictionary))

			self.File.Delete(self.backup_file)

		# Update state and define text to write if text key is in state names list
		if self.text["key"] in self.states["names"]:
			state_texts = self.states[self.text["key"]]["texts"]

			order = ""

			if state_texts["current"] == []:
				order = "first"

			if state_texts["current"] != [] and state_texts["current"][0] == state_texts["first"][self.user_language]:
				order = "second"

			self.Update_State(self.text["key"], order)

			text_to_write = state_texts[order][self.user_language]

		# Add dot to end of text if it is not present
		if "." not in text_to_write[-1]:
			text_to_write += "."

		if self.text["key"] not in self.slim_texts:
			print()

			Write_On_Diary_Slim_Module(text_to_write)