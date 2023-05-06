# Register.py

from Watch_History.Watch_History import Watch_History as Watch_History

class Register(Watch_History):
	def __init__(self, dictionary = {}):
		super().__init__()

		self.dictionary = dictionary

		# Ask for the entry information
		if self.dictionary == {}:
			self.Type_Entry_Information()

		self.dictionary["Entry"].update({
			"Dates": {
				"UTC": self.dictionary["Entry"]["Date"]["UTC"]["DateTime"]["Formats"]["YYYY-MM-DDTHH:MM:SSZ"],
				"Timezone": self.dictionary["Entry"]["Date"]["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"]
			},
			"Diary Slim": {
				"Text": "",
				"Clean text": ""
			},
			"States": {
				"Post on the Social Networks": False
			}
		})

		# Define the media variable to make typing the media dictionary easier
		self.media = self.dictionary["Media"]

		self.Check_Media_Status()

		if self.media["States"]["Re-watching"] == False:
			if self.media["States"]["Completed media"] == True or self.media["States"]["Completed media item"] == True:
				self.Check_Media_Dates()

		# Database related methods
		self.Register_In_JSON()
		self.Create_Entry_File()
		self.Add_Entry_File_To_Year_Folder()

		self.Define_Diary_Slim_Text()

		self.Post_On_Social_Networks()

		self.Write_On_Diary_Slim()

		self.Show_Information()

	def Type_Entry_Information(self):
		# To-Do: Make this method
		pass

	def Register_In_JSON(self):
		self.media_type = self.dictionary["Media type"]["Plural"]["en"]

		# Re-read the "Watched" file to get the most updated data
		self.dictionaries["Watched"] = self.JSON.To_Python(self.media["Item"]["folders"]["watched"]["entries"])

		# Re-read the "Entries" file to get the most updated data
		self.dictionaries["Entries"] = self.JSON.To_Python(self.folders["watch_history"]["current_year"]["entries"])

		dicts = [
			self.dictionaries["Entries"],
			self.dictionaries["Media type"][self.media_type],
			self.dictionaries["Watched"]
		]

		# Add one to the entry, media type entry, and root media type entry numbers
		for dict_ in dicts:
			dict_["Numbers"]["Total"] += 1

			if "Per Media Type" in dict_["Numbers"]:
				dict_["Numbers"]["Per Media Type"][self.media_type] += 1

		# Define sanitized version of entry name for files
		self.dictionary["Entry"]["Name"] = {
			"Normal": str(self.dictionaries["Entries"]["Numbers"]["Total"]) + ". " + self.media_type + " (" + self.dictionary["Entry"]["Dates"]["Timezone"] + ")",
			"Sanitized": ""
		}

		self.dictionary["Entry"]["Name"]["Sanitized"] = self.dictionary["Entry"]["Name"]["Normal"].replace(":", ";").replace("/", "-")

		# Add to the "Entries" lists
		for dict_ in dicts:
			if self.dictionary["Entry"]["Name"]["Normal"] not in dict_["Entries"]:
				dict_["Entries"].append(self.dictionary["Entry"]["Name"]["Normal"])

		# Update the number of Entries of all dictionaries using the length of the Entries list
		for dict_ in dicts:
			dict_["Numbers"]["Total"] = len(dict_["Entries"])

		# Define local media and media item titles to remove some keys from them
		media_titles = self.media["Titles"].copy()
		item_titles = self.media["Item"]["Titles"].copy()

		for dict_ in [media_titles, item_titles]:
			dict_.pop("Language")

			for key in ["ja", "Sanitized"]:
				if key in dict_:
					dict_.pop(key)

			for language in self.languages["small"]:
				if language in dict_:
					if dict_["Original"] == dict_[language] or "Romanized" in dict_ and dict_["Romanized"] == dict_[language]:
						dict_.pop(language)

		self.key = self.dictionary["Entry"]["Name"]["Normal"]

		# Add the "Entry" dictionary to the "Entries" dictionary
		self.dictionaries["Entries"]["Dictionary"][self.key] = {
			"Number": self.dictionaries["Entries"]["Numbers"]["Total"],
			"Type number": self.dictionaries["Media type"][self.media_type]["Numbers"]["Total"],
			"Entry": self.dictionary["Entry"]["Name"]["Normal"],
			"Media": media_titles,
			"Item": item_titles,
			"Episode": {
				"Number": 1,
				"Titles": self.media["Episode"]["Titles"]
			},
			"Type": self.media_type,
			"Date": self.dictionary["Entry"]["Dates"]["UTC"]
		}

		# Remove the media item dictionary if the media has not media item list, the media item title is the same as the media title, or the media is non-series media
		if self.media["States"]["Media item list"] == False or self.media["Item"]["Title"] == self.media["Title"] or self.media["States"]["Series media"] == False:
			self.dictionaries["Entries"]["Dictionary"][self.key].pop("Item")

		# Remove episode titles and number keys of dictionary if media is non-series media or single unit
		if self.media["States"]["Series media"] == False or self.media["States"]["Single unit"] == True:
			self.dictionaries["Entries"]["Dictionary"][self.key].pop("Episode")

		# Define episode number on dictionary if media is series media and not single unit and is episodic
		if self.media["States"]["Series media"] == True and self.media["States"]["Single unit"] == False and self.media["States"]["Episodic"] == True:
			self.dictionaries["Entries"]["Dictionary"][self.key]["Episode"]["Number"] = self.media["Episode"]["Number"]

		# Remove "Number" key from Episode dictionary is the media is non-episodic
		if "Episode" in self.dictionaries["Entries"]["Dictionary"][self.key] and self.media["States"]["Episodic"] == False:
			self.dictionaries["Entries"]["Dictionary"][self.key]["Episode"].pop("Number")

		# Add episode ID if the key is present inside the episode dictionary
		if "ID" in self.media["Episode"]:
			self.dictionaries["Entries"]["Dictionary"][self.key]["ID"] = self.media["Episode"]["ID"]

			# Add episode link
			if "remote" in self.media["Episode"]:
				self.dictionaries["Entries"]["Dictionary"][self.key]["Link"] = self.media["Episode"]["Remote"]["Link"]

		# Add the "Comment" dictionary if it exists
		if "Comment" in self.dictionary["Comment Writer"]:
			self.dictionaries["Entries"]["Dictionary"][self.key]["Comment"] = self.dictionary["Comment Writer"]["Comment"]

			if list(self.dictionaries["Entries"]["Dictionary"][self.key]["Comment"].keys()) == ["Date"] and self.dictionaries["Entries"]["Dictionary"][self.key]["Comment"]["Date"] == self.dictionaries["Entries"]["Dictionary"][self.key]["Date"]:
				self.dictionaries["Entries"]["Dictionary"][self.key].pop("Comment")

		# Get the States dictionary
		self.dictionary["States"] = self.Define_States_Dictionary(self.dictionary)

		# Add the States dictionary into the Entry dictionary if it is not empty
		if self.dictionary["States"]["States"] != {}:
			self.dictionaries["Entries"]["Dictionary"][self.key]["States"] = self.dictionary["States"]["States"]

		# Add entry dictionary to media type and Watched entry dictionaries
		for dict_ in dicts:
			if dict_ != self.dictionaries["Entries"]:
				dict_["Dictionary"][self.key] = self.dictionaries["Entries"]["Dictionary"][self.key].copy()

		# Get the "Comments" dictionary from the file
		self.dictionaries["Comments"] = self.JSON.To_Python(self.folders["comments"]["comments"])

		# Get the year comment number from the "Comments.json" file
		self.dictionaries["Entries"]["Numbers"]["Comments"] = self.dictionaries["Comments"]["Numbers"]["Years"][self.current_year["Number"]]

		# Get the year media type comment number from the "Comments.json" file
		self.dictionaries["Media type"][self.media_type]["Numbers"]["Comments"] = self.dictionaries["Comments"]["Numbers"]["Type"][self.media_type]["Years"][self.current_year["Number"]]

		# Add to the media "Watched" comments number
		if self.dictionary["Comment Writer"]["States"]["Write"] == True:
			self.dictionaries["Watched"]["Numbers"]["Comments"] += 1

		# Update the "Entries.json" file
		self.JSON.Edit(self.folders["watch_history"]["current_year"]["entries"], self.dictionaries["Entries"])

		# Update the media type "Entries.json" file
		self.JSON.Edit(self.dictionary["Media type"]["Folders"]["per_media_type"]["entries"], self.dictionaries["Media type"][self.media_type])

		# Update the media "Watched.json" file
		self.JSON.Edit(self.media["Item"]["folders"]["watched"]["entries"], self.dictionaries["Watched"])

		# Add to the "Entry list.txt" files
		if self.dictionary["Entry"]["Name"]["Normal"] not in self.File.Contents(self.folders["watch_history"]["current_year"]["entry_list"])["lines"]:
			self.File.Edit(self.folders["watch_history"]["current_year"]["entry_list"], self.dictionary["Entry"]["Name"]["Normal"], "a")

		if self.dictionary["Entry"]["Name"]["Normal"] not in self.File.Contents(self.dictionary["Media type"]["Folders"]["per_media_type"]["entry_list"])["lines"]:
			self.File.Edit(self.dictionary["Media type"]["Folders"]["per_media_type"]["entry_list"], self.dictionary["Entry"]["Name"]["Normal"], "a")

		if self.dictionary["Entry"]["Name"]["Normal"] not in self.File.Contents(self.media["Item"]["folders"]["watched"]["entry_list"])["lines"]:
			self.File.Edit(self.media["Item"]["folders"]["watched"]["entry_list"], self.dictionary["Entry"]["Name"]["Normal"], "a")

	def Create_Entry_File(self):
		# Number: [Episode number]
		# Type number: [Type number]
		# 
		# Media:
		# [Media titles]
		# (
		# Item:
		# [Item titles]
		# 
		# Titles:
		# [Episode titles]
		# )
		# Type:
		# [Media type]
		#
		# Dates:
		# [Entry dates]
		# 
		# File name:
		# [Number. Type (Time)]

		# Define the entry file
		folder = self.dictionary["Media type"]["Folders"]["per_media_type"]["files"]["root"]
		file = folder + self.dictionary["Entry"]["Name"]["Sanitized"] + ".txt"
		self.File.Create(file)

		self.dictionary["Entry"]["Text"] = {
			"General": self.Define_File_Text("General")
		}

		for language in self.languages["small"]:
			self.dictionary["Entry"]["Text"][language] = self.Define_File_Text(language)

		# Write the entry text into the entry file
		self.File.Edit(file, self.dictionary["Entry"]["Text"]["General"], "w")

		# Write the entry text into the "Watched" entry file
		file = self.media["Item"]["folders"]["watched"]["files"]["root"] + self.dictionary["Entry"]["Name"]["Sanitized"] + ".txt"

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
			self.texts["media_type_number"][language] + ": " + str(self.dictionaries["Media type"][self.media_type]["Numbers"]["Total"]),
			"\n" + self.JSON.Language.texts["media, title()"][language] + ":" + "\n" + "{}"
		]

		# Add item and episode titles lines
		if self.media["States"]["Series media"] == True:
			if self.media["States"]["Media item list"] == True and self.media["Item"]["Title"] != self.media["Title"]:
				lines.append(self.texts["item, title()"][language] + ":" + "\n" + "{}")

			if self.media["States"]["Single unit"] == False:
				text = self.JSON.Language.texts["titles, title()"][language]

				if language_parameter != "General":
					text = self.JSON.Language.texts["title, title()"][language]

				list_ = []

				for title in list(self.media["Episode"]["Titles"].values()):
					if title not in list_:
						list_.append(title)

				if len(list_) == 1:
					text = self.JSON.Language.texts["title, title()"][language]

				lines.append(text + ":" + "\n" + "{}")

		lines_to_add = [
			self.JSON.Language.texts["type, title()"][language] + ":" + "\n" + self.dictionary["Media type"]["Plural"][language] + "\n"
		]

		text = self.Date.texts["times, title()"][language] + ":" + "\n" + "{}"

		if self.dictionary["Entry"]["Dates"]["UTC"] == self.dictionary["Entry"]["Dates"]["Timezone"]:
			text = self.Date.texts["time, title()"][language] + ":" + "\n" + "{}"

		lines_to_add.append(text)

		lines_to_add.append(self.File.texts["file_name"][language] + ":" + "\n" + self.dictionary["Entry"]["Name"]["Normal"])

		lines.extend(lines_to_add)

		# Add states texts lines
		if self.dictionary["States"]["Texts"] != {}:
			text = "\n" + self.JSON.Language.texts["states, title()"][language] + ":" + "\n"

			for key in self.dictionary["States"]["Texts"]:
				language_text = self.dictionary["States"]["Texts"][key][language]

				text += language_text

				if key != list(self.dictionary["States"]["Texts"].keys())[-1]:
					text += "\n"

			lines.append(text)

		# Define language entry text
		file_text = self.Text.From_List(lines)

		# Define items to be added to entry text
		items = []

		titles = ""

		# Add media titles to items list
		key = "Original"

		if "Romanized" in self.media["Titles"]:
			key = "Romanized"

		titles += self.media["Titles"][key]

		if self.media["Titles"]["Language"] != self.media["Titles"][key]:
			titles += "\n" + self.media["Titles"]["Language"]

		items.append(titles + "\n")

		if self.media["States"]["Series media"] == True:
			# Add media item titles to media item titles list
			if self.media["States"]["Media item list"] == True and self.media["Item"]["Title"] != self.media["Title"]:
				key = "Original"

				if "Romanized" in self.media["Item"]["Titles"]:
					key = "Romanized"

				item_titles = self.media["Item"]["Titles"][key]

				if self.media["Item"]["Titles"]["Language"] != self.media["Item"]["Titles"][key]:
					item_titles += "\n" + self.media["Item"]["Titles"]["Language"]

				items.append(item_titles + "\n")

			if self.media["States"]["Single unit"] == False:
				# Add episode titles to episode titles list
				episode_titles = ""

				if language_parameter != "General":
					episode_title = self.media["Episode"]["Titles"][language]

					if episode_title == "":
						episode_title = "[" + self.JSON.Language.texts["empty, title()"][language] + "]"

					episode_titles = episode_title + "\n"

				if language_parameter == "General":
					for language in self.languages["small"]:
						episode_title = self.media["Episode"]["Titles"][language]

						if episode_title == "":
							episode_title = "[" + self.JSON.Language.texts["empty, title()"][language] + "]"

						if episode_title + "\n" not in episode_titles:
							episode_titles += episode_title + "\n"

				items.append(episode_titles)

		# Add the times to the items list
		times = ""

		for key in ["UTC", "Timezone"]:
			if key in self.dictionary["Entry"]["Dates"]:
				time = self.dictionary["Entry"]["Dates"][key]

				if time + "\n" not in times:
					times += time + "\n"

		items.append(times)

		return file_text.format(*items)

	def Add_Entry_File_To_Year_Folder(self):
		# Create folders
		for language in self.languages["small"]:
			full_language = self.languages["full"][language]

			# Folder names
			root_folder = self.texts["watched_media"][language]
			type_folder = self.dictionary["Media type"]["Plural"][language]

			# Watched media folder
			folder = self.current_year["folders"][full_language]["root"]
			self.Folder.Create(folder)

			self.current_year["folders"][full_language][root_folder] = {
				"root": folder + root_folder + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][root_folder]["root"])

			# Media type folder
			folder = self.current_year["folders"][full_language][root_folder]["root"]
			self.Folder.Create(folder)

			self.current_year["folders"][full_language][root_folder][type_folder] = {
				"root": folder + type_folder + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][root_folder][type_folder]["root"])

			# Watched media file
			folder = self.current_year["folders"][full_language][root_folder][type_folder]["root"]
			file_name = self.dictionary["Entry"]["Name"]["Sanitized"]
			self.current_year["folders"][full_language][root_folder][type_folder][file_name] = folder + file_name + ".txt"

			self.File.Create(self.current_year["folders"][full_language][root_folder][type_folder][file_name])

			self.File.Edit(self.current_year["folders"][full_language][root_folder][type_folder][file_name], self.dictionary["Entry"]["Text"][language], "w")

			# Firsts Of The Year subfolder folder
			firsts_of_the_year_text = self.JSON.Language.texts["firsts_of_the_year"][language]
			subfolder_name = self.JSON.Language.texts["media, title()"][language]

			folder = self.current_year["folders"][full_language][firsts_of_the_year_text]["root"]
			self.Folder.Create(folder)

			self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name] = {
				"root": folder + subfolder_name + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name]["root"])

			# Firsts Of The Year media type folder
			folder = self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name]["root"]
			self.Folder.Create(folder)

			type_folder = self.dictionary["Media type"]["Singular"][language]

			self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder] = {
				"root": folder + type_folder + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder]["root"])

			# First media type entry in year file
			if self.media["States"]["First media type entry in year"] == True:
				folder = self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder]["root"]
				self.Folder.Create(folder)

				self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name] = folder + file_name + ".txt"
				self.File.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name])

				self.File.Edit(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name], self.dictionary["Entry"]["Text"][language], "w")

	def Check_Media_Status(self):
		if self.media["States"]["Series media"] == True:
			# If the media has a media item list and the episode title is the last one
			if self.media["States"]["Media item list"] == True and self.media["Episode"]["Title"] == self.media["Item"]["Episodes"]["Titles"][self.media["Language"]][-1]:
				# And the media is not a YouTube channel
				if self.media["States"]["Video"] == False:
					# If the media item is the last media item, define the media as completed
					if self.media["Item"]["Title"] == self.media["Items"]["List"][-1]:
						self.media["States"]["Completed media"] = True

					# If the media item is not the last media item (media is not completed), get next media item
					if self.media["Item"]["Title"] != self.media["Items"]["List"][-1]:
						item_title = self.media["Items"]["List"][self.media["Item"]["Number"] + 1]

						sanitized_title = self.Sanitize_Title(item_title)

						# Define the next media item prototype dictionary
						self.media["Item"]["Next"] = {
							"Title": item_title,
							"Titles": {},
							"Sanitized": sanitized_title,
							"folders": {
								"root": self.media["Items"]["folders"]["root"] + sanitized_title + "/",
								"media": {
									"root": self.media["folders"]["media"]["root"] + sanitized_title + "/"
								}
							},
							"Number": self.media["Item"]["Number"] + 1
						}

						from copy import deepcopy

						# Define other variables for the next media item
						self.media["Item"]["Next"] = self.Define_Media_Item(deepcopy(self.dictionary), media_item = item_title)["Media"]["Item"]

						# Update current media item file
						self.File.Edit(self.media["Items"]["folders"]["current"], self.media["Item"]["Next"]["Title"], "w")

				# Add the "Status" key and value "Completed" to the end of the details
				key_value = {
					"key": self.JSON.Language.language_texts["status, title()"],
					"value": self.JSON.Language.language_texts["completed, title()"]
				}

				if self.media["States"]["Video"] == False:
					self.media["Item"]["details"] = self.JSON.Add_Key_After_Key(self.media["Item"]["details"], key_value, add_to_end = True)

				if self.language_texts["episode, title()"] in self.media["Item"]["details"] and self.media["States"]["Single unit"] == True:
					self.media["Item"]["details"].pop(self.language_texts["episode, title()"])

				# Update the media item details file
				self.File.Edit(self.media["Item"]["folders"]["details"], self.Text.From_Dictionary(self.media["Item"]["details"]), "w")

				if self.media["States"]["Video"] == False:
					self.media["States"]["Completed media item"] = True

			# If the media has no media item list and the episode title is the last one, define the media as completed
			if self.media["States"]["Media item list"] == False and self.media["Episode"]["Title"] == self.media["Item"]["Episodes"]["Titles"][self.media["Language"]][-1] and self.media["States"]["Video"] == False:
				self.media["States"]["Completed media"] = True

		# If the media is a movie, define it as completed
		if self.media["States"]["Series media"] == False:
			self.media["States"]["Completed media"] = True

		# If the media and media item are not completed, get next episode number
		if self.media["States"]["Completed media"] == False and self.media["States"]["Completed media item"] == False and len(self.media["Item"]["Episodes"]["Titles"][self.media["Language"]]) != 1:
			try:
				# Get next episode language title
				self.media["Episode"]["Next"] = self.media["Item"]["Episodes"]["Titles"][self.media["Language"]][self.media["Episode"]["Number"]]

				# Define current episode to watch as the next episode
				self.media["Item"]["details"][self.language_texts["episode, title()"]] = self.media["Episode"]["Next"]

				# Update media item details file
				self.File.Edit(self.media["Item"]["folders"]["details"], self.Text.From_Dictionary(self.media["Item"]["details"]), "w")

			except IndexError:
				pass

		# If the media is completed, define its status as completed
		if self.media["States"]["Completed media"] == True:
			if self.language_texts["remote_origin, title()"] in self.media["details"]:
				if self.media["details"][self.language_texts["remote_origin, title()"]] == "Animes Vision":
					self.media["details"].pop(self.language_texts["remote_origin, title()"])

				elif self.media["details"][self.language_texts["remote_origin, title()"]] == "YouTube":
					self.media["details"].pop(self.language_texts["remote_origin, title()"])

			# Update the status key in the media details
			self.Change_Status(self.dictionary)

		# Check if media item has a correspondent movie inside the movies folder
		if self.media["States"]["Series media"] == True and "Type" in self.media["Item"] and self.media["Item"]["Type"][self.user_language] == self.language_texts["movie"]:
			self.movies = self.Get_Media_List(self.media_types[self.texts["movies, title()"]["en"]], self.texts["plan_to_watch, title()"]["en"])

			for movie_title in self.movies:
				# If the media item title is inside the movies list and the media type is not "Movies"
				if self.media["Item"]["Title"] in movie_title:
					# Define the movie prototype dictionary
					self.movie_dictionary = {
						"Media type": self.media_types[self.texts["movies, title()"]["en"]],
						"Media": {
							"Title": movie_title
						}
					}

					# Define other variables for the movie
					self.movie_dictionary = self.Select_Media(self.movie_dictionary)

					# Copy the contents of the media comments folder to the movie comments folder
					self.Folder.Copy(self.media["Item"]["folders"]["comments"]["root"], self.movie_dictionary["Media"]["Item"]["folders"]["comments"]["root"])

					# Change the status of the movie to "Completed"
					self.Change_Status(self.movie_dictionary)

		# If the media is non-series media
		if self.media["States"]["Series media"] == False:
			# Define the empty series media list
			self.series_media_list = {}

			# Define the list of media types to not get a media list
			remove_list = [
				self.texts["movies, title()"]["en"],
				self.texts["videos, title()"]["en"]
			]

			# Define the status list to use to get the media with the statuses on the list
			status_list = [
				self.texts["watching, title()"]["en"],
				self.texts["re_watching, title()"]["en"],
				self.JSON.Language.texts["on_hold, title()"]["en"]
			]

			# Iterate through the English plural media types list
			for plural_media_type in self.media_types["Plural"]["en"]:
				if plural_media_type not in remove_list:
					media_list = self.Get_Media_List(self.media_types[plural_media_type], status_list)

					# Extend the series media list with the current media list
					self.series_media_list[plural_media_type] = media_list

			from copy import deepcopy

			# Iterate through the English plural media types list
			for plural_media_type in self.media_types["Plural"]["en"]:
				if plural_media_type in self.series_media_list:
					# Get the media list of the current media type
					media_list = self.series_media_list[plural_media_type]

					# Iterate through the media list
					for media_title in media_list:
						media_folder = self.media_types[plural_media_type]["folders"]["media_info"]["root"] + self.Sanitize_Title(media_title) + "/"

						media_items_folder = media_folder + self.media_types[plural_media_type]["subfolders"]["plural"] + "/"

						# If the media items folder exists
						if self.Folder.Exist(media_items_folder) == True:
							media_items_file = media_items_folder + self.media_types[plural_media_type]["subfolders"]["plural"] + ".txt"

							# Get the media items list
							media_items = self.File.Contents(media_items_file)["lines"]

							# Iterate through the media items list
							for item_title in media_items:
								item_folder = media_items_folder + self.Sanitize_Title(item_title) + "/"
								item_details_file = item_folder + self.JSON.Language.language_texts["details, title()"] + ".txt"

								item_details = self.File.Dictionary(item_details_file)

								# If the media item title is equal to the root media item title (the one that was watched)
								# Or is inside the item title and the year of the movie is the same as the year of the item
								if (
									item_title == self.media["Item"]["Title"] or
									self.media["Item"]["Title"].split(" (")[0] in item_title and self.media["Item"]["details"][self.Date.language_texts["year, title()"]] == item_details[self.Date.language_texts["year, title()"]]
								):
									# Define the media prototype dictionary
									media_dictionary = {
										"Media type": self.media_types[plural_media_type],
										"Media": {
											"Title": media_title
										}
									}

									# Define other variables for the media
									media_dictionary = self.Select_Media(media_dictionary)

									# Define the media item as the current media item
									media_dictionary["Media"]["Item"] = self.Define_Media_Item(deepcopy(media_dictionary), media_item = item_title)["Media"]["Item"]

									# Add the "Status" key and value "Completed" to the end of the details
									key_value = {
										"key": self.JSON.Language.language_texts["status, title()"],
										"value": self.JSON.Language.language_texts["completed, title()"]
									}

									media_dictionary["Media"]["Item"]["details"] = self.JSON.Add_Key_After_Key(media_dictionary["Media"]["Item"]["details"], key_value, add_to_end = True)

									# Update the media item details file
									self.File.Edit(media_dictionary["Media"]["Item"]["folders"]["details"], self.Text.From_Dictionary(media_dictionary["Media"]["Item"]["details"]), "w")

	def Check_Media_Dates(self):
		# Completed media and media item time and date template
		template = self.language_texts["when_i_finished_watching"] + ":" + "\n" + \
		self.dictionary["Entry"]["Dates"]["Timezone"] + "\n" + \
		"\n" + \
		self.Date.language_texts["duration, title()"] + ":" + "\n" + \
		"{}"

		# Gets the date that the user started and finished watching the media item and writes it into the media item dates file
		if self.media["States"]["Completed media item"] == True:
			# Gets the item dates from the item dates file
			self.media["Item"]["dates"] = self.File.Dictionary(self.media["Item"]["folders"]["dates"], next_line = True)

			key = self.language_texts["when_i_started_to_watch"]

			if self.media["States"]["Single unit"] == True:
				self.media["Item"]["dates"][key] = self.dictionary["Entry"]["Dates"]["Timezone"]

			# Get started watching time
			self.media["Item"]["started_watching_item"] = self.Date.To_UTC(self.Date.From_String(self.media["Item"]["dates"][key]))

			# Define time spent watching using started watching time and finished watching time
			self.media["Item"]["Time spent watching"] = self.Date.Difference(self.media["Item"]["started_watching_item"], self.dictionary["Entry"]["Date"]["UTC"]["Object"])["Text"][self.user_language]

			if self.media["Item"]["Time spent watching"][0] + self.media["Item"]["Time spent watching"][1] == ", ":
				self.media["Item"]["Time spent watching"] = self.media["Item"]["Time spent watching"][2:]

			# Format the time template
			self.media["Item"]["Formatted datetime template"] = "\n\n" + template.format(self.media["Item"]["Time spent watching"])

			# Read the media item dates file
			self.media["Item"]["Finished watching text"] = self.File.Contents(self.media["Item"]["folders"]["dates"])["string"]

			# Add the time template to the item dates text
			self.media["Item"]["Finished watching text"] += self.media["Item"]["Formatted datetime template"]

			# Update item dates text file
			self.File.Edit(self.media["Item"]["folders"]["dates"], self.media["Item"]["Finished watching text"], "w")

			self.media["Item"]["Finished watching text"] = self.media["Item"]["Finished watching text"].replace(self.language_texts["when_i_started_to_watch"], self.language_texts["when_i_started_to_watch"] + " " + self.media["texts"]["the_item"][self.user_language])

			# Add the time template to the Diary Slim text if the media is not completed
			if self.media["States"]["Completed media"] == False and self.media["States"]["Single unit"] == False:
				self.dictionary["Entry"]["Diary Slim"]["Dates"] = "\n\n" + self.media["Item"]["Finished watching text"]

		# Gets the date that the user started and finished watching the media and writes it to the media dates text file
		if self.media["States"]["Completed media"] == True:
			# Gets the media dates from the media dates file
			self.media["dates"] = self.File.Dictionary(self.media["folders"]["dates"], next_line = True)

			key = self.language_texts["when_i_started_to_watch"]

			# Get the started watching time
			self.media["Started watching"] = self.Date.To_UTC(self.Date.From_String(self.media["dates"][key]))

			# Define time spent watching using started watching time and finished watching time
			self.media["Time spent watching"] = self.Date.Difference(self.media["Started watching"], self.dictionary["Entry"]["Date"]["UTC"]["Object"])["Text"][self.user_language]

			if self.media["Time spent watching"][0] + self.media["Time spent watching"][1] == ", ":
				self.media["Time spent watching"] = self.media["Time spent watching"][2:]

			# Format the time template
			self.media["Item"]["Formatted datetime template"] = "\n\n" + template.format(self.media["Time spent watching"])

			# Read the media dates file
			self.media["Finished watching text"] = self.File.Contents(self.media["folders"]["dates"])["string"]

			# Add the time template to the media dates text
			self.media["Finished watching text"] += self.media["Item"]["Formatted datetime template"]

			# Update the media dates text file
			self.File.Edit(self.media["folders"]["dates"], self.media["Finished watching text"], "w")

			# Add the time template to the Diary Slim text
			self.media["Finished watching text"] = self.media["Finished watching text"].replace(self.language_texts["when_i_started_to_watch"], self.language_texts["when_i_started_to_watch"] + " " + self.media["texts"]["container_text"]["the"])

			if "Dates" not in self.dictionary["Entry"]["Diary Slim"]["Text"]:
				self.dictionary["Entry"]["Diary Slim"]["Dates"] = ""

			self.dictionary["Entry"]["Diary Slim"]["Dates"] += "\n\n" + self.media["Finished watching text"]

	def Define_Diary_Slim_Text(self):
		template = self.language_texts["i_just_finished_watching_{}"]

		if self.media["States"]["Series media"] == True:
			template += ' "{}"'

			text = self.dictionary["Media type"]["Genders"][self.user_language]["of_the"]

			if self.media["States"]["Video"] == True or self.media["States"]["Single unit"] == True:
				text = self.media_types["Genders"][self.user_language]["masculine"]["of_the"]

			# Add unit and "of the" text
			self.watched_item_text = self.language_texts["this_{}_{}"].format(self.media["texts"]["unit"][self.user_language], text)

			# Replaced "watching" with "re-watching" text
			if self.media["States"]["Re-watching"] == True:
				template = template.replace(self.language_texts["watching, infinitive"], self.language_texts["re_watching, infinitive"])

				template = template.replace(self.language_texts["re_watching, infinitive"], self.language_texts["re_watching, infinitive"] + " " + self.media["Episode"]["re_watched"]["time_text"][self.user_language])

			if self.media["States"]["Single unit"] == False and self.media["States"]["Video"] == False:
				# Replace "this" text with "the first" if the episode is the first one
				if self.media["Episode"]["Title"] == self.media["Item"]["Episodes"]["Titles"][self.media["Language"]][0]:
					self.watched_item_text = self.watched_item_text.replace(self.language_texts["this, masculine"], self.language_texts["the_first, masculine"])

				# Replace "this" text with "the last" if the episode is the last one
				if self.media["Episode"]["Title"] == self.media["Item"]["Episodes"]["Titles"][self.media["Language"]][-1] or len(self.media["Item"]["Episodes"]["Titles"][self.media["Language"]]) == 1:
					self.watched_item_text = self.watched_item_text.replace(self.language_texts["this, masculine"], self.language_texts["the_last, masculine"])

			if "Movie" in self.media["Episode"]["Titles"][self.media["Language"]]:
				self.watched_item_text = self.watched_item_text.replace(self.language_texts["episode"], self.language_texts["movie"])

			self.of_the_text = self.language_texts["of_the_{}"]

			if self.media["States"]["Media item list"] == True and self.media["Item"]["Title"] != self.media["Title"] and self.media["States"]["Single unit"] == False:
				if self.media["States"]["Video"] == False:
					text = ""

					# Replace "of the" text with "of the first" if the media item is the first one
					if self.media["Item"]["Title"] == self.media["Items"]["List"][0]:
						text = " " + self.language_texts["first, feminine"]

					# Replace "of the" text with "of the last" if the media item is the last one
					if self.media["Item"]["Title"] == self.media["Items"]["List"][-1]:
						text = " " + self.language_texts["last, feminine"]

					# Add item text ("season" or "series") to "of the" text
					self.of_the_text = self.of_the_text.format(text + self.media["texts"]["item"][self.user_language])

				if self.media["States"]["Video"] == True:
					self.of_the_text = self.of_the_text.format(self.language_texts["video_serie"])

				# Add "of the" text next to unit ("episode" or "video") text
				self.watched_item_text = self.watched_item_text.replace(self.media["texts"]["unit"][self.user_language], self.media["texts"]["unit"][self.user_language] + " {}".format(self.of_the_text))

				# Add media item title to "of the" text
				self.watched_item_text = self.watched_item_text.replace(self.of_the_text, self.of_the_text + ' "' + self.media["Item"]["Title"] + '"')

				# Replace media title with space in media item if it exists
				if self.media["Title"] + " " in self.media["Item"]:
					self.watched_item_text = self.watched_item_text.replace(self.media["Title"] + " ", "")

			# Add container (media type or "YouTube channel" text for video media type) to watched item text
			self.watched_item_text += " " + self.media["texts"]["container_text"]["container"]

			# Define Diary Slim text as the template formatted with the "watched item text" and the media title per language
			self.dictionary["Entry"]["Diary Slim"]["Text"] = template.format(self.watched_item_text, self.media["Titles"]["Language"])

		# If the media is a movie, only add the "this" text and the media type "movie" text in user language
		if self.media["States"]["Series media"] == False:
			self.dictionary["Entry"]["Diary Slim"]["Text"] = template.format(self.dictionary["Media type"]["Genders"][self.user_language]["this"] + " " + self.dictionary["Media type"]["Singular"][self.user_language].lower())

		# If the media unit is not single unit, add only the language episode (or movie) title
		if self.media["States"]["Single unit"] == False:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += ":\n"

			if self.media["Language"] in self.media["Episode"]["Titles"]:
				title = self.media["Episode"]["Titles"][self.media["Language"]]

			else:
				title = self.media["Episode"]["Titles"]["Language"]

			self.dictionary["Entry"]["Diary Slim"]["Text"] += title

		# If the media unit is single unit, add the episode with media title
		if self.media["States"]["Single unit"] == True:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += ":\n" + self.media["Episode"]["Titles"][self.media["Language"]]

		# Add the Re-watching text if the user is re-watching the media
		if self.media["States"]["Re-watching"] == True:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += self.media["Episode"]["re_watched"]["text"]

		# Add the episode link if it exists
		if "Remote" in self.media["Episode"] and "Link" in self.media["Episode"]["Remote"] and self.media["Episode"]["Remote"]["Title"] != "Animes Vision":
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.media["Episode"]["Remote"]["Link"]

		# Define the clean text to be used on the "Post_On_Social_Networks" method
		self.dictionary["Entry"]["Diary Slim"]["Clean text"] = self.dictionary["Entry"]["Diary Slim"]["Text"]

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

	def Post_On_Social_Networks(self):
		self.social_networks = [
			"WhatsApp",
			"Instagram",
			"Facebook",
			"Twitter",
		]

		self.social_networks_string = self.Text.From_List(self.social_networks, break_line = False, separator = ", ")
		self.first_three_social_networks = ""

		for social_network in self.social_networks:
			if social_network != self.social_networks[-1]:
				self.first_three_social_networks += social_network

				if social_network != "Facebook":
					self.first_three_social_networks += ", "

		self.twitter_social_network = self.social_networks[-1]

		text = self.language_texts["a_screenshot_of_the_episode"]

		if self.media["States"]["Series media"] == False:
			text = text.replace(self.language_texts["a_screenshot_of_the_episode"], self.language_texts["movie"])

		if self.media["Title"] in ["The Walking Dead", "Yuru Camp"]:
			text = text.replace(self.language_texts["a_screenshot_of_the_episode"], self.language_texts["a_summary_video"])

		self.posted_on_social_networks_text_template = self.language_texts["i_posted_the_watched_text_and_{}_on_the_status_of_{}_and_tweet_on_{}"] + "."

		self.dictionary["Entry"]["Diary Slim"]["Posted on the Social Networks text"] = self.posted_on_social_networks_text_template.format(text, self.first_three_social_networks, self.twitter_social_network)

		text = self.language_texts["post_on_the_social_networks"] + " (" + self.social_networks_string + ")"

		self.dictionary["Entry"]["States"]["Post on the Social Networks"] = self.Input.Yes_Or_No(text)

		if self.dictionary["Entry"]["States"]["Post on the Social Networks"] == True:
			from Social_Networks.Open_Social_Network import Open_Social_Network as Open_Social_Network

			Open_Social_Network(option_info = {"type": "profile"}, social_network_parameter = "WhatsApp", first_space = False, second_space = False)

			self.Input.Type(self.language_texts["press_enter_to_copy_the_watched_text"])

			self.Text.Copy(self.dictionary["Entry"]["Dates"]["Timezone"] + ":\n" + self.dictionary["Entry"]["Diary Slim"]["Clean text"])

		print()
		print("-----")
		print()

	def Write_On_Diary_Slim(self):
		# Add "Posted on Social Networks" text if the user wanted to post the entry text on the Social Networks
		if self.dictionary["Entry"]["States"]["Post on the Social Networks"] == True:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.dictionary["Entry"]["Diary Slim"]["Posted on the Social Networks text"]

		from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

		Write_On_Diary_Slim_Module(self.dictionary["Entry"]["Diary Slim"]["Text"], self.dictionary["Entry"]["Dates"]["Timezone"], add_dot = False)

	def Show_Information(self):
		self.dictionary["header_text"] = self.Text.Capitalize(self.media["texts"]["container_text"]["container"]) + ": "

		if self.media["States"]["Completed media"] == True:
			text = self.media["texts"]["container_text"]["this"]
			self.dictionary["header_text"] = self.language_texts["you_finished_watching_{}"].format(text) + ": "

		self.Show_Media_Information(self.dictionary)