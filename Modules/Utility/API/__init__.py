# API.py

import os
import requests
import urllib.parse

class API():
	def __init__(self):
		# Get modules dictionary
		self.modules = self.Modules.Set(self, ["Date", "File", "JSON"])

		self.Define_Folders(self, ["Secrets", "client_secrets"])

		self.secrets = self.JSON.To_Python(self.folders["apps"]["module_files"]["utility"][self.module["key"]]["secrets"])

	def YouTube(self, api):
		from google.auth.transport.requests import Request
		from google.oauth2.credentials import Credentials
		from google_auth_oauthlib.flow import InstalledAppFlow
		from googleapiclient.discovery import build

		self.folders["apps"]["module_files"]["utility"][self.module["key"]]["token"] = self.folders["apps"]["module_files"]["utility"][self.module["key"]]["root"] + "Token.json"

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
			self.JSON.Edit(self.folders["apps"]["module_files"]["utility"][self.module["key"]]["token"], api["credentials"].to_json())

		# Define API dictionary
		api.update({
			"version": "v3"
		})

		api["link"] = "https://www.youtube.com/"

		# Build API object
		api["object"] = build(api["name"], api["version"], developerKey = api["key"], credentials = api["credentials"])

		if "parameters" not in api:
			if api["item"] == "playlist":
				method = "playlistItems"

			else:
				method = api["item"]

			key = "id"

			if api["item"] == "playlist":
				key = api["item"] + "Id"

			api.update({
				"method": method,
				"submethod": "list",
				"parameters": {
					key: api["id"]
				}
			})

		if "part" not in api["parameters"]:
			api["parameters"]["part"] = ["id", "snippet"]

			if api["method"] == "comments":
				api["parameters"]["part"].remove("id")

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
			"Total Number": 0
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
					"Time": self.Get_Date(snippet["publishedAt"])["YYYY-MM-DDThh:mm:ssZ"]
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

			if self.switches["global"]["verbose"] == True:
				print("Progress: " + str(api["Dictionary"]["Number"]) + "/" + str(api["Dictionary"]["Total Number"]))

		api["Dictionary"].pop("Number")

		return api

	def Get_Date(self, string):
		# Define format for date
		format = "%Y-%m-%dT%H:%M:%SZ"

		if "." in string:
			format = "%Y-%m-%dT%H:%M:%S.%fZ"

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
			api.update(dictionary.copy())

			api.update({
				"name": service.lower(),
				"key": self.secrets[service]["key"],
				"service": getattr(self, service)
			})

			# Run service
			api = api["service"](api)

		return api