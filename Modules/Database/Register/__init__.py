# Register.py

from Database.Database import Database as Database

class Register(Database):
	def __init__(self):
		super().__init__()

		self.Ask_For_Entry_Info()

		self.entry = {
			"Title": "Entry One",
			"Times": {
				"UTC": "2023-02-09T06:54:00Z",
				"date_time_format": "03:54 09/02/2023",
			},
			"Type": self.types["Type One"],
			"States": {}
		}

		self.Register_In_JSON()
		self.Create_File()

		self.Add_File_To_Year_Folder()

		self.Show_Information()

	def Ask_For_Media_Info(self):
		# To-Do: Make this method
		pass

	def Register_In_JSON(self):
		self.type = self.entry["Type"]["plural"]["en"]

		# Add to entry number
		self.entries["Number"] += 1
		self.type_entries[self.type]["Number"] += 1

		if self.entries["Number"] == 0:
			self.entry["States"]["first_entry_in_year"] = True

		# Define sanitized version of entry name for files
		self.entry["Register"]["Entries"] = {
			"normal": str(self.entries["Number"]) + ". " + self.type + " (" + self.entry["Times"]["date_time_format"][self.user_language] + ")",
			"sanitized": {}
		}

		# Define sanitized version of entry name for files (per language)
		for language in self.languages["small"]:
			self.entry["Register"]["Entries"]["sanitized"][language] = str(self.entries["Number"]) + ". " + self.type + " (" + self.entry["Times"]["date_time_format"][language].replace(":", ";").replace("/", "-") + ")"

		# Add to "Entries" list
		self.entries["Entries"].append(self.entry["Register"]["Entries"]["normal"])
		self.type_entries["Entries"].append(self.entry["Register"]["Entries"]["normal"])

		key = self.entry["Register"]["Entries"]["normal"]

		self.entries["Dictionary"][key] = {
			"Number": self.entries["Number"],
			"Type number": self.type_entries[self.type]["Number"],
			"Entry": self.entry["Register"]["Entries"]["normal"],
			"Title": self.entry["Title"],
			"Type": self.type,
			"Time": self.entry["Times"]["UTC"]
		}

		# Add entry dictionary to type entries dictionary
		self.type_entries[self.type]["Dictionary"][key] = self.entries["Dictionary"][key].copy()

		# Update "Entries.json" file
		self.JSON.Edit(self.folders["history"]["current_year"]["entries"], self.entries)

		# Update type "Entries.json" file
		self.JSON.Edit(self.entry["type"]["folders"]["per_media_type"]["entries"], self.type_entries[self.type])

		# Add to root and type "Entry list.txt" file
		self.File.Edit(self.folders["history"]["current_year"]["entry_list"], self.entry["Register"]["Entries"]["normal"], "a")
		self.File.Edit(self.entry["Type"]["folders"]["per_media_type"]["entry_list"], self.entry["Register"]["Entries"]["normal"], "a")

	def Create_File(self):
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
		folder = self.entry["Type"]["folders"]["per_media_type"]["files"]["root"]
		file = folder + self.entry["Register"]["Entries"]["sanitized"][self.user_language] + ".txt"
		self.File.Create(file)

		self.entry["Register"]["file_text"] = {}

		self.entry["Register"]["file_text"]["general"] = self.Define_File_Text("general")

		for language in self.languages["small"]:
			self.entry["Register"]["file_text"][language] = self.Define_File_Text(language)

		# Write entry text into entry file
		self.File.Edit(file, self.entry["Register"]["file_text"]["general"], "w")

	def Define_File_Text(self, language_parameter = None):
		if language_parameter != "general":
			language = language_parameter

		if language_parameter == "general":
			language = "en"

		full_language = self.languages["full"][language]

		# Define entry text lines
		lines = [
			self.Language.texts["number, title()"][language] + ": " + str(self.entries["Number"]),
			self.texts["type_number"][language] + ": " + str(self.type_entries[self.type]["Number"]),
			"\n" + self.Language.texts["title, title()"][language] + ":" + "\n" + "{}",
			self.Language.texts["type, title()"][language] + ": " + self.entry["Type"]["plural"]["en"] + "\n",
			self.Date.texts["times, title()"][language] + ":" + "\n" + "{}",
			self.texts["entry, title()"][language] + ": " + self.entry["Register"]["Entries"]["normal"]
		])

		# Define language entry text
		file_text = self.Text.From_List(lines)

		# Define items to be added to entry text
		items = [
			self.entry["Title"]
		]

		# Add times to items list
		times = ""

		for key in ["UTC", "date_time_format"]:
			time = self.entry["Times"][key]

			if key == "UTC":
				times += time + "\n"

			if key == "date_time_format":
				if language_parameter != "general":
					times += time[language] + "\n"

				if language_parameter == "general":
					for language in self.languages["small"]:
						times += time[language] + "\n"

		items.append(times)

		return file_text.format(*items)

	def Add_File_To_Year_Folder(self):
		# Create folders
		for language in self.languages["small"]:
			full_language = self.languages["full"][language]

			# Folder names
			root_folder = self.texts["added_entries"][language]
			type_folder = self.entry["Type"]["singular"][language]

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

			# Firsts Of The Year subfolder folder
			firsts_of_the_year_text = self.Language.texts["firsts_of_the_year"][language]
			subfolder_name = self.texts["entry, title()"][language]

			folder = self.current_year["folders"][full_language][firsts_of_the_year_text]["root"]

			self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name] = {
				"root": folder + subfolder_name + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name]["root"])

			# Firsts Of The Year type folder
			folder = self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name]["root"]
			
			self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder] = {
				"root": folder + type_folder + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder]["root"])

			# Entry file
			folder = self.current_year["folders"][full_language][root_folder][type_folder]["root"]
			file_name = self.entry["Register"]["Entries"]["sanitized"][language]
			self.current_year["folders"][full_language][root_folder][type_folder][file_name] = folder + file_name + ".txt"

			self.File.Create(self.current_year["folders"][full_language][root_folder][type_folder][file_name])

			self.File.Edit(self.current_year["folders"][full_language][root_folder][type_folder][file_name], self.entry["Register"]["file_text"][language], "w")

			# First type entry in year file
			if self.entry["states"]["first_entry_in_year"] == True:
				folder = self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder]["root"]

				self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name] = folder + file_name + ".txt"
				self.File.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name])

				self.File.Edit(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name], self.entry["Register"]["file_text"][language], "w")

	def Show_Information(self):
		self.JSON.Show(self.entry)