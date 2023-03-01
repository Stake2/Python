# Register.py

from Database.Database import Database as Database

class Register(Database):
	def __init__(self, entry = {}):
		super().__init__()

		self.dictionaries["Entry"] = entry

		if self.dictionaries["Entry"] == {}:
			self.Select_Type()
			self.Type_Entry_Information()

		self.dictionaries["Entry"].update({
			"Times": {
				"UTC": self.Date.To_String(self.dictionaries["Entry"]["Time"]["utc"]),
				"Timezone": self.dictionaries["Entry"]["Time"]["hh:mm DD/MM/YYYY"]
			},
			"States": {
				"First entry in year": False,
				"First type entry in year": False
			}
		})

		# Database related methods
		self.Register_In_JSON()
		self.Create_Entry_File()
		self.Add_Entry_File_To_Year_Folder()

		from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

		# Write on Diary Slim
		Write_On_Diary_Slim_Module(self.dictionaries["Entry"]["Titles"][self.user_language], self.dictionaries["Entry"]["Times"]["Timezone"], show_text = False)

		self.Show_Information()

	def Select_Type(self):
		options = self.types["plural"]["en"]
		language_options = self.types["plural"][self.user_language]

		show_text = self.JSON.Language.language_texts["types, title()"]
		select_text = self.JSON.Language.language_texts["select_a_type"]

		dictionary = self.Input.Select(options, language_options = language_options, show_text = show_text, select_text = select_text)

		self.dictionaries["Entry"] = {
			"Name": {},
			"Titles": {},
			"Type": self.types[dictionary["option"]],
			"Time": self.Date.Now()
		}

	def Type_Entry_Information(self):
		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language][self.user_language]

			type_text = self.language_texts["type_the_entry_title_in"] + " " + translated_language

			self.dictionaries["Entry"]["Titles"][language] = self.Input.Type(type_text)

	def Register_In_JSON(self):
		self.type = self.dictionaries["Entry"]["Type"]["plural"]["en"]

		# Add to entry number
		self.dictionaries["Entries"]["Numbers"]["Total"] += 1
		self.dictionaries["Entry Type"][self.type]["Numbers"]["Total"] += 1

		if self.dictionaries["Entries"]["Numbers"]["Total"] == 1:
			self.dictionaries["Entry"]["States"]["First entry in year"] = True

		if self.dictionaries["Entry Type"][self.type]["Numbers"]["Total"] == 1:
			self.dictionaries["Entry"]["States"]["First type entry in year"] = True

		# Define sanitized version of entry name for files
		self.dictionaries["Entry"]["Name"] = {
			"Normal": str(self.dictionaries["Entries"]["Numbers"]["Total"]) + ". " + self.type + " (" + self.dictionaries["Entry"]["Times"]["Timezone"] + ")",
			"Sanitized": ""
		}

		self.dictionaries["Entry"]["Name"]["Sanitized"] = self.dictionaries["Entry"]["Name"]["Normal"].replace(":", ";").replace("/", "-")

		# Add to "Entries" list
		self.dictionaries["Entries"]["Entries"].append(self.dictionaries["Entry"]["Name"]["Normal"])
		self.dictionaries["Entry Type"][self.type]["Entries"].append(self.dictionaries["Entry"]["Name"]["Normal"])

		self.key = self.dictionaries["Entry"]["Name"]["Normal"]

		self.dictionaries["Entries"]["Dictionary"][self.key] = {
			"Number": self.dictionaries["Entries"]["Numbers"]["Total"],
			"Type number": self.dictionaries["Entry Type"][self.type]["Numbers"]["Total"],
			"Entry": self.dictionaries["Entry"]["Name"]["Normal"],
			"Titles": self.dictionaries["Entry"]["Titles"],
			"Type": self.type,
			"Time": self.dictionaries["Entry"]["Times"]["UTC"]
		}

		# Get States dictionary
		self.states_dictionary = self.Define_States_Dictionary(self.dictionaries["Entry"])

		if self.states_dictionary != {}:
			self.dictionaries["Entries"]["Dictionary"][self.key]["States"] = self.states_dictionary["States"]

		# Add entry dictionary to type entries dictionary
		self.dictionaries["Entry Type"][self.type]["Dictionary"][self.key] = self.dictionaries["Entries"]["Dictionary"][self.key].copy()

		# Update "Entries.json" file
		self.JSON.Edit(self.folders["history"]["current_year"]["entries"], self.dictionaries["Entries"])

		# Update type "Entries.json" file
		self.JSON.Edit(self.dictionaries["Entry"]["Type"]["folders"]["per_type"]["entries"], self.dictionaries["Entry Type"][self.type])

		# Add to root and type "Entry list.txt" file
		self.File.Edit(self.folders["history"]["current_year"]["entry_list"], self.dictionaries["Entry"]["Name"]["Normal"], "a")
		self.File.Edit(self.dictionaries["Entry"]["Type"]["folders"]["per_type"]["entry_list"], self.dictionaries["Entry"]["Name"]["Normal"], "a")

	def Create_Entry_File(self):
		# Number: [entry number]
		# Type number: [Type number]
		# 
		# Title:
		# [Title]
		# 
		# Type: [Type]
		#
		# Times:
		# [Entry times]
		# 
		# File name: [Number. Type (Time)]

		# Define entry file
		folder = self.dictionaries["Entry"]["Type"]["folders"]["per_type"]["files"]["root"]
		file = folder + self.dictionaries["Entry"]["Name"]["Sanitized"] + ".txt"
		self.File.Create(file)

		self.dictionaries["Entry"]["Text"] = {
			"General": self.Define_File_Text("General")
		}

		for language in self.languages["small"]:
			self.dictionaries["Entry"]["Text"][language] = self.Define_File_Text(language)

		# Write entry text into entry file
		self.File.Edit(file, self.dictionaries["Entry"]["Text"]["General"], "w")

	def Define_File_Text(self, language_parameter = None):
		if language_parameter != "General":
			language = language_parameter

		if language_parameter == "General":
			language = "en"

		full_language = self.languages["full"][language]

		# Define entry text lines
		lines = [
			self.JSON.Language.texts["number, title()"][language] + ": " + str(self.dictionaries["Entries"]["Numbers"]["Total"]),
			self.JSON.Language.texts["type_number"][language] + ": " + str(self.dictionaries["Entry Type"][self.type]["Numbers"]["Total"])
		]

		# Add entry title lines
		if language_parameter != "General":
			text = self.JSON.Language.texts["title, title()"][language]

		if language_parameter == "General":
			text = self.JSON.Language.texts["titles, title()"][language]

		lines.append("\n" + text + ":" + "\n" + "{}")

		lines.extend([
			self.JSON.Language.texts["type, title()"][language] + ": " + self.dictionaries["Entry"]["Type"]["plural"]["en"] + "\n",
			self.Date.texts["times, title()"][language] + ":" + "\n" + "{}",
			self.JSON.Language.texts["entry, title()"][language] + ": " + self.dictionaries["Entry"]["Name"]["Normal"]
		])

		# Add states texts lines
		if self.states_dictionary != {}:
			text = "\n" + self.JSON.Language.texts["states, title()"][language] + ":" + "\n"

			for key in self.states_dictionary["Texts"]:
				language_text = self.states_dictionary["Texts"][key][language]

				text += language_text

				if key != list(self.states_dictionary["Texts"].keys())[-1]:
					text += "\n"

			lines.append(text)

		# Define items to be added to file text format
		items = []

		# Add entry titles to items list
		titles = ""

		if language_parameter != "General":
			titles = self.dictionaries["Entry"]["Titles"][language] + "\n"

		if language_parameter == "General":
			for language in self.languages["small"]:
				titles += self.dictionaries["Entry"]["Titles"][language] + "\n"

		items.append(titles)

		# Add times to items list
		times = ""

		for key in ["UTC", "Timezone"]:
			time = self.dictionaries["Entry"]["Times"][key]

			times += time + "\n"

		items.append(times)

		# Define language entry text
		file_text = self.Text.From_List(lines)

		return file_text.format(*items)

	def Add_Entry_File_To_Year_Folder(self):
		# Create folders
		for language in self.languages["small"]:
			full_language = self.languages["full"][language]

			# Folder names
			root_folder = self.texts["added_entries"][language]
			type_folder = self.dictionaries["Entry"]["Type"]["plural"][language]

			# Entries folder
			folder = self.current_year["folders"][full_language]["root"]

			self.current_year["folders"][full_language][root_folder] = {
				"root": folder + root_folder + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][root_folder]["root"])

			# Type folder
			folder = self.current_year["folders"][full_language][root_folder]["root"]

			self.current_year["folders"][full_language][root_folder][type_folder] = {
				"root": folder + type_folder + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][root_folder][type_folder]["root"])

			# Entry file
			folder = self.current_year["folders"][full_language][root_folder][type_folder]["root"]
			file_name = self.dictionaries["Entry"]["Name"]["Sanitized"]
			self.current_year["folders"][full_language][root_folder][type_folder][file_name] = folder + file_name + ".txt"

			self.File.Create(self.current_year["folders"][full_language][root_folder][type_folder][file_name])

			self.File.Edit(self.current_year["folders"][full_language][root_folder][type_folder][file_name], self.dictionaries["Entry"]["Text"][language], "w")

			# Firsts Of The Year subfolder folder
			firsts_of_the_year_text = self.JSON.Language.texts["firsts_of_the_year"][language]
			subfolder_name = self.JSON.Language.texts["entries, title()"][language]

			folder = self.current_year["folders"][full_language][firsts_of_the_year_text]["root"]

			self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name] = {
				"root": folder + subfolder_name + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name]["root"])

			# Firsts Of The Year type folder
			folder = self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name]["root"]
			type_folder = self.dictionaries["Entry"]["Type"]["singular"][language]

			self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder] = {
				"root": folder + type_folder + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder]["root"])

			# First type entry in year file
			if self.dictionaries["Entry"]["States"]["First type entry in year"] == True:
				folder = self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder]["root"]

				self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name] = folder + file_name + ".txt"
				self.File.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name])

				self.File.Edit(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name], self.dictionaries["Entry"]["Text"][language], "w")

	def Show_Information(self):
		print()
		print(self.large_bar)
		print()

		print(self.JSON.Language.language_texts["entry, title()"] + ":")

		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language][self.user_language]

			print("\t" + translated_language + ":")
			print("\t" + self.dictionaries["Entry"]["Titles"][language])
			print()

		print(self.JSON.Language.language_texts["type, title()"] + ":")

		text = self.dictionaries["Entry"]["Type"]["plural"]["en"]

		if self.dictionaries["Entry"]["Type"]["plural"][self.user_language] != self.dictionaries["Entry"]["Type"]["plural"]["en"]:
			text = "\t" + text + "\n"
			text += "\t" + self.dictionaries["Entry"]["Type"]["plural"][self.user_language]

		print(text)
		print()

		print(self.JSON.Language.language_texts["when, title()"] + ":")
		print(self.dictionaries["Entry"]["Times"]["Timezone"])