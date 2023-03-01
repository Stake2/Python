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
				"Text": ""
			}
		})

		if self.dictionary["Entry"]["Time"] != {}:
			self.dictionary["Entry"]["Times"] = {
				"UTC": self.Date.To_String(self.dictionary["Entry"]["Time"]["utc"]),
				"Timezone": self.Date.To_Timezone(self.dictionary["Entry"]["Time"])["hh:mm DD/MM/YYYY"]
			}

		# Database related methods
		self.Register_In_JSON()
		self.Create_Entry_File()
		self.Add_Entry_File_To_Year_Folder()

		self.Define_Diary_Slim_Text()

		self.Check_Media_Status()

		if self.dictionary["Media"]["States"]["Re-watching"] == False:
			if self.dictionary["Media"]["States"]["Completed media"] == True or self.dictionary["Media"]["States"]["Completed media item"] == True:
				self.Set_Media_As_Completed()

		if "Old history" not in self.dictionary["Media"]["States"]:
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
		self.media_type = self.dictionary["media_type"]["plural"]["en"]

		self.dictionaries["Watched"] = self.JSON.To_Python(self.dictionary["Media"]["item"]["folders"]["watched"]["entries"])

		# Add to watched episode, root episode and media type episode numbers
		self.dictionaries["Entries"]["Numbers"]["Total"] += 1
		self.dictionaries["Watched"]["Numbers"]["Total"] += 1
		self.dictionaries["Media Type"][self.media_type]["Numbers"]["Total"] += 1

		# Define sanitized version of entry name for files
		self.dictionary["Entry"]["Name"] = {
			"Normal": str(self.dictionaries["Entries"]["Numbers"]["Total"]) + ". " + self.media_type,
			"Sanitized": ""
		}

		if "Timezone" in self.dictionary["Entry"]["Times"]:
			self.dictionary["Entry"]["Name"]["Normal"] += " (" + self.dictionary["Entry"]["Times"]["Timezone"] + ")"

		self.dictionary["Entry"]["Name"]["Sanitized"] = self.dictionary["Entry"]["Name"]["Normal"].replace(":", ";").replace("/", "-")

		# Add to "Entries" list
		self.dictionaries["Entries"]["Entries"].append(self.dictionary["Entry"]["Name"]["Normal"])
		self.dictionaries["Media Type"][self.media_type]["Entries"].append(self.dictionary["Entry"]["Name"]["Normal"])
		self.dictionaries["Watched"]["Entries"].append(self.dictionary["Entry"]["Name"]["Normal"])

		# Define local media and media item titles to remove some keys from them
		media_titles = self.dictionary["Media"]["titles"].copy()
		item_titles = self.dictionary["Media"]["item"]["titles"].copy()

		for dictionary in [media_titles, item_titles]:
			dictionary.pop("language")

			for key in ["ja", "sanitized"]:
				if key in dictionary:
					dictionary.pop(key)

		self.key = self.dictionary["Entry"]["Name"]["Normal"]

		# Add Entry dictionary to Entries dictionary
		self.dictionaries["Entries"]["Dictionary"][self.key] = {
			"Number": self.dictionaries["Entries"]["Numbers"]["Total"],
			"Type number": self.dictionaries["Media Type"][self.media_type]["Numbers"]["Total"],
			"Entry": self.dictionary["Entry"]["Name"]["Normal"],
			"Media": media_titles,
			"Item": item_titles,
			"Episode": {
				"Number": 1,
				"Titles": self.dictionary["Media"]["episode"]["titles"]
			},
			"Type": self.media_type,
			"Time": ""
		}

		if "UTC" in self.dictionary["Entry"]["Times"]:
			self.dictionaries["Entries"]["Dictionary"][self.key]["Time"] = self.dictionary["Entry"]["Times"]["UTC"]

		# Remove the media item dictionary if the media has not media item list, the media item title is the same as the media title, or the media is non-series media
		if self.dictionary["Media"]["States"]["Media item list"] == False or self.dictionary["Media"]["item"]["title"] == self.dictionary["Media"]["title"] or self.dictionary["Media"]["States"]["series_media"] == False:
			self.dictionaries["Entries"]["Dictionary"][self.key].pop("Item")

		# Remove episode titles and number keys of dictionary if media is non-series media or single unit
		if self.dictionary["Media"]["States"]["series_media"] == False or self.dictionary["Media"]["States"]["single_unit"] == False:
			self.dictionaries["Entries"]["Dictionary"][self.key].pop("Episode")

		# Define episode number on dictionary if media is series media and not single unit
		if self.dictionary["Media"]["States"]["series_media"] == True and self.dictionary["Media"]["States"]["single_unit"] == False:
			self.dictionaries["Entries"]["Dictionary"][self.key]["Episode"]["Number"] = self.dictionary["Media"]["episode"]["number"]

		# Add episode ID if the key is present inside the episode dictionary
		if "id" in self.dictionary["Media"]["episode"]:
			self.dictionaries["Entries"]["Dictionary"][self.key]["ID"] = self.dictionary["Media"]["episode"]["id"]

			# Add episode link
			if "remote" in self.dictionary["Media"]["episode"]:
				self.dictionaries["Entries"]["Dictionary"][self.key]["Link"] = self.dictionary["Media"]["episode"]["remote"]["link"]

		# Add the "Comment" dictionary if it exists
		if "Comment" in self.dictionary["Comment Writer"]:
			self.dictionaries["Entries"]["Dictionary"][self.key]["Comment"] = self.dictionary["Comment Writer"]["Comment"]

		# Get the States dictionary
		self.states_dictionary = self.Define_States_Dictionary(self.dictionary)

		# Add the States dictionary into the Entry dictionary if it is not empty
		if self.states_dictionary != {}:
			self.dictionaries["Entries"]["Dictionary"][self.key]["States"] = self.states_dictionary["States"]

		# Add entry dictionary to media type entry dictionary
		self.dictionaries["Media Type"][self.media_type]["Dictionary"][self.key] = self.dictionaries["Entries"]["Dictionary"][self.key].copy()

		# Define "Watched" entry dictionary as media type entry dictionary
		self.dictionaries["Watched"]["Dictionary"][self.key] = self.dictionaries["Media Type"][self.media_type]["Dictionary"][self.key]

		# Get Comments dictionary from file
		self.dictionaries["Comments"] = self.JSON.To_Python(self.folders["comments"]["comments"])

		# Get year comment number from "Comments.json" file
		self.dictionaries["Entries"]["Numbers"]["Comments"] = self.dictionaries["Comments"]["Numbers"]["Years"][self.current_year["Number"]]

		# Get year media type comment number from "Comments.json" file
		self.dictionaries["Media Type"][self.media_type]["Numbers"]["Comments"] = self.dictionaries["Comments"]["Numbers"]["Type"][self.media_type]["Years"][self.current_year["Number"]]

		# Add to media comments number
		if self.dictionary["Comment Writer"]["States"]["write"] == True:
			self.dictionaries["Watched"]["Numbers"]["Comments"] += 1

		# Update "Entries.json" file
		self.JSON.Edit(self.folders["watch_history"]["current_year"]["entries"], self.dictionaries["Entries"])

		# Update media type "Entries.json" file
		self.JSON.Edit(self.dictionary["media_type"]["folders"]["per_media_type"]["entries"], self.dictionaries["Media Type"][self.media_type])

		# Update media "Watched.json" file
		self.JSON.Edit(self.dictionary["Media"]["item"]["folders"]["watched"]["entries"], self.dictionaries["Watched"])

		# Add to root and media type "Entry list.txt" file
		self.File.Edit(self.folders["watch_history"]["current_year"]["entry_list"], self.dictionary["Entry"]["Name"]["Normal"], "a")
		self.File.Edit(self.dictionary["media_type"]["folders"]["per_media_type"]["entry_list"], self.dictionary["Entry"]["Name"]["Normal"], "a")

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
		file = self.dictionary["Media"]["item"]["folders"]["watched"]["files"]["root"] + self.dictionary["Entry"]["Name"]["Normal"] + ".txt"

		self.File.Create(file)
		self.File.Edit(file, self.dictionary["Entry"]["Text"][self.user_language], "w")

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
		if self.dictionary["Media"]["States"]["series_media"] == True:
			if self.dictionary["Media"]["States"]["Media item list"] == True and self.dictionary["Media"]["item"]["title"] != self.dictionary["Media"]["title"]:
				lines.append(self.texts["item, title()"][language] + ":" + "\n" + "{}")

			if self.dictionary["Media"]["States"]["single_unit"] == False:
				text = self.texts["episode_titles"][language]

				if language_parameter != "General":
					text = self.texts["episode_title"][language]

				if self.dictionary["Media"]["States"]["video"] == True:
					text = self.texts["video_titles"][language]

				lines.append(text + ":" + "\n" + "{}")

		lines_to_add = [
			self.JSON.Language.texts["type, title()"][language] + ": " + self.dictionary["media_type"]["plural"]["en"] + "\n"
		]

		if self.dictionary["Entry"]["Times"] != {}:
			lines_to_add.append(self.Date.texts["times, title()"][language] + ":" + "\n" + "{}")

		lines_to_add.append(self.File.texts["file_name"][language] + ": " + self.dictionary["Entry"]["Name"]["Normal"])

		lines.extend(lines_to_add)

		# Add states texts lines
		if self.states_dictionary != {}:
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
		key = "original"

		if self.dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"] and "romanized" in self.dictionary["Media"]["titles"]:
			key = "romanized"

		titles += self.dictionary["Media"]["titles"][key]

		if self.dictionary["Media"]["titles"]["language"] != self.dictionary["Media"]["titles"][key]:
			titles += "\n" + self.dictionary["Media"]["titles"]["language"]

		items.append(titles + "\n")

		if self.dictionary["Media"]["States"]["series_media"] == True:
			# Add media item titles to media item titles list
			if self.dictionary["Media"]["States"]["Media item list"] == True and self.dictionary["Media"]["item"]["title"] != self.dictionary["Media"]["title"]:
				key = "original"

				if self.dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"] and "romanized" in self.dictionary["Media"]["item"]["titles"]:
					key = "romanized"

				item_titles = self.dictionary["Media"]["item"]["titles"][key]

				if self.dictionary["Media"]["item"]["titles"]["language"] != self.dictionary["Media"]["item"]["titles"][key]:
					item_titles += "\n" + self.dictionary["Media"]["item"]["titles"]["language"]

				items.append(item_titles + "\n")

			if self.dictionary["Media"]["States"]["single_unit"] == False:
				# Add episode titles to episode titles list
				episode_titles = ""

				if language_parameter != "General":
					episode_title = self.dictionary["Media"]["episode"]["titles"][language]

					if episode_title == "":
						episode_title = "[" + self.JSON.Language.texts["empty, title()"][language] + "]"

					episode_titles = episode_title + "\n"

				if language_parameter == "General":
					for language in self.languages["small"]:
						episode_title = self.dictionary["Media"]["episode"]["titles"][language]

						if episode_title == "":
							episode_title = "[" + self.JSON.Language.texts["empty, title()"][language] + "]"

						episode_titles += episode_title + "\n"

				items.append(episode_titles)

		if self.Date.texts["times, title()"][language] + ":" + "\n" + "{}" in lines:
			# Add times to items list
			times = ""

			for key in ["UTC", "Timezone"]:
				if key in self.dictionary["Entry"]["Times"]:
					time = self.dictionary["Entry"]["Times"][key]

					times += time + "\n"

			if times != "":
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
			file_name = self.dictionary["Entry"]["Name"]["Sanitized"]
			self.current_year["folders"][full_language][root_folder][type_folder][file_name] = folder + file_name + ".txt"

			self.File.Create(self.current_year["folders"][full_language][root_folder][type_folder][file_name])

			self.File.Edit(self.current_year["folders"][full_language][root_folder][type_folder][file_name], self.dictionary["Entry"]["Text"][language], "w")

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
			type_folder = self.dictionary["media_type"]["singular"][language]

			self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder] = {
				"root": folder + type_folder + "/"
			}

			self.Folder.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder]["root"])

			# First media type entry in year file
			if self.dictionary["Media"]["States"]["First media type entry in year"] == True:
				folder = self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder]["root"]

				self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name] = folder + file_name + ".txt"
				self.File.Create(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name])

				self.File.Edit(self.current_year["folders"][full_language][firsts_of_the_year_text][subfolder_name][type_folder][file_name], self.dictionary["Entry"]["Text"][language], "w")

	def Define_Diary_Slim_Text(self):
		template = self.language_texts["i_just_finished_watching_{}"]

		if self.dictionary["Media"]["States"]["series_media"] == True:
			template += ' "{}"'

			text = self.dictionary["media_type"]["genders"][self.user_language]["of_the"]

			if self.dictionary["Media"]["States"]["video"] == True:
				text = self.media_types["genders"][self.user_language]["masculine"]["of_the"]

			# Add unit and "of the" text
			self.watched_item_text = self.language_texts["this_{}_{}"].format(self.dictionary["Media"]["texts"]["unit"][self.user_language], text)

			# Replaced "watching" with "re-watching" text
			if self.dictionary["Media"]["States"]["Re-watching"] == True:
				template = template.replace(self.language_texts["watching, infinitive"], self.language_texts["re_watching, infinitive"])

				template = template.replace(self.language_texts["re_watching, infinitive"], self.language_texts["re_watching, infinitive"] + " " + self.dictionary["Media"]["episode"]["re_watched"]["time_text"][self.user_language])

			if self.dictionary["Media"]["States"]["single_unit"] == False:
				# Replace "this" text with "the first" if the episode is the first one
				if self.dictionary["Media"]["episode"]["title"] == self.dictionary["Media"]["item"]["episodes"]["titles"][self.dictionary["Media"]["Language"]][0]:
					self.watched_item_text = self.watched_item_text.replace(self.language_texts["this, masculine"], self.language_texts["the_first, masculine"])

				# Replace "this" text with "the last" if the episode is the last one
				if self.dictionary["Media"]["episode"]["title"] == self.dictionary["Media"]["item"]["episodes"]["titles"][self.dictionary["Media"]["Language"]][-1] or len(self.dictionary["Media"]["item"]["episodes"]["titles"][self.dictionary["Media"]["Language"]]) == 1:
					self.watched_item_text = self.watched_item_text.replace(self.language_texts["this, masculine"], self.language_texts["the_last, masculine"])

			if "Movie" in self.dictionary["Media"]["episode"]["titles"][self.dictionary["Media"]["Language"]]:
				self.watched_item_text = self.watched_item_text.replace(self.language_texts["episode"], self.language_texts["movie"])

			self.of_the_text = self.language_texts["of_the_{}"]

			if self.dictionary["Media"]["States"]["Media item list"] == True and self.dictionary["Media"]["item"]["title"] != self.dictionary["Media"]["title"] and self.dictionary["Media"]["States"]["single_unit"] == False:
				if self.dictionary["Media"]["States"]["video"] == False:
					text = ""

					# Replace "of the" text with "of the first" if the media item is the first one
					if self.dictionary["Media"]["item"]["title"] == self.dictionary["Media"]["items"]["list"][0]:
						text = " " + self.language_texts["first, feminine"]

					# Replace "of the" text with "of the last" if the media item is the last one
					if self.dictionary["Media"]["item"]["title"] == self.dictionary["Media"]["items"]["list"][-1]:
						text = " " + self.language_texts["last, feminine"]

					# Add item text ("season" or "series") to "of the" text
					self.of_the_text = self.of_the_text.format(text + self.dictionary["Media"]["texts"]["item"][self.user_language])

				if self.dictionary["Media"]["States"]["video"] == True:
					self.of_the_text = self.of_the_text.format(self.language_texts["video_serie"])

				# Add "of the" text next to unit ("episode" or "video") text
				self.watched_item_text = self.watched_item_text.replace(self.dictionary["Media"]["texts"]["unit"][self.user_language], self.dictionary["Media"]["texts"]["unit"][self.user_language] + " {}".format(self.of_the_text))

				# Add media item title to "of the" text
				self.watched_item_text = self.watched_item_text.replace(self.of_the_text, self.of_the_text + ' "' + self.dictionary["Media"]["item"]["title"] + '"')

				# Replace media title with space in media item if it exists
				if self.dictionary["Media"]["title"] + " " in self.dictionary["Media"]["item"]:
					self.watched_item_text = self.watched_item_text.replace(self.dictionary["Media"]["title"] + " ", "")

			# Add container (media type or "YouTube channel" text for video media type) to watched item text
			self.watched_item_text += " " + self.dictionary["Media"]["texts"]["container_text"]["container"]

			# Define Diary Slim text as the template formatted with the "watched item text" and the media title per language
			self.dictionary["Entry"]["Diary Slim"]["Text"] = template.format(self.watched_item_text, self.dictionary["Media"]["titles"]["language"])

		# If the media is a movie, only add the "this" text and the media type "movie" text in user language
		if self.dictionary["Media"]["States"]["series_media"] == False:
			self.dictionary["Entry"]["Diary Slim"]["Text"] = template.format(self.dictionary["media_type"]["genders"][self.user_language]["this"] + " " + self.dictionary["media_type"]["singular"][self.user_language].lower())

		# Add language media episode (or movie title)
		if self.dictionary["Media"]["States"]["single_unit"] == False:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += ":\n"

			if self.dictionary["Media"]["Language"] in self.dictionary["Media"]["episode"]["titles"]:
				title = self.dictionary["Media"]["episode"]["titles"][self.dictionary["Media"]["Language"]]

			else:
				title = self.dictionary["Media"]["episode"]["titles"]["language"]

			self.dictionary["Entry"]["Diary Slim"]["Text"] += title

		if self.dictionary["Media"]["States"]["single_unit"] == True:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += ":\n" + self.dictionary["Media"]["episode"]["with_title"][self.dictionary["Media"]["Language"]]

		if self.dictionary["Media"]["States"]["Re-watching"] == True:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += self.dictionary["Media"]["episode"]["re_watched"]["text"]

		# Add media episode link if it exists
		if "remote" in self.dictionary["Media"]["episode"] and "link" in self.dictionary["Media"]["episode"]["remote"]:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.dictionary["Media"]["episode"]["remote"]["link"]

		if "Timezone" in self.dictionary["Entry"]["Times"]:
			time = self.dictionary["Entry"]["Times"]["Timezone"]

		else:
			time = self.Date.Now()["hh:mm DD/MM/YYYY"]

		# Add time
		self.dictionary["Entry"]["Diary Slim"]["Text"] = time + ":\n" + self.dictionary["Entry"]["Diary Slim"]["Text"]

	def Check_Media_Status(self):
		if self.dictionary["Media"]["States"]["series_media"] == True:
			# If the media has a media item list and the episode title is the last one
			if self.dictionary["Media"]["States"]["Media item list"] == True and self.dictionary["Media"]["episode"]["title"] == self.dictionary["Media"]["item"]["episodes"]["titles"][self.dictionary["Media"]["Language"]][-1]:
				# And the episode is not a video
				if self.dictionary["Media"]["States"]["video"] == False:
					# If the media item is the last media item, define the media as completed
					if self.dictionary["Media"]["item"]["title"] == self.dictionary["Media"]["items"]["list"][-1]:
						self.dictionary["Media"]["States"]["Completed media"] = True

					# If the media item is not the last media item (media is not completed), get next media item
					if self.dictionary["Media"]["item"]["title"] != self.dictionary["Media"]["items"]["list"][-1]:
						title = self.dictionary["Media"]["items"]["list"][self.dictionary["Media"]["item"]["number"] + 1]

						# Define next media item
						self.dictionary["Media"]["item"]["next"] = {
							"title": title,
							"sanitized": self.Sanitize_Title(title),
							"titles": {},
							"folders": {
								"root": self.dictionary["Media"]["items"]["folders"]["root"] + self.Sanitize_Title(title) + "/",
								"media": {
									"root": self.dictionary["Media"]["folders"]["media"]["root"] + self.Sanitize_Title(title) + "/"
								}
							},
							"number": self.dictionary["Media"]["item"]["number"] + 1
						}

						# Define local media dictionary to update it
						dictionary = {
							"texts": {
								"select": "",
							},
							"media_type": self.dictionary["media_type"],
							"Media": self.dictionary["Media"]["item"]["next"]
						}

						# Update the titles and folders of the next media item dictionary
						self.dictionary["Media"]["item"]["next"] = self.Select_Media(dictionary)["Media"]

						print(self.dictionary["Media"]["item"]["next"]["details"])

						if "Old history" not in self.dictionary["Media"]["States"]:
							# Update current media item file
							self.File.Edit(self.dictionary["Media"]["items"]["folders"]["current"], self.dictionary["Media"]["item"]["next"]["title"], "w")

					# Add the "Status" key and value "Completed" after the "Link" key
					key_value = {
						"key": self.language_texts["status, title()"],
						"value": self.JSON.Language.language_texts["completed, title()"]
					}

					self.dictionary["Media"]["item"]["details"] = self.JSON.Add_Key_After_Key(self.dictionary["Media"]["item"]["details"], key_value, self.JSON.Language.language_texts["link, title()"])

					if self.language_texts["episode, title()"] in self.dictionary["Media"]["item"]["details"] and self.dictionary["Media"]["States"]["single_unit"] == True:
						self.dictionary["Media"]["item"]["details"].pop(self.language_texts["episode, title()"])

					if "Old history" not in self.dictionary["Media"]["States"]:
						# Update media item details file
						self.File.Edit(self.dictionary["Media"]["item"]["folders"]["details"], self.Text.From_Dictionary(self.dictionary["Media"]["item"]["details"]), "w")

				self.dictionary["Media"]["States"]["Completed media item"] = True

			# If the media has no media item list and the episode title is the last one, define the media as completed
			if self.dictionary["Media"]["States"]["Media item list"] == False and self.dictionary["Media"]["episode"]["title"] == self.dictionary["Media"]["item"]["episodes"]["titles"][self.dictionary["Media"]["Language"]][-1]:
				self.dictionary["Media"]["States"]["Completed media"] = True

		# If the media is a movie, define it as completed
		if self.dictionary["Media"]["States"]["series_media"] == False:
			self.dictionary["Media"]["States"]["Completed media"] = True

		# If the media and media item are not completed, get next episode number
		if self.dictionary["Media"]["States"]["Completed media"] == False and self.dictionary["Media"]["States"]["Completed media item"] == False:
			# Get next episode language title
			self.dictionary["Media"]["episode"]["next"] = self.dictionary["Media"]["item"]["episodes"]["titles"][self.dictionary["Media"]["Language"]][self.dictionary["Media"]["episode"]["number"]]

			# Define current episode to watch as the next episode
			self.dictionary["Media"]["item"]["details"][self.language_texts["episode, title()"]] = self.dictionary["Media"]["episode"]["next"]

			if "Old history" not in self.dictionary["Media"]["States"]:
				# Update media item details file
				self.File.Edit(self.dictionary["Media"]["item"]["folders"]["details"], self.Text.From_Dictionary(self.dictionary["Media"]["item"]["details"]), "w")

		# If the media is completed, define its status as completed
		if self.dictionary["Media"]["States"]["Completed media"] == True:
			if self.dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"] and self.dictionary["Media"]["details"][self.language_texts["remote_origin, title()"]] == "Animes Vision":
				self.dictionary["Media"]["details"].pop(self.language_texts["remote_origin, title()"])

			if self.dictionary["media_type"]["plural"]["en"] == self.texts["videos"]["en"] and self.dictionary["Media"]["details"][self.language_texts["remote_origin, title()"]] == "YouTube":
				self.dictionary["Media"]["details"].pop(self.language_texts["remote_origin, title()"])

			if "Old history" not in self.dictionary["Media"]["States"]:
				# Update status key in media details
				self.Change_Status(self.dictionary)

	def Set_Media_As_Completed(self):
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
		if self.dictionary["Media"]["States"]["Completed media item"] == True and self.dictionary["Entry"]["Time"] != {}:
			# Gets the item dates from the item dates file
			self.dictionary["Media"]["item"]["dates"] = self.File.Dictionary(self.dictionary["Media"]["item"]["folders"]["dates"], next_line = True)

			if "Timezone" not in self.dictionary["Entry"]["Times"]:
				key = self.language_texts["when_i_finished_watching"]

				self.dictionary["Entry"]["Times"]["Timezone"] = self.dictionary["Media"]["item"]["dates"][key]

			key = self.language_texts["when_i_started_to_watch"]

			if self.dictionary["Media"]["States"]["single_unit"] == True:
				self.dictionary["Media"]["item"]["dates"][key] = self.dictionary["Entry"]["Times"]["Timezone"]

			# Get started watching time
			self.dictionary["Media"]["item"]["started_watching_item"] = self.Date.To_UTC(self.Date.From_String(self.dictionary["Media"]["item"]["dates"][key]))

			# Define time spent watching using started watching time and finished watching time
			self.dictionary["Media"]["item"]["time_spent_watching"] = self.Date.Difference(self.dictionary["Media"]["item"]["started_watching_item"], self.dictionary["Entry"]["Time"])["difference_strings"][self.user_language]

			if self.dictionary["Media"]["item"]["time_spent_watching"][0] + self.dictionary["Media"]["item"]["time_spent_watching"][1] == ", ":
				self.dictionary["Media"]["item"]["time_spent_watching"] = self.dictionary["Media"]["item"]["time_spent_watching"][2:]

			# Format the time template
			self.dictionary["Media"]["item"]["formatted_template"] = "\n\n" + template.format(self.dictionary["Media"]["item"]["time_spent_watching"])

			# Add the time template to the item dates text
			self.dictionary["Media"]["item"]["finished_watching_text"] = self.File.Contents(self.dictionary["Media"]["item"]["folders"]["dates"])["string"]

			if "Old history" not in self.dictionary["Media"]["States"]:
				self.dictionary["Media"]["item"]["finished_watching_text"] += self.dictionary["Media"]["item"]["formatted_template"]

				# Update item dates text file
				self.File.Edit(self.dictionary["Media"]["item"]["folders"]["dates"], self.dictionary["Media"]["item"]["finished_watching_text"], "w")

			self.dictionary["Media"]["item"]["finished_watching_text"] = self.dictionary["Media"]["item"]["finished_watching_text"].replace(self.language_texts["when_i_started_to_watch"], self.language_texts["when_i_started_to_watch"] + " " + self.dictionary["Media"]["texts"]["the_item"][self.user_language])

			# Add the time template to the Diary Slim text if the media is not completed
			if self.dictionary["Media"]["States"]["Completed media"] == False and self.dictionary["Media"]["States"]["single_unit"] == False:
				self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.dictionary["Media"]["item"]["finished_watching_text"]

		# Gets the date that the user started and finished watching the media and writes it to the media dates text file
		if self.dictionary["Media"]["States"]["Completed media"] == True and self.dictionary["Entry"]["Time"] != {}:
			# Gets the media dates from the media dates file
			self.dictionary["Media"]["dates"] = self.File.Dictionary(self.dictionary["Media"]["folders"]["dates"], next_line = True)

			if "Timezone" not in self.dictionary["Entry"]["Times"]:
				key = self.language_texts["when_i_finished_watching"]

				self.dictionary["Entry"]["Times"]["Timezone"] = self.dictionary["Media"]["dates"][key]

			key = self.language_texts["when_i_started_to_watch"]

			# Get started watching time
			self.dictionary["Media"]["started_watching"] = self.Date.To_UTC(self.Date.From_String(self.dictionary["Media"]["dates"][key]))

			# Define time spent watching using started watching time and finished watching time
			self.dictionary["Media"]["time_spent_watching"] = self.Date.Difference(self.dictionary["Media"]["started_watching"], self.dictionary["Entry"]["Time"])["difference_strings"][self.user_language]

			if self.dictionary["Media"]["time_spent_watching"][0] + self.dictionary["Media"]["time_spent_watching"][1] == ", ":
				self.dictionary["Media"]["time_spent_watching"] = self.dictionary["Media"]["time_spent_watching"][2:]

			# Format the time template
			self.dictionary["Media"]["item"]["formatted_template"] = "\n\n" + template.format(self.dictionary["Media"]["time_spent_watching"])

			# Add the time template to the media dates text
			self.dictionary["Media"]["finished_watching_text"] = self.File.Contents(self.dictionary["Media"]["folders"]["dates"])["string"]

			if "Old history" not in self.dictionary["Media"]["States"]:
				self.dictionary["Media"]["finished_watching_text"] += self.dictionary["Media"]["item"]["formatted_template"]

				# Update media dates text file
				self.File.Edit(self.dictionary["Media"]["folders"]["dates"], self.dictionary["Media"]["finished_watching_text"], "w")

			# Add the time template to the Diary Slim text
			self.dictionary["Media"]["finished_watching_text"] = self.dictionary["Media"]["finished_watching_text"].replace(self.language_texts["when_i_started_to_watch"], self.language_texts["when_i_started_to_watch"] + " " + self.dictionary["Media"]["texts"]["container_text"]["the"])

			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.dictionary["Media"]["finished_watching_text"]

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

		if self.dictionary["Media"]["States"]["series_media"] == False:
			text = text.replace(self.language_texts["a_screenshot_of_the_episode"], self.language_texts["movie"])

		if self.dictionary["Media"]["title"] in ["The Walking Dead", "Yuru Camp"]:
			text = text.replace(self.language_texts["a_screenshot_of_the_episode"], self.language_texts["a_summary_video"])

		self.posted_on_social_networks_text_template = self.language_texts["i_posted_the_watched_text_and_{}_on_the_status_of_{}_and_tweet_on_{}"] + "."

		self.dictionary["Entry"]["Diary Slim"]["posted_on_social_networks"] = self.posted_on_social_networks_text_template.format(text, self.first_three_social_networks, self.twitter_social_network)

		text = self.language_texts["post_on_the_social_networks"] + " (" + self.social_networks_string + ")"

		self.dictionary["Entry"]["post_on_social_networks"] = self.Input.Yes_Or_No(text)

		if self.dictionary["Entry"]["post_on_social_networks"] == True:
			from Social_Networks.Open_Social_Network import Open_Social_Network as Open_Social_Network

			Open_Social_Network(option_info = {"type": "profile"}, social_network_parameter = "WhatsApp", first_space = False, second_space = False)

			self.Input.Type(self.language_texts["press_enter_to_copy_the_watched_text"])

			self.Text.Copy(self.dictionary["Entry"]["Diary Slim"]["Text"])

		print()
		print("-----")
		print()

	def Write_On_Diary_Slim(self):
		# Add "Posted on Social Networks" text if the user wanted to post the entry text on the Social Networks
		if self.dictionary["Entry"]["post_on_social_networks"] == True:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.dictionary["Entry"]["Diary Slim"]["posted_on_social_networks"]

		add_dot = True

		if self.dictionary["Entry"]["post_on_social_networks"] == False and self.dictionary["Media"]["States"]["video"] == True:
			add_dot = False

		from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

		Write_On_Diary_Slim_Module(self.dictionary["Entry"]["Diary Slim"]["Text"], add_time = False, add_dot = add_dot)

	def Show_Information(self):
		self.dictionary["header_text"] = self.Text.Capitalize(self.dictionary["Media"]["texts"]["container_text"]["container"]) + ": "

		if self.dictionary["Media"]["States"]["Completed media"] == True:
			text = self.dictionary["Media"]["texts"]["container_text"]["this"]
			self.dictionary["header_text"] = self.language_texts["you_finished_watching_{}"].format(text) + ": "

		self.Show_Media_Information(self.dictionary)