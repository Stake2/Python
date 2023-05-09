# Add_A_New_Data.py

from Database.Database import Database as Database

class Add_A_New_Data(Database):
	def __init__(self):
		super().__init__()

		# Define the dictionary and select the data type
		self.dictionary = {
			"Type": self.Select_Type(),
			"Data": {
				"Title": "",
				"Titles": {}
			}
		}

		self.data = self.dictionary["Data"]

		# Ask for the data information
		self.Type_Data_Information()

		# Create the details dictionary
		self.Create_Details()

		# Select the data to define its variables
		self.Select_Data(self.dictionary)

		# Add the data to the Data Information Database
		self.Add_To_The_Database()

		# Instantiate the root class to update the database files
		super().__init__()

	def Type_Data_Information(self):
		print()
		print(self.large_bar)
		print()
		print(self.language_texts["type_the_data_titles_(press_enter_to_leave_it_empty)"] + ":")

		# Ask for the data titles
		self.data["Title"] = self.Input.Type(self.JSON.Language.language_texts["original_title"], next_line = True, accept_enter = False)
		self.data["Titles"]["Original"] = self.data["Title"]

		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language][self.user_language]

			title = self.Input.Type(self.JSON.Language.language_texts["title_in_{}"].format(translated_language), next_line = True)

			if title != "":
				self.data["Titles"][language] = title

		title = self.Input.Type(self.JSON.Language.language_texts["romanized_title"], next_line = True)

		if title != "":
			self.data["Titles"]["Romanized"] = title

		# Ask for the data year and dates
		text = self.Date.language_texts["year, title()"] + " (" + self.JSON.Language.language_texts["format"] + ": " + str(self.Date.Now()["Units"]["Year"]) + ")"
		self.data["Year"] = self.Input.Type(text, next_line = True, regex = "^[1-9]{1}[0-9]{3}; " + str(self.Date.Now()["Units"]["Year"]), accept_enter = False)

		for date_type in ["start", "end"]:
			text = self.Date.language_texts[date_type + "_date"] + " (" + self.JSON.Language.language_texts["format"] + ": " + self.Date.Now()["Formats"]["DD/MM/YYYY"] + ")"

			accept_enter = False
			regex = None

			if date_type == "end":
				accept_enter = True

			date = self.Input.Type(text, next_line = True, accept_enter = accept_enter, regex = "[0-9]{2}\/[0-9]{2}\/[1-9]{1}[0-9]{3}; " + self.Date.Now()["Formats"]["DD/MM/YYYY"])

			if date != "":
				import re

				if date_type == "end" and re.search("[0-9]{2}\/[0-9]{2}\/[1-9]{1}[0-9]{3}", date) == None:
					date = self.Input.Type(text, next_line = True, accept_enter = False, regex = "[0-9]{2}\/[0-9]{2}\/[1-9]{1}[0-9]{3}; " + self.Date.Now()["Formats"]["DD/MM/YYYY"])

				self.data[date_type.title() + " date"] = date

		# Ask for the original language of the data
		show_text = self.JSON.Language.language_texts["languages, title()"]
		select_text = self.JSON.Language.language_texts["language, title()"]

		languages = list(self.languages["full"].values())
		languages.append("[" + self.JSON.Language.language_texts["empty, title()"] + "]")

		language = self.Input.Select(show_text = show_text, select_text = select_text, options = languages)["option"]

		if language != self.full_user_language:
			self.data["Language"] = language

		# Ask for the data status
		show_text = self.JSON.Language.language_texts["statuses, title()"]
		select_text = self.JSON.Language.language_texts["status, title()"]

		self.data["Status"] = self.Input.Select(show_text = show_text, select_text = select_text, options = self.language_texts["statuses, type: list"])["option"]

		# Ask for the data origin type
		show_text = self.JSON.Language.language_texts["origin_types"]
		select_text = self.JSON.Language.language_texts["origin_type"]

		self.data["Origin type"] = self.Input.Select(show_text = show_text, select_text = select_text, options = self.JSON.Language.language_texts["origin_types, type: list"])["option"]

	def Create_Details(self):
		self.data["Details"] = {
			self.JSON.Language.language_texts["title, title()"]: self.data["Title"]
		}

		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language][self.user_language]

			key = self.JSON.Language.language_texts["title_in_{}"].format(translated_language) 

			if language in self.data["Titles"]:
				self.data["Details"][key] = self.data["Titles"][language]

		if "Romanized" in self.data["Titles"]:
			key = self.JSON.Language.language_texts["romanized_title"]

			self.data["Details"][key] = self.data["Titles"]["Romanized"]

		self.data["Details"][self.Date.language_texts["year, title()"]] = self.data["Year"]

		if "Start date" in self.data:
			self.data["Details"][self.Date.language_texts["start_date"]] = self.data["Start date"]

		if "End date" in self.data:
			self.data["Details"][self.Date.language_texts["end_date"]] = self.data["End date"]

		if "Language" in self.data:
			self.data["Details"][self.JSON.Language.language_texts["original_language"]] = self.data["Language"]

		if self.data["Status"] != self.JSON.Language.language_texts["remote, title()"]:
			self.data["Details"][self.JSON.Language.language_texts["status, title()"]] = self.data["Status"]

		self.data["Details"][self.JSON.Language.language_texts["origin_type"]] = self.data["Origin type"]

		# Create the data folders
		self.data["folders"] = {
			"root": self.dictionary["Type"]["Folders"]["information"]["root"] + self.Sanitize(self.data["Title"], restricted_characters = True) + "/"
		}

		self.Folder.Create(self.data["folders"]["root"])

		# Create the data details file
		self.data["folders"]["details"] = self.data["folders"]["root"] + self.JSON.Language.language_texts["details, title()"] + ".txt"
		self.File.Create(self.data["folders"]["details"])

		# Write into the data details file
		self.File.Edit(self.data["folders"]["details"], self.Text.From_Dictionary(self.data["Details"]), "w")

		# Remove the "folders" dictionary to let "Select_Data" create it
		self.data.pop("folders")

	def Add_To_The_Database(self):
		self.dictionary["Type"]["JSON"] = self.JSON.To_Python(self.dictionary["Type"]["Folders"]["information"]["info"])

		# Add to the titles list
		self.dictionary["Type"]["JSON"]["Titles"].append(self.data["Title"])

		# Add to the status titles list
		english_status = self.Get_Language_Status(self.data["Status"])

		self.dictionary["Type"]["JSON"]["Status"][english_status].append(self.data["Title"])

		# Update the number of data inside the json dictionary
		self.dictionary["Type"]["JSON"]["Number"] = len(self.dictionary["Type"]["JSON"]["Titles"])

		# Edit the "Info.json" file with the new dictionary
		self.JSON.Edit(self.dictionary["Type"]["Folders"]["information"]["info"], self.dictionary["Type"]["JSON"])