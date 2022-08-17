# Add_Python_Apps_To_Remote.py

from Script_Helper import *

from Unified_Remote_Manager.Unified_Remote_Manager import Unified_Remote_Manager as Unified_Remote_Manager

class Add_Python_Apps_To_Remote(Unified_Remote_Manager):
	def __init__(self):
		super().__init__()

		self.shortcuts_folder = scripts_folder + "Atalhos/"

		self.layout_xml_file = self.apps_remote_folder + "layout.xml"
		self.remote_lua = self.apps_remote_folder + "remote.lua"

		self.List_Files()
		self.Define_Strings()
		self.Add_To_Layout()
		self.Add_To_Remote()
		self.Write_To_Files()

	def List_Files(self):
		self.shortcuts = List_Files(self.shortcuts_folder, add_none = False)
		self.shortcuts_names = List_Filenames(self.shortcuts_folder, add_none = False)

	def Define_Strings(self):
		self.layout_contents = '<?xml version="1.0" encoding="utf-8"?>\n<layout>\n\t<tabs>\n\t\t<tab text="Apps">\n{}\n\t\t</tab>\n\t</tabs>\n</layout>'

		self.layout_row_template = '\t\t\t<row>\n\t\t\t\t<button text="{}" ontap="{}" />\n\t\t\t</row>'

		self.layout_rows = ""

		self.remote_contents = "-- Documentation\n-- http://www.unifiedremote.com/api\n\n-- OS Library\n-- http://www.unifiedremote.com/api/libs/os\n\n-- Written in: \"{}\"\n\nio.popen(\"C:/Apps/Module/Unified_Remote_Manager/__init__.pyw\");\n\n".format(time.strftime("%H:%M %d/%m/%Y"))

		self.remote_action_template = "actions[\"{}\"] = function ()\n\tio.popen(\"{}\");\nend;"

		self.remote_actions = ""

	def Add_To_Layout(self):
		i = 0
		for shortcut in self.shortcuts:
			shortcut_name = self.shortcuts_names[i]

			self.layout_rows += self.layout_row_template.format(shortcut_name.replace("_", " "), shortcut_name)

			if shortcut_name != self.shortcuts_names[-1]:
				self.layout_rows += "\n"

			i += 1

		self.layout_contents = self.layout_contents.format(self.layout_rows)

	def Add_To_Remote(self):
		i = 0
		for shortcut in self.shortcuts:
			shortcut_name = self.shortcuts_names[i]

			self.remote_actions += self.remote_action_template.format(shortcut_name, shortcut)

			if shortcut_name != self.shortcuts_names[-1]:
				self.remote_actions += "\n\n"

			i += 1

		self.remote_contents += self.remote_actions

	def Write_To_Files(self):
		if Read_String(self.layout_xml_file) != self.layout_contents:
			Write_To_File(self.layout_xml_file, self.layout_contents, self.global_switches)

		if Read_String(self.remote_lua) != self.remote_contents:
			Write_To_File(self.remote_lua, self.remote_contents, self.global_switches)