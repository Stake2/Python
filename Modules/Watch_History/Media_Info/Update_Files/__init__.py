# Update_Files.py

from Watch_History.Watch_History import Watch_History as Watch_History

import re

class Update_Files(Watch_History):
	def __init__(self):
		super().__init__()

		self.Iterate()

	def Iterate(self):
		i = 0
		for plural_media_type in self.media_types["plural"]["en"]:
			key = plural_media_type.lower().replace(" ", "_")

			language_media_type = self.media_types["plural"][self.user_language][i]

			media_list = self.media_types[plural_media_type]["media_list"]
			comments_folder = self.folders["comments"][key]["root"]

			print()
			print("----------")
			print()
			print(language_media_type + ":")

			for media in media_list:
				self.dictionary = {
					"media_type": self.media_types[plural_media_type],
					"media": {
						"title": media
					}
				}

				self.dictionary = self.Select_Media(self.dictionary)

				print()
				print("-")
				print()
				print(self.dictionary["media"]["title"] + ":")

				media_items = [self.dictionary["media"]["item"]["title"]]

				if self.dictionary["media"]["states"]["media_list"] == True:
					media_items = self.dictionary["media"]["items"]["list"]

				for media_item in media_items:
					# Define media item
					self.dictionary = self.Define_Media_Item(self.dictionary, media_item = media_item)

					self.Convert_Comments()

			i += 1

	def Convert_Comments(self):
		folder = self.dictionary["media"]["item"]["folders"]["media_type_comments"]["root"]

		contents = self.Folder.Contents(folder)

		if len(contents["file"]["list"]) != 1:
			print()
			print(self.language_texts["comments, title()"] + ":")
			print()
			print(self.Folder.language_texts["folder, title()"] + ":")
			print(folder)
			print()

			if self.dictionary["media"]["states"]["series_media"] == True:
				comments_json_file = contents["dictionary"]["Comments"]
				comments_json = self.JSON.To_Python(comments_json_file)

				for file in contents["file"]["list"]:
					if "Comments.json" not in file and "Times" not in file:
						file_name = self.File.Name(file)
						episode_number = file_name.split(" ")[0]

						states = {
							"re_watched": {},
							"christmas": False,
							"dubbed": False
						}

						if re.search(" " + self.texts["re_watched, type: regex, en - pt"], file_name) != None:
							states["re_watched"] = {
								"Times": int(file_name.split(self.texts["re_watched, title()"]["en"] + " ")[1].split("x")[0])
							}

						comment = self.File.Contents(file)["lines"]

						if self.language_texts["dubbed"] in comment[1]:
							states["dubbed"] = True

						# Get time
						if "Times" in contents["dictionary"]:
							times_folder = contents["dictionary"]["Times"]

							time = self.File.Contents(times_folder[file_name])["lines"][0]

						else:
							time = self.File.Contents(file)["lines"][4]

						if re.search(" " + self.texts["re_watched, type: regex, en - pt"], file_name) != None:
							file_name = re.sub(" " + self.texts["re_watched, type: regex, en - pt"], "", file_name)

							self.File.Move(file, folder + file_name + ".txt")

						if "25/12" in time:
							states["christmas"] = True

						# Add file name to file names list
						if file_name not in comments_json["File names"]:
							comments_json["File names"].append(file_name)

						# Add to Comments.json dictionary
						comments_json["Dictionary"][file_name] = {
							"File name": file_name,
							"Times": {
								"date": str(self.Date.From_String(time)["date"]),
								"date_time_format": time
							},
							"Titles": {}
						}

						dict_ = {}

						keys = [
							"re_watched",
							"christmas",
							"dubbed"
						]

						for key in keys:
							state = states[key]

							expression = state == True

							if key == "re_watched":
								expression = state != {}

							if expression:
								dict_[key.title()] = states[key.lower()]

						if dict_ != {}:
							comments_json["Dictionary"][file_name]["States"] = dict_

						# Get media or episode titles
						for language in self.small_languages:
							full_language = self.full_languages[language]

							file = self.dictionary["media"]["item"]["folders"]["titles"]["root"] + full_language + ".txt"
							titles = self.File.Contents(file)["lines"]

							title = ""

							if titles != []:
								title = titles[int(episode_number) - 1]

								list_ = []

								for alternative_episode_type in self.alternative_episode_types:
									if alternative_episode_type not in title:
										list_.append(False)

								if self.dictionary["media"]["episode"]["separator"] not in title and len(list_) == len(self.alternative_episode_types):
									title = self.dictionary["media"]["episode"]["separator"] + episode_number + " " + title

							comments_json["Dictionary"][file_name]["Titles"][language] = title

						# Add YouTube ID, comment link, and comment ID
						if self.dictionary["media"]["states"]["video"] == True:
							youtube_ids_file = self.dictionary["media"]["item"]["folders"]["youtube_ids"]
							youtube_id = self.File.Contents(youtube_ids_comment_file)["lines"][int(episode_number) - 1]

							youtube_comment_id_file = contents["dictionary"]["YouTube IDs"][file_name]
							youtube_comment_ids = self.File.Contents(youtube_comment_id_file)["lines"]

							comments_json["Dictionary"][file_name].update({
								"YouTube ID": youtube_id,
								"Link": youtube_comment_ids[1],
								"ID": youtube_comment_ids[0]
							})

						self.JSON.Show(comments_json)
						input()