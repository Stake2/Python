# API.py

from Global_Switches import Global_Switches as Global_Switches

from Language import Language as Language
from File import File as File
from Folder import Folder as Folder
from Date import Date as Date
from JSON import JSON as JSON
from Text import Text as Text

import requests
import urllib.parse

class API():
	def __init__(self, parameter_switches = None):
		# Global Switches dictionary
		self.global_switches = Global_Switches().global_switches

		self.global_switches.update({
			"testing": False,
			"folder": {
				"create": True,
				"delete": True,
				"copy": True,
				"move": True
			},
			"file": {
				"create": True,
				"delete": True,
				"copy": True,
				"move": True,
				"edit": True
			}
		})

		if parameter_switches != None:
			self.global_switches.update(parameter_switches)

			if "testing" in self.global_switches and self.global_switches["testing"] == True:
				for item in ["folder", "file"]:
					for switch in self.global_switches[item]:
						self.global_switches[item][switch] = False

		self.Language = Language(self.global_switches)
		self.File = File(self.global_switches)
		self.Folder = Folder(self.global_switches)
		self.Date = Date(self.global_switches)
		self.JSON = JSON(self.global_switches)
		self.Text = Text(self.global_switches)

		self.app_settings = self.Language.app_settings
		self.small_languages = self.Language.languages["small"]
		self.full_languages = self.Language.languages["full"]
		self.user_language = self.Language.user_language

		self.folders = self.Folder.folders
		self.root_folders = self.folders["root"]
		self.user_folders = self.folders["user"]
		self.apps_folders = self.folders["apps"]
		self.mega_folders = self.folders["mega"]
		self.notepad_folders = self.folders["notepad"]

		self.date = self.Date.date

		self.Define_Folders()

	def Define_Folders(self):
		self.app_text_files_folder = self.Language.app_text_files_folder

		self.module = {
			"name": self.__module__,
		}

		if "." in self.module["name"]:
			self.module["name"] = self.module["name"].split(".")[0]

		if self.module["name"] == "__main__":
			self.module["name"] = "API"

		self.module["key"] = self.module["name"].lower()

		for item in ["module_files", "modules"]:
			self.apps_folders[item][self.module["key"]] = self.apps_folders[item]["root"] + self.module["name"] + "/"
			self.Folder.Create(self.apps_folders[item][self.module["key"]])

			self.apps_folders[item][self.module["key"]] = self.Folder.Contents(self.apps_folders[item][self.module["key"]], lower_key = True)["dictionary"]

		# Define Secrets file
		self.apps_folders["module_files"][self.module["key"]]["secrets"] = self.apps_folders["module_files"][self.module["key"]]["root"] + "Secrets.json"
		self.File.Create(self.apps_folders["module_files"][self.module["key"]]["secrets"])

		self.secrets = self.JSON.To_Python(self.apps_folders["module_files"][self.module["key"]]["secrets"])

	def YouTube(self, api):
		from google.auth.transport.requests import Request
		from google.oauth2.credentials import Credentials
		from google_auth_oauthlib.flow import InstalledAppFlow
		from googleapiclient.discovery import build

		self.apps_folders["module_files"][self.module["key"]]["token"] = self.apps_folders["module_files"][self.module["key"]]["root"] + "Token.json"

		self.client_secrets = self.JSON.To_Python(self.apps_folders["module_files"][self.module["key"]]["client_secrets"])

		api["scopes"] = [
			"https://www.googleapis.com/auth/youtube",
			"https://www.googleapis.com/auth/youtube.force-ssl",
			"https://www.googleapis.com/auth/youtube.readonly",
			"https://www.googleapis.com/auth/youtubepartner"
		]

		api["credentials"] = None

		if self.File.Exist(self.apps_folders["module_files"][self.module["key"]]["token"]) == True:
			api["credentials"] = Credentials.from_authorized_user_file(self.apps_folders["module_files"][self.module["key"]]["token"], api["scopes"])

		# If there are no (valid) credentials available, let the user log in
		if not api["credentials"] or not api["credentials"].valid:
			if api["credentials"] and api["credentials"].expired and api["credentials"].refresh_token:
				api["credentials"].refresh(Request())

			else:
				print()
				api["flow"] = InstalledAppFlow.from_client_secrets_file(self.apps_folders["module_files"][self.module["key"]]["client_secrets"], api["scopes"])
				api["credentials"] = api["flow"].run_local_server(port = 0)

			# Save the credentials for the next run
			self.File.Create(self.apps_folders["module_files"][self.module["key"]]["token"])
			self.JSON.Edit(self.apps_folders["module_files"][self.module["key"]]["token"], api["credentials"].to_json())

		# Define API dictionary
		api.update({
			"version": "v3"
		})

		api["link"] = "https://www.youtube.com/"

		# Build API object
		api["object"] = build(api["name"], api["version"], developerKey = api["key"], credentials = api["credentials"])

		if "parameters" not in api:
			if "playlist" in api["item"]:
				method = "playlistItems"

			else:
				method = api["item"]

			key = "id"

			if "playlist" in api["item"]:
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
						api["Dictionary"][key].pop("Number")

				if "resourceId" in snippet:
					id = snippet["resourceId"]["videoId"]

				elif "playlistId" in api["parameters"]:
					id = api["parameters"]["playlistId"]

				elif "id" in api["parameters"]:
					id = api["parameters"]["id"]

				date = self.Get_Date(snippet["publishedAt"])

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
					"Number": api["Dictionary"]["Number"],
					"Title": "",
					"ID": id,
					"Link": link + id,
					"Description": "",
					"Text": {},
					"Times": {
						"date": str(date["date"]),
						"date_time_format": date["date_time_format"][self.user_language]
					}
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

			if self.global_switches["verbose"] == True:
				print("Progress: " + str(api["Dictionary"]["Number"]) + "/" + str(api["Dictionary"]["Total Number"]))

		return api

	def Get_Date(self, string):
		# Define format for date
		format = "%Y-%m-%dT%H:%M:%SZ"

		if "." in string:
			format = "%Y-%m-%dT%H:%M:%S.%fZ"

		# Get Date object from date string
		return self.Date.From_String(string, format = format)

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