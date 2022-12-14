# Folder.py

from Global_Switches import Global_Switches as Global_Switches

from Language import Language as Language
from Date import Date as Date
from File import File as File

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
		self.File = File(self.global_switches)

		self.app_settings = self.Language.app_settings
		self.date = self.Date.date

		self.Define_Folders()
		self.Define_Texts()
		self.Create_Folders()

	def Define_Folders(self):
		self.module = {
			"name": self.__module__,
		}

		if "." in self.module["name"]:
			self.module["name"] = self.module["name"].split(".")[0]

		if self.module["name"] == "__main__":
			self.module["name"] = "Folder"

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
			"media": os.path.join(self.hard_drive_letter, "M??dias/"),
			"sony_vegas_files": {
				"root": os.path.join(self.hard_drive_letter, "Sony Vegas Files/"),
			},
			"xampp": {
				"root": os.path.join(self.hard_drive_letter, "XAMPP/"),
			},
		}

		if "media_folder" in self.app_settings:
			self.root_folders["media"] = self.app_settings["media_folder"]

		# Apps folders
		self.apps_folders = {
			"root": self.root_folders["apps"],
		}

		# Apps sub folders
		for folder in ["Module Files", "Modules", "Shortcuts"]:
			key = folder.lower().replace(" ", "_")

			if key == "shortcuts":
				folder = "Atalhos"

			self.apps_folders[key] = {
				"root": os.path.join(self.apps_folders["root"], folder + "/"),
			}

		self.apps_folders["modules"]["usage_modules"] = self.apps_folders["modules"]["root"] + "Usage modules.txt"

		self.apps_folders["shortcuts"]["white_shortcuts"] = os.path.join(self.apps_folders["shortcuts"]["root"], "??cone Branco/")

		# User folders
		self.user_folders = {
			"root": self.Sanitize(os.path.join(self.root_folders["users"], pathlib.Path.home().name + "/")),
		}

		# User sub folders
		for folder in ["AppData", "Downloads", "Pictures", "Videos"]:
			key = folder.lower().replace(" ", "_")

			self.user_folders[key] = {
				"root": os.path.join(self.user_folders["root"], folder + "/"),
			}

		# Downloads folders
		for folder in ["Mega", "V??deos"]:
			key = folder.lower().replace(" ", "_")

			self.user_folders["downloads"][key] = {
				"root": os.path.join(self.user_folders["downloads"]["root"], folder + "/"),
			}

		# AppData folders
		for folder in ["Local", "Roaming"]:
			key = folder.lower().replace(" ", "_")

			self.user_folders["appdata"][key] = {
				"root": os.path.join(self.user_folders["appdata"]["root"], folder + "/"),
			}

		# System32 subfolders
		self.root_folders["system32"]["drivers/etc"] = self.Sanitize(os.path.join(self.root_folders["system32"]["root"], "drivers/etc/"))

		# Sony Vegas Files subfolders
		for folder in ["Render", "Story Covers"]:
			key = folder.lower().replace(" ", "_")

			self.root_folders["sony_vegas_files"][key] = {
				"root": os.path.join(self.root_folders["sony_vegas_files"]["root"], folder + "/"),
			}

		# XAMPP folder
		self.root_folders["xampp"]["xampp-control"] = self.root_folders["xampp"]["root"] + "xampp-control.exe"

		# Mega folders
		self.mega_folders = {
			"root": self.root_folders["mega"],
		}

		# Mega subfolders
		for folder in ["Notepad", "Image", "PHP", "Obsidian's Vaults", "Stories", "Websites"]:
			key = folder.lower().replace(" ", "_").replace("'", "_")

			if key == "notepad":
				folder = "Bloco De Notas"

			self.mega_folders[key] = {
				"root": os.path.join(self.mega_folders["root"], folder + "/"),
			}

		# Mega Notepad folders
		self.mega_folders["notepad"]["effort"] = {
			"root": os.path.join(self.mega_folders["notepad"]["root"], "Dedica????o/"),
		}

		# Mega Notepad Effort folders
		for folder in ["Diary", "Diary Slim", "Food", "Networks", "Years"]:
			key = folder.lower().replace(" ", "_")

			self.mega_folders["notepad"]["effort"][key] = {
				"root": os.path.join(self.mega_folders["notepad"]["effort"]["root"], folder + "/"),
			}

		# Mega Notepad Effort Networks folders
		for folder in ["Audiovisual Media Network", "Game Network", "Productive Network"]:
			key = folder.lower().replace(" ", "_")

			self.mega_folders["notepad"]["effort"]["networks"][key] = {
				"root": os.path.join(self.mega_folders["notepad"]["effort"]["networks"]["root"], folder + "/"),
			}

		# Mega Notepad/Effort/Networks/Audiovisual Media Network folders
		for item in ["Comments", "Data", "Media Info", "Network Data", "Watch History"]:
			key = item.lower().replace(" ", "_")

			self.mega_folders["notepad"]["effort"]["networks"]["audiovisual_media_network"][key] = {
				"root": os.path.join(self.mega_folders["notepad"]["effort"]["networks"]["audiovisual_media_network"]["root"], item + "/"),
			}

		# Audiovisual Media Network/Media Info folders and files
		for item in ["Info.json"]:
			key = item.lower().replace(" ", "_").replace(".json", "")

			self.mega_folders["notepad"]["effort"]["networks"]["audiovisual_media_network"]["media_info"][key] = os.path.join(self.mega_folders["notepad"]["effort"]["networks"]["audiovisual_media_network"]["media_info"]["root"], item)

		# Audiovisual Media Network/Network Data files
		for item in ["Media Types.json"]:
			key = item.lower().replace(" ", "_").replace(".json", "")

			self.mega_folders["notepad"]["effort"]["networks"]["audiovisual_media_network"]["network_data"][key] = os.path.join(self.mega_folders["notepad"]["effort"]["networks"]["audiovisual_media_network"]["network_data"]["root"], item)

		# Audiovisual Media Network/Watch History folders
		for item in ["Movies"]:
			key = item.lower().replace(" ", "_")

			self.mega_folders["notepad"]["effort"]["networks"]["audiovisual_media_network"]["watch_history"][key] = {
				"root": os.path.join(self.mega_folders["notepad"]["effort"]["networks"]["audiovisual_media_network"]["watch_history"]["root"], item + "/"),
			}

		# Audiovisual Media Network/Watch History year folders
		for item in [self.date["year"]]:
			key = str(item).lower().replace(" ", "_")

			self.mega_folders["notepad"]["effort"]["networks"]["audiovisual_media_network"]["watch_history"][key] = {
				"root": os.path.join(self.mega_folders["notepad"]["effort"]["networks"]["audiovisual_media_network"]["watch_history"]["root"], str(item) + "/"),
			}

			for item in ["Per Media Type"]:
				self.mega_folders["notepad"]["effort"]["networks"]["audiovisual_media_network"]["watch_history"][key][item] = {
					"root": os.path.join(self.mega_folders["notepad"]["effort"]["networks"]["audiovisual_media_network"]["watch_history"][key]["root"], str(item) + "/"),
				}

			# Episodes.json file
			self.mega_folders["notepad"]["effort"]["networks"]["audiovisual_media_network"]["watch_history"][key]["episodes"] = self.mega_folders["notepad"]["effort"]["networks"]["audiovisual_media_network"]["watch_history"][key]["root"] + "Episodes.json"

		# Mega Notepad/Effort/Networks/Productive Network folders
		for item in ["Data", "Network Data", "Task History"]:
			key = item.lower().replace(" ", "_")

			self.mega_folders["notepad"]["effort"]["networks"]["productive_network"][key] = {
				"root": os.path.join(self.mega_folders["notepad"]["effort"]["networks"]["productive_network"]["root"], item + "/"),
			}

		# Networks/Productive Network/Task History folders
		for item in [self.date["year"]]:
			key = str(item).lower().replace(" ", "_")

			self.mega_folders["notepad"]["effort"]["networks"]["productive_network"]["task_history"][key] = {
				"root": os.path.join(self.mega_folders["notepad"]["effort"]["networks"]["productive_network"]["task_history"]["root"], str(item) + "/"),
			}

			for item in ["Per Task Type"]:
				self.mega_folders["notepad"]["effort"]["networks"]["productive_network"]["task_history"][key][item] = {
					"root": os.path.join(self.mega_folders["notepad"]["effort"]["networks"]["productive_network"]["task_history"][key]["root"], str(item) + "/"),
				}

			# Tasks.json file
			self.mega_folders["notepad"]["effort"]["networks"]["productive_network"]["task_history"][key]["tasks"] = self.mega_folders["notepad"]["effort"]["networks"]["productive_network"]["task_history"][key]["root"] + "Tasks.json"

			# Task list.txt file
			self.mega_folders["notepad"]["effort"]["networks"]["productive_network"]["task_history"][key]["task_list"] = self.mega_folders["notepad"]["effort"]["networks"]["productive_network"]["task_history"][key]["root"] + "Task list.txt"

		# Years folders
		for item in range(2021, self.date["year"] + 1):
			key = str(item).lower().replace(" ", "_")

			self.mega_folders["notepad"]["effort"]["years"][key] = {
				"root": os.path.join(self.mega_folders["notepad"]["effort"]["years"]["root"], str(item) + "/"),
			}

			# Experienced Media folder
			self.mega_folders["notepad"]["effort"]["years"][key]["experienced_media"] = {
				"root": os.path.join(self.mega_folders["notepad"]["effort"]["years"][key]["root"], "Experienced Media/"),
			}

			if key == str(self.date["year"]):
				self.mega_folders["notepad"]["effort"]["years"]["current_year"] = self.mega_folders["notepad"]["effort"]["years"][key]

		# Notepad folders
		self.notepad_folders = {}

		for key in self.mega_folders["notepad"]:
			self.notepad_folders[key] = self.mega_folders["notepad"][key]

		for key in self.mega_folders["notepad"]["effort"]:
			self.notepad_folders[key] = self.mega_folders["notepad"]["effort"][key]

		# Temporary set PHP folder to Remake
		self.mega_folders["php"] = {
			"root": os.path.join(self.mega_folders["php"]["root"], "Remake/"),
		}

		# Mega PHP folders
		for item in ["JSON"]:
			key = item.lower().replace(" ", "_")

			self.mega_folders["php"][key] = {
				"root": os.path.join(self.mega_folders["php"]["root"], item + "/"),
			}

		# Mega PHP JSON files
		for item in ["Colors", "URL", "Websites"]:
			key = item.lower().replace(" ", "_")

			self.mega_folders["php"]["json"][key] = os.path.join(self.mega_folders["php"]["json"]["root"], item + ".json")

		# Mega Obsidian's Vaults folders
		for item in ["Creativity"]:
			key = item.lower().replace(" ", "_")

			self.mega_folders["obsidian_s_vaults"][key] = {
				"root": os.path.join(self.mega_folders["obsidian_s_vaults"]["root"], item + "/"),
			}

		# Mega Obsidian's Vaults/Creativity folders
		for item in ["Literature"]:
			key = item.lower().replace(" ", "_")

			self.mega_folders["obsidian_s_vaults"]["creativity"][key] = {
				"root": os.path.join(self.mega_folders["obsidian_s_vaults"]["creativity"]["root"], item + "/"),
			}

		# Mega Obsidian's Vaults/Creativity/Literature folders
		for item in ["Stories"]:
			key = item.lower().replace(" ", "_")

			self.mega_folders["obsidian_s_vaults"]["creativity"]["literature"][key] = {
				"root": os.path.join(self.mega_folders["obsidian_s_vaults"]["creativity"]["literature"]["root"], item + "/"),
			}

		# Mega Websites folders and files
		for item in ["Website.json", "Images"]:
			key = item.lower().replace(" ", "_").replace(".json", "")

			if "." in item:
				self.mega_folders["websites"][key] = os.path.join(self.mega_folders["websites"]["root"], item)

			else:
				self.mega_folders["websites"][key] = {
					"root": os.path.join(self.mega_folders["websites"]["root"], item + "/"),
				}

		self.mega_folders["websites"]["images"]["story_covers"] = self.mega_folders["websites"]["images"]["root"] + "Story Covers/"

		# Get website subdomain
		self.website = self.Language.JSON_To_Python(self.mega_folders["websites"]["website"])

		# Create links dictionary with Stake2 Website link
		self.links = {
			"Stake2 Website": "https://" + self.website["subdomain"] + "." + self.website["netlify"] + "/"
		}

		# Define Folder related variables (texts file)
		self.module_text_files_folder = self.apps_folders["module_files"]["root"] + self.module["name"] + "/"

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

	def Exist(self, path):
		path = self.Sanitize(path)

		if os.path.isdir(path) == True:
			return True

		if os.path.isdir(path) == False:
			return False

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

	def Create_Folders(self, folders = None, depth = 0):
		if folders == None:
			folders = self.folders

		for value in folders.values():
			if type(value) != dict:
				if os.path.isfile(value) == False and "." not in value:
					self.Create(value)

				if os.path.isfile(value) == False and "." in value:
					self.File.Create(value)

			if type(value) == dict:
				found = self.Create_Folders(value, depth = depth + 1)

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

	def Contents(self, folder, add_sub_folders = True, lower_key = False):
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

			# Add files to list and names lists
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
				if lower_key == True:
					root_folder_name = root_folder_name.lower().replace(" ", "_")

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

					if lower_key == True:
						file_name = file_name.lower().replace(" ", "_").replace(".", "")

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

			# Root folder on dictionary if slash count of root folder is equal to folder plus two slash or equal to folder
			# Add sub-sub-folders
			if folder.count("/") + 2 == root_folder.count("/"):
				root_folder = self.Sanitize(root_folder)

				root_folder_name = root_folder.split("/")[-3]
				sub_sub_folder_name = root_folder.split("/")[-2]

				if lower_key == True:
					root_folder_name = root_folder_name.lower().replace(" ", "_")
					sub_sub_folder_name = sub_sub_folder_name.lower().replace(" ", "_")

				# Add sub-sub-folder to dictionary
				if root_folder_name in contents["dictionary"] and sub_sub_folder_name not in contents["dictionary"][root_folder_name] and sub_sub_folder_name != folder_name and type(contents["dictionary"][root_folder_name]) != str:
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

					if lower_key == True:
						file_name = file_name.lower().replace(" ", "_").replace(".", "")

					# Add file if root_folder_name key is not string
					if type(contents["dictionary"]) != str and type(contents["dictionary"][root_folder_name]) != str and type(contents["dictionary"][root_folder_name][sub_sub_folder_name]) != str:
						contents["dictionary"][root_folder_name][sub_sub_folder_name][file_name] = files[i]

					if os.path.isfile(files[i]) == True:
						contents["size"] += os.stat(files[i]).st_size

					i += 1

				contents["size"] += os.stat(root_folder).st_size

			# Root folder on dictionary if slash count of root folder is equal to folder plus three slash or equal to folder
			# Add sub-sub-sub-folders
			if folder.count("/") + 3 == root_folder.count("/"):
				root_folder = self.Sanitize(root_folder)

				root_folder_name = root_folder.split("/")[-4]
				sub_sub_folder_name = root_folder.split("/")[-3]
				sub_sub_sub_folder_name = root_folder.split("/")[-2]

				if lower_key == True:
					root_folder_name = root_folder_name.lower().replace(" ", "_")
					sub_sub_folder_name = sub_sub_folder_name.lower().replace(" ", "_")
					sub_sub_sub_folder_name = sub_sub_sub_folder_name.lower().replace(" ", "_")

				# Add sub-sub-sub-folder to dictionary
				if root_folder_name in contents["dictionary"] and sub_sub_folder_name in contents["dictionary"][root_folder_name] and type(contents["dictionary"][root_folder_name][sub_sub_folder_name]) != str:
					contents["dictionary"][root_folder_name][sub_sub_folder_name][sub_sub_sub_folder_name] = {}

					if "root" not in contents["dictionary"][root_folder_name][sub_sub_folder_name][sub_sub_sub_folder_name]:
						contents["dictionary"][root_folder_name][sub_sub_folder_name][sub_sub_sub_folder_name]["root"] = self.Sanitize(root_folder)

				# Add sub-sub-sub-sub-files to dictionary
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

					if lower_key == True:
						file_name = file_name.lower().replace(" ", "_").replace(".", "")

					# Add file if root_folder_name key is not string
					if root_folder_name in contents["dictionary"] and sub_sub_folder_name in contents["dictionary"][root_folder_name] and \
					sub_sub_sub_folder_name in contents["dictionary"][root_folder_name][sub_sub_folder_name] and \
					type(contents["dictionary"][root_folder_name][sub_sub_folder_name]) != str and type(contents["dictionary"][root_folder_name][sub_sub_folder_name][sub_sub_sub_folder_name]) != str:
						contents["dictionary"][root_folder_name][sub_sub_folder_name][sub_sub_sub_folder_name][file_name] = files[i]

					if os.path.isfile(files[i]) == True:
						contents["size"] += os.stat(files[i]).st_size

					i += 1

				contents["size"] += os.stat(root_folder).st_size

			# Root folder on dictionary if slash count of root folder is equal to folder plus four slash or equal to folder
			# Add sub-sub-sub-sub-folders
			if folder.count("/") + 4 == root_folder.count("/"):
				root_folder = self.Sanitize(root_folder)

				root_folder_name = root_folder.split("/")[-5]
				sub_sub_folder_name = root_folder.split("/")[-4]
				sub_sub_sub_folder_name = root_folder.split("/")[-3]
				sub_sub_sub_sub_folder_name = root_folder.split("/")[-2]

				if lower_key == True:
					root_folder_name = root_folder_name.lower().replace(" ", "_")
					sub_sub_folder_name = sub_sub_folder_name.lower().replace(" ", "_")
					sub_sub_sub_folder_name = sub_sub_sub_folder_name.lower().replace(" ", "_")
					sub_sub_sub_sub_folder_name = sub_sub_sub_sub_folder_name.lower().replace(" ", "_")

				# Add sub-sub-sub-folder to dictionary
				if root_folder_name in contents["dictionary"] and sub_sub_folder_name in contents["dictionary"][root_folder_name] and sub_sub_sub_folder_name in contents["dictionary"][root_folder_name][sub_sub_folder_name]:
					contents["dictionary"][root_folder_name][sub_sub_folder_name][sub_sub_sub_folder_name][sub_sub_sub_sub_folder_name] = {}

					if "root" not in contents["dictionary"][root_folder_name][sub_sub_folder_name][sub_sub_sub_folder_name][sub_sub_sub_sub_folder_name]:
						contents["dictionary"][root_folder_name][sub_sub_folder_name][sub_sub_sub_folder_name][sub_sub_sub_sub_folder_name]["root"] = self.Sanitize(root_folder)

				# Add sub-sub-sub-sub-files to dictionary
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

					if lower_key == True:
						file_name = file_name.lower().replace(" ", "_").replace(".", "")

					# Add file if root_folder_name key is not string
					if root_folder_name in contents["dictionary"] and sub_sub_folder_name in contents["dictionary"][root_folder_name] and sub_sub_sub_folder_name in contents["dictionary"][root_folder_name][sub_sub_folder_name]:
						contents["dictionary"][root_folder_name][sub_sub_folder_name][sub_sub_sub_folder_name][sub_sub_sub_sub_folder_name][file_name] = files[i]

					if os.path.isfile(files[i]) == True:
						contents["size"] += os.stat(files[i]).st_size

					i += 1

				contents["size"] += os.stat(root_folder).st_size

		return contents