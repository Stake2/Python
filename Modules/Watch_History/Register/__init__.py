# Register.py

from Watch_History.Watch_History import Watch_History as Watch_History

class Register(Watch_History):
	def __init__(self, run_as_module = False, media_dictionary = None):
		super().__init__()

		self.run_as_module = run_as_module
		self.media_dictionary = media_dictionary

		if self.run_as_module == False:
			self.Type_Entry_Information()

		self.media_dictionary["Entry"].update({
			"Times": {
				"UTC": self.Date.To_String(self.media_dictionary["Entry"]["Time"]["utc"]),
				"Timezone": self.media_dictionary["Entry"]["Time"]["hh:mm DD/MM/YYYY"]
			},
			"Diary Slim": {
				"Text": ""
			}
		})

		# Database related methods
		self.Register_In_JSON()
		self.Create_Entry_File()
		self.Add_Entry_File_To_Year_Folder()

		self.Define_Diary_Slim_Text()
		self.Check_Media_Status()

		if self.media_dictionary["Media"]["States"]["Re-watching"] == False:
			if self.media_dictionary["Media"]["States"]["Completed media"] == True or self.media_dictionary["Media"]["States"]["Completed media item"] == True:
				self.Set_Media_As_Completed()

		self.Post_On_Social_Networks()

		self.Write_On_Diary_Slim()

		if self.switches["verbose"] == True:
			print()
			print(self.large_bar)
			print()
			print("Register:")

		self.Show_Information()

	def Type_Entry_Information(self):
		# To-Do: Make this method
		pass

	def Register_In_JSON(self):
		self.media_type = self.media_dictionary["media_type"]["plural"]["en"]

		self.dictionaries["Watched"] = self.JSON.To_Python(self.media_dictionary["Media"]["item"]["folders"]["watched"]["entries"])

		# Add to watched episode, root episode and media type episode numbers
		self.dictionaries["Entries"]["Numbers"]["Total"] += 1
		self.dictionaries["Watched"]["Numbers"]["Total"] += 1
		self.dictionaries["Media Type"][self.media_type]["Numbers"]["Total"] += 1

		# Define sanitized version of entry name for files
		self.media_dictionary["Entry"]["Name"] = {
			"Normal": str(self.dictionaries["Entries"]["Numbers"]["Total"]) + ". " + self.media_type + " (" + self.media_dictionary["Entry"]["Times"]["Timezone"] + ")",
			"Sanitized": ""
		}

		self.media_dictionary["Entry"]["Name"]["Sanitized"] = self.media_dictionary["Entry"]["Name"]["Normal"].replace(":", ";").replace("/", "-")

		# Add to "Entries" list
		self.dictionaries["Entries"]["Entries"].append(self.media_dictionary["Entry"]["Name"]["Normal"])
		self.dictionaries["Media Type"][self.media_type]["Entries"].append(self.media_dictionary["Entry"]["Name"]["Normal"])
		self.dictionaries["Watched"]["Entries"].append(self.media_dictionary["Entry"]["Name"]["Normal"])

		# Add episode dictionary to episodes dictionary
		media_titles = self.media_dictionary["Media"]["titles"].copy()
		item_titles = self.media_dictionary["Media"]["item"]["titles"].copy()

		for key in ["jp", "sanitized"]:
			if key in media_titles:
				media_titles.pop(key)

			if key in item_titles:
				item_titles.pop(key)

		if media_titles["language"] == media_titles["original"]:
			media_titles.pop("language")

		if item_titles["language"] == item_titles["original"]:
			item_titles.pop("language")

		for dictionary in [media_titles, item_titles]:
			if "romanized" in dictionary and dictionary["language"] == dictionary["romanized"]:
				dictionary.pop("romanized")

		self.key = self.media_dictionary["Entry"]["Name"]["Normal"]

		self.dictionaries["Entries"]["Dictionary"][self.key] = {
			"Number": self.dictionaries["Entries"]["Numbers"]["Total"],
			"Type number": self.dictionaries["Media Type"][self.media_type]["Numbers"]["Total"],
			"Entry": self.media_dictionary["Entry"]["Name"]["Normal"],
			"Media": media_titles,
			"Item": item_titles,
			"Episode titles": self.media_dictionary["Media"]["episode"]["titles"],
			"Episode number": "",
			"Type": self.media_type,
			"Time": self.media_dictionary["Entry"]["Times"]["UTC"]
		}

		if self.media_dictionary["Media"]["States"]["media_list"] == False or self.media_dictionary["Media"]["item"]["title"] == self.media_dictionary["Media"]["title"] or self.media_dictionary["Media"]["States"]["series_media"] == False:
			self.dictionaries["Entries"]["Dictionary"][self.key].pop("Item")

		# Remove episode titles and number keys of dictionary if media is non-series media or single unit
		if self.media_dictionary["Media"]["States"]["series_media"] == False or self.media_dictionary["Media"]["States"]["single_unit"] == True or self.media_dictionary["Media"]["States"]["episodic"] == False:
			self.dictionaries["Entries"]["Dictionary"][self.key].pop("Episode titles")
			self.dictionaries["Entries"]["Dictionary"][self.key].pop("Episode number")

		# Define episode number on dictionary if media is series media and not single unit
		if self.media_dictionary["Media"]["States"]["series_media"] == True and self.media_dictionary["Media"]["States"]["single_unit"] == False and self.media_dictionary["Media"]["States"]["episodic"] == True:
			self.dictionaries["Entries"]["Dictionary"][self.key]["Episode number"] = self.media_dictionary["Media"]["episode"]["number"]

		# Add episode ID if the key is present inside the episode dictionary
		if "id" in self.media_dictionary["Media"]["episode"]:
			self.dictionaries["Entries"]["Dictionary"][self.key]["ID"] = self.media_dictionary["Media"]["episode"]["id"]

		states_dictionary = self.Define_States_Dictionary(self.media_dictionary)["states"]

		if states_dictionary != {}:
			self.dictionaries["Entries"]["Dictionary"][self.key]["States"] = states_dictionary

		# Add entry dictionary to media type entry dictionary
		self.dictionaries["Media Type"][self.media_type]["Dictionary"][self.key] = self.dictionaries["Entries"]["Dictionary"][self.key].copy()

		# Define "Watched" entry dictionary as media type entry dictionary
		self.dictionaries["Watched"]["Dictionary"][self.key] = self.dictionaries["Media Type"][self.media_type]["Dictionary"][self.key]

		# Get Comments dictionary from file
		self.dictionaries["Comments"] = self.JSON.To_Python(self.folders["comments"]["comments"])

		# Get year comment number from "Comments.json" file
		self.dictionaries["Entries"]["Numbers"]["Comments"] = self.dictionaries["Comments"]["Numbers"]["Years"][str(self.date["year"])]

		# Get year media type comment number from "Comments.json" file
		self.dictionaries["Media Type"][self.media_type]["Numbers"]["Comments"] = self.dictionaries["Comments"]["Numbers"]["Type"][self.media_type]["Years"][str(self.date["year"])]

		# Add to media comments number
		if self.media_dictionary["Comment Writer"]["States"]["write"] == True:
			self.dictionaries["Watched"]["Numbers"]["Comments"] += 1

		# Update "Entries.json" file
		self.JSON.Edit(self.folders["watch_history"]["current_year"]["entries"], self.dictionaries["Entries"])

		# Update media type "Entries.json" file
		self.JSON.Edit(self.media_dictionary["media_type"]["folders"]["per_media_type"]["entries"], self.dictionaries["Media Type"][self.media_type])

		# Update media "Watched.json" file
		self.JSON.Edit(self.media_dictionary["Media"]["item"]["folders"]["watched"]["entries"], self.dictionaries["Watched"])

		# Add to root and media type "Entry list.txt" file
		self.File.Edit(self.folders["watch_history"]["current_year"]["entry_list"], self.media_dictionary["Entry"]["Name"]["Normal"], "a")
		self.File.Edit(self.media_dictionary["media_type"]["folders"]["per_media_type"]["entry_list"], self.media_dictionary["Entry"]["Name"]["Normal"], "a")

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
		# [Episode/Video] titles:
		# [Episode titles]
		# )
		# Type: [Media type]
		#
		# Times:
		# [Episode times]
		# 
		# File name: [Number. Type (Time)]

		# Define entry file
		folder = self.media_dictionary["media_type"]["folders"]["per_media_type"]["files"]["root"]
		file = folder + self.media_dictionary["Entry"]["Name"]["Sanitized"] + ".txt"
		self.File.Create(file)

		self.media_dictionary["Entry"]["Text"] = {
			"General": self.Define_File_Text("General")
		}

		for language in self.languages["small"]:
			self.media_dictionary["Entry"]["Text"][language] = self.Define_File_Text(language)

		# Write entry text into entry file
		self.File.Edit(file, self.media_dictionary["Entry"]["Text"]["General"], "w")

		# Write entry text into "Watched" entry file
		file = self.media_dictionary["Media"]["item"]["folders"]["watched"]["files"]["root"] + self.media_dictionary["Entry"]["Name"]["Normal"] + ".txt"

		self.File.Create(file)
		self.File.Edit(file, self.media_dictionary["Entry"]["Text"][self.user_language], "w")

	def Define_File_Text(self, language_parameter = None):
		if language_parameter != "General":
			language = language_parameter

		if language_parameter == "General":
			language = "en"

		full_language = self.languages["full"][language]

		# Define entry text lines
		lines = [
			self.JSON.Language.texts["number, title()"][language] + ": " + str(self.dictionaries["Entries"]["Numbers"]["Total"]),
			self.texts["media_type_number"][language] + ": " + str(self.dictionaries["Media Type"][self.media_type]["Numbers"]["Total"]),
			"\n" + self.texts["media, title()"][language] + ":" + "\n" + "{}"
		]

		# Add item and episode titles lines
		if self.media_dictionary["Media"]["States"]["series_media"] == True:
			if self.media_dictionary["Media"]["States"]["media_list"] == True and self.media_dictionary["Media"]["item"]["title"] != self.media_dictionary["Media"]["title"]:
				lines.append(self.texts["item, title()"][language] + ":" + "\n" + "{}")

			if self.media_dictionary["Media"]["States"]["single_unit"] == False:
				text = self.texts["episode_titles"][language]

				if language_parameter != "General":
					text = self.texts["episode_title"][language]

				if self.media_dictionary["Media"]["States"]["video"] == True:
					text = self.texts["video_titles"][language]

				lines.append(text + ":" + "\n" + "{}")

		lines.extend([
			self.JSON.Language.texts["type, title()"][language] + ": " + self.media_dictionary["media_type"]["plural"]["en"] + "\n",
			self.Date.texts["times, title()"][language] + ":" + "\n" + "{}",
			self.File.texts["file_name"][language] + ": " + self.media_dictionary["Entry"]["Name"]["Normal"]
		])

		states_dictionary = self.Define_States_Dictionary(self.media_dictionary)

		# Add states texts lines
		if states_dictionary != {}:
			text = "\n" + self.JSON.Language.texts["states, title()"][language] + ":" + "\n"

			for key in states_dictionary["texts"]:
				language_text = states_dictionary["texts"][key][language]

				text += language_text

				if key != list(states_dictionary["texts"].keys())[-1]:
					text += "\n"

			lines.append(text)

		# Define language entry text
		file_text = self.Text.From_List(lines)

		# Define items to be added to entry text
		items = []

		titles = ""

		# Add media titles to items list
		key = "original"

		if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"] and "romanized" in self.media_dictionary["Media"]["titles"]:
			key = "romanized"

		titles += self.media_dictionary["Media"]["titles"][key]

		if self.media_dictionary["Media"]["titles"]["language"] != self.media_dictionary["Media"]["titles"][key]:
			titles += "\n" + self.media_dictionary["Media"]["titles"]["language"]

		items.append(titles + "\n")

		if self.media_dictionary["Media"]["States"]["series_media"] == True:
			# Add media item titles to media item titles list
			if self.media_dictionary["Media"]["States"]["media_list"] == True and self.media_dictionary["Media"]["item"]["title"] != self.media_dictionary["Media"]["title"]:
				key = "original"

				if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"] and "romanized" in self.media_dictionary["Media"]["item"]["titles"]:
					key = "romanized"

				item_titles = self.media_dictionary["Media"]["item"]["titles"][key]

				if self.media_dictionary["Media"]["item"]["titles"]["language"] != self.media_dictionary["Media"]["item"]["titles"][key]:
					item_titles += "\n" + self.media_dictionary["Media"]["item"]["titles"]["language"]

				items.append(item_titles + "\n")

			if self.media_dictionary["Media"]["States"]["single_unit"] == False:
				# Add episode titles to episode titles list
				episode_titles = ""

				if language_parameter != "General":
					episode_title = self.media_dictionary["Media"]["episode"]["titles"][language]

					if episode_title == "":
						episode_title = "[" + self.JSON.Language.texts["empty, title()"][language] + "]"

					episode_titles = episode_title + "\n"

				if language_parameter == "General":
					for language in self.languages["small"]:
						episode_title = self.media_dictionary["Media"]["episode"]["titles"][language]

						if episode_title == "":
							episode_title = "[" + self.JSON.Language.texts["empty, title()"][language] + "]"

						episode_titles += episode_title + "\n"

				items.append(episode_titles)

		# Add times to items list
		times = ""

		for key in ["UTC", "Timezone"]:
			time = self.media_dictionary["Entry"]["Times"][key]

			times += time + "\n"

		items.append(times)

		return file_text.format(*items)

	def Add_Entry_File_To_Year_Folder(self):
		# Create folders
		for language in self.languages["small"]:
			full_language = self.languages["full"][language]

			# Folder names
			root_folder = self.texts["watched_media"][language]
			type_folder = self.media_dictionary["media_type"]["plural"][language]

			# Watched media folder
			folder = self.current_year["folders"][full_language]["root"]

			self.current_year["folders"][full_language][root_folder] = {
				"root": folder + root_folder + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][root_folder]["root"])

			# Media type folder
			folder = self.current_year["folders"][full_language][root_folder]["root"]

			self.current_year["folders"][full_language][root_folder][type_folder] = {
				"root": folder + type_folder + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][root_folder][type_folder]["root"])

			# Watched media file
			folder = self.current_year["folders"][full_language][root_folder][type_folder]["root"]
			file_name = self.media_dictionary["Entry"]["Name"]["Sanitized"]
			self.current_year["folders"][full_language][root_folder][type_folder][file_name] = folder + file_name + ".txt"

			self.File.Create(self.current_year["folders"][full_language][root_folder][type_folder][file_name])

			self.File.Edit(self.current_year["folders"][full_language][root_folder][type_folder][file_name], self.media_dictionary["Entry"]["Text"][language], "w")

			# Firsts Of The Year subfolder folder
			firsts_of_the_year_text = self.JSON.Language.texts["firsts_of_the_year"][language]
			subfolder_name = self.texts["media, title()"][language]

			folder = self.current_year["folders"][full_language][firsts_of_the_year_text]["root"]

			self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name] = {
				"root": folder + subfolder_name + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name]["root"])

			# Firsts Of The Year media type folder
			folder = self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name]["root"]
			type_folder = self.media_dictionary["media_type"]["singular"][language]

			self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder] = {
				"root": folder + type_folder + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder]["root"])

			# First media type entry in year file
			if self.media_dictionary["Media"]["States"]["First media type entry in year"] == True:
				folder = self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder]["root"]

				self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name] = folder + file_name + ".txt"
				self.File.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name])

				self.File.Edit(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name], self.media_dictionary["Entry"]["Text"][language], "w")

	def Define_Diary_Slim_Text(self):
		template = self.language_texts["i_just_finished_watching_{}"]

		if self.media_dictionary["Media"]["States"]["series_media"] == True:
			template += ' "{}"'

			text = self.media_dictionary["media_type"]["genders"][self.user_language]["of_the"]

			if self.media_dictionary["Media"]["States"]["video"] == True:
				text = self.media_types["genders"][self.user_language]["masculine"]["of_the"]

			# Add unit and "of the" text
			self.watched_item_text = self.language_texts["this_{}_{}"].format(self.media_dictionary["Media"]["texts"]["unit"][self.user_language], text)

			# Replaced "watching" with "re-watching" text
			if self.media_dictionary["Media"]["States"]["Re-watching"] == True:
				template = template.replace(self.language_texts["watching, infinitive"], self.language_texts["re_watching, infinitive"])

				template = template.replace(self.language_texts["re_watching, infinitive"], self.language_texts["re_watching, infinitive"] + " " + self.media_dictionary["Media"]["episode"]["re_watched"]["time_text"][self.user_language])

			if self.media_dictionary["Media"]["States"]["single_unit"] == False:
				# Replace "this" text with "the first" if the episode is the first one
				if self.media_dictionary["Media"]["episode"]["title"] == self.media_dictionary["Media"]["item"]["episodes"]["titles"][self.media_dictionary["Media"]["Language"]][0]:
					self.watched_item_text = self.watched_item_text.replace(self.language_texts["this, masculine"], self.language_texts["the_first, masculine"])

				# Replace "this" text with "the last" if the episode is the last one
				if self.media_dictionary["Media"]["episode"]["title"] == self.media_dictionary["Media"]["item"]["episodes"]["titles"][self.media_dictionary["Media"]["Language"]][-1] or len(self.media_dictionary["Media"]["item"]["episodes"]["titles"][self.media_dictionary["Media"]["Language"]]) == 1:
					self.watched_item_text = self.watched_item_text.replace(self.language_texts["this, masculine"], self.language_texts["the_last, masculine"])

			if "Movie" in self.media_dictionary["Media"]["episode"]["titles"][self.media_dictionary["Media"]["Language"]]:
				self.watched_item_text = self.watched_item_text.replace(self.language_texts["episode"], self.language_texts["movie"])

			self.of_the_text = self.language_texts["of_the_{}"]

			if self.media_dictionary["Media"]["States"]["media_list"] == True and self.media_dictionary["Media"]["item"]["title"] != self.media_dictionary["Media"]["title"] and self.media_dictionary["Media"]["States"]["single_unit"] == False:
				if self.media_dictionary["Media"]["States"]["video"] == False:
					text = ""

					# Replace "of the" text with "of the first" if the media item is the first one
					if self.media_dictionary["Media"]["item"]["title"] == self.media_dictionary["Media"]["items"]["list"][0]:
						text = " " + self.language_texts["first, feminine"]

					# Replace "of the" text with "of the last" if the media item is the last one
					if self.media_dictionary["Media"]["item"]["title"] == self.media_dictionary["Media"]["items"]["list"][-1]:
						text = " " + self.language_texts["last, feminine"]

					# Add item text ("season" or "series") to "of the" text
					self.of_the_text = self.of_the_text.format(text + self.media_dictionary["Media"]["texts"]["item"][self.user_language])

				if self.media_dictionary["Media"]["States"]["video"] == True:
					self.of_the_text = self.of_the_text.format(self.language_texts["video_serie"])

				# Add "of the" text next to unit ("episode" or "video") text
				self.watched_item_text = self.watched_item_text.replace(self.media_dictionary["Media"]["texts"]["unit"][self.user_language], self.media_dictionary["Media"]["texts"]["unit"][self.user_language] + " {}".format(self.of_the_text))

				# Add media item title to "of the" text
				self.watched_item_text = self.watched_item_text.replace(self.of_the_text, self.of_the_text + ' "' + self.media_dictionary["Media"]["item"]["title"] + '"')

				# Replace media title with space in media item if it exists
				if self.media_dictionary["Media"]["title"] + " " in self.media_dictionary["Media"]["item"]:
					self.watched_item_text = self.watched_item_text.replace(self.media_dictionary["Media"]["title"] + " ", "")

			# Add container (media type or "YouTube channel" text for video media type) to watched item text
			self.watched_item_text += " " + self.media_dictionary["Media"]["texts"]["container_text"]["container"]

			# Define Diary Slim text as the template formatted with the "watched item text" and the media title per language
			self.media_dictionary["Entry"]["Diary Slim"]["Text"] = template.format(self.watched_item_text, self.media_dictionary["Media"]["titles"]["language"])

		# If the media is a movie, only add the "this" text and the media type "movie" text in user language
		if self.media_dictionary["Media"]["States"]["series_media"] == False:
			self.media_dictionary["Entry"]["Diary Slim"]["Text"] = template.format(self.media_dictionary["media_type"]["genders"][self.user_language]["this"] + " " + self.media_dictionary["media_type"]["singular"][self.user_language].lower())

		# Add language media episode (or movie title)
		if self.media_dictionary["Media"]["States"]["single_unit"] == False:
			self.media_dictionary["Entry"]["Diary Slim"]["Text"] += ":\n" + self.media_dictionary["Media"]["episode"]["titles"][self.media_dictionary["Media"]["Language"]]

		if self.media_dictionary["Media"]["States"]["single_unit"] == True:
			self.media_dictionary["Entry"]["Diary Slim"]["Text"] += ":\n" + self.media_dictionary["Media"]["episode"]["with_title"][self.media_dictionary["Media"]["Language"]]

		if self.media_dictionary["Media"]["States"]["Re-watching"] == True:
			self.media_dictionary["Entry"]["Diary Slim"]["Text"] += self.media_dictionary["Media"]["episode"]["re_watched"]["text"]

		# Add YouTube video link for video media
		if self.media_dictionary["Media"]["States"]["video"] == True:
			self.media_dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.media_dictionary["Media"]["episode"]["remote"]["link"]

		self.media_dictionary["Entry"]["Diary Slim"]["Text"] = self.media_dictionary["Entry"]["Times"]["Timezone"] + ":\n" + self.media_dictionary["Entry"]["Diary Slim"]["Text"]

	def Check_Media_Status(self):
		if self.media_dictionary["Media"]["States"]["series_media"] == True:
			# If the media has a media list and the episode title is the last one
			if self.media_dictionary["Media"]["States"]["media_list"] == True and self.media_dictionary["Media"]["episode"]["title"] == self.media_dictionary["Media"]["item"]["episodes"]["titles"][self.media_dictionary["Media"]["Language"]][-1]:
				# And the episode is not a video
				if self.media_dictionary["Media"]["States"]["video"] == False:
					# If the media item is the last media item, define the media as completed
					if self.media_dictionary["Media"]["item"]["title"] == self.media_dictionary["Media"]["items"]["list"][-1]:
						self.media_dictionary["Media"]["States"]["Completed media"] = True

					# If the media item is not the last media item (media is not completed), get next media item
					if self.media_dictionary["Media"]["item"]["title"] != self.media_dictionary["Media"]["items"]["list"][-1]:
						title = self.media_dictionary["Media"]["items"]["list"][self.media_dictionary["Media"]["item"]["number"] + 1]

						# Define next media item
						self.media_dictionary["Media"]["item"]["next"] = {
							"title": title,
							"sanitized": self.Sanitize_Title(title),
							"titles": {},
							"folders": {
								"root": self.media_dictionary["Media"]["items"]["folders"]["root"] + self.Sanitize_Title(title) + "/",
								"media": self.media_dictionary["Media"]["folders"]["media"]["root"] + self.Sanitize_Title(title) + "/",
								"media_type_comments": {
									"root": self.media_dictionary["Media"]["folders"]["media_type_comments"]["root"] + self.Sanitize_Title(title) + "/"
								}
							},
							"number": self.media_dictionary["Media"]["item"]["number"] + 1
						}

						# Define local media dictionary to update it
						dictionary = {
							"texts": {
								"select": "",
							},
							"media_type": self.media_dictionary["media_type"],
							"Media": self.media_dictionary["Media"]["item"]["next"]
						}

						# Update the titles and folders of the next media item dictionary
						self.media_dictionary["Media"]["item"]["next"] = self.Select_Media(dictionary)["Media"]

						# Update current media item file
						self.File.Edit(self.media_dictionary["Media"]["items"]["folders"]["current"], self.media_dictionary["Media"]["item"]["next"]["title"], "w")

				self.media_dictionary["Media"]["States"]["Completed media item"] = True

			# If the media has no media list and the episode title is the last one, define the media as completed
			if self.media_dictionary["Media"]["States"]["media_list"] == False and self.media_dictionary["Media"]["episode"]["title"] == self.media_dictionary["Media"]["item"]["episodes"]["titles"][self.media_dictionary["Media"]["Language"]][-1]:
				self.media_dictionary["Media"]["States"]["Completed media"] = True

		# If the media is a movie, define it as completed
		if self.media_dictionary["Media"]["States"]["series_media"] == False:
			self.media_dictionary["Media"]["States"]["Completed media"] = True

		# If the media and media item are not completed, get next episode number
		if self.media_dictionary["Media"]["States"]["Completed media"] == False and self.media_dictionary["Media"]["States"]["Completed media item"] == False:
			# Get next episode language title
			self.media_dictionary["Media"]["episode"]["next"] = self.media_dictionary["Media"]["item"]["episodes"]["titles"][self.media_dictionary["Media"]["Language"]][self.media_dictionary["Media"]["episode"]["number"]]

			# Add hybrid origin type to episode title
			if self.media_dictionary["Media"]["States"]["hybrid"] == True:
				self.media_dictionary["Media"]["episode"]["next"] += self.media_dictionary["Media"]["episode"]["hybrid_origin_type"]

			# Define current episode to watch as the next episode
			self.media_dictionary["Media"]["item"]["details"][self.language_texts["episode, title()"]] = self.media_dictionary["Media"]["episode"]["next"]

			# Update media item details file
			self.File.Edit(self.media_dictionary["Media"]["item"]["folders"]["details"], self.Text.From_Dictionary(self.media_dictionary["Media"]["item"]["details"]), "w")

		# If the media is completed, define its status as completed
		if self.media_dictionary["Media"]["States"]["Completed media"] == True:
			if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"] and self.media_dictionary["Media"]["details"][self.language_texts["remote_origin, title()"]] == "Animes Vision":
				self.media_dictionary["Media"]["details"].pop(self.language_texts["remote_origin, title()"])

			if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["videos"]["en"] and self.media_dictionary["Media"]["details"][self.language_texts["remote_origin, title()"]] == "YouTube":
				self.media_dictionary["Media"]["details"].pop(self.language_texts["remote_origin, title()"])

			# Update status key in media details
			self.Change_Status(self.media_dictionary)

	def Set_Media_As_Completed(self):
		# Completed media and media item time and date part
		template = self.language_texts["when_i_finished_watching"] + " {}:" + "\n" + \
		self.media_dictionary["Entry"]["Times"]["Timezone"] + "\n" + \
		"\n" + \
		self.Date.language_texts["duration, title()"] + ":" + "\n" + \
		"{}"

		# Gets the date that the user started and finished watching the media item and writes it into the media item dates file
		if self.media_dictionary["Media"]["States"]["Completed media item"] == True:
			# Gets the item dates from the item dates file
			self.media_dictionary["Media"]["item"]["dates"] = self.File.Dictionary(self.media_dictionary["Media"]["item"]["folders"]["dates"], next_line = True)

			if self.media_dictionary["Media"]["States"]["single_unit"] == True:
				key = self.language_texts["when_i_started_to_watch"] + " " + self.media_dictionary["Media"]["texts"]["the_item"][self.user_language]

				self.media_dictionary["Media"]["item"]["dates"][key] = self.media_dictionary["Entry"]["Times"]["Timezone"]

			key = self.language_texts["when_i_started_to_watch"] + " " + self.media_dictionary["Media"]["texts"]["the_item"][self.user_language]

			# Get started watching time
			self.media_dictionary["Media"]["item"]["started_watching_item"] = self.media_dictionary["Media"]["item"]["dates"][key]

			# Define time spent watching using started watching time and finished watching time
			self.media_dictionary["Media"]["item"]["time_spent_watching"] = self.Date.Difference(self.media_dictionary["Media"]["item"]["started_watching_item"], self.media_dictionary["Entry"]["Time"])["difference_strings"][self.user_language]

			if self.media_dictionary["Media"]["item"]["time_spent_watching"][0] + self.media_dictionary["Media"]["item"]["time_spent_watching"][1] == ", ":
				self.media_dictionary["Media"]["item"]["time_spent_watching"] = self.media_dictionary["Media"]["item"]["time_spent_watching"][2:]

			# Format the time template
			self.media_dictionary["Media"]["item"]["formatted_template"] = "\n\n" + template.format(self.media_dictionary["Media"]["texts"]["the_item"][self.user_language], self.media_dictionary["Media"]["item"]["time_spent_watching"])

			# Add the time template to the item dates text
			self.media_dictionary["Media"]["item"]["finished_watching_text"] = self.File.Contents(self.media_dictionary["Media"]["item"]["folders"]["dates"])["string"] + self.media_dictionary["Media"]["item"]["formatted_template"]

			# Update item dates text file
			self.File.Edit(self.media_dictionary["Media"]["item"]["folders"]["dates"], self.media_dictionary["Media"]["item"]["finished_watching_text"], "w")

			text = self.media_dictionary["Media"]["item"]["finished_watching_text"]
			text = text.replace(self.language_texts["when_i_started_to_watch"] + " " + self.media_dictionary["Media"]["texts"]["the_item"][self.user_language], self.language_texts["when_i_started_to_watch"])
			text = text.replace(self.language_texts["when_i_finished_watching"] + " " + self.media_dictionary["Media"]["texts"]["the_item"][self.user_language], self.language_texts["when_i_finished_watching"])

			# Add the time template to the Diary Slim text if the media is not completed
			if self.media_dictionary["Media"]["States"]["Completed media"] == False and self.media_dictionary["Media"]["States"]["single_unit"] == False:
				self.media_dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + text

		# Gets the date that the user started and finished watching the media and writes it to the media dates text file
		if self.media_dictionary["Media"]["States"]["Completed media"] == True:
			# Gets the media dates from the media dates file
			self.media_dictionary["Media"]["dates"] = self.File.Dictionary(self.media_dictionary["Media"]["folders"]["dates"], next_line = True)

			key = self.language_texts["when_i_started_to_watch"] + " " + self.media_dictionary["Media"]["texts"]["genders"][self.user_language]["the"] + " " + self.media_dictionary["Media"]["texts"]["container"][self.user_language].lower()

			# Get started watching time
			self.media_dictionary["Media"]["started_watching"] = self.Date.From_String(self.media_dictionary["Media"]["dates"][key])

			# Define time spent watching using started watching time and finished watching time
			self.media_dictionary["Media"]["time_spent_watching"] = self.Date.Difference(self.media_dictionary["Media"]["started_watching"], self.media_dictionary["Entry"]["Time"])["difference_strings"][self.user_language]

			if self.media_dictionary["Media"]["time_spent_watching"][0] + self.media_dictionary["Media"]["time_spent_watching"][1] == ", ":
				self.media_dictionary["Media"]["time_spent_watching"] = self.media_dictionary["Media"]["time_spent_watching"][2:]

			# Format the time template
			self.media_dictionary["Media"]["item"]["formatted_template"] = "\n\n" + template.format(self.media_dictionary["Media"]["texts"]["container_text"]["the"], self.media_dictionary["Media"]["time_spent_watching"])

			# Add the time template to the media dates text
			self.media_dictionary["Media"]["finished_watching_text"] = self.File.Contents(self.media_dictionary["Media"]["folders"]["dates"])["string"] + self.media_dictionary["Media"]["item"]["formatted_template"]

			# Update media dates text file
			self.File.Edit(self.media_dictionary["Media"]["folders"]["dates"], self.media_dictionary["Media"]["finished_watching_text"], "w")

			text = self.media_dictionary["Media"]["finished_watching_text"]
			text = text.replace(self.language_texts["when_i_started_to_watch"] + " " + self.media_dictionary["Media"]["texts"]["container_text"]["the"], self.language_texts["when_i_started_to_watch"])
			text = text.replace(self.language_texts["when_i_finished_watching"] + " " + self.media_dictionary["Media"]["texts"]["container_text"]["the"], self.language_texts["when_i_finished_watching"])

			# Add the time template to the Diary Slim text
			self.media_dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + text

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

		if self.media_dictionary["Media"]["States"]["series_media"] == False:
			text = text.replace(self.language_texts["a_screenshot_of_the_episode"], self.language_texts["movie"])

		if self.media_dictionary["Media"]["title"] in ["The Walking Dead", "Yuru Camp"]:
			text = text.replace(self.language_texts["a_screenshot_of_the_episode"], self.language_texts["a_summary_video"])

		self.posted_on_social_networks_text_template = self.language_texts["i_posted_the_watched_text_and_{}_on_the_status_of_{}_and_tweet_on_{}"] + "."

		self.media_dictionary["Entry"]["Diary Slim"]["posted_on_social_networks"] = self.posted_on_social_networks_text_template.format(text, self.first_three_social_networks, self.twitter_social_network)

		text = self.language_texts["post_on_the_social_networks"] + " (" + self.social_networks_string + ")"

		self.media_dictionary["Entry"]["post_on_social_networks"] = self.Input.Yes_Or_No(text)

		if self.media_dictionary["Entry"]["post_on_social_networks"] == True:
			from Social_Networks.Open_Social_Network import Open_Social_Network as Open_Social_Network

			Open_Social_Network(option_info = {"type": "profile"}, social_network_parameter = "WhatsApp", first_space = False, second_space = False)

			self.Input.Type(self.language_texts["press_enter_to_copy_the_watched_text"])

			self.Text.Copy(self.media_dictionary["Entry"]["Diary Slim"]["Text"])

		print()
		print("-----")
		print()

	def Write_On_Diary_Slim(self):
		# Add "Posted on Social Networks" text if the user wanted to post the entry text on the Social Networks
		if self.media_dictionary["Entry"]["post_on_social_networks"] == True:
			self.media_dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.media_dictionary["Entry"]["Diary Slim"]["posted_on_social_networks"]

		add_dot = True

		if self.media_dictionary["Entry"]["post_on_social_networks"] == False and self.media_dictionary["Media"]["States"]["video"] == True:
			add_dot = False

		from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

		Write_On_Diary_Slim_Module(self.media_dictionary["Entry"]["Diary Slim"]["Text"], add_time = False, add_dot = add_dot)

	def Show_Information(self):
		self.media_dictionary["header_text"] = self.Text.Capitalize(self.media_dictionary["Media"]["texts"]["container_text"]["container"]) + ": "

		if self.media_dictionary["Media"]["States"]["Completed media"] == True:
			text = self.media_dictionary["Media"]["texts"]["container_text"]["this"]
			self.media_dictionary["header_text"] = self.language_texts["you_finished_watching_{}"].format(text) + ": "

		self.Show_Media_Information(self.media_dictionary)