# Iterate_Through_The_Media_List.py

from Watch_History.Watch_History import Watch_History as Watch_History

class Iterate_Through_The_Media_List(Watch_History):
	def __init__(self):
		super().__init__()

		# Iterate through the list of medias
		self.Iterate()

	def Iterate(self):
		# Define default comments number dictionary
		self.comments_number = {
			"Numbers": {
				"Total": 0,
				"No time": 0,
				"Years": {},
				"Type": {}
			}
		}

		# Add missing year numbers
		for year in range(2018, self.date["Units"]["Year"] + 1):
			if str(year) not in self.comments_number["Numbers"]["Years"]:
				# If the year of the entry is not inside the comment numbers by year, add it
				self.comments_number["Numbers"]["Years"][str(year)] = 0

				for plural_media_type in self.media_types["Plural"]["en"]:
					if plural_media_type not in self.comments_number["Numbers"]["Type"]:
						self.comments_number["Numbers"]["Type"][plural_media_type] = {
							"Total": 0,
							"No time": 0,
							"Years": {}
						}

					# If the year of the entry is not inside the comment numbers by type and by year, add it
					if str(year) not in self.comments_number["Numbers"]["Type"][plural_media_type]["Years"]:
						self.comments_number["Numbers"]["Type"][plural_media_type]["Years"][str(year)] = 0

		# Iterate through English plural media types list
		i = 0
		for plural_media_type in self.media_types["Plural"]["en"]:
			# Define the key of the media type for getting media type folders
			key = plural_media_type.lower().replace(" ", "_")

			# Define the language media type
			language_media_type = self.media_types["Plural"][self.language["Small"]][i]

			# Get media with all "watching statuses", not just the "Watching" and "Re-watching" ones
			media_list = self.Get_Media_List(self.media_types[plural_media_type], self.texts["statuses, type: list"]["en"])

			# Sort the media item list as case insensitive
			media_list = sorted(media_list, key = str.lower)

			# Show the language media type
			print()
			print("----------")
			print()
			print(language_media_type + ":")

			media_types_to_remove = [
				self.texts["animes, title()"]["en"],
				self.texts["cartoons, title()"]["en"],
				self.texts["series, title()"]["en"],
				self.texts["movies, title()"]["en"],
				#self.texts["videos, title()"]["en"]
			]

			#string = ""
			ask_for_input = True

			# Remove a media type from the list (optional)
			if plural_media_type not in media_types_to_remove:
				# Define the media number
				media_number = 1

				# For media in media item list
				for self.media_title in media_list:
					# Define root dictionary with media type and media
					self.dictionary = {
						"Media type": self.media_types[plural_media_type],
						"Media": {
							"Title": self.media_title
						}
					}

					# Show a three dash space separator
					print()
					print(self.separators["3"])

					# Show the media number
					print()
					print(self.Language.language_texts["number, title()"] + ":")
					print("[" + str(media_number) + "/" + str(len(media_list)) + "]")

					# Show the language media type
					print()
					print(self.language_texts["media_type"])
					print("[" + language_media_type + "]")

					# Show the media title
					print()
					print(self.Language.language_texts["media, title()"] + ":")
					print("[" + self.dictionary["Media"]["Title"] + "]")

					# Select the media and define its variables, returning the media dictionary (without asking user to select the media)
					self.dictionary = self.Select_Media(self.dictionary)

					# Define the "media" variable for easier typing
					self.media = self.dictionary["Media"]

					# Define the media items list as the media title for media without a media item list
					self.media_items_list = [
						self.media["Item"]["Title"]
					]

					# For media with the media item list, get the actual media items
					if self.media["States"]["Has a list of media items"] == True:
						self.media_items_list = self.media["Items"]["List"]

					# Iterate through the media items list
					self.media_item_number = 0

					for self.media_item in self.media_items_list:
						# Define the media item
						self.dictionary = self.Define_Media_Item(self.dictionary, media_item = self.media_item)

						# Define a shortcut for the "Media" dictionary for easier typing
						self.media = self.dictionary["Media"]

						# Show the media item title
						if self.media["Item"]["Title"] != self.media["Title"]:
							print()
							print(self.Language.language_texts["item"].title() + ":")
							print("[" + self.media["Item"]["Title"] + "]")

						# Update the watched files of the media
						#self.Update_Watched_Files()

						# Update the "Comments" JSON dictionary
						#self.Update_Comments_JSON()

						# Update the text of the comment files
						#self.Update_Comment_Files()

						# Verify if there are empty episode titles files
						#self.Check_Episodes_Titles()

						# Add exact media or media item creation or release to media or media item details
						#self.Add_Date()

						# Re-count comments numbers
						#self.Count_Comments_Number()

						# Add anime information to anime details
						#if self.dictionary["Media type"]["Plural"]["en"] == self.texts["animes, title()"]["en"]:
						#	self.Add_Anime_Information()

						# Add media information to media details and media information file
						#self.Add_Media_Information()

						#if self.dictionary["Media type"]["Plural"]["en"] == self.texts["videos, title()"]["en"]:
						#	self.Add_Last_Playlist_Date()

						#if self.dictionary["Media type"]["Plural"]["en"] == self.texts["movies, title()"]["en"]:
						#	if self.language["Small"] in self.media["Item"]["Titles"]:
						#		string += self.media["Item"]["Titles"][self.language["Small"]]
						#		string += " (" + self.media["Title"].split(" (")[-1] + "\n"

						# Watch the media for testing purposes
						#if self.switches["Testing"] == True:
						#	if hasattr(self, "Watch_Media") == False:
						#		from Watch_History.Watch_Media import Watch_Media as Watch_Media
						#		self.Watch_Media = Watch_Media
						#
						#	self.Watch_Media(self.dictionary, open_media = False)

						# Move the media folder to the new media type local folder
						#self.Move_Folder()

						self.media_item_number += 1

					# Add one to the "media number"
					media_number += 1

					if (
						self.switches["Testing"] == True and
						self.media_title != media_list[-1] and
						ask_for_input == True
					):
						self.Input.Type(self.Language.language_texts["continue, title()"])

			#self.Text.Copy(string)
			#input()

			if (
				self.switches["Testing"] == True and
				plural_media_type != self.media_types["Plural"]["en"][-1] and
				plural_media_type not in media_types_to_remove
			):
				self.Input.Type(self.Language.language_texts["continue, title()"])

			i += 1

		import collections

		# Sort the comment numbers by year dictionary based on its keys
		self.comments_number["Numbers"]["Years"] = dict(collections.OrderedDict(sorted(self.comments_number["Numbers"]["Years"].items())))

		# Sort the comment numbers by media type and by year dictionary based on its keys
		for plural_media_type in self.media_types["Plural"]["en"]:
			self.comments_number["Numbers"]["Type"][plural_media_type]["Years"] = dict(collections.OrderedDict(sorted(self.comments_number["Numbers"]["Type"][plural_media_type]["Years"].items())))

		# Only edit the root "Comments.json" file if the program iterated through all of the media types
		# (If a media type was removed from the list, the comments number will be wrong)
		#if media_types_to_remove == []:
			# Update the root "Comments.json" file
			#self.JSON.Edit(self.folders["Comments"]["Comments"], self.comments_number)

	def Update_Watched_Files(self):
		# Get the watched dictionary from the watched "Entries.json" file
		watched = self.JSON.To_Python(self.dictionary["Media"]["Item"]["Folders"]["Watched"]["entries"])

		# If the list of entries is not empty
		# And the dictionary of entries is empty
		if (
			watched["Entries"] != [] and
			watched["Dictionary"] == {}
		):
			# Iterate through the list of entries
			for entry_name in watched["Entries"]:
				import re

				# Search for the year inside the entry name
				match = re.search(r"\b(\d{4})\b", entry_name)

				# If it exists
				if match:
					# Get the year from the search group
					year = match.group(1)

				# Get the year folder
				year_folder = self.folders["Watch History"][str(year)]

				# Get the entries file
				entries_file = year_folder["root"] + "Entries.json"

				# Read it
				entries = self.JSON.To_Python(entries_file)

				if entry_name not in entries["Dictionary"]:
					print()
					print(entry_name)
					self.System.Open(entries_file, open = True)

				# Get the entry dictionary based on the entry name
				entry = entries["Dictionary"][entry_name]

				# Add the entry dictionary to the watched "Dictionary" key
				watched["Dictionary"][entry_name] = entry

		# Update the watched "Entries.json" file with the updated watched dictionary
		self.JSON.Edit(self.dictionary["Media"]["Item"]["Folders"]["Watched"]["entries"], watched)

	def Update_Comments_JSON(self):
		# Get the comments dictionary from the comments file
		comments = self.JSON.To_Python(self.dictionary["Media"]["Item"]["Folders"]["comments"]["comments"])

		# If the list of entries is not empty
		if comments["Entries"] != []:
			# Define the comment number
			comment_number = 1

			# Iterate through the list of entries
			for entry in comments["Entries"]:
				# Get the comment dictionary from the entries dictionary
				comment = comments["Dictionary"][entry]

				# Add the comment number as the first key
				comment = {
					"Comment number": comment_number,
					**comment
				}

				# Replace the "Lines" key with the "Number of comment lines"
				new_key = "Number of comment lines"
				after_key = "Lines"
				comment = self.JSON.Add_Key_After_Key(comment, {new_key: comment[after_key]}, after_key = after_key, remove_after_key = True)

				# Update the root comment dictionary with the local comment dictionary
				comments["Dictionary"][entry] = comment

				# Add to the comment number
				comment_number += 1

		# Update the "Comments.json" file with the updated comments dictionary
		self.JSON.Edit(self.dictionary["Media"]["Item"]["Folders"]["comments"]["comments"], comments)

	def Update_Comment_Files(self):
		# Make a shortcut for the comments "Files" folder
		files_folder = self.media["Item"]["Folders"]["comments"]["files"]["root"]

		# List the comment files inside the folder
		files = self.Folder.Contents(files_folder)["file"]["list"]

		# Define the "to convert" variable to specify what should be converted
		to_convert = "Time"

		# Iterate through the files inside the list of files
		for file in files:
			# Get the text of the file
			text = self.File.Contents(file)["string"]

			# If the "to convert" variable is "Episode titles"
			if to_convert == "Episode titles":
				# Iterate through the list of texts to replace
				for item in ["Títulos do episódio", "Título do episódio"]:
					# Define the "with" text to add in place of the item as "Episode title"
					with_ = self.language_texts["episode_title"]

					# Get the title text template
					title_template = self.language_texts["{}_title"]

					# If the item type is not in the list of main media types
					# And the item type is inside the list of alternative episode types
					# alternative_episode_types = ["OVA", "ONA", "Special", "Especial", "Shorts", "Curtas"]
					if (
						self.media["Item"]["Type"]["en"] not in self.media_types["Singular"]["en"] and
						self.media["Item"]["Type"]["en"] in self.alternative_episode_types
					):
						# Format it as "Title of the [item type]" in the user language
						with_ = title_template.format(self.media["Item"]["Type"][self.language["Small"]].lower())

					# If the media type is "Movies"
					# Or the media type is "Videos" and the media is not episodic
					if (
						self.dictionary["Media type"]["Plural"]["en"] == "Movies" or
						(self.dictionary["Media type"]["Plural"]["en"] == "Videos" and
						not self.media["States"]["Episodic"])
					):
						# Define a shortcut for the singular media type
						singular_media_type = self.dictionary["Media type"]["Singular"][self.language["Small"]]

						# Determine the case of the singular media type based on the position of the "{}" characters
						if title_template.startswith("{}"):
							# If "{}" is at the beginning, use the media type as is (already in uppercase)
							with_ = title_template.format(singular_media_type)

						else:
							# If "{}" is at the end, convert the media type to lowercase
							with_ = title_template.format(singular_media_type.lower())

					# Replace the current text with the "with" text (in the user language)
					text = text.replace(item + ":", with_ + ":")

			# If the "to convert" variable is "Time"
			elif to_convert == "Time":
				# Define the "replace" text as "Time" in the user language
				replace_ = self.Date.language_texts["time, title()"]

				# Define the "with" text to add in place of the item as "Comment time"
				with_ = self.language_texts["comment_time"]

				# Replace the current text with the "with" text (in the user language)
				text = text.replace(replace_ + ":", with_ + ":")

			# Update the file
			self.File.Edit(file, text, "w")

	def Check_Episodes_Titles(self):
		# Get the media status
		media_status = self.dictionary["Media"]["Details"][self.Language.language_texts["status, title()"]]

		# Get the list of on hold statuses
		on_hold_statuses = [
			"Plan to watch",
			"Completed"
		]

		# If the "Titles" key is present in the media item "Folders" dictionary
		# And the media watching status is not "Plan to watch" or "Completed"
		if (
			"Titles" in self.dictionary["Media"]["Item"]["Folders"] and
			media_status not in on_hold_statuses
		):
			# Define a shortcut to the titles folder
			titles_folder = self.dictionary["Media"]["Item"]["Folders"]["Titles"]["root"]

			# Define the titles file to check its contents
			titles_file = titles_folder + self.languages["Full"]["en"] + ".txt"

			# If the titles file is empty
			if self.File.Contents(titles_file)["lines"] == []:
				# Iterate through the language dictionaries
				for language in self.languages["Dictionary"].values():
					# Define a shortcut to the full language
					full_language = language["Full"]

					# Define the language titles file
					titles_file = titles_folder + full_language + ".txt"

					# Open it for user to fill it with titles
					self.System.Open(titles_file)

				# Wait for the user input (meaning the user finished filling the titles file)
				self.Input.Type(self.Language.language_texts["continue, title()"])

	def Add_Date(self):
		item_types = ["Media"]

		if self.dictionary["Media"]["States"]["Has a list of media items"] == True:
			item_types.append("Item")

		# Iterate through the item_types list
		for item_type in item_types:
			media_dictionary = self.dictionary["Media"]

			if item_type == "Item":
				media_dictionary = self.dictionary["Media"]["Item"]

			# Get the details file and details for the media (item)
			self.date_dictionary = {
				"file": media_dictionary["Folders"]["details"],
				"Details": self.File.Dictionary(media_dictionary["Folders"]["details"])
			}

			ask = False

			# If the "Year" key is in the details and is not "?" and the "Date" key is not in the details
			if (
				self.Date.language_texts["year, title()"] in self.date_dictionary["Details"] and
				self.date_dictionary["Details"][self.Date.language_texts["year, title()"]] != "?" and
				self.Date.language_texts["start_date"] not in self.date_dictionary["Details"]
			):
				# Get the year from the details
				year = self.date_dictionary["Details"][self.Date.language_texts["year, title()"]]

				# If the media has a list of media items
				if media_dictionary["States"]["Has a list of media items"] == True:
					# If the media title is equal to the media item title and the date is already present in the media details
					if self.dictionary["Media"]["Title"] == self.dictionary["Media"]["Item"]["Title"] and self.Date.language_texts["start_date"] in self.dictionary["Media"]["Details"]:
						# Get the date from the media details
						date = self.dictionary["Media"]["Details"][self.Date.language_texts["start_date"]]

						# Do not ask for the full date
						ask = False

					# If the media title is not equal to the media item title or the date is not present in the media details
					if item_type == "Item" and self.dictionary["Media"]["Title"] != self.dictionary["Media"]["Item"]["Title"] or self.Date.language_texts["start_date"] not in self.dictionary["Media"]["Details"]:
						# Do ask for the full date
						ask = True

				# If the media has no media item list, ask for the full date
				if media_dictionary["States"]["Has a list of media items"] == False:
					ask = True

				if ask == True:
					# If the media item title is not equal to the media title, show the media item title
					if self.dictionary["Media"]["Item"]["Title"] != self.dictionary["Media"]["Title"]:
						print()
						print(self.dictionary["Media"]["Item"]["Title"] + ":")

					# Show the year
					print(self.Date.language_texts["year, title()"] + ": " + year)

					date = ""

					# Ask for the day and month separated by a slash, because the year is already inside the details
					while re.search(r"[0-9]{2,2}/[0-9]{2,2}", date) == None:
						date = self.Input.Type(self.Date.language_texts["day, title()"] + " " + self.Language.language_texts["and"] + " " + self.Date.language_texts["month"]) + "/" + year

				# Add the "date" key and value after the "year" key
				key_value = {
					"key": self.Date.language_texts["start_date"],
					"value": date
				}

				self.date_dictionary["Details"] = self.JSON.Add_Key_After_Key(self.date_dictionary["Details"], key_value, self.Date.language_texts["year, title()"])

				# Update the media or media item details file
				self.File.Edit(self.date_dictionary["file"], self.Text.From_Dictionary(self.date_dictionary["Details"]), "w")

			# If the "Year" key is not inside the media (item) details
			if self.Date.language_texts["year, title()"] not in self.date_dictionary["Details"]:
				# Show the details file
				print(self.date_dictionary["file"])

				# Open it on the text editor
				self.System.Open(self.date_dictionary["file"], open = True)

				# And end the program execution
				quit()

	def Count_Comments_Number(self):
		# Get comments dictionary from file
		comments = self.JSON.To_Python(self.dictionary["Media"]["Item"]["Folders"]["comments"]["comments"])

		# If the entries list is not empty
		if comments["Entries"] != []:
			# Iterate through the entries list
			for entry_name in comments["Entries"]:
				# Get the entry from the entries dictionary
				entry = comments["Dictionary"][entry_name]

				# If the "Date" key is inside the entry dictionary
				if "Date" in entry:
					# If the date is not empty
					if entry["Date"] != "":
						# If the date has more than the year
						if len(entry["Date"]) != 4:
							# Get the year from the date by converting the date into a date dictionary
							year = self.Date.From_String(entry["Date"])["Units"]["Year"]

						# If the date contains only the year
						if len(entry["Date"]) == 4:
							year = entry["Date"]

						# Add one to the comments number by year
						self.comments_number["Numbers"]["Years"][str(year)] += 1

						# Add one to the comments number by type and by year
						self.comments_number["Numbers"]["Type"][self.dictionary["Media type"]["Plural"]["en"]]["Years"][str(year)] += 1

					# If the date is empty or the date contains only the year
					if entry["Date"] == "" or len(entry["Date"]) == 4:
						# Add one to the comments without date
						self.comments_number["Numbers"]["No time"] += 1

						# Add one to the comments without time by type
						self.comments_number["Numbers"]["Type"][self.dictionary["Media type"]["Plural"]["en"]]["No time"] += 1

					# Add one to the total comments number by type
					self.comments_number["Numbers"]["Total"] += 1

					# Add one to the total comments number by type
					self.comments_number["Numbers"]["Type"][self.dictionary["Media type"]["Plural"]["en"]]["Total"] += 1

	def Add_Anime_Information(self):
		item_types = ["Media"]

		if self.dictionary["Media"]["States"]["Has a list of media items"] == True:
			item_types.append("Item")

		for item_type in item_types:
			media_dictionary = self.dictionary["Media"]

			if item_type == "Item":
				media_dictionary = self.dictionary["Media"]["Item"]

			if "Link" not in media_dictionary["Details"]:
				# Remove special characters from media (item) title
				title = media_dictionary["title"]

				# Remove non-url items from title
				for text in [",", ":", "(", ")", ".", "!", "?"]:
					title = title.replace(text, "")

				# Add media title to media item title to use on search
				if self.dictionary["Media"]["Item"]["Title"] != self.dictionary["Media"]["Title"]:
					title = self.dictionary["Media"]["Title"] + " " + title

				if (
					# If media has media item list and the media item is not the same as the the root media
					self.dictionary["Media"]["States"]["Has a list of media items"] == True and
					self.dictionary["Media"]["Item"]["Title"] != self.dictionary["Media"]["Title"] or

					# If media has media item list and the media item is not the same as the the root media
					self.dictionary["Media"]["States"]["Has a list of media items"] == True and
					self.dictionary["Media"]["Item"]["Title"] == self.dictionary["Media"]["Title"] or

					# Or the media does not have a media item list and the media item is the same as the root media and the "ID" key is not present inside the media details
					self.dictionary["Media"]["States"]["Has a list of media items"] == False and
					self.dictionary["Media"]["Item"]["Title"] == self.dictionary["Media"]["Title"] and
					"ID" not in self.dictionary["Media"]["Details"]

				):
					# Open MyAnimeList search page with media (item) title parameter
					self.System.Open("https://myanimelist.net/search/all?q={}&cat=anime".format(title))

					print()
					print("\t\t" + media_dictionary["title"] + ":")

					# Ask for media (item) link
					link = self.Input.Type(self.Language.language_texts["{}_website_link"].format("MyAnimeList"))

					# Get ID from link
					id = link.split("/")[-2]

					# Get information from MyAnimeList using anime ID
					get_information_from_mal = True

				# If the media has a list of media items and the media item is the same as the media and the "ID" key is present inside the media details
				if (
					self.dictionary["Media"]["Item"]["Title"] == self.dictionary["Media"]["Title"] and
					"ID" in self.dictionary["Media"]["Details"]
				):
					# Get link and ID from media details
					link = self.dictionary["Media"]["Details"]["Link"]
					id = self.dictionary["Media"]["Details"]["ID"]

					# Get anime information from "Anime.json" file
					media_dictionary["Information"]["Dictionary"] = self.JSON.To_Python(self.dictionary["Media"]["Folders"]["anime"])

					# Do not get information from MyAnimeList
					get_information_from_mal = False

				# Add the MyAnimeList ID after the "Episodes" key
				key_value = {
					"key": "ID",
					"value": id
				}

				after_key = self.language_texts["episodes, title()"]

				if self.dictionary["Media"]["States"]["Single unit"] == True:
					after_key = self.language_texts["single_unit"]

				media_dictionary["Details"] = self.JSON.Add_Key_After_Key(media_dictionary["Details"], key_value, after_key = after_key)

				# Add the MyAnimeList Link after the "ID" key
				key_value = {
					"key": "Link",
					"value": link
				}

				media_dictionary["Details"] = self.JSON.Add_Key_After_Key(media_dictionary["Details"], key_value, after_key = "ID")

				if get_information_from_mal == True:
					# Get anime details
					media_dictionary["Information"]["Dictionary"] = self.API.Call("MyAnimeList", {"id": media_dictionary["Details"]["ID"]})["response"]

					# Define links dictionary
					media_dictionary["Information"]["Dictionary"]["Links"] = {
						"Official": {},
						"MyAnimeList": {
							"Link": link,
							"en": link,
							"ID": id
						}
					}

				self.Paste_Links(media_dictionary)

				# Format anime information dictionary
				media_dictionary["Information"]["Dictionary"] = self.Format_Anime_Information(media_dictionary, media_dictionary["Information"]["Dictionary"])

				# Add time to date
				if "Broadcast" in media_dictionary["Information"] and media_dictionary["Information"]["Dictionary"]["Broadcast"]:
					if len(media_dictionary["Details"][self.Date.language_texts["start_date"]]) <= 10 and len(media_dictionary["Information"]["Dictionary"]["Broadcast"]["Time"]) == 5:
						media_dictionary["Details"][self.Date.language_texts["start_date"]] = media_dictionary["Information"]["Broadcast"]["Time"] + " " + media_dictionary["Details"][self.Date.language_texts["start_date"]]

				# Remove the "date" key of media (anime) details
				if self.Date.language_texts["date, title()"] in media_dictionary["Details"]:
					media_dictionary["Details"].pop(self.Date.language_texts["date, title()"])

				# Add start and end date to media (item) details
				for key in ["Start", "End"]:
					text_key = "start_date"
					after_key = self.Date.language_texts["year, title()"]

					if key == "End":
						text_key = "end_date"
						after_key = self.Date.language_texts["start_date"]

					# Add date key to media (item) details after the "Year" key
					key_value = {
						"key": self.Date.language_texts[text_key],
						"value": "??/??/????"
					}

					if media_dictionary["Information"]["Dictionary"]["Dates"][key] != {}:
						key_value["value"] = media_dictionary["Information"]["Dictionary"]["Dates"][key]["Date"]["DD/MM/YYYY"]

						if media_dictionary["Information"]["Dictionary"]["Dates"][key]["Date Time"] != {}:
							key_value["value"] = media_dictionary["Information"]["Dictionary"]["Dates"][key]["DateTime"]["HH:MM DD/MM/YYYY"]

					media_dictionary["Details"] = self.JSON.Add_Key_After_Key(media_dictionary["Details"], key_value, after_key = after_key)

				media_dictionary["Details"] = self.JSON.Add_Key_After_Key(media_dictionary["Details"], key_value, after_key = self.Date.language_texts["start_date"])

				# Add the episode duration after the "Episodes" key
				key_value = {
					"key": self.Date.language_texts["duration, title()"],
					"value": media_dictionary["Information"]["Dictionary"]["Duration"]["Text"][self.language["Small"]]
				}

				if key_value["value"] == "":
					key_value["value"] = 0

				# Change duration key if episodes are more than one
				if media_dictionary["Information"]["Dictionary"]["Episodes"]["Number"] > 1:
					key_value["key"] = self.language_texts["episodes_duration"]

				media_dictionary["Details"] = self.JSON.Add_Key_After_Key(media_dictionary["Details"], key_value, after_key = self.language_texts["episodes, title()"])

				# Add "Studio(s)" key to media (item) details after the "Episodes duration" key
				key_value = {
					"key": self.Text.By_Number(media_dictionary["Information"]["Dictionary"]["Studios"], self.Language.language_texts["studio, title()"], self.Language.language_texts["studios, title()"]),
					"value": self.Text.From_List(media_dictionary["Information"]["Dictionary"]["Studios"])
				}

				media_dictionary["Details"] = self.JSON.Add_Key_After_Key(media_dictionary["Details"], key_value, after_key = self.language_texts["episodes_duration"])

				if media_dictionary["Information"]["Dictionary"]["Links"]["Wikipedia"] != {}:
					# Add "Wikipedia" key to media (item) details after the "Link" key
					key_value = {
						"key": self.Language.language_texts["wikipedia, title()"],
						"value": ""
					}

					if self.language["Small"] in media_dictionary["Information"]["Dictionary"]["Links"]["Wikipedia"]:
						key_value["value"] = media_dictionary["Information"]["Dictionary"]["Links"]["Wikipedia"][self.language["Small"]]

					else:
						key_value["value"] = media_dictionary["Information"]["Dictionary"]["Links"]["Wikipedia"]["en"]

					media_dictionary["Details"] = self.JSON.Add_Key_After_Key(media_dictionary["Details"], key_value, after_key = self.Language.language_texts["link, title()"])

				# Update media (item) details file
				self.File.Edit(media_dictionary["Folders"]["details"], self.Text.From_Dictionary(media_dictionary["Details"]), "w")

				if media_dictionary["Information"]["Dictionary"]["Links"]["Wikipedia"]["Episode list"] == {}:
					media_dictionary["Information"]["Dictionary"]["Links"]["Wikipedia"].pop("Episode list")

				# Write anime details into media "[Anime]/[Season].json" file
				self.JSON.Edit(media_dictionary["Folders"][media_dictionary["Information"]["Key"]], media_dictionary["Information"]["Dictionary"])

	def Format_Anime_Information(self, media_dictionary, information):
		new_information = {
			"Title": "",
			"Titles": {},
			"ID": "",
			"Link": media_dictionary["Details"]["Link"],
			"Links": {},
			"Description": "",
			"Background": "",
			"Format": "",
			"Source": "",
			"Rating": "",
			"Pictures": [],
			"Genres": [],
			"Media items": {},
			"Episodes": {
				"Number": 0,
				"Titles": {}
			},
			"Duration": {},
			"Time": "",
			"Dates": {
				"Start": {},
				"End": {}
			},
			"Start season": {},
			"Broadcast": {},
			"Related": {},
			"Studios": [],
			"Original language": "Japanese",
			"Country of origin": "Japan"
		}

		if "title" in information:
			new_information["Title"] = information["title"]

		else:
			new_information["Title"] = information["Title"]

		for title in media_dictionary["Titles"]:
			if key not in ["Language", "Sanitized"]:
				new_information["Titles"][key] = media_dictionary["Titles"][key]

		if "alternative_titles" in information:
			new_information["Titles"].update(information["alternative_titles"])

		if "id" in information:
			new_information["ID"] = information["id"]

		else:
			new_information["ID"] = information["ID"]

		# Add link to links dictionary
		for key in information["Links"]:
			new_information["Links"][key] = information["Links"][key]

		if "Media type" in information:
			new_information["Format"] = information["Media type"]

		else:
			new_information["Format"] = information["Format"]

		# Change format of anime to title if it is not "TV", "OVA", or "ONA"
		if new_information["Format"] in ["movie", "special", "music"]:
			new_information["Format"] = new_information["Format"].title()

		# Change format of anime to uppercase if it is "TV", "OVA", or "ONA"
		else:
			new_information["Format"] = new_information["Format"].upper()

		if "source" in information:
			new_information["Source"] = information["source"].replace("4_koma", "4-koma").replace("_", " ").capitalize()

		else:
			new_information["Source"] = information["Source"]

		if "rating" in information:
			new_information["Rating"] = information["rating"].upper().replace("_", " ")

		else:
			new_information["Rating"] = information["Rating"]

		# Add pictures
		if "pictures" in information:
			for dict_ in information["pictures"]:
				new_information["Pictures"].append(dict_["large"])

		else:
			new_information["Pictures"] = information["Pictures"]

		# Add genres
		if "genres" in information:
			for dict_ in information["genres"]:
				new_information["Genres"].append(dict_["name"])

		else:
			new_information["Genres"] = information["Genres"]

		# Add media items number
		if media_dictionary["title"] == self.dictionary["Media"]["Title"]:
			new_information["Media items"] = {
				"Number": self.dictionary["Media"]["Items"]["number"],
				"List": self.dictionary["Media"]["Items"]["List"]
			}

		# Get episode number
		if "num_episodes" in information:
			new_information["Episodes"]["Number"] = information["num_episodes"]

		else:
			if "Episodes" in information["Episodes"]:
				new_information["Episodes"]["Number"] = information["Episodes"]["Number"]

			else:
				new_information["Episodes"]["Number"] = media_dictionary["episodes"]["number"]

		# Get the episode titles
		if "Titles" in self.dictionary["Media"]["Item"]["Episodes"]:
			new_information["Episodes"]["Titles"] = self.dictionary["Media"]["Item"]["Episodes"]["Titles"]

			if "Files" in new_information["Episodes"]["Titles"]:
				new_information["Episodes"]["Titles"].pop("Files")

		if "average_episode_duration" in information:
			new_information["Duration"] = information["average_episode_duration"]

			# Define duration dictionary
			new_information["Duration"] = {
				"Hours": 0,
				"Minutes": divmod(new_information["Duration"], 60)[0],
				"Seconds": divmod(new_information["Duration"], 60)[1],
				"Time": "",
				"Text": {}
			}

			# Define duration text
			new_information["Duration"]["Time"] = str(new_information["Duration"]["Minutes"]) + ":" + str(new_information["Duration"]["Seconds"])

			# Define duration time text
			for language in self.languages["Small"]:
				# Define duration time text using "Time_Text" method of "Date" class
				new_information["Duration"]["Text"][language] = self.Date.Time_Text("0:" + new_information["Duration"]["Time"], language)

			if new_information["Duration"]["Minutes"] > 60:
				# Define add leading zeroes to hours
				new_information["Duration"]["Hours"] = self.Text.Add_Leading_Zeroes(divmod(new_information["Duration"]["Minutes"], 60)[0])

				# Define add leading zeroes to minutes
				new_information["Duration"]["Minutes"] = self.Text.Add_Leading_Zeroes(divmod(new_information["Duration"]["Minutes"], 60)[1])

				# Define add leading zeroes to seconds
				new_information["Duration"]["Seconds"] = self.Text.Add_Leading_Zeroes(new_information["Duration"]["Seconds"])

				# Define duration time
				new_information["Duration"]["Time"] = str(new_information["Duration"]["Hours"]) + ":" + str(new_information["Duration"]["Minutes"]) + ":" + str(new_information["Duration"]["Seconds"])

				# Define duration time text using "Time_Text" method of "Date" class
				for language in self.languages["Small"]:
					new_information["Duration"]["Text"][language] = self.Date.Time_Text(new_information["Duration"]["Time"], language)

				# Convert times to integer
				for key in new_information["Duration"]:
					if key not in ["Time", "Text"]:
						new_information["Duration"][key] = int(new_information["Duration"][key])

		else:
			new_information["Duration"] = information["Duration"]

		# Add time
		if "start_date" in information:
			# Add dates
			for key in ["Start", "End"]:
				if "start_date" in information:
					date = information["start_date"]

					if key == "End":
						date = information["end_date"]

					new_information["Dates"][key] = {
						"Date": {
							"YYYY-MM-DD": date,
							"DD/MM/YYYY": self.Date.From_String(date)["Formats"]["DD/MM/YYYY"]
						},
						"Time": {},
						"DateTime": {},
						"Year": self.Date.From_String(date)["Units"]["Year"]
					}

			new_information["Time"] = self.Date.To_String(self.Date.From_String(information["start_date"])["Object"], utc = True)

		else:
			if "Dates" in information:
				new_information["Dates"] = information["Dates"]

			if "Time" in information:
				new_information["Time"] = information["Time"]

			elif new_information["Dates"]["Start"] != {} and new_information["Dates"]["Start"]["DateTime"] != {}:
				new_information["Time"] = new_information["Dates"]["Start"]["DateTime"]["YYYY-MM-DDTHH:MM:SSZ"]

			if "DateTime" in new_information["Dates"]["Start"] and new_information["Dates"]["Start"]["DateTime"] == {}:
				new_information["Time"] = self.Date.To_String(self.Date.From_String(new_information["Dates"]["Start"]["Date"]["YYYY-MM-DD"])["Object"], utc = True)

		if "start_season" in information:
			new_information["Start season"] = {
				"Year": information["start_season"]["year"],
				"Season": information["start_season"]["season"].title()
			}

		elif "Start season" in information:
			new_information["Start season"] = information["Start season"]

		# Add broadcast time to anime dates
		if "broadcast" in information:
			new_information["Broadcast"]["Time"] = information["broadcast"]["start_time"]

			for key in ["Start", "End"]:
				date = information["start_date"]

				if key == "End":
					date = information["end_date"]

				# And hours and minutes
				new_information["Dates"][key]["Time"]["HH:MM"] = information["broadcast"]["start_time"]

				# Add ISO-8601 date time and European date time
				new_information["Dates"][key]["Date Time"].update({
					"YYYY-MM-DDTHH:MM:SSZ": new_information["Dates"][key]["Date"]["YYYY-MM-DD"] + "T" + information["broadcast"]["start_time"] + ":00Z",
					"HH:MM DD/MM/YYYY": information["broadcast"]["start_time"] + " " + self.Date.From_String(date)["Formats"]["DD/MM/YYYY"]
				})

			new_information["Time"] = new_information["Dates"]["Start"]["Date Time"]["YYYY-MM-DDTHH:MM:SSZ"]

		elif "Broadcast" in information:
			new_information["Broadcast"] = information["Broadcast"]

		if "synopsis" in information:
			new_information["Description"] = information["synopsis"]

		else:
			new_information["Description"] = information["Description"]

		# Add related manga
		if "related_manga" in information:
			if information["related_manga"] != []:
				new_information["Related"]["Manga"] = {}

				# Iterate through manga dictionaries
				for dict_ in information["related_manga"]:
					dict_ = {
						"ID": dict_["node"]["id"],
						"Title": dict_["node"]["title"],
						"Picture": dict_["node"]["main_picture"]["large"],
						"Relation": {
							"Lower": dict_["relation_type"],
							"Type": dict_["relation_type_formatted"]
						}
					}

					new_information["Related"]["Manga"][dict_["Title"]] = dict_

		elif "Manga" in information["Related"]:
			new_information["Related"]["Manga"] = information["Related"]["Manga"]

		# Add related anime
		if "related_anime" in information:
			if information["related_anime"] != []:
				new_information["Related"]["Anime"] = {}

				# Iterate through anime dictionaries
				for dict_ in information["related_anime"]:
					dict_ = {
						"ID": dict_["node"]["id"],
						"Title": dict_["node"]["title"],
						"Picture": dict_["node"]["main_picture"]["large"],
						"Relation": {
							"Lower": dict_["relation_type"],
							"Type": dict_["relation_type_formatted"]
						}
					}

					new_information["Related"]["Anime"][dict_["Title"]] = dict_

		else:
			new_information["Related"]["Anime"] = information["Related"]["Anime"]

		# Add studios
		if "studios" in information:
			for dict_ in information["studios"]:
				new_information["Studios"].append(dict_["name"])

		else:
			new_information["Studios"] = information["Studios"]

		if "background" in information:
			new_information["Background"] = information["background"]

		elif "Background" in information:
			new_information["Background"] = information["Background"]

		# If background is empty, remove the key
		if new_information["Background"] == "":
			new_information.pop("Background")

		return new_information

	def Add_Media_Information(self):
		item_types = ["Media"]

		if self.dictionary["Media"]["States"]["Has a list of media items"] == True:
			item_types.append("Item")

		for item_type in item_types:
			media_dictionary = self.dictionary["Media"]

			if item_type == "Item":
				media_dictionary = self.dictionary["Media"]["Item"]

			if self.File.Contents(media_dictionary["Folders"][media_dictionary["Information"]["Key"]])["lines"] == []:
				# Remove special characters from media (item) title
				title = media_dictionary["title"]

				# Remove non-url items from title
				for text in [",", ":", "(", ")", ".", "!", "?"]:
					title = title.replace(text, "")

				# Add media title to media item title to use on search
				if self.dictionary["Media"]["Item"]["Title"] != self.dictionary["Media"]["Title"]:
					title = self.dictionary["Media"]["Title"] + " " + title

				self.Paste_Links(media_dictionary)

				# Format media information dictionary
				media_dictionary["Information"]["Dictionary"] = self.Format_Media_Information(media_dictionary, media_dictionary["Information"]["Dictionary"])

				# Update media (item) details file
				self.File.Edit(media_dictionary["Folders"]["details"], self.Text.From_Dictionary(media_dictionary["Details"]), "w")

				# Write media details into media "[Information file name].json" file
				self.JSON.Edit(media_dictionary["Folders"][media_dictionary["Information"]["Key"]], media_dictionary["Information"]["Dictionary"])

		# --- Videos --- #
		# To-Do: Add title and titles to "Channel.json" and "Playlist.json"
		# Add links and dates dictionaries
		# Add episodes and episode titles, pictures, (media items), original language, and country of origin
		# -------------- #

		variable = None

	def Paste_Links(self, media_dictionary):
		links = {
			"Official": {
				"Link": self.Language.language_texts["official_website"],
				"Twitter": "Twitter"
			},
			"Wikipedia": {
				"Languages": [
					"ja",
					"en",
					"pt"
				],
				"Gender": "feminine"
			},
			"Fandom": {
				"Languages": [
					"en"
				]
			},
			"IMDB": {
				"Languages": [
					"en"
				]
			}
		}

		# Add "CrunchyRoll" website to links dictionary
		if self.dictionary["Media type"]["Plural"]["en"] == self.texts["animes, title()"]["en"]:
			links["CrunchyRoll"] = {
				"Languages": [
					"en"
				],
				"Gender": "feminine"
			}

		# Add "Netflix" website to links dictionary
		if self.dictionary["Media type"]["Plural"]["en"] == self.texts["series, title()"]["en"]:
			links["Netflix"] = {
				"Languages": [
					"en"
				],
				"Gender": "feminine"
			}

		# Define links dictionary of video media
		if self.dictionary["Media type"]["Plural"]["en"] == self.texts["videos, title()"]["en"]:
			links = {
				"Official": {},
				"YouTube": {
					"Link": "YouTube"
				}
			}

		# Remove Japanese Wikipedia language if media type is not "Animes"
		if self.dictionary["Media type"]["Plural"]["en"] != self.texts["animes, title()"]["en"] and "Wikipedia" in links:
			links["Wikipedia"]["Languages"].pop("ja")

		# Iterate through links dictionary
		for link_key in links:
			link = links[link_key]

			# If the link key is not inside media information links, add it
			if link_key not in media_dictionary["Information"]["Dictionary"]["Links"]:
				media_dictionary["Information"]["Dictionary"]["Links"][link_key] = {}

			# if the link key is inside the root media information links, get the links dictionary from it
			if link_key in self.dictionary["Media"]["Information"]["Dictionary"]["Links"]:
				media_dictionary["Information"]["Dictionary"]["Links"][link_key] = self.dictionary["Media"]["Information"]["Dictionary"]["Links"][link_key]

			if "Languages" in link:
				for language in link["Languages"]:
					if language in self.languages["Translated"][language]:
						# Get the transtaled language
						translated_full_language = self.languages["Translated"][language][self.language["Small"]]

					else:
						translated_full_language = language

					if "Gender" not in link:
						link["Gender"] = "masculine"

					# Define of and in texts
					of_text = self.Language.texts["genders, type: dictionary"][self.language["Small"]][link["Gender"]]["of"]
					in_text = self.Language.texts["genders, type: dictionary"][self.language["Small"]][link["Gender"]]["in"]

					# Define text to show when asking for user to paste the website link
					text = self.Language.language_texts["{}_website_link"].format(in_text + " " + translated_full_language + " " + of_text + " " + link_key)

					# If the language is not inside the links dictionary, ask for the website link
					if language not in media_dictionary["Information"]["Dictionary"]["Links"][link_key]:
						typed_link = self.Input.Type(text)

						# If the typed link is not empty, define the language link as the typed link
						if typed_link != "":
							media_dictionary["Information"]["Dictionary"]["Links"][link_key][language] = typed_link

							if link_key == "Fandom":
								media_dictionary["Information"]["Dictionary"]["Links"][link_key]["Domain"] = typed_link.split("https://")[-1].split(".")[0]

							if link_key in ["IMDB", "CrunchyRoll"]:
								media_dictionary["Information"]["Dictionary"]["Links"][link_key]["ID"] = typed_link.split("/")[-2]

					# If the link key is "Wikipedia" and the language is not "Japanese"
					if link_key == "Wikipedia" and language != "ja":
						# Define empty dictionary for "episode list" links
						episode_list_links = {}

						# Define text to show when asking for user to paste the episode list website link
						text = self.Language.language_texts["{}_website_link"].format(of_text + " " + self.language_texts["episode_list"].lower() + " " + in_text + " " + translated_full_language + " " + of_text + " " + self.Language.language_texts["wikipedia, title()"])

						# If the language is not inside the episode list links dictionary, ask for the episode list website link
						if (
							"Episode list" in media_dictionary["Information"]["Dictionary"]["Links"][link_key] and language not in media_dictionary["Information"]["Dictionary"]["Links"][link_key]["Episode list"] or
							"Episode list" not in media_dictionary["Information"]["Dictionary"]["Links"][link_key]
						):
							typed_link = self.Input.Type(text)

							# If the typed link is not empty, define the episode list language link as the typed link
							if typed_link != "":
								episode_list_links[language] = typed_link

			# If the link key is "Wikipedia"
			if link_key == "Wikipedia":
				# If the "Episode list" key is not inside the links dictionary
				if "Episode list" not in media_dictionary["Information"]["Dictionary"]["Links"][link_key]:
					# Define the "Episode list" dictionary as the episode list links dictionary
					media_dictionary["Information"]["Dictionary"]["Links"][link_key]["Episode list"] = episode_list_links

			# If the link dictionary does not contain a "Languages" list
			if "Languages" not in link:
				# Get the type text to show from the English language (default link language)
				text = link["Link"]

				if "Link" not in media_dictionary["Information"]["Dictionary"]["Links"][link_key]:
					typed_link = self.Input.Type(text)

					if typed_link != "":
						media_dictionary["Information"]["Dictionary"]["Links"][link_key]["Link"] = typed_link

				if "Twitter" not in media_dictionary["Information"]["Dictionary"]["Links"][link_key]:
					typed_link = self.Input.Type("Twitter")

					if typed_link != "":
						media_dictionary["Information"]["Dictionary"]["Links"][link_key]["Twitter"] = typed_link

		if self.dictionary["Media type"]["Plural"]["en"] == self.texts["videos, title()"]["en"]:
			media_dictionary["Information"]["Dictionary"]["Links"]["YouTube"]["ID"] = media_dictionary["Details"]["ID"]

			media_dictionary["Information"]["Dictionary"]["Links"]["Official"] = media_dictionary["Information"]["Dictionary"]["Links"]["YouTube"]

	def Format_Media_Information(self, media_dictionary, information):
		new_information = {
			"Title": "",
			"Titles": {},
			"ID": "", # For anime, videos

			# Anime: MyAnimeList
			# Cartoons, series, and movies: English Wikipedia
			# Videos: YouTube
			"Link": media_dictionary["Details"]["Link"],

			"Links": {},

			# Anime, cartoons, series, and movies: Synopsis
			# Videos: Channel/Playlist description
			"Description": "",

			# For anime
			"Background": "",
			"Format": "",
			"Source": "",

			# For anime, cartoons, movies, and series
			"Rating": "",
			"Director": [],
			"Producer": [],
			"Distributor": [],
			# ---------------------------------------

			"Pictures": [],
			"Genres": [], # Videos: Type genres (Input.Lines)
			"Media items": {},
			"Episodes": {
				"Number": 0,
				"Titles": {}
			},
			"Duration": {},
			"Time": "", # YYYY-MM-DDTHH:MM:SSZ
			"Dates": {
				"Start": {},
				"End": {}
			},

			# For anime
			"Start season": {},
			"Broadcast": {},
			"Related": {},
			"Studios": [],
			# ---------

			"Chronology": {}, # Cartoons, movies, and series
			"Original language": "",
			"Country of origin": ""
		}

		# Add media titles
		for title in media_dictionary["Titles"]:
			if key not in ["Language", "Sanitized"]:
				new_information["Titles"][key] = media_dictionary["Titles"][key]

		# Remove ID if media type is not "Animes" or "Videos"
		if self.dictionary["Media type"]["Plural"]["en"] not in [self.texts["animes, title()"]["en"], self.texts["videos, title()"]["en"]]:
			new_information.pop("ID")

		# Remove chronology item if media type is "Animes" or "Videos"
		if self.dictionary["Media type"]["Plural"]["en"] in [self.texts["animes, title()"]["en"], self.texts["videos, title()"]["en"]]:
			new_information.pop("Chronology")

		items_to_remove = []

		# Remove anime items if media type is not "Animes"
		if self.dictionary["Media type"]["Plural"]["en"] != self.texts["animes, title()"]["en"]:
			items_to_remove.extend([
				"Background",
				"Format",
				"Source",
				"Start season",
				"Broadcast",
				"Related",
				"Studios"
			])

		# Remove non-video items if the media type is "Videos"
		if self.dictionary["Media type"]["Plural"]["en"] != self.texts["videos, title()"]["en"]:
			items_to_remove.extend([
				"Rating",
				"Director",
				"Producer",
				"Distributor"
			])

		for item in items_to_remove:
			if item in new_information:
				new_information.pop(item)

	def Move_Folder(self):
		old_folder = self.media["Folders"]["Media"]["root"]

		media_type_key = self.dictionary["Media type"]["Plural"]["en"].lower().replace(" ", "_")

		new_folder = self.folders["Media"][media_type_key]["root"] + self.media["Titles"]["Sanitized"] + "/"

		if self.Folder.Exists(old_folder) == True and self.Folder.Exists(new_folder) == False and self.media_item_number == 0:
			self.Folder.Create(new_folder)

			# Move the "C:/" folder
			self.Folder.Move(old_folder, new_folder)

			# Move the "D:/" folder
			old_folder = old_folder.replace("C:", "D:")
			new_folder = new_folder.replace("C:", "D:")

			self.Folder.Create(new_folder)

			self.Folder.Move(old_folder, new_folder)

		# Delete the empty old folders
		old_folder = self.Folder.folders["Media"]["root"] + self.media["Titles"]["Sanitized"] + "/"

		import os

		if self.Folder.Exists(old_folder) == True:
			file_list = self.Folder.Contents(old_folder)["file"]["list"]

			if file_list == []:
				self.Folder.Delete(old_folder)