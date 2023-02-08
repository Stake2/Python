# Python.py

from Utility.Global_Switches import Global_Switches as Global_Switches

from Utility.Language import Language as Language
from Utility.File import File as File
from Utility.Folder import Folder as Folder
from Utility.Date import Date as Date
from Utility.Input import Input as Input
from Utility.JSON import JSON as JSON
from Utility.Text import Text as Text

class Python(object):
	def __init__(self):
		self.Global_Switches = Global_Switches()

		self.Define_Basic_Variables()

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.Define_Texts()

		self.Define_Files()
		self.Define_Lists()

	def Define_Basic_Variables(self):
		self.switches = Global_Switches().switches["global"]

		self.Language = Language()
		self.File = File()
		self.Folder = Folder()
		self.Date = Date()
		self.Input = Input()
		self.JSON = JSON()
		self.Text = Text()

		self.languages = self.Language.languages

		self.user_language = self.Language.user_language
		self.full_user_language = self.Language.full_user_language

		self.Sanitize = self.File.Sanitize

		self.folders = self.Folder.folders

		self.date = self.Date.date

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

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
		self.root_code_template_file = self.folders["apps"]["module_files"][self.module["key"]]["root"] + "Root code template.txt"
		self.File.Create(self.root_code_template_file)

		self.main_class_code_template_file = self.folders["apps"]["module_files"][self.module["key"]]["root"] + "Main class code template.txt"
		self.File.Create(self.main_class_code_template_file)

		self.sub_class_code_template_file = self.folders["apps"]["module_files"][self.module["key"]]["root"] + "Sub class code template.txt"
		self.File.Create(self.sub_class_code_template_file)

		self.last_module_xml_file = self.folders["apps"]["module_files"][self.module["key"]]["root"] + "Last module XML.txt"
		self.File.Create(self.last_module_xml_file)

		self.last_task_number_file = self.folders["apps"]["module_files"][self.module["key"]]["root"] + "Last task number.txt"
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

			self.module_files[language_type] = self.folders["apps"]["modules"]["root"] + self.Text.Capitalize(self.texts[key]["en"]) + ".txt"

	def Define_Lists(self):
		self.root_code_template = self.File.Contents(self.root_code_template_file)["string"]
		self.main_class_code_template = self.File.Contents(self.main_class_code_template_file)["string"]
		self.sub_class_code_template = self.File.Contents(self.sub_class_code_template_file)["string"]