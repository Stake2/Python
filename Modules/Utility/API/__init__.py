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

		# Get the "Secrets" dictionary
		self.secrets = self.JSON.To_Python(self.module["Files"]["Secrets"])

	def Import_Classes(self):
		import importlib

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

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

	def Define_Switches(self):
		# Get the "Switches" dictionary from the "Global_Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# Update the "Switches" dictionary, adding the "File" dictionary
		self.switches.update({
			"File": {
				"Create": True,
				"Delete": True,
				"Copy": True,
				"Move": True,
				"Edit": True
			}
		})

		# If the "Testing" switch is True
		if self.switches["Testing"] == True:
			# Iterate through the switches inside the "File" dictionary
			for switch in self.switches["File"]:
				# Define them as False
				self.switches["File"][switch] = False

	def YouTube(self, api):
		from google.auth.transport.requests import Request
		from google.oauth2.credentials import Credentials
		from google.auth.exceptions import RefreshError
		from google_auth_oauthlib.flow import InstalledAppFlow
		from googleapiclient.discovery import build

		self.token_file = self.module["Files"]["Token"]

		self.client_secrets = self.JSON.To_Python(self.module["Files"]["Client secrets"])

		api["scopes"] = [
			"https://www.googleapis.com/auth/youtube",
			"https://www.googleapis.com/auth/youtube.force-ssl",
			"https://www.googleapis.com/auth/youtube.readonly",
			"https://www.googleapis.com/auth/youtubepartner"
		]

		api["credentials"] = None

		if self.File.Exist(self.token_file) == True:
			api["credentials"] = Credentials.from_authorized_user_file(self.token_file, api["scopes"])

		# If there are no (valid) credentials available, let the user log in
		if (
			not api["credentials"] or not
			api["credentials"].valid
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

			# Save the credentials for the next run
			self.File.Create(self.token_file)
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
			api["parameters"]["part"] = ["snippet"]

		if (
			api["item"] == "playlists" and
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

		# Define empty Dictionary
		api["Dictionary"] = {
			"Number": 0,
			"Total Number": 1
		}

		# Treat response
		while "nextPageToken" in api["response"]:
			# Add next page token
			if api["response"]["nextPageToken"] != "":
				api["parameters"]["pageToken"] = api["response"]["nextPageToken"]

			# Add to number
			api["Dictionary"]["Number"] += 1

			# Define request with parameters
			api["request"] = api["submethod_object"](**api["parameters"])

			# Run request and get response
			api["response"] = api["request"].execute()

			if (
				"pageInfo" in api["response"] and
				"totalResults" in api["response"]["pageInfo"]
			):
				api["Dictionary"]["Total Number"] = api["response"]["pageInfo"]["totalResults"]

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

				# Get Channel or Playlist Dictionary
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
					link_addon = "channel/"

				# If the method is "playlists", define the link addon as the PHP "playlist" file name and the "list" playlist parameter
				elif (
					api["method"] == "playlists" or
					"Playlist" in api["Dictionary"]
				):
					link_addon = "playlist?list="

				# If the method is "videos" or "playlistItems", define the link addon as the PHP "watch" file name and the "v" video parameter
				if api["method"] in ["videos", "playlistItems"]:
					link_addon = "watch?v="

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
					"Channel ID": "",
					"ID": id,
					"Link": link + id,
					"Description": "",
					"Text": {},
					"Date": date["UTC"]["DateTime"]["Formats"]["YYYY-MM-DDTHH:MM:SSZ"],
					"Date (Timezone)": date["Timezone"]["DateTime"]["Formats"]["YYYY-MM-DDTHH:MM:SSZ"],
					"Date (Timezone user format)": date["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"],
					"Times": {
						"Timezone": date["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"],
						"UTC": date["UTC"]["DateTime"]["Formats"]["YYYY-MM-DDTHH:MM:SSZ"]
					},
					"Images": [],
					"Language": ""
				}

				# If title or description are inside the snippet, add them to the item dictionary
				# Else, remove the key from the item dictionary
				for name in ["title", "description"]:
					if name in snippet:
						items[id][name.title()] = snippet[name]

					else:
						items[id].pop(name.title())

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

				# If the "thumbnails" is inside the snippet, create a list with the links of all images
				if "thumbnails" in snippet:
					for image_key in snippet["thumbnails"]:
						image = snippet["thumbnails"][image_key]
						items[id]["Images"].append(image["url"])

				# Else, remove the "Images" key
				else:
					items[id].pop("Images")

				# If the "defaultAudioLanguage" key is inside the snippet, add the "Language" and "Full langauge" keys
				if "defaultAudioLanguage" in snippet:
					items[id]["Language"] = snippet["defaultAudioLanguage"]

					if snippet["defaultAudioLanguage"] not in self.Language.languages["full"]:
						snippet["defaultAudioLanguage"] = snippet["defaultAudioLanguage"].split("-")[0]

					if snippet["defaultAudioLanguage"] not in self.Language.languages["full"]:
						snippet["defaultAudioLanguage"] = "pt"

					items[id]["Full language"] = self.Language.languages["full"][snippet["defaultAudioLanguage"]]

				# Else, remove the "Language" key
				else:
					items[id].pop("Language")

				# Add the localized dictionary
				if "localized" in snippet:
					items[id]["Localized"] = {}

					for key in snippet["localized"]:
						items[id]["Localized"][key.capitalize()] = snippet["localized"][key]

				# Add the Channel ID
				if "channelId" in snippet:
					items[id]["Channel ID"] = snippet["channelId"]

				# Else, remove the "Channel ID" key
				else:
					items[id].pop("Channel ID")

				# If the item is "videos", create the "Video" key for easier accessing of values
				if api["item"] == "videos":
					items["Video"] = items[id]

				# If the item is "playlists", create the "Playlist" key for easier accessing of values
				if api["item"] == "playlists":
					items["Playlist"] = items[id]

				# If the item is "comments", create the "Comment" key for easier accessing of values
				if api["item"] == "comments":
					items["Comment"] = items[id]

				# If the "Title" key is inside the item dictionary and the video is private, remove it from the items dictionary
				if (
					"Title" in items[id] and
					items[id]["Title"] in ["Private video", "Deleted video"]
				):
					items.pop(id)

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