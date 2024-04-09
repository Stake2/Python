# Register.py

from Database.Database import Database as Database

class Register(Database):
	def __init__(self, dictionary = {}):
		super().__init__()

		self.dictionary = dictionary

		# Ask for the entry information
		if self.dictionary == {}:
			self.Select_Type()
			self.Type_Entry_Information()

		# Define the data variable to make typing the data dictionary easier
		self.data = self.dictionary["Data"]

		self.dictionary["Entry"].update({
			"Dates": {
				"UTC": self.dictionary["Entry"]["Date"]["UTC"]["DateTime"]["Formats"]["YYYY-MM-DDTHH:MM:SSZ"],
				"Timezone": self.dictionary["Entry"]["Date"]["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"]
			},
			"Diary Slim": {
				"Text": ""
			}
		})

		self.Check_Data_Status()

		if (
			self.data["States"]["Re-experiencing"] == False and
			self.data["States"]["Completed data"] == True
		):
			self.Check_Data_Dates()

		# Database related methods
		self.Register_In_JSON()
		self.Create_Entry_File()
		self.Add_Entry_File_To_Year_Folder()

		self.Write_On_Diary_Slim()

		self.Show_Information(self.dictionary)

	def Select_Type(self):
		options = self.types["Plural"]["en"]
		language_options = self.types["Plural"][self.user_language]

		show_text = self.JSON.Language.language_texts["types, title()"]
		select_text = self.JSON.Language.language_texts["select_a_type"]

		dictionary = self.Input.Select(options, language_options = language_options, show_text = show_text, select_text = select_text)

		self.dictionary["Entry"] = {
			"Type": self.types[dictionary["option"]],
			"Name": {},
			"Titles": {},
			"Date": self.Date.Now()
		}

	def Type_Entry_Information(self):
		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language][self.user_language]

			type_text = self.language_texts["type_the_entry_title_in"] + " " + translated_language

			self.data["Titles"][language] = self.Input.Type(type_text)

	def Register_In_JSON(self):
		self.type = self.dictionary["Type"]["Plural"]["en"]

		dicts = [
			self.dictionaries["Entries"],
			self.dictionaries["Entry type"][self.type],
			self.dictionaries["Registered"]
		]

		# Add one to the entry, type entry, and root type entry numbers
		for dict_ in dicts:
			dict_["Numbers"]["Total"] += 1

			if "Per Type" in dict_["Numbers"]:
				dict_["Numbers"]["Per Type"][self.type] += 1

		# Define sanitized version of entry name for files
		self.dictionary["Entry"]["Name"] = {
			"Normal": str(self.dictionaries["Entries"]["Numbers"]["Total"]) + ". " + self.type + " (" + self.dictionary["Entry"]["Dates"]["Timezone"] + ")",
			"Sanitized": ""
		}

		self.dictionary["Entry"]["Name"]["Sanitized"] = self.dictionary["Entry"]["Name"]["Normal"].replace(":", ";").replace("/", "-")

		# Add to the "Entries" lists
		for dict_ in dicts:
			if self.dictionary["Entry"]["Name"]["Normal"] not in dict_["Entries"]:
				dict_["Entries"].append(self.dictionary["Entry"]["Name"]["Normal"])

		# Define local data titles to remove some keys from them
		data_titles = self.data["Titles"].copy()
		data_titles.pop("Language")

		for key in ["ja", "Sanitized"]:
			if key in data_titles:
				data_titles.pop(key)

		for language in self.languages["small"]:
			if language in data_titles and data_titles["Original"] == data_titles[language]:
				data_titles.pop(language)

		self.key = self.dictionary["Entry"]["Name"]["Normal"]

		self.dictionaries["Entries"]["Dictionary"][self.key] = {
			"Number": self.dictionaries["Entries"]["Numbers"]["Total"],
			"Type number": self.dictionaries["Entry type"][self.type]["Numbers"]["Total"],
			"Entry": self.dictionary["Entry"]["Name"]["Normal"],
			"Titles": data_titles,
			"Type": self.type,
			"Date": self.dictionary["Entry"]["Dates"]["UTC"]
		}

		# Get the States dictionary
		self.dictionary["States"] = self.Define_States_Dictionary(self.dictionary)

		if self.dictionary["States"]["States"] != {}:
			self.dictionaries["Entries"]["Dictionary"][self.key]["States"] = self.dictionary["States"]["States"]

		# Add entry dictionary to type and Registered entry dictionaries
		for dict_ in dicts:
			if dict_ != self.dictionaries["Entries"]:
				dict_["Dictionary"][self.key] = self.dictionaries["Entries"]["Dictionary"][self.key].copy()

		# Update the "Entries.json" file
		self.JSON.Edit(self.folders["history"]["current_year"]["entries"], self.dictionaries["Entries"])

		# Update the type "Entries.json" file
		self.JSON.Edit(self.dictionary["Type"]["Folders"]["per_type"]["entries"], self.dictionaries["Entry type"][self.type])

		# Update the data "Registered.json" file
		self.JSON.Edit(self.data["Folders"]["Registered"]["entries"], self.dictionaries["Registered"])

		# Add to the root, type, and data "Entry list.txt" files
		self.File.Edit(self.folders["history"]["current_year"]["entry_list"], self.dictionary["Entry"]["Name"]["Normal"], "a")
		self.File.Edit(self.dictionary["Type"]["Folders"]["per_type"]["entry_list"], self.dictionary["Entry"]["Name"]["Normal"], "a")
		self.File.Edit(self.data["Folders"]["Registered"]["entry_list"], self.dictionary["Entry"]["Name"]["Normal"], "a")

	def Create_Entry_File(self):
		# Number: [entry number]
		# Type number: [Type number]
		# 
		# Title:
		# [Title]
		# 
		# Type:
		# [Type]
		#
		# Dates:
		# [Entry dates]
		# 
		# File name:
		# [Number. Type (Time)]

		# Define the entry file
		folder = self.dictionary["Type"]["Folders"]["per_type"]["files"]["root"]
		file = folder + self.dictionary["Entry"]["Name"]["Sanitized"] + ".txt"
		self.File.Create(file)

		self.dictionary["Entry"]["Text"] = {
			"General": self.Define_File_Text("General")
		}

		for language in self.languages["small"]:
			self.dictionary["Entry"]["Text"][language] = self.Define_File_Text(language)

		# Write the entry text into the entry file
		self.File.Edit(file, self.dictionary["Entry"]["Text"]["General"], "w")

		# Write the entry text into the "Registered" entry file
		file = self.data["Folders"]["Registered"]["files"]["root"] + self.dictionary["Entry"]["Name"]["Sanitized"] + ".txt"

		self.File.Create(file)
		self.File.Edit(file, self.dictionary["Entry"]["Text"][self.user_language], "w")

	def Define_File_Text(self, language_parameter = None):
		if language_parameter != "General":
			language = language_parameter

		if language_parameter == "General":
			language = self.user_language

		full_language = self.languages["full"][language]

		# Define entry text lines
		lines = [
			self.JSON.Language.texts["number, title()"][language] + ": " + str(self.dictionaries["Entries"]["Numbers"]["Total"]),
			self.JSON.Language.texts["type_number"][language] + ": " + str(self.dictionaries["Entry type"][self.type]["Numbers"]["Total"])
		]

		# Add entry title lines
		if language_parameter != "General":
			text = self.JSON.Language.texts["title, title()"][language]

		if language_parameter == "General":
			text = self.JSON.Language.texts["titles, title()"][language]

		lines.append("\n" + text + ":" + "\n" + "{}")

		lines.extend([
			self.JSON.Language.texts["type, title()"][language] + ":" + "\n" + self.dictionary["Type"]["Plural"][language] + "\n",
			self.Date.texts["times, title()"][language] + ":" + "\n" + "{}",
			self.JSON.Language.texts["entry, title()"][language] + ":" + "\n" + self.dictionary["Entry"]["Name"]["Normal"]
		])

		# Add states texts lines
		if self.dictionary["States"]["Texts"] != {}:
			text = "\n" + self.JSON.Language.texts["states, title()"][language] + ":" + "\n"

			for key in self.dictionary["States"]["Texts"]:
				language_text = self.dictionary["States"]["Texts"][key][language]

				text += language_text

				if key != list(self.dictionary["States"]["Texts"].keys())[-1]:
					text += "\n"

			lines.append(text)

		# Define items to be added to file text format
		items = []

		# Add entry titles to items list
		titles = []

		key = "Original"

		if "Romanized" in self.data["Titles"]:
			key = "Romanized"

		titles.append(self.data["Titles"][key])

		if self.data["Titles"]["Language"] != self.data["Titles"][key]:
			titles.append("\n" + self.data["Titles"]["Language"])

		i = 0
		for line in lines:
			if self.JSON.Language.texts["titles, title()"][language] in line:
				line = line.replace(self.JSON.Language.texts["titles, title()"][language], self.JSON.Language.texts["title, title()"][language])

				lines[i] = line

			i += 1

		items.append(self.Text.From_List(titles) + "\n")

		# Add times to items list
		times = ""

		for key in ["UTC", "Timezone"]:
			time = self.dictionary["Entry"]["Dates"][key]

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
			type_folder = self.dictionary["Type"]["Plural"][language]

			# Entries folder
			folder = self.current_year["Folders"][language]["root"]

			self.current_year["Folders"][language]["Added entries"] = {
				"root": folder + root_folder + "/"
			}

			self.Folder.Create(self.current_year["Folders"][language]["Added entries"]["root"])

			# Type folder
			folder = self.current_year["Folders"][language]["Added entries"]["root"]

			self.current_year["Folders"][language]["Added entries"][type_folder] = {
				"root": folder + type_folder + "/"
			}

			self.Folder.Create(self.current_year["Folders"][language]["Added entries"][type_folder]["root"])

			# Entry file
			folder = self.current_year["Folders"][language]["Added entries"][type_folder]["root"]
			file_name = self.dictionary["Entry"]["Name"]["Sanitized"]
			self.current_year["Folders"][language]["Added entries"][type_folder][file_name] = folder + file_name + ".txt"

			self.File.Create(self.current_year["Folders"][language]["Added entries"][type_folder][file_name])

			self.File.Edit(self.current_year["Folders"][language]["Added entries"][type_folder][file_name], self.dictionary["Entry"]["Text"][language], "w")

			# Firsts Of The Year subfolder folder
			subfolder_name = self.JSON.Language.texts["entries, title()"][language]

			folder = self.current_year["Folders"][language]["Firsts of the Year"]["root"]

			self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name] = {
				"root": folder + subfolder_name + "/"
			}

			self.Folder.Create(self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name]["root"])

			# Firsts Of The Year type folder
			folder = self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name]["root"]
			type_folder = self.dictionary["Type"]["Singular"][language]

			self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name][type_folder] = {
				"root": folder + type_folder + "/"
			}

			self.Folder.Create(self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name][type_folder]["root"])

			# First type entry in year file
			if self.data["States"]["First type entry in year"] == True:
				folder = self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name][type_folder]["root"]

				self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name][type_folder][file_name] = folder + file_name + ".txt"
				self.File.Create(self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name][type_folder][file_name])

				self.File.Edit(self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name][type_folder][file_name], self.dictionary["Entry"]["Text"][language], "w")

	def Check_Data_Status(self):
		self.data["States"]["Completed data"] = self.Input.Yes_Or_No(self.language_texts["did_you_finished_the_whole_data"])

		if self.data["States"]["Completed data"] == True:
			# Update the status key in the data details
			self.Change_Status(self.dictionary)

	def Check_Data_Dates(self):
		# Completed data time and date template
		template = self.language_texts["when_i_finished_experiencing"] + ":" + "\n" + \
		self.dictionary["Entry"]["Dates"]["Timezone"] + "\n" + \
		"\n" + \
		self.Date.language_texts["duration, title()"] + ":" + "\n" + \
		"{}"

		# Gets the date that the user started and finished experiencing the data and writes it to the data dates text file
		if self.data["States"]["Completed data"] == True:
			# Gets the data dates from the data dates file
			self.data["dates"] = self.File.Dictionary(self.data["Folders"]["dates"], next_line = True)

			key = self.language_texts["when_i_started_to_experience"]

			# Get the started experiencing time
			self.data["Started experiencing"] = self.Date.To_UTC(self.Date.From_String(self.data["dates"][key]))

			# Define time spent experiencing using started experiencing time and finished experiencing time
			self.data["Time spent experiencing"] = self.Date.Difference(self.data["Started experiencing"], self.dictionary["Entry"]["Date"]["UTC"]["Object"])["Texts"][self.user_language]

			if self.data["Time spent experiencing"][0] + self.data["Time spent experiencing"][1] == ", ":
				self.data["Time spent experiencing"] = self.data["Time spent experiencing"][2:]

			# Format the time template
			self.data["Formatted datetime template"] = "\n\n" + template.format(self.data["Time spent experiencing"])

			# Read the data dates file
			self.data["Finished experiencing text"] = self.File.Contents(self.data["Folders"]["dates"])["string"]

			# Add the time template to the data dates text
			self.data["Finished experiencing text"] += self.data["Formatted datetime template"]

			# Update the data dates text file
			self.File.Edit(self.data["Folders"]["dates"], self.data["Finished experiencing text"], "w")

			text = self.types["Genders"][self.user_language]["masculine"]["the"] + " " + self.language_texts["data, title()"].lower()

			# Add the time template to the Diary Slim text
			self.data["Finished experiencing text"] = self.data["Finished experiencing text"].replace(self.language_texts["when_i_started_to_experience"], self.language_texts["when_i_started_to_experience"] + " " + text)

			self.dictionary["Entry"]["Diary Slim"]["Dates"] = "\n\n" + self.data["Finished experiencing text"]

	def Write_On_Diary_Slim(self):
		self.dictionary["Entry"]["Diary Slim"]["Text"] = self.data["Titles"]["Language"]

		# If there are states, add the texts to the Diary Slim text
		if self.dictionary["States"]["States"] != {}:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.JSON.Language.language_texts["states, title()"] + ":" + "\n"

			for key in self.dictionary["States"]["Texts"]:
				self.dictionary["Entry"]["Diary Slim"]["Text"] += self.dictionary["States"]["Texts"][key][self.user_language]

				if key != list(self.dictionary["States"]["Texts"].keys())[-1]:
					self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n"

		# If there are dates, add them to the Diary Slim text
		if "Dates" in self.dictionary["Entry"]["Diary Slim"]:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += self.dictionary["Entry"]["Diary Slim"]["Dates"]

		from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

		# Define the "Write on Diary Slim" dictionary
		dictionary = {
			"Text": self.dictionary["Entry"]["Diary Slim"]["Text"],
			"Time": self.dictionary["Entry"]["Dates"]["Timezone"],
			"Add": {
				"Dot": False
			}
		}

		# Write the entry text on Diary Slim
		Write_On_Diary_Slim_Module(dictionary)