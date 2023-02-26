# API.py

class API():
	def __init__(self):
		from Utility.Global_Switches import Global_Switches as Global_Switches

		# Global Switches dictionary
		self.switches = Global_Switches().switches["global"]

		self.switches.update({
			"file": {
				"create": True,
				"delete": True,
				"copy": True,
				"move": True,
				"edit": True
			}
		})

		if self.switches["testing"] == True:
			for switch in self.switches["file"]:
				self.switches["file"][switch] = False

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self, ["Secrets", "client_secrets"])

		from Utility.File import File as File
		from Utility.Date import Date as Date
		from Utility.JSON import JSON as JSON

		self.File = File()
		self.Date = Date()
		self.JSON = JSON()

		self.secrets = self.JSON.To_Python(self.folders["apps"]["module_files"]["utility"][self.module["key"]]["secrets"])

	def YouTube(self, api):
		from google.auth.transport.requests import Request
		from google.oauth2.credentials import Credentials
		from google_auth_oauthlib.flow import InstalledAppFlow
		from googleapiclient.discovery import build

		self.folders["apps"]["module_files"]["utility"][self.module["key"]]["token"] = self.folders["apps"]["module_files"]["utility"][self.module["key"]]["root"] + "Token.json"

		self.client_secrets = self.JSON.To_Python(self.folders["apps"]["module_files"]["utility"][self.module["key"]]["client_secrets"])

		api["scopes"] = [
			"https://www.googleapis.com/auth/youtube",
			"https://www.googleapis.com/auth/youtube.force-ssl",
			"https://www.googleapis.com/auth/youtube.readonly",
			"https://www.googleapis.com/auth/youtubepartner"
		]

		api["credentials"] = None

		if self.File.Exist(self.folders["apps"]["module_files"]["utility"][self.module["key"]]["token"]) == True:
			api["credentials"] = Credentials.from_authorized_user_file(self.folders["apps"]["module_files"]["utility"][self.module["key"]]["token"], api["scopes"])

		# If there are no (valid) credentials available, let the user log in
		if not api["credentials"] or not api["credentials"].valid:
			if api["credentials"] and api["credentials"].expired and api["credentials"].refresh_token:
				api["credentials"].refresh(Request())

			else:
				print()
				api["flow"] = InstalledAppFlow.from_client_secrets_file(self.folders["apps"]["module_files"]["utility"][self.module["key"]]["client_secrets"], api["scopes"])
				api["credentials"] = api["flow"].run_local_server(port = 0)

			# Save the credentials for the next run
			self.File.Create(self.folders["apps"]["module_files"]["utility"][self.module["key"]]["token"])
			self.JSON.Edit(self.folders["apps"]["module_files"]["utility"][self.module["key"]]["token"], api["credentials"].to_json(), verbose = False)

		# Define API dictionary
		api.update({
			"version": "v3"
		})

		api["link"] = "https://www.youtube.com/"

		# Build API object
		api["object"] = build(api["name"], api["version"], developerKey = api["key"], credentials = api["credentials"])

		if "parameters" not in api:
			method = api["item"]

			if api["item"] == "playlistItems":
				method = "playlistItems"

			key = "id"

			if api["item"] == "playlistItems":
				key = "playlistId"

			api.update({
				"method": method,
				"submethod": "list",
				"parameters": {
					key: api["id"]
				}
			})

		if "part" not in api["parameters"]:
			api["parameters"]["part"] = ["snippet"]

		if "maxResults" not in api["parameters"] and api["method"] != "comments":
			api["parameters"]["maxResults"] = 1

		# Get method, for example, "videos"
		api["method_object"] = getattr(api["object"], api["method"])

		# Get submethod, for example, "list" method of "videos" method)
		api["submethod_object"] = getattr(api["method_object"](), api["submethod"])

		api["response"] = {
			"nextPageToken": "",
			"items": []
		}

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

			if "pageInfo" in api["response"] and "totalResults" in api["response"]["pageInfo"]:
				api["Dictionary"]["Total Number"] = api["response"]["pageInfo"]["totalResults"]

			for dictionary in api["response"]["items"]:
				snippet = dictionary["snippet"]

				for name in ["channelId", "playlistId"]:
					key = name.replace("Id", "").title()

					if name in snippet and key not in api["Dictionary"]:
						item = {
							"method": name.replace("Id", "") + "s",
							"submethod": "list",
							"parameters": {
								"id": snippet[name]
							}
						}

						api["Dictionary"][key] = self.Call("YouTube", item)["Dictionary"][snippet[name]]

				if "resourceId" in snippet:
					id = snippet["resourceId"]["videoId"]

				elif "playlistId" in api["parameters"]:
					id = api["parameters"]["playlistId"]

				elif "id" in api["parameters"]:
					id = api["parameters"]["id"]

				link = api["link"]

				if api["method"] == "channels":
					link += "channel/"

				if api["method"] == "playlists":
					link += "playlist?list="

				if api["method"] in ["videos", "playlistItems"]:
					link += "watch?v="

				items = api["Dictionary"]

				if api["method"] == "playlistItems":
					if "Videos" not in items:
						items["Videos"] = {}

					items = items["Videos"]

				items[id] = {
					"Title": "",
					"ID": id,
					"Link": link + id,
					"Description": "",
					"Text": {},
					"Time": self.Date.To_String(self.Get_Date(snippet["publishedAt"]))
				}

				for name in ["title", "description"]:
					if name in snippet:
						items[id][name.title()] = snippet[name]

					else:
						items[id].pop(name.title())

				if api["method"] != "comments":
					items[id].pop("Text")

				if api["method"] == "comments":
					items[id].pop("Link")

					items[id]["Text"].update({
						"Original": snippet["textOriginal"],
						"Display": snippet["textDisplay"]
					})

			if self.switches["verbose"] == True:
				print("Progress: " + str(api["Dictionary"]["Number"]) + "/" + str(api["Dictionary"]["Total Number"]))

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