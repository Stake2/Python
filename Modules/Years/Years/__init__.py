# Years.py

class Years(object):
	def __init__(self, select_year = False):
		# Define the module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.Define_Basic_Variables()

		self.Define_Texts()
		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()

		self.select_year = select_year

		if self.select_year == True:
			self.Select_Year()

	def Define_Basic_Variables(self):
		from copy import deepcopy

		# Import the JSON module
		from Utility.JSON import JSON as JSON

		self.JSON = JSON()

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

				# Add the sub-clas to the current module
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
		self.large_bar = "-----"
		self.dash_space = "-"

		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.JSON.Language.Item(self.texts)

		self.language_texts["month_names, type: list"] = self.Date.language_texts["month_names, type: list"]

		self.author = "Izaque Sanvezzo (Stake2, Funkysnipa Cat)"

		self.current_year_number = self.date["Units"]["Year"]

	def Define_Folders_And_Files(self):
		# Year text folders
		self.year_texts_folder = self.folders["notepad"]["effort"]["years"]["root"] + self.texts["texts, title()"]["en"] + "/"
		self.Folder.Create(self.year_texts_folder)

		self.years_file = self.folders["notepad"]["effort"]["years"]["root"] + self.texts["years, title()"]["en"] + ".json"
		self.File.Create(self.years_file)

	def Define_Lists_And_Dictionaries(self):
		# Lists
		december = self.Date.From_String("01/12/{}".format(self.date["Units"]["Year"]))

		month_days = december["Timezone"]["DateTime"]["Units"]["Month days"]
		year = self.date["Units"]["Year"]

		self.summary_date = self.Date.From_String("{}/12/{}".format(month_days, year))

		# Dictionaries
		self.years = {
			"Numbers": {
				"Total": 0
			},
			"List": []
		}

		# Add the Years to the Years list
		starting_year = 2018
		current_year = int(self.date["Units"]["Year"]) + 1

		for year in range(starting_year, current_year):
			self.years["List"].append(str(year))
			self.years["Numbers"]["Total"] += 1

		# Make a local copy of the Years dictionary
		from copy import deepcopy

		local_dictionary = deepcopy(self.years)

		# Fill the dictionaries
		for year in self.years["List"]:
			self.years[year] = {
				"Number": year
			}

			# Define the root folder
			self.years[year]["Folder"] = self.folders["notepad"]["effort"]["years"]["root"] + year + "/"
			self.Folder.Create(self.years[year]["Folder"])

			# Define the image folder
			self.years[year]["Image folder"] = self.folders["mega"]["image"]["years"]["root"] + year + "/"
			self.Folder.Create(self.years[year]["Image folder"])

			# Define the folders
			self.years[year]["Folders"] = self.Folder.Contents(self.years[year]["Folder"])["dictionary"]

			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				if full_language not in self.years[year]["Folders"]:
					self.years[year]["Folders"][full_language] = {
						"root": self.years[year]["Folders"]["root"] + full_language + "/"
					}

				text = self.JSON.Language.texts["firsts_of_the_year"][language]

				if text not in self.years[year]["Folders"][full_language]:
					self.years[year]["Folders"][full_language][text] = {
						"root": self.years[year]["Folders"][full_language]["root"] + text + "/"
					}

		# Current Year dictionary definition
		self.current_year = self.years[str(self.date["Units"]["Year"])]

		# Add the "Years" key to the local Years dictionary
		local_dictionary["Years"] = {}

		# Iterate through the Years list
		for year in self.years["List"]:
			# Add the Year dictionary to the "Years" key
			local_dictionary["Years"][year] = deepcopy(self.years[year])

			# Remove the "Folders" key from each Year dictionary
			local_dictionary["Years"][year].pop("Folders")

		# Define the "Year Texts" folders and its files
		local_dictionary["Year texts"] = self.Folder.Contents(self.year_texts_folder)["dictionary"]

		# Write the local updated Years dictionary to the "Years.json"
		self.JSON.Edit(self.years_file, local_dictionary)

	def Select_Year(self, years = None, select_text = None):
		if years == None:
			years = self.years["List"]

		show_text = self.language_texts["years, title()"]

		if select_text == None:
			select_text = self.language_texts["select_a_year"]

		year = self.years[self.Input.Select(years, show_text = show_text, select_text = select_text)["option"]]

		return year