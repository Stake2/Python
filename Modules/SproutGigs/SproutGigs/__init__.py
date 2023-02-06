# SproutGigs.py

from Social_Networks.Social_Networks import Social_Networks as Social_Networks
from Block_Websites.Unblock import Unblock as Unblock

class SproutGigs():
	def __init__(self):
		self.Import_Modules()
		self.Define_Module_Folder()
		self.Define_Texts()

		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()
		self.Define_Categories()

		self.Social_Networks = Social_Networks()

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

	def Define_Folders_And_Files(self):
		# Folders
		self.categories_folder = self.folders["apps"]["module_files"][self.module["key"]]["root"] + "Categories/"
		self.Folder.Create(self.categories_folder)

		# Files
		self.website_file = self.folders["apps"]["module_files"][self.module["key"]]["root"] + "Website.txt"
		self.File.Create(self.website_file)

		self.categories_file = self.categories_folder + "Categories.txt"
		self.File.Create(self.categories_file)

	def Define_Lists_And_Dictionaries(self):
		# Lists
		self.category_list = self.Folder.Contents(self.categories_folder)["folder"]["names"]

		self.File.Edit(self.categories_file, self.Text.From_List(self.category_list), "w")

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
			Unblock(self.category["name"])

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

			if self.switches["global"]["testing"] == False:
				self.File.Open(self.category["info"]["link"])