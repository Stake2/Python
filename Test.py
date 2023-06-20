# Test.py

import re
from urllib.parse import urlparse, parse_qs
import validators
from googleapiclient import discovery

class Main():
	def __init__(self):
		self.Define_Basic_Variables()

		methods = [
			"Notepad_Theme",
			"XML",
			"Remove_Line_Of_Files",
			"Add_Line_To_Files",
			"Replace_Lines",
			"Get_Video_Info",
			"Get_Playlist_IDs_And_Titles",
			"Get_Channel_ID",
			"Create_Playlist",
			"Add_To_Playlist",
			"Copy_Playlist",
			"Get_Comment_Info",
			"String_To_Date",
			"Time_Difference",
			"Play_Sound"
		]

		method_name = self.Input.Select(methods)["option"]
		method = getattr(self, method_name)
		method()

	def Define_Basic_Variables(self):
		from Utility.Global_Switches import Global_Switches as Global_Switches

		from Utility.API import API as API
		from Utility.File import File as File
		from Utility.Date import Date as Date
		from Utility.Folder import Folder as Folder
		from Utility.Input import Input as Input
		from Utility.JSON import JSON as JSON
		from Utility.Text import Text as Text

		self.Global_Switches = Global_Switches()
		self.Global_Switches.Reset()

		self.API = API()
		self.File = File()
		self.Date = Date()
		self.Folder = Folder()
		self.Input = Input()
		self.JSON = JSON()
		self.Text = Text()

		self.app_settings = self.JSON.Language.app_settings
		self.languages = self.JSON.Language.languages

		self.user_language = self.JSON.Language.user_language
		self.full_user_language = self.JSON.Language.full_user_language

		self.folders = self.Folder.folders

	def Notepad_Theme(self):
		self.File.Close("notepad++")

		self.folders["notepad"] = {
			"root": self.folders["appdata"]["roaming"]["root"] + "Notepad++/"
		}

		self.folders["notepad"]["config"] = self.folders["notepad"]["root"] + "config.xml"

		config = self.File.Contents(self.folders["notepad"]["config"])["string"]

		themes = [
			"Littletato",
			"SpaceLiving"
		]

		new_theme = self.Input.Select(themes)["option"]

		new_theme_config = self.File.Contents(self.folders["notepad"]["root"] + "config (" + new_theme + ").xml")["string"]

		template = 'name="DarkMode" enable="yes" colorTone="32" '
		dark_theme_name = ' darkThemeName="DarkModeDefault ({}).xml"'.format(new_theme)

		config = re.sub(template + '.*darkThemeName=".*\.xml"', template + new_theme_config + dark_theme_name, config)

		self.File.Edit(self.folders["notepad"]["config"], config, "w")

		self.Date.Sleep(2)

		notepad = self.folders["root"]["program_files"]["root"] + "Notepad++/notepad++.exe"

		self.File.Open(notepad)

	def Time_Difference(self):
		before = self.Date.Now()

		self.JSON.Show(before)

		differences = [
			self.Date.Relativedelta(hours = 1),
			self.Date.Relativedelta(hours = 1, minutes = 30),
			self.Date.Relativedelta(hours = 1, minutes = 30, seconds = 2)
		]

		for diff in differences:
			after = self.Date.Now(self.Date.Now()["Object"] + diff)

			difference = self.Date.Difference(before, after)

			print()
			print("-----")
			print()
			print("[" + str(diff) + "]:")

			for item in difference["Text"].values():
				print(item)

	def XML(self):
		folder = self.Folder.Sanitize(self.Input.Type("Folder"))
		files = self.Folder.Contents(folder, add_sub_folders = False)["file"]["list"]

		titles_file = self.Folder.Sanitize(self.Input.Type("Titles file"))
		titles = self.File.Contents(titles_file)["lines"]

		from xml.dom.minidom import getDOMImplementation
		import xml.dom.minidom as md

		implementation = getDOMImplementation()

		document = implementation.createDocument(None, "playlist", None)
		playlist = document.documentElement

		playlist.setAttribute("xmlns", "http://xspf.org/ns/0/")
		playlist.setAttribute("xmlns:vlc", "http://www.videolan.org/vlc/playlist/ns/0/")
		playlist.setAttribute("version", "1")

		# Create title element
		title = document.createElement("title")
		text = document.createTextNode(folder.split("/")[-2])
		title.appendChild(text)
		playlist.appendChild(title)

		# Create trackList element
		trackList = document.createElement("trackList")
		playlist.appendChild(trackList)

		# Create extension element
		extension = document.createElement("extension")
		extension.setAttribute("application", "http://www.videolan.org/vlc/playlist/0")
		playlist.appendChild(extension)

		i = 0
		for title in titles:
			print()
			print("-----")
			print()
			print(str(i + 1) + "/" + str(len(titles)) + ":")
			print(title)

			file = ""

			for item in files:
				if (
					self.File.Sanitize(title, restricted_characters = True) in item and
					"srt" not in item and "png" not in item and "jpg" not in item and "txt" not in item
				):
					file = item

			if file != "":
				print(file)

				track = document.createElement("track")

				for item in ["location", "title", "duration", "extension"]:
					element = document.createElement(item)

					if item == "location":
						from requests.utils import requote_uri
						text = document.createTextNode("file:///./" + requote_uri(self.File.Name(file) + "." + file.split(".")[-1]))
						element.appendChild(text)

					if item == "title":
						text = document.createTextNode(self.File.Name(file))
						element.appendChild(text)

					if item == "duration":
						from pymediainfo import MediaInfo
						media_info = MediaInfo.parse(file)
						duration = media_info.tracks[0].duration

						text = document.createTextNode(str(duration))
						element.appendChild(text)

					if item == "extension":
						element.setAttribute("application", "http://www.videolan.org/vlc/playlist/0")

						id_element = document.createElement("vlc:id")
						id = document.createTextNode(str(i))
						id_element.appendChild(id)

						element.appendChild(id_element)

					track.appendChild(element)

				element = document.createElement("vlc:item")
				element.setAttribute("tid", str(i))
				extension.appendChild(element)

				trackList.appendChild(track)

			i += 1

		export = document.toprettyxml(indent = "\t", newl = "\n")
		export = export[:-1]

		playlist_file = folder + "Playlist.xspf"
		self.File.Create(playlist_file)
		self.File.Edit(playlist_file, export)

		print()
		print(playlist_file)

	def Remove_Line_Of_Files(self):
		folder = self.Folder.Sanitize(self.Input.Type("Folder"))

		contents = self.Folder.Contents(folder, add_sub_folders = True)["file"]["list"]

		i = 0
		for file in contents.copy():
			if i > 5:
				contents.remove(file)

			i += 1

		files = []

		for file in contents:
			for text in ["Games", "Categories", "Time spent", "Times"]:
				if text in file:
					files.append(file)

		file_lines = self.File.Contents(files[1])["lines"]
		file_lines.append("[Finish]")

		self.JSON.Show(files)

		dictionary = {
			"option": ""
		}

		while dictionary["option"] != "[Finish]":
			dictionary = self.Input.Select(file_lines)
			number = dictionary["number_backup"]

			print(number)

			if dictionary["option"] != "[Finish]":
				file_lines.pop(number)

				for file in files:
					lines = self.File.Contents(file)["lines"]
					lines.pop(number)
					self.File.Edit(file, self.Text.From_List(lines))

	def Add_Line_To_Files(self):
		folder = self.Folder.Sanitize(self.Input.Type("Folder"))

		contents = self.Folder.Contents(folder, add_sub_folders = False)["file"]["list"]

		i = 0
		for file in contents.copy():
			if i > 5:
				contents.remove(file)

			i += 1

		files = {}

		for file in contents:
			for text in ["Games", "Categories", "Times", "Time spent"]:
				if text in file:
					files[text] = file

		file_lines = self.File.Contents(list(files.values())[2])["lines"]
		file_lines.append("[Finish]")

		self.JSON.Show(files)

		dictionary = {
			"option": ""
		}

		while dictionary["option"] != "[Finish]":
			if len(file_lines) == 1:
				file_lines.insert(0, "First line")

			dictionary = self.Input.Select(file_lines)
			number = dictionary["number"]

			if dictionary["option"] != "[Finish]":
				for file_name in files:
					file = files[file_name]

					lines = self.File.Contents(file)["lines"]

					text = self.Input.Type(file_name)

					lines.insert(number + 1, text)

					if file_name == "Episodes":
						print()
						print("[" + str(number + 2) + "]:")

					print("\t" + "[" + text + "]")

					self.File.Edit(file, self.Text.From_List(lines))

					if file == list(files.values())[2]:
						file_lines = self.File.Contents(list(files.values())[2])["lines"]
						file_lines.append("[Finish]")

	def Replace_Lines(self):
		input()

		lines = self.Text.Get_Clipboard().splitlines()

		i = 0
		for line in lines:
			if "$" not in line:
				lines[i] = "n"

			i += 1

		string = self.Text.From_List(lines)

		self.Text.Copy(string)

	def Reverse_Lines(self):
		lines = self.Text.Get_Clipboard().splitlines()

		list_ = []

		i = 0
		for line in lines:
			print()
			print(line)
			print(line.split(" ")[0])
			print(line.split(" - "))
			print(line.split(" - ")[0].split(" "))
			second = line.split(" - ")[0].split(" ")
			second.pop(0)
			second = " ".join(second)

			line = line.split(" ")[0] + " " + line.split(" - ")[1] + " - " + second

			lines[i] = line

			i += 1

		self.Text.Copy(self.Text.From_List(lines))

	def Get_ID(self, key = "", link = ""):
		if link == "":
			while link == "":
				link = self.Input.Type("{} link or ID".format(key.title()))

		ids = {
			"video": "v",
			"playlist": "list",
			"playlistItem": "list",
			"comment": "lc"
		}

		id = link

		if "youtube" in link:
			link = urlparse(link)
			query = link.query
			parameters = parse_qs(query)
			id = parameters[ids[key]][0]

		return id

	def Get_Comment_Info(self):
		id = self.Get_ID("comment")

		youtube = {
			"item": "comments",
			"id": id
		}

		dict_ = self.API.Call("YouTube", youtube)["Dictionary"]

		self.JSON.Show(dict_)

	def Get_Video_Info(self):
		id = self.Get_ID("video")

		youtube = {
			"item": "videos",
			"id": id
		}

		dict_ = self.API.Call("YouTube", youtube)["Dictionary"]

		self.JSON.Show(dict_)

	def Get_Playlist_IDs_And_Titles(self, ask_for_input = True):
		id = self.Get_ID("playlist")

		youtube = {
			"item": "playlistItems",
			"id": id
		}

		dict_ = self.API.Call("YouTube", youtube)["Dictionary"]

		print()

		if ask_for_input == False:
			from copy import deepcopy

			local_dict = deepcopy(dict_)

			if "Videos" in local_dict:
				local_dict.pop("Videos")

			self.JSON.Show(local_dict)

		if ask_for_input == True:
			self.JSON.Show(dict_)

			ids = []
			titles = []

			for id in dict_["Videos"]:
				ids.append(id)

				title = dict_["Videos"][id]["Title"]
				titles.append(title)

			self.Text.Copy(self.Text.From_List(ids))

			input()

			self.Text.Copy(self.Text.From_List(titles))

		return dict_

	def Get_Channel_ID(self):
		username = self.Input.Type("Username")

		youtube = {
			"item": "search",
			"parameters": {
				"part": "id,snippet",
				"type": "channel",
				"q": username
			}
		}

		dict_ = self.API.Call("YouTube", youtube)["Dictionary"]

		self.JSON.Show(dict_)

		self.Text.Copy(dict_["Channel"]["ID"])

		return dict_

	def Get_Video(self, link):
		id = self.Get_ID("video", link)

		youtube = {
			"item": "videos",
			"id": id
		}

		dict_ = self.API.Call("YouTube", youtube)["Dictionary"]

		self.JSON.Show(dict_)

		return dict_

	def Ask_For_Video(self):
		link = "Link"

		dictionary = {}

		while link != "":
			print()
			print("[" + str(len(list(dictionary.keys()))) + " + 1" + "]:")

			link = self.Input.Type("Video link or ID")

			if link not in ["", "Link"]:
				dict_ = self.Get_Video(link)

				dictionary[id] = dict_["Video"]

		return dictionary

	def Create_Playlist(self, title = None, description = None):
		if title == None:
			title = self.Input.Type("Playlist title")

		if description == None:
			description = self.Input.Lines("Playlist description")["string"]

		youtube = {
			"item": "playlists",
			"submethod": "insert",
			"title": title,
			"description": description
		}

		dict_ = self.API.Call("YouTube", youtube)["Dictionary"]

		print()

		self.JSON.Show(dict_)

		return dict_

	def Add_To_Playlist(self, playlist_dictionary = None, videos = None):
		if playlist_dictionary == None:
			youtube = {
				"item": "playlists",
				"id": self.Get_ID("playlist")
			}

			playlist_dictionary = self.API.Call("YouTube", youtube)["Dictionary"]

		destination_playlist = playlist_dictionary["Playlist"]

		print()
		self.JSON.Show(playlist_dictionary)

		if videos == None:
			ids = self.Input.Lines("Video links", accept_enter = False)["lines"]

			videos = {}

			for id in ids:
				id = self.Get_ID("video", id)

				videos[id] = self.Get_Video(id)["Video"]

		root_ids = list(videos.keys())

		number = 1
		for video_id in root_ids:
			youtube = {
				"item": "playlistItems",
				"submethod": "insert",
				"id": destination_playlist["ID"],
				"videoId": video_id
			}

			print()
			print("-----")
			print()
			print(str(number) + "/" + str(len(root_ids)) + ":")
			print()
			print("Title:")
			print("[" + videos[video_id]["Title"] + "]")
			print()
			print("ID:")
			print("[" + video_id + "]")

			add_to_playlist = self.API.Call("YouTube", youtube)["Dictionary"]

			number += 1

		print()
		print("-----")
		print()
		self.JSON.Show(add_to_playlist)

		return add_to_playlist

	def Copy_Playlist(self):
		root_playlist = self.Get_Playlist_IDs_And_Titles(ask_for_input = False)

		create_playlist = self.Input.Yes_Or_No("Create playlist")

		if create_playlist == True:
			destination_playlist_dictionary = self.Create_Playlist()
			destination_playlist = destination_playlist_dictionary["Playlist"]

		if create_playlist == False:
			youtube = {
				"item": "playlists",
				"id": self.Get_ID("playlist")
			}

			destination_playlist_dictionary = self.API.Call("YouTube", youtube)["Dictionary"]
			destination_playlist = dictionary["Playlist"]

		videos = root_playlist["Videos"]

		add_to_playlist = self.Add_To_Playlist(destination_playlist_dictionary, videos)

		return add_to_playlist

	def String_To_Date(self):
		before = self.Date.Now(self.Date.Datetime(2023, 1, 20, 2, 10, 22))["Object"]
		today = self.Date.Now()["Object"]

		relative_delta_difference = self.Date.Difference(before, today)
		date_difference = self.Date.Difference(before, today)

		print()
		print("Antes:")
		print("\t" + self.Date.Now(before)["Formats"]["HH:MM:SS DD/MM/YYYY"])
		print()
		print("Hoje:")
		print("\t" + self.Date.Now(today)["Formats"]["HH:MM:SS DD/MM/YYYY"])
		print()
		print("Diferença até hoje (Date.Difference):")
		print("\t" + date_difference["Text"][self.user_language])

		self.JSON.Show(self.Date.Now())

	def Tables(self):
		link = ""

		while validators.url(link) != True:
			link = self.Input.Type("Link of the website with a table")

		import json
		import pandas as pd

		dataframe = pd.read_html(link)[4]

		dictionary = json.loads(dataframe.to_json())

		self.JSON.Show(dictionary)

		titles = dictionary["Título"].copy()

		dictionary = {
			"titles": {},
			"list": titles
		}

		for language in self.languages["small"]:
			dictionary["titles"][language] = []

		a = 104
		i = 1
		for title in dictionary["list"].values():
			print()
			print([title])
			if re.search(" \(BR\).*\(PT\) ", title) != None:
				title = re.split(" \(BR\).*\(PT\) ", title)

			elif re.search(" \(PT\).*\(BR\)", title) != None and re.search(" \(PT\)\/\(BR\)", title) == None:
				title = re.split(" \(PT\) ", title)
				title[0] = '"' + title[1].split('" "')[0]
				title[1] = title[1].split('" "')[1]

			elif re.search(" \(BR \/ PT\) ", title) != None:
				title = re.split(" \(BR \/ PT\) ", title)

			elif re.search(" \(BR\/PT\) ", title) != None:
				title = re.split(" \(BR\/PT\) ", title)

			elif re.search(" \(BR\/PT\)  ", title) != None:
				title = re.split(" \(BR\/PT\)  ", title)

			elif re.search(" \(BR\/PT ", title) != None:
				title = re.split(" \(BR\/PT ", title)

			elif re.search(" \(BR\).*\(PT\) ", title) != None:
				title = re.split(" \(BR\).*\(PT\)  ", title)

			elif re.search(" \(BR\)\/\(PT\) ", title) != None:
				title = re.split(" \(BR\)\/\(PT\) ", title)

			elif re.search(" \(PT\/BR\)", title) != None:
				title = re.split(" \(PT\/BR\)", title)

			elif re.search(" \(PT\)\/\(BR\)", title) != None:
				title = re.split(" \(PT\)\/\(BR\)", title)

			elif re.search(" \(PT\)\/\(BR\)  ", title) != None:
				title = re.split(" \(PT\)\/\(BR\)  ", title)

			elif re.search(" \(BR\) ", title) != None:
				title = re.split(" \(BR\) ", title)

			elif re.search(".*\(PT\) ", title) != None:
				title = '"' + re.sub(".*\(PT\) ", "", title)
				title = re.split(" \(BR\)  ", title)

			ep = "EP" + self.Text.Add_Leading_Zeros(str(i)) + "(" + self.Text.Add_Leading_Zeros(str(a)) + ") "

			english = ep + '"' + title[1]
			portuguese = ep + title[0] + '"'

			if re.search(" \(.*\)", english) != None:
				english = re.sub(" \(.*\)", "", english)

			if re.search('" ', english) != None:
				english = re.sub('" ', '"', english)

			if re.search('"""', english) != None:
				english = re.sub('"""', '"', english)

			if re.search(" \(.*\)", portuguese) != None:
				portuguese = re.sub(" \(.*\)", "", portuguese)

			if re.search('" ', portuguese) != None:
				portuguese = re.sub('" ', '"', portuguese)

			if re.search('"""', portuguese) != None:
				portuguese = re.sub('"""', '"', portuguese)

			print(title)
			print(english)
			print(portuguese)

			dictionary["titles"]["en"].append(english)
			dictionary["titles"]["pt"].append(portuguese)

			a += 1
			i += 1

		for key in dictionary["titles"]:
			list_ = dictionary["titles"][key]
			print(key + ":")
			self.Text.Copy(self.Text.From_List(list_))
			input()

	def Play_Sound(self):
		from gtts import gTTS
		from io import BytesIO

		print()

		import pygame

		mp3_file_object = BytesIO()
		tts = gTTS(self.Input.Type("Text"), lang = "pt")
		tts.save("Test.mp3")
		file = open("test.mp3", "r")

		print(file)

		pygame.init()
		pygame.mixer.init()
		pygame.mixer.music.load(file, "mp3")
		pygame.mixer.music.play()

		import time
		time.sleep(15)

Main()