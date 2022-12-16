# Folder.py

from Global_Switches import Global_Switches as Global_Switches

from Language import Language as Language
from Date import Date as Date

import os
import platform
import pathlib
import shutil
import re
from distutils.dir_util import copy_tree

class Folder():
	def __init__(self, parameter_switches = None):
		# Global Switches dictionary
		self.global_switches = Global_Switches().global_switches

		self.global_switches.update({
			"folder": {
				"create": True,
				"delete": True,
				"copy": True,
				"move": True,
			},
		})

		if parameter_switches != None:
			self.global_switches.update(parameter_switches)

			if "testing" in self.global_switches and self.global_switches["testing"] == True:
				for switch in self.global_switches["folder"]:
					self.global_switches["folder"][switch] = False

		self.Language = Language(self.global_switches)
		self.Date = Date(self.global_switches)

		self.date = self.Date.date

		self.Define_Folders()
		self.Define_Texts()
		self.Create_Folders()

	def Define_Folders(self):
		self.module_name = self.__module__

		if "." in self.module_name:
			self.module_name = self.module_name.split(".")[0]

		self.module_name_lower = self.module_name.lower()

		if __name__ == "__main__":
			self.module_name = "Folder"

		self.folders = {}

		self.hard_drive_letter = os.path.normpath(pathlib.Path.home().drive) + "/"

		if platform.release() == "10":
			self.hard_drive_letter = "D:/"

		# Root folders
		self.root_folders = {
			"hard_drive_letter": self.hard_drive_letter,
			"users": self.Sanitize(pathlib.Path.home().parent),
			"program_files": os.path.join(self.hard_drive_letter, "Program Files/"),
			"program_files_86": os.path.join(self.hard_drive_letter, "Program Files (x86)/"),
			"system32": {
				"root": self.Sanitize(os.path.join(os.environ["SystemRoot"], "SysNative" if platform.architecture()[0] == '32bit' else "System32")),
			},
			"apps": os.path.join(self.hard_drive_letter, "Apps/"),
			"mega": os.path.join(self.hard_drive_letter, "Mega/"),
			"media": os.path.join(self.hard_drive_letter, "Mídias/"),
			"sony_vegas_files": {
				"root": os.path.join(self.hard_drive_letter, "Sony Vegas Files/"),
			},
			"xampp": {
				"root": os.path.join(self.hard_drive_letter, "XAMPP/"),
			},
		}

		# Apps folders
		self.apps_folders = {
			"root": self.root_folders["apps"],
		}

		self.apps_folders["modules"] = {
			"root": self.Sanitize(os.path.join(self.apps_folders["root"], "Modules/")),
		}

		self.apps_folders["modules"]["usage_modules"] = self.apps_folders["modules"]["root"] + "Usage modules.txt"

		self.apps_folders["app_text_files"] = {
			"root": os.path.join(self.apps_folders["root"], "App Text Files/"),
		}

		self.apps_folders["shortcuts"] = {
			"root": os.path.join(self.apps_folders["root"], "Atalhos/"),
		}

		self.apps_folders["shortcuts"]["white_shortcuts"] = os.path.join(self.apps_folders["shortcuts"]["root"], "Ícone Branco/")

		# User folders
		self.user_folders = {
			"root": self.Sanitize(os.path.join(self.root_folders["users"], pathlib.Path.home().name + "/")),
		}

		self.user_folders["downloads"] = {}
		self.user_folders["downloads"]["root"] = self.Sanitize(os.path.join(self.user_folders["root"], "Downloads/"))

		self.user_folders["videos"] = self.Sanitize(os.path.join(self.user_folders["downloads"]["root"], "Vídeos/"))
		self.user_folders["mega"] = self.Sanitize(os.path.join(self.user_folders["downloads"]["root"], "Mega/"))

		self.user_folders["appdata"] = {
			"root": self.Sanitize("/".join(self.Sanitize(os.getenv("APPDATA")).split("/")[:4])),
		}

		self.user_folders["appdata"]["local"] = self.Sanitize(os.path.join(self.user_folders["appdata"]["root"], "Local/"))
		self.user_folders["appdata"]["roaming"] = self.Sanitize(os.path.join(self.user_folders["appdata"]["root"], "Roaming/"))

		# System32 subfolders
		self.root_folders["system32"]["drivers/etc"] = self.Sanitize(os.path.join(self.root_folders["system32"]["root"], "drivers/etc/"))

		# Sony Vegas Files subfolders
		# Render
		self.root_folders["sony_vegas_files"]["render"] = self.root_folders["sony_vegas_files"]["root"] + "Render/"

		# Story Covers
		self.root_folders["sony_vegas_files"]["story_covers"] = self.root_folders["sony_vegas_files"]["root"] + "Story Covers/"

		# XAMPP folder
		self.root_folders["xampp"]["xampp-control"] = self.root_folders["xampp"]["root"] + "xampp-control.exe"

		# Mega folders
		self.mega_folders = {
			"root": self.root_folders["mega"],
		}

		self.mega_folders["notepad"] = {
			"root": os.path.join(self.mega_folders["root"], "Bloco De Notas/"),
		}

		self.mega_folders["notepad"]["effort"] = {
			"root": os.path.join(self.mega_folders["notepad"]["root"], "Dedicação/"),
		}

		self.mega_folders["notepad"]["effort"]["diary"] = {
			"root": os.path.join(self.mega_folders["notepad"]["effort"]["root"], "Diary/"),
		}

		self.mega_folders["notepad"]["effort"]["diary_slim"] = {
			"root": os.path.join(self.mega_folders["notepad"]["effort"]["root"], "Diary Slim/"),
		}

		self.mega_folders["notepad"]["effort"]["food_and_water_registers"] = {
			"root": os.path.join(self.mega_folders["notepad"]["effort"]["root"], "Food and Water Registers/"),
		}

		self.mega_folders["notepad"]["effort"]["food_and_water_registers"]["food"] = {
			"root": os.path.join(self.mega_folders["notepad"]["effort"]["food_and_water_registers"]["root"], "Food/"),
		}

		self.mega_folders["notepad"]["effort"]["networks"] = {
			"root": os.path.join(self.mega_folders["notepad"]["effort"]["root"], "Networks/"),
		}

		self.mega_folders["notepad"]["effort"]["networks"]["audiovisual_media_network"] = os.path.join(self.mega_folders["notepad"]["effort"]["networks"]["root"], "Audiovisual Media Network/")

		self.mega_folders["notepad"]["effort"]["networks"]["game_network"] = {
			"root": os.path.join(self.mega_folders["notepad"]["effort"]["networks"]["root"], "Game Network/"),
		}

		self.mega_folders["notepad"]["effort"]["networks"]["productive_network"] = os.path.join(self.mega_folders["notepad"]["effort"]["networks"]["root"], "Productive Network/")

		self.mega_folders["notepad"]["effort"]["years"] = {
			"root": os.path.join(self.mega_folders["notepad"]["effort"]["root"], "Years/"),
		}

		self.mega_folders["notepad"]["effort"]["years"]["current"] = {
			"root": os.path.join(self.mega_folders["notepad"]["effort"]["years"]["root"], str(self.date["year"]) + "/"),
		}

		self.mega_folders["notepad"]["effort"]["years"][str(self.date["year"])] = {
			"root": os.path.join(self.mega_folders["notepad"]["effort"]["years"]["root"], str(self.date["year"]) + "/"),
		}

		self.mega_folders["notepad"]["effort"]["years"]["current"]["experienced_media"] = os.path.join(self.mega_folders["notepad"]["effort"]["years"]["current"]["root"], "Experienced Media - Mídias Experimentadas/")

		# Notepad folders
		self.notepad_folders = {}

		for key in self.mega_folders["notepad"]:
			self.notepad_folders[key] = self.mega_folders["notepad"][key]

		for key in self.mega_folders["notepad"]["effort"]:
			self.notepad_folders[key] = self.mega_folders["notepad"]["effort"][key]

		# Mega image folder
		self.mega_folders["image"] = {
			"root": os.path.join(self.mega_folders["root"], "Image/"),
		}

		# Mega PHP folder
		self.mega_folders["php"] = {
			"root": os.path.join(self.mega_folders["root"], "PHP/"),
		}

		# Temporary set PHP folder to Remake
		self.mega_folders["php"] = {
			"root": os.path.join(self.mega_folders["root"], "PHP/Remake/"),
		}

		# Mega PHP JSON folder
		self.mega_folders["php"]["json"] = {
			"root": os.path.join(self.mega_folders["php"]["root"], "JSON/"),
		}

		# Mega PHP Website.json file
		self.mega_folders["php"]["website"] = os.path.join(self.mega_folders["php"]["root"], "Website.json")

		# Mega PHP JSON Colors.json file
		self.mega_folders["php"]["json"]["colors"] = os.path.join(self.mega_folders["php"]["json"]["root"], "Colors.json")

		# Mega PHP JSON URL.json file
		self.mega_folders["php"]["json"]["url"] = os.path.join(self.mega_folders["php"]["json"]["root"], "URL.json")

		# Mega Obsidian's Vaults folder
		self.mega_folders["obsidian_s_vaults"] = {
			"root": os.path.join(self.mega_folders["root"], "Obsidian's Vaults/"),
		}

		self.mega_folders["obsidian_s_vaults"]["creativity"] = {
			"root": os.path.join(self.mega_folders["obsidian_s_vaults"]["root"], "Creativity/"),
		}

		self.mega_folders["obsidian_s_vaults"]["creativity"]["literature"] = {
			"root": os.path.join(self.mega_folders["obsidian_s_vaults"]["creativity"]["root"], "Literature/"),
		}

		self.mega_folders["obsidian_s_vaults"]["creativity"]["literature"]["stories"] = {
			"root": os.path.join(self.mega_folders["obsidian_s_vaults"]["creativity"]["literature"]["root"], "Stories/"),
		}

		# Mega Stories folder
		self.mega_folders["stories"] = {
			"root": os.path.join(self.mega_folders["root"], "Stories/"),
		}

		# Mega Websites folder
		self.mega_folders["websites"] = {
			"root": os.path.join(self.mega_folders["root"], "Websites/"),
		}

		self.mega_folders["websites"]["subdomain"] = self.mega_folders["websites"]["root"] + "Subdomain.txt"
		self.mega_folders["websites"]["netlify"] = self.mega_folders["websites"]["root"] + "Netlify.txt"

		# Mega Websites Images folder
		self.mega_folders["websites"]["images"] = {
			"root": self.mega_folders["websites"]["root"] + "Images/",
		}

		self.mega_folders["websites"]["images"]["story_covers"] = self.mega_folders["websites"]["images"]["root"] + "Story Covers/"		

		# Instantiate File class
		from File import File as File

		self.File = File(self.global_switches)

		# Get website subdomain
		self.subdomain = self.File.Contents(self.mega_folders["websites"]["subdomain"])["lines"][0]

		# Get Netlify domain
		self.netlify_domain = self.File.Contents(self.mega_folders["websites"]["netlify"])["lines"][0]

		# Create links dictionary with Stake2 Website link
		self.links = {
			"Stake2 Website": "https://" + self.subdomain + "." + self.netlify_domain + "/"
		}

		self.module_text_files_folder = self.apps_folders["app_text_files"]["root"] + self.module_name + "/"

		self.texts_file = self.module_text_files_folder + "Texts.json"

		self.folders["root"] = self.root_folders
		self.folders["user"] = self.user_folders
		self.folders["apps"] = self.apps_folders
		self.folders["mega"] = self.mega_folders
		self.folders["notepad"] = self.notepad_folders

	def Define_Texts(self):
		self.texts = self.Language.JSON_To_Python(self.texts_file)

		self.language_texts = self.Language.Item(self.texts)

	def Sanitize(self, path, restricted_characters = False, check = False):
		if restricted_characters == False:
			path = os.path.normpath(path).replace("\\", "/")

			if os.path.splitext(path)[-1] == "" and "/" not in path[-1]:
				path += "/"

		if restricted_characters == True:
			restricted_characters = [":", "?", '"', "\\", "/", "|", "*", "<", ">"]

			for character in restricted_characters:
				if character in path:
					path = path.replace(character, "")

		return path

	def Split(self, path):
		return os.path.split(path)

	def Verbose(self, text, item):
		if self.global_switches["verbose"] == True:
			import inspect

			print()
			print(inspect.stack()[1][3] + "():")
			print("\t" + text + ":")
			print("\t" + item)

	def Exist(self, folder):
		folder = self.Sanitize(folder)

		if os.path.isdir(folder) == True:
			return True

		if os.path.isdir(folder) == False:
			return False

	def Create_Folders(self, folders = None, depth = 0):
		if folders == None:
			folders = self.folders

		for value in folders.values():
			if type(value) != dict and os.path.isfile(value) == False:
				self.Create(value)

			if type(value) == dict:
				found = self.Create_Folders(value, depth = depth + 1)

	def Type(self, text = None):
		if text == None:
			text = self.language_texts["type_or_paste_the_folder"] + ": "

		print()

		return input(text)

	def Create(self, folder = None, text = None):
		if folder == None:
			folder = self.Type(text)

		folder = self.Sanitize(folder)

		if self.Exist(folder) == True:
			return False

		if self.global_switches["folder"]["create"] == True and self.Exist(folder) == False:
			os.mkdir(folder)

			self.Verbose(self.language_texts["folder"].title() + " " + self.language_texts["created"], folder)

			return True

		else:
			return False

	def Delete(self, folder):
		if folder == None:
			folder = self.Type()

		folder = self.Sanitize(folder)

		if self.Exist(folder) == False:
			self.Verbose(self.language_texts["this_folder_does_not_exists"], folder)

			return False

		if self.global_switches["folder"]["delete"] == True and self.Exist(folder) == True:
			try:
				# Folder is empty
				os.rmdir(folder)

			except OSError:
				# Folder is not empty
				shutil.rmtree(folder)

			self.Verbose(self.language_texts["folder"].title() + " " + self.language_texts["deleted"], folder)

			return True

		else:
			return False

	def Copy(self, source_folder = None, destination_folder = None):
		if source_folder == None:
			source_folder = self.Type()

		if destination_folder == None:
			destination_folder = self.Type()

		source_folder = self.Sanitize(source_folder)
		destination_folder = self.Sanitize(destination_folder)

		if self.Exist(source_folder) == False:
			self.Verbose(self.language_texts["this_folder_does_not_exists"], source_folder)

			return False

		if self.global_switches["folder"]["copy"] == True and self.Exist(source_folder) == True:
			copy_tree(source_folder, destination_folder)

			self.Verbose(self.language_texts["source_folder"] + ":\n" + source_folder + "\n\n" + self.language_texts["destination_folder"], destination_folder)

			return True

		else:
			return False

	def Move(self, source_folder = None, destination_folder = None):
		if source_folder == None:
			source_folder = self.Type()

		if destination_folder == None:
			destination_folder = self.Type()

		source_folder = self.Sanitize(source_folder)
		destination_folder = self.Sanitize(destination_folder)

		if self.Exist(source_folder) == False:
			self.Verbose(self.language_texts["this_folder_does_not_exists"], source_folder)

			return False

		if self.global_switches["folder"]["move"] == True and self.Exist(source_folder) == True:
			for file_name in os.listdir(source_folder):
				source = os.path.join(source_folder, file_name)
				destination = os.path.join(destination_folder, file_name)

				shutil.move(source, destination)

			self.Verbose(self.language_texts["source_folder"] + ":\n" + source_folder + "\n\n" + self.language_texts["destination_folder"], destination_folder)

			return True

		else:
			return False

	def List(self, folder, contents_parameter = None):
		contents = contents_parameter

		if contents == None:
			contents = self.contents

		defined_contents = ""

		for item in os.listdir(folder):
			name = item
			item = self.Sanitize(folder + item)
			folder_name = item.split("/")[-2]

			self.contents["size"] += os.stat(folder + "/" + name).st_size

			if os.path.isdir(item) == True:
				if name not in self.contents["folder"]["names"]:
					self.contents["folder"]["names"].append(name)

				if item not in self.contents["folder"]["list"]:
					self.contents["folder"]["list"].append(item)

				defined_contents = contents["folders"]

				if folder_name not in defined_contents:
					defined_contents[folder_name] = {}

				defined_contents[folder_name]["root"] = self.Sanitize(item)

			if os.path.isfile(item) == True:
				item = self.Sanitize(folder + name, check = False)

				if name not in self.contents["file"]["names"]:
					self.contents["file"]["names"].append(name)

				if item not in self.contents["file"]["list"]:
					self.contents["file"]["list"].append(item)

				defined_contents = contents["files"]

				if contents_parameter != None and folder_name not in defined_contents:
					defined_contents[folder_name] = {}

				file_name = os.path.splitext(os.path.basename(item))[0]

				if contents_parameter == None:
					defined_contents[file_name] = item

				if contents_parameter != None:
					defined_contents[folder_name][file_name] = item

		return defined_contents

	def Old_Contents(self, folder, add_none = False):
		folder = self.Sanitize(folder)

		self.contents = {
			"folders": {},
			"root_folders": [],
			"folder_list": [],
			"folder_names": [],
			"files": {},
			"file_list": [],
			"file_names": [],
			"size": 0,
		}

		self.contents["root_folders"] = os.listdir(folder)

		for item in self.contents["root_folders"].copy():
			if os.path.isfile(self.Sanitize(folder + item)) == True:
				self.contents["root_folders"].remove(item)

		if self.Exist(folder) == True:
			self.List(folder)

			folders = self.contents["folders"].copy()

			for local_folder in folders:
				self.List(self.contents["folders"][local_folder]["root"], {"folders": self.contents["folders"][local_folder], "files": self.contents["files"]})

				if local_folder not in self.contents["files"]:
					self.contents["files"][local_folder] = {}

				for sub_folder_name in self.contents["folders"][local_folder].copy():
					if sub_folder_name in self.contents["folders"][local_folder]:
						sub_folder = self.contents["folders"][local_folder][sub_folder_name]

						if type(sub_folder) == dict:
							if sub_folder_name not in self.contents["folders"][local_folder]:
								self.contents["folders"][local_folder][sub_folder_name] = {}

							if sub_folder_name not in self.contents["files"][local_folder]:
								self.contents["files"][local_folder][sub_folder_name] = {}

							sub_folder = sub_folder["root"]

						dictionary = self.List(sub_folder, {"folders": self.contents["folders"][local_folder], "files": self.contents["folders"][local_folder]})

						for key in dictionary:
							value = dictionary[key]

							if type(value) == str:
								if os.path.isdir(value) == True:
									self.contents["folders"][local_folder][key] = value

							if type(value) == dict:
								for sub_key in value:
									sub_value = value[sub_key]

									if os.path.isfile(sub_value) == True:
										if key == local_folder:
											self.contents["files"][local_folder][sub_folder_name] = sub_value

										if key != local_folder and type(self.contents["files"][local_folder][sub_folder_name]) != str:
											self.contents["files"][local_folder][sub_folder_name][sub_key] = sub_value

						if "root" in self.contents["files"][local_folder]:
							del self.contents["files"][local_folder]["root"]

						if local_folder in self.contents["files"] and sub_folder_name in self.contents["files"][local_folder] and "root" in self.contents["files"][local_folder][sub_folder_name]:
							del self.contents["files"][local_folder][sub_folder_name]["root"]

						if local_folder in self.contents["folders"][local_folder]:
							del self.contents["folders"][local_folder][local_folder]

		if self.Exist(folder) == False:
			self.Verbose(self.language_texts["this_folder_does_not_exists"], folder)

		return self.contents

	def Remove_Folders(self, dictionary, to_remove):
		for item in to_remove:
			if item in dictionary:
				if type(dictionary) == list:
					dictionary.remove(item)

				if type(dictionary) == dict:
					dictionary.pop(item)

		if type(dictionary) != list:
			for key in dictionary.copy():
				for item in to_remove:
					if type(dictionary[key]) != str:
						if item in dictionary[key]:
							dictionary[key].pop(item)

					if item == key:
						dictionary.pop(key)

		return dictionary

	def Contents(self, folder, add_sub_folders = True):
		folder = self.Sanitize(folder)
		folder_name = folder.split("/")[-1]

		if folder_name == "":
			folder_name = folder.split("/")[-2]

		contents = {
			"folder": {
				"list": [],
				"names": [],
			},
			"file": {
				"list": [],
				"names": [],
			},
			"dictionary": {},
			"size": 0,
		}

		contents["dictionary"]["root"] = folder

		for (root_folder, sub_folders, files) in os.walk(folder, topdown=True):
			root_folder = self.Sanitize(root_folder)

			# Folder name to folder names
			root_folder_name = root_folder.split("/")[-1]

			if root_folder_name == "":
				root_folder_name = root_folder.split("/")[-2]

			if folder.count("/") + 1 == root_folder.count("/"):
				# Folder path to folder list
				contents["folder"]["list"].append(self.Sanitize(root_folder))

				contents["folder"]["names"].append(root_folder_name)

			# Add files to dictionary
			i = 0
			for file in files:
				file_name = files[i].split(".")[0]

				if len(files[i].split(".")) not in [0, 1] and files[i].count(".") > 1:
					file_name = ""

					for item in files[i].split("."):
						if item != files[i].split(".")[-1]:
							file_name += item

							if item != files[i].split(".")[-2]:
								file_name += "."

				if "/" not in root_folder[-1]:
					root_folder += "/"

				files[i] = self.Sanitize(root_folder) + files[i]

				# File path to file list
				contents["file"]["list"].append(files[i])

				# File name to file names
				contents["file"]["names"].append(file_name)

				i += 1

			# Root folder on dictionary if slash count of root folder is equal to folder plus one slash or equal to folder
			# Add subfolders
			if folder.count("/") + 1 == root_folder.count("/") or folder.count("/") == root_folder.count("/"):
				if root_folder_name not in contents["dictionary"] and root_folder_name != folder_name:
					contents["dictionary"][root_folder_name] = {}

					if "root" not in contents["dictionary"][root_folder_name]:
						contents["dictionary"][root_folder_name]["root"] = self.Sanitize(root_folder)

				# Add subfiles to dictionary
				i = 0
				for file in files:
					file_name = files[i].split("/")[-1].split(".")[0]

					if len(files[i].split(".")) not in [0, 1] and files[i].split("/")[-1].count(".") > 1:
						file_name = ""

						for item in files[i].split("/")[-1].split("."):
							if item != files[i].split("/")[-1].split(".")[-1]:
								file_name += item

								if item != files[i].split("/")[-1].split(".")[-2]:
									file_name += "."

					# If file is root file, from folder, add it to the root key
					if folder.count("/") == root_folder.count("/"):
						contents["dictionary"][file_name] = files[i]

					# Add file if root_folder_name key is not string
					if root_folder_name in contents["dictionary"] and type(contents["dictionary"][root_folder_name]) != str:
						contents["dictionary"][root_folder_name][file_name] = files[i]

					if os.path.isfile(files[i]) == True:
						contents["size"] += os.stat(files[i]).st_size

					i += 1

				contents["size"] += os.stat(root_folder).st_size

			# Root folder on dictionary if slash count of root folder is equal to folder plus one slash or equal to folder
			# Add sub-sub-folders
			if folder.count("/") + 2 == root_folder.count("/"):
				root_folder = self.Sanitize(root_folder)

				root_folder_name = root_folder.split("/")[-3]
				sub_sub_folder_name = root_folder.split("/")[-2]

				# Add sub-sub-folder to dictionary
				if root_folder_name in contents["dictionary"] and sub_sub_folder_name not in contents["dictionary"][root_folder_name] and sub_sub_folder_name != folder_name:
					contents["dictionary"][root_folder_name][sub_sub_folder_name] = {}

					if "root" not in contents["dictionary"][root_folder_name][sub_sub_folder_name]:
						contents["dictionary"][root_folder_name][sub_sub_folder_name]["root"] = self.Sanitize(root_folder)

				# Add sub-sub-sub-files to dictionary
				i = 0
				for file in files:
					file_name = files[i].split("/")[-1].split(".")[0]

					if len(files[i].split(".")) not in [0, 1] and files[i].split("/")[-1].count(".") > 1:
						file_name = ""

						for item in files[i].split("/")[-1].split("."):
							if item != files[i].split("/")[-1].split(".")[-1]:
								file_name += item

								if item != files[i].split("/")[-1].split(".")[-2]:
									file_name += "."

					# Add file if root_folder_name key is not string
					if root_folder_name in contents["dictionary"] and type(contents["dictionary"][root_folder_name]) != str:
						contents["dictionary"][root_folder_name][sub_sub_folder_name][file_name] = files[i]

					if os.path.isfile(files[i]) == True:
						contents["size"] += os.stat(files[i]).st_size

					i += 1

				contents["size"] += os.stat(root_folder).st_size

		return contents