# Language.py

# Import some useful module
import os
import re
import pytz
from datetime import datetime
import locale as locale_module
from encodings.aliases import aliases as encoding_aliases

class Language():
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.folders = self.Define_Folders(object = self, files = ["Languages"]).folders

		# Define the "Switches" dictionary
		self.Define_Switches()

		# Define the lists and dictionaries of the module
		self.Define_Lists_And_Dictionaries()

		# Define the languages
		self.Define_Languages()

		# Create the mapping dictionary
		self.Create_Mapping_Dictionary()

		# Create the locale dictionary
		self.Create_Locale_Dictionary()

		# Get information about the system
		self.Get_System_Information()

		# Define the texts of the module
		self.Define_Texts()

		# Define the language texts
		self.Define_Language_Texts()

		# Process the user settings
		self.Process_Settings()

	def Import_Classes(self):
		import importlib

		# Define the list of modules to be imported
		modules = [
			"Define_Folders",
			"Global_Switches"
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

			# Add the sub-class to the current module
			setattr(self, module_title, sub_class)

	def Define_Switches(self):
		# Get the "Switches" dictionary from the "Global_Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# Update the "Switches" dictionary, adding the "Folder" and "File" dictionaries
		self.switches.update({
			"Folder": {
				"Create": True,
			},
			"File": {
				"Create": True,
				"Edit": True
			}
		})

		# If the "Testing" switch is True
		if self.switches["Testing"] == True:
			# Iterate through the switch keys
			for item in ["Folder", "File"]:
				# Iterate through the switches inside the "Switches" dictionary
				for switch in self.switches[item]:
					# Define them as False
					self.switches[item][switch] = False

	def Define_Lists_And_Dictionaries(self):
		self.dictionary_separators = [
			"=",
			" = ",
			":",
			": "
		]

		self.setting_names = {
			"language": {
				"key": "language",
				"name": {
					"en": "language",
					"pt": "idioma"
				},
				"list": [
					"language",
					"Language",
					"idioma",
					"Idioma",
					"linguagem",
					"Linguagem"
				]
			},
			"text_language": {
				"key": "text_language",
				"name": {
					"en": "text_language",
					"pt": "idioma_de_texto"
				},
				"list": [
					"text language",
					"Text language",
					"idioma de texto",
					"Idioma de texto"
				]
			}
		}

	def Define_Languages(self):
		# Define the "Languages" dictionary
		self.languages = self.To_Python(self.module["Files"]["Languages"])

		# Iterate through the list of small languages
		for language in self.languages["small"]:
			# If the language is not in the "Supported" languages list
			if language not in self.languages["supported"]:
				# Remove it from the "small" list
				self.languages["small"].remove(language)

		# Define the countries dictionary
		self.countries = self.languages["Countries"]

	def Create_Mapping_Dictionary(self):
		# Define the default mapping dictionary
		self.mapping = {
			"Locales": {},
			"Encodings": {}
		}

		# Invert the keys and values of the "locale alias" dictionary
		for alias, locale_name in locale_module.locale_alias.items():
			# Remove the encoding from the locale name
			locale_name = locale_name.split(".")[0]

			# If the locale list is not present inside the "Locales" dictionary
			if locale_name not in self.mapping["Locales"]:
				# Create it
				self.mapping["Locales"][locale_name] = []

			# Add the alias to the list of aliases
			self.mapping["Locales"][locale_name].append(alias)

			# If the locale name is not inside the list of aliases
			if locale_name not in self.mapping["Locales"][locale_name]:
				# Add the locale name to the list of aliases
				self.mapping["Locales"][locale_name].append(locale_name)

		# Invert the keys and values of the "encoding aliases" dictionary
		for alias, encoding in encoding_aliases.items():
			# If the encoding list is not present inside the "Encodings" dictionary
			if encoding not in self.mapping["Encodings"]:
				# Create it
				self.mapping["Encodings"][encoding] = []

			# Add the alias to the list of aliases
			self.mapping["Encodings"][encoding].append(alias)

			# If the encoding is not inside the list of aliases
			if encoding not in self.mapping["Encodings"][encoding]:
				# Add the encoding to the list of aliases
				self.mapping["Encodings"][encoding].append(encoding)

	def Create_Locale_Dictionary(self):
		# Define the default locale dictionary
		self.locale = {
			"Locale": {
				"Original": locale_module.getdefaultlocale(),
				"Mapped": "",
				"Locale": "",
				"List": [],
				"Information": {}
			},
			"Encoding": {
				"Original": "",
				"Mapped": "",
				"List": []
			},
			"Module": locale_module
		}

		# Updated the mapped lists of locales and encodings based on the original locale
		self.Updated_Mapped_Lists(self.locale["Locale"]["Original"])

		# Define the original encoding
		self.locale["Encoding"]["Original"] = self.locale["Locale"]["Original"][1]

		# Set the locale using the mapped locale

		# Iterate through the list of locales
		for locale in self.locale["Locale"]["List"]:
			# Iterate through the list of encodings
			for encoding in self.locale["Encoding"]["List"]:
				# Map the two
				mapped = locale + "." + encoding

				# Try to set the locale
				try:
					locale_module.setlocale(locale_module.LC_ALL, mapped)

					# ----- #

					# Update the full locale (locale + encoding)
					self.locale["Locale"]["Mapped"] = mapped

					# ----- #

					# Update the mapped encoding
					self.locale["Encoding"]["Mapped"] = encoding

					# ----- #

					# Update the locale
					self.locale["Locale"]["Locale"] = locale

				except locale_module.Error as e:
					pass

		# Update the locale information
		self.locale["Locale"]["Information"] = locale_module.localeconv()

		# Update the "Module" key
		self.locale["Module"] = locale_module

	def Updated_Mapped_Lists(self, locale):
		# Get the list of locales
		locales = self.mapping["Locales"][locale[0]]

		# Fill the locales list
		self.locale["Locale"]["List"] = locales

		# ----- #

		# Get the list of encodings
		encodings = self.mapping["Encodings"][locale[1]]

		# Fill the encodings list
		self.locale["Encoding"]["List"] = encodings

	def Get_System_Information(self):
		# Import some useful modules
		import platform
		import pathlib
		import ctypes
		from tzlocal import get_localzone

		# ---------- #

		# Define the "system" dictionary
		self.system = {
			"Name": platform.system(), # The name of the system
			"Resolution": {} # The resolution of the system
		}

		# Get the "user32" class
		user32 = ctypes.windll.user32

		# Add the width
		self.system["Resolution"]["Width"] = str(user32.GetSystemMetrics(0))

		# Add the height
		self.system["Resolution"]["Height"] = str(user32.GetSystemMetrics(1))

		# Join the two dimensions
		self.system["Resolution"]["Dimensions"] = self.system["Resolution"]["Width"] + "x" + self.system["Resolution"]["Height"]

		# ---------- #

		# Define the "user" dictionary
		self.user = {
			# Get the user name, folder, and timezone
			"Name": str(pathlib.Path.home().name), 
			"Folder": self.Sanitize(str(pathlib.Path.home())),
			"Timezone": get_localzone(),

			# Get the user (system) locale
			"Locale": self.locale,

			# Define the user "Language" dictionary
			"Language": {
				"Small": "",
				"With country": "",
				"Full": ""
			},

			# Define the user "Country" dictionary
			"Country": {
				
			}
		}

		# ---------- #

		# Define a shortcut to the user timezone
		user_timezone = str(self.user["Timezone"])

		# Define a default date
		date = datetime.now()

		# Remove the microsecond from the date object
		date = date.replace(microsecond = 0)

		# Define the date object in the user timezone
		user_timezone_date = date.astimezone(self.user["Timezone"])

		# Update the user "Timezone" dictionary
		self.user["Timezone"] = {
			"String": user_timezone,
			"Name": user_timezone_date.strftime("%Z"),
			"UTC offset": user_timezone_date.strftime("%z"),
			"Timezone information": pytz.timezone(user_timezone)
		}

		# ---------- #

		# Define a shortcut to the user locale
		locale_shortcut = self.user["Locale"]["Locale"]["Original"]

		# Define the "Small" and "With country" language keys
		self.user["Language"]["Small"] = locale_shortcut[0].split("_")[0]
		self.user["Language"]["With country"] = locale_shortcut[0]

		# Get the country
		country = self.user["Language"]["With country"].split("_")[1]

		# Define the country code
		self.user["Country"]["Code"] = country

		# Get the country name
		country_name = self.languages["Countries"][country]

		# Define the country name
		self.user["Country"]["Name"] = country_name

		# Define a shortcut to the small language
		small_language = self.user["Language"]["Small"]

		# Define the full language keys
		self.user["Language"]["Full"] = self.languages["full"][small_language]
		self.user["Language"]["Full translated"] = self.languages["full_translated"][small_language]

		# ---------- #

		# Define a shortcut to the user "Language" dictionary
		self.language = self.user["Language"]

	def Sanitize(self, path):
		path = os.path.normpath(path).replace("\\", "/")

		if (
			"/" not in path[-1] and
			os.path.splitext(path)[-1] == ""
		):
			path += "/"

		return path

	def Current_Folder(self, file = None):
		# If the file parameter is None, define the file as "__file__"
		if file == None:
			file = __file__

		# Get the folder from the module file
		folder = self.Sanitize(os.path.dirname(file))

		# Return the folder
		return folder

	def Verbose(self, text, item):
		if self.switches["Verbose"] == True:
			import inspect

			print()
			print(inspect.stack()[1][3] + "():")
			print("\t" + text + ":")
			print("\t" + item)

	def File_Exists(self, file):
		# Sanitize the file path
		file = self.Sanitize(file)

		# Checks if the file exists and returns True if it does or False if it does not
		return os.path.isfile(file)

	def Folder_Exists(self, folder):
		# Sanitize the folder path
		folder = self.Sanitize(folder)

		# Checks if the folder exists and returns True if it does or False if it does not
		return os.path.isdir(folder)

	def Create(self, item = None, text = None):
		if item == None:
			item = self.Type(text)

		item = self.Sanitize(item)

		if os.path.splitext(item)[-1] == "":
			if (
				self.switches["Folder"]["Create"] == True and
				self.Folder_Exists(item) == False
			):
				os.mkdir(item)

		if os.path.splitext(item)[-1] != "":
			if (
				self.switches["File"]["Create"] == True and
				self.File_Exists(item) == False
			):
				create = open(item, "w", encoding = "utf8")
				create.close()

		return item

	def Contents(self, file):
		file = self.Sanitize(file)

		contents = {
			"lines": [],
			"lines_none": [None],
			"string": "",
			"size": 0,
			"length": 0
		}

		if self.File_Exists(file) == True:
			contents["string"] = open(file, "r", encoding = "utf8").read()
			contents["size"] += os.path.getsize(file)

			for line in open(file, "r", encoding = "utf8").readlines():
				line = line.replace("\n", "")

				contents["lines"].append(line)
				contents["lines_none"].append(line)

			contents["length"] = len(contents["lines"])

		if self.File_Exists(file) == False:
			self.Verbose(self.language_texts["this_file_does_not_exists"], file)

		return contents

	def Split_Dictionary(self, lines = None, dict_ = None, text = None, separator = ": ", next_line = False, convert = None):
		if next_line == False:
			split = text.split(separator)

			key = split[0]

			if key != "":
				if " " in key[-1]:
					key = key[:-1]

				if " " in key[0]:
					key = key[1:]

			value = split[text.count(separator)]

			if convert != None:
				value = convert(value)

			if text.count(separator) == 2:
				value = split[1] + separator + value

			if text.count(separator) >= 3:
				split.pop(0)
				value = ""

				for item in split:
					value += item

					if item != split[-1]:
						value += separator

			if separator in key:
				key = key.replace(separator, "")

		if next_line == True:
			i = 0
			for line in lines:
				try:
					if separator in line and lines[i + 1] != "":
						key = line.replace(separator, "")

						value = lines[i + 1]

						if convert != None:
							value = convert(value)

						dict_[key] = value

				except:
					pass

				i += 1

		if next_line == False:
			return [key, value]

	def File_Dictionary(self, file, dictionary_separators = ": ", next_line = False, convert = None, true_or_false = False):
		if type(dictionary_separators) == str:
			dictionary_separators = [dictionary_separators]

		dictionary = {}

		for line in self.Contents(file)["lines"]:
			for dictionary_separator in dictionary_separators:
				if re.findall(r"\b" + dictionary_separator + r"\b", line, re.IGNORECASE):
					key, value = self.Split_Dictionary(text = line, separator = dictionary_separator)

					if convert != None:
						value = convert(value)

					if true_or_false == True:
						if value == "True":
							value = True

						if value == "False":
							value = False

					dictionary[key] = value

				elif dictionary_separator in line:
					key, value = self.Split_Dictionary(text = line, separator = dictionary_separator)

					if convert != None:
						value = convert(value)

					dictionary[key] = value

		return dictionary

	def Edit(self, file, text, mode):
		file = self.Sanitize(file)

		contents = self.Contents(file)
		length = contents["length"]

		if self.File_Exists(file) == True:
			if (
				self.switches["File"]["Edit"] == True and
				contents["string"] != text
			):
				edit = open(file, mode, encoding = "UTF8")
				edit.write(text)
				edit.close()

				self.Verbose(self.language_texts["file"].title() + " " + self.language_texts["edited, masculine"], file)

	def Select(self, options, language_options = None, show_text = None, select_text = None, function = False, first_space = True):
		if show_text == None:
			show_text = self.language_texts["options, title()"] + ": "

		if select_text == None:
			select_text = self.language_texts["select_an_item_from_the_list"] + ": "

		if first_space == True:
			print()

		print(show_text)

		list_ = options.copy()

		if language_options != None:
			list_ += language_options.copy()

		numbers = []

		i = 0
		for option in options:
			if language_options != None:
				option = language_options[i]

				if type(option) == str:
					list_.append(option.lower())
					list_.append(option[0].lower())

			print("[" + str(i + 1) + "]" + " - " + option)

			numbers.append(i)
			numbers.append(str(i))

			i += 1

		letters = []

		for option in options:
			if type(option) == str:
				letters.append(option[0].lower())

		list_ += letters
		list_ += numbers

		print()

		option = ""

		while option in ["", " "]:
			option = input(select_text)

		found_option = False

		try:
			option = int(option)
			option_number = option - 1

			try:
				option = options[option_number]
				found_option = True

			except IndexError:
				option = 1000

				while option not in list_:
					try:
						option = int(input(select_text))

					except ValueError:
						option = str(option)

				option_number = option - 1
				option = options[option_number]
				found_option = True

		except ValueError:
			option = str(option)

			while option not in list_:
				option = input(select_text)

				try:
					option = int(option)
					option_number = option - 1

				except ValueError:
					option = str(option)

		possible_options = [option]

		if type(option) == str and found_option == False:
			possible_options.extend([
				str(option),
				str(option.lower()),
				str(option.title()),
				str(option.capitalize()),
				str(option.lower().title()),
				str(option.title()),
				str(option.capitalize())
			])

		i = 0
		for possible_option in possible_options:
			if type(possible_option) == str and found_option == False:
				if language_options != None:
					for option_ in language_options:
						if re.findall(possible_option, option_, re.IGNORECASE) != []:
							option = option_

							found_option = True

				if language_options == None:
					for option_ in options:
						if re.findall(possible_option, option_, re.IGNORECASE) != []:
							option = option_

							found_option = True
			i += 1

		if type(option) == str:
			i = 0
			for option_ in options:
				if option == option_:
					option_number = i

				i += 1

		dictionary = {
			"option": option,
			"language_option": option,
			"number": option_number,
		}

		if language_options != None:
			dictionary["language_option"] = language_options[dictionary["number"]]

		if found_option == True:
			print()
			print(self.language_texts["you_selected_this_option"] + ":")

			if language_options != None and str(option) != dictionary["language_option"]:
				print("\t" + dictionary["language_option"])
				print("\t" + str(option))

			if language_options == None or str(option) == dictionary["language_option"]:
				print(str(option))

			if function == True and type(option) in [function, type]:
				option()

		return dictionary

	def Define_Yes_Or_No(self, response):
		if response in ["Yes", self.language_texts["yes, title()"]]:
			return True

		if response in ["No", self.language_texts["no, title()"]]:
			return False

	def Yes_Or_No(self, question, convert_to_text = False, first_space = True):
		options = [
			self.language_texts["yes, title()"],
			self.language_texts["no, title()"],
		]

		if type(question) == dict:
			question = self.Item(question)

		option = self.Select(options, show_text = question + "?", select_text = self.language_texts["select_{}_or_{}_(number_or_word)"] + ": ", first_space = first_space)["option"]

		option = self.Define_Yes_Or_No(option)

		if convert_to_text == True:
			if option == True:
				option = self.language_texts["yes, title()"]

			if option == False:
				option = self.language_texts["no, title()"]

		return option

	def Type(self, text = None, accept_enter = True, next_line = False, first_space = True):
		if text == None:
			text = self.language_texts["type_or_paste_the_text"] + ": "

		if type(text) == dict:
			text = self.Item(text) + ": "

		if first_space == True:
			print()

		typed = ""

		if next_line == False:
			if accept_enter == True:
				typed = input(text)

			if accept_enter == False:
				while typed == "":
					typed = input(text)

		if next_line == True:
			print(text)

			if accept_enter == True:
				typed = input()

			if accept_enter == False:
				while typed == "":
					typed = input()

		return typed

	def Item(self, texts, user_language = None):
		if user_language == None:
			user_language = self.language["Small"]

		if user_language in texts:
			return texts[user_language]

		if user_language not in texts:
			language_texts = {}

			list_ = []

			for key in texts:
				language_texts[key] = texts[key]

				if type(language_texts[key]) == dict and user_language in language_texts[key]:
					if "masculine" in language_texts[key][user_language] or "feminine" in language_texts[key][user_language]:
						list_.append(True)

			add_gender_texts = False

			if len(list_) != 0:
				add_gender_texts = True

			del list_

			for key in texts:
				language_texts[key] = texts[key]

				if type(texts[key]) == dict and user_language in texts[key]:
					language_texts[key] = texts[key][user_language]

				language_texts[key + ", masculine"] = language_texts[key]
				language_texts[key + ", feminine"] = language_texts[key]

				if add_gender_texts == True and type(language_texts[key]) == dict:
					if "masculine" in language_texts[key]:
						language_texts[key + ", masculine"] = language_texts[key]["masculine"]

					if "feminine" in language_texts[key]:
						language_texts[key + ", feminine"] = language_texts[key]["feminine"]

					if "masculine" in language_texts[key]:
						language_texts[key] = language_texts[key]["masculine"]

			return language_texts

	def Title(self, texts):
		local_texts = {}
		local_texts.update(texts)

		for text in texts:
			if type(texts[text]) not in [str, list]:
				for language in self.languages["small"]:
					if language in texts[text]:
						if type(texts[text][language]) not in [list, dict]:
							local_texts[text + ", title()"] = {}

						if type(texts[text][language]) == dict:
							if "masculine" in texts[text][language]:
								local_texts[text + ", title(), masculine"] = {}

							if "feminine" in texts[text][language]:
								local_texts[text + ", title(), feminine"] = {}

		for text in texts:
			if type(texts[text]) not in [str, list]:
				for language in self.languages["small"]:
					if language in texts[text]:
						if type(texts[text][language]) not in [list, dict]:
							local_texts[text + ", title()"][language] = texts[text][language].title()

						if type(texts[text][language]) == dict:
							if "masculine" in texts[text][language]:
								local_texts[text + ", title(), masculine"][language] = local_texts[text][language]["masculine"]

							if "feminine" in texts[text][language]:
								local_texts[text + ", title(), feminine"][language] = local_texts[text][language]["feminine"]

							if text in local_texts and "masculine" in texts[text][language]:
								local_texts[text][language] = local_texts[text][language]["masculine"]

							elif text + ", title()" in local_texts and "masculine" in texts[text][language]:
								local_texts[text + ", title()"][language] = local_texts[text][language]["masculine"]

		return local_texts

	def List(self, texts, key, names):
		key = key + ", type: list"

		texts[key] = {}

		for language in self.languages:
			texts[key][language] = []

			for text in names:
				texts[key][language].append(texts[text][language])

		return texts

	def Dictionary(self, texts, key, languages):
		local_texts = {}
		local_texts.update(texts)

		new_key = key + ", type: dict, " + languages[0] + ": " + languages[1]

		local_texts[new_key] = {}

		i = 0
		for text in texts[key + ", type: list"][languages[0]]:
			local_texts[new_key][text] = local_texts[text.lower().replace(" ", "_")][languages[1]].title()

			i += 1

		return local_texts

	def Format(self, texts, key, text = "", mixed_text = "", languages = [], separator = " - ", title = False):
		local_texts = {}
		local_texts.update(texts)

		text_key = key

		if ", type: " in key:
			text_key = text_key.split(", ")[0]

		if ", type: " not in key:
			key += ", type: format"

		if text != "":
			local_texts[key] = {}

			for language in self.languages:
				local_texts[key][language] = text.replace("[language]", local_texts[text_key][language])

				if title == True:
					local_texts[key][language] = local_texts[key][language].title()

		if languages != []:
			key += ", " + languages[0] + separator + languages[1]

			local_texts[key] = mixed_text

			local_texts[key] = local_texts[key].replace("[1]", local_texts[text_key][languages[0]])
			local_texts[key] = local_texts[key].replace("[2]", local_texts[text_key][languages[1]])

			if title == True:
				local_texts[key] = local_texts[key].title()
				local_texts[key] = local_texts[key].title()

		return local_texts

	def Mix(self, texts, key, languages, separator = " - ", item = False, title = False):
		local_texts = {}
		local_texts.update(texts)

		joined_languages = languages[0] + separator + languages[1]

		key_text = key

		if ", type: " in key:
			key_text = key_text.split(", ")[0]

		if title == True:
			key_text += ", title()"

		key_text += ", " + joined_languages

		if item == False:
			local_texts[key_text] = []

		if type(texts[key][languages[0]]) == list:
			i = 0
			for text_backup in texts[key][languages[0]]:
				text = text_backup

				if text_backup != texts[key][languages[1]][i]:
					text = text_backup + separator + texts[key][languages[1]][i]

				if title == True:
					text = text.title()

				if item == False:
					local_texts[key_text].append(text)

				if item == True:
					key_text = text_backup.lower().replace(" ", "_")

					if title == True:
						key_text += ", title()"

					key_text += ", " + joined_languages

					local_texts[key_text] = text

				i += 1

		if type(texts[key][languages[0]]) == str:
			text = texts[key][languages[0]] + separator + texts[key][languages[1]]

			if title == True:
				text = text.title()

			key_text = texts[key][languages[0]].lower().replace(" ", "_")

			if title == True:
				key_text += ", title()"

			key_text += ", " + joined_languages

			local_texts[key_text] = text

		return local_texts

	def Split(self, text, languages, separator = ", ", user_language = None):
		if user_language == None:
			user_language = self.language["Small"]

		i = 0
		for language in languages:
			if language == user_language:
				language_number = i

			i += 1

		return text.split(separator)[language_number]

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.To_Python(self.module["Files"]["Texts"])

		# Define the "separators" dictionary
		self.separators = {}

		# Create separators from one to ten characters
		for number in range(1, 11):
			# Define the empty string
			string = ""

			# Add separators to it
			while len(string) != number:
				string += "-"

			# Add the string to the Separators dictionary
			self.separators[str(number)] = string

	def Define_Language_Texts(self):
		self.language_texts = self.Item(self.texts)

		for language_type in self.languages["types"]:
			language_type = language_type.lower().replace(" ", "_")

			self.language_texts["your_" + language_type + "_is"] = self.language_texts["your_{}_is"].format(self.Item(self.texts[language_type]))

		self.settings_file = self.folders["Apps"]["root"] + self.language_texts["settings"].capitalize() + ".json"

		if self.File_Exists(self.settings_file) == False:
			self.Create(self.settings_file)
			self.Edit(self.settings_file, self.From_Python({}), "w")

	def Process_Settings(self):
		# Define the default root settings dictionary
		self.settings = {}

		# If the settings file exists
		if self.File_Exists(self.settings_file) == True:
			# Read the "Settings.json" file to get the settings dictionary
			settings = self.To_Python(self.settings_file)

			# Iterate through the setting names inside the "setting names" list
			for setting_name in self.setting_names:
				possible_setting_names = self.setting_names[setting_name]["list"]

				for possible_setting_name in possible_setting_names:
					if possible_setting_name in settings:
						setting = settings[possible_setting_name]

						# If the setting name is "Language"
						if setting_name == "Language":
							# Get the locale based on the setting
							locale_shortcut = setting

							# Define the "Language" dictionary keys
							self.system["Language"]["Small"] = locale_shortcut[0].split("_")[0]
							self.system["Language"]["With country"] = locale_shortcut[0]
							self.system["Language"]["Full"] = self.languages["full"][self.system["Language"]["Small"]]

						self.settings[setting_name.replace("_", " ").capitalize()] = setting

						key = self.setting_names[setting_name]["name"][self.language["Small"]].replace("_", " ").capitalize()

						self.settings[key] = setting

			self.Define_Language_Texts()

			# Update the "Settings.json" file with the new settings dictionary
			self.Edit(self.settings_file, self.From_Python(self.settings), "w")

			# ----- #

			# Create 
			settings = {
				"Language": self.settings["Language"]
			}

			self.global_settings_file = self.folders["Apps"]["root"] + "Settings.json"

			self.Create(self.global_settings_file)
			self.Edit(self.global_settings_file, self.From_Python(settings), "w")

		# If the settings file does not exist
		if self.File_Exists(self.settings_file) == False:
			texts = {
				"en": "Default settings file not found, do you want to select settings",
				"pt": "Arquivo padrão de configurações não encontrado, você quer selecionar configurações",
			}

			option = self.Yes_Or_No(texts)

			if option == True:
				self.Create_Settings()

	def Create_Settings(self):
		# Create folder
		folder = self.Create(None, self.texts["type_or_paste_the_folder_where_you_want_to_create_the_settings_file"])

		settings_file = folder + self.language_texts["settings"].title() + ".txt"

		# Create file
		self.Create(settings_file)

		# Ask for each setting
		for setting_name in self.setting_names:
			setting_information = self.setting_names[setting_name]

			language_setting_name = setting_information["name"][self.app_settings["Language"]]

			option = self.Select(self.languages["small"], show_text = self.language_texts["languages"].title() + ":", select_text = self.language_texts["select_one_{}_(number_or_word), masculine"].format(language_setting_name) + ": ")

			self.Edit(settings_file, setting_name.title() + ": " + option, "a")

		self.Read_Settings_File()

	def From_Python(self, item):
		import json

		return json.dumps(item, indent = 4, ensure_ascii = False)

	def To_Python(self, file):
		import json

		file = self.Sanitize(file)

		dictionary = json.load(open(file, encoding = "utf8"))

		return dictionary

	def Copy(self, text):
		import pyperclip

		pyperclip.copy(text)

		self.Verbose(self.language_texts["copied_text"], text)

	def Create_Language_Text(self):
		template = '''"[key]": {
		[input]
	},'''

		empty_json = self.Yes_Or_No(self.language_texts["is_the_json_file_empty"])

		if empty_json == False:
			template = template.replace('"[key]', ',\n\t"[key]')
			template = template.replace('},', "}")

		if empty_json == True:
			template = "{\n\t" + template + "\n}"

		text = template

		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language][self.app_settings["Language"]]

			typed = self.Type(self.language_texts["type_the_text_in_{}"].format(translated_language) + ": ", accept_enter = False, next_line = True)

			if language == "en":
				key = typed.lower().replace(" ", "_")

				for item in [":", '"', "'", "\n", "."]:
					key = key.replace(item, "")

				if " " not in typed and typed[0].isupper() == True:
					key += ", title()"

				text = text.replace("[key]", key)

			typed = typed.replace('"', '\\"')

			language_text = '"' + language + '": "' + typed + '"'

			if language != self.languages["small"][-1]:
				language_text += "," + "\n\t\t[input]"

			text = text.replace("[input]", language_text)

		self.Copy(text)

		return text

	def Show_User_Information(self):
		# Show the class and method names and the "Showing user information" text
		print(self.language_texts["language_class"] + ", " + self.language_texts["show_user_information_method"] + ":")
		print("\t" + self.language_texts["showing_user_information"] + "...")
		print()

		# Define a quotes template
		quotes = '"{}"'

		# ---------- #

		# Show the user name
		print(self.language_texts["username, title(), type: self"] + ":")
		print("\t" + self.user["Name"])
		print()

		# Show the user folder
		print(self.language_texts["user_folder"] + ":")
		print("\t" + self.user["Folder"])
		print()

		# ---------- #

		# Show the user timezone
		print(self.language_texts["user_timezone"] + ":")

		# Show the timezone string
		print("\t" + self.language_texts["text, title()"] + ":")
		print("\t" + quotes.format(self.user["Timezone"]["String"]))
		print()

		# Show the timezone name
		print("\t" + self.language_texts["name, title()"] + ":")
		print("\t" + quotes.format(self.user["Timezone"]["Name"]))
		print()

		# Show the UTC offset
		print("\t" + self.language_texts["difference_from_utc"] + ":")

		utc_offset = self.user["Timezone"]["UTC offset"]

		if "-" in utc_offset:
			utc_offset = "UTC" + utc_offset

		print("\t" + utc_offset)
		print()

		# Show the timezone information
		print("\t" + self.language_texts["timezone_information"] + ":")
		print("\t" + str([self.user["Timezone"]["Timezone information"]]))
		print()

		# ---------- #

		# Show the user language information
		print(self.language_texts["user_language"] + ":")

		# Show the small language
		print("\t" + self.language_texts["small, title()"] + ":")
		print("\t" + quotes.format(self.user["Language"]["Small"]))
		print()

		# Show the language with country
		print("\t" + self.language_texts["with_country"] + ":")
		print("\t" + quotes.format(self.user["Language"]["With country"]))
		print()

		# Show the full language
		print("\t" + self.language_texts["full, title()"] + ":")
		print("\t" + quotes.format(self.user["Language"]["Full"]))
		print()

		# Show the full language translated
		print("\t" + self.language_texts["full_translated"] + ":")

		# Iterate through the list of small languages
		for language in self.languages["small"]:
			# If the language is not the user language
			if language != self.language["Small"]:
				# Get the translated language
				# (First the current language then the user language)
				translated_language = self.languages["full_translated"][language][self.language["Small"]]

				# Get the translated user language
				# (First the user language then the current language)
				translated_user_language = self.languages["full_translated"][self.language["Small"]][language]

				# Show the current language
				print("\t\t" + translated_language + ":")

				# Show the user language but translated to the current language
				print("\t\t" + quotes.format(translated_user_language))
				print()

		# ---------- #

		# Show the user country code
		print(self.language_texts["country_code"] + ":")
		print("\t" + quotes.format(self.user["Country"]["Code"]))
		print()

		# Show the user country name
		print(self.language_texts["country_name"] + ":")
		print("\t" + quotes.format(self.user["Country"]["Name"][self.language["Small"]]))
		print()

		# ---------- #

		# Show the system information
		print(self.language_texts["system_information"] + ":")

		# Show the system name
		print("\t" + self.language_texts["name, title()"] + ":")
		print("\t" + quotes.format(self.system["Name"]))
		print()

		# Show the system resolution
		print(self.language_texts["resolution, title()"] + ":")

		# Iterate through the list of sizes
		for key in ["Width", "Height", "Dimensions"]:
			# Define a text key
			text_key = key

			# If the size is "Dimensions"
			if key == "Dimensions":
				# Update the text key to "full"
				text_key = "Full"

			# Get the text for the size
			text = self.language_texts[text_key.lower() + ", title()"]

			# Get the size
			size = self.system["Resolution"][key]

			# If the size is not "Dimensions"
			if key != "Dimensions":
				# Add "px" to the size
				size += "px"

			# Show the text and the size
			print("\t" + text + ":")
			print("\t" + size)

			# If the key is not the last one
			if key != "Dimensions":
				print()

	def Text_From_List(self, list_, next_line = True, separator = ""):
		string = ""

		i = 0
		for item in list_:
			string += item

			if i != len(list_) - 1:
				if separator != "":
					string += separator

				if next_line == True:
					string += "\n"

			i += 1

		return string

	# Make the text difference between the text inside the file and the text to be written
	def Text_Difference(self, file_text, text_lines_to_write, filters = {}):
		# Get the lines list if the file text is a dictionary
		if type(file_text) == dict:
			file_text = file_text["lines"]

		# Get the lines list if the file text is a string
		if type(text_lines_to_write) == str:
			text_lines_to_write = text_lines_to_write.splitlines()

		settings = filters

		# Define the difference dictionary
		dictionary = {
			"Difference": {
				"Lines": [],
				"Text": ""
			},
			"Additions": 0,
			"Changes": 0,
			"Deletions": 0
		}

		# Get the length of the lines to write and the number of lines inside the file
		text_lines_number = len(text_lines_to_write)
		file_lines_number = len(file_text)

		difference_number = abs(text_lines_number - file_lines_number)

		# Define the line text and template
		line_text = self.language_texts["line, title()"]

		tab = "\t\t"

		template = tab + "{} " + line_text + " {}: [{}"

		added_space = False

		# Define the default settings dictionary
		self.default_settings = {
			"Filters": {
				"Deletions mode": False,
				"Full text": False
			},
			"Separators": True
		}

		# Check the settings dictionary
		for key, default in self.default_settings.items():
			if key not in settings:
				settings[key] = default

		i = 0
		line_number = 0
		for line in text_lines_to_write:
			add = False

			# If the "Separators" filter is on
			# And the "i" number is zero
			if (
				settings["Separators"] == True and
				i == 0
			):
				# Add a text to start the changes text
				dictionary["Difference"]["Lines"].append("")
				dictionary["Difference"]["Lines"].append(tab + "-----")
				dictionary["Difference"]["Lines"].append("")
				dictionary["Difference"]["Lines"].append(tab + self.language_texts["changes"].title() + ":")
				dictionary["Difference"]["Lines"].append("")
				dictionary["Difference"]["Lines"].append(tab + "---")

			# If the number of file lines is greater than or equal to number of text lines
			# Or the number of file lines is lesser than the number of text lines
			if (
				len(file_text) >= len(text_lines_to_write) or
				len(file_text) < len(text_lines_to_write)
			):
				# If the number of file lines is greater than or equal to number of text lines
				if len(file_text) >= len(text_lines_to_write):
					# If the "Full text" filter is off
					if settings["Filters"]["Full text"] == False:
						# If the current file line is not the same as the current text line
						# Or the line is not inside the file lines list
						if (
							file_text[i] != text_lines_to_write[i] or
							line not in file_text
						):
							# Add the line to the text difference list
							add = True

					# If the "Full text" filter is on
					# And the current file line is not the same as the current text line
					if (
						settings["Filters"]["Full text"] == True and
						file_text[i] != text_lines_to_write[i]
					):
						# Add the line to the text difference list
						add = True

					# If the line is empty
					if line == "":
						# Add the line to the text difference list
						add = True

				# If the number of file lines is lesser than the number of text lines
				if len(file_text) < len(text_lines_to_write):
					# If the current line is empty
					# Or the "i" number plus one is greater than or equal to the number of file text lines
					if (
						line == "" or
						(i + 1) >= len(file_text)
					):
						# Add the line to the text difference list
						add = True

					# If the "Full text" filter is off
					# And the line is not inside the file lines list
					if (
						settings["Filters"]["Full text"] == False and
						line not in file_text
					):
						# Add the line to the text difference list
						add = True

					# If the "Full text" filter is on
					# And the "i" number plus one is lesser than or equal to the number of file text lines
					if (
						settings["Filters"]["Full text"] == True and
						(i + 1) <= len(file_text)
					):
						# Add the line to the text difference list
						add = True

				# Add the line to the text difference list
				if add == True:
					# Create the number text
					number_text = str(i + 1)

					# If the number of lines to write are lesser than the number of lines inside the file
					if len(text_lines_to_write) < len(file_text):
						# Add one to the number of lines inside the file
						file_lines_number += 1

						# Change the number text to the number of lines inside the file
						number_text = str(file_lines_number)

					# While the length of the number text is lesser than the number of lines to write
					while len(number_text) < len(str(text_lines_number)):
						# Add spaces to the number text
						number_text = " " + number_text

					previous_line = dictionary["Difference"]["Lines"][-1]

					if previous_line == "":
						previous_line = dictionary["Difference"]["Lines"][-2]

					self.testing = False

					if self.testing == True:
						print()
						print("-----")
						print()
						print("[" + str(i - 1))
						print("[" + str(i))
						print("[" + str(i + 1))
						print("[" + str(line_number))
						print("[" + str(int(number_text) - 1))
						print()
						print(" - [" + previous_line)

					# If the "i" number is not in the previous line
					# And the "number_text" number is not in the previous line
					if (
						str(i) not in previous_line and
						str(int(number_text) - 1) not in previous_line
					):
						# Add a space to separate the change lines
						dictionary["Difference"]["Lines"].append("")

					# If the "Deletions mode" filter is on
					# And the "i" number plus one is lesser than or equal to the number of lines inside the file
					if (
						settings["Filters"]["Deletions mode"] == True and
						(i + 1) <= len(file_text)
					):
						# If the "i" number plus one is equal to the number of lines inside the file
						if (i + 1) == len(file_text) and len(text_lines_to_write) >= len(file_text):
							# Remove one from the line number
							line_number -= 1

						file_line = file_text[line_number]

						# Make the old line text with the "-" (minus) symbol
						old_line = template.format("-", number_text, file_line)

						# Add the old line text to the text difference list
						dictionary["Difference"]["Lines"].append(old_line)

						# Add to the deletions number
						dictionary["Deletions"] += 1

					symbol = "+"

					# If the "i" number plus one is lesser than or equal to the number of lines inside the file
					if (i + 1) <= len(file_text):
						# If the "Deletions mode" filter is off
						if settings["Filters"]["Deletions mode"] == False:
							symbol = "~"

						# Add to the changes number
						dictionary["Changes"] += 1

					# Make the new line text with the "+" (plus) symbol
					new_line = template.format(symbol, number_text, line)

					if self.testing == True:
						print(" - [" + new_line)
						input()

					# Add the new line text to the text difference list
					dictionary["Difference"]["Lines"].append(new_line)

					# If the "Deletions mode" filter is on
					# And the "i" number plus one is lesser than or equal to the number of lines inside the file
					# And the previous line is not a space
					if (
						settings["Filters"]["Deletions mode"] == True and
						(i + 1) <= len(file_text) and
						dictionary["Difference"]["Lines"][-1] != ""
					):
						# Add a space to separate the change lines
						dictionary["Difference"]["Lines"].append("")

					# If the "i" number plus one is lesser than or equal to the number of lines inside the file
					# And the number of lines to write is greater than or equal to the number of lines inside the file
					if (
						(i + 1) <= len(file_text) and
						len(text_lines_to_write) >= len(file_text)
					):
						# Add to the additions number
						dictionary["Additions"] += 1

			# If the "Separators" filter is on
			# And the "added_space" is False
			# And the "i" number plus one is lesser than or equal to the number of lines inside the file
			# And the "Additions" number is not zero
			if (
				settings["Separators"] == True and
				added_space == False and
				(i + 1) == len(file_text) and
				dictionary["Additions"] != 0
			):
				# Add a text to separate the lines

				# If the "Deletions mode" filter is off
				if settings["Filters"]["Deletions mode"] == False:
					dictionary["Difference"]["Lines"].append("")

				dictionary["Difference"]["Lines"].append(tab + "-----")
				dictionary["Difference"]["Lines"].append("")
				dictionary["Difference"]["Lines"].append(tab + self.language_texts["additions"].title() + ":")
				dictionary["Difference"]["Lines"].append("")
				dictionary["Difference"]["Lines"].append(tab + "---")

				added_space = True

			i += 1
			line_number += 1

		# Make the number of additions and deletions text
		numbers = []

		# Define the text template
		text_template = ""

		# Add the "changes" number and text if the changes are not zero
		if dictionary["Additions"] != 0:
			numbers.append(dictionary["Additions"])

			# Get the singular or plural text
			text = self.language_texts["addition"]

			if dictionary["Additions"] > 1:
				text = self.language_texts["additions"]

			# Add the " and {} additions" text
			text_template += "[{} " + text + "]"

		# Add the "changes" number and text if the changes are not zero
		if dictionary["Changes"] != 0:
			numbers.append(dictionary["Changes"])

			# Remove the "]" character of the text template
			if text_template != "" and "]" in text_template[-1]:
				text_template = text_template[:-1]

			# Get the singular or plural text
			text = self.language_texts["change"]

			if dictionary["Changes"] > 1:
				text = self.language_texts["changes"]

			# If the additions are not zero
			# Add the " and " text
			if dictionary["Additions"] != 0:
				text_template += " " + self.language_texts["and"] + " "

			# Else, add the "[" text
			# (Difference has only changes)
			else:
				text_template += "["

			# Add the " and {} changes" text
			text_template += "{} " + text

			# Re-add the "]" character
			text_template += "]"

		# Add the "deletions" number and text if the deletions are not zero
		if dictionary["Deletions"] != 0:
			numbers.append(dictionary["Deletions"])

			# Remove the "]" character of the text template
			if text_template != "" and "]" in text_template[-1]:
				text_template = text_template[:-1]

			# If the changes are not zero
			# Replace the " and " text with the ", " (comma and space) text
			if dictionary["Changes"] != 0:
				text_template = text_template.replace(" " + self.language_texts["and"] + " ", ", ")

			# Get the singular or plural text
			text = self.language_texts["deletion"]

			if dictionary["Deletions"] > 1:
				text = self.language_texts["deletions"]

			# If the changes are not zero
			# Add the ", and " text
			if dictionary["Changes"] != 0:
				text_template += ", " + self.language_texts["and"] + " "

			# Else, add the "[" text
			# (Difference has only deletions)
			else:
				text_template += "["

			# Add the " and {} deletions" text
			text_template += "{} " + text

			# Re-add the "]" character
			text_template += "]"

		# Format the text template
		if numbers != []:
			text = "\t\t" + text_template.format(*numbers)

			# Add a space and the template to the lines of text difference
			if dictionary["Difference"]["Lines"] != [] and dictionary["Difference"]["Lines"][-1] != "":
				dictionary["Difference"]["Lines"].append("")

			dictionary["Difference"]["Lines"].append(text)

		# Transform the lines list into a string
		dictionary["Difference"]["Text"] = self.Text_From_List(dictionary["Difference"]["Lines"])

		return dictionary["Difference"]["Text"]

	def Check_Text_Difference(self, file_text, text_lines_to_write, settings = {}, full_verbose = False):
		# Define the maximum number of lines of when to not use the text difference
		# Any changes that exceed this limit activate the full verbose mode
		maximum_lines = 20

		# Define the "make text difference" switch as True by default
		make_text_difference = True

		# If the "full verbose" parameter is True
		if full_verbose == True:
			# Change the "make text difference" switch to False
			make_text_difference = False

		# Define the default verbose text for the non-verbose mode
		verbose_text = self.language_texts["text, title()"] + ":\n[" + \
		text_lines_to_write + \
		"]"

		# If the verbose mode is activated
		# And the "make text difference" switch is True
		# And the number of lines of the text file is greater than the maximum number of lines to show
		# And the file is not empty
		# Show only the text difference, not the full text to write
		if (
			self.switches["Verbose"] == True and
			make_text_difference == True and
			len(file_text["lines"]) > maximum_lines and
			file_text["lines"] != []
		):
			# Make the text difference between the text inside the file and the text to be written
			text_difference = self.Text_Difference(file_text, text_lines_to_write, settings)

			# Update the verbose text to add the text difference
			verbose_text = self.language_texts["text_difference"] + ":\n" + \
			"\t[\n" + \
			text_difference + \
			"\n\t]"

		# Return the verbose text
		return verbose_text