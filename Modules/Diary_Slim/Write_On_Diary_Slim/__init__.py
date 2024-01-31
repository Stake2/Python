# Write_On_Diary_Slim.py

from Diary_Slim.Diary_Slim import Diary_Slim as Diary_Slim

from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

class Write_On_Diary_Slim(Diary_Slim):
	def __init__(self, option_info = None):
		super().__init__()

		self.option_info = option_info

		self.Configure_Slim_Texts()
		self.Select()
		self.Define_Text_Variables()
		self.Write()

		# Open the current Diary Slim file
		self.System.Open(self.current_year["File"])

		print()
		print(self.large_bar)

	def Configure_Slim_Texts(self):
		from copy import deepcopy

		self.date = self.Date.Now()

		# Get today task done text using weekday
		self.today_task_done_text = self.File.Contents(self.folders["Diary Slim"]["Data"]["things_done_texts"])["lines"][self.date["Units"]["Week day"]]

		default_dictionary = {
			"Key": "",
			"Folders": {},
			"Files": {},
			"Texts": {}
		}

		self.slim_texts["Dictionary"]["Today task"] = deepcopy(default_dictionary)
		self.slim_texts["Dictionary"]["Today task"]["Key"] = "Today task"
		self.slim_texts["Dictionary"]["Today task"]["Texts"][self.user_language] = ""

		for language in self.languages["small"]:
			# Iterate through the state names
			for state in self.states["names"]:
				state = self.states[state]
				state_texts = state["texts"]
				state_name = state["names"][self.user_language]

				order = "first"

				# If the current order text is first order, define the order as "second"
				if (
					state_texts["current"] != [] and
					state_texts["current"][0] == state_texts["first"][self.user_language]
				):
					order = "second"

				# Define the "first" or "second" order text in language
				text = self.JSON.Language.texts[order][language]

				# If the current order text is the second order text, remove the order from slim texts
				if (
					state_texts["current"] != [] and
					state_texts["current"][0] == state_texts["second"][self.user_language] and
					state_name in self.slim_texts["Dictionary"]
				):
					self.slim_texts["Dictionary"].pop(state_name)

				# If the current order text is empty, or the current order is not equal to the second order text, add state name to slim texts
				if (
					state_texts["current"] == [] or
					state_texts["current"] != [] and
					state_texts["current"][0] != state_texts["second"][self.user_language]
				):
					if state_name not in self.slim_texts["Dictionary"]:
						self.slim_texts["Dictionary"][state_name] = deepcopy(default_dictionary)

						self.slim_texts["Dictionary"][state_name]["Key"] = state_name

					self.slim_texts["Dictionary"][state_name]["Texts"][language] = state["names"][language] + " (" + text + " " + self.JSON.Language.texts["state"][language] + ")"

			# Add today done task to slim texts
			if self.today_task_done_text != "":
				if ", " not in self.today_task_done_text:
					self.slim_texts["Dictionary"]["Today task"]["Key"] = "Today task"
					self.slim_texts["Dictionary"]["Today task"]["Texts"][self.user_language] = self.today_task_done_text

				if ", " in self.today_task_done_text:
					items = [
						"First",
						"Second"
					]

					i = 0
					for item in items:
						key = item + " today task"

						self.slim_texts["Dictionary"][key] = deepcopy(default_dictionary)

						self.slim_texts["Dictionary"][key]["Key"] = key
						self.slim_texts["Dictionary"]["Today task"]["Texts"][self.user_language] = self.today_task_done_text.split(", ")[i]

						i += 1

	def Remove_State_Text(self, text):
		for state in self.states["names"]:
			items_to_remove = [
				" (" + self.JSON.Language.language_texts["first"] + " " + self.JSON.Language.language_texts["state"] + ")",
				" (" + self.JSON.Language.language_texts["second"] + " " + self.JSON.Language.language_texts["state"] + ")",
			]

			for item in items_to_remove:
				if item in text:
					text = text.replace(item, "")

		return text

	def Select(self):
		from copy import deepcopy

		if self.option_info == None:
			show_text = self.language_texts["texts_to_write"]
			select_text = self.language_texts["select_a_text_to_write"]

			options = list(self.slim_texts["Dictionary"].keys())
			language_options = []

			options_copy = deepcopy(options)

			for key in options_copy:
				dictionary = self.slim_texts["Dictionary"][key]

				text = dictionary["Texts"][self.user_language]

				if "Item" in dictionary:
					text += "..."

				language_options.append(text)

				if (
					key == "Today task" and
					text == ""
				):
					options.remove(key)
					options_copy.remove(key)
					language_options.remove(text)

			# Change the index of Slim texts if they have a custom index
			for key in options_copy:
				dictionary = self.slim_texts["Dictionary"][key]

				text = dictionary["Texts"][self.user_language]

				if "Index" in dictionary:
					index = dictionary["Index"] - 1

					if index == -1:
						index = len(options) - 1

					options.remove(key)
					options.insert(index, key)

					language_options.remove(text)
					language_options.insert(index, text)

			# Add the state texts to the end of the list
			for state in self.states["names"]:
				state = self.states[state]
				state_texts = state["texts"]
				state_name = state["names"][self.user_language]

				if state_name in options:
					options.remove(state_name)
					options.append(state_name)

					order = "first"

					# If the current order text is first order, define the order as "second"
					if (
						state_texts["current"] != [] and
						state_texts["current"][0] == state_texts["first"][self.user_language]
					):
						order = "second"

					text = state["names"][self.user_language] + " (" +  self.JSON.Language.texts[order][self.user_language] + " " + self.JSON.Language.texts["state"][self.user_language] + ")"

					if text in language_options:
						language_options.remove(text)

					language_options.append(text)

			# Add the "today task" text to the end of the list
			text = self.slim_texts["Dictionary"]["Today task"]["Texts"][self.user_language]

			if text in language_options:
				language_options.remove(text)

			if text != "":
				language_options.append(text)

			# Ask for the user to select the Slim text
			option_info = self.Input.Select(options, language_options = language_options, show_text = show_text, select_text = select_text)

		if self.option_info != None:
			print("---")
			print()
			print(self.language_texts["you_selected_this_option"] + ":")
			print(self.option_info["option"])

		if self.option_info == None:
			self.option_info = option_info

		self.text = self.slim_texts["Dictionary"][self.option_info["option"]]

	def Define_Text_Variables(self):
		for language in self.languages["small"]:
			self.text["Texts"][language] = self.text["Texts"][language].replace("...", "")

		# If key in slim texts, ask for description of text
		if "Item" in self.text:
			# Define the singular name if it is not present
			if "Singular name" not in self.text:
				self.text["Singular name"] = self.text["Item"]

			# Define the plural name if it is not present
			if "Plural name" not in self.text:
				self.text["Plural name"] = self.text["Singular name"] + "s"

			# Define the explain text if it is not present
			if "Explain text" not in self.text:
				self.text["Explain text"] = "say_what_you_did_on_the_{}"

			# Ask for the text data if it has a type text
			if "Type text" in self.text:
				print()
				print(self.large_bar)
				print()
				print(self.text["Texts"][self.user_language] + ":")

				self.text["Data"] = {}

				if "Options" not in self.text:
					self.text["Data"][self.user_language] = self.Input.Type(self.language_texts[self.text["Type text"]])

				else:
					options = self.text["Options"]

					item = options["Show"]

					if "_" not in item:
						item += ", title()"

					options["Show"] = self.JSON.Language.language_texts[item]

					self.text["Data"][self.user_language] = self.Input.Select(options["List"], show_text = options["Show"])["option"]

				for language in self.languages["small"]:
					if language not in self.text["Data"]:
						self.text["Data"][language] = self.text["Data"][self.user_language]

				# Split the text data items, add commas between them, and add "and" text before the last item
				if ", " in self.text["Data"][self.user_language]:
					for language in self.languages["small"]:
						split = self.text["Data"][language].split(", ")

						self.text["Data"][language] = ""

						for item in split:
							if (
								item != split[0] and
								len(split) == 2
							):
								self.text["Data"][language] += " "

							if item == split[-1]:
								self.text["Data"][language] += self.JSON.Language.texts["and"][language] + " "

							self.text["Data"][language] += item

							if (
								item != split[-1] and
								len(split) != 2
							):
								self.text["Data"][language] += ", "

						# Replace singular name with plural name on text
						if "Plural item" in self.text:
							self.text["Texts"][language] = self.text["Texts"][language].replace(self.texts[self.text["Singular name"]][language], self.texts[self.text["Plural name"]][language])

					self.text["Explain text"] = "say_what_you_did_on_the_{}, plural"

					self.text["Item"] = self.text["Plural item"]

				# Add quotes to text data if the text uses quotes
				else:
					if (
						"Quotes" not in self.text or
						"Quotes" in self.text and
						self.text["Quotes"] == True
					):
						for language in self.languages["small"]:
							self.text["Data"][language] = '"' + self.text["Data"][language] + '"'

				# Add text data to text
				for language in self.languages["small"]:
					self.text["Texts"][language] += " " + self.text["Data"][language]

			print()
			print("---")

			# Type task descriptions for the task
			self.Type_Task_Descriptions()

	def Type_Task_Descriptions(self):
		# Define task dictionary with titles, descriptions, type, time, and files
		self.task_dictionary = {
			"Type": self.text["Key"],
			"Task": {
				"Titles": {},
				"Descriptions": {}
			},
			"Entry": {
				"Date": self.Date.Now()
			},
			"Files": {}
		}

		print()
		print(self.language_texts["opening_the_description_files_for_you_to_type_on_them, type: explanation"])
		print()
		print(self.language_texts[self.text["Explain text"]].format(self.language_texts[self.text["Item"]]) + ".")

		# Add files to dictionary, create and open them
		for language in self.languages["small"]:
			full_language = self.languages["full"][language]

			self.task_dictionary["Files"][language] = self.folders["Notepad"]["Diary Slim"]["root"] + full_language + ".txt"
			self.File.Create(self.task_dictionary["Files"][language])

			if self.File.Exist(self.task_dictionary["Files"][language]) == True:
				self.System.Open(self.task_dictionary["Files"][language])

		# Create text with all languages translated to user language
		languages_text = ""

		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language][self.user_language]

			if len(self.languages["small"]) == 2 and language != self.languages["small"][0]:
				languages_text += " "

			if language == self.languages["small"][-1]:
				languages_text += self.JSON.Language.language_texts["and"] + " "

			languages_text += translated_language

			if len(self.languages["small"]) != 2 and language != self.languages["small"][-1]:
				languages_text += ", "

		# Wait for user to finish writing task descriptions
		self.Input.Type(self.language_texts["press_enter_when_you_finish_writing_and_saving_the_description_in_{}"].format(languages_text))

		# Create backup file
		self.backup_file = self.folders["Notepad"]["Diary Slim"]["root"] + "Descriptions backup.txt"
		self.File.Create(self.backup_file)

		# Define task descriptions and make a backup of them
		for language in self.languages["small"]:
			self.task_dictionary["Task"]["Titles"][language] = self.text["Texts"][language]

			self.task_dictionary["Task"]["Descriptions"][language] = self.task_dictionary["Task"]["Titles"][language] + "." + "\n\n"

			if self.switches["testing"] == False:
				self.task_dictionary["Task"]["Descriptions"][language] += self.File.Contents(self.task_dictionary["Files"][language])["string"]

			else:
				self.task_dictionary["Task"]["Descriptions"][language] += "[" + self.JSON.Language.texts["description, title()"][language] + "]"

			text = self.task_dictionary["Task"]["Descriptions"][language]

			if language != self.languages["small"][-1]:
				text += "\n\n"

			# Make backup
			self.File.Edit(self.backup_file, text, "a", next_line = False)

			self.File.Delete(self.task_dictionary["Files"][language])

	def Write(self):
		text_to_write = self.text["Texts"][self.user_language]

		# Register task and delete backup file if text key is in slim texts
		if "Item" in self.text:
			# Import the "Register" class of the "Tasks" module
			from Tasks.Register import Register as Register

			# Run the "Register" class
			Register(self.task_dictionary)

			# Delete the backup file
			self.File.Delete(self.backup_file)

		# Update the state and define the text to write if the text key is in the state names list
		if self.text["Key"] in self.states["names"]:
			state_texts = self.states[self.text["Key"]]["texts"]

			order = ""

			if state_texts["current"] == []:
				order = "first"

			if (
				state_texts["current"] != [] and
				state_texts["current"][0] == state_texts["first"][self.user_language]
			):
				order = "second"

			self.Update_State(self.text["Key"], order)

			text_to_write = state_texts[order][self.user_language]

		# Add dot to end of text if it is not present
		if "." not in text_to_write[-1]:
			text_to_write += "."

		if "Item" not in self.text:
			print()

			Write_On_Diary_Slim_Module(text_to_write)