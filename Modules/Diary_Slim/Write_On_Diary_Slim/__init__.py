# Write_On_Diary_Slim.py

from Diary_Slim.Diary_Slim import Diary_Slim as Diary_Slim

from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

from copy import deepcopy

class Write_On_Diary_Slim(Diary_Slim):
	def __init__(self):
		super().__init__()

		# Define the root dictionary
		self.dictionary = {
			"Text": {},
			"Text to write": "",
			"Question keys": [
				"Question",
				"Questions"
			]
		}

		# Define the States dictionary
		self.states = {
			"Multi-selection": False,
			"Input on end": False
		}

		# Select the Diary Slim text
		self.Select_The_Text()

		# If the Diary Slim text is a statistic
		if self.dictionary["Text"]["Is statistic"] == True:
			# Define the "Input on end" state as True
			self.states["Input on end"] = True

		# If the "Is task" key is inside the text dictionary
		if "Is task" in self.dictionary["Text"]:
			# Register the task
			self.Register_Task()

		# If the text key is inside the root "Statistics" dictionary
		if self.dictionary["Text"]["Key"] in self.statistics["Dictionary"]:
			# Run the method to manage statistics
			self.Manage_Statistic()

		# If the "Is task" key is inside the text dictionary
		# And the task was not registered
		# Or the "States" key is inside the "Text" dictionary
		# And the current state in the backup is not the first one
		if (
			"Is task" in self.dictionary["Text"] and
			self.task_dictionary["Register task"] == False or
			"States" in self.dictionary["Text"] and
			self.dictionary["Text"]["States (backup)"]["Current state"] != self.dictionary["Text"]["States"]["Dictionary"]["1"]
		):
			# Define the "Input on end" state as False
			self.states["Input on end"] = False

		# Write the Diary Slim text
		self.Write()

	def Select_The_Text(self):
		from copy import deepcopy

		global parameters

		# Define the parameters dictionary to use inside the "Select" method of the "Input" utility module
		parameters = {
			"options": deepcopy(self.diary_slim["Texts"]["Options"]["Keys"]),
			"language_options": deepcopy(self.diary_slim["Texts"]["Options"][self.language["Small"]]),
			"show_text": self.language_texts["texts_to_write"],
			"select_text": self.language_texts["select_a_text_to_write"]
		}

		# Change the index of the Diary Slim texts dictionary if the text has a custom index
		for key in self.diary_slim["Texts"]["Options"]["Keys"]:
			# Get the text dictionary
			dictionary = self.diary_slim["Texts"]["Dictionary"][key]

			# Get the user language text
			text = dictionary["Texts"][self.language["Small"]]

			# If the "Index" key is inside the dictionary
			if "Index" in dictionary:
				# Get the correct index
				index = dictionary["Index"] - 1

				# If the index is "-1", use the last index (the text will be the last one)
				if index == -1:
					index = len(parameters["options"]) - 1

				# Remove the key and insert it at the correct index
				parameters["options"].remove(key)
				parameters["options"].insert(index, key)

				# Remove the language text and insert it at the correct index
				parameters["language_options"].remove(text)
				parameters["language_options"].insert(index, text)

			# Remove the option if the "Multi-selection" mode is activated
			# And the "Is task" key is present inside the text dictionary
			if (
				self.states["Multi-selection"] == True and
				"Is task" in dictionary
			):
				parameters["options"].remove(key)
				parameters["language_options"].remove(text)

		# Change the index of the Diary Slim Texts dictionary if the text has a custom index
		i = 0
		for key in self.diary_slim["Texts"]["Options"]["Keys"]:
			# Get the text dictionary
			dictionary = self.diary_slim["Texts"]["Dictionary"][key]

			# If" "Is task" key is present inside the text dictionary
			if "Is task" in dictionary:
				# Get the user language text
				text = dictionary["Texts"][self.language["Small"]]

				# Define the item text key
				text_key = dictionary["Key"]

				# If the "Item" key is inside the text dictionary
				if "Item" in dictionary:
					# Get the item text
					text_key = dictionary["Item"]

					# If the "_" (underscore) character is not inside the text key
					if "_" not in text_key:
						# Add the ", title()" text to the text key
						text_key += ", title()"

				# Define the texts dictionary
				texts = self.Language.language_texts

				# If the text key is inside the texts dictionary
				if text_key in texts:
					# Get the item text
					item_text = self.Language.language_texts[text_key]

				else:
					# Define the item text as the text key
					item_text = text_key

				# Find the index of the text
				index = parameters["language_options"].index(text)

				# Update the text to add the item text and the three dots
				text = "(" + item_text + ") " + text + "..."

				# Update the text inside the list of language options
				parameters["language_options"][index] = text

		# Add the "[Multi-selection]" option if its mode is deactivated
		if self.states["Multi-selection"] == False:
			# Add the "[Multi-selection]" text to the list of options
			parameters["options"].append("[Multi-selection]")

			# Get the language text
			language_text = "[" + self.Language.language_texts["multi_selection"] + "]"

			# Add the "[Multi-selection]" text in the user language to the list of language options
			parameters["language_options"].append(language_text)

		# If the "Multi-selection" mode is activated
		# And the Diary Slim text is not a statistic
		if (
			self.states["Multi-selection"] == True and
			self.dictionary["Text"]["Is statistic"] == True
		):
			# Run the "Multi_Selection" method
			self.Multi_Selection()

		# If the "Multi-selection" mode is deactivated
		if self.states["Multi-selection"] == False:
			# Ask the user to select the Diary Slim text
			option = self.Input.Select(**parameters)["option"]

			# If the option is not "[Multi-selection]" one
			if option != "[Multi-selection]":
				# Define the "Text" dictionary inside the root dictionary
				self.dictionary["Text"] = self.diary_slim["Texts"]["Dictionary"][option]

				# Define the "Text to write" as the language text
				self.dictionary["Text to write"] = self.dictionary["Text"]["Texts"][self.language["Small"]]

				# If the "States" key is inside the "Text" dictionary
				if "States" in self.dictionary["Text"]:
					# Get the current state
					self.dictionary["Text to write"] = self.dictionary["Text"]["States"]["Current state"][self.language["Small"]]

			# If the option is the "[Multi-selection]" one
			if option == "[Multi-selection]":
				# Change the "Multi-selection" mode to activated
				self.states["Multi-selection"] = True

				# Run this method again to run it with the "Multi-selection" mode activated
				self.Select_The_Text()

			# If the "States" key is inside the "Text" dictionary
			if "States" in self.dictionary["Text"]:
				# Make a backup of the "States" dictionary
				self.dictionary["Text"]["States (backup)"] = deepcopy(self.dictionary["Text"]["States"])

				# Change the current state to the next state
				self.Next_State(self.dictionary["Text"])

			# Iterate through the list of question keys inside the list above
			for key in self.dictionary["Question keys"]:
				# If the key is inside the text dictionary
				if key in self.dictionary["Text"]:
					# Get the additional information about the Diary Slim text and update the text to write
					self.dictionary["Text to write"] = self.Get_Additional_Information(self.dictionary["Text"])["Text to write"]

	def Get_Additional_Information(self, dictionary, is_statistic = False):
		# Define the default text dictionary
		text_dictionary = dictionary

		# If the information is a statistic
		if is_statistic == True:
			# Define the text dictionary as the statistic one
			text_dictionary = dictionary["Statistic"]

		# Define the default questions dictionary
		questions = {}

		# Define the default "Has questions" state as False
		has_questions = False

		# If there is only one question
		if "Question" in text_dictionary:
			# Define the first question as the only question that exists
			questions["1"] = {
				"Key": "1",
				**text_dictionary["Question"]
			}

			# Change the "Has questions" state to True
			has_questions = True

		# If there are more questions
		if "Questions" in text_dictionary:
			# Re-define the questions dictionary as the one already inside the text dictionary
			questions = text_dictionary["Questions"]

			# Iterate through the questions inside the dictionary of questions, getting the key and question dictionary
			for key in questions:
				# Update the question dictionary inside the root questions dictionary
				questions[key] = {
					"Key": key,
					**questions[key]
				}

			# Change the "Has questions" state to True
			has_questions = True

		# Define the default text to write
		text_to_write = ""

		# Iterate through the questions inside the dictionary, getting the key and question dictionary
		for key, question in questions.items():
			# If the question type is "Yes or No"
			if question["Question type"] == "Yes or No":
				# Get the input text
				input_text = self.Define_Input_Text(question)

				# Ask the question and get the user response, adding it to the question dictionary
				questions[key]["Response"] = {
					"Boolean": self.Input.Yes_Or_No(input_text)
				}

				# Get the text version of the response (from "True" or "False" to "Yes" or "No")
				questions[key]["Response"]["Text"] = self.Input.Define_Yes_Or_No(questions[key]["Response"]["Boolean"], inverse = True)

				# If the text response exists inside the answers dictionary
				if questions[key]["Response"]["Text"] in question["Answers"]:
					# Define the response variable for easier typing
					response = questions[key]["Response"]["Text"]

					# Get the answer dictionary
					answer = question["Answers"][response]

					# If the "Question type" is inside the answer dictionary
					# And the question type is "Type"
					if (
						"Question type" in answer and
						answer["Question type"] == "Type"
					):
						# Get the input text
						answer["Text"] = self.Define_Input_Text(answer)

						# Get and verify the user input, creating the "Answers" dictionary
						questions[key]["Response"]["Answers"] = {
							response: self.Verify_Input(answer)
						}

					# If the "Format" key is inside the answer dictionary
					if "Format" in answer:
						# Define the format variable for easier typing
						format = answer["Format"][self.language["Small"]]

						# Define the text to write as the default one
						text_to_write = self.dictionary["Text"]["Texts"][self.language["Small"]]

						# Update the text to write
						text_to_write = format.replace("{Text}", text_to_write)

						# Format the format text with the text to write
						questions[key]["Response"] = text_to_write

			# If the question type is "Type"
			if question["Question type"] == "Type":
				# Get the input text
				question["Text"] = self.Define_Input_Text(question)

				# Get and verify the user input
				questions[key]["Response"] = self.Verify_Input(question)

			# If the question type is "Select"
			if question["Question type"] == "Select":
				# Create the local texts dictionary with the show and select texts
				texts = {
					"Show": question["Show text"],
					"Select": question["Select text"]
				}

				# Iterate through the texts inside the dictionary above
				for item, value in texts.items():
					# Define the local language texts dictionary
					language_texts = self.Language.language_texts

					# If the value (text key) is inside the language texts dictionary of this module
					if value in self.language_texts:
						# Define the local language texts dictionary as that one
						language_texts = self.language_texts

					# If the value (text key) is inside the local list of language texts
					if value in language_texts:
						# Get the language text for the current value (text key)
						texts[item] = language_texts[value]

				# Get the user response
				questions[key]["Response"] = self.Input.Select(question["List"], show_text = texts["Show"], select_text = texts["Select"])["Option"]["Original"]

				# If the "Genders" key is inside the question dictionary
				if "Genders" in question:
					# Define the item key
					item_key = "{" + question["Item"] + "}"

					# Iterate through the text keys inside the list of keys
					for text_key in question["Genders"]["Keys"]:
						# Get the text from the text key and add curly brackets
						text = "{" + self.Language.language_texts[text_key] + "}"

						# If the item text is not inside the key
						if question["Item"] not in text_key:
							# Define that key as the gender text key
							gender_text_key = text

						# If the text is inside the Diary Slim text
						if text in self.dictionary["Text"]["Texts"][self.language["Small"]]:
							# Define the item key as the text key
							item_key = text

					# Replace the item key with the user response
					self.dictionary["Text"]["Texts"][self.language["Small"]] = self.dictionary["Text"]["Texts"][self.language["Small"]].replace(item_key, questions[key]["Response"])

					# If the "Gender text" key is inside the text
					if gender_text_key in self.dictionary["Text"]["Texts"][self.language["Small"]]:
						# Iterate through the list of genders
						for gender in ["Masculine", "Feminine"]:
							# Get the gender dictionary
							gender = question["Genders"][gender]

							# If the user response is inside the gender list of the current gender
							if questions[key]["Response"] in gender["List"]:
								# Get the gender text key from the current gender dictionary
								text_key = gender["Format text"]

								# Get the language text
								text = self.Language.language_texts[text_key]

								# Replace the gender text template inside the text with the correct gender text
								self.dictionary["Text"]["Texts"][self.language["Small"]] = self.dictionary["Text"]["Texts"][self.language["Small"]].replace(gender_text_key, text)

					# Update the text to write
					text_to_write = self.dictionary["Text"]["Texts"][self.language["Small"]]

		# If the text to write continues to be empty
		if text_to_write == "":
			# Define it as the Diary Slim text in the user language
			text_to_write = self.dictionary["Text"]["Texts"][self.language["Small"]]

		# Define the return dictionary
		return_dictionary = {
			"Text to write": text_to_write,
			"Questions": questions,
			"Has questions": has_questions
		}

		return return_dictionary

	def Define_Input_Text(self, question):
		# Define the default value of the input text as the question
		input_text = question

		# If the "Input text" key is inside the question dictionary
		if "Input text" in question:
			# Define the input text
			input_text = question["Input text"]

		# If the input text is a string
		if isinstance(input_text, str) == True:
			# If the input text is a key inside the root texts dictionary of this module
			if input_text in self.texts:
				# Define the dictionary of texts as that one
				texts_dictionary = self.texts

			# Else, define it as the dictionary of the "Language" module
			else:
				texts_dictionary = self.Language.texts

			# If the input text is inside the local texts dictionary
			if input_text in texts_dictionary:
				# Get the correct text dictionary from the text key
				input_text = texts_dictionary[input_text]

			# If the user language key is inside the input text dictionary
			if self.language["Small"] in input_text:
				# Get the user language version of the input text
				input_text = input_text[self.language["Small"]]

		# Return the language input text
		return input_text

	def Verify_Input(self, type_dictionary):
		# Define the default regex
		regex = None

		# If the "Type" key is inside the type dictionary
		# And its value is "Number"
		if (
			"Type" in type_dictionary and
			type_dictionary["Type"] == "Number"
		):
			regex = r"\b[1-9][0-9]*\b; 10"

		# Ask the user to type the information with the type text
		text_to_write = self.Input.Type(type_dictionary["Text"], accept_enter = False, regex = regex)

		return text_to_write

	def Multi_Selection(self):
		# Add the "[Finish selection]" text to the list of options
		parameters["options"].append("[Finish selection]")

		# Define the language text
		language_text = "[" + self.Language.language_texts["finish_selection"] + "]"

		# Add the "[Finish selection]" text in the user language to the list of language options
		parameters["language_options"].append(language_text)

		# Define the option as an empty string
		option = ""

		# Define the empty texts list
		texts = []

		# Define the "finish selection" variable for easier typing
		finish_selection = "[Finish selection]"

		# While the option is not the "[Finish selection]" text
		while option != finish_selection:
			# Show a five dash space separator
			print()
			print(self.separators["5"])

			# If the list of texts is not empty
			if texts != []:
				# Show the "List:" text
				print()
				print(self.Language.language_texts["list, title()"] + ":")

				# Show the list of texts
				print("[")

				# Iterate through the texts in the list
				for text in texts:
					# Make a backup of the text
					text_backup = text

					# Add one tab to the text
					text = text.replace("\n", "\n\t")

					# Show the text with a tab and quotes around it
					print("\t" + '"' + text + '"')

					# If the text backup is not the last one, show a space separator
					if text_backup != texts[-1]:
						print()

				# Show the end of the list
				print("]")

			# Ask the user to select the Diary Slim text
			option = self.Input.Select(**parameters)["option"]

			# If the option is not the "[Finish selection]" text
			if option != finish_selection:
				# Define the "Text" dictionary inside the root dictionary
				self.dictionary["Text"] = self.diary_slim["Texts"]["Dictionary"][option]

				# Remove the selected text from the parameters dictionary
				parameters["options"].remove(option)
				parameters["language_options"].remove(self.dictionary["Text"]["Texts"][self.language["Small"]])

				# Add two line breaks if the text is not the first one
				if texts != []:
					self.dictionary["Text to write"] += "\n\n"

				# Define the language text
				language_text = self.dictionary["Text"]["Texts"][self.language["Small"]]

				# If the "States" key is inside the "Text" dictionary
				if "States" in self.dictionary["Text"]:
					# Get the current state
					language_text = self.dictionary["Text"]["States"]["Current state"][self.language["Small"]]

					# Change the current state to the next state
					self.Next_State(self.dictionary["Text"])

				# If the "Additional information" key is inside the "Text" dictionary
				if "Additional information" in self.dictionary["Text"]:
					# Define the additional information and update the text to write
					language_text = self.Define_Additional_Information(self.dictionary, language_text)["Text"]

				# Add the language text to the "Text to write" string
				self.dictionary["Text to write"] += language_text

				# Add a period to the end of the text if it is not present
				if "." not in self.dictionary["Text to write"][-1]:
					self.dictionary["Text to write"] += "."

				# Replace the line break characters (\n) inside the language text with real line breaks
				language_text = language_text.replace("\n", "\n")

				# Add the language text to the texts list
				texts.append(language_text)

	def Register_Task(self):
		# Define the task dictionary
		# With the task type and entry date
		self.task_dictionary = {
			"Type": self.dictionary["Text"]["Key"],
			"Entry": {
				"Times": {}
			},
			"Register task": True
		}

		# ---------- #

		# Register the completed task time in the "Times" dictionary
		time_key = "Completed task"
		self.task_dictionary["Entry"]["Times"][time_key] = self.Date.Now()

		# Register the completed task time in the UTC time
		self.task_dictionary["Entry"]["Times"][time_key + " (UTC)"] = self.task_dictionary["Entry"]["Times"][time_key]

		# ---------- #

		# If the "Has task progress" key is inside the text dictionary
		if "Has task progress" in self.dictionary["Text"]:
			# Define the list of options
			options = [
				"Register task",
				"Register task progress"
			]

			# Define the list of language options
			language_options = [
				self.language_texts["register_the_task"],
				self.language_texts["register_the_task_progress"]
			]

			# Define the show and select text
			show_text = self.language_texts["list_of_actions"]
			select_text = self.language_texts["choose_the_action"]

			# Ask if the user wants to register the task progress
			response = self.Input.Select(options, language_options = language_options, show_text = show_text, select_text = select_text)["Option"]["Original"]

			# If the answer is "Register task progress"
			if response == "Register task progress":
				# Change the "Register task" state to False
				self.task_dictionary["Register task"] = False

		# Import the "Register" class of the "Tasks" module
		from Tasks.Register import Register as Register

		# Run the "Register" class with the local Task dictionary
		Register(self.task_dictionary)

	def Manage_Statistic(self):
		# Define the key
		text_key = self.dictionary["Text"]["Key"]

		# Get the statistic
		statistic = {
			**self.statistics["Dictionary"][text_key],
			"Has questions": False
		}

		# Define the questions dictionary
		questions = statistic

		# If the "Is task" key is not inside the text dictionary
		# Or it is, and the task was registered
		if (
			"Is task" not in self.dictionary["Text"] or
			"Is task" in self.dictionary["Text"] and
			self.task_dictionary["Register task"] == True
		):
			# Iterate through the list of question keys inside the list above
			for question_key in self.dictionary["Question keys"]:
				# If the key is inside the statistic dictionary
				if question_key in self.dictionary["Text"]["Statistic"]:
					# Get the additional information about the statistic, passing the "Is statistic" parameter as True
					information = self.Get_Additional_Information(self.dictionary["Text"], is_statistic = True)

					# Define the text to write, questions, and "Has questions" state using the values inside the local information dictionary
					self.dictionary["Text to write"] = information["Text to write"]
					questions = information["Questions"]
					statistic["Has questions"] = information["Has questions"]

		# Get the statistic dictionary of the Diary Slim text, in the current year
		current_year_statistics = self.diary_slim["Current year"]["Statistics"][text_key]

		# Get the statistic dictionary of the Diary Slim text, in the current month
		current_month_statistics = self.diary_slim["Current year"]["Month"]["Statistics"][text_key]

		# ---------- #

		# Define the statistic text key
		statistic_text_key = statistic["Key"].replace(" ", "_").lower()

		# Define the default value for the statistic text as its key
		statistic_text = statistic["Key"]

		# Define the statistic text if the key exists inside the language texts dictionary of the "Language" class
		if statistic_text_key in self.Language.language_texts:
			statistic_text = self.Language.language_texts[statistic_text_key]

		# If the "Data" is inside the Diary Slim text dictionary
		if (
			"Data" in self.dictionary["Text"] and
			self.dictionary["Text"]["Data"][self.language["Small"]] in current_year_statistics
		):
			# Get the text from it
			statistic_text = self.dictionary["Text"]["Data"][self.language["Small"]]

		# If the "Text" key is inside the statistic dictionary
		if "Text" in statistic:
			statistic_text = statistic["Text"][self.language["Small"]]

		# ---------- #

		# Add to the statistic numbers of the current year

		# If the text key is inside the statistics dictionary of the current year
		if text_key in self.diary_slim["Current year"]["Statistics"]:
			# Define the statistic key as the key inside the statistic dictionary
			statistic_key = statistic["Key"]

		# If the "Question" key is inside the statistic dictionary
		# And the "Item" key is inside the question dictionary
		if (
			"Question" in statistic and
			"Item" in statistic["Question"]
		):
			# Define the statistic key as the response of the first question, as there is only one
			statistic_key = questions["1"]["Response"]

		# If the "Alternative key" key is inside the statistic dictionary
		if "Alternative key" in statistic:
			# Define the local statistic key as it
			statistic_key = statistic["Alternative key"]

		# ---------- #

		# Define the "Statistics" dictionary inside the Diary Slim text dictionary
		self.dictionary["Text"]["Statistics"] = {
			"Number": 0,
			"Dictionary": {
				statistic["Key"]: {
					"Text": statistic_text,
					"Old number": "",
					"Number": ""
				}
			},
			"Changed statistic": False
		}

		# ---------- #

		# Define the month statistics
		self.dictionary["Text"]["Statistics"]["Month"] = {
			"Number": 0,
			"Dictionary": {
				statistic["Key"]: {
					"Text": statistic_text,
					"Old number": "",
					"Number": ""
				}
			}
		}

		# ---------- #

		# Get the current number of the current year
		current_number = current_year_statistics[statistic_key]

		# Define the old and current number
		self.dictionary["Text"]["Statistics"]["Dictionary"][statistic["Key"]]["Old number"] = current_number
		self.dictionary["Text"]["Statistics"]["Dictionary"][statistic["Key"]]["Number"] = current_number

		# ---------- #

		# Get the current number of the current month
		current_number = current_month_statistics[statistic_key]

		# Define the old and current number
		self.dictionary["Text"]["Statistics"]["Month"]["Dictionary"][statistic["Key"]]["Old number"] = current_number
		self.dictionary["Text"]["Statistics"]["Month"]["Dictionary"][statistic["Key"]]["Number"] = current_number

		# ---------- #

		# Define the number to add as one
		number = 1

		# ---------- #

		# If the "Has questions" state is True
		if statistic["Has questions"] == True:
			# Iterate through the questions inside the dictionary, getting the key and question dictionary
			for key, question in questions.items():
				# Get the response
				response = question["Response"]

				# If the response is a dictionary
				if isinstance(response, dict):
					# Get the text response
					text_response = response["Text"]

					# If the "Answers" key is inside the response dictionary
					if "Answers" in response:
						# Get the answer dictionary, using the text response as the key
						answer = response["Answers"][text_response]

						# If the answer is a digit
						if answer.isdigit() == True:
							number = int(answer)

				# If the response is a number
				if (
					isinstance(response, dict) == False and
					response.isdigit() == True
				):
					# Define the number to add as the response
					number = int(response)

				# Define the list of no answers
				no_answers = ["No", 0, "0"]

				# If the response is inside the list of no answers
				# Or the response is a dictionary and the text inside of it is inside the list above
				if (
					response in no_answers or
					isinstance(response, dict) and
					response["Text"] in no_answers
				):
					# Define the number as zero
					number = 0

				# If the "Key" key is inside the question dictionary
				# And the key is not inside the range of the number of questions
				if (
					"Key" in question and
					int(question["Key"]) not in range(1, len(questions) + 1)
				):
					# Define the local text key
					local_text_key = question["Key"].replace(" ", "_").lower()

					# Define the old number
					old_number = current_year_statistics[question["Key"]]

					# Define the number to add as the response number
					number_to_add = number

					# Add the additional question key to the root statistics dictionary
					self.dictionary["Text"]["Statistics"]["Dictionary"][question["Key"]] = {
						"Text": self.Language.language_texts[local_text_key],
						"Old number": old_number,
						"Number": old_number + number_to_add
					}

					# Update the number in the month statistic key
					current_year_statistics[question["Key"]] = self.dictionary["Text"]["Statistics"]["Dictionary"][question["Key"]]["Number"]

					# ----- #

					# Define the old number
					old_number = current_month_statistics[question["Key"]]

					# Add the additional question key to the month statistics dictionary
					self.dictionary["Text"]["Statistics"]["Month"]["Dictionary"][question["Key"]] = {
						"Text": self.Language.language_texts[local_text_key],
						"Old number": old_number,
						"Number": old_number + number_to_add
					}

					# Update the number in the month statistic key
					current_month_statistics[question["Key"]] = self.dictionary["Text"]["Statistics"]["Month"]["Dictionary"][question["Key"]]["Number"]

					# Define the number as one
					number = 1

				# If the "Questions" key is inside the statistic dictionary
				if "Questions" in statistic:
					# If the "Create sub-dictionary" key is inside the question dictionary
					if "Create sub-dictionary" in question:
						# Define the sub-dictionary key
						sub_key = question["Response"]

						# Define the dictionary to add
						to_add = {
							"Text": statistic_text
						}

						# If the sub-key is not inside the dictionary
						if sub_key not in to_add:
							# Add the sub-key with the dictionary
							to_add[sub_key] = {
								statistic["Key"]: 0
							}

						# Update the old number
						old_number = to_add[sub_key][statistic["Key"]]

						# Add one to the number
						to_add[sub_key][statistic["Key"]] += 1

						# Define the sub-dictionaries dictionary, with the question key (question number)
						sub_dictionaries = {
							key: to_add[sub_key]
						}

						# Update the to add dictionary to add the keys of the root statistics dictionary
						to_add = {
							**to_add
						}

						# Update the numbers
						to_add["Old number"] = old_number
						to_add["Number"] = to_add[sub_key][statistic["Key"]]

						# Add the sub-dictionary to the root statistics dictionary
						self.dictionary["Text"]["Statistics"]["Dictionary"][statistic_key] = to_add

						# Add the sub-dictionary to the month statistics dictionary
						self.dictionary["Text"]["Statistics"]["Month"]["Dictionary"][statistic_key] = to_add

						# Update the current year statistics in the current statistic key
						self.diary_slim["Current year"]["Statistics"][text_key] = {
							sub_key: to_add
						}

						# Define the current year statistics dictionary (with the current statistic key) as the "to add" one
						current_year_statistics = self.diary_slim["Current year"]["Statistics"][text_key]

						# Update the current month statistics in the current statistic key
						self.diary_slim["Current year"]["Month"]["Statistics"][text_key] = {
							sub_key: to_add
						}

						# Define the current month statistics dictionary (with the current statistic key) as the "to add" one
						current_month_statistics = self.diary_slim["Current year"]["Month"]["Statistics"][text_key]

					# If the "Add to sub-dictionary" key is inside the question dictionary
					if "Add to sub-dictionary" in question:
						# Get the sub-key
						sub_key = question["Add to sub-dictionary"]

						# If the question key is not inside the sub-dictionary
						if question["Key"] not in sub_dictionaries[sub_key]:
							sub_dictionaries[sub_key][question["Key"]] = 0

						# Get the old number
						old_number = sub_dictionaries[sub_key][question["Key"]]

						# Add the question key with the response as value, to the selected sub-dictionary
						sub_dictionaries[sub_key][question["Key"]] = response

						# Define the sub-dictionary
						sub_dictionary = sub_dictionaries[sub_key]

						# Get the correct sub-key
						sub_key = questions[sub_key]["Response"]

						# Update the sub-dictionary on the root statistics dictionary
						self.dictionary["Text"]["Statistics"]["Dictionary"][statistic_key].update(sub_dictionary)

						# Update the sub-dictionary on the month statistics dictionary
						self.dictionary["Text"]["Statistics"]["Month"]["Dictionary"][statistic_key].update(sub_dictionary)

						# Update the current year statistics in the current statistic key
						self.diary_slim["Current year"]["Statistics"][text_key] = {
							sub_key: sub_dictionary
						}

						# Define the current year statistics dictionary (with the current statistic key) as the "to add" one
						current_year_statistics = {
							sub_key: self.diary_slim["Current year"]["Statistics"][text_key]
						}

						# Update the current month statistics in the current statistic key
						self.diary_slim["Current year"]["Month"]["Statistics"][text_key] = {
							sub_key: sub_dictionary
						}

						# Define the current month statistics dictionary (with the current statistic key) as the "to add" one
						current_month_statistics = {
							sub_key: self.diary_slim["Current year"]["Month"]["Statistics"][text_key]
						}

						# ---------- #

						# Define the local text key
						local_text_key = question["Key"].replace(" ", "_").lower()

						# Add the additional question key to the root statistics dictionary
						self.dictionary["Text"]["Statistics"]["Dictionary"][question["Key"]] = {
							"Text": self.Language.language_texts[local_text_key],
							"Old number": old_number,
							"Number": response
						}

						# If the "Money" key is inside the question dictionary
						if "Money" in question:
							# Add the money key to the root statistics dictionary
							self.dictionary["Text"]["Statistics"]["Dictionary"][question["Key"]]["Money"] = question["Money"]

						# ---------- #

						# Add the additional question key to the month statistics dictionary
						self.dictionary["Text"]["Statistics"]["Month"]["Dictionary"][question["Key"]] = {
							"Text": self.Language.language_texts[local_text_key],
							"Old number": old_number,
							"Number": response
						}

						# If the "Money" key is inside the question dictionary
						if "Money" in question:
							# Add the money key to the month statistics dictionary
							self.dictionary["Text"]["Statistics"]["Month"]["Dictionary"][question["Key"]]["Money"] = question["Money"]

						# ---------- #

						# Change the "Changed statistic" to True
						self.dictionary["Text"]["Statistics"]["Changed statistic"] = True

						# ---------- #

						# Define the number as zero
						number = 0

						# ---------- #

						# Define the list of items to use
						items = [
							sub_key,
							response
						]

						# If the "Money" key is inside the question dictionary
						if "Money" in question:
							# Define the "Use extended" variable
							use_extended = True

							# If the "Use extended money text" is inside the question dictionary
							if "Use extended money text" in question:
								# Define the "Use extended" variable as the one inside that key
								use_extended = question["Use extended money text"]

							# Add the money text to the response and update the item inside the list above
							items[1] = self.Define_Money_Text(response, use_extended = use_extended)

						# Get the format text
						format_text = question["Format text"]

						# Format the text with the list of items, updating the text to write
						self.dictionary["Text to write"] = self.Language.language_texts[format_text].format(*items)

		# ---------- #

		# If the "Secondary statistics" key is inside the statistic dictionary
		if "Secondary statistics" in statistic:
			# Iterate through the keys and statistic dictionaries on the "Secondary statistics" dictionary
			for key, local_statistic in statistic["Secondary statistics"].items():
				# Get the current number of the current year
				current_number = current_year_statistics[key]

				# Add the additional question key to the month statistics dictionary
				local_statistic = {
					"Text": local_statistic["Text"][self.language["Small"]],
					"Old number": current_number,
					"Number": current_number + 1
				}

				# Add the statistic dictionary to the current year statistics dictionaries
				self.dictionary["Text"]["Statistics"]["Dictionary"][key] = local_statistic

				# ----- #

				# Get the current number of the current year
				current_number = current_year_statistics[key]

				# Add the additional question key to the month statistics dictionary
				local_statistic = {
					"Text": local_statistic["Text"][self.language["Small"]],
					"Old number": current_number,
					"Number": current_number + 1
				}

				# Add the statistic dictionary to the current year and current month statistics dictionaries
				self.dictionary["Text"]["Statistics"]["Month"]["Dictionary"][key] = local_statistic

		# ---------- #

		# Update the number of statistics in the current year
		self.dictionary["Text"]["Statistics"]["Number"] = len(list(self.dictionary["Text"]["Statistics"]["Dictionary"].keys()))

		# ---------- #

		# Update the number of statistics in the current month
		self.dictionary["Text"]["Statistics"]["Month"]["Number"] = len(list(self.dictionary["Text"]["Statistics"]["Month"]["Dictionary"].keys()))

		# ---------- #

		# Define the "Add to number" state
		add_to_number = True

		# If the "States" key is inside the "Text" dictionary
		# And the current state in the backup is not the first one
		if (
			"States" in self.dictionary["Text"] and
			self.dictionary["Text"]["States (backup)"]["Current state"] != self.dictionary["Text"]["States"]["Dictionary"]["1"]
		):
			# Switch the "Add to number" state to False
			add_to_number = False

		# ---------- #

		# If the "add to number" state variable is True
		# And the statistic key exists inside the current year statistics dictionary
		# And the number is not equal to zero
		if (
			add_to_number == True and
			statistic_key in current_year_statistics and
			number != 0
		):
			# Add the defined number to the defined year statistic key
			current_year_statistics[statistic_key] += number

			# Update the number inside the statistics dictionary inside the Diary Slim text dictionary
			self.dictionary["Text"]["Statistics"]["Dictionary"][statistic["Key"]]["Number"] = current_year_statistics[statistic_key]

			# ---------- #

			# Add the defined number to the defined month statistic key
			current_month_statistics[statistic_key] += number

			# Update the number inside the month statistics dictionary inside the Diary Slim text dictionary
			self.dictionary["Text"]["Statistics"]["Month"]["Dictionary"][statistic["Key"]]["Number"] = current_month_statistics[statistic_key]

			# ---------- #

			# If the old number is not the same as the new number
			old_number = self.dictionary["Text"]["Statistics"]["Dictionary"][statistic["Key"]]["Old number"]
			new_number = self.dictionary["Text"]["Statistics"]["Dictionary"][statistic["Key"]]["Number"]

			if old_number != new_number:
				# Change the "Changed statistic" to True
				self.dictionary["Text"]["Statistics"]["Changed statistic"] = True

		# ---------- #

		# If the "Text decorator" is inside the statistic dictionary
		if "Text decorator" in self.dictionary["Text"]["Statistic"]:
			# Define a shortcut for the text decorator
			text_decorator = self.dictionary["Text"]["Statistic"]["Text decorator"]

			# Get the decorator key and text
			key = text_decorator["Key"]
			decorator_text = self.Language.language_texts[key]

			# Format the text

			# Replace the decorator template
			text = text_decorator["Format"].replace("{decorator}", decorator_text)

			# If the "{response}" text template is inside the format template
			if "{response}" in text:
				# Replace the response template with the response to the first question
				text = text.replace("{response}", questions["1"]["Response"])

			# If the "{text}" template is inside the format template
			if "{text}" in text:
				# Replace the text template
				text = text.replace("{text}", statistic["Key"])

			# Update the statistic text to be the local text
			self.dictionary["Text"]["Statistics"]["Dictionary"][statistic["Key"]]["Text"] = text

			# Update the month statistic text to be the local text
			self.dictionary["Text"]["Statistics"]["Month"]["Dictionary"][statistic["Key"]]["Text"] = text

		# ---------- #

		# Define the list of parameters (statistic dictionaries to update)
		parameters = [
			self.diary_slim["Current year"]["Statistics"],
			self.diary_slim["Current year"]["Month"]["Statistics"]
		]

		# Update the statistics of the current year, with the two parameters
		self.Update_Current_Year_Statistics(*parameters)

		# ---------- #

		# If the "No text" key is inside the statistic dictionary
		if "No text" in statistic:
			# Define the text to write as an empty string
			self.dictionary["Text to write"] = ""

	def Define_Money_Text(self, number, use_extended = True):
		# Define the default text key
		text_key = "money_text"

		# If the "Use extended" state is True
		if use_extended == True:
			# Add the "_extended" text to the text key
			text_key += "_extended"

		# Add the ", type: format" text to the text key
		text_key += ", type: format"

		# Format the money number with the correct money text defined before
		number = self.Language.language_texts[text_key].format(number)

		# Return the number with the money text
		return number

	def Write(self):
		# If the "Is task" key is not inside the text dictionary
		# (That means the "Register" sub-class of the "Tasks" class was not executed and did not wrote on Diary Slim
		# So this class needs to write on it)
		# And the text to write is not empty
		if (
			"Is task" not in self.dictionary["Text"] and
			self.dictionary["Text to write"] != ""
		):
			# Add a period to the end of the text if it is not present
			if "." not in self.dictionary["Text to write"][-1]:
				self.dictionary["Text to write"] += "."

			# Show a space separator
			print()

			# Define the "Write on Diary Slim" dictionary
			dictionary = {
				"Text": self.dictionary["Text to write"]
			}

			# Write the text on Diary Slim
			Write_On_Diary_Slim_Module(dictionary)

		# If the "Is task" key is inside the text dictionary
		# And the task was registered
		if (
			"Is task" in self.dictionary["Text"] and
			self.task_dictionary["Register task"] == True
		):
			# Show a five dash space separator
			print()
			print(self.separators["5"])

			# Show the "Class being executed" and the name of the module and class
			# So the user is sure that this is the Diary Slim module, not another one
			# "Diary Slim" (in the user language)
			print()
			print(self.Language.language_texts["class_being_executed"] + ":")
			print("\t" + self.language_texts["Diary_Slim.Write"])

		# If the "Is statistic" state is True
		# And the "Statistics" key is inside the Diary Slim text dictionary
		# And the "Changed statistic" is True
		if (
			self.dictionary["Text"]["Is statistic"] == True and
			"Statistics" in self.dictionary["Text"] and
			self.dictionary["Text"]["Statistics"]["Changed statistic"] == True
		):
			# Iterate through the list of date types
			for date_type in ["Year", "Month"]:
				# Define the local statistics dictionary
				statistics = self.dictionary["Text"]["Statistics"]

				# If the date type is "Month"
				if date_type == "Month":
					statistics = self.dictionary["Text"]["Statistics"]["Month"]

				# Show the statistics, passing the date type and the local dictionary as parameters
				self.Show_Statistics(date_type, statistics)

		# If the text to write is not empty
		if self.dictionary["Text to write"] != "":
			# Open the current Diary Slim file
			self.System.Open(self.diary_slim["Current year"]["Current Diary Slim file"], verbose = False)

		# Show a five dash space separator
		print()
		print(self.separators["5"])

		# If the "Input on end" state is True
		if self.states["Input on end"] == True:
			# Ask for input before ending the execution of the class
			self.Input.Type(self.Language.language_texts["press_enter_when_you_finish_reading_the_information_summary"])