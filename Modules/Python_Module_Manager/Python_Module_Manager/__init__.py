# Python_Module_Manager.py

from Script_Helper import *

from os.path import expanduser

class Python_Module_Manager(object):
	def __init__(self, parameter_switches = None):
		# Verbose variable
		self.verbose = False

		self.testing_script = False

		self.parameter_switches = parameter_switches

		self.Define_Basic_Variables()
		self.Define_Folders_And_Files()
		self.Define_Texts()

	def Define_Basic_Variables(self):
		self.option = True

		# Global Switches dictionary
		self.global_switches = {
			"write_to_file": self.option,
			"create_files": self.option,
			"create_folders": self.option,
			"move_files": self.option,
			"verbose": self.verbose,
			"testing_script": self.testing_script,
		}

		if self.parameter_switches != None:
			self.global_switches = self.parameter_switches
			self.testing_script = self.global_switches["testing_script"]

		if self.global_switches["testing_script"] == True:
			print(Language_Item_Definer("Testing script: Yes", "Testando script: Sim"))

		if self.global_switches["verbose"] == True:
			print(Language_Item_Definer("Verbose on", "Verbose ligado") + ".")

		if self.global_switches["testing_script"] == True:
			self.global_switches["write_to_file"] = False
			self.global_switches["create_files"] = False

		self.dot_text = ".txt"

	def Define_Folders_And_Files(self):
		self.scripts_folder = scripts_folder
		self.modules_folder = self.scripts_folder + "Modules/"
		self.script_text_files_folder = self.scripts_folder + "Script Text Files/"
		self.shortcuts_folder = self.scripts_folder + "Atalhos/"

		name = __name__

		if "." in __name__:
			name = __name__.split(".")[0]

		self.module_text_files_folder = self.script_text_files_folder + name + "/"
		Create_Folder(self.module_text_files_folder, self.global_switches)

		self.python_root_code_template_file = self.module_text_files_folder + "Python Root Code Template" + self.dot_text
		self.python_main_class_code_template_file = self.module_text_files_folder + "Python Main Class Code Template" + self.dot_text
		self.python_sub_class_code_template_file = self.module_text_files_folder + "Python Sub Class Code Template" + self.dot_text

		self.python_root_code_template = Read_String(self.python_root_code_template_file)
		self.python_main_class_code_template = Read_String(self.python_main_class_code_template_file)
		self.python_sub_class_code_template = Read_String(self.python_sub_class_code_template_file)

		self.last_module_xml_file = self.module_text_files_folder + "Last Module XML" + self.dot_text
		self.last_task_number_file = self.module_text_files_folder + "Last Task Number" + self.dot_text

		self.script_selector_python_file = self.scripts_folder + "SS.py"
		self.script_selector_python = Read_String(self.script_selector_python_file)

		self.conemu_xml_file = Sanitize_File_Path(expanduser("~")) + "AppData/Roaming/ConEmu.xml"

	def Define_Texts(self):
		self.conemu_task_xml_template = """				<key name="Task[Number]" modified="2022-02-08 14:24:07" build="210912">
					<value name="Name" type="string" data="{[Module_Name]}"/>
					<value name="Flags" type="dword" data="00000004"/>
					<value name="Hotkey" type="dword" data="00000000"/>
					<value name="GuiArgs" type="string" data=""/>
					<value name="Active" type="long" data="0"/>
					<value name="Count" type="long" data="1"/>
					<value name="Cmd1" type="string" data="[module_execution_line]"/>
				</key>"""

		self.type_the_text = Language_Item_Definer("Type the {} of the Python module in {}", "Digite as {} do módulo de Python em {}")
		self.conemu_bat_template = 'cd "C:\Program Files\ConEmu"' + "\n" + 'start ConEmu.exe -Dir "C:\Apps" -Title "[Name]" -FontSize 25 -run {[Module]}'