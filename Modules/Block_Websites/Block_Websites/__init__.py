# Block_Websites.py

# Import the "importlib" module
import importlib

class Block_Websites(object):
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.folders = self.Define_Folders(object = self).folders

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Import some usage classes
		self.Import_Usage_Classes()

		# Class methods
		self.Define_Files()
		self.Define_Lists()

	def Import_Classes(self):
		# Define the list of modules to be imported
		modules = [
			"Define_Folders",
			"JSON"
		]

		# Iterate through the list of modules
		for module_title in modules:
			# Import the module
			module = importlib.import_module("." + module_title, "Utility")

			# Get the sub-class
			sub_class = getattr(module, module_title)

			# If the module title is not "Define_Folders"
			if module_title != "Define_Folders":
				# Run the sub-class to define its variable
				sub_class = sub_class()

			# Add the sub-class to the current module
			setattr(self, module_title, sub_class)

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

	def Define_Basic_Variables(self):
		# Get the dictionary of modules
		self.modules = self.JSON.To_Python(self.folders["Apps"]["Modules"]["Modules"])

		# Create a list of the modules that will not be imported
		remove_list = [
			"Define_Folders",
			"Modules",
			"Language",
			"JSON"
		]

		# Iterate through the list of utility modules
		for module_title in self.modules["Utility"]["List"]:
			# If the module title is not inside the remove list
			if module_title not in remove_list:
				# Import the module
				module = importlib.import_module("." + module_title, "Utility")

				# Get the sub-class of the module
				sub_class = getattr(module, module_title)

				# Add the sub-class to the current class
				setattr(self, module_title, sub_class())

		# ---------- #

		# Get the switches dictionary from the "Global Switches" class
		self.switches = self.Global_Switches.switches["Global"]

		# ---------- #

		# Import some variables from the "Language" class

		# Import the "languages" dictionary
		self.languages = self.Language.languages

		# Import the "language" dictionary
		self.language = self.Language.language

		# Import the "separators" dictionary
		self.separators = self.Language.separators

		# ---------- #

		# Import the "folders" dictionary from the "Folder" class
		self.folders = self.Folder.folders

		# ---------- #

		# Import the "Sanitize" method from the "File" class
		self.Sanitize = self.File.Sanitize

		# ---------- #

		# Get the current date from the "Date" class
		self.date = self.Date.date

	def Define_Texts(self):
		# Define the "separators" dictionary
		self.separators = {}

		# Create separators from one to ten characters
		for number in range(1, 11):
			# Define the empty string
			string = ""

			# Add separators to it
			while len(string) != number:
				string += "-"

			# Add the string to the Separators dictionary
			self.separators[str(number)] = string

		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

		self.texts["redirect_ip"] = "127.0.0.1"
		self.texts["redirect_ip_space"] = self.texts["redirect_ip"] + "     "
		self.texts["task_name"] = "Re-Block Websites"
		self.texts["all_websites_are_unlocked_header"] = "# All websites are unlocked"
		self.texts["log"] = self.language_texts["blocking_state"] + ":\n{}\n\n" + self.language_texts["this_file_will_be_updated_every_{}_minutes_reopen_it_to_update"] + ".\n" + self.language_texts["last_update_in"] + ": {}"

		space = "               "
		bar = " --------------------------------------------- "

		self.texts["header"] = "#" + bar + "#" + "\n" \
		"#" + space + "Block_Websites.py" + space + "#" + "\n" + \
		"#" + bar + "#" + "\n\n"

	def Import_Usage_Classes(self):
		# Define the classes to be imported
		classes = [
			"Social_Networks"
		]

		# Import them
		for title in classes:
			# Import the module
			module = importlib.import_module("." + title, title)

			# Get the sub-class
			sub_class = getattr(module, title)

			# Add the sub-class to the current module
			setattr(self, title, sub_class())

	def Define_Files(self):
		self.hosts_file = self.folders["root"]["system32"]["drivers/etc"] + "hosts"

		self.additional_maps_file = self.folders["Apps"]["Module files"][self.module["key"]]["root"] + "Additional maps.txt"
		self.File.Create(self.additional_maps_file)

		self.blocked_by_default_file = self.folders["Apps"]["Module files"][self.module["key"]]["root"] + "Blocked by default.txt"
		self.File.Create(self.blocked_by_default_file)

		self.hosts_file_header_file = self.folders["Apps"]["Module files"][self.module["key"]]["root"] + "Hosts file header.txt"
		self.File.Create(self.hosts_file_header_file)

		self.hour_config_file = self.folders["Apps"]["Module files"][self.module["key"]]["root"] + "Hour config.txt"
		self.File.Create(self.hour_config_file)

		self.log_file = self.folders["Apps"]["Module files"][self.module["key"]]["root"] + "Log.txt"
		self.File.Create(self.log_file)

		# Social Networks Folder and Files
		self.social_networks_text_folder = self.Social_Networks.social_networks_text_folder

		self.social_networks_file = self.Social_Networks.social_networks_file

	def Define_Lists(self):
		self.hosts_file_header = self.File.Contents(self.hosts_file_header_file)["string"]

		self.blocked_by_default = self.File.Contents(self.blocked_by_default_file)["lines"]

		self.additional_maps = self.File.Contents(self.additional_maps_file)["lines"]

		self.websites_to_block = self.File.Contents(self.social_networks_file)["lines"]
		self.websites_to_block.remove("Habitica")

		self.domains = {}

		i = 0
		for website in self.websites_to_block:
			self.domains_file = self.social_networks_text_folder + website + "/Additional Domains.txt"

			self.domains[website] = self.File.Contents(self.domains_file)["lines"]

			i += 1

		self.map_dict = {
			"Blocked by default": self.blocked_by_default,
			"Additional maps": self.additional_maps,
		}

		self.hour_config = self.File.Dictionary(self.hour_config_file, convert = int)