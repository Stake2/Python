# Create_New_Module.py

from Script_Helper import *

from Python_Module_Manager.Python_Module_Manager import Python_Module_Manager as Python_Module_Manager

class Create_New_Module(Python_Module_Manager):
	def __init__(self):
		super().__init__()

		self.Ask_For_Module_Info()
		self.Define_Variables()
		self.Write_To_Files()
		self.Add_To_Script_Selector()
		self.Create_Module_Bat()
		self.Add_To_ConEmu_Tasks()
		self.Show_Module_Info()

	def Ask_For_Module_Info(self):
		self.module_name = Select_Choice(Language_Item_Definer("Type the name of the new Python module", "Digite o nome do novo módulo de Python"), second_space = False)

		self.module_name = self.module_name.title()

		if " " in self.module_name:
			self.module_name = self.module_name.replace(" ", "_")

		self.show_text = Language_Item_Definer("Type the descriptions of the Python module in {} and {}, in two lines", "Digite as descrições do módulo de Python em {} e {}, em duas linhas").format(full_languages_translated_dict["English"][Language_Item_Definer(1, 2)], full_languages_translated_dict["Português Brasileiro"][Language_Item_Definer(1, 2)]) + ":"
		self.module_descriptions_prototype = Text_Writer(self.show_text, finish_text = "default_list", return_list = True, capitalize_lines = True, second_space = False)

		self.module_descriptions = {}

		i = 0
		for full_language in full_languages_not_none:
			self.module_descriptions[full_language] = self.module_descriptions_prototype[i]

			i += 1

		self.show_text = Language_Item_Definer("Type the classes of the Python module in English, separated by lines", "Digite as classes do módulo de Python em Inglês, separadas por linhas") + ":"
		self.classes = Text_Writer(self.show_text, finish_text = "default_list", return_list = True, capitalize_lines = True, second_space = False)

		i = 0
		for class_ in self.classes:
			if "_" not in class_:
				class_ = class_.title().replace(" ", "_")

			self.classes[i] = class_

			i += 1

		self.class_descriptions = {}

		for full_language in full_languages_not_none:
			self.show_text = Language_Item_Definer("Type the descriptions of classes in {}, separated by lines", "Digite as descrições das classes em {}, separadas por linhas").format(full_languages_translated_dict[full_language][Language_Item_Definer(1, 2)])
			self.class_descriptions[full_language] = Text_Writer(self.show_text, finish_text = "default_list", return_list = True, capitalize_lines = True, second_space = False)

		i = 0
		for class_description in self.class_descriptions["English"]:
			if class_description == "":
				self.class_descriptions["English"][i] = Capitalize_First_Letter(self.classes[i].replace("_", " ").lower())

			i += 1

		print()

	def Define_Variables(self):
		self.script_folder = self.modules_folder + self.module_name + "/"
		Create_Folder(self.script_folder, self.global_switches["create_folders"])

		self.root_python_file = self.script_folder + "__init__.py"
		Create_Text_File(self.root_python_file, self.global_switches["create_files"])

		self.script_main_class_folder = self.script_folder + self.module_name + "/"
		Create_Folder(self.script_main_class_folder, self.global_switches["create_folders"])

		self.main_class_python_file = self.script_main_class_folder + "__init__.py"
		Create_Text_File(self.main_class_python_file, self.global_switches["create_files"])

		self.class_folders = {}
		self.class_files = {}

		self.classes_string = ""
		self.class_descriptions_string = ""
		self.import_classes_string = ""

		i = 0
		for class_ in self.classes:
			class_folder = self.script_folder + Remove_Non_File_Characters(class_) + "/"
			Create_Folder(class_folder, self.global_switches["create_folders"])

			init_file = class_folder + "__init__.py"
			Create_Text_File(init_file, self.global_switches["create_files"])

			self.class_folders[class_] = class_folder
			self.class_files[class_] = init_file

			self.classes_string += "\t" + class_ + ","

			self.class_descriptions_string += "\t" + "Language_Item_Definer(\"{}\", \"{}\"),".format(self.class_descriptions["English"][i], self.class_descriptions["Português Brasileiro"][i])

			self.import_classes_string += "from {}.{} import {} as {}".format(self.module_name, class_, class_, class_)

			if class_ != list(self.classes)[-1]:
				self.classes_string += "\n"
				self.class_descriptions_string += "\n"
				self.import_classes_string += "\n"

			i += 1

	def Write_To_Files(self):
		self.python_root_code = self.python_root_code_template.format(self.module_name, self.import_classes_string, self.module_name, self.classes_string, self.class_descriptions_string, self.module_descriptions["English"], self.module_descriptions["Português Brasileiro"])
		Write_To_File(self.root_python_file, self.python_root_code)

		self.python_main_class_code = self.python_main_class_code_template.replace("[]", self.module_name)
		Write_To_File(self.main_class_python_file, self.python_main_class_code)

		for class_ in self.classes:
			class_file = self.class_files[class_]

			self.python_sub_class_code = self.python_sub_class_code_template.format(class_, self.module_name, self.module_name, self.module_name, self.module_name, class_, self.module_name)

			Write_To_File(class_file, self.python_sub_class_code, self.global_switches)

	def Add_To_Script_Selector(self):
		self.script_selector_python = self.script_selector_python.replace('\tadd_import = ""', "\timport {}".format(self.module_name) + "\n" + '\tadd_import = ""')

		self.script_selector_python = self.script_selector_python.replace('add_argument = ""', 'script_selector_parser.add_argument("-{}", action="store_true", help="Runs the {}.py script.")'.format(self.module_name.lower(), self.module_name) + "\n\n" + 'add_argument = ""')

		self.script_selector_python += "\n\n" + '''if script_selector_arguments.{}:
	has_arguments = True

	import {}

	{}.Function_Choose()'''.format(self.module_name.lower(), self.module_name, self.module_name)

		Write_To_File(self.script_selector_python_file, self.script_selector_python, self.global_switches)

	def Create_Module_Bat(self):
		self.bat_file = self.shortcuts_folder + self.module_name + ".bat"
		Create_Text_File(self.bat_file, self.global_switches["create_files"])

		text_to_write = 'cd "C:\Program Files\ConEmu"' + "\n" + 'start ConEmu.exe -Dir "C:\Apps" -Title "[Name]" -FontSize 25 -run {[Module]}'
		text_to_write = text_to_write.replace("[Name]", self.module_name.replace("_", " ")).replace("[Module]", self.module_name.replace(" ", "_"))
		Write_To_File(self.bat_file, text_to_write, self.global_switches)

	def Add_To_ConEmu_Tasks(self):
		self.module_execution_line = "python C:\Apps\SS.py -{}".format(self.module_name.lower())

		self.last_module_xml = Read_String(self.last_module_xml_file)
		self.last_task_number = Create_Array_Of_File(self.last_task_number_file)[0]

		self.next_task_number = str(int(self.last_task_number) + 1)
		self.next_module_xml = self.conemu_task_xml_template.replace("[Number]", self.next_task_number)
		self.next_module_xml = self.next_module_xml.replace("[Script_Name]", self.module_name.replace(" ", "_"))
		self.next_module_xml = self.next_module_xml.replace("[module_execution_line]", self.module_execution_line)

		Copy_Text(self.next_module_xml)

		self.conemu_xml_text = Read_String(self.conemu_xml_file)

		self.conemu_xml_text = self.conemu_xml_text.replace(self.last_module_xml, self.last_module_xml + "\n" + self.next_module_xml)

		self.conemu_xml_text = self.conemu_xml_text.replace('<value name="Count" type="long" data="{}"/>'.format(self.last_task_number), '<value name="Count" type="long" data="{}"/>'.format(self.next_task_number))

		Write_To_File(self.conemu_xml_file, self.conemu_xml_text)

		Write_To_File(self.last_task_number_file, self.next_task_number, self.global_switches)

		Write_To_File(self.last_module_xml_file, self.next_module_xml, self.global_switches)

	def Show_Module_Info(self):
		self.large_bar = "-----"
		self.dash_space = "-"

		print(self.large_bar)
		print()
		print(Language_Item_Definer("Module Name", "Nome do Módulo") + ":")
		print(self.module_name)
		print()

		print(Language_Item_Definer("Module Descriptions", "Descrições do Módulo") + ":")

		for full_language in full_languages_not_none:
			print(self.module_descriptions[full_language])

		print()

		print(Language_Item_Definer("Classes and their descriptions", "Classes e suas descrições") + ":")

		i = 0
		for class_ in self.classes:
			print()
			print("\"" + class_ + "\":")
			print("[" + self.class_descriptions["English"][i])
			print(self.class_descriptions["Português Brasileiro"][i] + "]")

			i += 1

		print()

		print(self.large_bar)
		print()
		input(Language_Item_Definer("Press Enter when you finish reading the Info Summary", "Pressione Enter quando terminar de ler o Resumo de Informações") + ": ")