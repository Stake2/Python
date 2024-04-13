# Python.py

class Python(object):
	def __init__(self):
		# Define the module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.Define_Basic_Variables()

		self.Define_Texts()

		self.Define_Files()
		self.Define_Lists()

	def Define_Basic_Variables(self):
		from copy import deepcopy

		# Import the JSON module
		from Utility.JSON import JSON as JSON

		self.JSON = JSON()

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

		# Get the modules list
		self.modules = self.JSON.To_Python(self.folders["apps"]["modules"]["modules"])

		# Import the "importlib" module
		import importlib

		# Create a list of the modules that will not be imported
		remove_list = [
			"Define_Folders",
			"Language"
		]

		# Iterate through the Utility modules
		for module_title in self.modules["Utility"]["List"]:
			# If the module title is not inside the remove list
			if module_title not in remove_list:
				# Import the module
				module = importlib.import_module("." + module_title, "Utility")

				# Get the sub-class
				sub_class = getattr(module, module_title)

				# Add the sub-class to the current module
				setattr(self, module_title, sub_class())

		# Make a backup of the module folders
		self.module_folders = {}

		for item in ["modules", "module_files"]:
			self.module_folders[item] = deepcopy(self.folders["apps"][item][self.module["key"]])

		# Define the local folders dictionary as the Folder folders dictionary
		self.folders = self.Folder.folders

		# Restore the backup of the module folders
		for item in ["modules", "module_files"]:
			self.folders["apps"][item][self.module["key"]] = self.module_folders[item]

		# Get the switches dictionary from the "Global Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# Get the Languages dictionary
		self.languages = self.JSON.Language.languages

		# Get the user language and full user language
		self.user_language = self.JSON.Language.user_language
		self.full_user_language = self.JSON.Language.full_user_language

		# Get the Sanitize method of the File class
		self.Sanitize = self.File.Sanitize

		# Get the current date from the Date module
		self.date = self.Date.date

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.JSON.Language.Item(self.texts)

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

		self.conemu_bat_template = 'cd "C:\Program Files\ConEmu"' + "\n" + 'start ConEmu.exe -Dir "C:\Apps" -Title "[Name]" -FontSize 12 -run {[Module]}'

	def Define_Files(self):
		self.folders["modules_file"] = self.folders["apps"]["modules"]["modules"]

		self.modules = self.JSON.To_Python(self.folders["modules_file"])

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