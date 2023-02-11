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
		i = 0
		for plural_media_type in self.media_types["plural"]["en"]:
			key = plural_media_type.lower().replace(" ", "_")

			language_media_type = self.media_types["plural"][self.user_language][i]

			# Get media with all "watching statuses", not just the "Watching" and "Re-Watching" ones
			media_list = self.Get_Media_List(self.media_types[plural_media_type], self.texts["watching_statuses, type: list"]["en"])
			media_list = sorted(media_list, key=str.lower)

			print()
			print("----------")
			print()
			print(language_media_type + ":")

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

					if self.dictionary["Media"]["title"] != self.dictionary["Media"]["item"]["title"]:
						print()
						print("\t" + self.dictionary["Media"]["item"]["title"] + ":")

					# Verify if empty episodes' titles files exist
					#self.Check_Episodes_Titles()

					# Add exact media or media item creation or release to media or media item details
					self.Add_Date()

					# Convert comments with old registry style (Files) to the new one (JSON)
					if plural_media_type not in ["Movies"] and media_list_title not in ["Arkantos", "Ciência Todo Dia", "Egernético", "FAGames", "LCarrafaBR", "Lives do alanzoka", "Lives do Cellbit", "lunar clips", "MW Informática", "SINXPLAYSBR"]:
						self.Convert_Old_Comments()

					if self.switches["testing"] == True and list_item != media_items[-1]:
						input()

				if self.switches["testing"] == True and media_list_title != media_list[-1]:
					input()

			if self.switches["testing"] == True and plural_media_type != self.media_types["plural"]["en"][-1]:
				self.Input.Type(self.JSON.Language.language_texts["continue, title()"])

			i += 1

	def Check_Episodes_Titles(self):
		# If "titles" is present in the folders dictionary (not a single unit media item)
		# And status is not "Plan to watch" or "Completed"
		if "titles" in self.dictionary["Media"]["item"]["folders"] and self.dictionary["Media"]["details"][self.language_texts["status, title()"]] not in [self.language_texts["plan_to_watch, title()"], self.language_texts["completed, title()"]]:
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
		item_types = ["media"]

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
			if self.Date.language_texts["year, title()"] in self.date_dictionary["details"] and self.date_dictionary["details"][self.Date.language_texts["year, title()"]] != "?" and self.Date.language_texts["date, title()"] not in self.date_dictionary["details"]:
				year = self.date_dictionary["details"][self.Date.language_texts["year, title()"]]

				# If the media has a media item list
				if self.dictionary["Media"]["States"]["media_list"] == True:
					# If the media title is equal to the media item title and the date is already present in the media details
					if self.dictionary["Media"]["title"] == self.dictionary["Media"]["item"]["title"] and self.Date.language_texts["date, title()"] in self.dictionary["Media"]["details"]:
						# Get the date from the media details
						date = self.dictionary["Media"]["details"][self.Date.language_texts["date, title()"]]

						ask = False

					# If the media title is not equal to the media item title or the date is not present in the media details
					if item_type == "item" and self.dictionary["Media"]["title"] != self.dictionary["Media"]["item"]["title"] or self.Date.language_texts["date, title()"] not in self.dictionary["Media"]["details"]:
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

				# Add the date key to the details
				keys = list(self.date_dictionary["details"].keys())
				values = list(self.date_dictionary["details"].values())

				i = 0
				for key in keys.copy():
					# If the "Date" is not present inside the details, add it after the "Year" key
					if self.Date.language_texts["date, title()"] not in keys and key == self.Date.language_texts["year, title()"]:
						keys.insert(i + 1, self.Date.language_texts["date, title()"])
						values.insert(i + 1, date)

					# If the "Date" is present, update its value
					if self.Date.language_texts["date, title()"] in keys and key == self.Date.language_texts["date, title()"]:
						values[i] = date

					i += 1

				# Remake details dictionary
				self.date_dictionary["details"] = dict(zip(keys, values))

				# Update media or media item details file
				self.File.Edit(self.date_dictionary["file"], self.Text.From_Dictionary(self.date_dictionary["details"]), "w")

			if self.Date.language_texts["year, title()"] not in self.date_dictionary["details"]:
				print(self.date_dictionary["file"])
				self.File.Open(self.date_dictionary["file"], open = True)
				quit()

	def Convert_Old_Comments(self):
		folder = self.dictionary["Media"]["item"]["folders"]["media_type_comments"]["root"]

		contents = self.Folder.Contents(folder)

		if "comments" in self.dictionary["Media"]["item"]["folders"] and "root" in self.dictionary["Media"]["item"]["folders"]["comments"]:
			media_comments_folder = self.dictionary["Media"]["item"]["folders"]["comments"]["root"]

		else:
			media_comments_folder = self.dictionary["Media"]["item"]["folders"]["root"]

		comments_contents = self.Folder.Contents(media_comments_folder, lower_key = True)["dictionary"]

		if len(contents["file"]["list"]) != 1:
			print()
			print(self.JSON.Language.language_texts["comments, title()"] + ":")
			print()
			print(self.Folder.language_texts["folders, title()"] + ":")
			print(folder)
			print(media_comments_folder)
			print()

			if self.dictionary["Media"]["States"]["series_media"] == True:
				comments_json_file = contents["dictionary"]["Comments"]
				comments_json = self.JSON.To_Python(comments_json_file)

				number = 1
				for file in contents["file"]["list"]:
					if "Comments.json" not in file and "Times" not in file and "YouTube IDs" not in file:
						file_name = self.File.Name(file)
						episode_number = file_name.split(" ")[0]

						if re.search(r"[0-9]{2,4}\([0-9]{2,4}\)", episode_number) != None:
							episode_number = re.sub("\([0-9]{2,4}\)", "", episode_number)

						self.dictionary["Media"]["States"]["re_watching"] = False

						if re.search(" " + self.texts["re_watched, type: regex, en - pt"], file_name) != None:
							times = int(file_name.split(self.texts["re_watched, title()"]["en"] + " ")[1].split("x")[0])

							self.dictionary["Media"]["episode"]["re_watched"] = {
								"times": times
							}

							self.dictionary["Media"]["States"]["re_watching"] = True

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

						self.dictionary["Media"]["States"]["watch_dubbed"] = False

						if '"[' + self.language_texts["dubbed, title()"] + ']"' in self.Text.From_List(comment):
							self.dictionary["Media"]["States"]["watch_dubbed"] = True
							comment = self.Text.From_List(comment)
							comment = comment.replace('"[' + self.language_texts["dubbed, title()"] + ']"', "")
							comment = comment.splitlines()

						time = ""

						# Get time
						if "Times" in contents["dictionary"]:
							times_folder = contents["dictionary"]["Times"]

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
							new_file = folder + new_file_name + ".txt"

							self.File.Move(file, new_file)

							file = new_file
							file_name = new_file_name

						self.dictionary["Media"]["States"]["christmas"] = False

						if "25/12" in time:
							self.dictionary["Media"]["States"]["christmas"] = True

						self.dictionary["Media"]["States"]["First Entry In Year"] = False
						self.dictionary["Media"]["States"]["First Media Type Entry In Year"] = False

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
								self.dictionary["Media"]["States"]["First Entry In Year"] = True

							if comment[1] in media_type_episodes and comment[1] == media_type_episodes[0]:
								self.dictionary["Media"]["States"]["First Media Type Entry In Year"] = True

						# Add file name to file names list
						if file_name not in comments_json["Entries"]:
							comments_json["Entries"].append(file_name)

						# Add to Comments.json dictionary
						string_time = time

						if string_time != "":
							string_time = self.Date.To_String(self.Date.To_UTC(self.Date.From_String(string_time, "%H:%M %d/%m/%Y")["date"]))

						comments_json["Dictionary"][file_name] = {
							"Number": number,
							"Entry": file_name,
							"Type": self.dictionary["media_type"]["plural"]["en"],
							"Time": string_time,
							"Titles": {}
						}

						if self.dictionary["Media"]["States"]["video"] == True:
							comments_json["Dictionary"][file_name].pop("Time")

							comments_json["Dictionary"][file_name].update({
								"ID": "",
								"Link": ""
							})

						dict_ = self.Define_States_Dictionary(self.dictionary)

						if dict_ != {}:
							comments_json["Dictionary"][file_name]["States"] = dict_

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

							comments_json["Dictionary"][file_name]["Titles"][language] = title

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
									comments_json["Dictionary"][file_name]["ID"]
								]

							video = self.Get_YouTube_Information("video", video_id)

							youtube_comment = self.Get_YouTube_Information("comment", youtube_comment_ids[0])

							comments_json["Dictionary"][file_name].update({
								"ID": youtube_comment_ids[0],
								"Link": self.remote_origins["YouTube"] + "watch?v=" + video_id + "&list=" + self.dictionary["Media"]["item"]["details"][self.language_texts["origin_location"]] + "&index=" + str(int(episode_number)) + "&lc=" + youtube_comment_ids[0],
								"Time": youtube_comment["Time"]
							})

							if self.Date.From_String(youtube_comment["Time"])["date"] > self.Date.From_String(string_time)["date"]:
								comments_json["Dictionary"][file_name]["Time"] = string_time

								comment[4] = self.Date.To_Timezone(self.Date.From_String(string_time))["hh:mm DD/MM/YYYY"]

							if self.Date.From_String(string_time)["date"] > self.Date.From_String(youtube_comment["Time"])["date"]:
								comments_json["Dictionary"][file_name]["Time"] = youtube_comment["Time"]

								comment[4] = self.Date.To_Timezone(self.Date.From_String(youtube_comment["Time"]))["hh:mm DD/MM/YYYY"]

							comments_json["Dictionary"][file_name].update({
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

						if file_name not in comments_contents:
							comments_contents[file_name] = comments_contents["root"] + file_name + ".txt"
							self.File.Create(comments_contents[file_name])

						# Update media comment file with new comment
						self.File.Edit(comments_contents[file_name], text, "w")

						number += 1

				# Sort file names and dictionary keys
				comments_json["Entries"] = sorted(comments_json["Entries"], key=str.lower)
				comments_json["Dictionary"] = dict(collections.OrderedDict(sorted(comments_json["Dictionary"].items())))

				# Update media comments number
				comments_json.update({
					"Numbers": {
						"Total": len(comments_json["Entries"]),
					},
					"Entries": comments_json["Entries"],
					"Dictionary": comments_json["Dictionary"]
				})

				# Update media "Comments.json" file
				self.JSON.Edit(comments_contents["comments"], comments_json)

				# Update media type "Comments.json" file
				self.JSON.Edit(comments_json_file, comments_json)

				if "Times" in contents["dictionary"]:
					self.Folder.Delete(contents["dictionary"]["Times"]["root"])

				if "YouTube IDs" in contents["dictionary"]:
					self.Folder.Delete(contents["dictionary"]["YouTube IDs"]["root"])

	def Sort_Comment_Dictionary(self):
		entries = self.JSON.To_Python(self.dictionary["Media"]["item"]["folders"]["comments"]["comments"])

		for entry_name in entries["Entries"]:
			entry = entries["Dictionary"][entry_name]

			comment = {
				"Number": entry["Number"],
				"Entry": entry["Entry"],
				"Type": entry["Type"],
				"Titles": entry["Titles"],
				"ID": entry["ID"],
				"Link": entry["Link"],
				"Time": entry["Time"],
				"Video": entry["Video"]
			}

			entries["Dictionary"][entry_name] = comment

		self.JSON.Edit(self.dictionary["Media"]["item"]["folders"]["comments"]["comments"], entries)
		self.JSON.Edit(self.dictionary["Media"]["item"]["folders"]["media_type_comments"]["comments"], entries)

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