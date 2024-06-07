# SproutGigs.py

# Import the "importlib" module
import importlib

class SproutGigs():
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.folders = self.Define_Folders(object = self).folders

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Folders, files, lists, and dictionaries methods
		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()

		# Import the usage classes
		self.Import_Usage_Classes()

		# Class methods
		self.Define_Categories()

	def Define_Basic_Variables(self):
		from copy import deepcopy

		# Import the JSON module
		from Utility.JSON import JSON as JSON

		self.JSON = JSON()

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

		# Get the modules list
		self.modules = self.JSON.To_Python(self.folders["Apps"]["Modules"]["Modules"])

		# Create a list of the modules that will not be imported
		remove_list = [
			"Define_Folders",
			"Language",
			"JSON"
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
			self.module_folders[item] = deepcopy(self.folders["Apps"][item][self.module["key"]])

		# Define the local folders dictionary as the Folder folders dictionary
		self.folders = self.Folder.folders

		# Restore the backup of the module folders
		for item in ["modules", "module_files"]:
			self.folders["Apps"][item][self.module["key"]] = self.module_folders[item]

		# Get the switches dictionary from the "Global Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# Get the Languages dictionary
		self.languages = self.Language.languages

		# Get the user language and full user language
		self.user_language = self.Language.user_language
		self.full_user_language = self.Language.full_user_language

		# Get the Sanitize method of the File class
		self.Sanitize = self.File.Sanitize

		# Get the current date from the Date module
		self.date = self.Date.date

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

		# Define the "Separators" dictionary
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

	def Define_Folders_And_Files(self):
		# Folders
		self.categories_folder = self.folders["Apps"]["Module files"][self.module["key"]]["root"] + "Categories/"
		self.Folder.Create(self.categories_folder)

		# Files
		self.website_file = self.folders["Apps"]["Module files"][self.module["key"]]["root"] + "Website.txt"
		self.File.Create(self.website_file)

		self.categories_file = self.categories_folder + "Categories.txt"
		self.File.Create(self.categories_file)

	def Define_Lists_And_Dictionaries(self):
		# Lists
		self.category_list = self.Folder.Contents(self.categories_folder)["folder"]["names"]

		self.File.Edit(self.categories_file, self.Text.From_List(self.category_list, break_line = True), "w")

		self.additional_options = [
			"[" + self.language_texts["change_category"] + "]",
			"[" + self.language_texts["open_category_page"] + "]",
			"[" + self.language_texts["finish_working"] + "]",
		]

		# Dictionaries
		# Website
		self.website = {
			"data": self.File.Dictionary(self.website_file, next_line = True),
		}

		for key in self.website["data"]:
			self.website[key.lower()] = self.website["data"][key]

		self.website["link"] = "https://{}.{}/".format(self.website["name"].lower(), self.website["tld"])
		self.website["job link"] = self.website["link"] + "jobs.php"

		self.website["category_link_template"] = self.website["job link"] + "?category={}&sub_category="

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

	def Define_Categories(self):
		self.categories = {}

		for category in self.category_list:
			self.categories[category] = {}
			self.categories[category]["name"] = category

			category_folder = self.categories_folder + category + "/"
			self.Folder.Create(self.categories_folder)

			# Data file
			data_file = category_folder + "Data.json"
			self.File.Create(data_file)

			# Data Dictionary
			data = self.JSON.To_Python(data_file)

			# Add category data to category dictionary
			self.categories[category]["data"] = {}
			self.categories[category]["info"] = {}

			for key in data:
				value = data[key]

				if key != "number":
					key = self.language_texts[key]

				self.categories[category]["data"][key] = value

			self.categories[category]["info"]["number"] = self.categories[category]["data"]["number"]

			del self.categories[category]["data"]["number"]

	def Select_Category(self):
		show_text = self.language_texts["categories, title()"]
		select_text = self.language_texts["select_a_job_category_to_work"]

		if self.category != None:
			print()
			print("-----")

		self.category_name = self.Input.Select(list(self.categories.keys()), show_text = show_text, select_text = select_text)["option"]

		self.category = self.categories[self.category_name]

		for option in self.additional_options:
			self.category["data"][option] = ""

		self.Open_Category_Tab(self.category)

		if self.category["name"] in self.Social_Networks.social_networks:
			from Block_Websites.Unblock import Unblock as Unblock

			Unblock(websites = self.category["name"])

	def Open_Category_Tab(self, category, open = False):
		text = self.language_texts["opening_{}_on_this_category_to_work"].format(self.website["name"])

		print()
		print("-----")
		print()

		if self.first_time == False and open == False:
			text = self.language_texts["changing_to_this_category"]

		print(text + ":")
		print(category["name"])

		if self.first_time == True:
			print()

		if self.first_time == False and category["name"] not in self.Social_Networks.social_networks and open == False:
			print()

		if open == True:
			print()

		if self.first_time == True or open == True:
			self.category["info"]["link"] = self.website["category_link_template"].format(category["info"]["number"])

			print(self.language_texts["link, title()"] + ":")
			print(self.category["info"]["link"])

			if self.switches["Testing"] == False:
				self.System.Open(self.category["info"]["link"])