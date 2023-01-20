# Python.py

from Global_Switches import Global_Switches as Global_Switches

from Language import Language as Language
from File import File as File
from Folder import Folder as Folder
from Date import Date as Date
from Input import Input as Input
from JSON import JSON as JSON
from Text import Text as Text

class Python(object):
	def __init__(self, parameter_switches = None):
		self.parameter_switches = parameter_switches

		self.Global_Switches = Global_Switches()

		self.Define_Basic_Variables()
		self.Define_Module_Folder()
		self.Define_Texts()

		self.Define_Files()
		self.Define_Lists()

	def Define_Basic_Variables(self):
		# Global Switches dictionary
		self.global_switches = Global_Switches().global_switches

		if self.parameter_switches != None:
			self.global_switches.update(self.parameter_switches)

		self.Language = Language(self.global_switches)
		self.File = File(self.global_switches)
		self.Folder = Folder(self.global_switches)
		self.Date = Date(self.global_switches)
		self.Input = Input(self.global_switches)
		self.JSON = JSON(self.global_switches)
		self.Text = Text(self.global_switches)

		self.app_settings = self.Language.app_settings
		self.languages = self.Language.languages
		self.small_languages = self.languages["small"]
		self.full_languages = self.languages["full"]
		self.translated_languages = self.languages["full_translated"]

		self.user_language = self.Language.user_language
		self.full_user_language = self.Language.full_user_language

		self.Sanitize = self.File.Sanitize

		self.folders = self.Folder.folders
		self.root_folders = self.folders["root"]
		self.user_folders = self.folders["user"]
		self.apps_folders = self.folders["apps"]
		self.mega_folders = self.folders["mega"]
		self.notepad_folders = self.folders["notepad"]

		self.date = self.Date.date

	def Define_Module_Folder(self):
		self.module = {
			"name": self.__module__,
		}

		if "." in self.module["name"]:
			self.module["name"] = self.module["name"].split(".")[0]

		self.module["key"] = self.module["name"].lower()

		self.apps_folders["modules"][self.module["key"]] = {
			"root": self.apps_folders["modules"]["root"] + self.module["name"] + "/",
		}

		self.apps_folders["module_files"][self.module["key"]] = {
			"root": self.apps_folders["module_files"]["root"] + self.module["name"] + "/",
		}

		for item in ["module_files", "modules"]:
			self.apps_folders[item][self.module["key"]] = self.apps_folders[item]["root"] + self.module["name"] + "/"
			self.apps_folders[item][self.module["key"]] = self.Folder.Contents(self.apps_folders[item][self.module["key"]], lower_key = True)["dictionary"]

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.apps_folders["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.Language.Item(self.texts)

		self.large_bar = "-----"
		self.dash_space = "-"

		self.conemu_task_xml_template = """				<key name="Task[Number]" modified="2022-02-08 14:24:07" build="210912">
					<value name="Name" type="string" data="{[Module_Name]}"/>
					<value name="Flags" type="dword" data="00000004"/>
					<value name="Hotkey" type="dword" data="00000000"/>
					<value name="GuiArgs" type="string" data=""/>
					<value name="Active" type="long" data="0"/>
					<value name="Count" type="long" data="1"/>
					<value name="Cmd1" type="string" data="[module_execution_line]"/>
				</key>"""

		self.conemu_bat_template = 'cd "C:\Program Files\ConEmu"' + "\n" + 'start ConEmu.exe -Dir "C:\Apps" -Title "[Name]" -FontSize 25 -run {[Module]}'

	def Define_Files(self):
		self.root_code_template_file = self.apps_folders["module_files"][self.module["key"]]["root"] + "Root code template.txt"
		self.File.Create(self.root_code_template_file)

		self.main_class_code_template_file = self.apps_folders["module_files"][self.module["key"]]["root"] + "Main class code template.txt"
		self.File.Create(self.main_class_code_template_file)

		self.sub_class_code_template_file = self.apps_folders["module_files"][self.module["key"]]["root"] + "Sub class code template.txt"
		self.File.Create(self.sub_class_code_template_file)

		self.last_module_xml_file = self.apps_folders["module_files"][self.module["key"]]["root"] + "Last module XML.txt"
		self.File.Create(self.last_module_xml_file)

		self.last_task_number_file = self.apps_folders["module_files"][self.module["key"]]["root"] + "Last task number.txt"
		self.File.Create(self.last_task_number_file)

		self.conemu_xml_file = self.user_folders["appdata"]["roaming"] + "ConEmu.xml"
		self.File.Create(self.conemu_xml_file)

		self.module_types = [
			"utility_modules",
			"usage_modules",
		]

		self.module_files = {}

		for key in self.module_types:
			language_type = self.language_texts[key]

			self.module_files[language_type] = self.apps_folders["modules"]["root"] + self.Text.Capitalize(self.texts[key]["en"]) + ".txt"

	def Define_Lists(self):
		self.root_code_template = self.File.Contents(self.root_code_template_file)["string"]
		self.main_class_code_template = self.File.Contents(self.main_class_code_template_file)["string"]
		self.sub_class_code_template = self.File.Contents(self.sub_class_code_template_file)["string"]