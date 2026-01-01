# Text.py

# Import some useful modules
import importlib
import os

class Text():
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.Define_Folders(object = self)

		# Define the "Switches" dictionary
		self.Define_Switches()

		# Define the texts of the module
		self.Define_Texts()

	def Import_Classes(self):
		# Define the list of modules to be imported
		modules = [
			"Define_Folders",
			"Global_Switches",
			"JSON"
		]

		# Iterate through the list of modules
		for module_title in modules:
			# Import the module
			module = importlib.import_module("." + module_title, "Utility")

			# Get the sub-class
			sub_class = getattr(module, module_title)

			# If the module title is not "Define_Folders"
			if module_title != "Define_Folders":
				# Run the sub-class to define its variable
				sub_class = sub_class()

			# Add the sub-class to the current class
			setattr(self, module_title, sub_class)

		# ---------- #

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

	def Define_Switches(self):
		# Define the "Switches" dictionary
		self.switches = {
			"Verbose": True
		}

	def Verbose(self, text, item, verbose = None, first_space = True):
		# If the "Verbose" switch is True
		# And the verbose parameter is None
		# Or the verbose parameter is True
		if (
			self.switches["Verbose"] == True and
			verbose == None or
			verbose == True
		):
			import inspect

			# Get the name of the method which ran this method (the "Verbose" one)
			runner_method_name = inspect.stack()[1][3]

			# If the "first space" parameter is True
			if first_space == True:
				# Show the first space separator
				print()

			# Show the module name (Text) and the method which ran this method (the "Verbose" one)
			print(self.module["Name"] + "." + runner_method_name + "():")

			# Show the verbose text
			print("\t" + text + ":")

			# Show the verbose item
			print("\t" + item)

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

	def Add_Leading_Zeroes(self, number):
		if int(number) <= 9:
			number = str("0" + str(number))

		return number

	def Remove_Leading_Zeroes(self, number):
		# If the number is lesser than or equal to nine
		# And the zero number is inside the number
		if (
			int(number) <= 9 and
			"0" in str(number)
		):
			# Remove the zero number
			number = str(number)[1:]

		# Return the number
		return number

	def By_Number(self, number, singular, plural):
		# If the type of the number is a list
		if type(number) == list:
			# Define it as the length of the list
			number = len(number)

		# If the number is lesser than or equal to one
		if int(number) <= 1:
			# Define the text as the singular one
			text = singular

		# If the number is greater than or equal to two
		if int(number) >= 2:
			# Define the text as the plural one
			text = plural

		# Return the defined text
		return text

	def Lower(self, text):
		return text.lower()

	def Replace(self, text, replace, with_):
		return text.replace(replace, with_)

	def Title(self, text):
		return text.title()

	def Capitalize(self, text, lower = False):
		text = list(text)

		if lower == False:
			text[0] = text[0].upper()

		if lower == True:
			text[0] = text[0].lower()

		text = "".join(text)

		return text

	def Remove_Accents(self, text):
		# Define a dictionary of letters and their accented counterparts
		accents = {
			"a": {
				"Lower": ["á", "à", "â", "ä", "ã", "å"],
				"Upper": ["Á", "À", "Â", "Ä", "Ã", "Å"]
			},
			"e": {
				"Lower": ["é", "è", "ê", "ë"],
				"Upper": ["É", "È", "Ê", "Ë"]
			},
			"i": {
				"Lower": ["í", "ì", "î", "ï"],
				"Upper": ["Í", "Ì", "Î", "Ï"]
			},
			"o": {
				"Lower": ["ó", "ò", "ô", "ö", "õ", "ø"],
				"Upper": ["Ó", "Ò", "Ô", "Ö", "Õ", "Ø"]
			},
			"u": {
				"Lower": ["ú", "ù", "û", "ü"],
				"Upper": ["Ú", "Ù", "Û", "Ü"]
			}
		}

		# List the letters in the text
		letters = list(text)

		# Iterate through the list of letters
		for letter_number, letter in enumerate(letters):
			# Iterate through the normal letters and lists inside the accents dictionary
			for normal_letter, lists in accents.items():
				# If the letter in the text is inside the list of lowercase accented letters
				if letter in lists["Lower"]:
					# Change the letter to its non-accented lowercase version
					letters[letter_number] = normal_letter

					# Exit the loop after finding a match
					break

				# If the letter in the text is inside the list of uppercase accented letters
				if letter in lists["Upper"]:
					# Change the letter to its non-accented uppercase version
					letters[letter_number] = normal_letter.upper()

					# Exit the loop after finding a match
					break

		# Define the text as the list of letters
		text = "".join(letters)

		# Return the version of the text without accents
		return text

	def Remove_Special_Characters(self, text):
		# Define a list of special characters
		special_characters = [
			"-", " ", ".", ",", ";", ":", "!", "?", "'", '"', "“", "”",
			"(", ")", "[", "]", "{", "}", "/", "&", "$", "`",
			"´", "~", "#"
		]

		 # Remove each special character from the text
		for character in special_characters:
			text = text.replace(character, "")

		# Return the text without special characters
		return text

	def Copy(self, text, verbose = True, first_space = True):
		# If the text is a list, convert it to a text
		if type(text) == list:
			text = self.From_List(text)

		# If the text is a dictionary, convert it to a text
		if type(text) == dict:
			text = self.From_Dictionary(text)

		# Import the "pyperclip" module
		import pyperclip

		# Copy the text
		pyperclip.copy(text)

		# Show the verbose text about the copied text
		self.Verbose(self.Language.language_texts["copied_text"], "[" + text + "]", verbose = verbose, first_space = first_space)

	def From_List(self, items, genders = [], language = None, lower = False, next_line = True, and_text = True, or_text = False, quotes = False):
		# Define the text initially as an empty string
		text = ""

		# Define the texts dictionary as the "language texts" dictionary of the "Language" utility class
		texts = self.Language.language_texts

		# If the "language" parameter is not None
		if language != None:
			# Define the texts dictionary as the "texts" dictionary of the "Language" utility class
			texts = self.Language.texts

		# Iterate through the indexes and items inside the list of items
		for index, item in enumerate(items):
			# Create a backup of the item
			item_backup = item

			# If the list of genders is not empty
			if genders != []:
				# Get the current gender
				gender = genders[index]

				# Define the text key for the prefix as the "of_{}" text
				text_key = "of_{}"

				# Get the prefix text using the text key
				prefix_text = texts[text_key]

				# If the "language" parameter is not None
				if language != None:
					# Get the text in the correct language
					prefix_text = prefix_text[language]

				# If the current gender is inside the prefix text
				if gender in prefix_text:
					# Get the text in the currrent gender
					prefix_text = prefix_text[gender]

			# If the item backup is the last one inside the list
			# And the "next line" parameter is False
			if (
				item_backup == items[-1] and
				next_line == False
			):
				# If the list of items is two or greater than two
				if (
					len(items) == 2 or
					len(items) > 2
				):
					# Define the separator text as an empty string
					separator_text = ""

					# If the "and text" parameter is True, define the separator text as "and"
					if and_text == True:
						separator_text = texts["and"]

					# If the "or text" parameter is True, define the separator text as "or"
					if or_text == True:
						separator_text = texts["or"]

					# If the "language" parameter is not None
					# And the separator text is not empty
					if (
						language != None and
						separator_text != ""
					):
						# Get the separator text in the correct language
						separator_text = separator_text[language]

					# If the separator is not empty, add the separator to the text first
					if separator_text != "":
						text += separator_text + " "

			# If the "lower" parameter is True, then convert the item into lowercase
			if lower == True:
				item = item.lower()

			# If the "quotes" parameter is True, add quotes around the item
			if quotes == True:
				item = '"' + item + '"'

			# If the list of genders is not empty
			if genders != []:
				# If the "language" parameter is not English
				# Or it is
				# And the item is the first one
				if (
					language != "en" or
					language == "en" and
					index == 0
				):
					# Format the item using the prefix text
					item = prefix_text.format(item)

			# If the item index is not the last one inside the list
			# And the "next line" parameter is False
			if (
				index != len(items) - 1 and
				next_line == False
			):
				# If the number of items is two
				if len(items) == 2:
					# Add a space to the end of the item
					item += " "

				# If the number of items is greater than two
				if len(items) > 2:
					# Add a comma and a space to the end of the item
					item += ", "

			# If the item index is not the last one inside the list
			# And the "next line" parameter is True
			if (
				index < len(items) - 1 and
				next_line == True
			):
				# Add a line break to the item
				item += "\n"

			# If the item backup is an empty string
			# And the "next line" parameter is True
			if (
				item_backup == "" and
				next_line == True
			):
				# Define the item as the line break
				item = "\n"

			# Add the item to the text
			text += item

		# Return the full text
		return text

	def From_Dictionary(self, dictionary, break_line = True, next_line = False):
		keys = list(dictionary.keys())
		values = list(dictionary.values())

		string = ""

		i = 0
		for value in values:
			key = keys[i]

			string += key + ": "

			if next_line == True:
				string = string[:-1] + "\n"

			string += str(value)

			if (
				key != keys[-1] and
				break_line == True
			):
				string += "\n"

				if next_line == True:
					string += "\n"

			i += 1

		return string

	def Has_Duplicates(self, item_list):
		return len(item_list) != len(set(item_list))

	def Get_Clipboard(self):
		# Import the "win32clipboard" module
		import win32clipboard

		# Open the clipboard
		win32clipboard.OpenClipboard()

		# Get the clipboard data
		data = win32clipboard.GetClipboardData()

		# Close the clipboard
		win32clipboard.CloseClipboard()

		# Return the data
		return data