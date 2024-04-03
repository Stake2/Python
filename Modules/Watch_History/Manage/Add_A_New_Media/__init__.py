# Add_A_New_Media.py

from Watch_History.Watch_History import Watch_History as Watch_History

class Add_A_New_Media(Watch_History):
	def __init__(self):
		super().__init__()

		# Define the dictionary and select the media type
		self.dictionary = {
			"Media type": self.Select_Media_Type(),
			"Media": {
				"Title": "",
				"Titles": {}
			}
		}

		self.media = self.dictionary["Media"]

		# Ask for the media information
		self.media = self.Type_Media_Information()

		self.dictionary["Media"] = self.media

		# Select the media to define its variables
		self.Select_Media(self.dictionary)

		self.media["States"]["Has media item list"] = True

		# Add the media to the Media Information Database
		self.Add_To_The_Database()

		if self.media["States"]["Series media"] == True:
			self.Add_Media_Items()

		if self.media["States"]["Media item list"] == True:
			# Remove "folders" key from the Media dictionary
			if "Folders" in self.dictionary["Media"]:
				self.dictionary["Media"].pop("Folders")

			self.media = self.dictionary["Media"]

			# Re-select the media to recreate the "folders" key
			self.dictionary = self.Select_Media(self.dictionary)

		self.dictionary["Added media"] = True

		if self.dictionary["Media type"]["Plural"]["en"] != self.texts["movies, title()"]["en"]:
			# Ask user to fill the media files
			from Watch_History.Manage.Fill_Media_Files import Fill_Media_Files as Fill_Media_Files

			Fill_Media_Files(self.dictionary)

		# Run the root class to update the media and database files
		super().__init__()

	def Type_Media_Information(self, item = False):
		self.item = item

		media = self.media

		if self.item == True:
			media = self.media["Item"]

		# Create the "Staff keys" list for the anime media type
		if self.dictionary["Media type"]["Plural"]["en"] == self.texts["animes, title()"]["en"]:
			media["Staff keys"] = [
				"studios"
			]

		multiple_staff_media_types = [
			self.texts["cartoons, title()"]["en"],
			self.texts["series, title()"]["en"],
			self.texts["movies, title()"]["en"]
		]

		# Create the "Staff keys" list for media types that has directors, producers, and distributors
		if self.dictionary["Media type"]["Plural"]["en"] in multiple_staff_media_types:
			media["Staff keys"] = [
				"directors",
				"producers",
				"distributors"
			]

		print()
		print(self.separators["5"])
		print()

		text = self.language_texts["type_the_media_information_(some_items_can_be_left_empty_by_pressing_enter)"]

		if self.item == True:
			text = self.language_texts["type_the_media_item_information_(some_items_can_be_left_empty_by_pressing_enter)"]

		print(text + ":")

		# Ask for the media (item) titles
		if self.switches["testing"] == False:
			title = self.Input.Type(self.JSON.Language.language_texts["original_title"], next_line = True, accept_enter = False)

		if self.switches["testing"] == True:
			title = self.JSON.Language.language_texts["title, title()"] + " (" + self.dictionary["Media type"]["Singular"][self.user_language] + ")"

			if self.item == True:
				title = self.dictionary["Media type"]["Subfolders"]["Singular"] + " " + str(self.media["Items"]["Number"] + 1)

		media["Title"] = title
		media["Titles"]["Original"] = media["Title"]
		media["Titles"]["Sanitized"] = self.Sanitize_Title(media["Title"])

		# Ask for the media (item) titles per langauge
		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language][self.user_language]

			title = ""

			if self.switches["testing"] == False:
				title = self.Input.Type(self.JSON.Language.language_texts["title_in_{}"].format(translated_language), next_line = True)

			if title != "":
				media["Titles"][language] = title

		# If the media type is not "Videos"
		if self.dictionary["Media type"]["Plural"]["en"] != self.texts["videos, title()"]["en"]:
			# Ask for the romanized title
			accept_enter = True

			if self.item == False and self.dictionary["Media type"]["Plural"]["en"] == self.texts["animes, title()"]["en"]:
				accept_enter = False

			if self.switches["testing"] == False:
				title = self.Input.Type(self.JSON.Language.language_texts["romanized_title"], next_line = True, accept_enter = accept_enter)

			if self.switches["testing"] == True:
				title = "Título romanizado"

			if title != "":
				media["Titles"]["Romanized"] = title

			# Ask for the media year and dates
			text = self.Date.language_texts["year, title()"] + " (" + self.JSON.Language.language_texts["format"] + ": " + str(self.Date.Now()["Units"]["Year"]) + ")"

			accept_enter = False

			if (
				self.item == True and
				self.media["States"]["First media item"] == True
			):
				accept_enter = True

			if self.switches["testing"] == False:
				date = self.Input.Type(text, next_line = True, regex = "^[1-9]{1}[0-9]{3}; " + str(self.Date.Now()["Units"]["Year"]), accept_enter = accept_enter)

			if self.switches["testing"] == True:
				date = str(self.Date.Now()["Units"]["Year"])

			if date != "":
				media["Year"] = date

			if date == "":
				media["Year"] = self.media["Year"]

			for date_type in ["start", "end"]:
				text = self.Date.language_texts[date_type + "_date"] + " (" + self.JSON.Language.language_texts["format"] + ": " + self.Date.Now()["Formats"]["DD/MM/YYYY"] + ")"

				accept_enter = False
				regex = None

				if (
					date_type == "end" or
					self.item == True and self.media["States"]["First media item"] == True and date_type.title() + " date" in self.media
				):
					accept_enter = True

				if self.switches["testing"] == False:
					date = self.Input.Type(text, next_line = True, accept_enter = accept_enter, regex = "[0-9]{2}\/[0-9]{2}\/[1-9]{1}[0-9]{3}; " + self.Date.Now()["Formats"]["DD/MM/YYYY"])

				if self.switches["testing"] == True:
					date = self.Date.Now()["Formats"]["DD/MM/YYYY"]

				if date != "":
					import re

					if date_type == "end" and re.search("[0-9]{2}\/[0-9]{2}\/[1-9]{1}[0-9]{3}", date) == None:
						date = self.Input.Type(text, next_line = True, accept_enter = False, regex = "[0-9]{2}\/[0-9]{2}\/[1-9]{1}[0-9]{3}; " + self.Date.Now()["Formats"]["DD/MM/YYYY"])

					media[date_type.title() + " date"] = date

				if (
					date == "" and
					self.item == True and
					self.media["States"]["First media item"] == True and
					date_type.title() + " date" in self.media
				):
					media[date_type.title() + " date"] = self.media[date_type.title() + " date"]

		if self.item == False:
			# Ask for the user information if the media type is "Videos"
			if self.dictionary["Media type"]["Plural"]["en"] == self.texts["videos, title()"]["en"]:
				if self.switches["testing"] == False:
					handle = self.Input.Type(self.JSON.Language.language_texts["handle, title()"], next_line = True)
					id = self.Input.Type(self.JSON.Language.language_texts["id, upper()"], next_line = True)

				if self.switches["testing"] == True:
					handle = "@arroba"
					id = "UCwCC0_ax9am34MtX8EFrRGA"

				media["Handle"] = handle
				media["ID"] = id

			# Ask for the media staff information
			if "Staff keys" in media:
				for key in media["Staff keys"]:
					text = self.JSON.Language.language_texts[key + ", title()"]

					if self.switches["testing"] == False:
						media[key.capitalize()] = self.Input.Type(text + ":", next_line = True, accept_enter = False)

					if self.switches["testing"] == True:
						media[key.capitalize()] = text

			# Ask for the original language of the media
			show_text = self.JSON.Language.language_texts["languages, title()"]
			select_text = self.JSON.Language.language_texts["language, title()"]

			languages = list(self.languages["full"].values())
			languages.append("[" + self.JSON.Language.language_texts["empty, title()"] + "]")

			if self.switches["testing"] == False:
				language = self.Input.Select(show_text = show_text, select_text = select_text, options = languages)["option"]

				if language != "[" + self.JSON.Language.language_texts["empty, title()"] + "]":
					media["Language"] = language

			if self.dictionary["Media type"]["Plural"]["en"] != self.texts["videos, title()"]["en"]:
				# Ask if the media has dubbing
				if self.switches["testing"] == False:
					media["Dubbing"] = self.Input.Yes_Or_No(self.JSON.Language.language_texts["dubbing, title()"], convert_to_text = True)

				if self.switches["testing"] == True:
					media["Dubbing"] = self.JSON.Language.language_texts["yes, title()"]

			# Ask for the media status
			show_text = self.language_texts["select_one_watching_status_from_the_status_list"]
			select_text = self.JSON.Language.language_texts["status, title()"]

			if self.switches["testing"] == False:
				status = self.Input.Select(show_text = show_text, select_text = select_text, options = self.language_texts["statuses, type: list"])["option"]

			if self.switches["testing"] == True:
				status = self.language_texts["statuses, type: list"][0]

			media["Status"] = status

			# Ask for the media origin type
			show_text = self.JSON.Language.language_texts["origin_types"]
			select_text = self.JSON.Language.language_texts["origin_type"]

			if self.switches["testing"] == False:
				media["Origin type"] = self.Input.Select(show_text = show_text, select_text = select_text, options = self.JSON.Language.language_texts["origin_types, type: list"])["option"]

			if self.switches["testing"] == True:
				media["Origin type"] = self.JSON.Language.language_texts["origin_types, type: list"][0]

			if self.dictionary["Media type"]["Plural"]["en"] != self.texts["videos, title()"]["en"]:
				# Ask if the user wants to add the "Dubbed" text to the media title
				if self.switches["testing"] == False:
					media["Dubbed to the media title"] = self.Input.Yes_Or_No(self.language_texts["dubbed_to_the_media_title"], convert_to_text = True)

				if self.switches["testing"] == True:
					media["Dubbed to the media title"] = self.JSON.Language.language_texts["yes, title()"]

		if self.item == True:
			# Define the media staff information
			if "Staff keys" in media:
				for key in media["Staff keys"]:
					if key.capitalize() in self.media:
						media[key.capitalize()] = self.media[key.capitalize()]

			# Ask for the playlist information if the media type is "Videos"
			if self.dictionary["Media type"]["Plural"]["en"] == self.texts["videos, title()"]["en"]:
				if self.switches["testing"] == False:
					id = self.Input.Type(self.JSON.Language.language_texts["id, upper()"], next_line = True)

				if self.switches["testing"] == True:
					id = "PLrVhyUnEQMV-eML_NqunfE0uOunraC0Xu"

				if "?list=" in media["ID"]:
					media["ID"] = media["ID"].split("?list=")[1]

			if self.dictionary["Media type"]["Plural"]["en"] != self.texts["videos, title()"]["en"]:
				# Ask the user to select the media item type
				show_text = self.JSON.Language.language_texts["types, title()"]
				select_text = self.JSON.Language.language_texts["type, title()"]

				# Ask which secondary type the media item is
				self.local_secondary_types = self.secondary_types["Singular"][self.user_language]

				empty_text = "[" + self.JSON.Language.language_texts["empty, title()"] + "]"

				self.local_secondary_types.append(empty_text)

				if self.switches["testing"] == False:
					media_item_type = self.Input.Select(show_text = show_text, select_text = select_text, options = self.local_secondary_types)["option"]

				if self.switches["testing"] == True:
					media_item_type = self.local_secondary_types[3]

				if media_item_type == empty_text:
					media_item_type = ""

				if media_item_type != empty_text:
					media["Type"] = media_item_type

				# Ask if the media item is a single unit
				if self.switches["testing"] == False:
					media["Single unit"] = self.Input.Yes_Or_No(self.language_texts["single_unit"], convert_to_text = True)

				if self.switches["testing"] == True:
					media["Single unit"] = self.JSON.Language.language_texts["yes, title()"]

				# Ask if the media item title replaces the media title
				if self.switches["testing"] == False:
					media["Replace title"] = self.Input.Yes_Or_No(self.language_texts["replace_title"], convert_to_text = True)

				if self.switches["testing"] == True:
					media["Replace title"] = self.JSON.Language.language_texts["yes, title()"]

		if self.dictionary["Media type"]["Plural"]["en"] != self.texts["videos, title()"]["en"]:
			# Ask if the user wants to always watch the media (item) dubbed
			if self.switches["testing"] == False:
				media["Watch dubbed"] = self.Input.Yes_Or_No(self.language_texts["watch_dubbed"], convert_to_text = True)

			if self.switches["testing"] == True:
				media["Watch dubbed"] = self.JSON.Language.language_texts["yes, title()"]

			# Ask for title and episode separators
			media["Separators"] = {}

			for item_type in ["title", "episode"]:
				text = self.JSON.Language.language_texts[item_type + "_separator"]

				if self.switches["testing"] == False:
					separator = self.Input.Type(text, next_line = True)

				if self.switches["testing"] == True:
					separator = ""

				if separator != "":
					media["Separators"][item_type] = separator

		media = self.Create_Details(media)

		return media

	def Create_Details(self, media):
		media["Details"] = {
			self.JSON.Language.language_texts["original_title"]: media["Title"]
		}

		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language][self.user_language]

			key = self.JSON.Language.language_texts["title_in_{}"].format(translated_language) 

			if language in media["Titles"]:
				media["Details"][key] = media["Titles"][language]

		if self.dictionary["Media type"]["Plural"]["en"] != self.texts["videos, title()"]["en"] and "Romanized" in media["Titles"]:
			key = self.JSON.Language.language_texts["romanized_title"]

			media["Details"][key] = media["Titles"]["Romanized"]

		media["Details"][self.Date.language_texts["year, title()"]] = ""
		media["Details"][self.Date.language_texts["start_date"]] = ""

		if self.dictionary["Media type"]["Plural"]["en"] != self.texts["videos, title()"]["en"]:
			media["Details"][self.Date.language_texts["year, title()"]] = media["Year"]

			if "Start date" in media:
				media["Details"][self.Date.language_texts["start_date"]] = media["Start date"]

			if "End date" in media:
				media["Details"][self.Date.language_texts["end_date"]] = media["End date"]

		if "Staff keys" in media:
			for key in media["Staff keys"]:
				text_key = key

				if ", " not in media[key.capitalize()]:
					text_key = text_key[:-1]

				text_key = self.JSON.Language.language_texts[text_key + ", title()"]

				if key.capitalize() in media:
					media["Details"][text_key] = media[key.capitalize()]

		if self.item == False:
			if "Handle" in media:
				media["Details"][self.JSON.Language.language_texts["handle, title()"]] = media["Handle"]

			if "ID" in media:
				media["Details"][self.JSON.Language.language_texts["id, upper()"]] = media["ID"]

			if self.dictionary["Media type"]["Plural"]["en"] == self.texts["videos, title()"]["en"]:
				media["Link"] = self.remote_origins["YouTube"] + "channel/" + media["ID"]

			if "Language" in media:
				media["Details"][self.JSON.Language.language_texts["original_language"]] = media["Language"]

			if self.dictionary["Media type"]["Plural"]["en"] != self.texts["videos, title()"]["en"]:
				if media["Dubbing"] != self.JSON.Language.language_texts["no, title()"]:
					media["Details"][self.JSON.Language.language_texts["dubbing, title()"]] = media["Dubbing"]

				if media["Status"] != self.JSON.Language.language_texts["remote, title()"]:
					media["Details"][self.JSON.Language.language_texts["status, title()"]] = media["Status"]

			media["Details"][self.JSON.Language.language_texts["origin_type"]] = media["Origin type"]

			if self.dictionary["Media type"]["Plural"]["en"] != self.texts["videos, title()"]["en"] and media["Dubbed to the media title"] != self.JSON.Language.language_texts["no, title()"]:
				media["Details"][self.language_texts["dubbed_to_the_media_title"]] = media["Dubbed to the media title"]

		if self.item == True:
			if self.dictionary["Media type"]["Plural"]["en"] == self.texts["videos, title()"]["en"]:
				media["Details"][self.JSON.Language.language_texts["origin_location"]] = media["ID"]
				media["Details"][self.JSON.Language.language_texts["link, title()"]] = self.remote_origins["YouTube"] + "playlist?list=" + media["ID"]

			if self.dictionary["Media type"]["Plural"]["en"] != self.texts["videos, title()"]["en"]:
				if (
					"Type" in media and
					media["Type"] != ""
				):
					media["Details"][self.JSON.Language.language_texts["type, title()"]] = media["Type"]

				if media["Single unit"] != self.JSON.Language.language_texts["no, title()"]:
					media["Details"][self.language_texts["single_unit"]] = media["Single unit"]

				if media["Replace title"] != self.JSON.Language.language_texts["no, title()"]:
					media["Details"][self.language_texts["replace_title"]] = media["Replace title"]

		if self.dictionary["Media type"]["Plural"]["en"] != self.texts["videos, title()"]["en"]:
			if media["Watch dubbed"] != self.JSON.Language.language_texts["no, title()"]:
				media["Details"][self.language_texts["watch_dubbed"]] = media["Watch dubbed"]

			if media["Separators"] != {}:
				for item_type in media["Separators"]:
					separator = media["Separators"][item_type]

					text = self.JSON.Language.language_texts[item_type + "_separator"]

					media["Details"][text] = separator

		# Create the media (item) folders
		media["Folders"] = {
			"root": self.dictionary["Media type"]["Folders"]["Media information"]["root"] + self.Sanitize(self.media["Title"], restricted_characters = True) + "/"
		}

		self.Folder.Create(media["Folders"]["root"])

		if self.item == True:
			media["Folders"]["root"] += self.dictionary["Media type"]["Subfolders"]["Plural"] + "/" + self.Sanitize_Title(media["Title"]) + "/"
			self.Folder.Create(media["Folders"]["root"])

		# Create the media (item) details file
		media["Folders"]["details"] = media["Folders"]["root"] + self.JSON.Language.language_texts["details, title()"] + ".txt"
		self.File.Create(media["Folders"]["details"])

		# Write into the media (item) details file
		self.File.Edit(media["Folders"]["details"], self.Text.From_Dictionary(media["Details"]), "w")

		# Remove the "folders" dictionary to let "Select_Media" create it
		media.pop("Folders")

		return media

	def Add_To_The_Database(self):
		self.dictionary["Media type"]["JSON"] = self.JSON.To_Python(self.dictionary["Media type"]["Folders"]["Media information"]["Information"])

		# Add to the titles list
		self.dictionary["Media type"]["JSON"]["Titles"].append(self.media["Title"])

		# Add to the status titles list
		english_status = self.Get_Language_Status(self.media["Status"])

		self.dictionary["Media type"]["JSON"]["Status"][english_status].append(self.media["Title"])

		# Update the number of media inside the json dictionary
		self.dictionary["Media type"]["JSON"]["Number"] = len(self.dictionary["Media type"]["JSON"]["Titles"])

		# Edit the "Info.json" file with the new dictionary
		self.JSON.Edit(self.dictionary["Media type"]["Folders"]["Media information"]["Information"], self.dictionary["Media type"]["JSON"])

	def Add_Media_Items(self):
		# Ask if the media has media items
		self.local_secondary_types = self.secondary_types["Plural"][self.user_language]

		text = self.language_texts["has_media_items"] + " (" + self.JSON.Language.language_texts["like"] + " " + self.Text.List_To_Text(self.local_secondary_types, or_ = True, lower = True) + ")"

		self.media["States"]["Media item list"] = self.Input.Yes_Or_No(text)

		self.first_time = True

		from copy import deepcopy

		if self.media["States"]["Media item list"] == True:
			# Delete the unused folders
			self.Folder.Delete(self.dictionary["Media"]["Item"]["Folders"]["Watched"]["root"])
			self.Folder.Delete(self.dictionary["Media"]["Item"]["Folders"]["comments"]["root"])
			self.Folder.Delete(self.dictionary["Media"]["Item"]["Folders"]["titles"]["root"])

			# Define the media items dictionary with the folders and number keys
			self.media["Items"] = {
				"Folders": {
					"root": self.media["Folders"]["root"] + self.dictionary["Media type"]["Subfolders"]["Plural"] + "/"
				},
				"Number": 0
			}

			self.Folder.Create(self.media["Items"]["Folders"]["root"])

			# Iterate through item type keys
			for name in ["List", "Current"]:
				key = name

				if name == "List":
					key = "Plural"

				# Define the item type text file
				self.media["Items"]["Folders"][name.lower()] = self.media["Items"]["Folders"]["root"] + self.dictionary["Media type"]["Subfolders"][key] + ".txt"
				self.File.Create(self.media["Items"]["Folders"][name.lower()])

				# Get the contents of the text file
				self.media["Items"][name] = self.File.Contents(self.media["Items"]["Folders"][name.lower()])["lines"]

				# If the contents is not empty and the item type is "current"
				if (
					self.media["Items"][name] != [] and
					name == "Current"
				):
					# Define the contents as the first line of the text file
					self.media["Items"][name] = self.media["Items"][name][0]

				# If the item type is "list"
				if name == "List":
					# Define the items number as the number of lines of the text file
					self.media["Items"]["Number"] = len(self.media["Items"]["List"])

			self.media["States"]["First media item"] = True
			self.media["States"]["Add more"] = True

			add_text = self.language_texts["add_more"]

			# Ask for the media information
			while self.media["States"]["Add more"] == True:
				media_item = self.Type_Media_Information(item = True)

				# Update the media items number
				self.media["Items"]["Number"] += 1

				# Add to media items list
				self.media["Items"]["List"].append(media_item["Title"])

				if self.media["States"]["First media item"] == True:
					self.media["States"]["First media item"] = False

				self.media["States"]["Add more"] = self.Input.Yes_Or_No(self.JSON.Language.language_texts["add_more"])

			# Update the media items list file
			self.File.Edit(self.media["Items"]["Folders"]["list"], self.Text.From_List(self.media["Items"]["List"]), "w")

			# Define the current media item as the first one
			self.media["Items"]["Current"] = [
				self.media["Items"]["List"][0]
			]

			# Update the current media item file
			self.File.Edit(self.media["Items"]["Folders"]["current"], self.Text.From_List(self.media["Items"]["Current"]), "w")

			self.dictionary["Media"].pop("Folders")