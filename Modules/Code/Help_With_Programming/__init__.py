# Help_With_Programming.py

from Code.Code import Code as Code

class Help_With_Programming(Code):
	def __init__(self, custom_options = None):
		super().__init__(parameter_switches)

		self.custom_options = custom_options

		self.Select_Programming_Language()

		if self.programming_language_settings["Modes"] == True:
			self.Select_Mode()

		if self.programming_language_settings["Setting file"] == True:
			self.Change_Settings_Files()

		if self.programming_language_settings["First function"] == True:
			self.Execute_Function("First")

		if self.programming_language_settings["Tools"] == True:
			self.Define_Tools()
			self.Manage_Tools("open")

			self.Input.Type(self.language_texts["press_enter_when_you_finish_programming_in"] + " " + self.programming_language)

		if self.programming_language_settings["Final function"] == True:
			self.Execute_Function("Final")

		if self.programming_language_settings["Tools"] == True:
			self.Manage_Tools("close")

		self.Register_On_Diary_Slim()

		print(self.large_bar)
		print()
		print(self.language_texts["you_finished_programming_in"] + " " + self.programming_language + ".")

	def Select_Programming_Language(self):
		if self.custom_options == None:
			self.show_text = self.language_texts["programming_languages"]
			self.select_text = self.language_texts["select_a_programming_language_to_use"]

			self.programming_language = self.Input.Select(self.programming_languages, show_text = self.show_text, select_text = self.select_text)["option"]

		else:
			self.programming_language = self.custom_options["Programming Language"]

			print("---")
			print()
			print(self.language_texts["you_selected_this_programming_language"] + ":")
			print(self.programming_language + ".")

		self.programming_language_folder = self.programming_language_folders[self.programming_language]

		self.programming_language_settings_file = self.programming_language_folder + "Settings.txt"
		self.File.Create(self.programming_language_settings_file)

		self.programming_language_settings = self.File.Dictionary(self.programming_language_settings_file, true_or_false = True)

		for item_name in self.programming_mode_item_names:
			if item_name not in self.programming_language_settings:
				self.programming_language_settings[item_name] = False

			item_folder = self.programming_language_folder + item_name + "/"

			if item_name in self.programming_language_settings:
				value = self.programming_language_settings[item_name]

			if self.Folder.Exist(item_folder) == True:
				value = True

			if self.Folder.Exist(item_folder) == False:
				value = False

			if value == self.Language.language_texts["yes, title()"]:
				value = True

			if value == self.Language.language_texts["no, title()"]:
				value = False

			self.programming_language_settings[item_name] = value

		self.item_data = {}

		for item_name in self.programming_mode_item_names:
			if self.programming_language_settings[item_name] == True:
				self.item_data[item_name] = {}
				self.item_data[item_name]["Folder"] = self.programming_language_folder + item_name + "/"

	def Select_Mode(self):
		self.modes_folder = self.programming_language_folder + "Modes/"
		self.Folder.Create(self.modes_folder)

		self.contents = self.Folder.Contents(self.modes_folder)

		for folder in self.contents["folder"]["list"].copy():
			if self.modes_folder.count("/") + 1 != folder.count("/"):
				self.contents["folder"]["list"].remove(folder)

				if folder.split("/")[-2] in self.contents["folder"]["names"]:
					self.contents["folder"]["names"].remove(folder.split("/")[-2])

		self.modes = {}

		self.mode_names = []
		self.language_mode_names = {}

		for language in self.languages["small"]:
			self.language_mode_names[language] = []

		self.mode_settings = {}
		self.mode_settings.update(self.programming_language_settings)

		for mode_name in self.contents["folder"]["names"]:
			self.mode_names.append(mode_name)

			self.modes[mode_name] = {}

			self.mode = self.modes[mode_name]

			# Mode settings read
			self.mode_settings[mode_name] = {}
			self.mode_settings[mode_name].update(self.programming_language_settings)

			mode_folder = self.modes_folder + mode_name + "/"

			# Mode settings read
			self.mode_settings_file = mode_folder + "Settings.txt"

			self.mode_settings_read = {}

			if self.File.Exist(self.mode_settings_file) == True:
				self.mode_settings_read = self.File.Dictionary(self.mode_settings_file, true_or_false = True)

			# Mode names
			self.mode["Language names"] = self.JSON.To_Python(mode_folder + "Data.json")

			self.language_mode_names[mode_name] = {}

			for language in self.languages["small"]:
				language_name = self.texts["language_name"][language][self.user_language]

				self.language_mode_names[language].append(self.mode["Language names"][language])
				self.language_mode_names[mode_name][language] = self.mode["Language names"][language]

			for item_name in self.programming_mode_item_names:
				item_folder = mode_folder + item_name + "/"

				value = True

				if self.Folder.Exist(item_folder) == False:
					value = False

				if item_name in self.mode_settings_read:
					value = self.mode_settings_read[item_name]

				if value == self.Language.language_texts["yes, title()"]:
					value = True

				if value == self.Language.language_texts["no, title()"]:
					value = False

				self.mode_settings[mode_name][item_name] = value

		self.options = self.mode_names
		self.language_options = self.Language.Item(self.language_mode_names)

		self.show_text = self.language_texts["programming_modes"]
		self.select_text = self.language_texts["select_the_programming_mode"]

		self.dictionary = self.Input.Select(self.options, self.language_options, select_text = self.select_text, show_text = self.show_text)

		self.programming_mode_number = self.dictionary["number"]
		self.programming_mode = self.dictionary["option"]
		self.programming_mode_folder = self.modes_folder + self.programming_mode + "/"

		self.programming_language_folder = self.programming_mode_folder

		first_function_folder = self.programming_language_folder + "First Function/"

		if self.Folder.Exist(first_function_folder) == True:
			self.mode_settings["First function"] = True

		self.mode_settings = self.mode_settings[self.programming_mode]
		self.programming_language_settings = self.mode_settings

		for item_name in self.programming_mode_item_names:
			item_folder = self.programming_language_folder + item_name + "/"

			self.item_data[item_name] = {}
			self.item_data[item_name]["Folder"] = item_folder

	def Define_Function_Variables(self, function_folder, function_data):
		self.function_folder = function_folder
		self.function_data = function_data

		if "Extension" not in self.function_data:
			self.function_data["Extension"] = "py"

		self.function_code_file = self.function_folder + "Function_Code." + self.function_data["Extension"]

		if self.programming_language_settings["Modes"] == True:
			for language in self.languages["small"]:
				language_name = self.texts["language_name"][language][self.user_language]

				if language_name not in self.function_data:
					self.function_data[language] = self.language_mode_names[self.programming_mode][language]

		self.code_title = self.Language.Item(self.function_data)

		self.ellipsis_in_title = False

		if "..." in self.code_title:
			self.code_title = self.code_title.replace("...", "")

			self.ellipsis_in_title = True

		if self.programming_language not in self.code_title:
			self.code_title += " (" + self.programming_language + ")"

		if self.ellipsis_in_title == True:
			self.code_title += "..."

		self.code_header = self.large_bar + "\n\n" + self.code_title + ":"

		self.code_footer = "\n" + self.large_bar

		if "Title space" not in self.function_data:
			self.code_header += "\n"

		if "Second space" not in self.function_data:
			self.code_footer += "\n"

		if self.ellipsis_in_title == True:
			self.code_header = self.code_header.replace(":", "")

	def Execute_Function(self, function):
		self.function_folder = self.programming_language_folder + function + " Function/"
		self.data_file = self.function_folder + "Data.json"

		self.data = {}

		if self.File.Exist(self.data_file) == True:
			self.data.update(self.JSON.To_Python(self.data_file))

		for key in self.data:
			if self.data[key] == "True":
				self.data[key] = True

			if self.data[key] == "False":
				self.data[key] = False

		self.Define_Function_Variables(self.function_folder, self.data)

		self.data = self.function_data

		print()

		print(self.code_header)

		if self.data["Extension"] == "py":
			import importlib.util

			path = importlib.util.spec_from_file_location(self.data["en"], self.function_code_file)
			Function = importlib.util.module_from_spec(path)
			path.loader.exec_module(Function)

		if function == "Final":
			print()

		if function != "Final":
			print(self.code_footer)

	def Change_Settings_Files(self):
		self.setting_files_file = self.item_data["Setting file"]["Folder"] + "Data.json"
		self.File.Create(self.setting_files_file)

		self.settings_files_data = self.JSON.To_Python(self.setting_files_file)

		if self.custom_options != None:
			self.programming_mode = self.custom_options["Mode"]

		for setting_name in self.settings_files_data:
			if ", " in self.settings_files_data[setting_name]:
				self.settings_files_data[setting_name] = self.settings_files_data[setting_name].split(", ")

		self.setting_template_folder = self.item_data["Setting file"]["Folder"] + "Templates/"

		i = 0
		for setting_file_name in self.settings_files_data[self.language_texts["file_names"]]:
			self.last_setting_data_folder = self.folders["apps"]["module_files"][self.module["key"]]["root"] + "Last setting data/"

			self.last_data_file = self.last_setting_data_folder + setting_file_name
			self.File.Create(self.last_data_file)

			self.last_data = self.File.Contents(self.last_data_file)["string"]

			self.new_data_file = self.setting_template_folder + setting_file_name
			self.new_data = self.File.Contents(self.new_data_file)["string"]

			self.destination_data_file = self.settings_files_data[self.language_texts["file_paths"]][i]
			self.destination_data = self.File.Contents(self.destination_data_file)["string"]

			if self.last_data in self.destination_data:
				text_to_write = self.destination_data.replace(self.last_data, self.new_data)

				self.File.Edit(self.destination_data_file, text_to_write, "w")
				self.File.Edit(self.last_data_file, self.new_data, "w")

			i += 1

	def Define_Tools(self):
		self.tools_folder = self.item_data["Tools"]["Folder"]

		self.tool_files = self.Folder.Contents(self.tools_folder)["file"]["list"]

		self.tool_data = {}
		self.tool_names = []

		for tool_file in self.tool_files:
			tool_info = self.File.Dictionary(tool_file)

			tool_name = tool_info[self.language_texts["original_name"]]
			self.tool_names.append(tool_name)

			self.tool_data[tool_name] = {}
			tool_data = self.tool_data[tool_name]

			tool_data[self.language_texts["original_name"]] = tool_name

			for language in self.languages["small"]:
				language_name = self.texts["language_name"][language][self.user_language]

				if language_name in tool_info:
					tool_data[language_name] = tool_info[language_name]

			tool_data[self.language_texts["path, title()"]] = tool_info[self.language_texts["path, title()"]]

			for tool_sub_name in self.tool_sub_names:
				if tool_sub_name in tool_info:
					value = tool_info[tool_sub_name]

					if value == self.Language.language_texts["yes, title()"]:
						value = True

					if value == self.Language.language_texts["no, title()"]:
						value = False

					tool_data[tool_sub_name] = value

			if self.language_texts["programs_to_close"] in tool_data and ", " in tool_data[self.language_texts["programs_to_close"]]:
				tool_data[self.language_texts["programs_to_close"]] = tool_data[self.language_texts["programs_to_close"]].split(", ")

			else:
				tool_data[self.language_texts["programs_to_close"]] = []
				tool_data[self.language_texts["programs_to_close"]].append(tool_name + ".exe")

	def Manage_Tools(self, mode):
		if mode == "open":
			mode_text = mode

		if mode == "close":
			mode_text = mode[:-1]

		mode_text += "ing"

		language_mode_text = self.language_texts[mode_text + ", title()"]

		show = True

		for tool_name in self.tool_names:
			tool_data = self.tool_data[tool_name]

			if mode == "close" and self.language_texts["close_tool"] in tool_data:
				show = False

		if show == True and self.programming_language_settings["First function"] == False:
			print()
			print("-----")

		i = 0
		for tool_name in self.tool_names:
			tool_data = self.tool_data[tool_name]

			tool_path = tool_data[self.language_texts["path, title()"]]
			programs_to_close = tool_data[self.language_texts["programs_to_close"]]

			language_tool_name = tool_name

			for language in self.languages["small"]:
				language_name = self.texts["language_name"][language][self.user_language]

				if language_name in tool_data:
					language_tool_name = tool_data[language_name]

			Open = self.File.Open

			if self.language_texts["function, title()"] in tool_data:
				Open = self.basic_functions[tool_data[self.language_texts["function, title()"]]]

			self.text_to_print = self.language_texts["{}_the_programming_tool"].format(language_mode_text) + ' "' + language_tool_name + '"'

			if mode == "close" and Open == self.File.Open and self.language_texts["close_tool"] not in tool_data or mode == "open":
				print()
				print(self.text_to_print + "...")
				print()
				print(self.language_texts["path, title()"] + ":")
				print(tool_path)

			if mode == "close" and Open == self.File.Open and self.language_texts["close_tool"] not in tool_data and self.switches["global"]["testing"] == False:
				for program in programs_to_close:
					self.File.Close(program)

			if mode == "open" and self.switches["global"]["testing"] == False:
				Open(tool_path)

				self.Date.Sleep(2)

			i += 1

		if show == True:
			print()
			print("-----")

	def Register_On_Diary_Slim(self):
		from Diary_Slim.Write_On_Diary_Slim import Write_On_Diary_Slim as Write_On_Diary_Slim

		if self.programming_language == "PHP" and self.programming_mode == "Udemy course":
			self.programming_language = "Udemy course"

		if self.switches["global"]["testing"] == False:
			Write_On_Diary_Slim(self.programming_language)

		if self.programming_language == "Udemy course":
			self.programming_language = "PHP"