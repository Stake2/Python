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

		# Check the media status
		self.Check_Media_Status()

		# If the user is re-watching the media and media item
		if self.media["States"]["Re-watching"] == False:
			# If the user completed the media or the media item
			if (
				self.media["States"]["Completed media"] == True or
				self.media["States"]["Completed media item"] == True
			):
				# Check the media and media item dates and the date files
				self.Check_Media_Dates()

		# Define the "test things" switch as [the value I am using if I am testing the class]
		test_stuff = False

		# If the switch is False
		if test_stuff == False:
			# Database related methods
			self.Register_In_JSON()
			self.Create_Entry_File()
			self.Add_Entry_File_To_Year_Folder()

			# Define the Diary Slim text
			self.Define_Diary_Slim_Text()

			# If the "Defined title" key is not inside the root dictionary
			if "Defined title" not in self.dictionary:
				# Post about the watched media (and item) on the social networks
				self.Post_On_Social_Networks()

			# Write the watched media (item) description text in the user language on the Diary Slim
			self.Write_On_Diary_Slim()

		# Update the statistic about the media watched
		self.Update_Statistic()

		# If the "Defined title" key is not inside the root dictionary
		if "Defined title" not in self.dictionary:
			# Show information about the watched media (item)
			self.Show_Information()

		# Re-initiate the root class to update the files
		del self.folders

		super().__init__()

	def Type_Entry_Information(self):
		# To-Do: Make this method
		pass

	def Register_In_JSON(self):
		self.media_type = self.dictionary["Media type"]["Plural"]["en"]

		# Re-read the "Watched.json" file to get the most updated data
		self.dictionaries["Watched"] = self.JSON.To_Python(self.media["Item"]["Folders"]["Watched"]["entries"])

		# Re-read the "Entries.json" file to get the most updated data
		if "Defined title" not in self.dictionary:
			self.dictionaries["Entries"] = self.JSON.To_Python(self.folders["Watch History"]["Current year"]["Entries"])

		# If the "Dictionaries" variable is inside the root dictionary
		if "Dictionaries" in self.dictionary:
			# Define the local "dictionaries" variable as the variable inside the root dictionary
			self.dictionaries = self.dictionary["Dictionaries"]

			if "Watched" in self.dictionary:
				self.dictionaries["Watched"] = self.dictionary["Watched"]

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

		# Define the local media and media item titles to remove some keys from them
		media_titles = self.media["Titles"].copy()
		item_titles = self.media["Item"]["Titles"].copy()

		# Define the list of titles to remove some keys
		titles = [
			media_titles,
			item_titles
		]

		# Remove the keys
		for dict_ in titles:
			dict_.pop("Language")

			for key in ["ja", "Sanitized"]:
				if key in dict_:
					dict_.pop(key)

			for language in self.languages["small"]:
				if language in dict_:
					if (
						dict_["Original"] == dict_[language] or
						"Romanized" in dict_ and
						dict_["Romanized"] == dict_[language]
					):
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

		# Remove the media item dictionary if the media does not contain a media item list,
		# The media item title is the same as the media title,
		# Or the media is non-series media
		if (
			self.media["States"]["Media item list"] == False or
			self.media["States"]["Media item is media"] == True
		):
			self.dictionaries["Entries"]["Dictionary"][self.key].pop("Item")

		# Remove episode titles and number keys of dictionary if media is non-series media or single unit
		if (
			self.media["States"]["Series media"] == False or
			self.media["States"]["Single unit"] == True
		):
			self.dictionaries["Entries"]["Dictionary"][self.key].pop("Episode")

		# Define episode number on dictionary if media is series media and not single unit and is episodic
		if (
			self.media["States"]["Series media"] == True and
			self.media["States"]["Single unit"] == False and
			self.media["States"]["Episodic"] == True
		):
			self.dictionaries["Entries"]["Dictionary"][self.key]["Episode"]["Number"] = self.media["Episode"]["Number"]

		# Remove "Number" key from Episode dictionary is the media is non-episodic
		if (
			"Episode" in self.dictionaries["Entries"]["Dictionary"][self.key] and
			self.media["States"]["Episodic"] == False
		):
			self.dictionaries["Entries"]["Dictionary"][self.key]["Episode"].pop("Number")

		# Add episode ID if the key is present inside the episode dictionary
		if "ID" in self.media["Episode"]:
			self.dictionaries["Entries"]["Dictionary"][self.key]["ID"] = self.media["Episode"]["ID"]

			# Add episode link
			if "Remote" in self.media["Episode"]:
				self.dictionaries["Entries"]["Dictionary"][self.key]["Link"] = self.media["Episode"]["Remote"]["Link"]

		# Add the "Comment" dictionary if it exists
		if "Comment" in self.dictionary["Comment Writer"]:
			self.dictionaries["Entries"]["Dictionary"][self.key]["Comment"] = self.dictionary["Comment Writer"]["Comment"]

			if (
				list(self.dictionaries["Entries"]["Dictionary"][self.key]["Comment"].keys()) == ["Date"] and
				self.dictionaries["Entries"]["Dictionary"][self.key]["Comment"]["Date"] == self.dictionaries["Entries"]["Dictionary"][self.key]["Date"]
			):
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
		self.dictionaries["Comments"] = self.JSON.To_Python(self.folders["Comments"]["Comments"])

		# Get the year comment number from the "Comments.json" file
		self.dictionaries["Entries"]["Numbers"]["Comments"] = self.dictionaries["Comments"]["Numbers"]["Years"][self.current_year["Number"]]

		# Get the year media type comment number from the "Comments.json" file
		self.dictionaries["Media type"][self.media_type]["Numbers"]["Comments"] = self.dictionaries["Comments"]["Numbers"]["Type"][self.media_type]["Years"][self.current_year["Number"]]

		# Add to the media "Watched" comments number
		if self.dictionary["Comment Writer"]["States"]["Write"] == True:
			self.dictionaries["Watched"]["Numbers"]["Comments"] += 1

		# Update the "Entries.json" file
		self.JSON.Edit(self.folders["Watch History"]["Current year"]["Entries"], self.dictionaries["Entries"])

		# Update the media type "Entries.json" file
		self.JSON.Edit(self.dictionary["Media type"]["Folders"]["Per Media Type"]["Entries"], self.dictionaries["Media type"][self.media_type])

		# Update the media "Watched.json" file
		self.JSON.Edit(self.media["Item"]["Folders"]["Watched"]["entries"], self.dictionaries["Watched"])

		# Add to the "Entry list.txt" files
		lines = self.File.Contents(self.folders["Watch History"]["Current year"]["Entry list"])["lines"]

		if self.dictionary["Entry"]["Name"]["Normal"] not in lines:
			self.File.Edit(self.folders["Watch History"]["Current year"]["Entry list"], self.dictionary["Entry"]["Name"]["Normal"], "a")

		lines = self.File.Contents(self.dictionary["Media type"]["Folders"]["Per Media Type"]["Entry list"])["lines"]

		if self.dictionary["Entry"]["Name"]["Normal"] not in lines:
			self.File.Edit(self.dictionary["Media type"]["Folders"]["Per Media Type"]["Entry list"], self.dictionary["Entry"]["Name"]["Normal"], "a")

		lines = self.File.Contents(self.media["Item"]["Folders"]["Watched"]["entry_list"])["lines"]

		if self.dictionary["Entry"]["Name"]["Normal"] not in lines:
			self.File.Edit(self.media["Item"]["Folders"]["Watched"]["entry_list"], self.dictionary["Entry"]["Name"]["Normal"], "a")

	def Create_Entry_File(self):
		# Number: [Episode number]
		# Type number: [Type number]
		# 
		# Media:
		# [Media titles]
		# 
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
		# 
		# (
		# States:
		# [State texts]
		# )

		# Define the general Entry file inside the media type folder
		folder = self.dictionary["Media type"]["Folders"]["Per Media Type"]["Files"]["root"]
		file = folder + self.dictionary["Entry"]["Name"]["Sanitized"] + ".txt"
		self.File.Create(file)

		self.dictionary["Entry"]["Text"] = {
			"General": self.Define_File_Text("General")
		}

		for language in self.languages["small"]:
			self.dictionary["Entry"]["Text"][language] = self.Define_File_Text(language)

		# Write the Entry text into the general Entry file inside the media type folder
		self.File.Edit(file, self.dictionary["Entry"]["Text"]["General"], "w")

		# Define the Entry file inside the "Watched" folder of the media (item) folder
		file = self.media["Item"]["Folders"]["Watched"]["files"]["root"] + self.dictionary["Entry"]["Name"]["Sanitized"] + ".txt"

		# Create the file
		self.File.Create(file)

		# Write the Entry text into the Entry file
		self.File.Edit(file, self.dictionary["Entry"]["Text"][self.user_language], "w")

	def Define_File_Text(self, language_parameter = None):
		if language_parameter != "General":
			language = language_parameter

		if language_parameter == "General":
			language = self.user_language

		full_language = self.languages["full"][language]

		# Define the Entry text lines list
		lines = [
			self.Language.texts["number, title()"][language] + ": " + str(self.dictionaries["Entries"]["Numbers"]["Total"]),
			self.texts["media_type_number"][language] + ": " + str(self.dictionaries["Media type"][self.media_type]["Numbers"]["Total"]),
			"\n" + self.Language.texts["media, title()"][language] + ":" + "\n" + "{}"
		]

		# Add the item and episode titles lines
		if self.media["States"]["Series media"] == True:
			if (
				self.media["States"]["Media item list"] == True and
				self.media["States"]["Media item is media"] == False
			):
				lines.append(self.Language.texts["item, title()"][language] + ":" + "\n" + "{}")

			if self.media["States"]["Single unit"] == False:
				text = self.Language.texts["titles, title()"][language]

				if language_parameter != "General":
					text = self.Language.texts["title, title()"][language]

				list_ = []

				for title in list(self.media["Episode"]["Titles"].values()):
					if title not in list_:
						list_.append(title)

				if len(list_) == 1:
					text = self.Language.texts["title, title()"][language]

				lines.append(text + ":" + "\n" + "{}")

		lines_to_add = [
			self.Language.texts["type, title()"][language] + ":" + "\n" + self.dictionary["Media type"]["Plural"][language] + "\n"
		]

		text = self.Date.texts["times, title()"][language] + ":" + "\n" + "{}"

		if self.dictionary["Entry"]["Dates"]["UTC"] == self.dictionary["Entry"]["Dates"]["Timezone"]:
			text = self.Date.texts["time, title()"][language] + ":" + "\n" + "{}"

		lines_to_add.append(text)

		lines_to_add.append(self.File.texts["file_name"][language] + ":" + "\n" + self.dictionary["Entry"]["Name"]["Normal"])

		lines.extend(lines_to_add)

		# Add the state texts lines
		if self.dictionary["States"]["Texts"] != {}:
			text = "\n" + self.Language.texts["states, title()"][language] + ":" + "\n"

			for key in self.dictionary["States"]["Texts"]:
				language_text = self.dictionary["States"]["Texts"][key][language]

				text += language_text

				if key != list(self.dictionary["States"]["Texts"].keys())[-1]:
					text += "\n"

			lines.append(text)

		# Define the language entry text
		file_text = self.Text.From_List(lines, next_line = True)

		# Define the items to be added to the entry text
		items = []

		titles = ""

		# Add the media titles to the items list
		key = "Original"

		# If there is a romanized title, add the original title and change the key to "Romanized"
		if "Romanized" in self.media["Titles"]:
			titles += self.media["Titles"]["Original"] + "\n"

			key = "Romanized"

		# Add the original or romanized title to the titles string
		titles += self.media["Titles"][key]

		# If the language parameter is "General"
		# And the language title is not equal to the original or romanized title
		if (
			language_parameter == "General" and
			self.media["Titles"]["Language"] != self.media["Titles"][key]
		):
			# Add the language title to the titles string
			titles += "\n" + self.media["Titles"]["Language"]

			# Iterate through the small languages list
			for local_language in self.languages["small"]:
				# If the local language exists inside the dictionary of titles
				# And the title in that language is not equal to the language title
				if (
					local_language in self.media["Titles"] and
					self.media["Titles"][local_language] != self.media["Titles"]["Language"]
				):
					# Add the current language title to the titles string
					titles += "\n" + self.media["Titles"][local_language]

		# If the language parameter is not "General"
		if language_parameter != "General" and language in self.media["Titles"]:
			# Add the langauge title to the titles string
			titles += "\n" + self.media["Titles"][language]

		# Add the titles string to the items list
		items.append(titles + "\n")

		if self.media["States"]["Series media"] == True:
			# Add the media item titles to the media item titles list
			if (
				self.media["States"]["Media item list"] == True and
				self.media["States"]["Media item is media"] == False
			):
				key = "Original"

				item_titles = ""

				if "Romanized" in self.media["Item"]["Titles"]:
					item_titles = self.media["Item"]["Titles"][key] + "\n"

					key = "Romanized"

				item_titles += self.media["Item"]["Titles"][key]

				if self.media["Item"]["Titles"]["Language"] != self.media["Item"]["Titles"][key]:
					item_titles += "\n" + self.media["Item"]["Titles"]["Language"]

				items.append(item_titles + "\n")

			if self.media["States"]["Single unit"] == False:
				# Add episode titles to episode titles list
				episode_titles = ""

				if language_parameter != "General":
					episode_title = self.media["Episode"]["Titles"][language]

					if episode_title == "":
						episode_title = "[" + self.Language.texts["empty, title()"][language] + "]"

					episode_titles = episode_title + "\n"

				if language_parameter == "General":
					for language in self.languages["small"]:
						episode_title = self.media["Episode"]["Titles"][language]

						if episode_title == "":
							episode_title = "[" + self.Language.texts["empty, title()"][language] + "]"

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
			root_folder = self.Language.texts["watched_media"][language]
			type_folder = self.dictionary["Media type"]["Plural"][language]

			# Watched media folder
			folder = self.current_year["Folders"][language]["root"]
			self.Folder.Create(folder)

			self.current_year["Folders"][language]["Watched media"] = {
				"root": folder + root_folder + "/"
			}

			self.Folder.Create(self.current_year["Folders"][language]["Watched media"]["root"])

			# Define the media type folder
			folder = self.current_year["Folders"][language]["Watched media"]["root"]
			self.Folder.Create(folder)

			self.current_year["Folders"][language]["Watched media"][type_folder] = {
				"root": folder + type_folder + "/"
			}

			self.Folder.Create(self.current_year["Folders"][language]["Watched media"][type_folder]["root"])

			# Define the watched media file
			folder = self.current_year["Folders"][language]["Watched media"][type_folder]["root"]
			file_name = self.dictionary["Entry"]["Name"]["Sanitized"]
			self.current_year["Folders"][language]["Watched media"][type_folder][file_name] = folder + file_name + ".txt"

			self.File.Create(self.current_year["Folders"][language]["Watched media"][type_folder][file_name])

			# Write the Entry text per language inside the year Entry file
			self.File.Edit(self.current_year["Folders"][language]["Watched media"][type_folder][file_name], self.dictionary["Entry"]["Text"][language], "w")

			# "Firsts Of The Year" part
			if self.media["States"]["First media type entry in year"] == True:
				# "Firsts Of The Year" subfolder
				subfolder_name = self.Language.texts["media, title()"][language]

				folder = self.current_year["Folders"][language]["Firsts of the Year"]["root"]
				self.Folder.Create(folder)

				# Define the subfolder dictionary
				self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name] = {
					"root": folder + subfolder_name + "/"
				}

				self.Folder.Create(self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name]["root"])

				type_folder = self.dictionary["Media type"]["Singular"][language]

				# Define the media type folder dictionary
				self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name][type_folder] = {
					"root": folder + type_folder + "/"
				}

				self.Folder.Create(self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name][type_folder]["root"])

				# Define the "First Of The Year" Entry file
				self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name][type_folder][file_name] = folder + file_name + ".txt"
				self.File.Create(self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name][type_folder][file_name])

				# Write the Entry text per language inside the "First Of The Year" Entry file
				self.File.Edit(self.current_year["Folders"][language]["Firsts of the Year"][subfolder_name][type_folder][file_name], self.dictionary["Entry"]["Text"][language], "w")

	def Check_Media_Status(self):
		if self.media["States"]["Series media"] == True:
			# If the media has a media item list
			# And the episode title is the last one
			if (
				self.media["States"]["Media item list"] == True and
				self.media["Episode"]["Title"] == self.media["Item"]["Episodes"]["Titles"][self.media["Language"]][-1]
			):
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
							"Folders": {
								"root": self.media["Items"]["Folders"]["root"] + sanitized_title + "/",
								"Media": {
									"root": self.media["Folders"]["Media"]["root"] + sanitized_title + "/"
								}
							},
							"Number": self.media["Item"]["Number"] + 1
						}

						from copy import deepcopy

						# Define other variables for the next media item
						self.media["Item"]["Next"] = self.Define_Media_Item(deepcopy(self.dictionary), media_item = item_title)["Media"]["Item"]

						# Update current media item file
						self.File.Edit(self.media["Items"]["Folders"]["current"], self.media["Item"]["Next"]["Title"], "w")

					# Add the "Status" key and value "Completed" to the end of the media item details
					key_value = {
						"key": self.Language.language_texts["status, title()"],
						"value": self.Language.language_texts["completed, title()"]
					}

					self.media["Item"]["Details"] = self.JSON.Add_Key_After_Key(self.media["Item"]["Details"], key_value, add_to_end = True)

				# If the "Episode" key is inside the media item details
				# And the media item is a single unit
				if (
					self.Language.language_texts["episode, title()"] in self.media["Item"]["Details"] and
					self.media["States"]["Single unit"] == True
				):
					# Remove the "Episode" key
					self.media["Item"]["Details"].pop(self.Language.language_texts["episode, title()"])

				# Update the media item details file with the updated media item details dictionary
				self.File.Edit(self.media["Item"]["Folders"]["details"], self.Text.From_Dictionary(self.media["Item"]["Details"]), "w")

				# If the media is not a video channel
				# And the media item is not the last one on the list of media items
				if (
					self.media["States"]["Video"] == False and
					len(self.media["Items"]["List"]) != 1
				):
					# Define the media item as completed
					self.media["States"]["Completed media item"] = True

			# If the media has no media item list
			# And the episode title is the last one
			# And the media is not a video channel
			if (
				self.media["States"]["Media item list"] == False and
				self.media["Episode"]["Title"] == self.media["Item"]["Episodes"]["Titles"][self.media["Language"]][-1] and
				self.media["States"]["Video"] == False
			):
				# Define the media as completed
				self.media["States"]["Completed media"] = True

		# If the media is a movie, define it as completed
		if self.media["States"]["Series media"] == False:
			self.media["States"]["Completed media"] = True

		# If the media and media item are not completed, get next episode number
		if (
			self.media["States"]["Completed media"] == False and
			self.media["States"]["Completed media item"] == False and
			len(self.media["Item"]["Episodes"]["Titles"][self.media["Language"]]) != 1
		):
			try:
				# Get next episode language title
				self.media["Episode"]["Next"] = self.media["Item"]["Episodes"]["Titles"][self.media["Language"]][self.media["Episode"]["Number"]]

				# Define current episode to watch as the next episode
				self.media["Item"]["Details"][self.Language.language_texts["episode, title()"]] = self.media["Episode"]["Next"]

				# Update media item details file
				self.File.Edit(self.media["Item"]["Folders"]["details"], self.Text.From_Dictionary(self.media["Item"]["Details"]), "w")

			except IndexError:
				pass

		# If the media is completed, define its status as completed
		if self.media["States"]["Completed media"] == True:
			if self.Language.language_texts["remote_origin"] in self.media["Details"]:
				if self.media["Details"][self.Language.language_texts["remote_origin"]] == "Animes Vision":
					self.media["Details"].pop(self.Language.language_texts["remote_origin"])

				elif self.media["Details"][self.Language.language_texts["remote_origin"]] == "YouTube":
					self.media["Details"].pop(self.Language.language_texts["remote_origin"])

			# Define the new status as "Completed"
			self.media["Status change"] = {
				"Old": self.media["Details"][self.Language.language_texts["status, title()"]],
				"New": self.Language.language_texts["completed, title()"]
			}

			# Update the status key in the media details
			self.Change_Status(self.dictionary)

		# Check if the media item has a correspondent movie inside the movies folder
		if (
			self.media["States"]["Series media"] == True and
			"Type" in self.media["Item"] and
			self.media["Item"]["Type"][self.user_language] == self.language_texts["movie"]
		):
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
					self.Folder.Copy(self.media["Item"]["Folders"]["comments"]["root"], self.movie_dictionary["Media"]["Item"]["Folders"]["comments"]["root"])

					# Change the status of the movie to "Completed"
					self.Change_Status(self.movie_dictionary)

		# Check if the movie has a correspondent media item inside the series media folders
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
				self.Language.texts["on_hold, title()"]["en"],
				self.texts["watching, title()"]["en"],
				self.texts["re_watching, title()"]["en"]
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
						media_folder = self.media_types[plural_media_type]["Folders"]["Media information"]["root"] + self.Sanitize_Title(media_title) + "/"

						media_items_folder = media_folder + self.media_types[plural_media_type]["Subfolders"]["Plural"] + "/"

						# If the media items folder exists
						if self.Folder.Exist(media_items_folder) == True:
							media_items_file = media_items_folder + self.media_types[plural_media_type]["Subfolders"]["Plural"] + ".txt"

							# Get the media items list
							media_items = self.File.Contents(media_items_file)["lines"]

							# Iterate through the media items list
							for item_title in media_items:
								item_folder = media_items_folder + self.Sanitize_Title(item_title) + "/"
								item_details_file = item_folder + self.Language.language_texts["details, title()"] + ".txt"

								item_details = self.File.Dictionary(item_details_file)

								# If the media item title is equal to the root media item title (the one that was watched)
								# Or is inside the item title and the year of the movie is the same as the year of the item
								if (
									item_title == self.media["Item"]["Title"] or
									self.media["Item"]["Title"].split(" (")[0] in item_title and
									self.media["Item"]["Details"][self.Date.language_texts["year, title()"]] == item_details[self.Date.language_texts["year, title()"]]
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
										"key": self.Language.language_texts["status, title()"],
										"value": self.Language.language_texts["completed, title()"]
									}

									media_dictionary["Media"]["Item"]["Details"] = self.JSON.Add_Key_After_Key(media_dictionary["Media"]["Item"]["Details"], key_value, add_to_end = True)

									# Update the media item details file
									self.File.Edit(media_dictionary["Media"]["Item"]["Folders"]["details"], self.Text.From_Dictionary(media_dictionary["Media"]["Item"]["Details"]), "w")

	def Check_Media_Dates(self):
		# Completed media and media item time and date template
		template = self.language_texts["when_i_finished_watching"] + ":" + "\n" + \
		self.dictionary["Entry"]["Dates"]["Timezone"] + "\n" + \
		"\n" + \
		self.Date.language_texts["duration, title()"] + ":" + "\n" + \
		"{}"

		# Gets the date that the user started and finished watching the media item and writes it into the media item dates file
		# If the user completed the media item
		if self.media["States"]["Completed media item"] == True:
			# Gets the item dates from the item dates file
			self.media["Item"]["dates"] = self.File.Dictionary(self.media["Item"]["Folders"]["dates"], next_line = True)

			key = self.language_texts["when_i_started_to_watch"]

			if self.media["States"]["Single unit"] == True:
				self.media["Item"]["dates"][key] = self.dictionary["Entry"]["Dates"]["Timezone"]

			# Get started watching time
			self.media["Item"]["started_watching_item"] = self.Date.To_UTC(self.Date.From_String(self.media["Item"]["dates"][key]))

			# Define the difference between the two dates
			difference = self.Date.Difference(self.media["Item"]["started_watching_item"], self.dictionary["Entry"]["Date"]["UTC"]["Object"])

			# Define time spent watching using started watching time and finished watching time
			self.media["Item"]["Time spent watching"] = difference["Text"][self.user_language]

			if self.media["Item"]["Time spent watching"][0] + self.media["Item"]["Time spent watching"][1] == ", ":
				self.media["Item"]["Time spent watching"] = self.media["Item"]["Time spent watching"][2:]

			# Format the time template
			self.media["Item"]["Formatted datetime template"] = "\n\n" + template.format(self.media["Item"]["Time spent watching"])

			# Read the media item dates file
			self.media["Item"]["Finished watching text"] = self.File.Contents(self.media["Item"]["Folders"]["dates"])["string"]

			# Add the time template to the item dates text
			self.media["Item"]["Finished watching text"] += self.media["Item"]["Formatted datetime template"]

			# Update item dates text file
			self.File.Edit(self.media["Item"]["Folders"]["dates"], self.media["Item"]["Finished watching text"], "w")

			self.media["Item"]["Finished watching text"] = self.media["Item"]["Finished watching text"].replace(self.language_texts["when_i_started_to_watch"], self.language_texts["when_i_started_to_watch"] + " " + self.media["texts"]["the_item"][self.user_language])

			# Add the time template to the Diary Slim text if the media is not completed
			if (
				self.media["States"]["Completed media"] == False and
				self.media["States"]["Single unit"] == False
			):
				self.dictionary["Entry"]["Diary Slim"]["Dates"] = "\n\n" + self.media["Item"]["Finished watching text"]

		# Gets the date that the user started and finished watching the media and writes it to the media dates text file
		# If the user completed the media
		# Or the media item title is the same as the media title
		if (
			self.media["States"]["Completed media"] == True or
			self.media["States"]["Media item is media"] == True
		):
			# Gets the media dates from the media dates file
			self.media["dates"] = self.File.Dictionary(self.media["Folders"]["dates"], next_line = True)

			key = self.language_texts["when_i_started_to_watch"]

			# Get the started watching time
			self.media["Started watching"] = self.Date.To_UTC(self.Date.From_String(self.media["dates"][key]))

			# Define the difference between the two dates
			difference = self.Date.Difference(self.media["Started watching"], self.dictionary["Entry"]["Date"]["UTC"]["Object"])

			# Define time spent watching using started watching time and finished watching time
			self.media["Time spent watching"] = difference["Text"][self.user_language]

			if self.media["Time spent watching"][0] + self.media["Time spent watching"][1] == ", ":
				self.media["Time spent watching"] = self.media["Time spent watching"][2:]

			# Format the time template
			self.media["Item"]["Formatted datetime template"] = "\n\n" + template.format(self.media["Time spent watching"])

			# Read the media dates file
			self.media["Finished watching text"] = self.File.Contents(self.media["Folders"]["dates"])["string"]

			# Add the time template to the media dates text
			self.media["Finished watching text"] += self.media["Item"]["Formatted datetime template"]

			# Update the media dates text file
			self.File.Edit(self.media["Folders"]["dates"], self.media["Finished watching text"], "w")

			# Add the time template to the Diary Slim text
			self.media["Finished watching text"] = self.media["Finished watching text"].replace(self.language_texts["when_i_started_to_watch"], self.language_texts["when_i_started_to_watch"] + " " + self.media["texts"]["container_text"]["the"])

			if "Dates" not in self.dictionary["Entry"]["Diary Slim"]["Text"]:
				self.dictionary["Entry"]["Diary Slim"]["Dates"] = ""

			self.dictionary["Entry"]["Diary Slim"]["Dates"] += "\n\n" + self.media["Finished watching text"]

	def Define_Diary_Slim_Text(self):
		template = self.language_texts["i_just_finished_watching_{}"]

		# Replaced "watching" with "re-watching" text
		if self.media["States"]["Re-watching"] == True:
			template = template.replace(self.language_texts["watching, infinitive"], self.language_texts["re_watching, infinitive"])

			template = template.replace(self.language_texts["re_watching, infinitive"], self.language_texts["re_watching, infinitive"] + " " + self.media["Episode"]["Re-watched"]["Texts"]["Times"][self.user_language])

		if self.media["States"]["Series media"] == True:
			template += ' "{}"'

			text = self.dictionary["Media type"]["Genders"][self.user_language]["of_the"]

			if self.dictionary["Media type"]["Plural"]["en"] != self.texts["series, title()"]["en"]:
				text = self.media_types["Genders"][self.user_language]["masculine"]["of_the"]

			# Define the unit text
			unit_text = self.media["texts"]["unit"][self.user_language]

			# If the media item is a single unit one
			if self.media["States"]["Single unit"] == True:
				# Define the unit text as the media item type text
				unit_text = self.media["Item"]["Type"][self.user_language].lower()

			# Add unit and "of the" text
			self.watched_item_text = self.Language.language_texts["genders, type: dict, masculine"]["this"] + " " + unit_text + " " + text

			if (
				self.media["States"]["Single unit"] == False and
				self.media["States"]["Video"] == False
			):
				# Replace "this" text with "the first" if the episode is the first one
				if self.media["Episode"]["Title"] == self.media["Item"]["Episodes"]["Titles"][self.media["Language"]][0]:
					self.watched_item_text = self.watched_item_text.replace(self.Language.language_texts["genders, type: dict, masculine"]["this"], self.Language.language_texts["the_first, masculine"])

				# Replace "this" text with "the last" if the episode is the last one
				if (
					self.media["Episode"]["Title"] == self.media["Item"]["Episodes"]["Titles"][self.media["Language"]][-1] or
					len(self.media["Item"]["Episodes"]["Titles"][self.media["Language"]]) == 1
				):
					self.watched_item_text = self.watched_item_text.replace(self.Language.language_texts["genders, type: dict, masculine"]["this"], self.Language.language_texts["the_last, masculine"])

			if "Movie" in self.media["Episode"]["Titles"][self.media["Language"]]:
				self.watched_item_text = self.watched_item_text.replace(self.language_texts["episode"], self.language_texts["movie"])

			self.of_the_text = self.Language.language_texts["of_the_{}"]

			if (
				self.media["States"]["Media item list"] == True and
				self.media["States"]["Media item is media"] == False and
				self.media["States"]["Single unit"] == False
			):
				if self.media["States"]["Video"] == False:
					text = ""

					# Replace the "of the" text with "of the first" if the media item is the first one
					if self.media["Item"]["Title"] == self.media["Items"]["List"][0]:
						text = self.Language.language_texts["first, feminine"] + " "

					# Replace the "of the" text with "of the last" if the media item is the last one
					if self.media["Item"]["Title"] == self.media["Items"]["List"][-1]:
						text = self.Language.language_texts["last, feminine"] + " "

					# Add the item text ("season" or "series") to "of the" text
					self.of_the_text = self.of_the_text.format(text + self.language_texts["season, title()"].lower())

				if self.media["States"]["Video"] == True:
					self.of_the_text = self.of_the_text.format(self.language_texts["video_serie"])

				# If the watched media is not a video channel
				if self.media["States"]["Video"] == False:
					# Add "of the" text next to unit ("episode" or "video") text
					self.watched_item_text = self.watched_item_text.replace(self.media["texts"]["unit"][self.user_language], self.media["texts"]["unit"][self.user_language] + " {}".format(self.of_the_text))

					# Define the media item title variable
					media_item_title = self.Define_Title(self.media["Item"]["Titles"])

					# If the season text is not inside the media item title
					if " " + self.language_texts["season, title()"] not in media_item_title:
						# Add quotes around the media item title
						media_item_title = '"' + media_item_title + '"'

					# Add the media item title to the "of the" text
					self.watched_item_text = self.watched_item_text.replace(self.of_the_text, self.of_the_text + " " + media_item_title)

					# If the season text is inside the media item title
					if " " + self.language_texts["season, title()"] in media_item_title:
						# Remove it
						self.watched_item_text = self.watched_item_text.replace(" " + self.language_texts["season, title()"].lower(), "")

				# Replace the media title with space in the media item if it exists
				if self.media["Title"] + " " in self.media["Item"]:
					self.watched_item_text = self.watched_item_text.replace(self.media["Title"] + " ", "")

			# Add container (media type or "YouTube channel" text for video media type) to watched item text
			self.watched_item_text += " " + self.media["texts"]["container_text"]["container"]

			# Define the "Diary Slim" text as the template formatted with the "watched item text" and the media title per language
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

			# If the length of the title is greater than one
			# And the first two characters of the title are a space and a colon
			if (
				len(title) > 1 and
				title[0] + title[1] == ": "
			):
				# Remove them
				title = title[2:]

			self.dictionary["Entry"]["Diary Slim"]["Text"] += title

		# If the media unit is single unit, add the episode with media title
		if self.media["States"]["Single unit"] == True:
			# Define the episode title
			episode_title = self.media["Episode"]["Titles"][self.media["Language"]]

			# If the length of the title is greater than one
			# And the first two characters of the title are a space and a colon
			if (
				len(episode_title) > 1 and
				episode_title[0] + episode_title[1] == ": "
			):
				# Remove them
				episode_title = episode_title[2:]

			self.dictionary["Entry"]["Diary Slim"]["Text"] += ":\n" + episode_title

		# Add year and distributor/producer to title for movies
		if self.media["States"]["Series media"] == False:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += " (" + self.media["Episode"]["Titles"]["Original"].split("(")[1]

		# Add the Re-watching text if the user is re-watching the media
		if self.media["States"]["Re-watching"] == True:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += self.media["Episode"]["Re-watched"]["Texts"]["Number"][self.user_language]

		# Add the episode link if it exists
		if (
			"Remote" in self.media["Episode"] and
			"Link" in self.media["Episode"]["Remote"] and
			self.media["Episode"]["Remote"]["Title"] != "Animes Vision"
		):
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.media["Episode"]["Remote"]["Link"]

		# Define the clean text to be used on the "Post_On_Social_Networks" method
		self.dictionary["Entry"]["Diary Slim"]["Clean text"] = self.dictionary["Entry"]["Diary Slim"]["Text"]

		# If there are states, add the texts to the Diary Slim text
		if self.dictionary["States"]["States"] != {}:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.Language.language_texts["states, title()"] + ":" + "\n"

			for key in self.dictionary["States"]["Texts"]:
				self.dictionary["Entry"]["Diary Slim"]["Text"] += self.dictionary["States"]["Texts"][key][self.user_language]

				if key != list(self.dictionary["States"]["Texts"].keys())[-1]:
					self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n"

		# If there are dates, add them to the Diary Slim text
		if "Dates" in self.dictionary["Entry"]["Diary Slim"]:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += self.dictionary["Entry"]["Diary Slim"]["Dates"]

	def Post_On_Social_Networks(self):
		# Define the "Social Networks" dictionary
		self.social_networks = {
			"List": [
				"Discord",
				"WhatsApp",
				"Instagram",
				"Facebook"
			],
			"List text": ""
		}

		# Define the list text, with all the Social Networks separated by commas
		self.social_networks["List text"] = self.Text.From_List(self.social_networks["List"])

		# Remove the "Discord" social networks
		self.social_networks["List"].remove("Discord")

		# Define the list text, with all the Social Networks separated by commas
		# But without Discord
		self.social_networks["List text (without Discord)"] = self.Text.From_List(self.social_networks["List"])

		# Define the item text to be used
		self.social_networks["Item text"] = self.language_texts["the_episode_cover"]

		if self.media["States"]["Series media"] == False:
			self.social_networks["Item text"] = self.social_networks["Item text"].replace(self.language_texts["episode"], self.language_texts["movie"])

		if self.media["States"]["Video"] == True:
			self.social_networks["Item text"] = self.social_networks["Item text"].replace(self.language_texts["episode"], self.Language.language_texts["video, title()"].lower())

		# Define the "posted" template
		self.social_networks["Template"] = self.language_texts["i_posted_the_watched_text, type: template"] + "."

		# Define the template items list
		self.social_networks["Items"] = [
			self.social_networks["Item text"],
			"Discord",
			self.social_networks["List text (without Discord)"],
			"Twitter, Bluesky, " + self.Language.language_texts["and"] + " Threads"
		]

		# Format the template with the items list
		self.dictionary["Entry"]["Diary Slim"]["Posted on the Social Networks text"] = self.social_networks["Template"].format(*self.social_networks["Items"])

		# Define the text to show while asking the user if they want to post on the social networks
		text = self.language_texts["post_on_the_social_networks"] + " (" + self.social_networks["List text"] 

		# Add the "and others" text
		text += ", " + self.Language.language_texts["and_others, feminine"]

		# Add the closing parenthesis
		text += ")"

		# Define the "ask for input" switch as False
		ask_for_input = False

		# Define the "Post on the social networks" state as True
		self.dictionary["Entry"]["States"]["Post on the Social Networks"] = True

		# If the "Testing" switch is False
		# If the "ask for input" switch is True
		if (
			self.switches["Testing"] == False and
			ask_for_input == True
		):
			# Ask if the user wants to post the watched media status on the social networks
			self.dictionary["Entry"]["States"]["Post on the Social Networks"] = self.Input.Yes_Or_No(text)

		# If the user answer is yes
		if self.dictionary["Entry"]["States"]["Post on the Social Networks"] == True:
			# Import the "Open_Social_Network" sub-class of the "Social_Networks" module
			from Social_Networks.Open_Social_Network import Open_Social_Network as Open_Social_Network

			# Define the Social Networks dictionary
			social_networks = {
				"List": [
					"WhatsApp",
					"Facebook",
					"Discord"
				],
				"Custom links": {
					"Discord": "https://discord.com/channels/311004778777935872/641352970352459776" # "#watch-history" channel on my Discord server
				}
			}

			# Open the Social Networks, one by one
			# (Commented out because this class is not working properly)
			#Open_Social_Network(social_networks)

		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

	def Write_On_Diary_Slim(self):
		# Add "Posted on Social Networks" text if the user wanted to post the entry text on the Social Networks
		if self.dictionary["Entry"]["States"]["Post on the Social Networks"] == True:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.dictionary["Entry"]["Diary Slim"]["Posted on the Social Networks text"]

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

	def Get_The_Media_Title(self, is_media_item = False, media_item = None, language = False, no_media_title = False):
		# Define the key to get the media title
		key = "Original"

		if "Romanized" in self.media["Titles"]:
			key = "Romanized"

		# If the "language" parameter is True
		if language == True:
			# Define the media title key as the "Language" one
			key = "Language"

		# Define the local media title variable
		media_title = self.media["Titles"][key]

		# If the "is media item" parameter is True
		# And there is a media item inside the media dictionary
		# And the media item is not the root media
		if (
			is_media_item == True and
			"Item" in self.media and
			self.media["States"]["Media item is media"] == False
		):
			# If the media item parameter is None
			if media_item == None:
				media_item = self.media["Item"]

			# Define the key to get the media item title
			key = "Original"

			if "Romanized" in media_item["Titles"]:
				key = "Romanized"

			# If the "language" parameter is True
			if language == True:
				# Define the media title key as the "Language" one
				key = "Language"

			# Get the media item title using the key
			media_item_title = media_item["Titles"][key]

			# If the first two characters of the title are not a colon and a space
			if media_item_title[0] + media_item_title[1] != ": ":
				# Add a space
				media_title += " "

			# If the "no media title" parameter is True
			if no_media_title == True:
				# Reset the media title to an empty string
				media_title = ""

			# Add the media item title to the root media title
			media_title += media_item_title

			# If the "no media title" parameter is True
			# And the first two characters of the media title are a colon and a space
			if (
				no_media_title == True and
				media_title[0] + media_title[1] == ": "
			):
				# Remove the colon and space
				media_title = media_title[2:]

		# Return the media title
		return media_title

	def Update_Statistic(self):
		# Define a local media dictionary
		media = {
			"Titles": {
				"Original": self.Get_The_Media_Title(),
				"Language": self.Get_The_Media_Title(language = True)
			}
		}

		# Copy the "texts" dictionary of the root media dictionary to the local one
		media["texts"] = self.media["texts"]

		# If there is a media item inside the media dictionary
		if "Item" in self.media:
			# Copy the "Item" dictionary of the root media dictionary to the local one
			media["Item"] = self.media["Item"]

			# Create a media item titles dictionary and add it to the "Item" key
			media["Titles"]["Item"] = {
				"Original": self.Get_The_Media_Title(is_media_item = True),
				"Original (no media title)": self.Get_The_Media_Title(is_media_item = True, no_media_title = True),
				"Language": self.Get_The_Media_Title(is_media_item = True, language = True)
			}

		# If the media contains media items
		if "Items" in self.media:
			# Pass the "Items" dictionary to the local media dictionary
			media["Items"] = self.media["Items"]

		# Define the media type dictionary
		media_type = {
			"Plural": self.media_type,
			"The": self.media["texts"]["container_text"]["the (original)"]
		}

		# Update the media statistics for the current year and month, passing the local media dictionary and the media type
		# And getting the statistics text back
		self.dictionary["Statistics text"] = Watch_History.Update_Statistics(self, self.dictionary, media, media_type)

	def Show_Information(self):
		self.dictionary["Header text"] = self.Text.Capitalize(self.media["texts"]["container_text"]["container"]) + ":"

		if self.media["States"]["Completed media"] == True:
			text = self.media["texts"]["container_text"]["this"]

			self.dictionary["Header text"] = self.language_texts["you_finished_watching"] + " " + text + ":"

		if self.media["States"]["Re-watching"] == True:
			self.dictionary["Header text"] = self.dictionary["Header text"].replace(self.language_texts["watching, infinitive"], self.language_texts["re_watching, infinitive"])

		self.Show_Media_Information(self.dictionary)