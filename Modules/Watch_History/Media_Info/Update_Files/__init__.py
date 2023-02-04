# Update_Files.py

from Watch_History.Watch_History import Watch_History as Watch_History

import re
from urllib.parse import urlparse, parse_qs
import validators
import collections

class Update_Files(Watch_History):
	def __init__(self):
		super().__init__()

		self.Iterate()
		#self.Create_Comment_Dictionary()

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

			if plural_media_type != "Movies":
				for media in media_list:
					self.dictionary = {
						"media_type": self.media_types[plural_media_type],
						"media": {
							"title": media
						}
					}

					print()
					print("---")
					print()
					print(self.dictionary["media"]["title"] + ":")

					self.dictionary = self.Select_Media(self.dictionary)

					# Verify if the media is inside the correct "watching status" list
					self.Check_Status(self.dictionary)

					# Define the media items as the media title
					media_items = [self.dictionary["media"]["item"]["title"]]

					# For media with media list, get the actual media items
					if self.dictionary["media"]["states"]["media_list"] == True:
						media_items = self.dictionary["media"]["items"]["list"]

					# Iterate through media items list
					for media_item in media_items:
						# Define media item
						self.dictionary = self.Define_Media_Item(self.dictionary, media_item = media_item)

						if self.dictionary["media"]["title"] != self.dictionary["media"]["item"]["title"]:
							print()
							print("\t" + self.dictionary["media"]["item"]["title"] + ":")

						# Verify if empty episodes' titles files exist
						#self.Check_Titles()

						# Add exact media or media item creation or release to media or media item details
						self.Add_Date()

						# Convert comments with old registry style (Files) to the new one (JSON)
						#if media != "FAGames":
						#	self.Convert_Comments()

			if self.global_switches["testing"] == True:
				input()

			i += 1

	def Check_Titles(self):
		# If "titles" is present in the folders dictionary (not a single unit media item)
		# And status is not "Plan to watch" or "Completed"
		if "titles" in self.dictionary["media"]["item"]["folders"] and self.dictionary["media"]["details"]["status"] not in [self.language_texts["plan_to_watch, title()"], self.language_texts["completed, title()"]]:
			# Get titles file to check its contents
			titles_file = self.dictionary["media"]["item"]["folders"]["titles"]["root"] + self.full_languages["en"] + ".txt"

			# If file is empty
			if self.File.Contents(titles_file)["lines"] == []:
				# Iterate through languages list
				for language in self.small_languages:
					full_language = self.full_languages[language]

					# Define the language titles file
					titles_file = self.dictionary["media"]["item"]["folders"]["titles"]["root"] + full_language + ".txt"

					# Open it for user to fill it with episode titles
					self.File.Open(titles_file)

				# Wait for user input
				self.Input.Type()

	def Add_Date(self):
		names = ["media"]

		if self.dictionary["media"]["states"]["media_list"] == True:
			names.append("item")

		# Iterate through the names list
		for key in names:
			# Get the details file for media
			details = self.dictionary["media"]["details"]
			file = self.dictionary["media"]["folders"]["details"]

			# Get the details file for media item
			if key == "item":
				details = self.dictionary["media"]["item"]["details"]
				file = self.dictionary["media"]["item"]["folders"]["details"]

			# If the "Year" key in details and "Date" key not in details
			if self.Date.language_texts["year, title()"] in details and self.Date.language_texts["date, title()"] not in details:
				year = details[self.Date.language_texts["year, title()"]]

				# If the media has a media item list
				if self.dictionary["media"]["states"]["media_list"] == True:
					# If the media title is equal to the media item title and the date is already present in the media details
					if self.dictionary["media"]["title"] == self.dictionary["media"]["item"]["title"] and self.Date.language_texts["date, title()"] in self.dictionary["media"]["details"]:
						# Get the date from the media details
						date = self.dictionary["media"]["details"][self.Date.language_texts["date, title()"]]

					# If the media title is not equal to the media item title or the date is not present in the media details
					if self.dictionary["media"]["title"] != self.dictionary["media"]["item"]["title"] or self.Date.language_texts["date, title()"] not in self.dictionary["media"]["details"]:
						# If verbose is true, show the media item title again because there is more text above that pushes above the media item title shown before
						if self.global_switches["verbose"] == True and self.dictionary["media"]["title"] != self.dictionary["media"]["item"]["title"]:
							print()
							print(self.dictionary["media"]["item"]["title"] + ":")

						# Ask for the day and month separated by a slash, because the year is already inside the details
						date = self.Input.Type(self.Date.language_texts["day, title()"] + " " + self.Language.language_texts["and"] + " " + self.Date.language_texts["month"]) + "/" + year

				# If the media has no media item list
				if self.dictionary["media"]["states"]["media_list"] == False:
					# Ask for the day and month separated by a slash, because the year is already inside the details
					date = self.Input.Type(self.Date.language_texts["day, title()"] + " " + self.Language.language_texts["and"] + " " + self.Date.language_texts["month"]) + "/" + year

				# Add the date key to the details
				keys = list(details.keys())
				values = list(details.values())

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
				details = dict(zip(keys, values))

				# Update media or media item details file
				self.File.Edit(file, self.Text.From_Dictionary(details), "w")

	def Convert_Comments(self):
		folder = self.dictionary["media"]["item"]["folders"]["media_type_comments"]["root"]

		contents = self.Folder.Contents(folder)

		media_comments_folder = self.dictionary["media"]["item"]["folders"]["comments"]["root"]

		comments_contents = self.Folder.Contents(media_comments_folder, lower_key = True)["dictionary"]

		if len(contents["file"]["list"]) != 1:
			print()
			print(self.Language.language_texts["comments, title()"] + ":")
			print()
			print(self.Folder.language_texts["folders, title()"] + ":")
			print(folder)
			print(media_comments_folder)
			print()

			if self.dictionary["media"]["states"]["series_media"] == True:
				comments_json_file = contents["dictionary"]["Comments"]
				comments_json = self.JSON.To_Python(comments_json_file)

				for file in contents["file"]["list"]:
					if "Comments.json" not in file and "Times" not in file and "YouTube IDs" not in file:
						file_name = self.File.Name(file)
						episode_number = file_name.split(" ")[0]

						if re.search(r"[0-9]{2,4}\([0-9]{2,4}\)", episode_number) != None:
							episode_number = re.sub("\([0-9]{2,4}\)", "", episode_number)

						self.dictionary["media"]["states"]["re_watching"] = False

						if re.search(" " + self.texts["re_watched, type: regex, en - pt"], file_name) != None:
							times = int(file_name.split(self.texts["re_watched, title()"]["en"] + " ")[1].split("x")[0])

							self.dictionary["media"]["episode"]["re_watched"] = {
								"times": times
							}

							self.dictionary["media"]["states"]["re_watching"] = True

						comment = self.File.Contents(file)["lines"]

						if self.Language.language_texts["title, title()"] + ":" not in comment[0]:
							comment.insert(0, "")
							comment.insert(0, "")
							comment.insert(0, "")
							comment[0] = self.Language.language_texts["title, title()"] + ":"

						if self.dictionary["media"]["title"] in comment[1] and self.dictionary["media"]["title"] not in self.dictionary["media"]["item"]["title"]:
							comment[1] = comment[1].replace(self.dictionary["media"]["title"], self.dictionary["media"]["titles"]["language"])

						elif self.dictionary["media"]["titles"]["language"] not in comment[1] and self.dictionary["media"]["titles"]["language"] not in self.dictionary["media"]["item"]["title"]:
							comment[1] = self.dictionary["media"]["titles"]["language"] + " " + comment[1]

						if self.dictionary["media"]["title"] == "Yuru Camp△":
							comment[1] = comment[1].replace(self.dictionary["media"]["title"][:-1], self.dictionary["media"]["title"])

						self.dictionary["media"]["states"]["watch_dubbed"] = False

						if '"[' + self.language_texts["dubbed, title()"] + ']"' in self.Text.From_List(comment):
							self.dictionary["media"]["states"]["watch_dubbed"] = True
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

						self.dictionary["media"]["states"]["christmas"] = False

						if "25/12" in time:
							self.dictionary["media"]["states"]["christmas"] = True

						self.dictionary["media"]["states"]["first_episode_in_year"] = False
						self.dictionary["media"]["states"]["first_media_type_episode_in_year"] = False

						# First watched in year state
						key = self.dictionary["media_type"]["plural"]["en"]

						if key != "Animes":
							key = key + " - " + self.dictionary["media_type"]["plural"]["pt"]

						key = key.lower().replace(" ", "_")

						episode_year = ""

						if time != "":
							episode_year = time.split("/")[-1]

						if time == "":
							for year in range(2018, self.date["year"]):
								folders = self.Folder.Contents(self.folders["watch_history"][str(year)]["per_media_type"]["files"]["root"], lower_key = True)["dictionary"]
								folders = folders[key]

								episodes = self.File.Contents(folders["episodes"])["lines"]

								if comment[1] in episodes:
									episode_year = year

						if episode_year != "":
							folders = self.Folder.Contents(self.folders["watch_history"][str(episode_year)]["per_media_type"]["root"], lower_key = True)["dictionary"]
							folders = folders["files"][key]

							episodes = self.File.Contents(self.folders["watch_history"][str(episode_year)]["episodes"])["lines"]
							media_type_episodes = self.File.Contents(folders["episodes"])["lines"]

							if comment[1] in episodes and comment[1] == episodes[0]:
								self.dictionary["media"]["states"]["first_episode_in_year"] = True

							if comment[1] in media_type_episodes and comment[1] == media_type_episodes[0]:
								self.dictionary["media"]["states"]["first_media_type_episode_in_year"] = True

						# Add file name to file names list
						if file_name not in comments_json["File names"]:
							comments_json["File names"].append(file_name)

						# Add to Comments.json dictionary
						string_time = time

						if string_time != "":
							string_time = str(self.Date.From_String(time)["date"])

						comments_json["Dictionary"][file_name] = {
							"File name": file_name,
							"Type": self.dictionary["media_type"]["plural"]["en"],
							"Times": {
								"date": string_time,
								"date_time_format": time
							},
							"Titles": {}
						}

						dict_ = self.Define_States_Dictionary(self.dictionary)

						if dict_ != {}:
							comments_json["Dictionary"][file_name]["States"] = dict_

						if self.dictionary["media"]["item"]["title"] not in comment[1] and self.dictionary["media"]["states"]["video"] == False:
							title = self.dictionary["media"]["item"]["title"]

							comment[1] += title

							if len(title) > 1 and title[0] + title[1] != ": ":
								comment[1] += " "

						# Get media or episode titles
						for language in self.small_languages:
							full_language = self.full_languages[language]

							titles_file = self.dictionary["media"]["item"]["folders"]["titles"]["root"] + full_language + ".txt"
							titles = self.File.Contents(titles_file)["lines"]

							title = ""

							if titles != []:
								if self.dictionary["media"]["states"]["episodic"] == False:
									i = 0
									for title in titles:
										if file_name == title:
											episode_number = i + 1

										i += 1

								title = titles[int(episode_number) - 1]

								list_ = []

								for alternative_episode_type in self.alternative_episode_types:
									if alternative_episode_type not in title:
										list_.append(False)

								if self.dictionary["media"]["episode"]["separator"] not in title and len(list_) == len(self.alternative_episode_types):
									title = self.dictionary["media"]["episode"]["separator"] + episode_number + " " + title

							comments_json["Dictionary"][file_name]["Titles"][language] = title

							if language == self.user_language and title not in comment[1]:
								comment[1] += title

						# Add YouTube ID, comment link, and comment ID
						if self.dictionary["media"]["states"]["video"] == True:
							youtube_ids_file = self.dictionary["media"]["item"]["folders"]["youtube_ids"]
							youtube_id = self.File.Contents(youtube_ids_file)["lines"][int(episode_number) - 1]

							youtube_comment_id_file = contents["dictionary"]["YouTube IDs"][file_name]
							youtube_comment_ids = self.File.Contents(youtube_comment_id_file)["lines"]

							comments_json["Dictionary"][file_name].update({
								"Video ID": youtube_id,
								"Video link": self.remote_origins["YouTube"] + "watch?v=" + youtube_id + "&list=" + self.dictionary["media"]["item"]["details"][self.language_texts["origin_location"]] + "&index=" + str(int(episode_number)),
							})

							comments_json["Dictionary"][file_name].update({
								"Comment ID": youtube_comment_ids[0],
								"Comment link": comments_json["Dictionary"][file_name]["Video link"] + "&lc=" + youtube_comment_ids[0]
							})

							if youtube_id not in comment[2]:
								comment.insert(2, youtube_id)

						# Update media type comment file with new comment
						text = self.Text.From_List(comment)
						self.File.Edit(file, text, "w")

						if file_name not in comments_contents:
							comments_contents[file_name] = comments_contents["root"] + file_name + ".txt"
							self.File.Create(comments_contents[file_name])

						# Update media comment file with new comment
						self.File.Edit(comments_contents[file_name], text, "w")

				# Sort file names and dictionary keys
				comments_json["File names"] = sorted(comments_json["File names"], key=str.lower)
				comments_json["Dictionary"] = collections.OrderedDict(sorted(comments_json["Dictionary"].items(), key=str.lower))

				# Update media type "Comments.json" file
				self.JSON.Edit(comments_json_file, comments_json)

				# Update media "Comments.json" file
				self.JSON.Edit(comments_contents["comments"], comments_json)

				if "Times" in contents["dictionary"]:
					self.Folder.Delete(contents["dictionary"]["Times"]["root"])

				if "YouTube IDs" in contents["dictionary"]:
					self.Folder.Delete(contents["dictionary"]["YouTube IDs"]["root"])

	def Create_Comment_Dictionary(self):
		self.dictionary = self.Select_Media_Type_And_Media()

		comment = {
			"File name": self.Input.Type(self.File.language_texts["file_name"]),
			"Media Type": self.dictionary["media_type"]["plural"]["en"],
			"Times": {
				"date": "",
				"date_time_format": ""
			},
			"Titles": {}
		}

		date = self.Date.Now()
		comment["Times"]["date_time_format"] = date["date_time_format"][self.user_language]
		comment["Times"]["date"] = str(date["date"])

		if comment["Media Type"] == "Videos":
			comment.update({
				"Video ID": "",
				"Video link": self.remote_origins["YouTube"] + "watch?v={}",
				"ID": "",
				"Link": self.remote_origins["YouTube"] + "watch?v={}&lc={}"
			})

			link = ""

			while validators.url(link) != True:
				# Ask for YouTube comment link
				link = self.Input.Type(self.language_texts["paste_the_comment_link_of_youtube"])

			if validators.url(link) == True:
				link = urlparse(link)
				query = link.query
				parameters = parse_qs(query)	

				comment["Video ID"] = parameters["v"][0]
				comment["ID"] = parameters["lc"][0]

			comment["Video link"] = comment["Video link"].format(comment["Video ID"])
			comment["Link"] = comment["Link"].format(comment["Video ID"], comment["ID"])

		print()
		print(self.Language.language_texts["titles, title()"] + ":")
		print()

		if self.dictionary["media"]["states"]["episodic"] == False:
			comment["Titles"][self.user_language] = comment["File name"]

		for language in self.small_languages:
			if self.dictionary["media"]["states"]["episodic"] == True or self.dictionary["media"]["states"]["episodic"] == False and language != self.user_language:
				translated_language = self.translated_languages[language][self.user_language]

				comment["Titles"][language] = self.Input.Type(translated_language, first_space = False)

		dictionary = self.JSON.To_Python(self.dictionary["media"]["item"]["folders"]["comments"]["comments"])

		dictionary["File names"].append(comment["File name"])
		dictionary["Dictionary"][comment["File name"]] = comment

		dictionary["File names"] = sorted(dictionary["File names"], key=str.lower)
		dictionary["Dictionary"] = collections.OrderedDict(sorted(dictionary["Dictionary"].items(), key=str.lower))

		self.JSON.Edit(self.dictionary["media"]["item"]["folders"]["comments"]["comments"], dictionary)