# Create_New_Module.py

from Python.Python import Python as Python

class Create_New_Module(Python):
	def __init__(self):
		super().__init__()

		self.Ask_For_Module_Info()
		self.Create_Folders_And_Files()
		self.Write_To_Files()
		self.Create_Module_Bat()
		self.Add_To_ConEmu_Tasks()
		self.Add_To_Modules_List()
		self.Change_Global_Switches()
		self.Show_Module_Information()

	def Ask_For_Module_Info(self):
		# Show a space and a five dash separator
		print()
		print(self.separators["5"])

		# Ask for the module name
		self.module_name = self.Input.Type(self.language_texts["type_the_name_of_the_new_python_module"])

		# Replace spaces with underscores on the module name
		if " " in self.module_name:
			self.module_name = self.module_name.replace(" ", "_")

		# Get the module key
		self.module["key"] = self.module_name.lower()

		# ---------- #

		# Module descriptions

		# Make a list of the translated languages in the user language
		self.translated_languages = []

		# Iterate through the language keys and dictionaries
		for small_language, language in self.languages["Dictionary"].items():
			# Get the current language translated to the user language
			translated_language = language["Translated"][self.language["Small"]]

			# Add the translated language in the user language to the local list of translated languages
			self.translated_languages.append("[" + translated_language + "]")

		# Define the lines text, which shows the number of languages
		self.lines_text = self.language_texts["{}_lines_in_this_order"].format(self.Date.language_texts["number_names_feminine, type: list"][len(self.languages["Small"])])

		# Define the show text for the descriptions of the module
		show_text = "\n" + self.language_texts["type_the_{}_of_the_python_module_in_{}"].format(self.language_texts["descriptions"], self.lines_text) + ": "

		# Show a five dash separator
		print()
		print(self.separators["5"])

		# Ask for the user to type the module descriptions in all languages
		prototype = self.Input.Lines(show_text, length = 2, line_options_parameter = {"enumerate": True, "enumerate_text": False, "capitalize": True}, line_texts = self.translated_languages, first_space = False)["lines"]

		# Define and fill the module descriptions dictionary
		self.module_descriptions = {}

		# Iterate through list of small languages
		i = 0
		for small_language in self.languages["Small"]:
			# Get the language description
			self.module_descriptions[small_language] = prototype[i]

			# If the local language is "en" (English)
			# And the English module description is empty
			if (
				small_language == "en" and
				prototype[i] == ""
			):
				# Then define the module description in English as the module name
				self.module_descriptions[small_language] = self.Text.Title(self.module_name.replace("_", " "))

			i += 1

		# ---------- #

		# Classes

		# Get the English language dictionary
		english = self.languages["Dictionary"]["en"]

		# Get the English language translated to the user language
		translated_english = english["Translated"][self.language["Small"]]

		# Define the show text for the classes of the module
		show_text = self.language_texts["type_the_{}_of_the_python_module_in_{}"].format(self.language_texts["classes"], translated_english + ", " + self.language_texts["separated_by_lines"]) + ": "

		# Ask for the user to type the classes of the module
		classes_list = self.Input.Lines(show_text, line_options_parameter = {"enumerate": True, "enumerate_text": False, "capitalize": True})["lines"]

		# Update the classes list
		i = 0
		for class_name in classes_list:
			if " " in class_name:
				classes_list[i] = class_name.replace(" ", "_")

		# Create the empty classes dictionary
		self.classes = {
			"List": classes_list,
			"Dictionary": {}
		}

		# Iterate through the classes list
		i = 0
		for class_name in classes_list:
			# Replace spaces with underscores on the class name
			if " " in class_name:
				class_name = class_name.replace(" ", "_")

			# Create the class dictionary inside the classes dictionary
			self.classes["Dictionary"][class_name] = {
				"Name": class_name,
				"Descriptions": {},
				"Folder": {},
				"File": {}
			}

			i += 1

		# ---------- #

		# Class descriptions

		# Define and fill the module class descriptions dictionary
		self.class_descriptions = {}

		# Iterate through the language keys and dictionaries
		for small_language, language in self.languages["Dictionary"].items():
			# Get the current language translated to the user language
			translated_language = language["Translated"][self.language["Small"]]

			# Define the show text, with the description of classes, separated by lines
			show_text = self.language_texts["type_the_{}_of_the_python_module_in_{}"].format(self.language_texts["descriptions_of_classes"], translated_language + ", " + self.language_texts["separated_by_lines"]) + ":"

			# Ask for the descriptions of the classes
			self.class_descriptions[small_language] = self.Input.Lines(show_text, length = len(self.classes["List"]), line_options_parameter = {"enumerate": True, "enumerate_text": False, "capitalize": True})["lines"]

		# Iterate through the classes list
		i = 0
		for class_name in self.classes["List"]:
			# Add the class descriptions in all languages to the class descriptions dictionary
			for small_language in self.languages["Small"]:
				self.classes["Dictionary"][class_name]["Descriptions"][small_language] = self.class_descriptions[small_language][i]

			i += 1

		# Fill the class descriptions that are empty
		for class_name in self.classes["List"]:
			class_dictionary = self.classes["Dictionary"][class_name]

			if class_dictionary["Descriptions"]["en"] == "":
				class_dictionary["Descriptions"]["en"] = self.Text.Capitalize(class_name.replace("_", " ").lower())

		# Show a space separator
		print()

	def Create_Folders_And_Files(self):
		# Define and create the module folder
		self.module_folder = self.folders["Apps"]["Modules"]["root"] + self.module_name + "/"
		self.Folder.Create(self.module_folder)

		# Define and create the root Python file
		self.root_python_file = self.module_folder + "__init__.py"
		self.File.Create(self.root_python_file)

		# Define and create the descriptions file
		self.descriptions_file = self.module_folder + "Descriptions.json"
		self.File.Create(self.descriptions_file)

		# Define and create the main class folder
		self.main_class_folder = self.module_folder + self.module_name + "/"
		self.Folder.Create(self.main_class_folder)

		# Define and create the main class Python file
		self.main_class_python_file = self.main_class_folder + "__init__.py"
		self.File.Create(self.main_class_python_file)

		# Define the module folder inside the "Module files" folder
		self.folders["Apps"]["Module files"][self.module["key"]] = {
			"root": self.folders["Apps"]["Module files"]["root"] + self.module_name + "/"
		}

		# Create it
		self.Folder.Create(self.folders["Apps"]["Module files"][self.module["key"]]["root"])

		# Define and create the "Texts.json" file inside the module folder that is inside the "Module files" folder
		self.folders["Apps"]["Module files"][self.module["key"]]["texts"] = self.folders["Apps"]["Module files"][self.module["key"]]["root"] + "Texts.json"
		self.File.Create(self.folders["Apps"]["Module files"][self.module["key"]]["texts"])

		# ---------- #

		self.class_folders = {}
		self.class_files = {}

		# Iterate through the classes in the classes list
		for class_name in self.classes["List"]:
			# Define and create the class folder
			self.classes["Dictionary"][class_name]["Folder"] = self.module_folder + self.Sanitize(class_name, restricted_characters = True) + "/"
			self.Folder.Create(self.classes["Dictionary"][class_name]["Folder"])

			# Define and create the class Python init file
			self.classes["Dictionary"][class_name]["File"] = self.classes["Dictionary"][class_name]["Folder"] + "__init__.py"
			self.File.Create(self.classes["Dictionary"][class_name]["File"])

	def Write_To_Files(self):
		# Format the root code template
		root_code = self.python["Templates"]["Root"].replace("[module_name]", self.module_name)

		# Write to the root "__init__.py" Python file
		self.File.Edit(self.root_python_file, root_code, "w")

		# ---------- #

		# Define the Descriptions dictionary
		self.descriptions = {
			"Show text": self.module_descriptions
		}

		# Iterate through the classes in the classes dictionary
		for class_dictionary in self.classes["Dictionary"].values():
			# Define the class name variable for easier typing
			class_name = class_dictionary["Name"]

			# Add the descriptions of the class to the root Descriptions dictionary
			self.descriptions[class_name] = class_dictionary["Descriptions"]

		# Write to the "Descriptions.json"
		self.JSON.Edit(self.descriptions_file, self.descriptions)

		# ---------- #

		# Format the main class code template
		self.main_class_code = self.python["Templates"]["Main class"].replace("[module_name]", self.module_name)

		# Write to the main class Python file
		self.File.Edit(self.main_class_python_file, self.main_class_code, "w")

		# ---------- #

		# Define the template
		template = self.python["Templates"]["Sub-class"]

		# Iterate through the classes in the classes dictionary
		for class_dictionary in self.classes["Dictionary"].values():
			# Get the class file
			file = class_dictionary["File"]

			# Define the list of items to use to format the template
			items = [
				class_dictionary["Name"],
				self.module_name,
				self.module_name,
				self.module_name,
				self.module_name,
				class_dictionary["Name"],
				self.module_name
			]

			# Format the sub-class code template with the list of items
			sub_class_code = template.format(*items)

			# Write to the class code file
			self.File.Edit(file, sub_class_code, "w")

		# ---------- #

		# Write to the "Texts.json" file
		self.File.Edit(self.folders["Apps"]["Module files"][self.module["key"]]["texts"], "{\n\t\n}", "w")

	def Create_Module_Bat(self):
		# Define and create the module bat file
		bat_file = self.folders["Apps"]["Shortcuts"]["root"] + self.module_name + ".bat"
		self.File.Create(bat_file)

		bat_text = self.python["Templates"]["Bat"]

		# Format the ConEmu bat template
		# Adding the name of the module and the module folder name
		bat_text = bat_text.replace("[Name]", self.module_name.replace("_", " "))
		bat_text = bat_text.replace("[Module]", self.module_name.replace(" ", "_"))

		# Write to the bat file
		self.File.Edit(bat_file, bat_text, "w")

	def Add_To_ConEmu_Tasks(self):
		# Get the last task number
		last_task_number = self.File.Contents(self.python["Files"]["Task number"])["lines"][0]

		# Add one to it
		next_task_number = str(int(last_task_number) + 1)

		# Write to the "Last task number" file
		self.File.Edit(self.python["Files"]["Task number"], next_task_number, "w")

		# ---------- #

		# Update the "Last module" file

		# Define the module execution line
		module_execution_line = "py C:\Apps\MS.py -{}".format(self.module_name.lower())

		# Format the ConEmu task XML template
		# Updating the number of the task
		# Adding the module name and execution line
		current_module_xml = self.python["Templates"]["Task"].replace("[Number]", next_task_number)
		current_module_xml = current_module_xml.replace("[Module_Name]", self.module_name.replace(" ", "_"))
		current_module_xml = current_module_xml.replace("[module_execution_line]", module_execution_line)

		# Write to the "Last module" file
		self.File.Edit(self.python["Files"]["Last module"], current_module_xml, "w")

		# ---------- #

		# Update the "ConEmu XML" file

		# Get the last module XML
		last_module_xml = self.File.Contents(self.python["Files"]["Last module"])["string"]

		# Read the text of the "ConEmu.xml" file
		conemu_xml_text = self.File.Contents(self.python["Files"]["ConEmu"])["string"]

		# Update the ConEmu text to add the XML dictionary of the newly added module
		conemu_xml_text = conemu_xml_text.replace(last_module_xml, last_module_xml + "\n" + current_module_xml)

		# Update the value of the "Count" number, which is the number of tasks inside the ConEmu configuration file
		value_count_template = '<value name="Count" type="long" data="{}"/>'

		# Replace the number of tasks line inside the ConEmu text, with the new number of tasks
		conemu_xml_text = conemu_xml_text.replace(value_count_template.format(last_task_number), value_count_template.format(next_task_number))

		# Update the "ConEmu.xml" file
		self.File.Edit(self.python["Files"]["ConEmu"], conemu_xml_text, "w")

	def Add_To_Modules_List(self):
		# If the module name is not inside the list of usage modules
		if self.module_name not in self.python["Modules"]["Dictionary"]["Usage"]["List"]:
			# Add it
			self.python["Modules"]["Dictionary"]["Usage"]["List"].append(self.module_name)

		# Sort the lists of utility and usage modules
		for key in self.python["Modules"]["Types"]["List"]:
			self.python["Modules"]["Dictionary"][key]["List"] = sorted(self.python["Modules"]["Dictionary"][key]["List"], key = str.lower)

		# Update the "Modules.json" file with the updated "Modules" dictionary
		self.JSON.Edit(self.python["Files"]["Modules"], self.python["Modules"]["Dictionary"])

	def Change_Global_Switches(self):
		# Get the switches file
		self.switches_file = self.Global_Switches.switches["File"]

		# Read it
		self.switches["Global"] = self.JSON.To_Python(self.switches_file)

		# Change the testing and verbose switches to True
		self.switches["Global"]["testing"] = True
		self.switches["Global"]["versbose"] = True

		# Switch the global switches, using the modified switches above
		self.Global_Switches.Switch(self.switches["Global"])

	def Show_Module_Information(self):
		# Show a five dash separator
		print(self.separators["5"])
		print()

		# Show the module name
		print(self.language_texts["module_name"] + ":")
		print("\t" + self.module_name)
		print()

		# Show the "Module descriptions" text and an opening bracket
		print(self.language_texts["module_descriptions"] + " = {")

		# Iterate through the language keys and dictionaries
		for small_language, language in self.languages["Dictionary"].items():
			# Get the current language translated to the user language
			translated_language = language["Translated"][self.language["Small"]]

			# Add quotes and a colon around the translated language
			translated_language = '"' + translated_language + '": '

			# Define the text with the translated language and the module description
			text = "\t" + translated_language + '"' + self.module_descriptions[small_language] + '"'

			# If the language is not the last one
			if small_language != self.languages["Small"][-1]:
				# Add a comma to the text
				text += ","

			# Show the translated language and module description text
			print(text)

		# Show the closing bracket and a space
		print("}")
		print()

		# Show the "Classes and their descriptions" text
		print(self.language_texts["classes_and_their_descriptions"] + ":")

		# Define the template text
		template = "{}" + '"{}"'

		# Iterate through the classes inside the classes dictionary
		for class_dictionary in self.classes["Dictionary"].values():
			# Define the class name variable for easier typing
			class_name = class_dictionary["Name"]

			# Show the name of the class and an opening bracket
			print("\t" + class_name + " = {")

			# Iterate through the language keys and dictionaries
			for small_language, language in self.languages["Dictionary"].items():
				# Get the current language translated to the user language
				translated_language = language["Translated"][self.language["Small"]]

				# Add quotes and a colon around the translated language
				translated_language = '"' + translated_language + '": '

				# If the class is not the first one
				if class_name != self.classes["List"][0]:
					# Show a space separator
					print()
	
				# Format the template text with the translated language and the class descriptions
				text = "\t\t" + template.format(translated_language, class_dictionary["Descriptions"][small_language])

				# If the language is not the last one
				if small_language != self.languages["Small"][-1]:
					# Add a comma to the text
					text += ","

				# Show the formatted template
				print(text)

			# Show a closing bracket with a tab
			print("\t" + "}")

		# Show space separators and a five dash separator
		print()
		print(self.separators["5"])