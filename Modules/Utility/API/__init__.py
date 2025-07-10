# API.py

class API():
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the files of the module
		files = [
			"Secrets",
			"Client secrets",
			"Token"
		]

		# Define the folders of the module
		self.Define_Folders(object = self, files = files)

		# Define the "Switches" dictionary
		self.Define_Switches()

		# Read the "Secrets" dictionary to get the API keys
		self.secrets = self.JSON.To_Python(self.module["Files"]["Secrets"])

	def Import_Classes(self):
		import importlib

		# ---------- #

		# Define the list of modules to be imported
		modules = [
			"Define_Folders",
			"Global_Switches",
			"File",
			"Date",
			"JSON"
		]

		# Iterate through the list of modules
		for module_title in modules:
			# Import the module
			module = importlib.import_module("." + module_title, "Utility")

			# Get the sub-class
			sub_class = getattr(module, module_title)

			# If the module title is not "Define_Folders"
			if module_title != "Define_Folders":
				# Run the sub-class to define its variable
				sub_class = sub_class()

			# Add the sub-class to the current module
			setattr(self, module_title, sub_class)

		# ---------- #

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

		# Import some variables from the "Language" class

		# Import the "languages" dictionary
		self.languages = self.Language.languages

		# Import the "language" dictionary
		self.language = self.Language.language

		# Import the "user" dictionary
		self.user = self.Language.user

		# Import the "separators" dictionary
		self.separators = self.Language.separators

	def Define_Switches(self):
		# Get the "Switches" dictionary from the "Global_Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# Update the "Switches" dictionary, adding the "File" dictionary
		self.switches.update({
			"File": {
				"Create": True,
				"Move": True,
				"Edit": True
			}
		})

	def YouTube(self, api):
		# Import some important modules from the Google module
		from google.auth.transport.requests import Request
		from google.oauth2.credentials import Credentials
		from google.auth.exceptions import RefreshError
		from google_auth_oauthlib.flow import InstalledAppFlow
		from googleapiclient.discovery import build

		# Get the token file
		self.token_file = self.module["Files"]["Token"]

		# Get the client secrets
		self.client_secrets = self.JSON.To_Python(self.module["Files"]["Client secrets"])

		api["scopes"] = [
			"https://www.googleapis.com/auth/youtube",
			"https://www.googleapis.com/auth/youtube.force-ssl",
			"https://www.googleapis.com/auth/youtube.readonly",
			"https://www.googleapis.com/auth/youtubepartner"
		]

		api["credentials"] = None

		if self.File.Exists(self.token_file) == True:
			api["credentials"] = Credentials.from_authorized_user_file(self.token_file, api["scopes"])

		# If there are no (valid) credentials available, let the user log in
		if (
			not api["credentials"] or
			not api["credentials"].valid
		):
			if (
				api["credentials"] and
				api["credentials"].expired and
				api["credentials"].refresh_token
			):
				try:
					api["credentials"].refresh(Request())

				except RefreshError:
					print()

					api["flow"] = InstalledAppFlow.from_client_secrets_file(self.module["Files"]["Client secrets"], api["scopes"])
					api["credentials"] = api["flow"].run_local_server(port = 0)

			else:
				print()

				api["flow"] = InstalledAppFlow.from_client_secrets_file(self.module["Files"]["Client secrets"], api["scopes"])
				api["credentials"] = api["flow"].run_local_server(port = 0)

			# Create the token file
			self.File.Create(self.token_file)

			# Save the credentials for the next run by editing the "Token.json" file with the credentials
			# Passing the "edit" parameter to write into the file even if the file "Edit" switch is False (that means the "Testing" switch is on)
			self.JSON.Edit(self.token_file, api["credentials"].to_json(), edit = True)

		# Define API dictionary
		api.update({
			"version": "v3"
		})

		api["link"] = "https://www.youtube.com/"

		# Build API object
		api["object"] = build(api["name"], api["version"], developerKey = api["key"], credentials = api["credentials"])

		if (
			"submethod" not in api or
			api["submethod"] == ""
		):
			api["submethod"] = "list"

		if "method" not in api:
			api["method"] = api["item"]

		if "parameters" not in api:
			key = "id"

			if api["item"] == "playlistItems":
				key = "playlistId"

			if api["submethod"] != "insert":
				api["parameters"] = {
					key: api["id"]
				}

			if (
				api["item"] == "playlists" and
				api["submethod"] == "insert"
			):
				api["parameters"] = {
					"body": {
						"snippet": {
							"title": api["title"],
							"description": api["description"]
						},
						"status": {
							"privacyStatus": "public"
						}
					}
				}

			if (
				api["item"] == "playlistItems" and
				api["submethod"] == "insert"
			):
				api["parameters"] = {
					"body": {
						"snippet": {
							"playlistId": api["id"],
							"resourceId": {
								"kind": "youtube#video",
								"videoId": api["videoId"]
							}
						}
					}
				}

		if "part" not in api["parameters"]:
			api["parameters"]["part"] = [
				"snippet"
			]

		if api["item"] == "channels":
			api["parameters"]["part"] = [
				"id",
				"snippet",
				"brandingSettings",
				"contentDetails",
				"contentOwnerDetails",
				"localizations",
				"statistics",
				"status",
				"topicDetails"
			]

		if api["item"] == "playlistItems":
			api["parameters"]["part"] = [
				"id",
				"snippet",
				"contentDetails",
				"status"
			]

		if (
			api["item"] == "playlist" and
			api["submethod"] == "list"
		):
			api["parameters"]["part"] = [
				"id",
				"contentDetails",
				"localizations",
				"player",
				"snippet",
				"status"
			]

		if (
			api["item"] == "playlist" and
			api["submethod"] == "insert"
		):
			api["parameters"]["part"] = [
				"snippet",
				"status"
			]

		if "maxResults" not in api["parameters"]:
			if api["item"] not in ["comments", "playlists"]:
				api["parameters"]["maxResults"] = 1

		if (
			api["submethod"] == "insert" and
			"maxResults" in api["parameters"]
		):
			api["parameters"].pop("maxResults")

		# Get method, for example, "videos"
		api["method_object"] = getattr(api["object"], api["method"])

		# Get submethod, for example, "list" method of "videos" method)
		api["submethod_object"] = getattr(api["method_object"](), api["submethod"])

		# Define empty response Dictionary
		api["response"] = {
			"nextPageToken": "",
			"items": []
		}

		# If the "Remove private videos" key is not inside the API dictionary, add it as True
		if "Remove private videos" not in api:
			api["Remove private videos"] = True

		# Define empty Dictionary
		api["Dictionary"] = {
			"Number": 0,
			"Total number": 0
		}

		# Define a dictionary of link addons
		api["Link addons"] = {
			"Video": "watch?v=",
			"Channel": "channel/",
			"Playlist": "playlist?list="
		}

		# Treat the response
		while "nextPageToken" in api["response"]:
			# Add the next page token
			if api["response"]["nextPageToken"] != "":
				api["parameters"]["pageToken"] = api["response"]["nextPageToken"]

			# Define the request with the parameters dictionary
			api["request"] = api["submethod_object"](**api["parameters"])

			# Run the request and get the response
			api["response"] = api["request"].execute()

			if (
				"pageInfo" in api["response"] and
				"totalResults" in api["response"]["pageInfo"]
			):
				api["Dictionary"]["Total number"] = api["response"]["pageInfo"]["totalResults"]

				# Add to the dictionary number
				api["Dictionary"]["Number"] += 1

			# Define shortcuts for the current and total numbers
			current_number = api["Dictionary"]["Number"]
			total_number = api["Dictionary"]["Total number"]

			# If the "Verbose" switch is True
			# And the current number and total number are not zero and also not one
			if (
				self.switches["Verbose"] == True and
				(current_number, total_number) != (0, 0) and
				(current_number, total_number) != (1, 1)
			):
				# If the dictionary number is one
				if api["Dictionary"]["Number"] == 1:
					print()
					print(self.separators["10"])
					print()

				# Show the current number and the total number
				print(self.Language.language_texts["number, title()"] + ":")
				print(str(api["Dictionary"]["Number"]) + "/" + str(api["Dictionary"]["Total number"]))
				print()

			# Define a default id
			id = ""

			if "items" not in api["response"]:
				if "id" in api["response"]:
					id = api["response"]["id"]

				# Get the snippet
				snippet = api["response"]["snippet"]

				# Add the returned item inside to the items list
				api["response"]["items"] = [
					{
						"snippet": snippet
					}
				]

			# Iterate through the response items list
			for dictionary in api["response"]["items"]:
				# Get the snippet
				snippet = dictionary["snippet"]

				# Define a default branding settings variable
				branding_settings = {}

				# If the "brandingSettings" key is in the dictionary, get the branding settings
				if "brandingSettings" in dictionary:
					branding_settings = dictionary["brandingSettings"]

				# Get the channel or playlist dictionary
				for name in ["channelId", "playlistId"]:
					name_key = name.replace("Id", "").title()

					if (
						name in snippet and
						name_key not in api["Dictionary"]
					):
						item = {
							"item": name.replace("Id", "") + "s",
							"submethod": "list",
							"parameters": {
								"id": snippet[name]
							}
						}

						api["Dictionary"][name_key] = self.Call("YouTube", item)["Dictionary"][snippet[name]]

				# Use the video ID as the ID
				if "resourceId" in snippet:
					id = snippet["resourceId"]["videoId"]

				# Else, use the ID inside the first item
				elif "id" in dictionary:
					id = dictionary["id"]

					if (
						type(id) == dict and
						"channelId" in id
					):
						id = id["channelId"]

				# Else, use the Playlist ID as the ID
				elif "playlistId" in api["parameters"]:
					id = api["parameters"]["playlistId"]

				# Else, get the normal ID
				elif "id" in api["parameters"]:
					id = api["parameters"]["id"]

				# Get the root YouTube link
				link = api["link"]

				# If the method is "channels", define the link addon as the channel folder
				if (
					api["method"] == "channels" or
					"Channel" in api["Dictionary"]
				):
					link_addon = api["Link addons"]["Channel"]

				# If the method is "playlists", define the link addon as the PHP "playlist" file name and the "list" playlist parameter
				if (
					api["method"] == "playlists" or
					"Playlist" in api["Dictionary"]
				):
					link_addon = api["Link addons"]["Playlist"]

				# If the method is "videos" or "playlistItems", define the link addon as the PHP "watch" file name and the "v" video parameter
				if api["method"] in ["videos", "playlistItems"]:
					link_addon = api["Link addons"]["Video"]

				# Add the link addon to the link
				link += link_addon

				# Define the items dictionary as the Dictionary
				items = api["Dictionary"]

				# If the method is "playlistItems", create the videos dictionary inside the items list and make that the default list
				if api["method"] == "playlistItems":
					if "Videos" not in items:
						items["Videos"] = {}

					items = items["Videos"]

				# Get the item date
				date = self.Get_Date(snippet["publishedAt"])

				# Add the ID (video, playlist, or comment) to the items dictionary, with the default values
				items[id] = {
					"Title": "",
					"ID": id,
					"Link": link + id,
					"Channel": {
						"Handle": "",
						"ID": "",
						"Link": "",
						"Custom link": ""
					},
					"Playlist": {
						"Title": "",
						"ID": "",
						"Link": ""
					},
					"Video": {
						"Title": "",
						"ID": "",
						"Link": ""
					},
					"Language": "",
					"Country": "",
					"Description": "",
					"Text": {},
					"Times": {
						"Timezone": date["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"],
						"UTC": date["UTC"]["DateTime"]["Formats"]["YYYY-MM-DDTHH:MM:SSZ"]
					},
					"Images": {},
					"Channel trailer": {},
					"Playlists": {},
					"Numbers": {
						"Views": "",
						"Subscribers": "",
						"Videos": ""
					},
					"Status": {
						"Privacy": "",
						"Is linked": "",
						"Long uploads status": "",
						"Made for kids": "",
						"Self-declared made for kids": "",
						"Is channel monetization enabled": ""
					},
					"Localized": {},
					"Localizations": {}
				}

				# If title or description are inside the snippet, add them to the item dictionary
				# Else, remove the key from the item dictionary
				for name in ["title", "description"]:
					if name in snippet:
						items[id][name.title()] = snippet[name]

					else:
						items[id].pop(name.title())

				# Add the Channel ID
				if "channelId" in snippet:
					items[id]["Channel"]["ID"] = snippet["channelId"]

				# If the id is not an empty string
				elif id != "":
					# Define the "Channel ID" key as the defined it
					items[id]["Channel"]["ID"] = id

				# If the method is "channels"
				if (
					api["method"] == "channels" or
					"Channel" in api["Dictionary"]
				):
					# Get the root YouTube link
					local_link = api["link"]

					# Define the channel link as the root link + the channel link addon + the channel ID
					items[id]["Channel"]["Link"] = local_link + api["Link addons"]["Channel"] + items[id]["Channel"]["ID"]

					# Get the channel title from the "channelTitle" key
					if "channelTitle" in snippet:
						items[id]["Channel"] = {
							"Title": snippet["channelTitle"],
							**items[id]["Channel"]
						}

					elif (
						"Title" in items[id] and
						items[id]["Title"] != "" and
						api["method"] == "channels"
					):
						# Define it as the "Title" key and remove the "Title" key
						items[id]["Channel"] = {
							"Title": items[id]["Title"],
							**items[id]["Channel"]
						}

				if "channelId" not in snippet:
					# If the channel ID is empty
					if items[id]["Channel"]["ID"] == "":
						# Remove it
						items[id]["Channel"].pop("ID")

					# If the channel link is empty
					if items[id]["Channel"]["Link"] == "":
						# Remove it
						items[id]["Channel"].pop("Link")

				# If the method is "playlists" or "playlistItems"
				if api["method"] in ["playlists", "playlistItems"]:
					# Add the playlist ID
					items[id]["Playlist"]["ID"] = items[id]["ID"]

					# If the method is "playlistItems"
					if api["method"] == "playlistItems":
						# Update the playlist ID do be the "playlistId"
						items[id]["Playlist"]["ID"] = snippet["playlistId"]

					# Define the playlist link as the root link + the playlist link addon + the playlist ID
					items[id]["Playlist"]["Link"] = local_link + api["Link addons"]["Playlist"] + items[id]["Playlist"]["ID"]

					# If the method is "playlists"
					if api["method"] == "playlists":
						# Add the playlist title
						items[id]["Playlist"]["Title"] = items[id]["Title"]

					if items[id]["Playlist"]["Title"] == "":
						# Remove the "Title" key
						items[id]["Playlist"].pop("Title")

				# If the method is not "playlists" neither "playlistItems"
				if api["method"] not in ["playlists", "playlistItems"]:
					# Remove the playlist "ID" key
					items[id]["Playlist"].pop("ID")

					# Remove the playlist "Link" key
					items[id]["Playlist"].pop("Link")

					# Remove the playlist "Title" key
					items[id]["Playlist"].pop("Title")

				# If the "Playlist" dictionary is empty, remove it
				if items[id]["Playlist"] == {}:
					items[id].pop("Playlist")

				# If the method is either "videos" or "playlistItems"
				if api["method"] in ["videos", "playlistItems"]:
					# Add the video ID
					items[id]["Video"]["ID"] = items[id]["ID"]

					# Define the playlist link as the root link + the playlist link addon + the playlist ID
					items[id]["Video"]["Link"] = local_link + api["Link addons"]["Video"] + items[id]["Video"]["ID"]

					# Add the video title
					items[id]["Video"]["Title"] = items[id]["Title"]

					# If the method is "playlistItems"
					if api["method"] == "playlistItems":
						# Add the video playlist position
						items[id]["Video"]["Position"] = snippet["position"]

				else:
					# Remove the video "ID" key
					items[id]["Video"].pop("ID")

					# Remove the video "Link" key
					items[id]["Video"].pop("Link")

					# Remove the video "Title" key
					items[id]["Video"].pop("Title")

				# If the "Video" dictionary is empty, remove it
				if items[id]["Video"] == {}:
					items[id].pop("Video")

				# Add the custom URl (handle) if it exists
				if "customUrl" in snippet:
					items[id]["Channel"]["Handle"] = snippet["customUrl"]
					items[id]["Channel"]["Custom link"] = link.replace("channel/", "") + items[id]["Channel"]["Handle"]

				else:
					items[id]["Channel"].pop("Handle")
					items[id]["Channel"].pop("Custom link")

				# If the item is not "comments", remove the "Text" key as it is not needed
				if api["item"] != "comments":
					items[id].pop("Text")

				# If the item is "comments", remove the "Link" key as it is not needed
				if api["item"] == "comments":
					items[id].pop("Link")

					# Add the orignal and display texts of the Comment to the item dictionary
					items[id]["Text"].update({
						"Original": snippet["textOriginal"],
						"Display": snippet["textDisplay"]
					})

				# If there are thumbnails, add the images to the "Images" dictionary
				if "thumbnails" in snippet:
					# Define a key map to change the keys
					key_map = {
						"default": "Small",
						"standard": "Standard",
						"medium": "Medium",
						"high": "Large",
						"maxres": "Maximum resolution"
					}

					# Iterate through the keys and thumbnails
					for key, image in snippet["thumbnails"].items():
						# Get the new key
						key = key_map[key]

						# Create a new image dictionary
						new_image = {
							"Link": image["url"]
						}

						# If the "width" key is inside the original image dictionary
						if "width" in image:
							# Transform the dimension numbers into strings and add them to the new image dictionary
							for dimension in ["width", "height"]:
								new_image[dimension.capitalize()] = str(image[dimension]) + "px"

							# Join the two dimensions to create the "Dimensions" key
							new_image["Dimensions"] = str(image["width"]) + "x" + str(image["height"])

						# Add the image dictionary to the "Images" dictionary with the new key
						items[id]["Images"][key] = new_image

					# If the "brandingSettings" key is in the dictionary
					if "brandingSettings" in dictionary:
						# If the "image" key is inside the branding settings dictionary
						if "image" in branding_settings:
							# Get the banner image and add it to the "Images" dictionary
							image = branding_settings["image"]

							items[id]["Images"]["Banner"] = {
								"Link": image["bannerExternalUrl"]
							}

				# Else, remove the "Images" key
				elif branding_settings == {}:
					items[id].pop("Images")

				# If the "defaultAudioLanguage" key is inside the snippet, add the "Language" and "Full langauge" keys
				if "defaultAudioLanguage" in snippet:
					items[id]["Language"] = {
						"Small": snippet["defaultAudioLanguage"]
					}

					if snippet["defaultAudioLanguage"] not in self.languages["full"]:
						snippet["defaultAudioLanguage"] = snippet["defaultAudioLanguage"].split("-")[0]

					if snippet["defaultAudioLanguage"] not in self.languages["full"]:
						snippet["defaultAudioLanguage"] = "pt"

					items[id]["Language"]["Full"] = self.languages["full"][snippet["defaultAudioLanguage"]]

				# If the "defaultLanguage" key is inside the snippet, add the "Language" and "Full langauge" keys
				if "defaultLanguage" in snippet:
					items[id]["Language"] = {
						"Small": snippet["defaultLanguage"]
					}

					if snippet["defaultLanguage"] not in self.languages["full"]:
						snippet["defaultLanguage"] = snippet["defaultLanguage"].split("-")[0]

					if snippet["defaultLanguage"] not in self.languages["full"]:
						snippet["defaultLanguage"] = "pt"

					items[id]["Language"]["Full"] = self.languages["full"][snippet["defaultLanguage"]]

				# Else, remove the "Language" key
				else:
					items[id].pop("Language")

				# Add the localized dictionary
				if "localized" in snippet:
					for key in snippet["localized"]:
						items[id]["Localized"][key.capitalize()] = snippet["localized"][key]

				else:
					items[id].pop("Localized")

				# Add the country if it exists
				if "country" in snippet:
					items[id]["Country"] = snippet["country"]

				else:
					items[id].pop("Country")

				# If the item is "videos", create the "Video" key for easier accessing of values
				if api["item"] == "videos":
					items["Video"] = items[id]

				# If the item is "playlists", create the "Playlist" key for easier accessing of values
				if api["item"] == "playlists":
					items["Playlist"] = items[id]

				# If the item is "comments", create the "Comment" key for easier accessing of values
				if api["item"] == "comments":
					items["Comment"] = items[id]

				# ---------- #

				# If the "brandingSettings" key is in the dictionary
				# And the "channel" dictionary is present
				# And the "unsubscribedTrailer" key is in that dictionary
				if (
					"brandingSettings" in dictionary and
					"channel" in branding_settings and
					"unsubscribedTrailer" in branding_settings["channel"]
				):
					# Get the channel trailer ID
					trailer_id = branding_settings["channel"]["unsubscribedTrailer"]

					# Create the channel trailer dictionary
					items[id]["Channel trailer"] = {
						"ID": trailer_id,
						"Link": api["link"] + "watch?v=" + trailer_id
					}

				else:
					# Remove the "Channel trailer" key
					items[id].pop("Channel trailer")

				# ---------- #

				# If the "contentDetails" key is in the dictionary, get the content details
				if "contentDetails" in dictionary:
					content_details = dictionary["contentDetails"]

					# If the "relatedPlaylists" key is present
					if "relatedPlaylists" in content_details:
						# Get the related playlists
						related_playlists = content_details["relatedPlaylists"]

						# Get the uploads ID
						uploads_id = related_playlists["uploads"]

						# Create the uploads playlist dictionary
						items[id]["Playlists"]["Uploads"] = {
							"ID": uploads_id,
							"Link": api["link"] + "playlist?list=" + uploads_id
						}

						# Get the likes ID
						likes_id = related_playlists["likes"]

						# If it is not empty
						if likes_id != "":
							# Create the likes playlist dictionary
							items[id]["Playlists"]["Likes"] = {
								"ID": likes_id,
								"Link": api["link"] + "playlist?list=" + likes_id
							}

				else:
					# Remove the "Playlists" key
					items[id].pop("Playlists")

				# ---------- #

				# If the "localizations" key is in the dictionary, get the localizations dictionary
				if "localizations" in dictionary:
					localizations = dictionary["localizations"]

					# Add it to the item dictionary
					items[id]["Localizations"] = localizations

				else:
					# Remove the "Localizations" key
					items[id].pop("Localizations")

				# ---------- #

				# If the "statistics" key is in the dictionary
				if "statistics" in dictionary:
					# Get the statistics dictionary
					statistics = dictionary["statistics"]

					# Get the user locale module
					locale = self.user["Locale"]["Module"]

					# Format the numbers
					for key, number in statistics.items():
						number = locale.format_string("%d", int(number), grouping = True)

						# Update it
						statistics[key] = number

					# Update the root "Numbers" dictionary to add the numbers
					items[id]["Numbers"] = {
						"Views": statistics["viewCount"],
						"Subscribers": statistics["subscriberCount"],
						"Videos": statistics["videoCount"]
					}

				else:
					items[id].pop("Numbers")

				# ---------- #

				# If the "status" key is in the dictionary, get the status dictionary
				if "status" in dictionary:
					status = dictionary["status"]

					# Create a new status dictionary to update the keys
					new_status = {
						"Privacy": "",
						"Is linked": "",
						"Long uploads status": "",
						"Made for kids": "",
						"Self-declared made for kids": "",
						"Is channel monetization enabled": ""
					}

					# ----- #

					# If the "privacyStatus" key is present, add it to the new status dictionary
					if "privacyStatus" in status:
						new_status["Privacy"] = status["privacyStatus"].capitalize()

					# Else, remove the key
					else:
						new_status.pop("Privacy")

					# ----- #

					# If the "isLinked" key is present, add it to the new status dictionary
					if "isLinked" in status:
						new_status["Is linked"] = status["isLinked"]

					# Else, remove the key
					else:
						new_status.pop("Is linked")

					# ----- #

					# If the "longUploadsStatus" key is present, add it to the new status dictionary
					if "longUploadsStatusstatus" in status:
						value = status["longUploadsStatus"]

						# If the key is "Longuploadsunspecified"
						if value == "Longuploadsunspecified":
							# Update it to separate the words
							value = "Long uploads unspecified"

						# Update the root key
						new_status["Long uploads status"] = value

					# Else, remove the key
					else:
						new_status.pop("Long uploads status")

					# ----- #

					# If the "madeForKids" key is present, add it to the new status dictionary
					if "madeForKids" in status:
						new_status["Made for kids"] = status["madeForKids"]

					# Else, remove the key
					else:
						new_status.pop("Made for kids")

					# ----- #

					# If the "selfDeclaredMadeForKids" key is present, add it to the new status dictionary
					if "selfDeclaredMadeForKids" in status:
						new_status["Self-declared made for kids"] = status["selfDeclaredMadeForKids"]

					# Else, remove the key
					else:
						new_status.pop("Self-declared made for kids")

					# ----- #

					# If the "isChannelMonetizationEnabled" key is present, add it to the new status dictionary
					if "isChannelMonetizationEnabled" in status:
						new_status["Is channel monetization enabled"] = status["isChannelMonetizationEnabled"]

					# Else, remove the key
					else:
						new_status.pop("Is channel monetization enabled")

					# ----- #

					# If the new status is not empty
					if new_status != {}:
						# Add it to the item dictionary
						items[id]["Status"] = new_status

					# Else, remove the "Status" key
					else:
						items[id].pop("Status")

				# Else, remove the "Status" key
				else:
					items[id].pop("Status")

				# ---------- #

				# If the "Title" key is inside the item dictionary
				# And the video is private or deleted
				# And the "Remove private videos" API key is True
				if (
					"Title" in items[id] and
					items[id]["Title"] in ["Private video", "Deleted video"] and
					api["Remove private videos"] == True
				):
					items.pop(id)

				# ---------- #

				if (
					api["item"] == "search" and
					"nextPageToken" in api["response"]
				):
					api["response"].pop("nextPageToken")

		return api

	def MyAnimeList(self, api):
		import requests
		import urllib

		api.update({
			"url": "https://api.myanimelist.net/v2/anime/" + api["id"] + "?",
			"parameters": {
				"fields": "id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics"
			},
			"headers": {
				"X-MAL-CLIENT-ID": api["key"]
			}
		})

		api["response"] = requests.get(
			api["url"],
			params = api["parameters"],
			headers = api["headers"]
		).json()

		return api

	def Get_Date(self, string):
		# Get Date object from date string
		return self.Date.From_String(string)

	def Call(self, service = None, dictionary = {}):
		# Define service and dictionary
		api = {
			"name": "",
			"key": "",
			"service": ""
		}

		if service != None:
			api.update({
				"name": service.lower(),
				"key": self.secrets[service]["key"],
				"service": getattr(self, service)
			})

			# Get items from provided dictionary
			api.update(dictionary)

			# Run service
			api = api["service"](api)

		return api