# Test.py

# Import the "importlib" module
import importlib

import re
from urllib.parse import urlparse, parse_qs
import validators
from googleapiclient import discovery

class Main():
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.folders = self.Define_Folders(object = self).folders

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Class methods

		# Get the methods of the class
		self.Get_Methods()

	def Import_Classes(self):
		# Define the list of modules to be imported
		modules = [
			"Define_Folders",
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

	def Define_Basic_Variables(self):
		# Get the modules list
		self.modules = self.JSON.To_Python(self.folders["Apps"]["Modules"]["Modules"])

		# Create a list of the modules that will not be imported
		remove_list = [
			"Define_Folders",
			"Modules",
			"Language",
			"JSON"
		]

		# Iterate through the Utility modules
		for module_title in self.modules["Utility"]["List"]:
			# If the module title is not inside the remove list
			if module_title not in remove_list:
				# Import the module
				module = importlib.import_module("." + module_title, "Utility")

				# Get the sub-class
				sub_class = getattr(module, module_title)

				# Add the sub-class to the current module
				setattr(self, module_title, sub_class())

		# Get the switches dictionary from the "Global Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# Get the Languages dictionary
		self.languages = self.Language.languages

		# Get the user language and full user language
		self.user_language = self.Language.user_language
		self.full_user_language = self.Language.full_user_language

		# Define the local "folders" dictionary as the dictionary inside the "Folder" class
		self.folders = self.Folder.folders

		# Get the Sanitize method of the File class
		self.Sanitize = self.File.Sanitize

		# Get the current date from the Date module
		self.date = self.Date.date

	def Define_Texts(self):
		# Define the "Separators" dictionary
		self.separators = {}

		# Create separators from one to ten characters
		for number in range(1, 11):
			# Define the empty string
			string = ""

			# Add separators to it
			while len(string) != number:
				string += "-"

			# Add the string to the Separators dictionary
			self.separators[str(number)] = string

	def Get_Methods(self):
		# Get the members
		import inspect
 
		members = inspect.getmembers(self, predicate = inspect.ismethod)

		# Define a list of methods to remove
		remove_list = [
			"__init__",
			"Define_Basic_Variables",
			"Define_Texts",
			"Import_Classes"
		]

		# Iterate through the tuples in the members
		for tuple_ in members.copy():
			# Get the member (method) name
			member = tuple_[0]

			# If the member is in the remove list
			if member in remove_list:
				# Remove it
				members.remove(tuple_)

		# Create the dictionary of methods
		methods = {}

		# Iterate through the members, create their dictionaries, and add them to the methods dictionary
		for member in members:
			method = member[1]

			# Replace the underlines in the method name with spaces
			key = member[0].replace("_", " ")

			# Add the method to the methods dictionary
			methods[key] = method

		# List the names
		names = list(methods.keys())

		# List the methods
		methods = list(methods.values())

		# Ask the user to select a method
		method = self.Input.Select(methods, names)["option"]

		# Run the method
		method()

	def Delete_Discord_Messages(self):
		# Define the Discord folder
		discord_folder = self.folders["User"]["Documents"]["root"] + "Discord/"

		# Define the day folder
		day_folder = discord_folder + "08-10-2024/"

		# Define the messages folder
		messages_folder = day_folder + "messages/"

		# Define the index file
		index_json = messages_folder + "index.json"

		# Read the index file
		index = self.JSON.To_Python(index)

	def Shortcut(self):
		# Define the default shortcut dictionary
		dictionary = {
			#"File": "C:/Apps/Sync.lnk"
			"Name": "Requisitos",
			"Folder": "C:/Apps/Shortcuts/",
			"Target": "C:/Apps/requirements.txt"
		}

		# Create the shortcut
		shortcut = self.System.Create_Shortcut(dictionary)

		# Get the shortcut dictionary
		#shortcut = self.System.Get_Shortcut(dictionary)

		# Show it
		self.JSON.Show(shortcut)

	def Write_File_Names_To_File(self):
		folder = self.Folder.Sanitize(self.Input.Type(self.Folder.language_texts["folder, title()"]))

		files = self.Folder.Contents(folder)["file"]["names"]

		i = 0
		for file in files:
			file = file.replace("_", " ")
			file = file.replace("FênixFansub", "Fênix Fansub")
			file = file.replace("OldAge", "Old Age")

			files[i] = file

			i += 1

		file = self.File.Sanitize(self.Input.Type("File to write to"))

		self.File.Edit(file, self.Text.From_List(files, break_line = True))

	def Make_Dual_Audio_Of_Media(self):
		import os
		import subprocess

		print()
		print(self.separators["5"])
		print()

		# Define the media type and title
		media_type = "Animes"
		media_title = "Yuru Camp△"

		# Define the file of titles
		titles_file = "C:/Mega/Bloco De Notas/Redes de Dados/Mídia Audiovisual/Informações de mídia/{}/{}/Temporadas/Season 2/Títulos/Português.txt".format(media_type, media_title)

		titles_file = self.File.Sanitize(titles_file)

		# Define the root folder
		root_folder = "C:/Mídias/{}/{}/Season 2/".format(media_type, media_title)

		root_folder = self.Folder.Sanitize(root_folder)

		# Define the command parameters
		command_parameters = {
			"Video input": 'i "{Root folder}/Legendado/{}.mkv"',
			"Input timestamp offset": "itsoffset 1",
			"Audio input": 'i "{Root folder}/Português/MP3/{}.mp3"',
			"Map external subtitle": 'map 0:s "{Root folder}/Legendas/{}.ass"',
			"Map all": "map 0",
			"Remove subtitles from original file": "map -0:s",
			"Remove attachments from original file": "map -0:t",
			"Map first audio input to second audio stream": "map 1:a",
			"Make first audio the default audio": "disposition:a:1 default",
			"Remove disposition from the first audio": "disposition:a:0 0",
			"Copy streams from original video": "c copy",
			"Add the title of the episode": 'metadata title="{}"',
			"Add the language and title of the Japanese audio": 'metadata:s:a:0 title="Japanese (Japonês)" -metadata:s:a:0 language=ja -metadata:s:a:0 lang=ja -metadata:s:a:0 handler_name=ja',
			"Add the language and title of the Portuguese audio": 'metadata:s:a:1 title="Portuguese (Português)" -metadata:s:a:1 language=pt -metadata:s:a:1 lang=pt -metadata:s:a:1 handler_name=pt',
			"Output file": '"{Root folder}/{}.mp4"'
		}

		# Replace the root folder template with the real root folder
		for key, value in command_parameters.items():
			if "{Root folder}" in value:
				value = value.replace("{Root folder}", root_folder[:-1])

				command_parameters[key] = value

		# Define the command templates
		command_types = {
			"Normal": {
				"Name": "Normal",
				"Remove": [
					#"Input timestamp offset",
					"Map external subtitle",
					"Remove subtitles from original file",
					"Remove attachments from original file"
				]
			},
			"Add external subtitles": {
				"Name": "Add external subtitles",
				"Remove": []
			}
		}

		# Select the command type
		command_type = command_types["Normal"]

		# Define the default command template
		command_template = "ffmpeg -y ^" + "\n"

		# Define the list of keys
		keys = list(command_parameters.keys())

		# Iterate through the command parameters in the dictionary to make the command template
		for key, parameter in command_parameters.items():
			# If the key is not in the "Remove" list of the command type
			if key not in command_type["Remove"]:
				# If the key is not "Output file"
				if key != "Output file":
					# Add a dash to the command template
					command_template += "-"

				# Add the parameter
				command_template += parameter

				# If the key is not the last one
				if key != keys[-1]:
					# Add a break line symbol and a line break symbol
					command_template += " ^" + "\n"

		# Get the list of titles
		titles = self.File.Contents(titles_file)["lines"]

		# Iterate through the titles
		for title in titles:
			# Define the title dictionary with the encoded quotes and no quotes version of the title
			title = {
				"Normal": media_title + " " + title,
				"Encoded": media_title + " " + title.replace('"', '\\"'),
				"No quotes": title.replace('"', ""),
				"Original": title
			}

			# Define the list of items to use to format the command template
			items = [
				title["No quotes"],
				title["No quotes"]
			]

			# If the command type is "Normal"
			if command_type["Name"] == "Normal":
				# Add the encoded title
				items.append(title["Encoded"])

			# If the command type is "Add external subtitles"
			if command_type["Name"] == "Add external subtitles":
				# Add the "No quotes" title
				items.append(title["No quotes"])

				# Add the encoded title
				items.append(title["Encoded"])

			# Add the "No quotes" title
			items.append(title["No quotes"])

			# Sanitize the items
			i = 0
			for item in items:
				item = self.File.Sanitize(item, restricted_characters = True)

				items[i] = item

				i += 1

			# Format the command template with the list of items, making the command
			command = str(command_template.format(*items))

			# If the title is not the first one
			if title["Original"] != titles[0]:
				# Show some space separators
				print()
				print(self.separators["5"])
				print()

			# Show the title
			print(title["Normal"])

			# Copy the command to the clipboard for the user to run it
			self.Text.Copy(command)

			# If the title is not the last one
			if title["Original"] != titles[-1]:
				# Ask for user input before continuing
				self.Input.Type(self.Language.language_texts["continue, title()"])

	def Download_Minecraft_Assets(self):
		# Import the "requests" module
		import requests

		# Define the "Download" dictionary
		self.download = {
			"Folders": {
				"root": self.folders["User"]["AppData"]["Roaming"]["root"] + ".minecraft/",
				"Downloads": {
					"root": self.folders["User"]["Downloads"]["root"] + "Minecraft/"
				}
			},
			"Versions": [],
			"Version": "",
			"Link": "https://resources.download.minecraft.net/"
		}

		# Define the folders
		folders = [
			"Assets"
		]

		for folder in folders:
			self.download["Folders"][folder] = {
				"root": self.download["Folders"]["root"] + folder + "/"
			}

			self.Folder.Create(self.download["Folders"][folder]["root"])

		# Define the sub-folders
		folders = [
			"Indexes",
			"Objects"
		]

		for folder in folders:
			self.download["Folders"]["Assets"][folder] = {
				"root": self.download["Folders"]["Assets"]["root"] + folder + "/"
			}

			self.Folder.Create(self.download["Folders"]["Assets"][folder]["root"])

		# Get the Minecraft versions
		self.download["Versions"] = self.Folder.Contents(self.download["Folders"]["Assets"]["Indexes"]["root"])["file"]["names"]

		self.download["Versions (options)"] = self.download["Versions"]

		i = 0
		for version in self.download["Versions"]:
			if "." not in version:
				version = version[0] + "." + version[1]

				if len(version) == 3:
					version += "0"

				self.download["Versions (options)"][i] = version

			i += 1

		# Select the Minecraft version
		self.download["Version"] = self.Input.Select(self.download["Versions"], language_options = self.download["Versions (options)"])["option"]

		# Create the "Minecraft" folder
		self.Folder.Create(self.download["Folders"]["Downloads"]["root"])

		# Update the "Minecraft" folder with the selected version
		self.download["Folders"]["Downloads"]["root"] += self.download["Version"] + "/"
		self.Folder.Create(self.download["Folders"]["Downloads"]["root"])

		# Define the other folders
		for folder in ["Extracted"]:
			self.download["Folders"]["Downloads"][folder] = {
				"root": self.download["Folders"]["Downloads"]["root"] + folder + "/"
			}

			#self.Folder.Create(self.download["Folders"]["Downloads"][folder]["root"])

		# Define the indexes file name
		file_name = self.download["Version"]

		if "." in file_name:
			split = self.download["Version"].split(".")

			file_name = split[0] + "." + split[1]

		# Get the indexes file
		self.download["Indexes file"] = self.download["Folders"]["Assets"]["Indexes"]["root"] + file_name + ".json"

		# Read the indexes file and get the indexes
		self.download["Indexes"] = self.JSON.To_Python(self.download["Indexes file"])["objects"]

		# Iterate through the indexes in the Indexes dictionary
		i = 1
		length = len(self.download["Indexes"].keys())

		for key, index in self.download["Indexes"].items():
			# Get the hash and mini-hash
			hash = index["hash"]

			mini_hash = hash[0] + hash[1]

			# Create the mini-hash folder
			assets_folder = self.download["Folders"]["Assets"]["Objects"]["root"] + mini_hash + "/"
			self.Folder.Create(assets_folder)

			# Create the "Extracted" folder
			extracted_folder = self.download["Folders"]["Downloads"]["Extracted"]["root"]

			# Get the sub-folders
			sub_folders = key.split("/")
			sub_folders.pop(-1)

			# Create the sub-folders
			for folder in sub_folders:
				extracted_folder += folder + "/"
				#self.Folder.Create(extracted_folder)

			# Define the extracted file
			extracted_file = extracted_folder + key.split("/")[-1]

			# Define the link to download the object file
			link = self.download["Link"] + mini_hash + "/" + hash

			# Define the file path
			file = assets_folder + hash

			if self.File.Exist(file) == False:
				# Show a five dash separator
				print()
				print(self.separators["5"])
				print()

				# Show the current asset number and total number
				print(self.Language.language_texts["number, title()"] + ":")
				print("[" + str(i) + "/" + str(length) + "]")
				print()

				# Show the asset key
				print(self.Language.language_texts["key, title()"] + ":")
				print("[" + key + "]")
				print()

				# Show the folder
				print(self.Language.language_texts["folder, title()"] + ":")
				print("[" + assets_folder + "]")
				print()

				# Show the link
				print(self.Language.language_texts["link, title()"] + ":")
				print("[" + link + "]")
				print()

				# Show the asset object file
				print(self.Language.language_texts["file, title()"] + ":")
				print("[" + file + "]")
				print()

				# Show the extracted and converted file
				print(self.Language.language_texts["file, title()"] + " (2)" + ":")
				print("[" + extracted_file + "]")

				# Download the object file
				response = requests.get(link)

				# Define the content variable
				content = response.content

				# Save the files
				open(file, "wb").write(content)

				#if self.File.Exist(extracted_file) == False:
				#	open(extracted_file, "wb").write(content)

				# Get the status code
				code = response.status_code

				# Show the code
				print()
				print(self.Language.language_texts["code, title()"] + ":")
				print("[" + str(code) + "]")

				# If the code is not "200"
				if code != 200:
					input()

			i += 1

	def Notepad_Theme(self):
		self.File.Close("notepad++")

		self.folders["notepad++"] = {
			"root": self.folders["appdata"]["roaming"]["root"] + "Notepad++/"
		}

		self.folders["notepad++"]["themes"] = {
			"root": self.folders["notepad++"]["root"] + "themes/"
		}

		self.folders["notepad++"]["config"] = self.folders["notepad++"]["root"] + "config.xml"

		config = self.File.Contents(self.folders["notepad++"]["config"])["string"]

		themes = [
			"Littletato",
			"Littletato (Brown)",
			"SpaceLiving"
		]

		new_theme = self.Input.Select(themes)["option"]

		new_theme_config = self.File.Contents(self.folders["notepad++"]["themes"]["root"] + new_theme + ".txt")["string"]

		template = 'name="DarkMode" enable="yes" colorTone="32" '
		dark_theme_name = ' darkThemeName="{}.xml"'.format(new_theme)

		config = re.sub(template + '.*darkThemeName=".*\.xml"', template + new_theme_config + dark_theme_name, config)

		self.File.Edit(self.folders["notepad++"]["config"], config, "w")

		self.Date.Sleep(1)

		notepad = self.folders["root"]["program_files"]["root"] + "Notepad++/notepad++.exe"

		self.File.Open(notepad)

	def Time_Difference(self):
		# Define the before time
		before = self.Date.Now()

		# Show it
		print(before["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"])

		# Test parameters
		# Parâmetros de teste
		hours = 1
		minutes = 30
		seconds = 4

		# Define the list of differences to test
		differences = [
			self.Date.Relativedelta(hours = hours),
			self.Date.Relativedelta(minutes = minutes),
			self.Date.Relativedelta(seconds = seconds),
			self.Date.Relativedelta(hours = hours, minutes = minutes),
			self.Date.Relativedelta(hours = hours, seconds = seconds),
			self.Date.Relativedelta(minutes = minutes, seconds = seconds),
			self.Date.Relativedelta(hours = hours, minutes = minutes, seconds = seconds)
		]

		# Iterate through the differences
		for diff in differences:
			# Define the after, with the before time and the current difference
			after = self.Date.Now(before["Object"] + diff)

			# Define the time difference
			difference = self.Date.Difference(before, after)

			# Show a five dash space separator
			print()
			print(self.separators["5"])
			print()

			# Get the time difference unit text
			unit_text = str(diff).split("(")[1].split(")")[0]
			unit_text = unit_text.capitalize().replace("=+", " + ")

			# Show it
			print(unit_text + ":")

			# Show the difference texts in all languages
			for item in difference["Text"].values():
				print(item)

	def XML(self):
		folder = self.Folder.Sanitize(self.Input.Type(self.Folder.language_texts["folder, title()"]))
		files = self.Folder.Contents(folder, add_sub_folders = False)["file"]["list"]

		titles_file = self.Folder.Sanitize(self.Input.Type(self.File.language_texts["file, title()"] + " " + self.Language.language_texts["genders, type: dict"]["of"] + " " + self.Language.language_texts["titles, title()"].lower()))
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

		accepted_extensions = [
			"mp4",
			"mkv",
			"webm"
		]

		i = 0
		for title in titles:
			print()
			print(self.separators["5"])
			print()
			print(str(i + 1) + "/" + str(len(titles)) + ":")
			print(title)

			sanitized_title = self.File.Sanitize(title, restricted_characters = True)

			if sanitized_title != title:
				print(sanitized_title)

			file = ""

			for item in files:
				if sanitized_title in item:
					extensions_list = []

					for ext in accepted_extensions:
						if (
							"." + ext in item and
							item.split(".")[-1] == ext
						):
							file = item

			if file == "":
				input()

			if file != "":
				print()
				print(self.File.language_texts["file, title()"] + ":")
				print(file)

				track = document.createElement("track")

				for item in ["location", "title", "duration", "extension"]:
					element = document.createElement(item)

					if item == "location":
						from requests.utils import requote_uri

						url = self.File.Name(file) + "." + file.split(".")[-1]
						url = url.replace("#", "%23")

						media_folder = file.replace(folder, "")
						media_folder = media_folder.replace(self.File.Name(file), "")
						media_folder = media_folder.split(".")[0]

						url = media_folder + url

						text = document.createTextNode("file:///./" + url)
						element.appendChild(text)

						print()
						print("URL:")
						print("./" + url)

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
		print(self.separators["5"])
		print()
		print(self.Language.language_texts["playlist, title()"] + ":")
		print(playlist_file)

	def Remove_Dots_From_String(self):
		type = ""

		while type != "exit":
			type = self.Input.Type()

			if type != "exit":
				clipboard = self.Text.Get_Clipboard().splitlines()

				i = 0
				for line in clipboard:
					if line != "" and line[-1] == "." and line[-3] + line[-2] + line[-1] != "...":
						clipboard[i] = clipboard[i][:-1]

					i += 1

				self.Text.Copy(self.Text.From_List(clipboard, break_line = True))

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

					self.File.Edit(file, self.Text.From_List(lines, break_line = True))

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

					self.File.Edit(file, self.Text.From_List(lines, break_line = True))

					if file == list(files.values())[2]:
						file_lines = self.File.Contents(list(files.values())[2])["lines"]
						file_lines.append("[Finish]")

	def Replace_Lines(self):
		lines = list(self.Text.Get_Clipboard().splitlines())

		i = 0
		for line in lines:
			if "msgstr" not in line:
				lines.remove(line)

			i += 1

		string = self.Text.From_List(lines, break_line = True)

		self.Text.Copy(string, verbose = False)

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

		self.Text.Copy(self.Text.From_List(lines, break_line = True))

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

	def Get_Channel_Info(self):
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

		self.JSON.Show(dict_["Channel"])

		self.Text.Copy(dict_["Channel"])

		return dict_

	def Get_Video_Images(self):
		folder = self.Folder.Sanitize(self.Input.Type("Folder"))

		titles_file = folder + self.languages["full"]["pt"] + ".txt"
		titles = self.File.Contents(titles_file)["lines"]

		ids_file = folder + "IDs.txt"
		ids = self.File.Contents(ids_file)["lines"]

		youtube_link = "https://i.ytimg.com/vi/{}/{}default.jpg"

		import wget
		import requests

		downloads_folder = self.folders["user"]["downloads"]["root"]

		download_folder = downloads_folder + folder.split("/")[-3] + "/"
		self.Folder.Create(download_folder)

		i = 0
		for id in ids:
			title = titles[i]

			print()
			print(self.separators["5"])
			print()
			print(str(i + 1) + "/" + str(len(ids)) + ":")
			print()
			print(title + ":")
			print()

			found_file = False

			for quality in ["maxres", "hq"]:
				link = youtube_link.format(id, quality)

				print("\t" + link)

				request = requests.get(link)

				if (
					found_file == False and
					request.status_code == 200
				):
					file_name = self.Sanitize(title, restricted_characters = True) + ".jpg"

					print()
					print()

					file = download_folder + file_name

					if self.File.Exist(file) == False:
						wget.download(link, file)

					print()

					found_file = True

			i += 1

	def Get_Playlist_IDs_And_Titles(self, ask_for_input = True):
		id = self.Get_ID("playlist")

		youtube = {
			"item": "playlistItems",
			"id": id
		}

		dict_ = self.API.Call("YouTube", youtube)["Dictionary"]

		print()
		self.JSON.Show(dict_)
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

			self.Text.Copy(self.Text.From_List(ids, break_line = True))

			input()

			self.Text.Copy(self.Text.From_List(titles, break_line = True))

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
			print(self.separators["5"])
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
		print(self.separators["5"])
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
		before = self.Date.From_String(self.Input.Type())

		units = {
			"years": 0,
			"months": 0,
			"days": 1,
			"hours": 12,
			"minutes": 32,
			"seconds": 19
		}

		before["Object"] += self.Date.Relativedelta(**units)

		before = self.Date.Now(before["Object"])

		print(self.Date.To_String(before, utc = True))

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
			self.Text.Copy(self.Text.From_List(list_, break_line = True))
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