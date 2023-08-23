# Convert_History.py

from Watch_History.Watch_History import Watch_History as Watch_History

class Convert_History(Watch_History):
	def __init__(self):
		super().__init__()

		self.Per_Media()
		#self.By_File()
		#self.By_Year()

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
			"Entries file": self.dictionary["Media"]["Item"]["folders"]["watched"]["entries"],
			"Entries": self.JSON.To_Python(self.dictionary["Media"]["Item"]["folders"]["watched"]["entries"]),
			"Entry list": self.File.Contents(self.dictionary["Media"]["Item"]["folders"]["watched"]["entry_list"])["lines"],
			"Files": self.dictionary["Media"]["Item"]["folders"]["watched"]["files"],
			"Correct titles file": self.dictionary["Media"]["Item"]["folders"]["watched"]["root"] + "Correct titles.txt"
		}

		self.watched["Correct titles"] = self.File.Contents(self.watched["Correct titles file"])["lines"]

		# Create the "Correct titles.txt" file
		self.File.Create(self.watched["Correct titles file"])

		if self.watched["Correct titles"] == []:
			titles_list = []

			for entry in self.watched["Entries"]["Dictionary"].values():
				titles_list.append(entry["Episode"]["Titles"][self.media["Language"]])

			self.File.Edit(self.watched["Correct titles file"], self.Text.From_List(titles_list), "a")

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

			new_title = self.Input.Type(self.JSON.Language.language_texts["title, title()"], next_line = True)

			if new_title != "":
				self.watched["Correct titles"][i] = new_title

				self.File.Edit(self.watched["Correct titles file"], self.Text.From_List(self.watched["Correct titles"]), "w")

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
					"Entries file": self.folders["watch_history"][year]["entries"],
					"Entries": "",
					"Media type Entries file": self.folders["watch_history"][year]["per_media_type"][media_type_key]["entries"],
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
					"current_year": self.Years.years[year]
				}

				# Update the episode title in the year Entry file
				per_media_type_folder = self.folders["watch_history"][year]["per_media_type"][media_type_key]["files"]["root"]
				year_entry_file = per_media_type_folder + self.dictionary["Entry"]["Name"]["Sanitized"] + ".txt"

				# Get the Entry file lines
				lines = self.File.Contents(year_entry_file)["lines"]

				# Update the episode titles lines inside the Entry file
				lines[10] = titles[self.media["Language"]]
				lines[11] = titles["en"]

				# Update the year Entry file
				self.File.Edit(year_entry_file, self.Text.From_List(lines), "w")

				# Iterate through the small languages list
				for language in self.languages["small"]:
					full_language = self.languages["full"][language]

					# Get the root and type folder
					root_folder = self.texts["watched_media"][language]
					type_folder = self.dictionary["Media type"]["Plural"][language]

					# Get the type folder inside the root folder which is inside the year language folder
					folder = self.dictionary["Entry"]["current_year"]["folders"][full_language][root_folder][type_folder]["root"]
					file_name = self.dictionary["Entry"]["Name"]["Sanitized"]

					# Get the year Entry file per language
					file = folder + file_name + ".txt"

					# Get the file and update the episode title inside it
					lines = self.File.Contents(file)["lines"]
					lines[10] = titles[language]

					# Update the year Entry file per language
					self.File.Edit(file, self.Text.From_List(lines), "w")

				# Update the episode title in the Watched Entry file
				watched_entry_file = self.watched["Files"]["root"] + watched_entry["Entry"].replace(":", ";").replace("/", "-") + ".txt"

				# Get the Entry file lines
				lines = self.File.Contents(watched_entry_file)["lines"]

				# Update the episode titles lines inside the Entry file
				lines[10] = titles[self.media["Language"]]

				# Update the Watched Entry file
				self.File.Edit(watched_entry_file, self.Text.From_List(lines), "w")

				# --- #

				# Update the year "Entries.json" file
				self.JSON.Edit(year_dictionary[year]["Entries file"], year_dictionary[year]["Entries"])

				# Update the year media type "Entries.json" file
				self.JSON.Edit(year_dictionary[year]["Media type Entries file"], year_dictionary[year]["Media type Entries"])

				# Update the Watched "Entries.json" file
				self.JSON.Edit(self.watched["Entries file"], self.watched["Entries"])

				print()

				print(self.JSON.Language.language_texts["entry, title()"] + ":")
				print("[" + year_entry["Entry"] + "]")
				print()

				print(self.JSON.Language.language_texts["line, title()"] + ":")
				print("[" + str(i + 1) + "]")
				print()

				print(self.JSON.Language.language_texts["wrong, title()"] + ":")
				print("[" + wrong_title + "]")
				print()

				print(self.JSON.Language.language_texts["right, title()"] + ":")
				print("[" + correct_title + "]")

				if self.switches["testing"] == True:
					self.Input.Type(self.JSON.Language.language_texts["continue, title()"])

				print()
				print("-----")

			i += 1

		# Get the Comments dictionary
		self.comments = {
			"Comments": self.JSON.To_Python(self.dictionary["Media"]["Item"]["folders"]["comments"]["comments"])
		}

	def By_File(self):
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
		self.dictionaries["History"] = self.JSON.To_Python(self.folders["watch_history"]["history"])

		self.year = str(self.date["Units"]["Year"])

		# Define the year dictionary with the year number and folders
		self.year = {
			"Number": self.year,
			"folders": {
				"root": self.folders["watch_history"]["root"] + self.year + "/"
			},
			"Entries": self.dictionaries["Entries"]
		}

		# Define the "Pre-entries.json" file
		self.year["folders"]["pre_entries"] = self.year["folders"]["root"] + "Pre-entries.json"

		# Read the "Pre-entries.json" file
		self.year["Pre-entries"] = self.JSON.To_Python(self.year["folders"]["pre_entries"])

		pre_entries_list = list(self.year["Pre-entries"].values())
		last_pre_entry = pre_entries_list[-1]

		# Iterate through the Entries list
		e = 0
		for entry in pre_entries_list:
			if entry["Title"] == last_pre_entry["Title"]:
				print()

			# Define the progress text with progress (current number and entries number)
			# Media type, entry date and name
			progress_text = "-----" + "\n" + \
			"\n" + \
			str(e + 1) + "/" + str(len(pre_entries_list)) + ":" + "\n" + "\n" + \
			self.JSON.Language.language_texts["type, title()"] + ":" + "\n" + \
			"[" + entry["Type"] + "]" + "\n" + \
			"\n" + \
			self.Date.language_texts["date, title()"] + ":" + "\n" + \
			"[" + entry["Date"] + "]" + "\n" + \
			"\n" + \
			self.JSON.Language.language_texts["title, title()"] + ":" + "\n" + \
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
			print(self.JSON.Language.language_texts["media, title()"] + ":")
			print("[" + self.media["Title"] + "]")

			# Define the media item dictionary
			if "Item" in entry:
				self.dictionary.update(self.Define_Media_Item(deepcopy(self.dictionary), media_item = entry["Item"]))

			# Define the media dictionary to speed up typing
			self.media = self.dictionary["Media"]

			# Show the media item title
			if self.media["Item"]["Title"] != self.media["Title"]:
				text = "[" + self.media["Item"]["Title"] + "]"

				progress_text += "\n" + self.JSON.Language.language_texts["item"].title() + ":" + "\n" + \
				text + "\n"

				print()
				print(self.JSON.Language.language_texts["item"].title() + ":")
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
			if states_dictionary["Series media"] == False or states_dictionary["Single unit"] == True:
				comment_entry = self.JSON.Language.language_texts["comment, title()"]

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

				# Remove Comment dictionary from Entry dictionary if the date is empty and the "ID" key is not inside the Comment dictionary
				# The Comment dictionary is only useful to be inside the Entry dictionary if it contains the date of the comment and/or the ID and Link of the comment
				if (
					entry["Comment"]["Date"] == "" and "ID" not in entry["Comment"] or \
					list(entry["Comment"].keys()) == ["Date"] and entry["Comment"]["Date"] == entry["Date"]
				):
					entry.pop("Comment")
					self.dictionary["Comment Writer"].pop("Comment")

				# Set the "Commented" state as True
				states_dictionary["Commented"] = True

			self.media["States"] = states_dictionary
			self.dictionary["Media"]["States"] = states_dictionary

			# Keep the original switches inside the "Switches.json" file before running the "Register" class
			self.Global_Switches.Switch(switches_dictionary)

			setattr(self.Register, "dictionaries", self.dictionaries)
			setattr(self.Register, "self.dictionaries", self.dictionaries)

			# Run the "Register" class to register the media unit
			register = self.Register(self.dictionary)

			self.dictionaries = getattr(register, "dictionaries")

			if progress_text[-1] == "\n":
				progress_text = progress_text[:-1]

			print()
			print(progress_text)

			if entry["Title"] != last_pre_entry["Title"] and self.switches["testing"] == True:
				self.Input.Type(self.JSON.Language.language_texts["continue, title()"] + " (" + self.JSON.Language.language_texts["next, feminine"].title() + " " + self.JSON.Language.language_texts["entry"] + ")")

				print()

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
		self.dictionaries["History"] = self.JSON.To_Python(self.folders["watch_history"]["history"])

		self.years_list = range(2018, self.date["Units"]["Year"] + 1)

		# Iterate through the years list (of the years that contain a "Watch_History" folder)
		for self.year in self.years_list:
			# Convert the year number into a string
			self.year = str(self.year)

			# Define the year dictionary with the year number and folders
			self.year = {
				"Number": self.year,
				"folders": {
					"root": self.folders["watch_history"]["root"] + self.year + "/"
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
				self.year["folders"][key] = {
					"root": self.year["folders"]["root"] + folder_name + "/"
				}

				self.Folder.Create(self.year["folders"][key]["root"])

			# Define the "Files" folder inside the "Per Media Type"
			self.year["folders"]["per_media_type"]["files"] = {
				"root": self.year["folders"]["per_media_type"]["root"] + "Files/"
			}

			exist = False

			# Define and create the "Entries.json" file
			self.year["folders"]["entries"] = self.year["folders"]["root"] + "Entries.json"

			if self.File.Exist(self.year["folders"]["entries"]) == True:
				exist = True

			self.File.Create(self.year["folders"]["entries"])

			# Define and create the "Entry list.txt" file
			self.year["folders"]["entry_list"] = self.year["folders"]["root"] + "Entry list.txt"
			self.File.Create(self.year["folders"]["entry_list"])

			# Define the per media type "Files" folders
			for plural_media_type in self.media_types["Plural"]["en"]:
				key = plural_media_type.lower().replace(" ", "_")

				# Create the media type folder
				self.year["folders"]["per_media_type"][key] = {
					"root": self.year["folders"]["per_media_type"]["root"] + plural_media_type + "/"
				}

				self.Folder.Create(self.year["folders"]["per_media_type"][key]["root"])

				# Create the "Files" media type folder
				self.year["folders"]["per_media_type"][key]["files"] = {
					"root": self.year["folders"]["per_media_type"][key]["root"] + "Files/"
				}

				self.Folder.Create(self.year["folders"]["per_media_type"][key]["files"]["root"])

				# Define and create the media type "Entries.json" file
				self.year["folders"]["per_media_type"][key]["entries"] = self.year["folders"]["per_media_type"][key]["root"] + "Entries.json"
				self.File.Create(self.year["folders"]["per_media_type"][key]["entries"])

				# Define and create the media type "Entry list.txt" file
				self.year["folders"]["per_media_type"][key]["entry_list"] = self.year["folders"]["per_media_type"][key]["root"] + "Entry list.txt"
				self.File.Create(self.year["folders"]["per_media_type"][key]["entry_list"])

				# Define the media type "Files" folder
				self.year["folders"]["per_media_type"]["files"][key] = {
					"root": self.year["folders"]["per_media_type"]["files"]["root"] + plural_media_type + "/"
				}

				# Define the media type "Episodes" file
				self.year["folders"]["per_media_type"]["files"][key]["episodes"] = self.year["folders"]["per_media_type"]["files"][key]["root"] + "Episodes.txt"

				if self.Folder.Exist(self.year["folders"]["per_media_type"]["files"][key]["root"]) == True:
					# Create media type lists dictionary and read "Episodes" file
					self.year["Lists"][plural_media_type] = {
						"Episodes": self.File.Contents(self.year["folders"]["per_media_type"]["files"][key]["episodes"])["lines"]
					}

			# Define the entry files
			for file_name in ["Episodes", "Media Types", "Number", "Times", "YouTube IDs"]:
				key = file_name.lower().replace(" ", "_")

				# Define the entry file
				self.year["folders"][key] = self.year["folders"]["root"] + file_name + ".txt"

				if self.File.Exist(self.year["folders"][key]) == True:
					# Get the list of lines inside the file
					self.year["Lists"][file_name] = self.File.Contents(self.year["folders"][key])["lines"]

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

				remove_list = self.File.Contents(self.Folder.folders["apps"]["root"] + "Test.txt")["lines"]

				self.old_history = {
					"current_year": self.Years.years[self.year["Number"]],
					"folders": self.year["folders"],
					"old_history": {
						"Number": self.year["Number"]
					},
					"Entries": self.dictionaries["Entries"],
					"Media type": self.dictionaries["Media type"],
					"Change year": True
				}

				# If the "Entries.json" is not empty and has entries, get Entries dictionary from it
				if self.File.Contents(self.year["folders"]["entries"])["lines"] != [] and self.JSON.To_Python(self.year["folders"]["entries"])["Entries"] != []:
					self.dictionaries["Entries"] = self.JSON.To_Python(self.year["folders"]["entries"])

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
					self.JSON.Language.language_texts["type, title()"] + ":" + "\n" + \
					"[" + entry["Type"] + "]" + "\n" + \
					"\n" + \
					self.Date.language_texts["date, title()"] + ":" + "\n" + \
					"[" + entry["Date"] + "]" + "\n" + \
					"\n" + \
					self.JSON.Language.language_texts["entry, title()"] + ":" + "\n" + \
					"[" + entry["Episode title"] + "]" + "\n"

					# Show the progress text
					print(progress_text)

					# Define default media dictionary
					self.dictionary = {}

					# If testing is True and the episode title is not inside the remove list
					# Or testing is False and the remove list is empty
					if (
						self.switches["testing"] == True and entry["Episode title"] not in remove_list or
						self.switches["testing"] == False and remove_list == []
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

									self.Replace_Year_Number(self.dictionary["Media type"]["Folders"]["per_media_type"], str(self.date["Units"]["Year"]), self.year["Number"])

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

								progress_text += "\n" + self.JSON.Language.language_texts["item"].title() + ":" + "\n" + \
								text.replace(tab, "") + "\n"

								print()
								print(text)

							# If the media is series media
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
												self.File.Edit(self.media["Item"]["Episodes"]["Titles"]["Files"][language], self.Text.From_List(self.media["Item"]["Episodes"]["Titles"][language]), "w")

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
							if self.JSON.Language.language_texts["dubbed, title()"] in entry["Episode title"]:
								states_dictionary["Watch dubbed"] = True

							# If the language "Re-watching" text is inside the episode title, set the "Re-watching" state as True
							if self.language_texts["re_watched, capitalize()"] in entry["Episode title"]:
								states_dictionary["Re-watching"] = True

								self.media["Episode"]["re_watched"] = {
									"times": 0,
									"text": "",
									"re_watched_text": {},
									"time_text": {}
								}

								# Get re-watched times
								self.dictionary["Media"]["Episode"]["re_watched"]["times"] = int(entry["Episode title"].split(self.language_texts["re_watched, capitalize()"] + " ")[-1].split("x")[0])

								self.media["Episode"]["re_watched"]["text"] = " (" + self.language_texts["re_watched, capitalize()"] + " " + str(self.media["Episode"]["re_watched"]["times"]) + "x)"

								number = self.media["Episode"]["re_watched"]["times"]

								for language in self.languages["small"]:
									text = self.Text.By_Number(number, self.JSON.Language.texts["{}_time"][language], self.JSON.Language.texts["{}_times"][language])

									self.media["Episode"]["re_watched"]["time_text"][language] = text.format(self.Date.texts["number_names_feminine, type: list"][language][number])

									self.media["Episode"]["re_watched"]["re_watched_text"][language] = self.texts["re_watched, capitalize()"][language] + " " + self.media["Episode"]["re_watched"]["time_text"][language]

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
								comment_entry = self.JSON.Language.language_texts["comment, title()"]

							# Add Re-watching text to comment file name if it exists
							if states_dictionary["Re-watching"] == True:
								comment_entry += self.media["Episode"]["re_watched"]["text"]

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
								self.dictionary["Old history"]["re_watched"] = self.dictionary["Media"]["Episode"]["re_watched"]

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

							if entry["Episode title"] != self.year["Lists"]["Episodes"][-1] and self.switches["testing"] == True:
								self.Input.Type(self.JSON.Language.language_texts["continue, title()"] + " (" + self.JSON.Language.language_texts["next, feminine"].title() + " " + self.JSON.Language.language_texts["entry"] + ")")

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
					self.File.Delete(self.year["folders"][key])

				# Delete the "Per Media Type" folders
				for folder_name in ["Files", "Folders"]:
					folder = self.year["folders"]["per_media_type"]["root"] + folder_name + "/"
					self.Folder.Delete(folder)

			from Watch_History.Watch_History import Watch_History as Watch_History

			self.old_history = {
				"current_year": self.Years.years[self.year["Number"]],
				"folders": self.year["folders"],
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
				self.Input.Type(self.JSON.Language.language_texts["continue, title()"] + " (" + self.JSON.Language.language_texts["next, masculine"].title() + " " + self.Date.language_texts["year, title()"] + ")")

		# Update the "History.json" file with the new History dictionary
		self.JSON.Edit(self.folders["watch_history"]["history"], self.dictionaries["History"])

	def Replace_Year_Number(self, folders, to_replace, replace_with):
		for key, value in folders.items():
			value = folders[key]

			if type(value) == str:
				folders[key] = folders[key].replace(to_replace, replace_with)

			if type(value) == dict:
				self.Replace_Year_Number(value, to_replace, replace_with)