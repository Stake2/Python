# Convert_History.py

from Watch_History.Watch_History import Watch_History as Watch_History

# Import the "importlib" module
import importlib

class Convert_History(Watch_History):
	def __init__(self):
		super().__init__()

		print()
		print(self.separators["5"])
		print()
		print(self.language_texts["convert_history"] + ":")

		#self.Per_Media()
		self.With_File()
		#self.By_Year()
		#self.Fix_Comment_Dictionaries()

	def Per_Media(self):
		from copy import deepcopy

		# Define the root dictionary with the media type and media
		self.dictionary = {
			"Media type": self.media_types["Videos"],
			"Media": {
				"Title": "FAGames"
			}
		}

		# Select the media and define its variables, returning the media dictionary (without asking the user to select the media)
		self.dictionary = self.Select_Media(self.dictionary)

		# Define the media item dictionary
		self.dictionary.update(self.Define_Media_Item(deepcopy(self.dictionary), media_item = "DayZ"))

		self.media = self.dictionary["Media"]

		# Create the Watched dictionary
		self.watched = {
			"Entries file": self.dictionary["Media"]["Item"]["Folders"]["Watched"]["entries"],
			"Entries": self.JSON.To_Python(self.dictionary["Media"]["Item"]["Folders"]["Watched"]["entries"]),
			"Entry list": self.File.Contents(self.dictionary["Media"]["Item"]["Folders"]["Watched"]["entry_list"])["lines"],
			"Files": self.dictionary["Media"]["Item"]["Folders"]["Watched"]["files"],
			"Correct titles file": self.dictionary["Media"]["Item"]["Folders"]["Watched"]["root"] + "Correct titles.txt"
		}

		self.watched["Correct titles"] = self.File.Contents(self.watched["Correct titles file"])["lines"]

		# Create the "Correct titles.txt" file
		self.File.Create(self.watched["Correct titles file"])

		if self.watched["Correct titles"] == []:
			titles_list = []

			for entry in self.watched["Entries"]["Dictionary"].values():
				titles_list.append(entry["Episode"]["Titles"][self.media["Language"]])

			self.File.Edit(self.watched["Correct titles file"], self.Text.From_List(titles_list, next_line = True), "a")

			self.watched["Correct titles"] = self.File.Contents(self.watched["Correct titles"])["lines"]

		#self.Iterate_Through_Watched_Entries()
		self.Per_Media_Run()

	def Iterate_Through_Watched_Entries(self):
		entries = list(self.watched["Entries"]["Dictionary"].values())

		list_ = []

		i = 0
		while i < len(entries):
			entry = entries[i]

			date = entry["Entry"].split(")")[0].split(" ")[-1]

			if date not in list_:
				print()
				print("-----")

				self.Text.Copy(date, verbose = False)

				self.Input.Type(self.Date.language_texts["date, title()"] + ":\n" + date, add_colon = False, next_line = True)

			print("-")
			print()

			if date not in list_:
				list_.append(date)

			time = entry["Entry"].split("(")[1].split(" ")[0]

			print(str(i + 1) + "/" + str(len(entries)) + ":")
			print(time + " " + date)
			print()
			print(entry["Episode"]["Titles"][self.media["Language"]])

			self.Text.Copy(time, verbose = False)

			new_title = self.Input.Type(self.Language.language_texts["title, title()"], next_line = True)

			if new_title != "":
				self.watched["Correct titles"][i] = new_title

				self.File.Edit(self.watched["Correct titles file"], self.Text.From_List(self.watched["Correct titles"], next_line = True), "w")

			i += 1

	def Per_Media_Run(self):
		# Get the Entries keys list
		entry_keys = self.watched["Entries"]["Entries"]

		year = self.date["Units"]["Year"]

		year_dictionary = {}

		media_type_key = self.dictionary["Media type"]["Plural"]["en"].lower().replace(" ", "_")

		# Iterate through the correct titles list
		i = 0
		for correct_title in self.watched["Correct titles"]:
			# Get the Watched Entry dictionary
			watched_entry = self.watched["Entries"]["Dictionary"][entry_keys[i]]

			# Get the year that the user watched the media unit
			year = str(watched_entry["Date"].split("-")[0])

			if year not in year_dictionary:
				year_dictionary[year] = {
					"Entries file": self.folders["Watch History"][year]["entries"],
					"Entries": "",
					"Media type Entries file": self.folders["Watch History"][year]["per_media_type"][media_type_key]["entries"],
					"Media type Entries": ""
				}

				year_dictionary[year]["Entries"] = self.JSON.To_Python(year_dictionary[year]["Entries file"])
				year_dictionary[year]["Media type Entries"] = self.JSON.To_Python(year_dictionary[year]["Media type Entries file"])

			# Get the year Entry
			year_entry = year_dictionary[year]["Entries"]["Dictionary"][entry_keys[i]]

			# Get the year media type Entry
			media_type_entry = year_dictionary[year]["Media type Entries"]["Dictionary"][entry_keys[i]]

			# If the episode title inside the Entry dictionary is not the correct title
			if year_entry["Episode"]["Titles"][self.media["Language"]] != correct_title:
				wrong_title = year_entry["Episode"]["Titles"][self.media["Language"]]

				# Iterate through the episode titles list to get the episode title in all languages
				e = 0
				for episode_title in self.media["Item"]["Episodes"]["Titles"][self.media["Language"]]:
					# If the current episode title is equal to the correct title
					if episode_title == correct_title:
						titles = {}

						for key in year_entry["Episode"]["Titles"]:
							titles[key] = self.media["Item"]["Episodes"]["Titles"][key][e]

						id = self.media["Item"]["Episodes"]["Titles"]["IDs"][e]

					e += 1

				# Update the episode titles, IDs, and media unit links
				for dict_ in [year_entry, media_type_entry, watched_entry]:
					dict_["Episode"]["Titles"] = titles
					dict_["ID"] = id
					dict_["Link"] = dict_["Link"][:32] + dict_["ID"] + dict_["Link"][43:]

				# Define the Entry dictionary
				self.dictionary["Entry"] = {
					"Name": {
						"Normal": year_entry["Entry"],
						"Sanitized": year_entry["Entry"].replace(":", ";").replace("/", "-")
					},
					"Current year": self.Years.years["Dictionary"][year]
				}

				# Update the episode title in the year Entry file
				per_media_type_folder = self.folders["Watch History"][year]["per_media_type"][media_type_key]["files"]["root"]
				year_entry_file = per_media_type_folder + self.dictionary["Entry"]["Name"]["Sanitized"] + ".txt"

				# Get the Entry file lines
				lines = self.File.Contents(year_entry_file)["lines"]

				# Update the episode titles lines inside the Entry file
				lines[10] = titles[self.media["Language"]]
				lines[11] = titles["en"]

				# Update the year Entry file
				self.File.Edit(year_entry_file, self.Text.From_List(lines, next_line = True), "w")

				# Iterate through the small languages list
				for language in self.languages["small"]:
					full_language = self.languages["full"][language]

					# Get the root and type folder
					root_folder = self.Language.texts["watched_media"][language]
					type_folder = self.dictionary["Media type"]["Plural"][language]

					# Get the type folder inside the root folder which is inside the year language folder
					folder = self.dictionary["Entry"]["current_year"]["Folders"][full_language][root_folder][type_folder]["root"]
					file_name = self.dictionary["Entry"]["Name"]["Sanitized"]

					# Get the year Entry file per language
					file = folder + file_name + ".txt"

					# Get the file and update the episode title inside it
					lines = self.File.Contents(file)["lines"]
					lines[10] = titles[language]

					# Update the year Entry file per language
					self.File.Edit(file, self.Text.From_List(lines, next_line = True), "w")

				# Update the episode title in the Watched Entry file
				watched_entry_file = self.watched["Files"]["root"] + watched_entry["Entry"].replace(":", ";").replace("/", "-") + ".txt"

				# Get the Entry file lines
				lines = self.File.Contents(watched_entry_file)["lines"]

				# Update the episode titles lines inside the Entry file
				lines[10] = titles[self.media["Language"]]

				# Update the Watched Entry file
				self.File.Edit(watched_entry_file, self.Text.From_List(lines, next_line = True), "w")

				# --- #

				# Update the year "Entries.json" file
				self.JSON.Edit(year_dictionary[year]["Entries file"], year_dictionary[year]["Entries"])

				# Update the year media type "Entries.json" file
				self.JSON.Edit(year_dictionary[year]["Media type Entries file"], year_dictionary[year]["Media type Entries"])

				# Update the Watched "Entries.json" file
				self.JSON.Edit(self.watched["Entries file"], self.watched["Entries"])

				print()

				print(self.Language.language_texts["entry, title()"] + ":")
				print("[" + year_entry["Entry"] + "]")
				print()

				print(self.Language.language_texts["line, title()"] + ":")
				print("[" + str(i + 1) + "]")
				print()

				print(self.Language.language_texts["wrong, title()"] + ":")
				print("[" + wrong_title + "]")
				print()

				print(self.Language.language_texts["right, title()"] + ":")
				print("[" + correct_title + "]")

				if self.switches["Testing"] == True:
					self.Input.Type(self.Language.language_texts["continue, title()"])

				print()
				print("-----")

			i += 1

		# Get the Comments dictionary
		self.comments = {
			"Comments": self.JSON.To_Python(self.dictionary["Media"]["Item"]["Folders"]["comments"]["comments"])
		}

	def With_File(self):
		from copy import deepcopy

		# Copy the switches dictionary
		switches_dictionary = deepcopy(self.switches)

		# Define the classes to be imported
		classes = [
			"Watch_Media",
			"Register"
		]

		# Import them
		for title in classes:
			# Import the module
			module = importlib.import_module("." + title, self.__module__.split(".")[0])

			# Get the sub-class
			sub_class = getattr(module, title)

			# Add the sub-class to the current module
			setattr(self, title, sub_class)

		# Show the "with_file" text
		print(self.Language.language_texts["with_file"])
		print()

		# Get the History dictionary to update the entries number
		self.dictionaries["History"] = self.JSON.To_Python(self.folders["Watch History"]["History"])

		self.year = str(self.date["Units"]["Year"])

		# Define the year dictionary with the year number and folders
		self.year = {
			"Number": self.year,
			"Folders": {
				"root": self.folders["Watch History"]["root"] + self.year + "/"
			},
			"Entries": self.dictionaries["Entries"]
		}

		# Define the "Pre-entries.json" file
		self.year["Folders"]["Pre-entries"] = self.year["Folders"]["root"] + "Pre-entries.json"

		# Read the "Pre-entries.json" file
		self.year["Pre-entries"] = self.JSON.To_Python(self.year["Folders"]["Pre-entries"])

		# Define the Pre-entries dictionary template
		self.pre_entries = {
			"Items": {
				"Media": "Media title",
				"Item": "Media item",
				"Type": "Media type"
			},
			"Entries": {
				"1": {
					"Item": "Media item",
					"Title": "Episode title",
					"Date": "01:20 01/03/2024"
				}
			}
		}

		# Get the pre-entries list
		pre_entries_list = list(self.year["Pre-entries"]["Entries"].values())

		# Define the item names list
		item_names = ["Item", "Title", "Date"]

		# Remove item names that are already defined
		for item_name in item_names:
			if item_name in self.year["Pre-entries"]["Items"]:
				item_names.remove(item_name)

		# Ask for the pre-entries if the list is empty
		# Or if the "Fill file" switch is True
		if (
			pre_entries_list == [] or
			"Switches" in self.year["Pre-entries"] and
			"Fill file" in self.year["Pre-entries"]["Switches"] and
			self.year["Pre-entries"]["Switches"]["Fill file"] == True
		):
			# Get the media dictionary if it exists
			if "Media" in self.year["Pre-entries"]["Items"]:
				# Define the default dictionary with the media type and media title
				self.dictionary = {
					"Media type": self.media_types["Videos"],
					"Media": {
						"Title": self.year["Pre-entries"]["Items"]["Media"]
					}
				}

				# Select the media to define its variables
				self.year["Media"] = self.Select_Media(self.dictionary)["Media"]

			# Define the number of pre-entries
			number = 1

			# Define the "add_more" variable
			title = ""

			# While the variable above is True
			while title != "stop":
				# Show a dash and space separator, and the number
				print(self.separators["5"])
				print()
				print(self.Language.language_texts["number, title()"] + ":")
				print("[" + str(number) + "/" + str(number) + "]")

				# Define the empty entry dictionary
				entry = {}

				# Ask for the title and date of the entry
				for item_name in item_names:
					# If the "Media" key is inside the year dictionary
					# And the item name is not "Item"
					# Or the "Media" key is inside the year dictionary
					if (
						"Media" in self.year and
						item_name != "Item" or
						"Media" not in self.year
					):
						# Define the text key
						text_key = item_name.lower() + ", title()"

						# Get the language text
						language_text = self.Language.language_texts[text_key]

						ask_for_item = True

						if (
							item_name == "Date" and
							entry["Title"] == "stop"
						):
							ask_for_item = False

						if ask_for_item == True:
							regex = None

							if item_name == "Date":
								regex = {
									"Regex": "^([0-9]{2}:[0-9]{2} [0-9]{2}/[0-9]{2})$",
									"Example": self.Date.Now()["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"][:-5]
								}

							# Ask for the entry item
							value = self.Input.Type(language_text, next_line = True, regex = regex)

							if item_name == "Date":
								value += "/2024"

					# If the "Media" key is inside the year dictionary
					# And the item name is "Item"
					if (
						"Media" in self.year and
						item_name == "Item"
					):
						# Get the media items list
						media_items = self.year["Media"]["Items"]["List"]

						# Ask the user to select a media item
						show_text = self.Language.language_texts["items, title()"]
						select_text = self.Language.language_texts["item, title()"]

						value = self.Input.Select(media_items, show_text = show_text, select_text = select_text)["option"]

					# Add the item value to the entry dictionary
					entry[item_name] = value

				# Define the value of the "title" variable
				title = entry["Title"]

				# Add the entry to the pre-entries list
				pre_entries_list.append(entry)

				# Add the entry to the Pre-entries dictionary
				self.year["Pre-entries"]["Entries"][str(number)] = entry

				# Add to the pre-entries number
				number += 1

				print()

				# Update the "Pre-entries.json" file with the updated "Pre-entries" dictionary
				self.JSON.Edit(self.year["Folders"]["Pre-entries"], self.year["Pre-entries"])

		last_pre_entry = pre_entries_list[-1]

		items = [
			"Type",
			"Media",
			"Item"
		]

		# Iterate through the Entries list
		e = 0
		for entry in pre_entries_list:
			if entry["Title"] == last_pre_entry["Title"]:
				print()

			for item in items:
				if item not in entry:
					entry[item] = self.year["Pre-entries"]["Items"][item]

			# Define the progress text with the progress (current number and entries number)
			# Media type, entry date, and title
			progress_text = "-----" + "\n" + \
			"\n" + \
			self.Language.language_texts["number, title()"] + ":" + "\n" + \
			"[" + str(e + 1) + "/" + str(len(pre_entries_list)) + "]" + "\n" + "\n" + \
			self.Language.language_texts["type, title()"] + ":" + "\n" + \
			"[" + entry["Type"] + "]" + "\n" + \
			"\n" + \
			self.Date.language_texts["date, title()"] + ":" + "\n" + \
			"[" + entry["Date"] + "]" + "\n" + \
			"\n" + \
			self.Language.language_texts["title, title()"] + ":" + "\n" + \
			"[" + entry["Title"] + "]" + "\n"

			# Convert the Date to UTC
			entry["Date"] = self.Date.To_UTC(self.Date.From_String(entry["Date"], "%H:%M %d/%m/%Y"))

			# Show the progress text
			print(progress_text)

			# Define the root dictionary with the media type and media
			self.dictionary = {
				"Media type": self.media_types[entry["Type"]],
				"Media": {
					"Title": entry["Media"]
				}
			}

			# Select the media and define its variables, returning the media dictionary (without asking the user to select the media)
			self.dictionary = self.Select_Media(self.dictionary)

			# Define the media dictionary to speed up typing
			self.media = self.dictionary["Media"]

			# Show the media title
			text = self.Language.language_texts["media, title()"] + ":" + "\n" + \
			"[" + self.media["Title"] + "]"

			progress_text += "\n" + text + "\n"

			print(text)

			# Define the media item dictionary
			if "Item" in entry:
				self.dictionary.update(self.Define_Media_Item(deepcopy(self.dictionary), media_item = entry["Item"]))

			# Define the media dictionary to speed up typing
			self.media = self.dictionary["Media"]

			# Show the media item title
			if self.media["Item"]["Title"] != self.media["Title"]:
				text = "[" + self.media["Item"]["Title"] + "]"

				progress_text += "\n" + self.Language.language_texts["item"].title() + ":" + "\n" + \
				text + "\n"

				print()
				print(self.Language.language_texts["item"].title() + ":")
				print(text)

			# Define the title
			self.dictionary["Defined title"] = entry["Title"]

			# Add the Entry dictionary to the root dictionary
			self.dictionary.update({
				"Entry": {
					"Date": entry["Date"]
				}
			})

			# Run the "Watch_Media" class to define more media variables
			self.dictionary = self.Watch_Media(self.dictionary, open_media = False).dictionary

			self.media = self.dictionary["Media"]

			self.media["States"]["Finished watching"] = True

			self.media["States"]["Replace title"] = False

			self.dictionary["Comment Writer"] = {
				"States": {
					"Backup": True,
					"New": True,
					"Make": False,
					"Write": False
				}
			}

			states_dictionary = deepcopy(self.media["States"])

			comment_entry = ""

			# Comment file name for non-movies
			if states_dictionary["Series media"] == True:
				add = False

				for alternative_episode_type in self.alternative_episode_types:
					if alternative_episode_type in self.media["Episode"]["Separator"]:
						add = True

				if add == True:
					comment_entry += self.media["Episode"]["Separator"] + " "

				if states_dictionary["Episodic"] == True:
					if "Number text" in self.media["Episode"]:
						comment_entry += self.media["Episode"]["Number text"]

					else:
						comment_entry += str(self.Text.Add_Leading_Zeroes(self.media["Episode"]["Number"]))

				if states_dictionary["Episodic"] == False:
					comment_entry = self.media["Episode"]["Title"]

					if self.media["Language"] != self.user_language:
						comment_entry = self.media["Episode"]["Titles"][self.media["Language"]]

			# Comment file name for movies or single unit media items
			if (
				states_dictionary["Series media"] == False or
				states_dictionary["Single unit"] == True
			):
				comment_entry = self.Language.language_texts["comment, title()"]

			# If the comment entry name exists inside the media Comments dictionary
			if comment_entry in self.media["Item"]["Comments"]["Entries"]:
				# Get the Comment dictionary from the media Comments dictionary
				entry["Comment"] = self.media["Item"]["Comments"]["Dictionary"][comment_entry]

				# Define the keys to be removed from the "Comment" dictionary
				keys_to_remove = [
					"Entry",
					"Type",
					"Titles",
					"States",
					"Lines"
				]

				if self.media["States"]["Episodic"] == False:
					keys_to_remove.append("Number")

				# Remove not useful keys from "Comment" dictionary
				for key in keys_to_remove:
					if key in entry["Comment"]:
						entry["Comment"].pop(key)

				self.dictionary["Comment Writer"]["Comment"] = entry["Comment"]

				# Remove the Comment dictionary from the Entry dictionary if the date is empty
				# And the "ID" key is not inside the Comment dictionary
				# Or the Comment dictionary contains only the "Date" key
				# And the comment date is the same as the entry date
				# (The Comment dictionary is only useful to be inside of the Entry dictionary if it contains the date of the comment)
				if (
					entry["Comment"]["Date"] == "" and
					"ID" not in entry["Comment"] or
					list(entry["Comment"].keys()) == ["Date"] and
					entry["Comment"]["Date"] == entry["Date"]
				):
					entry.pop("Comment")

					self.dictionary["Comment Writer"].pop("Comment")

				# Set the "Commented" state as True
				states_dictionary["Commented"] = True

			# Define the states dictionary
			self.media["States"] = states_dictionary
			self.dictionary["Media"]["States"] = states_dictionary

			# Keep the original switches inside the "Switches.json" file before running the "Register" class
			self.Global_Switches.Switch(switches_dictionary)

			self.dictionary["Dictionaries"] = self.dictionaries

			# Update the "dictionaries" variable
			setattr(self.Register, "dictionaries", self.dictionary["Dictionaries"])

			# Run the "Register" class to register the media unit
			register = self.Register(self.dictionary)

			# Get the updated "dictionaries" variable from the "Register" class
			self.dictionary["Dictionaries"] = getattr(register, "dictionaries")

			if progress_text[-1] == "\n":
				progress_text = progress_text[:-1]

			# Show the progress text
			print()
			print(progress_text)

			# If the entry title is not the last one
			# And the testing switch is True
			if (
				entry["Title"] != last_pre_entry["Title"] and
				self.switches["Testing"] == True
			):
				# Ask for user input before continuing the conversion
				self.Input.Type(self.Language.language_texts["continue, title()"] + " (" + self.Language.language_texts["next, feminine"].title() + " " + self.Language.language_texts["entry"] + ")")

				# Show a space separator
				print()

			# Show a five dash separator if the entry is the last one
			if entry["Title"] == last_pre_entry["Title"]:
				print()
				print("-----")

			e += 1

	def By_Year(self):
		from copy import deepcopy

		# Copy the switches dictionary
		switches_dictionary = deepcopy(self.switches)

		# Import the Watch_Media class
		from Watch_History.Watch_Media import Watch_Media as Watch_Media

		self.Watch_Media = Watch_Media

		# Import the Register class
		from Watch_History.Register import Register as Register

		self.Register = Register

		# Get the History dictionary to update the entries number
		self.dictionaries["History"] = self.JSON.To_Python(self.folders["Watch History"]["History"])

		self.years_list = range(2018, self.date["Units"]["Year"] + 1)

		# Iterate through the years list (of the years that contain a "Watch_History" folder)
		for self.year in self.years_list:
			# Convert the year number into a string
			self.year = str(self.year)

			# Define the year dictionary with the year number and folders
			self.year = {
				"Number": self.year,
				"Folders": {
					"root": self.folders["Watch History"]["root"] + self.year + "/"
				},
				"Entries dictionary": deepcopy(self.template),
				"Lists": {}
			}

			print()
			print("----------")
			print()
			print(self.Date.language_texts["year, title()"] + ": " + self.year["Number"])

			# Define the history folders
			for folder_name in ["Per Media Type"]:
				key = folder_name.lower().replace(" ", "_")

				# Define the folder
				self.year["Folders"][key] = {
					"root": self.year["Folders"]["root"] + folder_name + "/"
				}

				self.Folder.Create(self.year["Folders"][key]["root"])

			# Define the "Files" folder inside the "Per Media Type"
			self.year["Folders"]["per_media_type"]["files"] = {
				"root": self.year["Folders"]["per_media_type"]["root"] + "Files/"
			}

			exist = False

			# Define and create the "Entries.json" file
			self.year["Folders"]["entries"] = self.year["Folders"]["root"] + "Entries.json"

			if self.File.Exist(self.year["Folders"]["entries"]) == True:
				exist = True

			self.File.Create(self.year["Folders"]["entries"])

			# Define and create the "Entry list.txt" file
			self.year["Folders"]["entry_list"] = self.year["Folders"]["root"] + "Entry list.txt"
			self.File.Create(self.year["Folders"]["entry_list"])

			# Define the per media type "Files" folders
			for plural_media_type in self.media_types["Plural"]["en"]:
				key = plural_media_type.lower().replace(" ", "_")

				# Create the media type folder
				self.year["Folders"]["per_media_type"][key] = {
					"root": self.year["Folders"]["per_media_type"]["root"] + plural_media_type + "/"
				}

				self.Folder.Create(self.year["Folders"]["per_media_type"][key]["root"])

				# Create the "Files" media type folder
				self.year["Folders"]["per_media_type"][key]["files"] = {
					"root": self.year["Folders"]["per_media_type"][key]["root"] + "Files/"
				}

				self.Folder.Create(self.year["Folders"]["per_media_type"][key]["files"]["root"])

				# Define and create the media type "Entries.json" file
				self.year["Folders"]["per_media_type"][key]["entries"] = self.year["Folders"]["per_media_type"][key]["root"] + "Entries.json"
				self.File.Create(self.year["Folders"]["per_media_type"][key]["entries"])

				# Define and create the media type "Entry list.txt" file
				self.year["Folders"]["per_media_type"][key]["entry_list"] = self.year["Folders"]["per_media_type"][key]["root"] + "Entry list.txt"
				self.File.Create(self.year["Folders"]["per_media_type"][key]["entry_list"])

				# Define the media type "Files" folder
				self.year["Folders"]["per_media_type"]["files"][key] = {
					"root": self.year["Folders"]["per_media_type"]["files"]["root"] + plural_media_type + "/"
				}

				# Define the media type "Episodes" file
				self.year["Folders"]["per_media_type"]["files"][key]["episodes"] = self.year["Folders"]["per_media_type"]["files"][key]["root"] + "Episodes.txt"

				if self.Folder.Exist(self.year["Folders"]["per_media_type"]["files"][key]["root"]) == True:
					# Create media type lists dictionary and read "Episodes" file
					self.year["Lists"][plural_media_type] = {
						"Episodes": self.File.Contents(self.year["Folders"]["per_media_type"]["files"][key]["episodes"])["lines"]
					}

			# Define the entry files
			for file_name in ["Episodes", "Media Types", "Number", "Times", "YouTube IDs"]:
				key = file_name.lower().replace(" ", "_")

				# Define the entry file
				self.year["Folders"][key] = self.year["Folders"]["root"] + file_name + ".txt"

				if self.File.Exist(self.year["Folders"][key]) == True:
					# Get the list of lines inside the file
					self.year["Lists"][file_name] = self.File.Contents(self.year["Folders"][key])["lines"]

			if "Episodes" in self.year["Lists"] and self.year["Number"] != list(self.years_list)[-1] and exist == False:
				self.Input.Type("Finished creating files")

			if "Episodes" in self.year["Lists"]:
				# Add to the total and comments numbers
				self.year["Entries dictionary"]["Numbers"]["Total"] = len(self.year["Lists"]["Episodes"])
				self.year["Entries dictionary"]["Numbers"]["Comments"] = self.dictionaries["Root comments"]["Numbers"]["Years"][self.year["Number"]]

				# Define the media type dictionaries
				self.media_type_dictionaries = {}

				# Iterate through the English plural media types
				for plural_media_type in self.media_types["Plural"]["en"]:
					# Create the media type dictionary with media number and media item list (with all media titles)
					self.media_type_dictionaries[plural_media_type] = {
						"Number": 1,
						"Media list": self.Get_Media_List(self.media_types[plural_media_type], self.texts["statuses, type: list"]["en"])
					}

				remove_list = self.File.Contents(self.Folder.folders["Apps"]["root"] + "Test.txt")["lines"]

				self.old_history = {
					"Current year": self.Years.years["Dictionary"][self.year["Number"]],
					"Folders": self.year["Folders"],
					"old_history": {
						"Number": self.year["Number"]
					},
					"Entries": self.dictionaries["Entries"],
					"Media type": self.dictionaries["Media type"],
					"Change year": True
				}

				# If the "Entries.json" is not empty and has entries, get Entries dictionary from it
				if self.File.Contents(self.year["Folders"]["entries"])["lines"] != [] and self.JSON.To_Python(self.year["Folders"]["entries"])["Entries"] != []:
					self.dictionaries["Entries"] = self.JSON.To_Python(self.year["Folders"]["entries"])

				# Iterate through the episodes list
				e = 0
				for entry in self.year["Lists"]["Episodes"]:
					# Define the Entry dictionary
					entry = {
						"Episode title": entry,
						"Type": self.year["Lists"]["Media Types"][e],
						"Date": self.year["Lists"]["Times"][e]
					}

					if entry["Episode title"] == self.year["Lists"]["Episodes"][0]:
						print()

					# Define the progress text with progress (current number and entries number)
					# Media type, entry time and name
					progress_text = "-----" + "\n" + \
					"\n" + \
					str(e + 1) + "/" + str(len(self.year["Lists"]["Episodes"])) + ":" + "\n" + "\n" + \
					self.Language.language_texts["type, title()"] + ":" + "\n" + \
					"[" + entry["Type"] + "]" + "\n" + \
					"\n" + \
					self.Date.language_texts["date, title()"] + ":" + "\n" + \
					"[" + entry["Date"] + "]" + "\n" + \
					"\n" + \
					self.Language.language_texts["entry, title()"] + ":" + "\n" + \
					"[" + entry["Episode title"] + "]" + "\n"

					# Show the progress text
					print(progress_text)

					# Define default media dictionary
					self.dictionary = {}

					# If testing is True and the episode title is not inside the remove list
					# Or testing is False and the remove list is empty
					if (
						self.switches["Testing"] == True and entry["Episode title"] not in remove_list or
						self.switches["Testing"] == False and remove_list == []
					):
						# Find the media and get media titles
						for media_title in self.media_type_dictionaries[entry["Type"]]["Media list"]:
							possible_options = [
								media_title,
								media_title.upper(),
								media_title.lower(),
								media_title.title(),
								media_title.capitalize()
							]

							for option in possible_options:
								possible_option = option

								if entry["Type"] == self.texts["videos, title()"]["en"]:
									possible_option = possible_option + ": "

								if possible_option in entry["Episode title"]:
									# Define the root dictionary with media type and media
									self.dictionary = {
										"Media type": self.media_types[entry["Type"]],
										"Media": {
											"Title": option
										}
									}

									# Select media and define its variables, returning the media dictionary (without asking user to select the media)
									self.dictionary = self.Select_Media(self.dictionary)

									self.Replace_Year_Number(self.dictionary["Media type"]["Folders"]["Per Media Type"], str(self.date["Units"]["Year"]), self.year["Number"])

						if self.dictionary != {}:
							self.dictionary["Old history"] = self.old_history

							# Define media dictionary to speed up typing
							self.media = self.dictionary["Media"]

							# Show media title
							print("\t" + self.media["Title"] + ":")

							# If the media has a media item list
							if self.media["States"]["Media item list"] == True:
								media_items = {}

								# Iterate through the media item list
								for media_list_item in self.media["Items"]["List"]:
									# Define the media item dictionary
									media_dictionary = self.Define_Media_Item(deepcopy(self.dictionary), media_item = media_list_item)
									media_list_item = media_dictionary["Media"]["Item"]

									# If the user language key is inside the episodes dictionary
									if self.user_language in media_list_item["episodes"]["titles"]:
										# Define the episode titles as the user language episode titles
										episode_titles = media_list_item["episodes"]["titles"][self.user_language]

									# If there is no user language key, define the episode titles as the media item title and the language item title
									# (That means that the media item is a single unit media item and has no titles list)
									if self.user_language not in media_list_item["episodes"]["titles"]:
										episode_titles = [
											media_list_item["title"],
											media_list_item["Titles"]["Language"]
										]

									if episode_titles != []:
										# Iterate through media item user language episode titles list
										for episode_title in episode_titles:
											# If the episode title is in the episode title string
											if episode_title in entry["Episode title"]:
												if media_list_item["title"] not in media_items:
													media_items[media_list_item["title"]] = media_dictionary

								media_dictionary = list(media_items.values())[0]

								# Select one of the media items if the episode title is present on more than one media item
								if len(list(media_items.keys())) > 1:
									media_item_title = self.Input.Select(list(media_items.keys()))["option"]

									media_dictionary = media_items[media_item_title]

								# Update the dictionary with the variables gotten from the media dictionary
								self.dictionary.update(deepcopy(media_dictionary))

								self.media = self.dictionary["Media"]

							# Show the media item title
							tab = "\t"

							if self.media["Item"]["Title"] != self.media["Title"]:
								tab = "\t\t"

								text = tab + "[" + self.media["Item"]["Title"] + "]"

								progress_text += "\n" + self.Language.language_texts["item"].title() + ":" + "\n" + \
								text.replace(tab, "") + "\n"

								print()
								print(text)

							# If the media is a series media
							if self.media["States"]["Series media"] == True:
								if self.media["States"]["Single unit"] == True:
									for language in self.languages["small"]:
										if language not in self.media["Episode"]["Titles"] or language in self.media["Titles"] and self.media["Episode"]["Titles"][language] == self.media["Titles"][language]:
											self.media["Episode"]["Titles"][language] = self.Get_Media_Title(self.dictionary, language = language, item = True)

										self.media["Item"]["Episodes"]["Titles"][language] = [
											self.media["Episode"]["Titles"][language]
										]

								# Iterate through episode titles list
								number = 1
								for episode_title in self.media["Item"]["Episodes"]["Titles"][self.user_language]:
									root_episode_title = entry["Episode title"]

									if " (" + self.language_texts["re_watched, capitalize()"] in root_episode_title:
										root_episode_title = root_episode_title.split(" (" + self.language_texts["re_watched, capitalize()"])[0]

									expression = episode_title in root_episode_title

									if entry["Type"] == self.texts["videos, title()"]["en"]:
										root_episode_title = root_episode_title.replace(self.media["Title"] + ": ", "")
										expression = episode_title == root_episode_title

									# If the above expression evaluates to True
									if expression:
										self.media["Episode"]["Number"] = number

										# Iterate through the languages list to get the language episode titles
										for language in self.languages["small"]:
											self.media["Episode"]["Titles"][language] = self.media["Item"]["Episodes"]["Titles"][language][number - 1]

										# Iterate through the languages list to check if a language episode title is the same as the episode title in the user language
										for language in self.languages["small"]:
											if (
												self.media["Language"] in self.media["Episode"]["Titles"][language] and
												language != self.media["Language"] and
												self.media["Episode"]["Titles"][language] == self.media["Episode"]["Titles"][self.media["Language"]]
											):
												# Import the "Fill_Media_Files" class
												if hasattr(self, "Fill_Media_Files") == False:
													from Watch_History.Media_Info.Fill_Media_Files import Fill_Media_Files as Fill_Media_Files

													self.Fill_Media_Files = Fill_Media_Files(self.dictionary)

												# Translate the title
												title = self.Fill_Media_Files.Add_Missing_Titles(language, self.media["Item"]["Episodes"]["Titles"], self.media["Episode"]["Titles"][language])

												# Update the episode title in the list
												self.media["Item"]["Episodes"]["Titles"][language][number - 1] = title

												self.Text.Copy(self.media["Item"]["Episodes"]["Titles"][language])
												self.Input.Type()

												# Update the episode titles list
												self.File.Edit(self.media["Item"]["Episodes"]["Titles"]["Files"][language], self.Text.From_List(self.media["Item"]["Episodes"]["Titles"][language], next_line = True), "w")

									number += 1

							if self.media["States"]["Series media"] == False:
								for language in self.languages["small"]:
									self.media["Episode"]["Titles"][language] = self.Get_Media_Title(self.dictionary, language = language)

							# Check if the gotten episode title is inside the entry episode title
							if self.media["Episode"]["Titles"][self.user_language] not in entry["Episode title"] and self.media["Episode"]["Titles"]["en"] not in entry["Episode title"]:
								print()
								print(entry["Episode title"])
								print(self.media["Episode"]["Titles"][self.user_language])
								print()
								input("Not equal: ")

							# If time is not unknown, convert it into a Date dictionary
							if entry["Date"] != "Unknown Watched Time - Horário Assistido Desconhecido":
								entry["Date"] = self.Date.To_UTC(self.Date.From_String(entry["Date"], "%H:%M %d/%m/%Y"))

							# Define the "Comment Writer" dictionary
							self.dictionary["Comment Writer"] = {
								"States": {
									"Write": False
								}
							}

							states_dictionary = deepcopy(self.media["States"])

							states_dictionary["Commented"] = False
							states_dictionary["Re-watching"] = False
							states_dictionary["Completed media"] = False
							states_dictionary["Completed media item"] = False
							states_dictionary["Watch dubbed"] = False
							states_dictionary["Replace title"] = False

							# If the language "Dubbed" text is inside the episode title, set the "Watch dubbed" state as True
							if self.Language.language_texts["dubbed, title()"] in entry["Episode title"]:
								states_dictionary["Watch dubbed"] = True

							# If the language "Re-watching" text is inside the episode title, set the "Re-watching" state as True
							if self.language_texts["re_watched, capitalize()"] in entry["Episode title"]:
								states_dictionary["Re-watching"] = True

								# Define the default re-watched dictionary
								self.media["Episode"]["Re-watched"] = {
									"Times": 0,
									"Number name": {},
									"Texts": {
										"Number": {},
										"Number name": {}
									}
								}

								# Get the re-watched times
								self.dictionary["Media"]["Episode"]["Re-watched"]["Times"] = int(entry["Episode title"].split(self.language_texts["re_watched, capitalize()"] + " ")[-1].split("x")[0])

								# Iterate through the list of small languages
								for language in self.languages["small"]:
									# Define the number name
									self.media["Episode"]["Re-watched"]["Number name"][language] = self.Date.texts["number_names_feminine, type: list"][language][watched_times]

									# Define the number re-watched text as the " (Re-watched [watched times]x)" text
									# 
									# Examples:
									# " (Re-watched 1x)"
									# " (Re-watched 2x)"
									self.media["Episode"]["Re-watched"]["Texts"]["Number"][language] = " (" + self.language_texts["re_watched, capitalize()"] + " " + str(self.media["Episode"]["Re-watched"]["Times"]) + "x)"

									# ---------- #

									# Define the text template for the number of watched times
									# (Singular or plural)
									text = self.Text.By_Number(watched_times, self.Language.texts["{}_time"][language], self.Language.texts["{}_times"][language])

									# Format the text template with the name of the number of watched times
									# Examples: one time, two times
									text = text.format(self.media["Episode"]["Re-watched"]["Number name"][language])

									# Define the number name re-watched text as the "Re-watched [watched times]" text
									# 
									# Examples:
									# Re-watched one time
									# Re-watched two times
									self.media["Episode"]["Re-watched"]["Texts"]["Number name"][language] = self.texts["re_watched, capitalize()"][language] + " " + self.media["Episode"]["Re-watched"]["Number name"][language]

							comment_entry = ""

							# Comment file name for non-movies
							if states_dictionary["Series media"] == True:
								add = False

								for alternative_episode_type in self.alternative_episode_types:
									if alternative_episode_type in self.media["Episode"]["Separator"]:
										add = True

								if add == True:
									comment_entry += self.media["Episode"]["Separator"] + " "

								if states_dictionary["Episodic"] == True:
									if "Number text" in self.media["Episode"]:
										comment_entry += self.media["Episode"]["Number text"]

									else:
										comment_entry += str(self.Text.Add_Leading_Zeroes(self.media["Episode"]["Number"]))

								if states_dictionary["Episodic"] == False:
									comment_entry = self.media["Episode"]["Title"]

							# Comment file name for movies or single unit media items
							if states_dictionary["Series media"] == False or states_dictionary["Single unit"] == True:
								comment_entry = self.Language.language_texts["comment, title()"]

							# Add Re-watching text to comment file name if it exists
							if states_dictionary["Re-watching"] == True:
								comment_entry += self.media["Episode"]["Re-watched"]["Texts"]["Number"][self.user_language]

							# If the comment entry name exists inside the media Comments dictionary
							if comment_entry in self.media["Item"]["Comments"]["Entries"]:
								# Get the Comment dictionary from the media Comments dictionary
								entry["Comment"] = self.media["Item"]["Comments"]["Dictionary"][comment_entry]

								# Define the keys to be removed from the "Comment" dictionary
								keys_to_remove = [
									"Entry",
									"Type",
									"Titles",
									"States",
									"Lines"
								]

								if self.media["States"]["Episodic"] == False:
									keys_to_remove.append("Number")

								# Remove not useful keys from "Comment" dictionary
								for key in keys_to_remove:
									if key in entry["Comment"]:
										entry["Comment"].pop(key)

								# Remove Comment dictionary from Entry dictionary if the date is empty and the "ID" key is not inside the Comment dictionary
								# The Comment dictionary is only useful to be inside the Entry dictionary if it contains the date of the comment and/or the ID and Link of the comment
								if entry["Comment"]["Date"] == "" and "ID" not in entry["Comment"]:
									entry.pop("Comment")

								if list(entry["Comment"].keys()) == ["Date"] and entry["Comment"]["Date"] == entry["Date"]:
									entry.pop("Comment")

								# Set the "Commented" state as True
								states_dictionary["Commented"] = True

								# Define the "write" state of the Comment Writer as True
								self.dictionary["Comment Writer"]["States"]["write"] = True

							# If the episode title is the same as the last episode title
							if self.media["Episode"]["Titles"][self.user_language] == self.media["Episode"]["Titles"][self.user_language][-1]:
								# And the plural media type is not "Videos"
								if entry["Type"] != self.texts["videos, title()"]["en"]:
									# Define the "Completed media" state as True
									states_dictionary["Completed media"] = True

								# If the media has a media list
								if self.dictionary["Media"]["States"]["Media item list"] == True:
									# Define the "Completed media item" state as True
									states_dictionary["Completed media item"] = True

							# If the media is non-series media
							if self.media["States"]["Series media"] == False:
								# Define the "Completed media" state as True
								states_dictionary["Completed media"] = True

							states_dictionary["Christmas"] = False

							# If the "25-12" text is inside the UTC time string (25 = day, 12 = month, Christmas day)
							if "25/12" in entry["Date"]["Formats"]["HH:MM DD/MM/YYYY"]:
								# Set the "Christmas" state as True
								states_dictionary["Christmas"] = True

							states_dictionary["First entry in year"] = False

							# If the episode title is the first episode title inside the Episodes list
							if entry["Episode title"] == self.year["Lists"]["Episodes"][0]:
								# Set the "First entry in year" state as True
								states_dictionary["First entry in year"] = True

							states_dictionary["First media type entry in year"] = False

							# If the episode title is the first episode title inside the media type Episodes list
							if entry["Episode title"] == self.year["Lists"][entry["Type"]]["Episodes"][0]:
								# Set the "First media type entry in year" state as True
								states_dictionary["First media type entry in year"] = True

							# Add Entry dictionary to root dictionary
							self.dictionary.update({
								"Entry": {
									"Date": entry["Date"]
								}
							})

							if self.dictionary["Entry"]["Date"] == "Unknown Watched Time - Horário Assistido Desconhecido":
								self.dictionary["Entry"]["Date"] = {}

							# Add Comment dictionary to "Comment Writer" dictionary
							if "Comment" in entry:
								self.dictionary["Comment Writer"]["Comment"] = entry["Comment"]

							# Add the "Old history" dictionary to add the year folder
							self.dictionary["Old history"].update({
								"Episode title": self.media["Episode"]["Titles"][self.user_language]
							})

							if "re_watched" in self.dictionary["Media"]["Episode"]:
								self.dictionary["Old history"]["re_watched"] = self.dictionary["Media"]["Episode"]["Re-watched"]

							for dictionary_name in ["Entries", "Media type"]:
								self.dictionaries[dictionary_name] = self.old_history[dictionary_name]

							# Run the "Watch_Media" class to define more media variables
							self.dictionary = self.Watch_Media(self.dictionary, open_media = False).media_dictionary

							self.media = self.dictionary["Media"]

							self.media["States"] = states_dictionary
							self.dictionary["Media"]["States"] = states_dictionary

							self.media["States"]["Finished watching"] = True

							self.media["States"]["Replace title"] = False

							# Keep the original switches inside the "Switches.json" file before running the "Register" class
							self.Global_Switches.Switch(switches_dictionary)

							# Run the "Register" class to register the media unit
							register_dictionaries = self.Register(self.dictionary).dictionaries

							for dictionary_name in ["Entries", "Media type"]:
								self.old_history[dictionary_name] = register_dictionaries[dictionary_name]

							if progress_text[-1] == "\n":
								progress_text = progress_text[:-1]

							print()
							print(progress_text)

							if entry["Episode title"] != self.year["Lists"]["Episodes"][-1] and self.switches["Testing"] == True:
								self.Input.Type(self.Language.language_texts["continue, title()"] + " (" + self.Language.language_texts["next, feminine"].title() + " " + self.Language.language_texts["entry"] + ")")

							print()

						else:
							print("\t" + "[" + entry["Episode title"] + "]")
							print()
							print("\t" + self.language_texts["the_media_is_not_inside_the_media_info_database"] + ".")
							print()
							quit("----------")

					e += 1

				# Delete the history files
				for file_name in ["Episodes", "Media Types", "Number", "Times", "YouTube IDs"]:
					key = file_name.lower().replace(" ", "_")

					# Delete the entry file
					self.File.Delete(self.year["Folders"][key])

				# Delete the "Per Media Type" folders
				for folder_name in ["Files", "Folders"]:
					folder = self.year["Folders"]["per_media_type"]["root"] + folder_name + "/"
					self.Folder.Delete(folder)

			from Watch_History.Watch_History import Watch_History as Watch_History

			self.old_history = {
				"Current year": self.Years.years["Dictionary"][self.year["Number"]],
				"Folders": self.year["Folders"],
				"old_history": {
					"Number": self.year["Number"]
				},
				"Entries": self.dictionaries["Entries"],
				"Media Type": self.dictionaries["Media type"],
				"Change year": True
			}

			# Add the keys and values of the dictionary to the pre-baked "Watch_History" class
			for key, value in self.old_history.items():
				setattr(Watch_History, key, value)

			Watch_History = Watch_History()

			if "Episodes" in self.year["Lists"] and self.year["Number"] != list(self.years_list)[-1]:
				self.Input.Type(self.Language.language_texts["continue, title()"] + " (" + self.Language.language_texts["next, masculine"].title() + " " + self.Date.language_texts["year, title()"] + ")")

		# Update the "History.json" file with the updated "History" dictionary
		self.JSON.Edit(self.folders["Watch History"]["History"], self.dictionaries["History"])

	def Fix_Comment_Dictionaries(self):
		# Fix Comment dictionaries that exist on the "Comments.json" file of media
		# But they do not exist on the Entry of the "Watch History" folder, in the "Entries.json" file

		from copy import deepcopy

		# Copy the switches dictionary
		switches_dictionary = deepcopy(self.switches)

		# Get the History dictionary to update the entries number
		self.dictionaries["History"] = self.JSON.To_Python(self.folders["Watch History"]["History"])

		self.years_list = range(2018, self.date["Units"]["Year"] + 1)

		self.medias = {}

		# Iterate through the years list (of the years that contain a "Watch_History" folder)
		for self.year in self.years_list:
			# Convert the year number into a string
			self.year = str(self.year)

			# Define the year dictionary with the year number and folders
			self.year = {
				"Number": self.year,
				"Folders": {
					"root": self.folders["Watch History"]["root"] + self.year + "/"
				},
				"Entries": deepcopy(self.template),
				"Media type entries": {}
			}

			print()
			print("----------")
			print()
			print(self.Date.language_texts["year, title()"] + ": " + self.year["Number"])

			# Define the history folders
			for folder_name in ["Per Media Type"]:
				key = folder_name.lower().replace(" ", "_")

				# Define the folder
				self.year["Folders"][key] = {
					"root": self.year["Folders"]["root"] + folder_name + "/"
				}

				self.Folder.Create(self.year["Folders"][key]["root"])

			# Define the "Files" folder inside the "Per Media Type"
			self.year["Folders"]["per_media_type"]["files"] = {
				"root": self.year["Folders"]["per_media_type"]["root"] + "Files/"
			}

			# Define and create the "Entries.json" file
			self.year["Folders"]["entries"] = self.year["Folders"]["root"] + "Entries.json"
			self.File.Create(self.year["Folders"]["entries"])

			# Define the Per Media Type files and folders
			for plural_media_type in self.media_types["Plural"]["en"]:
				key = plural_media_type.lower().replace(" ", "_")

				# Create the media type folder
				self.year["Folders"]["per_media_type"][key] = {
					"root": self.year["Folders"]["per_media_type"]["root"] + plural_media_type + "/"
				}

				self.Folder.Create(self.year["Folders"]["per_media_type"][key]["root"])

				# Define and create the media type "Entries.json" file
				self.year["Folders"]["per_media_type"][key]["entries"] = self.year["Folders"]["per_media_type"][key]["root"] + "Entries.json"
				self.File.Create(self.year["Folders"]["per_media_type"][key]["entries"])

				self.year["Media type entries"][plural_media_type] = self.JSON.To_Python(self.year["Folders"]["per_media_type"][key]["entries"])

			# Get the Entries dictionary
			self.year["Entries"] = self.JSON.To_Python(self.year["Folders"]["entries"])

			# Iterate through the Entries dictionary
			e = 0
			for entry_key, entry in self.year["Entries"]["Dictionary"].items():
				# If the "States" key is inside the Entry dictionary
				# And the "Commented" key is inside the States dictionary
				# And the "Commented" state is True
				if (
					"States" in entry and
					"Commented" in entry["States"] and
					entry["States"]["Commented"] == True
				):
					# Make a backup of the Entry dictionary to differentiate later
					entry_backup = deepcopy(entry)

					# Show the current and total entry number
					print()
					print(self.separators["5"])
					print()
					print(str(e + 1) + "/" + str(len(self.year["Entries"]["Dictionary"].keys())) + ":")

					# Show the Entry name
					print()
					print(self.Language.language_texts["entry, title()"] + ":")
					print("[" + entry["Entry"] + "]")
					print("[" + entry["Date"] + "]")
					print()

					self.media_title = entry["Media"]["Original"]

					if "Romanized" in entry["Media"]:
						self.media_title = entry["Media"]["Romanized"]

					# Show the media title
					print(self.Language.language_texts["media, title()"] + ":")
					print("[" + self.media_title + "]")

					if (
						self.user_language in entry["Media"] and
						entry["Media"][self.user_language] != self.media_title
					):
						print("[" + entry["Media"][self.user_language] + "]")

					# If there is a Episode, show its title in the user language
					if "Episode" in entry:
						print()
						print(self.Language.language_texts["episode, title()"] + ":")
						print("[" + entry["Episode"]["Titles"][self.user_language] + "]")

					# If there is a media Item, show its original title
					if "Item" in entry:
						print()
						print(self.Language.language_texts["item, title()"] + ":")
						print("[" + entry["Item"]["Original"] + "]")

						if (
							self.user_language in entry["Item"] and
							entry["Item"][self.user_language] != entry["Item"]["Original"]
						):
							print("[" + entry["Item"][self.user_language] + "]")

					if self.media_title not in self.medias:
						# Define the root dictionary with the media type and media
						self.medias[self.media_title] = {
							"Media type": self.media_types[entry["Type"]],
							"Media": {
								"Title": self.media_title
							}
						}

						# Select the media and define its variables, returning the media dictionary (without asking the user to select the media)
						self.medias[self.media_title] = self.Select_Media(self.medias[self.media_title])

						# Define the media item if it exists
						media_item = None

						if "Item" in entry:
							media_item = entry["Item"]["Original"]

						if (
							"Item" not in entry and
							"Items" in self.medias[self.media_title]
						):
							media_item = self.media_title

						# Update the root dictionary with the defined media item
						self.medias[self.media_title].update(self.Define_Media_Item(deepcopy(self.medias[self.media_title]), media_item = media_item))

						if "Watched" not in self.medias[self.media_title]:
							# Create the Watched dictionary
							self.medias[self.media_title]["Watched"] = {
								"Entries file": self.medias[self.media_title]["Media"]["Item"]["Folders"]["Watched"]["entries"]
							}

					# Define the media variable for easier typing
					self.media = self.medias[self.media_title]["Media"]

					print()
					print("Arquivo de Assistido:")
					print("[" + self.medias[self.media_title]["Watched"]["Entries file"] + "]")

					# Get the Watched Entries dictionary
					self.medias[self.media_title]["Watched"]["Entries"] = self.JSON.To_Python(self.medias[self.media_title]["Watched"]["Entries file"])

					# Read the "Comments.json" file to get the Comments dictionary
					self.comments = self.JSON.To_Python(self.medias[self.media_title]["Media"]["Item"]["Folders"]["comments"]["comments"])

					# Show the "Comments" header
					print()
					print(self.Language.language_texts["comments, title()"] + ":")

					found_comment = False

					found_comments = []

					# Iterate through the comments list
					c = 0
					for comment in self.comments["Entries"]:
						comment = self.comments["Dictionary"][comment]

						if found_comment == False:
							if c != 0:
								print()
								print("\t" + "---")
								print()

							# Show some Comment entry information
							print("\t" + "[" + str(c + 1) + "/" + str(len(self.comments["Entries"])) + "]:")
							print()
							print("\t" + self.Language.language_texts["entry, title()"] + ":")
							print("\t" + "[" + comment["Entry"] + "]")

							if comment["Titles"][self.user_language] != comment["Entry"]:
								print()
								print("\t" + self.Language.language_texts["title, title()"] + ":")
								print("\t" + "[" + comment["Titles"][self.user_language] + "]")

							print()
							print("\t" + self.Date.language_texts["date, title()"] + ":")
							print("\t" + "[" + comment["Date"] + "]")

						# Create the empty titles list
						titles_list = []

						# If there is a media title in the user language, add it to the titles list
						if self.user_language in entry["Media"]:
							titles_list.append(entry["Media"])

						# If there is an episode in the Entry dictionary, add it to the titles list
						if "Episode" in entry:
							titles_list.append(entry["Episode"]["Titles"])

						# If there is an episode in the Entry dictionary, add it to the titles list
						if "Item" in entry:
							titles_list.append(entry["Item"])

						# If the media unit has been re-watched
						if "Re-watched" in entry["States"]:
							# Get the re-watched times
							times = entry["States"]["Re-watched"]["Times"]

							# Define the re-watched text
							re_watched_text = self.language_texts["re_watched, capitalize()"] + " " + str(times) + "x"

							re_watched = True

							# Define the evaluation of "the re-watched text is in the Comment entry"
							# The re-watched text with re-watched times number needs to be in the Comment entry
							# The re-watched times number is included to differentiate between various re-watched comments
							re_watched_check = re_watched_text in comment["Entry"]

							print()
							print("\t" + self.language_texts["re_watched, capitalize()"] + ":")
							print("\t\t" + re_watched_text)
							print("\t\t" + comment["Entry"])
							print("\t\t" + str(re_watched))
							print("\t\t" + str(re_watched_check))

						# If the media unit has not been re-watched
						if "Re-watched" not in entry["States"]:
							re_watched = False

							# Define the evaluation of "the re-watched text is not in the Comment entry"
							# The re-watched text can not be in the Comment entry
							# The re-watched times number is excluded because no re-watched comment must be selected
							re_watched_check = self.language_texts["re_watched, capitalize()"] not in comment["Entry"]

						comment_copy = deepcopy(comment)

						# Iterate through the titles list
						for titles in titles_list:
							# If the re-watched check is correct
							if re_watched_check:
								# If the comment language title is equal to the media original title
								# Or the comment language title is equal to the media language title
								# Or the comment language title is equal to the media original title
								if (
									"Original" in titles and
									comment_copy["Titles"][self.user_language] == titles["Original"] or
									self.user_language in titles and
									comment_copy["Titles"][self.user_language] == titles[self.user_language]
								):
									# Define a list of keys to remove from the Comment dictionary
									keys_to_remove = [
										"Type",
										"Titles",
										"States",
										"Lines"
									]

									# If the media is non-episodic, add the "Number" key to be removed from the Comment dictionary
									if self.media["States"]["Episodic"] == False:
										keys_to_remove.append("Number")

										if (
											"Episode" in entry and
											comment_copy["Titles"][self.user_language] == entry["Episode"]["Titles"][self.user_language]
										):
											keys_to_remove.append("Entry")

									# Remove the not useful keys from the "Comment" dictionary
									for key in keys_to_remove:
										if key in comment:
											comment.pop(key)

									# Define the Entry Comment dictionary keys list
									keys = list(comment.keys())

									comment_backup = deepcopy(comment)

									# If the comment date is the same as the entry date
									if comment["Date"] == entry["Date"]:
										# Remove the "Date" key from the Comment dictionary
										comment.pop("Date")

										# Update the keys list
										keys = list(comment.keys())

										# If the only key left inside the Comment dictionary is "Dates"
										if keys == ["Dates"]:
											# Remove the Comment dictionary from the Entry dictionary
											entry.pop("Comment")

									# If the Comment dictionary does not contain only the "Entry" key
									if keys != ["Entry"]:
										# Add it to the Entry dictionary, after the "Date" key
										key_value = {
											"key": "Comment",
											"value": comment
										}

										entry = self.JSON.Add_Key_After_Key(entry, key_value, after_key = "Date")

									entry["Comment"] = comment

									# If the only key left inside the Comment dictionary is "Entry"
									if keys == ["Entry"]:
										# Remove the Comment dictionary from the Entry dictionary
										entry.pop("Comment")

									# If the entry backup is not the same as the entry, show it
									if entry_backup != entry:
										print()
										self.JSON.Show(entry)

										print()
										print(self.separators["5"])

										# If the keys list does not contain only the "Entry" key
										if keys != ["Entry"]:
											# Show the "Updated: The entry and comment dates are different. Updating comment."
											print()
											print("Atualizado:")

											if comment_backup["Date"] != entry["Date"]:
												print("As datas da entrada e do comentário são diferentes.")

											if comment_backup["Date"] == entry["Date"]:
												print("As datas da entrada e do comentário são iguais.")
												print('Removendo a chave "Date".')

											if self.media["States"]["Episodic"] == False:
												print('Removendo a chave "Number" pois a mídia é não-episódica.')

												if (
													"Episode" in entry and
													comment_copy["Titles"][self.user_language] == entry["Episode"]["Titles"][self.user_language]
												):
													print('Removendo a chave "Entry" pois ela tem o mesmo valor que o título do episódio.')

											print()
											print('Atualizando o dicionário "Comment" na Entrada.')

										# If the comment date is the same as the entry date
										if (
											entry_backup == entry and
											comment_backup["Date"] == entry["Date"]
										):
											# Show the "Skipped: The entry and comment dates are equal" text
											print()
											print("Pulado:")
											print("As datas da entrada e do comentário são iguais.")

										# If the only key left inside the Comment dictionary is "Dates"
										if keys == ["Dates"]:
											# Show the "Skipped: The only key left is 'Dates'" text
											print()
											print('Só sobrou a chave "' + keys[0] + '".')

										# If the only key left inside the Comment dictionary is "Entry"
										if keys == ["Entry"]:
											# Show the "Skipped: The only key left is 'Entry'" text
											print()
											print("Pulado:")
											print('Só sobrou a chave "' + keys[0] + '".')

										if (
											comment_backup["Date"] == entry["Date"] and
											"Comment" not in entry or
											keys == ["Entry"]
										):
											print()
											print('Removendo o dicionário "Comment" do dicionário da Entrada.')

										print()
										print(self.separators["5"])

									if entry_backup != entry:
										found_comments.append("Comment")

									found_comment = True		

						c += 1

					if (
						found_comment == False and
						found_comments != []
					):
						print()
						print("Aviso:")
						print("Comentário não encontrado.")
						input()
						print(self.separators["5"])

					if found_comments == []:
						print()
						print(self.separators["5"])
						print()
						print("Pulado:")
						print("O dicionário de Entrada original e editado são iguais, nada a ser alterado.")
						print("Os dados do comentário estão corretos.")
						print()
						print(self.separators["5"])

					# Show "Continue" text on testing mode to pause between entries
					if self.switches["Testing"] == True:
						self.Input.Type(self.Language.language_texts["continue, title()"])

					# Define the list of dictionaries to update the Entry dictionary
					dicts = [
						self.year["Entries"],
						self.year["Media type entries"][entry["Type"]],
						self.medias[self.media_title]["Watched"]["Entries"]
					]

					# Update the Entry dictionary in the dictionaries above
					for dict_ in dicts:
						dict_["Dictionary"][entry_key] = entry

					# Update the "Watched.json" file with the updated "Watched" dictionary
					self.JSON.Edit(self.medias[self.media_title]["Watched"]["Entries file"], self.medias[self.media_title]["Watched"]["Entries"])

					e += 1

			# Update the year "Entries.json" file with the updated year "Entries" dictionary
			self.JSON.Edit(self.year["Folders"]["entries"], self.year["Entries"])

			# Update the Per Media Type files
			for plural_media_type in self.media_types["Plural"]["en"]:
				key = plural_media_type.lower().replace(" ", "_")

				# Update the Per Media Type "Entries.json" file with the updated media type "Entries" dictionary
				self.JSON.Edit(self.year["Folders"]["per_media_type"][key]["entries"], self.year["Media type entries"][plural_media_type])

	def Replace_Year_Number(self, folders, to_replace, replace_with):
		for key, value in folders.items():
			value = folders[key]

			if type(value) == str:
				folders[key] = folders[key].replace(to_replace, replace_with)

			if type(value) == dict:
				self.Replace_Year_Number(value, to_replace, replace_with)