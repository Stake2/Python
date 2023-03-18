# Register.py

from Watch_History.Watch_History import Watch_History as Watch_History

class Register(Watch_History):
	def __init__(self, dictionary = None, run_as_module = False):
		# If the dictionary is not None and the "Old history" key is inside it
		if dictionary != None and "Old history" in dictionary:
			# Add the keys and values of the dictionary to the pre-baked "Watch_History" class
			for key, value in dictionary["Old history"].items():
				setattr(Watch_History, key, value)

		super().__init__()

		self.run_as_module = run_as_module
		self.dictionary = dictionary

		if self.dictionary != None and "Old history" in self.dictionary:
			self.folders["watch_history"]["current_year"] = self.dictionary["Old history"]["folders"]

		# Ask for entry information
		if self.run_as_module == False:
			self.Type_Entry_Information()

		self.dictionary["Entry"].update({
			"Times": {},
			"Diary Slim": {
				"Text": "",
				"Clean text": ""
			},
			"States": {
				"Post on the Social Networks": False
			}
		})

		# If the Time dictionary is not empty, get the UTC and Timezone times
		if self.dictionary["Entry"]["Time"] != {}:
			self.dictionary["Entry"]["Times"] = {
				"UTC": self.Date.To_String(self.dictionary["Entry"]["Time"]["utc"]),
				"Timezone": self.Date.Now(self.dictionary["Entry"]["Time"]["date"].astimezone())["hh:mm DD/MM/YYYY"]
			}

		# If the Time dictionary is empty, define the UTC and Timezone times as the current year number
		if self.dictionary["Entry"]["Time"] == {}:
			self.dictionary["Entry"]["Times"] = {
				"UTC": self.current_year["Number"],
				"Timezone": self.current_year["Number"]
			}

		# Define the media variable to make typing the media dictionary easier
		self.media = self.dictionary["Media"]

		self.Check_Media_Status()

		if self.media["States"]["Re-watching"] == False:
			if self.media["States"]["Completed media"] == True or self.media["States"]["Completed media item"] == True:
				self.Check_Media_Dates()

		# Database related methods
		self.Register_In_JSON()
		self.Create_Entry_File()

		if "Old history" not in self.dictionary or "Old history" in self.dictionary and self.switches["testing"] == False:
			self.Add_Entry_File_To_Year_Folder()

		self.Define_Diary_Slim_Text()

		if "Old history" not in self.dictionary:
			self.Post_On_Social_Networks()

			self.Write_On_Diary_Slim()

		if self.switches["verbose"] == True:
			print()
			print(self.large_bar)
			print()
			print("Register:")

		if "Old history" in self.dictionary and self.switches["testing"] == True:
			self.Text.Copy(self.JSON.From_Python(self.dictionaries["Entries"]), verbose = False)

		self.Show_Information()

	def Type_Entry_Information(self):
		# To-Do: Make this method
		pass

	def Register_In_JSON(self):
		self.media_type = self.dictionary["media_type"]["plural"]["en"]

		# Re-read the "Watched" file to get the most updated data
		self.dictionaries["Watched"] = self.JSON.To_Python(self.media["item"]["folders"]["watched"]["entries"])

		# Import dictionaries from "Old history" dictionary
		if "Old history" in self.dictionary and "Entries" in self.dictionary["Old history"] and self.switches["testing"] == True:
			for dictionary_name in ["Entries", "Media Type"]:
				self.dictionaries[dictionary_name] = self.dictionary["Old history"][dictionary_name]

		if "Old history" not in self.dictionary or "Old history" in self.dictionary and self.switches["testing"] == False:
			# Re-read the "Entries" file to get the most updated data
			self.dictionaries["Entries"] = self.JSON.To_Python(self.folders["watch_history"]["current_year"]["entries"])

		dicts = [
			self.dictionaries["Entries"],
			self.dictionaries["Media Type"][self.media_type],
			self.dictionaries["Watched"]
		]

		# Add to watched, root and media type entry numbers
		for dict_ in dicts:
			dict_["Numbers"]["Total"] += 1

		# Define sanitized version of entry name for files
		self.dictionary["Entry"]["Name"] = {
			"Normal": str(self.dictionaries["Entries"]["Numbers"]["Total"]) + ". " + self.media_type,
			"Sanitized": ""
		}

		if "Timezone" in self.dictionary["Entry"]["Times"]:
			self.dictionary["Entry"]["Name"]["Normal"] += " (" + self.dictionary["Entry"]["Times"]["Timezone"] + ")"

		self.dictionary["Entry"]["Name"]["Sanitized"] = self.dictionary["Entry"]["Name"]["Normal"].replace(":", ";").replace("/", "-")

		# Add to the "Entries" lists
		for dict_ in dicts:
			if self.dictionary["Entry"]["Name"]["Normal"] not in dict_["Entries"]:
				dict_["Entries"].append(self.dictionary["Entry"]["Name"]["Normal"])

		# Define local media and media item titles to remove some keys from them
		media_titles = self.media["Titles"].copy()
		item_titles = self.media["item"]["Titles"].copy()

		for dictionary in [media_titles, item_titles]:
			dictionary.pop("Language")

			for key in ["ja", "Sanitized"]:
				if key in dictionary:
					dictionary.pop(key)

			for language in self.languages["small"]:
				if language in dictionary and dictionary["Original"] == dictionary[language]:
					dictionary.pop(language)

		self.key = self.dictionary["Entry"]["Name"]["Normal"]

		# Add the "Entry" dictionary to the "Entries" dictionary
		self.dictionaries["Entries"]["Dictionary"][self.key] = {
			"Number": self.dictionaries["Entries"]["Numbers"]["Total"],
			"Type number": self.dictionaries["Media Type"][self.media_type]["Numbers"]["Total"],
			"Entry": self.dictionary["Entry"]["Name"]["Normal"],
			"Media": media_titles,
			"Item": item_titles,
			"Episode": {
				"Number": 1,
				"Titles": self.media["episode"]["titles"]
			},
			"Type": self.media_type,
			"Time": ""
		}

		if "UTC" in self.dictionary["Entry"]["Times"]:
			self.dictionaries["Entries"]["Dictionary"][self.key]["Time"] = self.dictionary["Entry"]["Times"]["UTC"]

		# Remove the media item dictionary if the media has not media item list, the media item title is the same as the media title, or the media is non-series media
		if self.media["States"]["Media item list"] == False or self.media["item"]["title"] == self.media["title"] or self.media["States"]["series_media"] == False:
			self.dictionaries["Entries"]["Dictionary"][self.key].pop("Item")

		# Remove episode titles and number keys of dictionary if media is non-series media or single unit
		if self.media["States"]["series_media"] == False or self.media["States"]["single_unit"] == True:
			self.dictionaries["Entries"]["Dictionary"][self.key].pop("Episode")

		# Define episode number on dictionary if media is series media and not single unit
		if self.media["States"]["series_media"] == True and self.media["States"]["single_unit"] == False:
			self.dictionaries["Entries"]["Dictionary"][self.key]["Episode"]["Number"] = self.media["episode"]["number"]

		# Add episode ID if the key is present inside the episode dictionary
		if "id" in self.media["episode"]:
			self.dictionaries["Entries"]["Dictionary"][self.key]["ID"] = self.media["episode"]["id"]

			# Add episode link
			if "remote" in self.media["episode"]:
				self.dictionaries["Entries"]["Dictionary"][self.key]["Link"] = self.media["episode"]["remote"]["link"]

		# Add the "Comment" dictionary if it exists
		if "Comment" in self.dictionary["Comment Writer"]:
			self.dictionaries["Entries"]["Dictionary"][self.key]["Comment"] = self.dictionary["Comment Writer"]["Comment"]

		# Get the States dictionary
		self.states_dictionary = self.Define_States_Dictionary(self.dictionary)

		# Add the States dictionary into the Entry dictionary if it is not empty
		if self.states_dictionary["States"] != {}:
			self.dictionaries["Entries"]["Dictionary"][self.key]["States"] = self.states_dictionary["States"]

		# Add entry dictionary to media type entry dictionary
		self.dictionaries["Media Type"][self.media_type]["Dictionary"][self.key] = self.dictionaries["Entries"]["Dictionary"][self.key].copy()

		# Define "Watched" entry dictionary as media type entry dictionary
		self.dictionaries["Watched"]["Dictionary"][self.key] = self.dictionaries["Media Type"][self.media_type]["Dictionary"][self.key]

		# Get the "Comments" dictionary from the file
		self.dictionaries["Comments"] = self.JSON.To_Python(self.folders["comments"]["comments"])

		# Get the year comment number from the "Comments.json" file
		self.dictionaries["Entries"]["Numbers"]["Comments"] = self.dictionaries["Comments"]["Numbers"]["Years"][self.current_year["Number"]]

		# Get the year media type comment number from the "Comments.json" file
		self.dictionaries["Media Type"][self.media_type]["Numbers"]["Comments"] = self.dictionaries["Comments"]["Numbers"]["Type"][self.media_type]["Years"][self.current_year["Number"]]

		# Add to the media "Watched" comments number
		if self.dictionary["Comment Writer"]["States"]["write"] == True:
			self.dictionaries["Watched"]["Numbers"]["Comments"] += 1

		# Update the "Entries.json" file
		self.JSON.Edit(self.folders["watch_history"]["current_year"]["entries"], self.dictionaries["Entries"])

		if "Old history" not in self.dictionary or "Old history" in self.dictionary and self.switches["testing"] == False:
			# Update the media type "Entries.json" file
			self.JSON.Edit(self.dictionary["media_type"]["folders"]["per_media_type"]["entries"], self.dictionaries["Media Type"][self.media_type])

		# Update the media "Watched.json" file
		self.JSON.Edit(self.media["item"]["folders"]["watched"]["entries"], self.dictionaries["Watched"])

		if "Old history" not in self.dictionary or "Old history" in self.dictionary and self.switches["testing"] == False:
			# Add to "Entry list.txt" files
			if self.dictionary["Entry"]["Name"]["Normal"] not in self.File.Contents(self.folders["watch_history"]["current_year"]["entry_list"])["lines"]:
				self.File.Edit(self.folders["watch_history"]["current_year"]["entry_list"], self.dictionary["Entry"]["Name"]["Normal"], "a")

			if self.dictionary["Entry"]["Name"]["Normal"] not in self.File.Contents(self.dictionary["media_type"]["folders"]["per_media_type"]["entry_list"])["lines"]:
				self.File.Edit(self.dictionary["media_type"]["folders"]["per_media_type"]["entry_list"], self.dictionary["Entry"]["Name"]["Normal"], "a")

			if self.dictionary["Entry"]["Name"]["Normal"] not in self.File.Contents(self.media["item"]["folders"]["watched"]["entry_list"])["lines"]:
				self.File.Edit(self.media["item"]["folders"]["watched"]["entry_list"], self.dictionary["Entry"]["Name"]["Normal"], "a")

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
		# Times:
		# [Episode times]
		# 
		# File name:
		# [Number. Type (Time)]

		# Define entry file
		folder = self.dictionary["media_type"]["folders"]["per_media_type"]["files"]["root"]
		file = folder + self.dictionary["Entry"]["Name"]["Sanitized"] + ".txt"
		self.File.Create(file)

		self.dictionary["Entry"]["Text"] = {
			"General": self.Define_File_Text("General")
		}

		for language in self.languages["small"]:
			self.dictionary["Entry"]["Text"][language] = self.Define_File_Text(language)

		# Write entry text into entry file
		self.File.Edit(file, self.dictionary["Entry"]["Text"]["General"], "w")

		# Write entry text into "Watched" entry file
		file = self.media["item"]["folders"]["watched"]["files"]["root"] + self.dictionary["Entry"]["Name"]["Sanitized"] + ".txt"

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
			self.texts["media_type_number"][language] + ": " + str(self.dictionaries["Media Type"][self.media_type]["Numbers"]["Total"]),
			"\n" + self.JSON.Language.texts["media, title()"][language] + ":" + "\n" + "{}"
		]

		# Add item and episode titles lines
		if self.media["States"]["series_media"] == True:
			if self.media["States"]["Media item list"] == True and self.media["item"]["title"] != self.media["title"]:
				lines.append(self.texts["item, title()"][language] + ":" + "\n" + "{}")

			if self.media["States"]["single_unit"] == False:
				text = self.JSON.Language.texts["titles, title()"][language]

				if language_parameter != "General":
					text = self.JSON.Language.texts["title, title()"][language]

				list_ = []

				for title in list(self.media["episode"]["titles"].values()):
					if title not in list_:
						list_.append(title)

				if len(list_) == 1:
					text = self.JSON.Language.texts["title, title()"][language]

				lines.append(text + ":" + "\n" + "{}")

		lines_to_add = [
			self.JSON.Language.texts["type, title()"][language] + ":" + "\n" + self.dictionary["media_type"]["plural"][language] + "\n"
		]

		if self.dictionary["Entry"]["Times"] != {}:
			text = self.Date.texts["times, title()"][language] + ":" + "\n" + "{}"

			if self.dictionary["Entry"]["Times"]["UTC"] == self.dictionary["Entry"]["Times"]["Timezone"]:
				text = self.Date.texts["time, title()"][language] + ":" + "\n" + "{}"

			lines_to_add.append(text)

		lines_to_add.append(self.File.texts["file_name"][language] + ":" + "\n" + self.dictionary["Entry"]["Name"]["Normal"])

		lines.extend(lines_to_add)

		# Add states texts lines
		if self.states_dictionary["Texts"] != {}:
			text = "\n" + self.JSON.Language.texts["states, title()"][language] + ":" + "\n"

			for key in self.states_dictionary["Texts"]:
				language_text = self.states_dictionary["Texts"][key][language]

				text += language_text

				if key != list(self.states_dictionary["Texts"].keys())[-1]:
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

		if self.media["States"]["series_media"] == True:
			# Add media item titles to media item titles list
			if self.media["States"]["Media item list"] == True and self.media["item"]["title"] != self.media["title"]:
				key = "Original"

				if "Romanized" in self.media["item"]["Titles"]:
					key = "Romanized"

				item_titles = self.media["item"]["Titles"][key]

				if self.media["item"]["Titles"]["Language"] != self.media["item"]["Titles"][key]:
					item_titles += "\n" + self.media["item"]["Titles"]["Language"]

				items.append(item_titles + "\n")

			if self.media["States"]["single_unit"] == False:
				# Add episode titles to episode titles list
				episode_titles = ""

				if language_parameter != "General":
					episode_title = self.media["episode"]["titles"][language]

					if episode_title == "":
						episode_title = "[" + self.JSON.Language.texts["empty, title()"][language] + "]"

					episode_titles = episode_title + "\n"

				if language_parameter == "General":
					for language in self.languages["small"]:
						episode_title = self.media["episode"]["titles"][language]

						if episode_title == "":
							episode_title = "[" + self.JSON.Language.texts["empty, title()"][language] + "]"

						if episode_title + "\n" not in episode_titles:
							episode_titles += episode_title + "\n"

				items.append(episode_titles)

		if self.dictionary["Entry"]["Times"] != {}:
			# Add times to items list
			times = ""

			for key in ["UTC", "Timezone"]:
				if key in self.dictionary["Entry"]["Times"]:
					time = self.dictionary["Entry"]["Times"][key]

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
			type_folder = self.dictionary["media_type"]["plural"][language]

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

			type_folder = self.dictionary["media_type"]["singular"][language]

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

	def Define_Diary_Slim_Text(self):
		template = self.language_texts["i_just_finished_watching_{}"]

		if self.media["States"]["series_media"] == True:
			template += ' "{}"'

			text = self.dictionary["media_type"]["genders"][self.user_language]["of_the"]

			if self.media["States"]["video"] == True:
				text = self.media_types["genders"][self.user_language]["masculine"]["of_the"]

			# Add unit and "of the" text
			self.watched_item_text = self.language_texts["this_{}_{}"].format(self.media["texts"]["unit"][self.user_language], text)

			# Replaced "watching" with "re-watching" text
			if self.media["States"]["Re-watching"] == True:
				template = template.replace(self.language_texts["watching, infinitive"], self.language_texts["re_watching, infinitive"])

				template = template.replace(self.language_texts["re_watching, infinitive"], self.language_texts["re_watching, infinitive"] + " " + self.media["episode"]["re_watched"]["time_text"][self.user_language])

			if self.media["States"]["single_unit"] == False:
				# Replace "this" text with "the first" if the episode is the first one
				if self.media["episode"]["title"] == self.media["item"]["episodes"]["titles"][self.media["Language"]][0]:
					self.watched_item_text = self.watched_item_text.replace(self.language_texts["this, masculine"], self.language_texts["the_first, masculine"])

				# Replace "this" text with "the last" if the episode is the last one
				if self.media["episode"]["title"] == self.media["item"]["episodes"]["titles"][self.media["Language"]][-1] or len(self.media["item"]["episodes"]["titles"][self.media["Language"]]) == 1:
					self.watched_item_text = self.watched_item_text.replace(self.language_texts["this, masculine"], self.language_texts["the_last, masculine"])

			if "Movie" in self.media["episode"]["titles"][self.media["Language"]]:
				self.watched_item_text = self.watched_item_text.replace(self.language_texts["episode"], self.language_texts["movie"])

			self.of_the_text = self.language_texts["of_the_{}"]

			if self.media["States"]["Media item list"] == True and self.media["item"]["title"] != self.media["title"] and self.media["States"]["single_unit"] == False:
				if self.media["States"]["video"] == False:
					text = ""

					# Replace "of the" text with "of the first" if the media item is the first one
					if self.media["item"]["title"] == self.media["items"]["list"][0]:
						text = " " + self.language_texts["first, feminine"]

					# Replace "of the" text with "of the last" if the media item is the last one
					if self.media["item"]["title"] == self.media["items"]["list"][-1]:
						text = " " + self.language_texts["last, feminine"]

					# Add item text ("season" or "series") to "of the" text
					self.of_the_text = self.of_the_text.format(text + self.media["texts"]["item"][self.user_language])

				if self.media["States"]["video"] == True:
					self.of_the_text = self.of_the_text.format(self.language_texts["video_serie"])

				# Add "of the" text next to unit ("episode" or "video") text
				self.watched_item_text = self.watched_item_text.replace(self.media["texts"]["unit"][self.user_language], self.media["texts"]["unit"][self.user_language] + " {}".format(self.of_the_text))

				# Add media item title to "of the" text
				self.watched_item_text = self.watched_item_text.replace(self.of_the_text, self.of_the_text + ' "' + self.media["item"]["title"] + '"')

				# Replace media title with space in media item if it exists
				if self.media["title"] + " " in self.media["item"]:
					self.watched_item_text = self.watched_item_text.replace(self.media["title"] + " ", "")

			# Add container (media type or "YouTube channel" text for video media type) to watched item text
			self.watched_item_text += " " + self.media["texts"]["container_text"]["container"]

			# Define Diary Slim text as the template formatted with the "watched item text" and the media title per language
			self.dictionary["Entry"]["Diary Slim"]["Text"] = template.format(self.watched_item_text, self.media["Titles"]["Language"])

		# If the media is a movie, only add the "this" text and the media type "movie" text in user language
		if self.media["States"]["series_media"] == False:
			self.dictionary["Entry"]["Diary Slim"]["Text"] = template.format(self.dictionary["media_type"]["genders"][self.user_language]["this"] + " " + self.dictionary["media_type"]["singular"][self.user_language].lower())

		# If the media unit is not single unit, add only the language episode (or movie) title
		if self.media["States"]["single_unit"] == False:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += ":\n"

			if self.media["Language"] in self.media["episode"]["titles"]:
				title = self.media["episode"]["titles"][self.media["Language"]]

			else:
				title = self.media["episode"]["titles"]["Language"]

			self.dictionary["Entry"]["Diary Slim"]["Text"] += title

		# If the media unit is single unit, add the episode with media title
		if self.media["States"]["single_unit"] == True:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += ":\n" + self.media["episode"]["with_title"][self.media["Language"]]

		# Add the Re-watching text if the user is re-watching the media
		if self.media["States"]["Re-watching"] == True:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += self.media["episode"]["re_watched"]["text"]

		# Define the clean text to be used on the "Post_On_Social_Networks" method
		self.dictionary["Entry"]["Diary Slim"]["Clean text"] = self.dictionary["Entry"]["Diary Slim"]["Text"]

		# Add the episode link if it exists
		if "remote" in self.media["episode"] and "link" in self.media["episode"]["remote"]:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.media["episode"]["remote"]["link"]

		# If there are states, add the texts to the Diary Slim text
		if self.states_dictionary["States"] != {}:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.JSON.Language.language_texts["states, title()"] + ":" + "\n"

			for key in self.states_dictionary["Texts"]:
				self.dictionary["Entry"]["Diary Slim"]["Text"] += self.states_dictionary["Texts"][key][self.user_language]

				if key != list(self.states_dictionary["Texts"].keys())[-1]:
					self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n"

		# If there is timezone inside the times dictionary, add it
		if "Timezone" in self.dictionary["Entry"]["Times"]:
			time = self.dictionary["Entry"]["Times"]["Timezone"]

		# Else, get the current time
		else:
			time = self.Date.Now()["hh:mm DD/MM/YYYY"]

		# Add the time to the Diary Slim normal and clean text
		self.dictionary["Entry"]["Diary Slim"]["Text"] = time + ":\n" + self.dictionary["Entry"]["Diary Slim"]["Text"]
		self.dictionary["Entry"]["Diary Slim"]["Clean text"] = time + ":\n" + self.dictionary["Entry"]["Diary Slim"]["Clean text"]

	def Check_Media_Status(self):
		if self.media["States"]["series_media"] == True:
			# If the media has a media item list and the episode title is the last one
			if self.media["States"]["Media item list"] == True and self.media["episode"]["title"] == self.media["item"]["episodes"]["titles"][self.media["Language"]][-1]:
				# And the episode is not a video
				if self.media["States"]["video"] == False:
					# If the media item is the last media item, define the media as completed
					if self.media["item"]["title"] == self.media["items"]["list"][-1]:
						self.media["States"]["Completed media"] = True

					# If the media item is not the last media item (media is not completed), get next media item
					if self.media["item"]["title"] != self.media["items"]["list"][-1]:
						item_title = self.media["items"]["list"][self.media["item"]["number"] + 1]

						sanitized_title = self.Sanitize_Title(item_title)

						# Define the next media item prototype dictionary
						self.media["item"]["next"] = {
							"title": item_title,
							"Titles": {},
							"Sanitized": sanitized_title,
							"folders": {
								"root": self.media["items"]["folders"]["root"] + sanitized_title + "/",
								"media": {
									"root": self.media["folders"]["media"]["root"] + sanitized_title + "/"
								}
							},
							"number": self.media["item"]["number"] + 1
						}

						from copy import deepcopy

						# Define other variables for the next media item
						self.media["item"]["next"] = self.Define_Media_Item(deepcopy(self.dictionary), media_item = item_title)["Media"]["item"]

						if "Old history" not in self.dictionary:
							# Update current media item file
							self.File.Edit(self.media["items"]["folders"]["current"], self.media["item"]["next"]["title"], "w")

				# Add the "Status" key and value "Completed" to the end of the details
				key_value = {
					"key": self.language_texts["status, title()"],
					"value": self.JSON.Language.language_texts["completed, title()"]
				}

				self.media["item"]["details"] = self.JSON.Add_Key_After_Key(self.media["item"]["details"], key_value, add_to_end = True)

				if self.language_texts["episode, title()"] in self.media["item"]["details"] and self.media["States"]["single_unit"] == True:
					self.media["item"]["details"].pop(self.language_texts["episode, title()"])

				if "Old history" not in self.dictionary:
					# Update the media item details file
					self.File.Edit(self.media["item"]["folders"]["details"], self.Text.From_Dictionary(self.media["item"]["details"]), "w")

				self.media["States"]["Completed media item"] = True

			# If the media has no media item list and the episode title is the last one, define the media as completed
			if self.media["States"]["Media item list"] == False and self.media["episode"]["title"] == self.media["item"]["episodes"]["titles"][self.media["Language"]][-1]:
				self.media["States"]["Completed media"] = True

		# If the media is a movie, define it as completed
		if self.media["States"]["series_media"] == False:
			self.media["States"]["Completed media"] = True

		# If the media and media item are not completed, get next episode number
		if self.media["States"]["Completed media"] == False and self.media["States"]["Completed media item"] == False:
			# Get next episode language title
			self.media["episode"]["next"] = self.media["item"]["episodes"]["titles"][self.media["Language"]][self.media["episode"]["number"]]

			# Define current episode to watch as the next episode
			self.media["item"]["details"][self.language_texts["episode, title()"]] = self.media["episode"]["next"]

			if "Old history" not in self.dictionary:
				# Update media item details file
				self.File.Edit(self.media["item"]["folders"]["details"], self.Text.From_Dictionary(self.media["item"]["details"]), "w")

		# If the media is completed, define its status as completed
		if self.media["States"]["Completed media"] == True:
			if self.language_texts["remote_origin, title()"] in self.media["details"]:
				if self.media["details"][self.language_texts["remote_origin, title()"]] == "Animes Vision":
					self.media["details"].pop(self.language_texts["remote_origin, title()"])

				if self.media["details"][self.language_texts["remote_origin, title()"]] == "YouTube":
					self.media["details"].pop(self.language_texts["remote_origin, title()"])

			if "Old history" not in self.dictionary:
				# Update status key in media details
				self.Change_Status(self.dictionary)

		# Check if media item has a correspondent movie inside the movies folder
		if self.media["item"]["Type"][self.user_language] == self.language_texts["movie"]:
			self.movies = self.Get_Media_List(self.media_types[self.texts["movies, title()"]["en"]], self.texts["plan_to_watch, title()"]["en"])

			for movie_title in self.movies:
				# If the media item title is inside the movies list and the media type is not "Movies"
				if self.media["item"]["title"] in movie_title:
					# Define the movie prototype dictionary
					self.movie_dictionary = {
						"media_type": self.media_types[self.texts["movies, title()"]["en"]],
						"Media": {
							"title": movie_title
						}
					}

					# Define other variables for the movie
					self.movie_dictionary = self.Select_Media(self.movie_dictionary)

					# Copy the contents of the media comments folder to the movie comments folder
					self.Folder.Copy(self.media["item"]["folders"]["comments"]["root"], self.movie_dictionary["Media"]["item"]["folders"]["comments"]["root"])

					# Change the status of the movie to "Completed"
					self.Change_Status(self.movie_dictionary)

		# If media is non-series media
		if self.media["States"]["series_media"] == False:
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
				self.texts["on_hold, title()"]["en"]
			]

			# Iterate through the English plural media types list
			for plural_media_type in self.media_types["plural"]["en"]:
				if plural_media_type not in remove_list:
					media_list = self.Get_Media_List(self.media_types[plural_media_type], status_list)

					# Extend the series media list with the current media list
					self.series_media_list[plural_media_type] = media_list

			# Iterate through the English plural media types list
			for plural_media_type in self.media_types["plural"]["en"]:
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
								# If the media item title is equal to the root media item title (the one that was watched)
								if item_title == self.media["item"]["title"] or self.media["item"]["title"].split(" (")[0] in item_title:
									# Define the media prototype dictionary
									media_dictionary = {
										"media_type": self.media_types[plural_media_type],
										"Media": {
											"title": media_title
										}
									}

									# Define other variables for the media
									media_dictionary = self.Select_Media(media_dictionary)

									# Define the media item as the current media item
									media_dictionary["Media"]["item"] = self.Define_Media_Item(deepcopy(media_dictionary), media_item = item_title)["Media"]["item"]

									# Add the "Status" key and value "Completed" to the end of the details
									key_value = {
										"key": self.language_texts["status, title()"],
										"value": self.JSON.Language.language_texts["completed, title()"]
									}

									media_dictionary["Media"]["item"]["details"] = self.JSON.Add_Key_After_Key(media_dictionary["Media"]["item"]["details"], key_value, add_to_end = True)

									# Update the media item details file
									self.File.Edit(media_dictionary["Media"]["item"]["folders"]["details"], self.Text.From_Dictionary(media_dictionary["Media"]["item"]["details"]), "w")

	def Check_Media_Dates(self):
		# Completed media and media item time and date part
		template = self.language_texts["when_i_finished_watching"] + ":" + "\n" + \
		"[Timezone]" + "\n" + \
		"\n" + \
		self.Date.language_texts["duration, title()"] + ":" + "\n" + \
		"{}"

		if "Timezone" in self.dictionary["Entry"]["Times"]:
			template = template.replace("[Timezone]", self.dictionary["Entry"]["Times"]["Timezone"])

		if self.dictionary["Entry"]["Time"] != {}:
			self.dictionary["Entry"]["Time"] = self.Date.To_Timezone(self.dictionary["Entry"]["Time"])

		# Gets the date that the user started and finished watching the media item and writes it into the media item dates file
		if self.media["States"]["Completed media item"] == True and self.dictionary["Entry"]["Time"] != {}:
			# Gets the item dates from the item dates file
			self.media["item"]["dates"] = self.File.Dictionary(self.media["item"]["folders"]["dates"], next_line = True)

			if "Timezone" not in self.dictionary["Entry"]["Times"]:
				key = self.language_texts["when_i_finished_watching"]

				self.dictionary["Entry"]["Times"]["Timezone"] = self.media["item"]["dates"][key]

			key = self.language_texts["when_i_started_to_watch"]

			if self.media["States"]["single_unit"] == True:
				self.media["item"]["dates"][key] = self.dictionary["Entry"]["Times"]["Timezone"]

			if "Old history" not in self.dictionary:
				# Get started watching time
				self.media["item"]["started_watching_item"] = self.Date.To_UTC(self.Date.From_String(self.media["item"]["dates"][key]))

			else:
				self.media["item"]["started_watching_item"] = self.Date.To_UTC(self.Date.Now())

			# Define time spent watching using started watching time and finished watching time
			self.media["item"]["time_spent_watching"] = self.Date.Difference(self.media["item"]["started_watching_item"], self.dictionary["Entry"]["Time"])["difference_strings"][self.user_language]

			if self.media["item"]["time_spent_watching"][0] + self.media["item"]["time_spent_watching"][1] == ", ":
				self.media["item"]["time_spent_watching"] = self.media["item"]["time_spent_watching"][2:]

			# Format the time template
			self.media["item"]["formatted_template"] = "\n\n" + template.format(self.media["item"]["time_spent_watching"])

			# Add the time template to the item dates text
			self.media["item"]["finished_watching_text"] = self.File.Contents(self.media["item"]["folders"]["dates"])["string"]

			if "Old history" not in self.dictionary:
				self.media["item"]["finished_watching_text"] += self.media["item"]["formatted_template"]

				# Update item dates text file
				self.File.Edit(self.media["item"]["folders"]["dates"], self.media["item"]["finished_watching_text"], "w")

			self.media["item"]["finished_watching_text"] = self.media["item"]["finished_watching_text"].replace(self.language_texts["when_i_started_to_watch"], self.language_texts["when_i_started_to_watch"] + " " + self.media["texts"]["the_item"][self.user_language])

			# Add the time template to the Diary Slim text if the media is not completed
			if self.media["States"]["Completed media"] == False and self.media["States"]["single_unit"] == False:
				self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.media["item"]["finished_watching_text"]

		# Gets the date that the user started and finished watching the media and writes it to the media dates text file
		if self.media["States"]["Completed media"] == True and self.dictionary["Entry"]["Time"] != {}:
			# Gets the media dates from the media dates file
			self.media["dates"] = self.File.Dictionary(self.media["folders"]["dates"], next_line = True)

			if "Timezone" not in self.dictionary["Entry"]["Times"]:
				key = self.language_texts["when_i_finished_watching"]

				self.dictionary["Entry"]["Times"]["Timezone"] = self.media["dates"][key]

			key = self.language_texts["when_i_started_to_watch"]

			# Get started watching time
			self.media["started_watching"] = self.Date.To_UTC(self.Date.From_String(self.media["dates"][key]))

			# Define time spent watching using started watching time and finished watching time
			self.media["time_spent_watching"] = self.Date.Difference(self.media["started_watching"], self.dictionary["Entry"]["Time"])["difference_strings"][self.user_language]

			if self.media["time_spent_watching"][0] + self.media["time_spent_watching"][1] == ", ":
				self.media["time_spent_watching"] = self.media["time_spent_watching"][2:]

			# Format the time template
			self.media["item"]["formatted_template"] = "\n\n" + template.format(self.media["time_spent_watching"])

			# Add the time template to the media dates text
			self.media["finished_watching_text"] = self.File.Contents(self.media["folders"]["dates"])["string"]

			if "Old history" not in self.dictionary:
				self.media["finished_watching_text"] += self.media["item"]["formatted_template"]

				# Update media dates text file
				self.File.Edit(self.media["folders"]["dates"], self.media["finished_watching_text"], "w")

			# Add the time template to the Diary Slim text
			self.media["finished_watching_text"] = self.media["finished_watching_text"].replace(self.language_texts["when_i_started_to_watch"], self.language_texts["when_i_started_to_watch"] + " " + self.media["texts"]["container_text"]["the"])

			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.media["finished_watching_text"]

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

		if self.media["States"]["series_media"] == False:
			text = text.replace(self.language_texts["a_screenshot_of_the_episode"], self.language_texts["movie"])

		if self.media["title"] in ["The Walking Dead", "Yuru Camp"]:
			text = text.replace(self.language_texts["a_screenshot_of_the_episode"], self.language_texts["a_summary_video"])

		self.posted_on_social_networks_text_template = self.language_texts["i_posted_the_watched_text_and_{}_on_the_status_of_{}_and_tweet_on_{}"] + "."

		self.dictionary["Entry"]["Diary Slim"]["Posted on the Social Networks text"] = self.posted_on_social_networks_text_template.format(text, self.first_three_social_networks, self.twitter_social_network)

		text = self.language_texts["post_on_the_social_networks"] + " (" + self.social_networks_string + ")"

		self.dictionary["Entry"]["States"]["Post on the Social Networks"] = self.Input.Yes_Or_No(text)

		if self.dictionary["Entry"]["States"]["Post on the Social Networks"] == True:
			from Social_Networks.Open_Social_Network import Open_Social_Network as Open_Social_Network

			Open_Social_Network(option_info = {"type": "profile"}, social_network_parameter = "WhatsApp", first_space = False, second_space = False)

			self.Input.Type(self.language_texts["press_enter_to_copy_the_watched_text"])

			self.Text.Copy(self.dictionary["Entry"]["Diary Slim"]["Clean text"])

		print()
		print("-----")
		print()

	def Write_On_Diary_Slim(self):
		# Add "Posted on Social Networks" text if the user wanted to post the entry text on the Social Networks
		if self.dictionary["Entry"]["States"]["Post on the Social Networks"] == True:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.dictionary["Entry"]["Diary Slim"]["Posted on the Social Networks text"]

		from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

		Write_On_Diary_Slim_Module(self.dictionary["Entry"]["Diary Slim"]["Text"], add_time = False, add_dot = False)

	def Show_Information(self):
		self.dictionary["header_text"] = self.Text.Capitalize(self.media["texts"]["container_text"]["container"]) + ": "

		if self.media["States"]["Completed media"] == True:
			text = self.media["texts"]["container_text"]["this"]
			self.dictionary["header_text"] = self.language_texts["you_finished_watching_{}"].format(text) + ": "

		self.Show_Media_Information(self.dictionary)