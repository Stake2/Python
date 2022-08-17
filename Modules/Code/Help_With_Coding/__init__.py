# Help_With_Coding.py

from Script_Helper import *

from Code.Code import Code as Code

Execute = exec

class Help_With_Coding(Code):
	def __init__(self, parameter_switches = None, custom_options = None):
		super().__init__(parameter_switches)

		self.custom_options = custom_options

		self.Select_Programming_Language()

		if self.programming_language_settings["Has Modes"] == True:
			self.Select_Mode()

		if self.programming_language_settings["Has Setting File"] == True:
			self.Change_Settings_Files()

		if self.programming_language_settings["Has First Function"] == True:
			self.Execute_First_Function()

		if self.programming_language_settings["Has Tools"] == True:
			self.Define_Tools()
			self.Manage_Tools("Open")

			print()
			input(Language_Item_Definer("Press Enter when you finish programming in", "Pressione Enter quando terminar de programar em") + " {}: ".format(self.programming_language))
			print()

		if self.programming_language_settings["Has Final Function"] == True:
			self.Execute_Final_Function()

		if self.programming_language_settings["Has Tools"] == True:
			self.Manage_Tools("Close")

		self.Register_On_Diary_Slim()

		print()
		print("---")
		print()
		print(Language_Item_Definer("Finished programming in {}", "Terminou de programar em {}").format(self.programming_language) + ".")

	def Select_Programming_Language(self):
		if self.custom_options == None:
			self.choice_text = Language_Item_Definer("Select a Programming Language to use", "Selecione uma Linguagem de Programação para usar")
			self.programming_language = Select_Choice_From_List(self.programming_languages, local_script_name, self.choice_text, second_choices_list = self.programming_languages, return_second_item_parameter = True, return_number = True, add_none = True, first_space = False, second_space = False)[0]

		else:
			self.programming_language = self.custom_options["Programming Language"]
			print("---")
			print()
			print(Language_Item_Definer('You selected the "{}" Programming Language', 'Você selecionou a Linguagem de Programação "{}"').format(self.programming_language) + ".")

		self.programming_language_folder = self.programming_language_folders[self.programming_language]

		self.programming_language_settings_file = self.programming_language_folder + "Programming Language Settings" + self.dot_text
		Create_Text_File(self.programming_language_settings_file, self.global_switches["create_files"])

		self.programming_language_settings = Make_Setting_Dictionary(self.programming_language_settings_file, define_yes_or_no = True, define_true_or_false = True, read_file = True)

		for setting_name in self.programming_language_setting_names:
			if setting_name not in self.programming_language_settings and setting_name not in self.programming_mode_item_names:
				self.programming_language_settings[setting_name] = False

			for item_name in self.programming_mode_item_names:
				item_folder = self.programming_language_folder + item_name + "/"

				if is_a_folder(item_folder) == True:
					setting_value = True

				if is_a_folder(item_folder) == False:
					setting_value = False

				if "Has " + item_name in self.programming_language_settings:
					setting_value = self.programming_language_settings["Has " + item_name]

				if "Has " + item_name in self.programming_language_settings:
					setting_value = self.programming_language_settings["Has " + item_name]

				self.programming_language_settings["Has " + item_name] = setting_value

		self.item_data = {}

		for item_name in self.programming_mode_item_names:
			if self.programming_language_settings["Has " + item_name] == True:
				self.item_data[item_name] = {}
				self.item_data[item_name]["Folder"] = self.programming_language_folder + item_name + "/"

	def Select_Mode(self):
		self.modes_folder = self.programming_language_folder + "Modes/"
		Create_Folder(self.modes_folder, self.global_switches["create_folders"])

		self.modes_folders = List_Folder(self.modes_folder)

		self.modes = {}

		self.mode_names = []
		self.language_mode_names = {}
		self.language_mode_names["English"] = []
		self.language_mode_names["Portuguese"] = []

		self.mode_settings = {}
		self.mode_settings.update(self.programming_language_settings)

		for mode_name in self.modes_folders:
			self.mode_names.append(mode_name)
			self.modes[mode_name] = {}
			self.mode = self.modes[mode_name]
			self.mode_settings[mode_name] = {}
			self.mode_settings[mode_name].update(self.programming_language_settings)

			folder = self.modes_folder + mode_name + "/"

			self.mode_settings_file = folder + "Settings" + self.dot_text

			self.mode_settings_read = {}

			if is_a_file(self.mode_settings_file) == True:
				self.mode_settings_read = Make_Setting_Dictionary(self.mode_settings_file, define_yes_or_no = True, define_true_or_false = True, read_file = True)

			language_names_file = folder + "Language names" + self.dot_text
			language_names = Make_Setting_Dictionary(language_names_file, read_file = True)
			self.mode["Language Names"] = language_names

			self.language_mode_names["English"].append(self.mode["Language Names"]["English Name"])
			self.language_mode_names["Portuguese"].append(self.mode["Language Names"]["Portuguese Name"])

			self.language_mode_names[mode_name] = {}

			self.language_mode_names[mode_name]["English"] = self.mode["Language Names"]["English Name"]
			self.language_mode_names[mode_name]["Portuguese"] = self.mode["Language Names"]["Portuguese Name"]

			for item_name in self.programming_mode_item_names:
				item_folder = folder + item_name + "/"

				if is_a_folder(item_folder) == True:
					setting_value = True

				if is_a_folder(item_folder) == False:
					setting_value = False

				if "Has " + item_name in self.mode_settings_read:
					setting_value = self.mode_settings_read["Has " + item_name]

				self.mode_settings[mode_name]["Has " + item_name] = setting_value

		self.choice_text = Language_Item_Definer("Select the programming mode", "Selecione o modo de programação")
		self.choice_list = Language_Item_Definer(self.language_mode_names["English"], self.language_mode_names["Portuguese"])

		self.programming_mode = Select_Choice_From_List(self.choice_list, local_script_name, self.choice_text, second_choices_list = self.mode_names, return_second_item_parameter = True, return_number = True, add_none = True, first_space = True)
		self.programming_mode_number = self.programming_mode[1] - 1
		self.programming_mode = self.programming_mode[0]
		self.programming_mode_folder = self.modes_folder + self.programming_mode + "/"

		self.programming_language_folder = self.programming_mode_folder

		first_function_folder = self.programming_language_folder + "First Function/"

		if is_a_folder(first_function_folder) == True:
			self.mode_settings["Has First Function"] = True

		self.mode_settings = self.mode_settings[self.programming_mode]
		self.programming_language_settings = self.mode_settings

		for item_name in self.programming_mode_item_names:
			item_folder = self.programming_language_folder + item_name + "/"

			self.item_data[item_name] = {}
			self.item_data[item_name]["Folder"] = item_folder

	def Execute_First_Function(self):
		self.first_function_folder = self.programming_language_folder + "First Function/"
		self.first_function_text_file = self.first_function_folder + "Data" + self.dot_text

		self.first_function_data = {}

		if is_a_file(self.first_function_text_file) == True:
			self.first_function_data.update(Make_Setting_Dictionary(self.first_function_text_file, read_file = True))

		self.Define_Function_Variables(self.first_function_folder, self.first_function_data)

		self.first_function_data = self.function_data

		print(self.code_header)

		if self.first_function_data["Extension"] == "py":
			import importlib.util

			path = importlib.util.spec_from_file_location(self.first_function_data["English Name"], self.function_code_file)
			First_Function = importlib.util.module_from_spec(path)
			path.loader.exec_module(First_Function)

		if self.programming_language_settings["Has Final Function"] == True:
			print()

		if self.programming_language_settings["Has Final Function"] == False:
			print(self.code_footer)

	def Change_Settings_Files(self):
		self.setting_files_file = self.item_data["Setting File"]["Folder"] + "Files" + self.dot_text
		Create_Text_File(self.setting_files_file, self.global_switches["create_files"])

		self.settings_files_data = Make_Setting_Dictionary(self.setting_files_file, read_file = True)

		if self.custom_options != None:
			self.programming_mode = self.custom_options["Mode"]

		for setting_name in self.settings_files_data:
			self.settings_files_data[setting_name] = self.settings_files_data[setting_name].split(", ")

		if self.programming_language_settings["Has Setting File"] != "No":
			self.setting_template_folder = self.item_data["Setting File"]["Folder"] + "Templates/"

			i = 0
			for setting_file_name in self.settings_files_data["File Names"]:
				self.last_setting_data_folder = self.module_text_files_folder + "Last Setting Data/"

				self.last_data_file = self.last_setting_data_folder + setting_file_name
				Create_Text_File(self.last_data_file, self.global_switches["create_files"])

				self.last_data = Read_String(self.last_data_file)

				self.new_data_file = self.setting_template_folder + setting_file_name
				self.new_data = Read_String(self.new_data_file)

				self.destination_data_file = self.settings_files_data["File Paths"][i]
				self.destination_data = Read_String(self.destination_data_file)

				if self.last_data in self.destination_data:
					text_to_write = self.destination_data.replace(self.last_data, self.new_data)
					Write_To_File(self.destination_data_file, text_to_write, self.global_switches)
					Write_To_File(self.last_data_file, self.new_data, self.global_switches)

				i += 1

	def Define_Tools(self):
		self.tools_folder = self.item_data["Tools"]["Folder"]

		self.tool_files = List_Files(self.tools_folder, add_none = False)

		self.tool_data = {}
		self.tool_names = []

		for tool_file in self.tool_files:
			tool_info = Make_Setting_Dictionary(tool_file, read_file = True)

			tool_name = tool_info["Name"]
			self.tool_names.append(tool_name)

			self.tool_data[tool_name] = {}
			self.tool_data[tool_name]["Name"] = tool_name

			for language_name_text in self.language_name_texts:
				if language_name_text in tool_info:
					self.tool_data[tool_name][language_name_text] = tool_info[language_name_text]

			self.tool_data[tool_name]["Path"] = tool_info["Path"]

			for tool_sub_name in self.tool_sub_names:
				if tool_sub_name in tool_info:
					self.tool_data[tool_name][tool_sub_name] = tool_info[tool_sub_name]

			self.tool_data[tool_name]["Close"] = []

			if "Programs To Close" in self.tool_data[tool_name]:
				if ", " in self.tool_data[tool_name]["Programs To Close"]:
					self.tool_data[tool_name]["Close"].extend(self.tool_data[tool_name]["Programs To Close"].split(", "))

				else:
					self.tool_data[tool_name]["Close"].append(self.tool_data[tool_name]["Programs To Close"])

			else:
				self.tool_data[tool_name]["Close"].append(tool_name + ".exe")

			self.tool_data[tool_name]["Programs To Close"] = self.tool_data[tool_name]["Close"]

	def Manage_Tools(self, mode):
		if mode == "Open":
			mode_text = "Opening"

		if mode == "Close":
			mode_text = "Closing"

		i = 0
		for tool_name in self.tool_names:
			tool_path = self.tool_data[tool_name]["Path"]
			tool_data = self.tool_data[tool_name]
			programs_to_close = self.tool_data[tool_name]["Programs To Close"]

			tool_name_print = tool_name

			if "English Name" in self.tool_data[tool_name]:
				tool_name_print = Language_Item_Definer(tool_data["English Name"], tool_data["Portuguese Name"])

			if "Function" not in self.tool_data[tool_name]:
				Open_Function = Open_File

			if "Function" in self.tool_data[tool_name]:
				Open_Function = self.basic_functions[self.tool_data[tool_name]["Function"]]

			self.text_to_print = self.texts_dictionary[mode_text + " tool format text"].format(tool_name_print) + "\n" + Language_Item_Definer("Path", "Caminho") + ': "' + tool_path + '"'

			if mode == "Close" and Open_Function == Open_File and "Close Tool" not in tool_data:
				print(self.text_to_print)

				for program in programs_to_close:
					if self.global_switches["testing_script"] == False:
						Close_Program(program)

				print()

			if mode == "Open":
				print(self.text_to_print)

				if self.global_switches["testing_script"] == False:
					Open_Function(tool_path)

				if tool_name != self.tool_names[-1]:
					time.sleep(2)
					print()

			i += 1

	def Execute_Final_Function(self):
		self.final_function_folder = self.programming_language_folder + "Final Function/"
		self.final_function_text_file = self.final_function_folder + "Data" + self.dot_text

		self.final_function_data = {}

		if is_a_file(self.final_function_text_file) == True:
			self.final_function_data.update(Make_Setting_Dictionary(self.final_function_text_file, read_file = True))

		self.Define_Function_Variables(self.final_function_folder, self.final_function_data)

		self.final_function_data = self.function_data

		print(self.code_header)

		if self.final_function_data["Extension"] == "py":
			import importlib.util

			path = importlib.util.spec_from_file_location(self.final_function_data["English Name"], self.function_code_file)
			Final_Function = importlib.util.module_from_spec(path)
			path.loader.exec_module(Final_Function)

		print(self.code_footer)

	def Define_Function_Variables(self, function_folder, function_data):
		self.function_folder = function_folder
		self.function_data = function_data

		if "Extension" not in self.function_data:
			self.function_data["Extension"] = "py"

		self.function_code_file = self.function_folder + "Function_Code" + "." + self.function_data["Extension"]

		if self.programming_language_settings["Has Modes"] == True and "English Name" not in self.function_data:
			self.function_data["English Name"] = self.language_mode_names[self.programming_mode]["English"]
			self.function_data["Portuguese Name"] = self.language_mode_names[self.programming_mode]["Portuguese"]

		self.code_title = Language_Item_Definer(self.function_data["English Name"], self.function_data["Portuguese Name"])

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

		if "Title Space" not in self.function_data:
			self.code_header += "\n"

		if "Second Space" not in self.function_data:
			self.code_footer += "\n"

		if self.ellipsis_in_title == True:
			self.code_header = self.code_header.replace(":", "")

	def Register_On_Diary_Slim(self):
		from Diary_Slim.Write_On_Diary_Slim import Write_On_Diary_Slim as Write_On_Diary_Slim

		if self.programming_language == "PHP" and self.programming_mode == "Udemy course":
			self.programming_language = "Udemy Course"

		if self.global_switches["testing_script"] == False:
			Write_On_Diary_Slim(self.programming_language)

		if self.programming_language == "Udemy Course":
			self.programming_language = "PHP"