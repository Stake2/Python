# API.py

# Import the "deepcopy" module from the "copy" module
from copy import deepcopy

class API():
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.folders = self.Define_Folders(object = self).folders

		# Define the "Switches" dictionary
		self.Define_Switches()

		# Define the API dictionary
		self.Define_API()

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

		# Import the "countries" dictionary
		self.countries = self.Language.countries

		# Import the "separators" dictionary
		self.separators = self.Language.separators

	def Define_Switches(self):
		# Get the "Switches" dictionary from the "Global_Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# Update the "Switches" dictionary, adding the "File" dictionary
		self.switches.update({
			"File": {
				"Create": True,
				"Edit": True
			}
		})

	def Define_API(self):
		# Define and create the "Services.json" file
		self.module["Files"]["Services"] = self.module["Folders"]["Module files"]["root"] + "Services.json"
		self.File.Create(self.module["Files"]["Services"])

		# Create a root API dictionary
		self.api = {
			"Services": {},
			"Service": {}
		}

		# Add the "Services" dictionary to the API dictionary
		self.api["Services"] = self.JSON.To_Python(self.module["Files"]["Services"])

	def Call(self, service, request):
		# Get the service dictionary
		self.api["Service"] = self.api["Services"]["Dictionary"][service]

		# Add the "Request" dictionary to the service dictionary
		self.api["Service"]["Request"] = request

		# Get the method for the service
		method = getattr(self, service)

		# Run the method of the service and get the updated service dictionary back
		service = method(self.api["Service"])

		# Return the service dictionary
		return service

	def YouTube(self, service):
		# Import some important modules from the Google modules
		from google.auth.transport.requests import Request
		from google.oauth2.credentials import Credentials
		from google.auth.exceptions import RefreshError
		from google_auth_oauthlib.flow import InstalledAppFlow
		from googleapiclient.discovery import build

		# If the "Credentials" key is a dictionary
		# And is not empty
		if (
			isinstance(service["Credentials"], dict) and
			service["Credentials"] != {}
		):
			# Get the credentials from it
			service["Credentials"] = Credentials.from_authorized_user_info(service["Credentials"], service["Scopes"])

		# If the "Credentials" key is an empty dictionary
		# Or the token is not valid
		if (
			service["Credentials"] == {} or
			service["Credentials"].valid == False
		):
			# If the "Credentials" key is not an empty dictionary
			# And the credentials expired
			# And the refresh token is valid
			if (
				service["Credentials"] and
				service["Credentials"].expired and
				service["Credentials"].refresh_token
			):
				# Try to refresh the credentials using the refrest token
				try:
					service["Credentials"].refresh(Request())

				# If the credentials could not be refreshed
				except RefreshError:
					# Show a five dash space separator
					print()
					print(self.separators["5"])
					print()

					# Ask for the user to authorize the app
					service["App flow"] = InstalledAppFlow.from_client_config(service["Client secrets"], service["Scopes"])

					# Run a local server to get the credentials from the app flow
					service["Credentials"] = service["App flow"].run_local_server(port = 0)

			# Otherwise, either the credentials are missing, still valid, or cannot be refreshed
			else:
				# Show a five dash space separator
				print()
				print(self.separators["5"])
				print()

				# Ask for the user to authorize the app
				service["App flow"] = InstalledAppFlow.from_client_config(service["Client secrets"], service["Scopes"])

				# Run a local server to get the credentials from the app flow
				service["Credentials"] = service["App flow"].run_local_server(port = 0)

			# ---------- #

			# Make a copy of the service dictionary
			service_copy = deepcopy(service)

			# Convert the credentials to JSON
			service_copy["Credentials"] = self.JSON.To_Python(service_copy["Credentials"].to_json())

			# If the "App flow" key is present in the dictionary
			if "App flow" in service_copy:
				# Remove the "App flow" key
				service_copy.pop("App flow")

			# Remove the "Request" key
			service_copy.pop("Request")

			# Update the service dictionary inside the services "Dictionary"
			self.api["Services"]["Dictionary"][service["Name"]] = service_copy

			# Save the credentials for the next run by editing the "Services.json" file
			# (Passing the "edit" parameter to write into the file even if the file "Edit" switch is False (that means the "Testing" switch is on))
			self.JSON.Edit(self.module["Files"]["Services"], self.api["Services"], edit = True)

		# Build the API object
		service["Object"] = build(service["Name"], service["Version"], developerKey = service["API key"], credentials = service["Credentials"])

		# ---------- #

		# Define an items map
		items_map = {
			"Playlist videos": "playlistItems"
		}

		# Define a shortcut to the "Request" dictionary
		request = service["Request"]

		# Update the "Item" key to be a dictionary
		request["Item"] = {
			"Normal": request["Item"],
			"Mapped": request["Item"]
		}

		# Define a shortcut to the request item
		item = request["Item"]["Normal"]

		# If the item is inside the items map dictionary
		if item in items_map:
			# Replace the item with the one inside the items map dictionary
			request["Item"]["Mapped"] = items_map[item]

		# If the "s" letter is not the last character of the mapped item
		if "s" not in request["Item"]["Mapped"]:
			# Add it
			request["Item"]["Mapped"] += "s"

		# Define a shortcut to the mapped item
		mapped_item = request["Item"]["Mapped"]

		# If the "Method" key is not present inside the request dictionary
		if "Method" not in request:
			# Define it as the mapped "Item" key
			request["Method"] = request["Item"]["Mapped"]

		# If the submethod is not present inside the request dictionary
		if "Submethod" not in request:
			# Define it as "List"
			request["Submethod"] = "List"

		# ---------- #

		# If the "Parameters" dictionary is not present inside the request dictionary
		if "Parameters" not in request:
			# Define the key as the "id" key
			key = "id"

			# If the request item is "Playlist videos"
			if item == "Playlist videos":
				# Define the key as "playlistId"
				key = "playlistId"

			# If the submethod is not "Insert"
			if request["Submethod"] != "Insert":
				# Define the "Parameters" dictionary as the "ID" key with the request "ID" value
				request["Parameters"] = {
					key: request["ID"]
				}

			# If the request item is "Playlist"
			# And the submethod is "Insert"
			# (This part creates a new playlist with its title and description)
			if (
				item == "Playlist" and
				request["Submethod"] == "Insert"
			):
				# Define the request "Parameters" dictionary
				request["Parameters"] = {
					"body": { # Define the body dictionary with its keys
						"snippet": { # Define a snippet dictionary for the playlist
							"title": request["Title"], # Define the playlist title
							"description": request["Description"] # Define the playlist description
						},
						"status": {
							"privacyStatus": "public" # Set the status of the playlist to public
						}
					}
				}

			# If the request item is "Playlist videos"
			# And the method is "Insert"
			if (
				item == "Playlist videos" and
				request["Submethod"] == "Insert"
			):
				# Define the request "Parameters" dictionary
				request["Parameters"] = {
					"body": { # Define the body dictionary with its keys
						"snippet": { # Define a snippet dictionary for the playlist
							"playlistId": request["ID"], # Define the playlist ID to add a video to it
							"resourceId": { # Define the "resourceId" dictionary with the YouTube "video" kind and the video ID
								"kind": "youtube#video",
								"videoId": request["Video ID"]
							}
						}
					}
				}

		# ---------- #

		# If the "part" key is not inside the request "Parameters" dictionary
		if "part" not in request["Parameters"]:
			# Define it as a list with only the "snippet" part
			request["Parameters"]["part"] = [
				"snippet"
			]

		# If the request item is "Channel"
		if item == "Channel":
			# Define a list of parts for channels
			request["Parameters"]["part"] = [
				"id",
				"snippet",
				"status",
				"brandingSettings",
				"contentDetails",
				"contentOwnerDetails",
				"localizations",
				"statistics",
				"topicDetails"
			]

		# If the request item is "Playlist"
		if item == "Playlist":
			# If the submethod is "List"
			if request["Submethod"] == "List":
				# Define a list of parts to list playlists
				request["Parameters"]["part"] = [
					"id",
					"snippet",
					"status",
					"contentDetails",
					"localizations",
					"player"
				]

			# If the submethod is "Insert"
			if request["Submethod"] == "Insert":
				# Define a list of parts to insert a video in a playlist
				request["Parameters"]["part"] = [
					"id",
					"snippet",
					"status"
				]

		# If the request item is "Playlist videos"
		if item == "Playlist videos":
			# Define a list of parts for playlist videos
			request["Parameters"]["part"] = [
				"id",
				"snippet",
				"status",
				"contentDetails"
			]

		# If the request item is "Video"
		if item == "Video":
			# Define a list of parts to list videos
			request["Parameters"]["part"] = [
				"id",
				"snippet",
				"status",
				"localizations",
				"contentDetails"
			]

		# If the request item is "Comment"
		if item == "Comment":
			# Define a list of parts to list comments
			request["Parameters"]["part"] = [
				"id",
				"snippet"
			]

		# ---------- #

		# If the "maxResults" key is not inside the request "Parameters" dictionary
		if "maxResults" not in request["Parameters"]:
			# If the request item is neither "Comment" nor "Playlist"
			if item not in ["Comment", "Playlist"]:
				# Define the max results as one
				request["Parameters"]["maxResults"] = 1

		# If the submethod is "Insert"
		# And the "maxResults" key is inside the request "Parameters" dictionary, remove the key
		if (
			request["Submethod"] == "Insert" and
			"maxResults" in request["Parameters"]
		):
			request["Parameters"].pop("maxResults")

		# ---------- #

		# Get the method object for the method
		# For example: "videos", "playlists", "playlistItems", or "comments" (always in lowercase)
		request["Method object"] = getattr(service["Object"], request["Method"].lower())

		# Get the submethod object
		# For example: the "list" submethod of the "videos", "playlists", and "channels" methods (always in lowercase)
		request["Submethod object"] = getattr(request["Method object"](), request["Submethod"].lower())

		# ---------- #

		# If the "Remove private videos" key is not inside the request dictionary, add it as True
		if "Remove private videos" not in request:
			request["Remove private videos"] = True

		# Define an empty results "Dictionary"
		request["Dictionary"] = {
			"Numbers": {
				"Current": 0,
				"Total": 0
			}
		}

		# ---------- #

		# Define an empty "Response" dictionary with the next page token and the list of items
		request["Response"] = {
			"nextPageToken": "",
			"items": []
		}

		# Define a shortcut to the "Response" dictionary
		response = request["Response"]

		# While the "nextPageToken" is inside the "Response" dictionary
		while "nextPageToken" in response:
			# If the "nextPageToken" key is not empty, define it as the current page token
			if response["nextPageToken"] != "":
				request["Parameters"]["pageToken"] = response["nextPageToken"]

			# Define the "Request" dictionary by calling the submethod object with the keys and values of the "Parameters" dictionary
			request["Request"] = request["Submethod object"](**request["Parameters"])

			# Execute the request and get the response
			request["Response"] = request["Request"].execute()

			# Update the shortcut
			response = request["Response"]

			# ---------- #

			# If the "pageInfo" key is inside the response dictionary
			# And the "totalResults" key is also inside it
			if (
				"pageInfo" in response and
				"totalResults" in response["pageInfo"]
			):
				# Define a shortcut to the "pageInfo" dictionary
				page_info = response["pageInfo"]

				# Define the "Total" number as the "totalResults" key
				request["Dictionary"]["Numbers"]["Total"] = page_info["totalResults"]

				# Add to the "Current" number
				request["Dictionary"]["Numbers"]["Current"] += 1

			# Define shortcuts for the current and total numbers
			current_number = request["Dictionary"]["Numbers"]["Current"]
			total_number = request["Dictionary"]["Numbers"]["Total"]

			# If the "Verbose" switch is True
			# And the current number and total number are not zero and also not one
			if (
				self.switches["Verbose"] == True and
				(current_number, total_number) != (0, 0) and
				(current_number, total_number) != (1, 1)
			):
				# If the current number is one
				if request["Dictionary"]["Numbers"]["Current"] == 1:
					# Show a five dash space separator
					print()
					print(self.separators["10"])
					print()

				# Show the current number and the total number
				print(self.Language.language_texts["number, title()"] + ":")
				print(str(current_number) + "/" + str(total_number))
				print()

			# ---------- #

			# Define a default ID as an empty string
			id = ""

			# If the "items" key is not inside the response dictionary
			if "items" not in response:
				# If the "id" key is inside the response dictionary
				if "id" in response:
					id = response["id"]

				# Get the snippet dictionary from the response dictionary
				snippet = response["snippet"]

				# Create a list of items with only the snippet inside it
				response["items"] = [
					{
						"snippet": snippet
					}
				]

			# ---------- #

			# Iterate through the list of items inside the response dictionary
			for dictionary in response["items"]:
				# Get the snippet from the item dictionary
				snippet = dictionary["snippet"]

				# Define a default branding settings dictionary
				branding_settings = {}

				# If the "brandingSettings" key is in the item dictionary
				if "brandingSettings" in dictionary:
					# Update the branding settings dictionary to be the correct one
					branding_settings = dictionary["brandingSettings"]

				# Get the channel or playlist dictionary if the key exists inside the snippet dictionary
				for name in ["Channel", "Playlist"]:
					# Define a name key for the name, converting it to lowercase and adding the "Id" text
					name_key = name.lower() + "Id"

					# If the name key is inside the snippet dictionary
					# And the name is not inside the request "Dictionary" dictionary
					if (
						name_key in snippet and
						name not in request["Dictionary"]
					):
						# Define a shortcut to the snippet ID
						snippet_id = snippet[name_key]

						# Define a local request dictionary
						local_request = {
							"Item": name, # "Channel" or "Playlist"
							"Parameters": {
								"id": snippet_id # Pass the channel or playlist ID
							}
						}

						# Create a new instance of the API class
						instance = API()

						# Request the channel or playlist dictionary from the YouTube API and get the local response
						# (By calling the "Call" method of the new instance of the API class, to not change the variables of the current execution)
						local_response = instance.Call("YouTube", local_request)["Request"]

						# Define the request dictionary in the name key ("Channel" or "Playlist") as the dictionary inside the snippet ID inside the local response "Dictionary"
						request["Dictionary"][name] = local_response["Dictionary"][snippet_id]

				# ---------- #

				# If the request item is not "Video"
				# And the "Video ID" key is inside the request dictionary
				# Or the "videoId" key is inside the snippet dictionary
				if (
					item != "Video" and
					(
						"Video ID" in request or
						"videoId" in snippet
					)
				):
					# If the "Video ID" key is inside the request dictionary
					if "Video ID" in request:
						# Define the video ID as it
						video_id = request["Video ID"]

					else:
						# Define the "videoId" key as the video ID
						video_id = snippet["videoId"]

					# Define a local request dictionary
					local_request = {
						"Item": "Video",
						"Parameters": {
							"id": video_id # Pass the video ID
						}
					}

					# Create a new instance of the API class
					instance = API()

					# Request the video dictionary from the YouTube API and get the local response
					# (By calling the "Call" method of the new instance of the API class, to not change the variables of the current execution)
					local_response = instance.Call("YouTube", local_request)["Request"]

					# Define the request dictionary in the "Video" as the dictionary inside the snippet ID inside the local response "Dictionary"
					request["Dictionary"]["Video"] = local_response["Dictionary"][video_id]

				# ---------- #

				# If the "resourceId" is inside the snippet dictionary
				if "resourceId" in snippet:
					# Define the local ID as the video ID
					id = snippet["resourceId"]["videoId"]

				# Else, if the ID is inside the item dictionary, use it
				elif "id" in dictionary:
					# Get the ID from the "id" key
					id = dictionary["id"]

					# If the ID is a dictionary
					# And the "channelId" key is found inside that dictionary
					if (
						type(id) == dict and
						"channelId" in id
					):
						# Get the correct channel ID
						id = id["channelId"]

				# Else, if the playlist ID is inside the "Parameters" dictionary, use it
				elif "playlistId" in request["Parameters"]:
					id = request["Parameters"]["playlistId"]

				# Else, get the normal ID from the "Parameters" dictionary
				elif "id" in request["Parameters"]:
					id = request["Parameters"]["id"]

				# Define the local items dictionary as the "Dictionary" dictionary
				items = request["Dictionary"]

				# Define the link as an empty string by default
				link = ""

				# If the request item is "Channel"
				if item == "Channel":
					# Define the link template as the channel one
					link_template = service["Link templates"]["Channel"]

					# Replace the "{Channel}" text with the channel ID
					link = link_template.replace("{Channel}", id)

				# If the request item is "Playlist"
				if item == "Playlist":
					# Define the link template as the playlist one
					link_template = service["Link templates"]["Playlist"]

					# Replace the "{Playlist}" text with the playlist ID
					link = link_template.replace("{Playlist}", id)

				# If the request item is "Playlist videos"
				if item == "Playlist videos":
					# If the "Videos" dictionary is not inside the items dictionary, add it
					if "Videos" not in items:
						items["Videos"] = {}

					# Define the local items dictionary as the "Videos" dictionary
					items = items["Videos"]

				# If the request item is either "Video" or "Playlist videos"
				if item in ["Video", "Playlist videos"]:
					# Define the link template as the video one
					link_template = service["Link templates"]["Video"]

					# Replace the "{Video}" text with the video ID
					link = link_template.replace("{Video}", id)

				# ---------- #

				# Create the default item dictionary with some variables
				items[id] = {
					"Title": "",
					"ID": id,
					"Link": link,
					"Description": "",
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
					}
				}

				# ---------- #

				# If there is a title or description inside the snippet dictionary, add them to the item dictionary
				# Else, remove the key from the item dictionary
				for name in ["Title", "Description"]:
					# Define the name key
					name_key = name.lower()

					if name_key in snippet:
						items[id][name] = snippet[name_key]

					else:
						items[id].pop(name)

				# ---------- #

				# If the channel ID is inside the snippet dictionary, add it to the "Channel" dictionary
				if "channelId" in snippet:
					items[id]["Channel"]["ID"] = snippet["channelId"]

				# Else, if the ID is not an empty string
				elif id != "":
					# Define the "Channel ID" key as the defined ID
					items[id]["Channel"]["ID"] = id

				# If the request item is "Channel"
				# Or the "Channel" dictionary is inside the item dictionary
				if (
					item == "Channel" or
					"Channel" in items[id]
				):
					# If the request item is "Channel"
					if item == "Channel":
						# Define the channel link as the local link
						items[id]["Channel"]["Link"] = link

					# Else if the "channelId" key is inside the snippet dictionary
					elif "channelId" in snippet:
						# Get the channel ID
						channel_id = snippet["channelId"]

						# Define the link template as the channel one
						link_template = service["Link templates"]["Channel"]

						# Replace the "{Channel}" text with the channel ID
						link = link_template.replace("{Channel}", channel_id)

						# Define the channel link as the local link
						items[id]["Channel"]["Link"] = link

					# If the channel title is inside the snippet dictionary, add the channel "Title" key to the "Channel" dictionary
					if "channelTitle" in snippet:
						items[id]["Channel"] = {
							"Title": snippet["channelTitle"],
							**items[id]["Channel"]
						}

					# Else if the "Title" key is inside the item dictionary
					# And it is not empty
					# And the request item is "Channel"
					elif (
						"Title" in items[id] and
						items[id]["Title"] != "" and
						item == "Channel"
					):
						# Define the channel title as the root "Title" key
						items[id]["Channel"] = {
							"Title": items[id]["Title"],
							**items[id]["Channel"]
						}

				# If the channel ID is not inside the snippet dictionary
				if "channelId" not in snippet:
					# If the channel ID is empty, remove the "ID" key
					if items[id]["Channel"]["ID"] == "":
						items[id]["Channel"].pop("ID")

					# If the channel link is empty, remove the "Link" key
					if items[id]["Channel"]["Link"] == "":
						items[id]["Channel"].pop("Link")

				# If the custom URL dictionary is inside the snippet dictionary
				if "customUrl" in snippet:
					# Define the channel "Handle" key as the custom URL
					items[id]["Channel"]["Handle"] = snippet["customUrl"]

					# Define the custom link as the root YouTube link plus the handle
					items[id]["Channel"]["Custom link"] = service["Link"] + items[id]["Channel"]["Handle"]

				# Else, remove the "Handle" and "Custom link" keys if they are empty
				else:
					# If the channel handle is empty, remove the key
					if items[id]["Channel"]["Handle"] == "":
						items[id]["Channel"].pop("Handle")

					# If the custom link is empty, remove the key
					if items[id]["Channel"]["Custom link"] == "":
						items[id]["Channel"].pop("Custom link")

				# ---------- #

				# If the request item is "Playlist" or "Playlist videos"
				if item in ["Playlist", "Playlist videos"]:
					# Define the playlist ID as the root ID
					items[id]["Playlist"]["ID"] = items[id]["ID"]

					# If the request item is "Playlist videos"
					if item == "Playlist videos":
						# Update the playlist ID to be the playlist ID inside the snippet dictionary
						items[id]["Playlist"]["ID"] = snippet["playlistId"]

					# Define the playlist link as the local link
					items[id]["Playlist"]["Link"] = link

					# If the request item is "Playlist"
					if item == "Playlist":
						# Define the playlist title as the root "Title" key
						items[id]["Playlist"]["Title"] = items[id]["Title"]

				# If the request item is not "Playlist" neither "Playlist videos"
				if item not in ["Playlist", "Playlist videos"]:
					# Remove the "Playlist" dictionary
					items[id].pop("Playlist")

				# ---------- #

				# If the request is either "Playlist videos", "Video", or "Comment"
				if item in ["Playlist videos", "Video", "Comment"]:
					# If the request item is not "Comment"
					if item != "Comment":
						# Define the video ID as the root ID
						items[id]["Video"]["ID"] = items[id]["ID"]

						# Define the video link as the root link
						items[id]["Video"]["Link"] = link

						# Define the video title as the root "Title" key
						items[id]["Video"]["Title"] = items[id]["Title"]

					# If the request item is "Playlist videos"
					if item == "Playlist videos":
						# Add the video position in the playlist
						items[id]["Video"]["Position"] = snippet["position"]

					# If the request item is "Comment"
					if item == "Comment":
						# Define the video ID as the video ID in the request dictionary
						items[id]["Video"]["ID"] = request["Video ID"]

						# Define the link template as the video one
						link_template = service["Link templates"]["Video"]

						# Replace the "{Video}" text with the video ID and define a local link
						local_link = link_template.replace("{Video}", items[id]["Video"]["ID"])

						# Define the video link as the local link
						items[id]["Video"]["Link"] = local_link

					# If the "Video" key is inside the response dictionary
					if "Video" in request["Dictionary"]:
						# Define the video title as the "Title" key inside the root "Video" dictionary
						items[id]["Video"]["Title"] = request["Dictionary"]["Video"]["Title"]

				# If the request is neither "Playlist videos", "Video", nor "Comment"
				if item not in ["Playlist videos", "Video", "Comment"]:
					# Remove the "Video" dictionary
					items[id].pop("Video")

				# ---------- #

				# Transform the "publishedAt" date into a date dictionary
				date = self.Date.From_String(snippet["publishedAt"])

				# Add the "Times" dictionary of the [channel/playlist/video/comment]
				items[id]["Times"] = {
					"Timezone": date["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"],
					"UTC": date["UTC"]["DateTime"]["Formats"]["YYYY-MM-DDTHH:MM:SSZ"]
				}

				# ---------- #

				# If the request item is "Comment"
				if item == "Comment":
					# Define the link template as the comment one
					link_template = service["Link templates"]["Comment"]

					# Replace the "{Video}" text with the video ID inside the request dictionary
					link = link_template.replace("{Video}", request["Video ID"])

					# Replace the "{Comment}" text with the comment ID
					link = link.replace("{Comment}", items[id]["ID"])

					# Define the root link as the local comment link
					items[id]["Link"] = link

					# Create the "Text" dictionary with the orignal and display texts of the comment inside the item dictionary
					items[id]["Text"] = {
						"Original": snippet["textOriginal"],
						"Display": snippet["textDisplay"]
					}

				# ---------- #

				# If the default audio language is inside the snippet dictionary
				# Or the default language is inside the same dictionary
				if (
					"defaultAudioLanguage" in snippet or
					"defaultLanguage" in snippet
				):
					# Define the default language key as "defaultAudioLanguage"
					language_key = "defaultAudioLanguage"

					# If the "defaultLanguage" key is present, define the language key as it
					if "defaultLanguage" in snippet:
						language_key = "defaultLanguage"

					# Get the language based on the language key
					language = snippet[language_key]

					# Define the "Language" dictionary inside the item dictionary with the "Small" key
					items[id]["Language"] = {
						"Small": language
					}

					# Define a shortcut to the list of full languages
					full_languages = self.languages["full"]

					# If the language is not inside the list of full languages
					if language not in full_languages:
						# Split the language and get the last value from the split list
						language = language.split("-")[0]

					# If the language is still not inside the list of full languages
					if language not in full_languages:
						# Define it as the Brazilian Portuguese language
						language = "pt"

					# Get the full language for the small language
					full_language = full_languages[language]

					# Define the full language inside the "Language" dictionary
					items[id]["Language"]["Full"] = full_language

				# ---------- #

				# If the country is inside the snippet dictionary
				if "country" in snippet:
					# Define a shortcut to the country
					country = snippet["country"]

					# Create the country dictionary
					items[id]["Country"] = {
						"Code": country,
						"Name": self.countries[country]
					}

				# ---------- #

				# If there are thumbnails inside the snippet dictionary
				if "thumbnails" in snippet:
					# Define a key map to change the keys
					key_map = {
						"default": "Small",
						"standard": "Standard",
						"medium": "Medium",
						"high": "Large",
						"maxres": "Maximum resolution"
					}

					# Create the "Images" dictionary
					items[id]["Images"] = {}

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

					# If the branding settings dictionary is not an empty dictionary
					if branding_settings != {}:
						# If the "image" key is inside the branding settings dictionary
						if "image" in branding_settings:
							# Get the banner image and add it to the "Images" dictionary
							image = branding_settings["image"]

							items[id]["Images"]["Banner"] = {
								"Link": image["bannerExternalUrl"]
							}

				# ---------- #

				# If the branding settings dictionary is not an empty dictionary
				# And the "channel" dictionary is present
				if (
					branding_settings != {} and
					"channel" in branding_settings
				):
					# Define a shortcut to the channel dictionary
					channel_dictionary = branding_settings["channel"]

					# If the "unsubscribedTrailer" key is in the "channel" dictionary
					if "unsubscribedTrailer" in channel_dictionary:
						# Get the channel trailer ID
						trailer_id = branding_settings["channel"]["unsubscribedTrailer"]

						# Define the link template as the video one
						link_template = service["Link templates"]["Video"]

						# Replace the "{Video}" text with the trailer ID inside the branding settings dictionary
						link = link_template.replace("{Video}", trailer_id)

						# Create the "Channel trailer" dictionary
						items[id]["Channel trailer"] = {
							"ID": trailer_id,
							"Link": link
						}

					# If the title is inside the channel dictionary
					if "title" in channel_dictionary:
						# Add the channel title to the item dictionary
						items[id] = {
							"Title": channel_dictionary["title"],
							**items[id]
						}

					# If the description is inside the channel dictionary
					if "description" in channel_dictionary:
						# Add the channel description to the item dictionary
						items[id] = {
							"Title": items[id]["Title"],
							"Description": channel_dictionary["description"],
							**items[id]
						}

					# If the country is inside the channel dictionary
					if "country" in channel_dictionary:
						# Define a shortcut to the country
						country = channel_dictionary["country"]

						# Create the country dictionary
						items[id]["Country"] = {
							"Code": country,
							"Name": self.countries[country]
						}

				# ---------- #

				# If there are content details inside the item dictionary
				if "contentDetails" in dictionary:
					# Get the content details dictionary
					content_details = dictionary["contentDetails"]

					# If the "relatedPlaylists" key is present
					if "relatedPlaylists" in content_details:
						# Get the related playlists
						related_playlists = content_details["relatedPlaylists"]

						# Get the uploads ID
						uploads_id = related_playlists["uploads"]

						# Define the link template as the playlist one
						link_template = service["Link templates"]["Playlist"]

						# Replace the "{Playlist}" text with the uploads playlist ID
						uploads_link = link_template.replace("{Playlist}", uploads_id)

						# Create the "Playlists" dictionary with the uploads playlist
						items[id]["Playlists"] = {
							"Uploads": {
								"ID": uploads_id,
								"Link": uploads_link
							}
						}

						# Get the likes ID
						likes_id = related_playlists["likes"]

						# Define the link template as the playlist one
						link_template = service["Link templates"]["Playlist"]

						# Replace the "{Playlist}" text with the likes playlist ID
						likes_link = link_template.replace("{Playlist}", likes_id)

						# If it is not empty
						if likes_id != "":
							# Create the "Likes" playlist dictionary
							items[id]["Playlists"]["Likes"] = {
								"ID": likes_id,
								"Link": likes_link
							}

					# Define a dictionary of video keys to search for
					video_keys = {
						"Duration": "duration",
						"Definition": "definition",
						"Captions": "caption",
						"Licensed content": "licensedContent",
						"Region restriction": "regionRestriction"
					}

					# Iterate through the dictionary of video keys
					for new_key, video_key in video_keys.items():
						# If the video key is present
						if video_key in content_details:
							# Get the value
							value = content_details[video_key]

							# If the new key is "Definition"
							if new_key == "Definition":
								# Convert the value to uppercase
								value = value.upper()

							# Define the key inside the "Video" dictionary
							items[id]["Video"][new_key] = value

							# If the new key is "Region restriction"
							if new_key == "Region restriction":
								# Transform the "allowed" and "blocked" keys into title case and remove the old key
								for key in ["allowed", "blocked"]:
									items[id]["Video"][new_key][key.title()] = items[id]["Video"][new_key][key]
									items[id]["Video"][new_key].pop(key)

				# ---------- #

				# If the statistics dictionary is in the item dictionary
				if "statistics" in dictionary:
					# Get the statistics dictionary
					statistics = dictionary["statistics"]

					# Get the user locale module
					locale = self.user["Locale"]["Module"]

					# Format the numbers of the statistics
					for key, number in statistics.items():
						number = locale.format_string("%d", int(number), grouping = True)

						# Update it
						statistics[key] = number

					# Create the "Numbers" dictionary with the numbers
					items[id]["Numbers"] = {
						"Views": statistics["viewCount"],
						"Subscribers": statistics["subscriberCount"],
						"Videos": statistics["videoCount"]
					}

					# If the "hiddenSubscriberCount" key is inside the statistics dictionary
					if "hiddenSubscriberCount" in statistics:
						# Update the "Numbers" dictionary to add the key
						items[id]["Numbers"] = {
							"Views": items[id]["Numbers"]["Views"],
							"Subscribers": statistics["subscriberCount"],
							"Hidden subscribers": statistics["hiddenSubscriberCount"],
							"Videos": statistics["videoCount"]
						}

				# ---------- #

				# If the status dictionary is in the item dictionary
				if "status" in dictionary:
					# Get the status dictionary
					status = dictionary["status"]

					# Create the "Status" dictionary inside the item dictionary
					items[id]["Status"] = {}

					# If the request item is "Channel"
					if item == "Channel":
						# Define a dictionary of channel status keys to search for
						status_keys = {
							"Privacy": "privacyStatus",
							"Is linked": "isLinked",
							"Long uploads status": "longUploadsStatus",
							"Made for kids": "madeForKids",
							"Self-declared made for kids": "selfDeclaredMadeForKids"
						}

					# If the request item is "Playlist"
					if item == "Playlist":
						# Define a dictionary of playlist status keys to search for
						status_keys = {
							"Privacy": "privacyStatus",
							"Podcast status": "podcastStatus"
						}

					# If the request item is "Playlist videos"
					if item == "Playlist videos":
						# Define a dictionary of playlist videos status keys to search for
						status_keys = {
							"Privacy": "privacyStatus"
						}

					# If the request item is "Video"
					if item == "Video":
						# Define a dictionary of video status keys to search for
						status_keys = {
							"Upload status": "uploadStatus",
							"Upload failure reason": "failureReason",
							"Upload rejection reason": "rejectionReason",
							"Privacy": "privacyStatus",
							"Publish at": "publishAt",
							"License": "license",
							"Embeddable": "embeddable",
							"Public statistics visible": "publicStatsViewable",
							"Made for kids": "madeForKids",
							"Self-declared made for kids": "selfDeclaredMadeForKids",
							"Contains synthetic media": "containsSyntheticMedia"
						}

					# Iterate through the dictionary of status keys
					for new_key, status_key in status_keys.items():
						# If the status key is present
						if status_key in status:
							# Get the status value
							status_value = status[status_key]

							# If the status key is "Long uploads status"
							# And the status value is "longUploadsUnspecified"
							if (
								status_key == "Long uploads status" and
								status_value == "longUploadsUnspecified"
							):
								# Change the status to "Long uploads unspecified"
								status_value = "Long uploads unspecified"

							# Else, if the status value is a string, capitalize it
							elif type(status_value) == str:
								status_value = status_value.capitalize()

								# If the status value is "Youtube"
								if status_value == "Youtube":
									# Change it to "YouTube"
									status_value = "YouTube"

							# Define the key inside the "Video" dictionary as the status value
							items[id]["Status"][new_key] = status_value

				# ---------- #

				# If the localized dictionary is inside the snippet dictionary, add it to the item dictionary
				if "localized" in snippet:
					# Define the "Localized" dictionary
					items[id]["Localized"] = {}

					# Define the sub-keys
					for key in snippet["localized"]:
						items[id]["Localized"][key.capitalize()] = snippet["localized"][key]

				# If the localizations dictionary is inside the snippet dictionary, add it to the item dictionary
				if "localizations" in dictionary:
					localizations = dictionary["localizations"]

					# Add it to the item dictionary
					items[id]["Localizations"] = localizations

				# ---------- #

				# Iterate through the list of item types
				for item_type in ["Channel", "Playlist", "Video", "Comment"]:
					# If the request item is the current item type
					# And the current item type key is not already inside the root items dictionary
					if (
						item == item_type and
						item_type not in items
					):
						# Create the [item type] key in the root items dictionary to access the [item type] more easily
						items[item_type] = items[id]

				# Iterate through the list of item types
				for item_type in ["Channel", "Playlist", "Video", "Comment"]:
					# If the current item type is not "Channel"
					# And the item is not "Channel"
					# And the "Channel" dictionary is in the root items dictionary
					if (
						item_type != "Channel" and
						item != "Channel" and
						"Channel" in items
					):
						# Define the "Channel" key of the item dictionary as the root ["Channel"]["Channel"] key
						items[id]["Channel"] = items["Channel"]["Channel"]

						# If the item type is inside the root items dictionary
						if item_type in items:
							# Define the channel inside the item type dictionary as the root ["Channel"]["Channel"] key
							items[item_type]["Channel"] = items["Channel"]["Channel"]

				# ---------- #

				# If the "Title" key is inside the item dictionary
				# And the video is private or deleted
				# And the "Remove private videos" API key is True
				if (
					"Title" in items[id] and
					items[id]["Title"] in ["Private video", "Deleted video"] and
					request["Remove private videos"] == True
				):
					# Then remove the ID from the dictionary of items
					items.pop(id)

				# ---------- #

				# If the item is "Search"
				# And the next page token is inside the response dictionary
				if (
					item == "search" and
					"nextPageToken" in response
				):
					# Remove the next page token
					response.pop("nextPageToken")

		# Return the service dictionary
		return service

	def MyAnimeList(self, service):
		# Import the requests and urllib modules
		import requests
		import urllib

		# Define a shortcut to the request dictionary
		request = service["Request"]

		# Define the request "Link" as the service link
		request["Link"] = service["Link"]

		# Update the link to add the media type
		request["Link"] += request["Media type"] + "/"

		# Add the media ID
		request["Link"] += request["Media ID"]

		# Define a dictionary of parameters to use
		request["Parameters"] = {
			"fields": "id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics"
		}

		# Define a dictionary of headers to use
		request["Headers"] = {
			"X-MAL-CLIENT-ID": service["API key"]
		}

		# Execute the request with "requests", get the response, and convert it to JSON
		request["Response"] = requests.get(
			request["Link"],
			params = request["Parameters"],
			headers = request["Headers"]
		).json()

		# Return the service dictionary
		return service