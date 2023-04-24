# Manage.py

from Watch_History.Watch_History import Watch_History as Watch_History

import re
import collections

class Manage(Watch_History):
	def __init__(self):
		super().__init__()

		methods = {
			"Iterate_Through_Media_List": self.language_texts["iterate_through_media_list"],
			#"Convert_History": self.language_texts["convert_history"],
			"Add_To_Comments_Dictionary": self.language_texts["add_to_comments_dictionary"]
		}

		# Get the keys and values
		for name in ["keys", "values"]:
			methods[name] = list(getattr(methods, name)())

		# Add the methods to method keys list
		for method in methods.copy():
			if method not in ["keys", "values"]:
				methods[method] = getattr(self, method)

		# Select the method
		method = methods[self.Input.Select(methods["keys"], language_options = methods["values"])["option"]]
		method()

	def Iterate_Through_Media_List(self):
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
		for year in range(2018, self.date["year"] + 1):
			if str(year) not in self.comments_number["Numbers"]["Years"]:
				# If the year of the entry is not inside the comment numbers per year, add it
				self.comments_number["Numbers"]["Years"][str(year)] = 0

				for plural_media_type in self.media_types["Plural"]["en"]:
					if plural_media_type not in self.comments_number["Numbers"]["Type"]:
						self.comments_number["Numbers"]["Type"][plural_media_type] = {
							"Total": 0,
							"No time": 0,
							"Years": {}
						}

					# If the year of the entry is not inside the comment numbers per type per year, add it
					if str(year) not in self.comments_number["Numbers"]["Type"][plural_media_type]["Years"]:
						self.comments_number["Numbers"]["Type"][plural_media_type]["Years"][str(year)] = 0

		# Iterate through English plural media types list
		i = 0
		for plural_media_type in self.media_types["Plural"]["en"]:
			# Define the key of the media type for getting media type folders
			key = plural_media_type.lower().replace(" ", "_")

			# Define the language media type
			language_media_type = self.media_types["Plural"][self.user_language][i]

			# Get media with all "watching statuses", not just the "Watching" and "Re-watching" ones
			media_list = self.Get_Media_List(self.media_types[plural_media_type], self.texts["watching_statuses, type: list"]["en"])

			# Sort the media item list as case insensitive
			media_list = sorted(media_list, key = str.lower)

			# Show language media type
			print()
			print("----------")
			print()
			print(language_media_type + ":")

			media_types_to_remove = [
				#self.texts["animes, title()"]["en"],
				#self.texts["cartoons, title()"]["en"],
				#self.texts["series, title()"]["en"],
				#self.texts["movies, title()"]["en"],
				#self.texts["videos, title()"]["en"]
			]

			#string = ""

			# Remove a media type from the list (optional)
			if plural_media_type not in media_types_to_remove:
				# For media in media item list
				for self.media_title in media_list:
					# Define root dictionary with media type and media
					self.dictionary = {
						"Media type": self.media_types[plural_media_type],
						"Media": {
							"Title": self.media_title
						}
					}

					# Show media title
					print()
					print("\t" + "---")
					print()
					print("\t" + self.dictionary["Media"]["Title"] + ":")

					# Select media and define its variables, returning the media dictionary (without asking user to select the media)
					self.dictionary = self.Select_Media(self.dictionary)

					# Define the media items list as the media title for media without a media item list
					self.media_items_list = [
						self.dictionary["Media"]["Item"]["Title"]
					]

					# For media with media item list, get the actual media items
					if self.dictionary["Media"]["States"]["Media item list"] == True:
						self.media_items_list = self.dictionary["Media"]["Items"]["List"]

					# Iterate through media items list
					for self.media_item in self.media_items_list:
						# Define media item
						self.dictionary = self.Define_Media_Item(self.dictionary, media_item = self.media_item)

						# Show media item title
						print()
						print("\t\t" + self.dictionary["Media"]["Item"]["Title"] + ":")

						# Verify if empty episodes' titles files exist
						#self.Check_Episodes_Titles()

						# Add exact media or media item creation or release to media or media item details
						self.Add_Date()

						# Re-count comments numbers
						self.Count_Comments_Number()

						# Add anime information to anime details
						#if self.dictionary["Media type"]["Plural"]["en"] == self.texts["animes, title()"]["en"]:
						#	self.Add_Anime_Information()

						# Add media information to media details and media information file
						#self.Add_Media_Information()

						#if self.dictionary["Media type"]["Plural"]["en"] == self.texts["videos, title()"]["en"]:
						#	self.Add_Last_Playlist_Date()

						#if self.dictionary["Media type"]["Plural"]["en"] == self.texts["movies, title()"]["en"]:
						#	if self.user_language in self.dictionary["Media"]["Item"]["Titles"]:
						#		string += self.dictionary["Media"]["Item"]["Titles"][self.user_language]
						#		string += " (" + self.dictionary["Media"]["Title"].split(" (")[-1] + "\n"

						# Watch the media for testing purposes
						#if self.switches["testing"] == True:
						#	if hasattr(self, "Watch_Media") == False:
						#		from Watch_History.Watch_Media import Watch_Media as Watch_Media
						#		self.Watch_Media = Watch_Media
						#
						#	self.Watch_Media(self.dictionary, open_media = False)

					if self.switches["testing"] == True and self.media_title != media_list[-1]:
						self.Input.Type(self.JSON.Language.language_texts["continue, title()"])

			#self.Text.Copy(string)
			#input()

			if self.switches["testing"] == True and plural_media_type != self.media_types["Plural"]["en"][-1] and plural_media_type not in media_types_to_remove:
				self.Input.Type(self.JSON.Language.language_texts["continue, title()"])

			i += 1

		# Sort year comment number keys
		self.comments_number["Numbers"]["Years"] = dict(collections.OrderedDict(sorted(self.comments_number["Numbers"]["Years"].items())))

		# Sort media type year comment numbers keys
		for plural_media_type in self.media_types["Plural"]["en"]:
			self.comments_number["Numbers"]["Type"][plural_media_type]["Years"] = dict(collections.OrderedDict(sorted(self.comments_number["Numbers"]["Type"][plural_media_type]["Years"].items())))

		# Only edit the root Comments file if the program iterated through all of the media types
		# (If a media type was removed from the list, the comments number will be wrong)
		if media_types_to_remove == []:
			# Update the root "Comments.json" file
			self.JSON.Edit(self.folders["comments"]["comments"], self.comments_number)

	def Check_Episodes_Titles(self):
		# If "titles" is present in the folders dictionary and is not a single unit media item
		# And the watching status is not "Plan to watch" or "Completed"
		if (
			"titles" in self.dictionary["Media"]["Item"]["folders"] and
			self.dictionary["Media"]["details"][self.JSON.Language.language_texts["status, title()"]] not in [self.language_texts["plan_to_watch, title()"], self.JSON.Language.language_texts["completed, title()"]]
		):
			# Define the titles file to check its contents
			titles_file = self.dictionary["Media"]["Item"]["folders"]["titles"]["root"] + self.languages["full"]["en"] + ".txt"

			# If the titles file is empty
			if self.File.Contents(titles_file)["lines"] == []:
				# Iterate through the small languages list
				for language in self.languages["small"]:
					# Get the full language based on the small language
					full_language = self.languages["full"][language]

					# Define the language titles file
					titles_file = self.dictionary["Media"]["Item"]["folders"]["titles"]["root"] + full_language + ".txt"

					# Open it for user to fill it with titles
					self.File.Open(titles_file)

				# Wait for the user input (meaning the user finished filling the titles file)
				self.Input.Type(self.JSON.Language.language_texts["continue, title()"])

	def Add_Date(self):
		item_types = ["Media"]

		if self.dictionary["Media"]["States"]["Media item list"] == True:
			item_types.append("Item")

		# Iterate through the item_types list
		for item_type in item_types:
			media_dictionary = self.dictionary["Media"]

			if item_type == "Item":
				media_dictionary = self.dictionary["Media"]["Item"]

			# Get the details file and details for the media (item)
			self.date_dictionary = {
				"file": media_dictionary["folders"]["details"],
				"details": self.File.Dictionary(media_dictionary["folders"]["details"])
			}

			ask = False

			# If the "Year" key is in the details and is not "?" and the "Date" key is not in the details
			if (
				self.Date.language_texts["year, title()"] in self.date_dictionary["details"] and
				self.date_dictionary["details"][self.Date.language_texts["year, title()"]] != "?" and
				self.Date.language_texts["start_date"] not in self.date_dictionary["details"]
			):
				# Get the year from the details
				year = self.date_dictionary["details"][self.Date.language_texts["year, title()"]]

				# If the media has a media item list
				if media_dictionary["States"]["Media item list"] == True:
					# If the media title is equal to the media item title and the date is already present in the media details
					if self.dictionary["Media"]["Title"] == self.dictionary["Media"]["Item"]["Title"] and self.Date.language_texts["start_date"] in self.dictionary["Media"]["details"]:
						# Get the date from the media details
						date = self.dictionary["Media"]["details"][self.Date.language_texts["start_date"]]

						# Do not ask for the full date
						ask = False

					# If the media title is not equal to the media item title or the date is not present in the media details
					if item_type == "Item" and self.dictionary["Media"]["Title"] != self.dictionary["Media"]["Item"]["Title"] or self.Date.language_texts["start_date"] not in self.dictionary["Media"]["details"]:
						# Do ask for the full date
						ask = True

				# If the media has no media item list, ask for the full date
				if media_dictionary["States"]["Media item list"] == False:
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
						date = self.Input.Type(self.Date.language_texts["day, title()"] + " " + self.JSON.Language.language_texts["and"] + " " + self.Date.language_texts["month"]) + "/" + year

				# Add the "date" key and value after the "year" key
				key_value = {
					"key": self.Date.language_texts["start_date"],
					"value": date
				}

				self.date_dictionary["details"] = self.JSON.Add_Key_After_Key(self.date_dictionary["details"], key_value, self.Date.language_texts["year, title()"])

				# Update the media or media item details file
				self.File.Edit(self.date_dictionary["file"], self.Text.From_Dictionary(self.date_dictionary["details"]), "w")

			# If the "Year" key is not inside the media (item) details
			if self.Date.language_texts["year, title()"] not in self.date_dictionary["details"]:
				# Show the details file
				print(self.date_dictionary["file"])

				# Open it on the text editor
				self.File.Open(self.date_dictionary["file"], open = True)

				# And end the program execution
				quit()

	def Count_Comments_Number(self):
		# Get comments dictionary from file
		comments = self.JSON.To_Python(self.dictionary["Media"]["Item"]["folders"]["comments"]["comments"])

		# If the entries list is not empty
		if comments["Entries"] != []:
			# Iterate through the entries list
			for entry_name in comments["Entries"]:
				# Get the entry from the entries dictionary
				entry = comments["Dictionary"][entry_name]

				# If the "Time" key is inside the entry dictionary
				if "Time" in entry:
					# If the time is not empty
					if entry["Time"] != "":
						# If the time has more than the year
						if len(entry["Time"]) != 4:
							# Get the year from the time by converting the time into a date dictionary
							year = self.Date.From_String(entry["Time"])["year"]

						# If the time contains only the year
						if len(entry["Time"]) == 4:
							year = entry["Time"]

						# Add one to the comments number per year
						self.comments_number["Numbers"]["Years"][str(year)] += 1

						# Add one to the comments number per type per year
						self.comments_number["Numbers"]["Type"][self.dictionary["Media type"]["Plural"]["en"]]["Years"][str(year)] += 1

					# If the time is empty or the time contains only the year
					if entry["Time"] == "" or len(entry["Time"]) == 4:
						# Add one to the comments without time
						self.comments_number["Numbers"]["No time"] += 1

						# Add one to the comments without time per type
						self.comments_number["Numbers"]["Type"][self.dictionary["Media type"]["Plural"]["en"]]["No time"] += 1

					# Add one to the total comments number per type
					self.comments_number["Numbers"]["Total"] += 1

					# Add one to the total comments number per type
					self.comments_number["Numbers"]["Type"][self.dictionary["Media type"]["Plural"]["en"]]["Total"] += 1

	def Add_Last_Playlist_Date(self):
		if len(self.dictionary["Media"]["Item"]["Episodes"]["Titles"]["IDs"]) >= 1:
			id = self.dictionary["Media"]["Item"]["Episodes"]["Titles"]["IDs"][-1]

			dict_ = self.Get_YouTube_Information("video", id)

			video_title = self.dictionary["Media"]["Item"]["Episodes"]["Titles"][self.dictionary["Media"]["Language"]][-1]
			video_title_from_api = dict_["Title"]

			video_title_from_api = video_title_from_api.replace("  ", " ")

			if video_title_from_api != video_title:
				print()
				print(video_title)
				print(video_title_from_api)
				print(id)

		else:
			print("IDs file empty.")

	def Add_Anime_Information(self):
		item_types = ["Media"]

		if self.dictionary["Media"]["States"]["Media item list"] == True:
			item_types.append("Item")

		for item_type in item_types:
			media_dictionary = self.dictionary["Media"]

			if item_type == "Item":
				media_dictionary = self.dictionary["Media"]["Item"]

			if "Link" not in media_dictionary["details"]:
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
					self.dictionary["Media"]["States"]["Media item list"] == True and
					self.dictionary["Media"]["Item"]["Title"] != self.dictionary["Media"]["Title"] or

					# If media has media item list and the media item is not the same as the the root media
					self.dictionary["Media"]["States"]["Media item list"] == True and
					self.dictionary["Media"]["Item"]["Title"] == self.dictionary["Media"]["Title"] or

					# Or the media does not have a media item list and the media item is the same as the root media and the "ID" key is not present inside the media details
					self.dictionary["Media"]["States"]["Media item list"] == False and
					self.dictionary["Media"]["Item"]["Title"] == self.dictionary["Media"]["Title"] and
					"ID" not in self.dictionary["Media"]["details"]

				):
					# Open MyAnimeList search page with media (item) title parameter
					self.File.Open("https://myanimelist.net/search/all?q={}&cat=anime".format(title))

					print()
					print("\t\t" + media_dictionary["title"] + ":")

					# Ask for media (item) link
					link = self.Input.Type(self.JSON.Language.language_texts["{}_website_link"].format("MyAnimeList"))

					# Get ID from link
					id = link.split("/")[-2]

					# Get information from MyAnimeList using anime ID
					get_information_from_mal = True

				# If the media has a media item list and the media item is the same as the media and the "ID" key is present inside the media details
				if (
					self.dictionary["Media"]["Item"]["Title"] == self.dictionary["Media"]["Title"] and
					"ID" in self.dictionary["Media"]["details"]
				):
					# Get link and ID from media details
					link = self.dictionary["Media"]["details"]["Link"]
					id = self.dictionary["Media"]["details"]["ID"]

					# Get anime information from "Anime.json" file
					media_dictionary["Information"]["Dictionary"] = self.JSON.To_Python(self.dictionary["Media"]["folders"]["anime"])

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

				media_dictionary["details"] = self.JSON.Add_Key_After_Key(media_dictionary["details"], key_value, after_key = after_key)

				# Add the MyAnimeList Link after the "ID" key
				key_value = {
					"key": "Link",
					"value": link
				}

				media_dictionary["details"] = self.JSON.Add_Key_After_Key(media_dictionary["details"], key_value, after_key = "ID")

				if get_information_from_mal == True:
					# Get anime details
					media_dictionary["Information"]["Dictionary"] = self.API.Call("MyAnimeList", {"id": media_dictionary["details"]["ID"]})["response"]

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
					if len(media_dictionary["details"][self.Date.language_texts["start_date"]]) <= 10 and len(media_dictionary["Information"]["Dictionary"]["Broadcast"]["Time"]) == 5:
						media_dictionary["details"][self.Date.language_texts["start_date"]] = media_dictionary["Information"]["Broadcast"]["Time"] + " " + media_dictionary["details"][self.Date.language_texts["start_date"]]

				# Remove the "date" key of media (anime) details
				if self.Date.language_texts["date, title()"] in media_dictionary["details"]:
					media_dictionary["details"].pop(self.Date.language_texts["date, title()"])

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
							key_value["value"] = media_dictionary["Information"]["Dictionary"]["Dates"][key]["Date Time"]["HH:MM DD/MM/YYYY"]

					media_dictionary["details"] = self.JSON.Add_Key_After_Key(media_dictionary["details"], key_value, after_key = after_key)

				media_dictionary["details"] = self.JSON.Add_Key_After_Key(media_dictionary["details"], key_value, after_key = self.Date.language_texts["start_date"])

				# Add the episode duration after the "Episodes" key
				key_value = {
					"key": self.Date.language_texts["duration, title()"],
					"value": media_dictionary["Information"]["Dictionary"]["Duration"]["Text"][self.user_language]
				}

				if key_value["value"] == "":
					key_value["value"] = 0

				# Change duration key if episodes are more than one
				if media_dictionary["Information"]["Dictionary"]["Episodes"]["Number"] > 1:
					key_value["key"] = self.language_texts["episodes_duration"]

				media_dictionary["details"] = self.JSON.Add_Key_After_Key(media_dictionary["details"], key_value, after_key = self.language_texts["episodes, title()"])

				# Add "Studio(s)" key to media (item) details after the "Episodes duration" key
				key_value = {
					"key": self.Text.By_Number(media_dictionary["Information"]["Dictionary"]["Studios"], self.JSON.Language.language_texts["studio, title()"], self.JSON.Language.language_texts["studios, title()"]),
					"value": self.Text.From_List(media_dictionary["Information"]["Dictionary"]["Studios"], break_line = False, separator = ", ")
				}

				media_dictionary["details"] = self.JSON.Add_Key_After_Key(media_dictionary["details"], key_value, after_key = self.language_texts["episodes_duration"])

				if media_dictionary["Information"]["Dictionary"]["Links"]["Wikipedia"] != {}:
					# Add "Wikipedia" key to media (item) details after the "Link" key
					key_value = {
						"key": "Wikipedia",
						"value": ""
					}

					if self.user_language in media_dictionary["Information"]["Dictionary"]["Links"]["Wikipedia"]:
						key_value["value"] = media_dictionary["Information"]["Dictionary"]["Links"]["Wikipedia"][self.user_language]

					else:
						key_value["value"] = media_dictionary["Information"]["Dictionary"]["Links"]["Wikipedia"]["en"]

					media_dictionary["details"] = self.JSON.Add_Key_After_Key(media_dictionary["details"], key_value, after_key = self.JSON.Language.language_texts["link, title()"])

				# Update media (item) details file
				self.File.Edit(media_dictionary["folders"]["details"], self.Text.From_Dictionary(media_dictionary["details"]), "w")

				if media_dictionary["Information"]["Dictionary"]["Links"]["Wikipedia"]["Episode list"] == {}:
					media_dictionary["Information"]["Dictionary"]["Links"]["Wikipedia"].pop("Episode list")

				# Write anime details into media "[Anime]/[Season].json" file
				self.JSON.Edit(media_dictionary["folders"][media_dictionary["Information"]["Key"]], media_dictionary["Information"]["Dictionary"])

	def Format_Anime_Information(self, media_dictionary, information):
		new_information = {
			"Title": "",
			"Titles": {},
			"ID": "",
			"Link": media_dictionary["details"]["Link"],
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

		for title in media_dictionary["titles"]:
			if key not in ["Language", "Sanitized"]:
				new_information["Titles"][key] = media_dictionary["titles"][key]

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

		# Get episode titles
		if "titles" in self.dictionary["Media"]["Item"]["Episodes"]:
			new_information["Episodes"]["Titles"] = self.dictionary["Media"]["Item"]["Episodes"]["Titles"]

			if "files" in new_information["Episodes"]["Titles"]:
				new_information["Episodes"]["Titles"].pop("files")

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
			for language in self.languages["small"]:
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
				for language in self.languages["small"]:
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
							"DD/MM/YYYY": self.Date.From_String(date)["DD/MM/YYYY"]
						},
						"Time": {},
						"Date Time": {},
						"Year": self.Date.From_String(date)["year"]
					}

			new_information["Time"] = self.Date.To_String(self.Date.From_String(information["start_date"])["date"])

		else:
			if "Dates" in information:
				new_information["Dates"] = information["Dates"]

			if "Time" in information:
				new_information["Time"] = information["Time"]

			elif new_information["Dates"]["Start"] != {} and new_information["Dates"]["Start"]["Date Time"] != {}:
				new_information["Time"] = new_information["Dates"]["Start"]["Date Time"]["YYYY-MM-DDTHH:MM:SSZ"]

			if "Date Time" in new_information["Dates"]["Start"] and new_information["Dates"]["Start"]["Date Time"] == {}:
				new_information["Time"] = self.Date.To_String(self.Date.From_String(new_information["Dates"]["Start"]["Date"]["YYYY-MM-DD"])["date"])

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
					"HH:MM DD/MM/YYYY": information["broadcast"]["start_time"] + " " + self.Date.From_String(date)["DD/MM/YYYY"]
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

		if self.dictionary["Media"]["States"]["Media item list"] == True:
			item_types.append("Item")

		for item_type in item_types:
			media_dictionary = self.dictionary["Media"]

			if item_type == "Item":
				media_dictionary = self.dictionary["Media"]["Item"]

			if self.File.Contents(media_dictionary["folders"][media_dictionary["Information"]["Key"]])["lines"] == []:
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
				self.File.Edit(media_dictionary["folders"]["details"], self.Text.From_Dictionary(media_dictionary["details"]), "w")

				# Write media details into media "[Information file name].json" file
				self.JSON.Edit(media_dictionary["folders"][media_dictionary["Information"]["Key"]], media_dictionary["Information"]["Dictionary"])

		# --- Videos --- #
		# To-Do: Add title and titles to "Channel.json" and "Playlist.json"
		# Add links and dates dictionaries
		# Add episodes and episode titles, pictures, (media items), original language, and country of origin
		# -------------- #

	def Paste_Links(self, media_dictionary):
		links = {
			"Official": {
				"Link": self.JSON.Language.language_texts["official_website"],
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
					if language in self.languages["full_translated"][language]:
						# Get transtaled language
						translated_full_language = self.languages["full_translated"][language][self.user_language]

					else:
						translated_full_language = language

					if "Gender" not in link:
						link["Gender"] = "masculine"

					# Define of and in texts
					of_text = self.JSON.Language.texts["genders, type: dict"][self.user_language][link["Gender"]]["of"]
					in_text = self.JSON.Language.texts["genders, type: dict"][self.user_language][link["Gender"]]["in"]

					# Define text to show when asking for user to paste the website link
					text = self.JSON.Language.language_texts["{}_website_link"].format(in_text + " " + translated_full_language + " " + of_text + " " + link_key)

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
						text = self.JSON.Language.language_texts["{}_website_link"].format(of_text + " " + self.language_texts["episode_list"].lower() + " " + in_text + " " + translated_full_language + " " + of_text + " " + link_key)

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
			media_dictionary["Information"]["Dictionary"]["Links"]["YouTube"]["ID"] = media_dictionary["details"]["ID"]

			media_dictionary["Information"]["Dictionary"]["Links"]["Official"] = media_dictionary["Information"]["Dictionary"]["Links"]["YouTube"]

	def Format_Media_Information(self, media_dictionary, information):
		new_information = {
			"Title": "",
			"Titles": {},
			"ID": "", # For anime, videos

			# Anime: MyAnimeList
			# Cartoons, series, and movies: English Wikipedia
			# Videos: YouTube
			"Link": media_dictionary["details"]["Link"],

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
		for title in media_dictionary["titles"]:
			if key not in ["Language", "Sanitized"]:
				new_information["Titles"][key] = media_dictionary["titles"][key]

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

	def Replace_Year_Number(self, folders, to_replace, replace_with):
		for key, value in folders.items():
			value = folders[key]

			if type(value) == str:
				folders[key] = folders[key].replace(to_replace, replace_with)

			if type(value) == dict:
				self.Replace_Year_Number(value, to_replace, replace_with)

	def Convert_History(self):
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

		self.years_list = range(2018, self.date["year"] + 1)

		# Iterate through years list (of years that contain a "Watch_History" folder)
		for self.year in self.years_list:
			# Convert the year number into a string
			self.year = str(self.year)

			# Define year dictionary with year number and folders
			self.year = {
				"Number": self.year,
				"folders": {
					"root": self.folders["watch_history"]["root"] + self.year + "/",
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
				# Add to total and comments numbers
				self.year["Entries dictionary"]["Numbers"]["Total"] = len(self.year["Lists"]["Episodes"])
				self.year["Entries dictionary"]["Numbers"]["Comments"] = self.dictionaries["Root comments"]["Numbers"]["Years"][self.year["Number"]]

				# Define the media type dictionaries
				self.media_type_dictionaries = {}

				# Iterate through the English plural media types
				for plural_media_type in self.media_types["Plural"]["en"]:
					# Create media type dictionary with media number and media item list (with all media titles)
					self.media_type_dictionaries[plural_media_type] = {
						"Number": 1,
						"Media list": self.Get_Media_List(self.media_types[plural_media_type], self.texts["watching_statuses, type: list"]["en"])
					}

				remove_list = self.File.Contents(self.Folder.folders["apps"]["root"] + "Test.txt")["lines"]

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
						"Time": self.year["Lists"]["Times"][e]
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
					self.Date.language_texts["time, title()"] + ":" + "\n" + \
					"[" + entry["Time"] + "]" + "\n" + \
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

									self.Replace_Year_Number(self.dictionary["Media type"]["Folders"]["per_media_type"], str(self.date["year"]), self.year["Number"])

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
							if entry["Time"] != "Unknown Watched Time - Horário Assistido Desconhecido":
								entry["Time"] = self.Date.To_UTC(self.Date.From_String(entry["Time"], "%H:%M %d/%m/%Y"))

							# Define the "Comment Writer" dictionary
							self.dictionary["Comment Writer"] = {
								"States": {
									"write": False
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
							if self.language_texts["dubbed, title()"] in entry["Episode title"]:
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

								# Remove Comment dictionary from Entry dictionary if the time is empty and the "ID" key is not inside the Comment dictionary
								# The Comment dictionary is only useful to be inside the Entry dictionary if it contains the time of the comment and/or the ID and Link of the comment
								if entry["Comment"]["Time"] == "" and "ID" not in entry["Comment"]:
									entry.pop("Comment")

								if list(entry["Comment"].keys()) == ["Time"] and entry["Comment"]["Time"] == entry["Time"]:
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

							# If the "12-25" text is inside the UTC time string (12 = month, 25 = day, Christmas day)
							if "12-25" in entry["Time"]["%H:%M %d/%m/%Y"] or "25/12" in entry["Time"]["%H:%M %d/%m/%Y"]:
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
									"Time": entry["Time"]
								}
							})

							if self.dictionary["Entry"]["Time"] == "Unknown Watched Time - Horário Assistido Desconhecido":
								self.dictionary["Entry"]["Time"] = {}

							# Add Comment dictionary to "Comment Writer" dictionary
							if "Comment" in entry:
								self.dictionary["Comment Writer"]["Comment"] = entry["Comment"]

							# Add the "Old history" dictionary to add the year folder
							self.dictionary["Old history"].update({
								"Episode title": self.media["Episode"]["Titles"][self.user_language]
							})

							if "re_watched" in self.dictionary["Media"]["Episode"]:
								self.dictionary["Old history"]["re_watched"] = self.dictionary["Media"]["Episode"]["re_watched"]

							for dictionary_name in ["Entries", "Media Type"]:
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

							for dictionary_name in ["Entries", "Media Type"]:
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

	def Add_To_Comments_Dictionary(self):
		options = {
			"Media type": {
				"Status": self.texts["watching_statuses, type: list"]["en"],

				# Remove the "Movies" media type from the media type dictionary, returning a local media types dictionary
				"List": self.Remove_Media_Type(self.texts["movies, title()"]["en"])
			}
		}

		self.dictionary = self.Select_Media_Type_And_Media(options, watch = True)

		import importlib

		classes = [
			"Watch_Media",
			"Comment_Writer"
		]

		for title in classes:
			class_ = getattr(importlib.import_module("."  + title, "Watch_History"), title)
			setattr(self, title, class_)

		# Define media dictionary with already selected media type and media
		self.dictionary = self.Watch_Media(self.dictionary, open_media = False).media_dictionary

		# Comment on media without having to register the watched media unit (episode, video, or movie)
		self.Comment_Writer(self.dictionary, write_comment = True)