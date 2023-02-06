# Python.py

class Python(object):
	def __init__(self):
		self.Import_Modules()
		self.Define_Module_Folder()
		self.Define_Texts()

		self.Define_Files()
		self.Define_Lists()

	def Import_Modules(self):
		from Utility.Modules import Modules as Modules

		# Get modules dictionary
		self.modules = Modules().Set(self)

	def Define_Module_Folder(self):
		self.module = {
			"name": self.__module__,
		}

		if "." in self.module["name"]:
			self.module["name"] = self.module["name"].split(".")[0]

		self.module["key"] = self.module["name"].lower()

		for item in ["module_files", "modules"]:
			self.folders["apps"][item][self.module["key"]] = self.folders["apps"][item]["root"] + self.module["name"] + "/"
			self.Folder.Create(self.folders["apps"][item][self.module["key"]])

			self.folders["apps"][item][self.module["key"]] = self.Folder.Contents(self.folders["apps"][item][self.module["key"]], lower_key = True)["dictionary"]

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

		self.conemu_xml_file = self.folders["user"]["appdata"]["roaming"]["root"] + "ConEmu.xml"
		self.File.Create(self.conemu_xml_file)

	def Define_Lists(self):
		self.root_code_template = self.File.Contents(self.root_code_template_file)["string"]
		self.main_class_code_template = self.File.Contents(self.main_class_code_template_file)["string"]
		self.sub_class_code_template = self.File.Contents(self.sub_class_code_template_file)["string"]