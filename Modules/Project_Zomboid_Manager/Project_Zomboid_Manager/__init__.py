# Project_Zomboid_Manager.py

from Script_Helper import *

class Project_Zomboid_Manager(object):
	def __init__(self, parameter_switches = None):
		# Verbose variable
		self.verbose = False

		self.testing_script = False

		self.parameter_switches = parameter_switches

		self.Define_Basic_Variables()
		self.Define_Lists()
		self.Define_Folders()
		self.Define_Dictionaries()

	def Define_Basic_Variables(self):
		self.option = True

		# Global Switches dictionary
		self.global_switches = {
		"write_to_file": self.option,
		"create_files": self.option,
		"create_folders": self.option,
		"move_files": self.option,
		"open_files": self.option,
		"verbose": self.verbose,
		"testing_script": self.testing_script,
		}

		if self.parameter_switches != None:
			self.global_switches = self.parameter_switches
			self.testing_script = self.global_switches["testing_script"]

		if self.global_switches["testing_script"] == True:
			print(Language_Item_Definer("Testing script: Yes", "Testando script: Sim"))

		if self.global_switches["verbose"] == True:
			print(Language_Item_Definer("Verbose on", "Verbose ligado") + ".")

		if self.global_switches["testing_script"] == True:
			self.global_switches["write_to_file"] = False
			self.global_switches["create_files"] = False

		self.dot_text = ".txt"

	def Define_Lists(self):
		self.kentucky_cities = [
		"Muldraugh, KY",
		"Riverside, KY",
		"Rosewood, KY",
		"West Point, KY",
		]

	def Define_Folders(self):
		self.stories_folder = mega_stories_folder
		self.media_multiverse_folder = self.stories_folder + "Media Multiverse/"
		self.media_multiverse_games_folder = self.media_multiverse_folder + "Games - Jogos/"
		self.project_zomboid_text_folder = self.media_multiverse_games_folder + "Project Zomboid/"
		self.database_folder = self.project_zomboid_text_folder + "Database/"

		Create_Folder(self.stories_folder, self.global_switches["create_folders"])
		Create_Folder(self.media_multiverse_folder, self.global_switches["create_folders"])
		Create_Folder(self.media_multiverse_games_folder, self.global_switches["create_folders"])
		Create_Folder(self.project_zomboid_text_folder, self.global_switches["create_folders"])
		Create_Folder(self.database_folder, self.global_switches["create_folders"])

	def Define_Dictionaries(self):
		self.kentucky_cities_folders = {}
		self.kentucky_cities_database_folders = {}
		self.character_files = {}
		self.characters_dict = {}

		for city in self.kentucky_cities:
			folder = self.project_zomboid_text_folder + city + "/"
			Create_Folder(folder, self.global_switches["create_folders"])

			database_folder = self.database_folder + city + "/"
			Create_Folder(database_folder, self.global_switches["create_folders"])

			database_characters_file = database_folder + "Characters" + self.dot_text
			Create_Text_File(database_characters_file, self.global_switches["create_files"])

			self.kentucky_cities_folders[city] = folder
			self.kentucky_cities_database_folders[city] = folder
			self.character_files[city] = database_characters_file
			self.characters_dict[city] = Create_Array_Of_File(self.character_files[city])