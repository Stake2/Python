# Update_Files.py

from Watch_History.Watch_History import Watch_History as Watch_History

import re
import collections

class Update_Files(Watch_History):
	def __init__(self):
		super().__init__()

		methods = {
			"Iterate": self.JSON.Language.language_texts["iterate, title()"],
			"Add_To_Comments_Dictionary": self.language_texts["add_to_comments_dictionary"]
		}

		# Get keys and values
		for name in ["keys", "values"]:
			methods[name] = list(getattr(methods, name)())

		# Add methods to method keys
		for method in methods.copy():
			if method not in ["keys", "values"]:
				methods[method] = getattr(self, method)

		# Select method
		method = methods[self.Input.Select(methods["keys"], language_options = methods["values"])["option"]]
		method()

	def Iterate(self):
		self.comments_number = {
			"Numbers": {
				"Total": 0,
				"No time": 0,
				"Years": {},
				"Type": {}
			}
		}

		if str(self.date["year"]) not in self.comments_number["Numbers"]["Years"]:
			self.comments_number["Numbers"]["Years"][str(self.date["year"])] = 0

		i = 0
		for plural_media_type in self.media_types["plural"]["en"]:
			if plural_media_type not in self.comments_number["Numbers"]["Type"]:
				self.comments_number["Numbers"]["Type"][plural_media_type] = {
					"Total": 0,
					"No time": 0,
					"Years": {}
				}

			if str(self.date["year"]) not in self.comments_number["Numbers"]["Type"][plural_media_type]["Years"]:
				self.comments_number["Numbers"]["Type"][plural_media_type]["Years"][str(self.date["year"])] = 0

			key = plural_media_type.lower().replace(" ", "_")

			language_media_type = self.media_types["plural"][self.user_language][i]

			# Get media with all "watching statuses", not just the "Watching" and "Re-watching" ones
			media_list = self.Get_Media_List(self.media_types[plural_media_type], self.texts["watching_statuses, type: list"]["en"])
			media_list = sorted(media_list, key=str.lower)

			print()
			print("----------")
			print()
			print(language_media_type + ":")

			if plural_media_type not in [""]:
				for media_list_title in media_list:
					self.dictionary = {
						"media_type": self.media_types[plural_media_type],
						"Media": {
							"title": media_list_title
						}
					}

					print()
					print("---")
					print()
					print(self.dictionary["Media"]["title"] + ":")

					self.dictionary = self.Select_Media(self.dictionary)

					# Define the media items as the media title
					media_items = [self.dictionary["Media"]["item"]["title"]]

					# For media with media list, get the actual media items
					if self.dictionary["Media"]["States"]["media_list"] == True:
						media_items = self.dictionary["Media"]["items"]["list"]

					# Iterate through media items list
					for list_item in media_items:
						# Define media item
						self.dictionary = self.Define_Media_Item(self.dictionary, media_item = list_item)

						print()
						print("\t" + self.dictionary["Media"]["item"]["title"] + ":")

						# Verify if empty episodes' titles files exist
						#self.Check_Episodes_Titles()

						# Add exact media or media item creation or release to media or media item details
						self.Add_Date()

						# Convert comments with old registry style (Files) to the new one (JSON)
						self.Convert_Old_Comments()

						# Re-count comments numbers
						self.Count_Comments_Number()

						# Add anime information to anime details
						if self.dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"]:
							self.Add_Anime_Information()

						if self.dictionary["media_type"]["plural"]["en"] == self.texts["videos"]["en"]:
							self.Convert_Video_Information()

					if self.switches["testing"] == True and media_list_title != media_list[-1]:
						input()

			if self.switches["testing"] == True and plural_media_type != self.media_types["plural"]["en"][-1]:
				self.Input.Type(self.JSON.Language.language_texts["continue, title()"])

			i += 1

		for plural_media_type in self.media_types["plural"]["en"]:
			for key in self.comments_number["Numbers"]["Type"][plural_media_type]["Years"]:
				if key not in self.comments_number["Numbers"]["Years"]:
					self.comments_number["Numbers"]["Years"][key] = 0

				# Add to root years numbers
				self.comments_number["Numbers"]["Years"][key] += self.comments_number["Numbers"]["Type"][plural_media_type]["Years"][key]

				# Add to total comment number per media type
				self.comments_number["Numbers"]["Type"][plural_media_type]["Total"] += self.comments_number["Numbers"]["Type"][plural_media_type]["Years"][key]

		# Add to total number from media type total numbers
		for plural_media_type in self.media_types["plural"]["en"]:
			self.comments_number["Numbers"]["Total"] += self.comments_number["Numbers"]["Type"][plural_media_type]["Total"]

		# Sort year comment number keys
		self.comments_number["Numbers"]["Years"] = dict(collections.OrderedDict(sorted(self.comments_number["Numbers"]["Years"].items())))

		# Sort media type year comment numbers keys
		for plural_media_type in self.media_types["plural"]["en"]:
			self.comments_number["Numbers"]["Type"][plural_media_type]["Years"] = dict(collections.OrderedDict(sorted(self.comments_number["Numbers"]["Type"][plural_media_type]["Years"].items())))

		# Update comments file
		self.JSON.Edit(self.folders["comments"]["comments"], self.comments_number)

	def Check_Episodes_Titles(self):
		# If "titles" is present in the folders dictionary (not a single unit media item)
		# And status is not "Plan to watch" or "Completed"
		if "titles" in self.dictionary["Media"]["item"]["folders"] and self.dictionary["Media"]["details"][self.language_texts["status, title()"]] not in [self.language_texts["plan_to_watch, title()"], self.JSON.Language.language_texts["completed, title()"]]:
			# Get titles file to check its contents
			titles_file = self.dictionary["Media"]["item"]["folders"]["titles"]["root"] + self.languages["full"]["en"] + ".txt"

			# If file is empty
			if self.File.Contents(titles_file)["lines"] == []:
				# Iterate through languages list
				for language in self.languages["small"]:
					full_language = self.languages["full"][language]

					# Define the language titles file
					titles_file = self.dictionary["Media"]["item"]["folders"]["titles"]["root"] + full_language + ".txt"

					# Open it for user to fill it with episode titles
					self.File.Open(titles_file)

				# Wait for user input
				self.Input.Type(self.JSON.Language.language_texts["continue, title()"])

	def Add_Date(self):
		item_types = ["Media"]

		if self.dictionary["Media"]["States"]["media_list"] == True:
			item_types.append("item")

		# Iterate through the item_types list
		for item_type in item_types:
			# Get the details file for media
			self.date_dictionary = {
				"file": self.dictionary["Media"]["folders"]["details"],
				"details": self.File.Dictionary(self.dictionary["Media"]["folders"]["details"])
			}

			# Get the details file for media item
			if item_type == "item":
				self.date_dictionary.update({
					"file": self.dictionary["Media"]["item"]["folders"]["details"],
					"details": self.File.Dictionary(self.dictionary["Media"]["item"]["folders"]["details"])
				})

			ask = False

			# If the "Year" key in details and "Date" key not in details
			if self.Date.language_texts["year, title()"] in self.date_dictionary["details"] and self.date_dictionary["details"][self.Date.language_texts["year, title()"]] != "?" and self.Date.language_texts["start_date"] not in self.date_dictionary["details"]:
				year = self.date_dictionary["details"][self.Date.language_texts["year, title()"]]

				# If the media has a media item list
				if self.dictionary["Media"]["States"]["media_list"] == True:
					# If the media title is equal to the media item title and the date is already present in the media details
					if self.dictionary["Media"]["title"] == self.dictionary["Media"]["item"]["title"] and self.Date.language_texts["start_date"] in self.dictionary["Media"]["details"]:
						# Get the date from the media details
						date = self.dictionary["Media"]["details"][self.Date.language_texts["start_date"]]

						ask = False

					# If the media title is not equal to the media item title or the date is not present in the media details
					if item_type == "item" and self.dictionary["Media"]["title"] != self.dictionary["Media"]["item"]["title"] or self.Date.language_texts["start_date"] not in self.dictionary["Media"]["details"]:
						ask = True

				# If the media has no media item list
				if self.dictionary["Media"]["States"]["media_list"] == False:
					ask = True

				if ask == True:
					if self.dictionary["Media"]["item"]["title"] != self.dictionary["Media"]["title"]:
						print()
						print(self.dictionary["Media"]["item"]["title"] + ":")

					print(self.Date.language_texts["year, title()"] + ": " + year)

					# Ask for the day and month separated by a slash, because the year is already inside the details
					date = ""

					while re.search(r"[0-9]{2,2}/[0-9]{2,2}", date) == None:
						date = self.Input.Type(self.Date.language_texts["day, title()"] + " " + self.JSON.Language.language_texts["and"] + " " + self.Date.language_texts["month"]) + "/" + year

				# Add the "date" key and value after the "year" key
				key_value = {
					"key": self.Date.language_texts["start_date"],
					"value": date
				}

				self.date_dictionary["details"] = self.JSON.Add_Key_After_Key(self.date_dictionary["details"], key_value, self.Date.language_texts["year, title()"])

				# Update media or media item details file
				self.File.Edit(self.date_dictionary["file"], self.Text.From_Dictionary(self.date_dictionary["details"]), "w")

			if self.Date.language_texts["year, title()"] not in self.date_dictionary["details"]:
				print(self.date_dictionary["file"])
				self.File.Open(self.date_dictionary["file"], open = True)
				quit()

	def Convert_Old_Comments(self):
		if hasattr(self, "dictionary_of_contents") == True:
			del dictionary_of_contents

		dictionary_of_contents = {
			"media_comments": self.Folder.Contents(self.dictionary["Media"]["item"]["folders"]["comments"]["root"], lower_key = True)
		}

		dictionary_of_contents["comments_json_file"] = dictionary_of_contents["media_comments"]["dictionary"]["comments"]
		dictionary_of_contents["comments_json"] = self.JSON.To_Python(dictionary_of_contents["comments_json_file"])

		if len(dictionary_of_contents["media_comments"]["file"]["list"]) != 1 and dictionary_of_contents["comments_json"]["Entries"] == []:
			number = 1
			for file in dictionary_of_contents["media_comments"]["file"]["list"]:
				if "Comments.json" not in file and "Times" not in file and "YouTube IDs" not in file:
					file_name = self.File.Name(file)
					episode_number = file_name.split(" ")[0]

					if re.search(r"[0-9]{2,4}\([0-9]{2,4}\)", episode_number) != None:
						episode_number = re.sub("\([0-9]{2,4}\)", "", episode_number)

					self.dictionary["Media"]["States"]["Re-watching"] = False

					if re.search(" " + self.texts["re_watched, type: regex, en - pt"], file_name) != None:
						times = int(file_name.split(self.texts["re_watched, capitalize()"]["en"] + " ")[1].split("x")[0])

						self.dictionary["Media"]["episode"]["re_watched"] = {
							"times": times
						}

						self.dictionary["Media"]["States"]["Re-watching"] = True

					comment = self.File.Contents(file)["lines"]

					added_title = False

					if self.JSON.Language.language_texts["title, title()"] + ":" not in comment[0]:
						comment.insert(0, "")
						comment.insert(0, "")
						comment.insert(0, "")
						comment[0] = self.JSON.Language.language_texts["title, title()"] + ":"

						added_title = True

					if self.dictionary["Media"]["title"] in comment[1] and self.dictionary["Media"]["title"] not in self.dictionary["Media"]["item"]["title"]:
						comment[1] = comment[1].replace(self.dictionary["Media"]["title"], self.dictionary["Media"]["titles"]["language"])

					elif self.dictionary["Media"]["titles"]["language"] not in comment[1] and self.dictionary["Media"]["titles"]["language"] not in self.dictionary["Media"]["item"]["title"]:
						if added_title == False:
							comment[1] = self.dictionary["Media"]["titles"]["language"] + " " + comment[1]

						if added_title == True:
							comment[1] = self.dictionary["Media"]["titles"]["language"]

							item_title = self.dictionary["Media"]["item"]["title"]

							if item_title != self.dictionary["Media"]["title"] and item_title[0] + item_title[1] != ": ":
								comment[1] += " "

					if self.dictionary["Media"]["title"] == "Yuru Camp△" and self.dictionary["Media"]["title"] not in comment[1]:
						comment[1] = comment[1].replace(self.dictionary["Media"]["title"][:-1], self.dictionary["Media"]["title"])

					if "△△" in comment[1]:
						comment[1] = comment[1].replace("△△", "△")

					self.dictionary["Media"]["States"]["Watch dubbed"] = False

					if '"[' + self.language_texts["dubbed, title()"] + ']"' in self.Text.From_List(comment):
						self.dictionary["Media"]["States"]["Watch dubbed"] = True
						comment = self.Text.From_List(comment)
						comment = comment.replace('"[' + self.language_texts["dubbed, title()"] + ']"', "")
						comment = comment.splitlines()

					time = ""

					# Get time
					if "times" in dictionary_of_contents["media_comments"]["dictionary"]:
						times_folder = dictionary_of_contents["media_comments"]["dictionary"]["times"]

						if file_name in times_folder:
							time = self.File.Contents(times_folder[file_name])["lines"][0]

					else:
						if self.language_texts["time, title()"] + ":" in comment[3]:
							time = comment[4]

					if time != "" and self.language_texts["time, title()"] + ":" not in comment[3]:
						comment.insert(3, self.language_texts["time, title()"] + ":")
						comment.insert(4, time)
						comment.insert(5, "")

					if re.search(" " + self.texts["re_watched, type: regex, en - pt"], file_name) != None:
						if re.search(" " + self.texts["re_watched, type: regex, en - pt"], comment[1]) != None:
							comment[1] = re.sub(self.texts["re_watched, type: regex"]["en"] + " - ", "", comment[1])

						new_file_name = re.sub(self.texts["re_watched, type: regex"]["en"] + " - ", "", file_name)
						new_file = self.dictionary["Media"]["item"]["folders"]["media_comments"]["root"] + new_file_name + ".txt"

						self.File.Move(file, new_file)

						file = new_file
						file_name = new_file_name

					self.dictionary["Media"]["States"]["Christmas"] = False

					if "25/12" in time:
						self.dictionary["Media"]["States"]["Christmas"] = True

					self.dictionary["Media"]["States"]["First entry in year"] = False
					self.dictionary["Media"]["States"]["First media type entry in year"] = False

					# First watched in year state
					key = self.dictionary["media_type"]["plural"]["en"]

					if key != "Animes":
						key = key + " - " + self.dictionary["media_type"]["plural"]["pt"]

					key = key.lower().replace(" ", "_")

					entry_year = ""

					if time != "":
						entry_year = time.split("/")[-1]

					if time == "":
						for year in range(2018, self.date["year"]):
							folders = self.Folder.Contents(self.folders["watch_history"][str(year)]["per_media_type"]["files"]["root"], lower_key = True)["dictionary"]
							folders = folders[key]

							episodes = self.File.Contents(folders["episodes"])["lines"]

							if comment[1] in episodes:
								entry_year = year

					if entry_year != "":
						folders = self.Folder.Contents(self.folders["watch_history"][str(entry_year)]["per_media_type"]["root"], lower_key = True)["dictionary"]
						folders = folders["files"][key]

						episodes = self.File.Contents(self.folders["watch_history"][str(entry_year)]["episodes"])["lines"]
						media_type_episodes = self.File.Contents(folders["episodes"])["lines"]

						if comment[1] in episodes and comment[1] == episodes[0]:
							self.dictionary["Media"]["States"]["First entry in year"] = True

						if comment[1] in media_type_episodes and comment[1] == media_type_episodes[0]:
							self.dictionary["Media"]["States"]["First media type entry in year"] = True

					# Add file name to file names list
					if file_name not in dictionary_of_contents["comments_json"]["Entries"]:
						dictionary_of_contents["comments_json"]["Entries"].append(file_name)

					# Add to Comments.json dictionary
					string_time = time

					if string_time != "":
						string_time = self.Date.To_String(self.Date.To_UTC(self.Date.From_String(string_time, "%H:%M %d/%m/%Y")["date"]))

					dictionary_of_contents["comments_json"]["Dictionary"][file_name] = {
						"Number": number,
						"Entry": file_name,
						"Type": self.dictionary["media_type"]["plural"]["en"],
						"Titles": {},
						"Time": string_time
					}

					if self.dictionary["Media"]["States"]["video"] == True:
						dictionary_of_contents["comments_json"]["Dictionary"][file_name].pop("Time")

						dictionary_of_contents["comments_json"]["Dictionary"][file_name].update({
							"ID": "",
							"Link": ""
						})

					dict_ = self.Define_States_Dictionary(self.dictionary)

					if dict_ != {}:
						dictionary_of_contents["comments_json"]["Dictionary"][file_name]["States"] = dict_

					if self.dictionary["Media"]["item"]["title"] not in comment[1] and self.dictionary["Media"]["item"]["titles"]["language"] not in comment[1] and self.dictionary["Media"]["States"]["video"] == False:
						title = self.dictionary["Media"]["item"]["title"]

						comment[1] += title

						if re.search("S[0-9]{2,2}", title) == None:
							comment[1] += " "

					# Get media or episode titles
					for language in self.languages["small"]:
						full_language = self.languages["full"][language]

						titles_file = self.dictionary["Media"]["item"]["folders"]["titles"]["root"] + full_language + ".txt"
						titles = self.File.Contents(titles_file)["lines"]

						title = ""

						if titles != []:
							if self.dictionary["Media"]["States"]["episodic"] == False:
								i = 0
								for title in titles:
									title = self.Sanitize_Title(title)

									if file_name == title:
										episode_number = i + 1

									i += 1

							title = titles[int(episode_number) - 1]

							list_ = []

							for alternative_episode_type in self.alternative_episode_types:
								if alternative_episode_type not in title:
									list_.append(False)

							if self.dictionary["Media"]["episode"]["separator"] not in title and len(list_) == len(self.alternative_episode_types):
								title = self.dictionary["Media"]["episode"]["separator"] + episode_number + " " + title

						dictionary_of_contents["comments_json"]["Dictionary"][file_name]["Titles"][language] = title

						if language == self.user_language and title not in comment[1]:
							comment[1] += title

					# Add YouTube ID, comment link, and comment ID
					if self.dictionary["Media"]["States"]["video"] == True:
						ids_file = self.dictionary["Media"]["item"]["folders"]["titles"]["ids"]
						video_id = self.File.Contents(ids_file)["lines"][int(episode_number) - 1]

						if "YouTube IDs" in contents["dictionary"]:
							youtube_comment_id_file = contents["dictionary"]["YouTube IDs"][file_name]
							youtube_comment_ids = self.File.Contents(youtube_comment_id_file)["lines"]

						else:
							youtube_comment_ids = [
								dictionary_of_contents["comments_json"]["Dictionary"][file_name]["ID"]
							]

						video = self.Get_YouTube_Information("video", video_id)

						youtube_comment = self.Get_YouTube_Information("comment", youtube_comment_ids[0])

						dictionary_of_contents["comments_json"]["Dictionary"][file_name].update({
							"ID": youtube_comment_ids[0],
							"Link": self.remote_origins["YouTube"] + "watch?v=" + video_id + "&list=" + self.dictionary["Media"]["item"]["details"][self.language_texts["origin_location"]] + "&index=" + str(int(episode_number)) + "&lc=" + youtube_comment_ids[0],
							"Time": youtube_comment["Time"]
						})

						if self.Date.From_String(youtube_comment["Time"])["date"] > self.Date.From_String(string_time)["date"]:
							dictionary_of_contents["comments_json"]["Dictionary"][file_name]["Time"] = string_time

							comment[4] = self.Date.To_Timezone(self.Date.From_String(string_time))["hh:mm DD/MM/YYYY"]

						if self.Date.From_String(string_time)["date"] > self.Date.From_String(youtube_comment["Time"])["date"]:
							dictionary_of_contents["comments_json"]["Dictionary"][file_name]["Time"] = youtube_comment["Time"]

							comment[4] = self.Date.To_Timezone(self.Date.From_String(youtube_comment["Time"]))["hh:mm DD/MM/YYYY"]

						dictionary_of_contents["comments_json"]["Dictionary"][file_name].update({
							"Video": {
								"ID": video_id,
								"Link": self.remote_origins["YouTube"] + "watch?v=" + video_id + "&list=" + self.dictionary["Media"]["item"]["details"][self.language_texts["origin_location"]] + "&index=" + str(int(episode_number)),
								"Time": video["Time"]
							}
						})

						if video_id not in comment[2]:
							comment.insert(2, video_id)

					# Update media type comment file with new comment
					text = self.Text.From_List(comment)
					self.File.Edit(file, text, "w")

					if file_name not in dictionary_of_contents["media_comments"]["dictionary"]:
						dictionary_of_contents["media_comments"]["dictionary"][file_name] = self.dictionary["Media"]["item"]["folders"]["comments"]["root"] + file_name + ".txt"
						self.File.Create(dictionary_of_contents["media_comments"]["dictionary"][file_name])

					# Update media comment file with new comment
					self.File.Edit(dictionary_of_contents["media_comments"]["dictionary"][file_name], text, "w")

					number += 1

			# Sort file names and dictionary keys
			dictionary_of_contents["comments_json"]["Entries"] = sorted(dictionary_of_contents["comments_json"]["Entries"], key=str.lower)
			dictionary_of_contents["comments_json"]["Dictionary"] = dict(collections.OrderedDict(sorted(dictionary_of_contents["comments_json"]["Dictionary"].items())))

			# Update media comments number
			dictionary_of_contents["comments_json"].update({
				"Numbers": {
					"Total": len(dictionary_of_contents["comments_json"]["Entries"]),
				},
				"Entries": dictionary_of_contents["comments_json"]["Entries"],
				"Dictionary": dictionary_of_contents["comments_json"]["Dictionary"]
			})

			# Update media type "Comments.json" file
			self.JSON.Edit(dictionary_of_contents["comments_json_file"], dictionary_of_contents["comments_json"])

			if "Times" in dictionary_of_contents["media_comments"]["dictionary"]:
				self.Folder.Delete(dictionary_of_contents["media_comments"]["dictionary"]["Times"]["root"])

			if "YouTube IDs" in dictionary_of_contents["media_comments"]["dictionary"]:
				self.Folder.Delete(dictionary_of_contents["media_comments"]["dictionary"]["YouTube IDs"]["root"])

	def Count_Comments_Number(self):
		entries = self.JSON.To_Python(self.dictionary["Media"]["item"]["folders"]["comments"]["comments"])

		if entries["Entries"] != []:
			for entry_name in entries["Entries"]:
				entry = entries["Dictionary"][entry_name]

				if "Time" in entry:
					if entry["Time"] != "":
						year = self.Date.From_String(entry["Time"])["year"]

						if str(year) not in self.comments_number["Numbers"]["Type"][self.dictionary["media_type"]["plural"]["en"]]["Years"]:
							self.comments_number["Numbers"]["Type"][self.dictionary["media_type"]["plural"]["en"]]["Years"][str(year)] = 0

						self.comments_number["Numbers"]["Type"][self.dictionary["media_type"]["plural"]["en"]]["Years"][str(year)] += 1

					if entry["Time"] == "":
						self.comments_number["Numbers"]["Type"][self.dictionary["media_type"]["plural"]["en"]]["Total"] += 1
						self.comments_number["Numbers"]["Type"][self.dictionary["media_type"]["plural"]["en"]]["No time"] += 1
						self.comments_number["Numbers"]["No time"] += 1

	def Sort_Comment_Dictionary(self):
		entries = self.JSON.To_Python(self.dictionary["Media"]["item"]["folders"]["comments"]["comments"])

		for entry_name in entries["Entries"]:
			entry = entries["Dictionary"][entry_name]

			comment = {
				"Number": entry["Number"],
				"Entry": entry["Entry"],
				"Type": entry["Type"],
				"Titles": entry["Titles"],
				"Time": entry["Time"]
			}

			if "States" in entry:
				comment["States"] = entry["States"]

			entries["Dictionary"][entry_name] = comment

		self.JSON.Edit(self.dictionary["Media"]["item"]["folders"]["comments"]["comments"], entries)

	def Add_Anime_Information(self):
		item_types = ["Media"]

		if self.dictionary["Media"]["States"]["media_list"] == True:
			item_types.append("item")

		for item_type in item_types:
			media_dictionary = self.dictionary["Media"]

			if item_type == "item":
				media_dictionary = self.dictionary["Media"]["item"]

			if "ID" not in media_dictionary["details"]:
				# Remove special characters from media (item) title
				title = media_dictionary["title"]

				# Remove non-url items from title
				for item in [",", ":", "(", ")", ".", "!", "?"]:
					title = title.replace(item, "")

				# Add media title to media item title to use on search
				if self.dictionary["Media"]["item"]["title"] != self.dictionary["Media"]["title"]:
					title = self.dictionary["Media"]["title"] + " " + title

				if (
					# If media has media list and the media item is not the same as the the root media
					self.dictionary["Media"]["States"]["media_list"] == True and
					self.dictionary["Media"]["item"]["title"] != self.dictionary["Media"]["title"] or

					# Or the media does not have a media list and the media item is the same as the root media and the "ID" key is not present inside the media details
					self.dictionary["Media"]["States"]["media_list"] == False or
					self.dictionary["Media"]["item"]["title"] == self.dictionary["Media"]["title"] and
					"ID" not in self.dictionary["Media"]["details"]
				):
					# Open MyAnimeList search page with media (item) title parameter
					self.File.Open("https://myanimelist.net/search/all?q={}&cat=anime".format(title))

					# Ask for media (item) link
					link = self.Input.Type(self.JSON.Language.language_texts["{}_website_link"].format("MyAnimeList"))

					# Get ID from link
					id = link.split("/")[-2]

					# Get information from MyAnimeList using anime ID
					get_information_from_mal = True

				# If the media has a media list and the media item is the same as the media and the "ID" key is present inside the media details
				if (
					self.dictionary["Media"]["States"]["media_list"] == True and
					self.dictionary["Media"]["item"]["title"] == self.dictionary["Media"]["title"] and
					"ID" in self.dictionary["Media"]["details"]
				):
					# Get link and ID from media details
					link = self.dictionary["Media"]["details"]["Link"]
					id = self.dictionary["Media"]["details"]["ID"]

					# Get anime information from "Anime.json" file
					media_dictionary["Information"] = self.JSON.To_Python(self.dictionary["Media"]["folders"]["anime"])

					# Do not get information from MyAnimeList
					get_information_from_mal = False

				# Add the MyAnimeList ID after the "Episodes" key
				key_value = {
					"key": "ID",
					"value": id
				}

				after_key = self.language_texts["episodes, title()"]

				if self.dictionary["Media"]["States"]["single_unit"] == True:
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
					media_dictionary["Information"] = self.API.Call("MyAnimeList", {"id": media_dictionary["details"]["ID"]})["response"]

					# Define links dictionary
					media_dictionary["Information"]["Links"] = {
						"Official": {},
						"MyAnimeList": {
							"Link": link,
							"en": link,
							"ID": id
						}
					}

				self.Paste_Links(media_dictionary)

				if get_information_from_mal == True:
					# Format anime details dictionary
					media_dictionary["Information"] = self.Format_Anime_Information(media_dictionary, media_dictionary["Information"])

				# Add time to date
				if "Broadcast" in media_dictionary["Information"] and media_dictionary["Information"]["Broadcast"]:
					if len(media_dictionary["details"][self.Date.language_texts["start_date"]]) <= 10 and len(media_dictionary["Information"]["Broadcast"]["Time"]) == 5:
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

					if media_dictionary["Information"]["Dates"][key] != {}:
						key_value["value"] = media_dictionary["Information"]["Dates"][key]["Date"]["DD/MM/YYYY"]

						if media_dictionary["Information"]["Dates"][key]["Date Time"] != {}:
							key_value["value"] = media_dictionary["Information"]["Dates"][key]["Date Time"]["HH:MM DD/MM/YYYY"]

					media_dictionary["details"] = self.JSON.Add_Key_After_Key(media_dictionary["details"], key_value, after_key = after_key)

				media_dictionary["details"] = self.JSON.Add_Key_After_Key(media_dictionary["details"], key_value, after_key = self.Date.language_texts["start_date"])

				# Add the episode duration after the "Episodes" key
				key_value = {
					"key": self.Date.language_texts["duration, title()"],
					"value": media_dictionary["Information"]["Duration"]["Text"][self.user_language]
				}

				if key_value["value"] == "":
					key_value["value"] = 0

				# Change duration key if episodes are more than one
				if media_dictionary["Information"]["Episodes"] > 1:
					key_value["key"] = self.language_texts["episodes_duration"]

				media_dictionary["details"] = self.JSON.Add_Key_After_Key(media_dictionary["details"], key_value, after_key = self.language_texts["episodes, title()"])

				# Add "Studio(s)" key to media (item) details after the "Episodes duration" key
				key_value = {
					"key": self.Text.By_Number(media_dictionary["Information"]["Studios"], self.JSON.Language.language_texts["studio, title()"], self.JSON.Language.language_texts["studios, title()"]),
					"value": self.Text.From_List(media_dictionary["Information"]["Studios"], break_line = False, separator = ", ")
				}

				media_dictionary["details"] = self.JSON.Add_Key_After_Key(media_dictionary["details"], key_value, after_key = self.language_texts["episodes_duration"])

				# Update media (item) details file
				self.File.Edit(media_dictionary["folders"]["details"], self.Text.From_Dictionary(media_dictionary["details"]), "w")

				if media_dictionary["Information"]["Links"]["Wikipedia"]["Episode list"] == {}:
					media_dictionary["Information"]["Links"]["Wikipedia"].pop("Episode list")

				# Write anime details into media "[Anime]/[Season].json" file
				self.JSON.Edit(media_dictionary["folders"][media_dictionary["Information file name"].lower()], media_dictionary["Information"])

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
				],
				"Gender": "masculine"
			},
			"IMDB": {
				"Languages": [
					"en"
				],
				"Gender": "masculine"
			}
		}

		# Add "CrunchyRoll" website to links dictionary
		if self.dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"]:
			links["CrunchyRoll"] = {
				"Languages": [
					"en"
				],
				"Gender": "feminine"
			}

		# Remove Japanese Wikipedia language if media type is not "Animes"
		if self.dictionary["media_type"]["plural"]["en"] != self.texts["animes"]["en"]:
			links["Wikipedia"]["Languages"].pop("ja")

		# Iterate through links dictionary
		for link_key in links:
			link = links[link_key]

			# If the link key is not inside media information links, add it
			if link_key not in media_dictionary["Information"]["Links"]:
				media_dictionary["Information"]["Links"][link_key] = {}

			# if the link key is inside the root media information links, get the links dictionary from it
			if link_key in self.dictionary["Media"]["Information"]["Links"]:
				media_dictionary["Information"]["Links"][link_key] = self.dictionary["Media"]["Information"]["Links"][link_key]

			if "Languages" in link:
				for language in link["Languages"]:
					if language in self.languages["full_translated"][language]:
						# Get transtaled language
						translated_full_language = self.languages["full_translated"][language][self.user_language]

					else:
						translated_full_language = language

					# Define of and in texts
					of_text = self.JSON.Language.texts["genders, type: dict"][self.user_language][link["Gender"]]["of"]
					in_text = self.JSON.Language.texts["genders, type: dict"][self.user_language][link["Gender"]]["in"]

					# Define text to show when asking for user to paste the website link
					text = self.JSON.Language.language_texts["{}_website_link"].format(in_text + " " + translated_full_language + " " + of_text + " " + link_key)

					# If the language is not inside the links dictionary, ask for the website link
					if language not in media_dictionary["Information"]["Links"][link_key]:
						typed_link = self.Input.Type(text)

						# If the typed link is not empty, define the language link as the typed link
						if typed_link != "":
							media_dictionary["Information"]["Links"][link_key][language] = typed_link

					# If the link key is "Wikipedia" and the language is not "Japanese"
					if link_key == "Wikipedia" and language != "ja":
						# Define empty dictionary for "episode list" links
						episode_list_links = {}

						# Define text to show when asking for user to paste the episode list website link
						text = self.JSON.Language.language_texts["{}_website_link"].format(of_text + " " + self.language_texts["episode_list"].lower() + " " + in_text + " " + translated_full_language + " " + of_text + " " + link_key)

						# If the language is not inside the episode list links dictionary, ask for the episode list website link
						if (
							"Episode list" in media_dictionary["Information"]["Links"][link_key] and language not in media_dictionary["Information"]["Links"][link_key]["Episode list"] or
							"Episode list" not in media_dictionary["Information"]["Links"][link_key]
						):
							typed_link = self.Input.Type(text)

							# If the typed link is not empty, define the episode list language link as the typed link
							if typed_link != "":
								episode_list_links[language] = typed_link

			# If the link key is "Wikipedia"
			if link_key == "Wikipedia":
				# If the "Episode list" key is not inside the links dictionary
				if "Episode list" not in media_dictionary["Information"]["Links"][link_key]:
					# Define the "Episode list" dictionary as the episode list links dictionary
					media_dictionary["Information"]["Links"][link_key]["Episode list"] = episode_list_links

			# If the link dictionary does not contain a "Languages" list
			if "Languages" not in link:
				# Get the type text to show from the English language (default link language)
				text = link["Link"]

				if "Link" not in media_dictionary["Information"]["Links"][link_key]:
					typed_link = self.Input.Type(text)

					media_dictionary["Information"]["Links"][link_key]["Link"] = typed_link

				if "Twitter" not in media_dictionary["Information"]["Links"][link_key]:
					typed_link = self.Input.Type("Twitter")

					media_dictionary["Information"]["Links"][link_key]["Twitter"] = typed_link

	def Format_Anime_Information(self, media_dictionary, information):
		new_information = {
			"Title": information["title"],
			"Titles": {
				**media_dictionary["titles"],
				**information["alternative_titles"]
			},
			"ID": information["id"],
			"Link": media_dictionary["details"]["Link"],
			"Links": {},
			"Format": information["media_type"],
			"Source": information["source"].replace("4_koma", "4-koma").replace("_", " ").capitalize(),
			"Rating": information["rating"].upper().replace("_", " "),
			"Pictures": [],
			"Genres": [],
			"Episodes": information["num_episodes"],
			"Episode titles": {},
			"Duration": information["average_episode_duration"],
			"Dates": {
				"Start": {},
				"End": {}
			},
			"Start season": {},
			"Broadcast": {},
			"Synopsis": information["synopsis"],
			"Background": information["background"],
			"Related": {},
			"Studios": [],
			"Original language": "Japanese",
			"Country of origin": "Japan"
		}

		# Add link to links dictionary
		for key in information["Links"]:
			new_information["Links"][key] = information["Links"][key]

		# Change format of anime to title if it is not "TV", "OVA", or "ONA"
		if new_information["Format"] in ["movie", "special", "music"]:
			new_information["Format"] = new_information["Format"].title()

		# Change format of anime to uppercase if it is "TV", "OVA", or "ONA"
		else:
			new_information["Format"] = new_information["Format"].upper()

		# Add pictures
		for dict_ in information["pictures"]:
			new_information["Pictures"].append(dict_["large"])

		# Add genres
		for dict_ in information["genres"]:
			new_information["Genres"].append(dict_["name"])

		# Get episode titles
		new_information["Episode titles"] = self.dictionary["Media"]["item"]["episodes"]["titles"]
		new_information["Episode titles"].pop("files")

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
			new_information["Duration"]["Hours"] = self.Text.Add_Leading_Zeros(divmod(new_information["Duration"]["Minutes"], 60)[0])

			# Define add leading zeroes to minutes
			new_information["Duration"]["Minutes"] = self.Text.Add_Leading_Zeros(divmod(new_information["Duration"]["Minutes"], 60)[1])

			# Define add leading zeroes to seconds
			new_information["Duration"]["Seconds"] = self.Text.Add_Leading_Zeros(new_information["Duration"]["Seconds"])

			# Define duration time
			new_information["Duration"]["Time"] = str(new_information["Duration"]["Hours"]) + ":" + str(new_information["Duration"]["Minutes"]) + ":" + str(new_information["Duration"]["Seconds"])

			# Define duration time text using "Time_Text" method of "Date" class
			for language in self.languages["small"]:
				new_information["Duration"]["Text"][language] = self.Date.Time_Text(new_information["Duration"]["Time"], language)

			# Convert times to integer
			for key in new_information["Duration"]:
				if key not in ["Time", "Text"]:
					new_information["Duration"][key] = int(new_information["Duration"][key])

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

		if "start_season" in information:
			new_information["Start season"] = {
				"Year": information["start_season"]["year"],
				"Season": information["start_season"]["season"].title()
			}

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

		# Add related manga
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

		# Add related anime
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

		# Add studios
		for dict_ in information["studios"]:
			new_information["Studios"].append(dict_["name"])

		# If background is empty, remove the key
		if new_information["Background"] == "":
			new_information.pop("Background")

		return new_information

	def Convert_Video_Information(self):
		# To-Do: Add title and titles to "Channel.json" and "Playlist.json"
		# Add links and dates dictionaries
		# Add episodes and episode titles, pictures, (series, series list), and original language
		pass

	def Add_To_Comments_Dictionary(self):
		self.dictionary = self.Select_Media_Type_And_Media()

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
		self.Comment_Writer(self.dictionary, only_comment = True)