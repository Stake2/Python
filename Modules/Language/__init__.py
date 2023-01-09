# Language.py

from Global_Switches import Global_Switches as Global_Switches

import os
import locale
import re
import pathlib
import json
import platform

class Language():
	def __init__(self, parameter_switches = None, show_global_switches = False):
		# Global Switches dictionary
		self.global_switches = Global_Switches().global_switches

		self.global_switches.update({
			"folder": {
				"create": True,
			},
			"file": {
				"create": True,
				"edit": True,
			},
		})

		if parameter_switches != None:
			self.global_switches.update(parameter_switches)

		self.Define_Lists_And_Dictionaries()
		self.Define_Folders()
		self.Define_Languages()
		self.Get_System_Information()
		self.Define_App_Settings()
		self.Define_Texts()
		self.Define_Language_Texts()
		self.Read_Settings_File()

		if show_global_switches == True:
			self.Show_Global_Switches(self.global_switches)

			if self.global_switches["user_information"] == True:
				self.Show_User_Information()

	def Define_Lists_And_Dictionaries(self):
		self.dictionary_separators = ["=", " = ", ":", ": "]

		self.setting_names = {
			"language": {
				"key": "language",
				"name": {
					"en": "language",
					"pt": "idioma",
				},
				"list": [
					"language",
					"Language",
					"idioma",
					"Idioma",
					"linguagem",
					"Linguagem",
				],
			},
		}

	def Define_Folders(self):
		self.hard_drive_letter = os.path.normpath(pathlib.Path.home().drive) + "/"

		if platform.release() == "10":
			self.hard_drive_letter = "D:/"

		self.apps_folder = self.hard_drive_letter + "Apps/"
		self.app_text_files_folder = self.apps_folder + "Module Files/"

		self.module = {
			"name": self.__module__,
		}

		if __name__ == "__main__":
			self.module["name"] = "Language"

		if "." in self.module["name"]:
			self.module["name"] = self.module["name"].split(".")[0]

		if self.module["name"] == "__main__":
			self.module["name"] = "File"

		self.module_text_files_folder = self.app_text_files_folder + self.module["name"] + "/"

		self.texts_file = self.module_text_files_folder + "Texts.json"
		self.Create(self.texts_file)

		self.languages_file = self.module_text_files_folder + "Languages.json"
		self.Create(self.languages_file)

	def Define_Languages(self):
		self.languages = self.JSON_To_Python(self.languages_file)

	def Get_System_Information(self):
		self.system_information = {}
		self.system_information["locale"] = locale.getdefaultlocale()
		self.system_information["encoding"] = self.system_information["locale"][1]
		self.system_information["language_with_country"] = self.system_information["locale"][0]

		self.system_information["language"] = self.system_information["language_with_country"]

		if "_" in self.system_information["language"]:
			self.system_information["language"] = self.system_information["language"].split("_")[0]

		if self.system_information["language"] in self.languages["full"]:
			self.system_information["full_language"] = self.languages["full"][self.system_information["language"]]

	def Sanitize(self, path):
		path = os.path.normpath(path).replace("\\", "/")

		if "/" not in path[-1] and os.path.splitext(path)[-1] == "":
			path += "/"

		return path

	def Verbose(self, text, item):
		if self.global_switches["verbose"] == True:
			import inspect

			print()
			print(inspect.stack()[1][3] + "():")
			print("\t" + text + ":")
			print("\t" + item)

	def Create(self, item = None, text = None):
		if item == None:
			item = self.Type(text)

		item = self.Sanitize(item)

		if os.path.splitext(item)[-1] == "":
			if self.global_switches["folder"]["create"] == True and os.path.isdir(item) == False:
				os.mkdir(item)

		if os.path.splitext(item)[-1] != "":
			if self.global_switches["file"]["create"] == True and os.path.isfile(item) == False:
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
		}

		contents["string"] = open(file, "r", encoding = "utf8").read()
		contents["size"] += os.path.getsize(file)

		for line in open(file, "r", encoding = "utf8").readlines():
			line = line.replace("\n", "")

			contents["lines"].append(line)
			contents["lines_none"].append(line)

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

		if self.global_switches["file"]["edit"] == True and os.path.isfile(file) == True:
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

	def Define_App_Settings(self):
		self.app_settings = {}

		self.app_settings["language"] = self.system_information["language"]
		self.user_language = self.app_settings["language"]
		self.full_user_language = self.languages["full"][self.user_language]

	def Python_To_JSON(self, item):
		return json.dumps(item, indent = 4, ensure_ascii = False)

	def JSON_To_Python(self, file):
		file = self.Sanitize(file)

		dictionary = json.load(open(file, encoding = "utf8"))

		return dictionary

	def Show_JSON(self, json):
		print(self.Python_To_JSON(json))

	def Item(self, texts, user_language = None):
		if user_language == None:
			user_language = self.user_language

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

							if "masculine" in texts[text][language]:
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
			user_language = self.user_language

		i = 0
		for language in languages:
			if language == user_language:
				language_number = i

			i += 1

		return text.split(separator)[language_number]

	def Define_Texts(self):
		self.texts = self.JSON_To_Python(self.texts_file)

	def Define_Language_Texts(self):
		self.texts = self.Title(self.texts)

		self.language_texts = self.Item(self.texts)

		for language_type in self.languages["types"]:
			self.language_texts["your_" + language_type + "_is"] = self.language_texts["your_{}_is"].format(self.Item(self.texts[language_type]))

		self.settings_file = os.path.join(self.apps_folder, self.language_texts["settings"].capitalize() + ".json")

		if os.path.isfile(self.settings_file) == False:
			self.Create(self.settings_file)
			self.Edit(self.settings_file, self.Python_To_JSON({}), "w")

	def Read_Settings_File(self):
		if os.path.isfile(self.settings_file) == True:
			settings = self.JSON_To_Python(self.settings_file)

			for setting_name in self.setting_names:
				possible_setting_names = self.setting_names[setting_name]["list"]

				for possible_setting_name in possible_setting_names:
					if possible_setting_name in settings:
						setting = settings[possible_setting_name]

						if setting in list(self.languages["full"].values()):
							for language in self.languages["full"]:
								full_language = self.languages["full"][language]

								if setting == full_language:
									setting = language

						self.app_settings[setting_name] = setting

						if setting in self.languages["small"]:
							self.user_language = setting
							self.full_user_language = self.languages["full"][setting]

			self.Define_Language_Texts()

		if os.path.isfile(self.settings_file) == False:
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

		settings_file = os.path.join(folder, self.language_texts["settings"].title() + ".txt")

		# Create file
		self.Create(settings_file)

		# Ask for each setting
		for setting_name in self.setting_names:
			setting_information = self.setting_names[setting_name]

			language_setting_name = setting_information["name"][self.app_settings["language"]]

			option = self.Select(self.languages["small"], show_text = self.language_texts["languages"].title() + ":", select_text = self.language_texts["select_one_{}_(number_or_word), masculine"].format(language_setting_name) + ": ")

			self.Edit(settings_file, setting_name.title() + ": " + option, "a")

		self.Read_Settings_File()

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
			translated_language = self.languages["full_translated"][language][self.app_settings["language"]]

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

	def Show_Global_Switches(self, local_switches, show_ending = False):
		has_true_variables = False

		for key in local_switches:
			if local_switches[key] == True:
				has_true_variables = True

		if has_true_variables == True:
			print()
			print("-----")
			print()

		for key in local_switches:
			if local_switches[key] == True:
				if key == "user_information":
					print()

				print(self.language_texts[key])

		if has_true_variables == True and local_switches["user_information"] == False or show_ending == True:
			print()
			print("-----")

	def Show_User_Information(self):
		print()
		print(self.language_texts["class, title()"] + ' "' + self.module["name"] + '", ' + self.language_texts["the_user_information"] + ":")

		for language_type in self.languages["types"]:
			print("\t" + self.language_texts[language_type].capitalize() + ":")
			print("\t\t" + self.system_information[language_type])

			if language_type != self.languages["types"][-1]:
				print()

		if "language" in self.app_settings and self.user_language != self.system_information["language"]:
			print()
			print("\t" + self.language_texts["your_{}_is"].format(self.language_texts["custom_language"]) + ":")
			print("\t\t" + self.user_language + ", " + self.full_languages[self.user_language])

		print()
		print("-----")

if __name__ == "__main__":
	Language = Language()
	Language.Create_Language_Text()