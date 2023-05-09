# Create_New_Module.py

from Python.Python import Python as Python

class Create_New_Module(Python):
	def __init__(self):
		super().__init__()

		self.Ask_For_Module_Info()
		self.Define_Variables()
		self.Write_To_Files()
		self.Create_Module_Bat()
		self.Add_To_ConEmu_Tasks()
		self.Add_To_Modules_List()
		self.Change_Global_Switches()
		self.Show_Module_Info()

	def Ask_For_Module_Info(self):
		# Module name
		self.module_name = self.Input.Type(self.language_texts["type_the_name_of_the_new_python_module"]).title()

		if " " in self.module_name:
			self.module_name = self.module_name.replace(" ", "_")

		self.module["key"] = self.module_name.lower()

		translated_language = ""

		i = 1
		for language in self.languages["small"]:
			translated_language += self.languages["full_translated"][language][self.user_language]

			if language != self.languages["small"][-1]:
				translated_language += "\n"

		self.translated_languages_language = []

		for language in self.languages["small"]:
			self.translated_languages_language.append(self.languages["full_translated"][language][self.user_language])

		self.lines_text = self.language_texts["{}_lines_in_thar_order"].format(self.Date.language_texts["number_names_feminine, type: list"][len(self.languages["small"])])

		# Module descriptions
		self.show_text = self.language_texts["type_the_{}_of_the_python_module_in_{}"].format(self.language_texts["descriptions"], self.lines_text) + ": "

		self.module_descriptions_prototype = self.Input.Lines(self.show_text, length = 2, line_options_parameter = {"enumerate": True, "enumerate_text": False, "capitalize": True}, line_texts = self.translated_languages_language)["lines"]

		self.module_descriptions = {}

		i = 0
		for language in self.languages["small"]:
			self.module_descriptions[language] = self.module_descriptions_prototype[i]

			if self.module_descriptions_prototype[i] == "" and language == "en":
				self.module_descriptions[language] = self.Text.Title(self.module_name.replace("_", " "))

			i += 1

		# Classes
		self.translated_english_language = self.languages["full_translated"]["en"][self.user_language]

		self.show_text = self.language_texts["type_the_{}_of_the_python_module_in_{}"].format(self.language_texts["classes"], self.translated_english_language + ", " + self.language_texts["separated_by_lines"]) + ": "

		self.classes = self.Input.Lines(self.show_text, line_options_parameter = {"enumerate": True, "enumerate_text": False, "capitalize": True})["lines"]

		i = 0
		for class_ in self.classes:
			if "_" not in class_:
				class_ = class_.title().replace(" ", "_")

			self.classes[i] = class_

			i += 1

		# Class descriptions
		self.class_descriptions = {}

		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language][self.user_language]

			self.show_text = self.language_texts["type_the_{}_of_the_python_module_in_{}"].format(self.language_texts["descriptions_of_classes"], translated_language + ", " + self.language_texts["separated_by_lines"]) + ":"

			self.class_descriptions[language] = self.Input.Lines(self.show_text, length = len(self.classes), line_options_parameter = {"enumerate": True, "enumerate_text": False, "capitalize": True})["lines"]

		i = 0
		for class_ in self.classes:
			self.class_descriptions[class_] = {}

			for language in self.languages["small"]:
				self.class_descriptions[class_][language] = self.class_descriptions[language][i]

			i += 1

		for language in self.languages["small"]:
			del self.class_descriptions[language]

		i = 0
		for class_ in self.classes:
			if self.class_descriptions[class_]["en"] == "":
				self.class_descriptions[class_]["en"] = self.Text.Capitalize(self.classes[i].replace("_", " ").lower())

			i += 1

		print()

	def Define_Variables(self):
		self.module_folder = self.folders["apps"]["modules"]["root"] + self.module_name + "/"
		self.Folder.Create(self.module_folder)

		self.root_python_file = self.module_folder + "__init__.py"
		self.File.Create(self.root_python_file)

		self.descriptions_file = self.module_folder + "Descriptions.json"
		self.File.Create(self.descriptions_file)

		self.main_class_folder = self.module_folder + self.module_name + "/"
		self.Folder.Create(self.main_class_folder)

		self.main_class_python_file = self.main_class_folder + "__init__.py"
		self.File.Create(self.main_class_python_file)

		self.folders["apps"]["module_files"][self.module["key"]] = {
			"root": self.folders["apps"]["module_files"]["root"] + self.module_name + "/",
		}

		self.Folder.Create(self.folders["apps"]["module_files"][self.module["key"]]["root"])

		self.folders["apps"]["module_files"][self.module["key"]]["texts"] = self.folders["apps"]["module_files"][self.module["key"]]["root"] + "Texts.json"
		self.File.Create(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

		self.class_folders = {}
		self.class_files = {}

		self.classes_string = ""

		i = 0
		for class_ in self.classes:
			class_folder = self.module_folder + self.Sanitize(class_, restricted_characters = True) + "/"
			self.Folder.Create(class_folder)

			init_file = class_folder + "__init__.py"
			self.File.Create(init_file)

			self.class_folders[class_] = class_folder
			self.class_files[class_] = init_file

			self.classes_string += '"' + class_ + '"'

			if class_ != list(self.classes)[-1]:
				self.classes_string += ",\n"

			i += 1

	def Write_To_Files(self):
		# Root code
		self.root_code = self.root_code_template.replace("[module_name]", self.module_name)
		self.root_code = self.root_code.replace("[classes]", self.classes_string)

		self.File.Edit(self.root_python_file, self.root_code, "w")

		# Descriptions
		self.descriptions = {**{"show_text": self.module_descriptions}, **self.class_descriptions}

		self.JSON.Edit(self.descriptions_file, self.descriptions)

		# Main class code
		self.main_class_code = self.main_class_code_template.replace("[]", self.module_name)

		self.File.Edit(self.main_class_python_file, self.main_class_code, "w")

		# Sub class code
		for class_ in self.classes:
			class_file = self.class_files[class_]

			self.sub_class_code = self.sub_class_code_template.format(class_, self.module_name, self.module_name, self.module_name, self.module_name, class_, self.module_name)

			self.File.Edit(class_file, self.sub_class_code, "w")

		# Texts.json
		self.File.Edit(self.folders["apps"]["module_files"][self.module["key"]]["texts"], "{\n\t\n}", "w")

	def Create_Module_Bat(self):
		self.bat_file = self.folders["apps"]["shortcuts"]["root"] + self.module_name + ".bat"
		self.File.Create(self.bat_file)

		bat_text = self.conemu_bat_template
		bat_text = bat_text.replace("[Name]", self.module_name.replace("_", " "))
		bat_text = bat_text.replace("[Module]", self.module_name.replace(" ", "_"))

		self.File.Edit(self.bat_file, bat_text, "w")

	def Add_To_ConEmu_Tasks(self):
		# Last task number file
		self.last_task_number = self.File.Contents(self.last_task_number_file)["lines"][0]

		self.next_task_number = str(int(self.last_task_number) + 1)

		self.File.Edit(self.last_task_number_file, self.next_task_number, "w")

		# ----- #
		# Last module XML file

		self.module_execution_line = "py C:\Apps\MS.py -{}".format(self.module_name.lower())

		self.next_module_xml = self.conemu_task_xml_template.replace("[Number]", self.next_task_number)
		self.next_module_xml = self.next_module_xml.replace("[Module_Name]", self.module_name.replace(" ", "_"))
		self.next_module_xml = self.next_module_xml.replace("[module_execution_line]", self.module_execution_line)

		self.File.Edit(self.last_module_xml_file, self.next_module_xml, "w")

		# ----- #
		# ConEmu XML file

		self.last_module_xml = self.File.Contents(self.last_module_xml_file)["string"]

		self.conemu_xml_text = self.File.Contents(self.conemu_xml_file)["string"]

		self.conemu_xml_text = self.conemu_xml_text.replace(self.last_module_xml, self.last_module_xml + "\n" + self.next_module_xml)

		self.value_count_template = '<value name="Count" type="long" data="{}"/>'

		self.conemu_xml_text = self.conemu_xml_text.replace(self.value_count_template.format(self.last_task_number), self.value_count_template.format(self.next_task_number))

		self.File.Edit(self.conemu_xml_file, self.conemu_xml_text, "w")

	def Add_To_Modules_List(self):
		if self.module_name not in self.modules["Usage"]["List"]:
			self.modules["Usage"]["List"].append(self.module_name)

		self.modules["Usage"]["List"] = sorted(self.modules["Usage"]["List"], key = str.lower)

		self.JSON.Edit(self.folders["modules_file"], self.modules)

	def Change_Global_Switches(self):
		self.switches_file = self.Global_Switches.switches["file"]

		self.switches["global"] = self.JSON.To_Python(self.switches_file)
		self.switches["global"]["testing"] = True
		self.switches["global"]["versbose"] = True

		self.JSON.Edit(self.switches_file, self.switches["global"])

	def Show_Module_Info(self):
		print(self.large_bar)
		print()
		print(self.language_texts["module_name"] + ":")
		print("\t" + self.module_name)
		print()

		print(self.language_texts["module_descriptions"] + " = {")

		for language in self.languages["small"]:
			translated_language = '"' + self.languages["full_translated"][language][self.user_language] + '": '

			print("\t" + translated_language + '"' + self.module_descriptions[language] + '",')

		print("}")
		print()

		print(self.language_texts["classes_and_their_descriptions"] + ":")

		format = "{}" + '"{}",'

		i = 0
		for class_ in self.classes:
			print("\t" + class_ + " = {")

			for language in self.languages["small"]:
				translated_language = '"' + self.languages["full_translated"][language][self.user_language] + '": '

				if class_ != self.classes[0]:
					print()
	
				print("\t\t" + format.format(translated_language, self.class_descriptions[class_][language]))

			print("\t" + "}")

			i += 1

		print()
 
		print(self.large_bar)
		print()

		input(self.JSON.Language.language_texts["press_enter_when_you_finish_reading_the_info_summary"] + ": ")