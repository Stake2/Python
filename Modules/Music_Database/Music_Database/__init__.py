# Music_Database.py

from Script_Helper import *

from Watch_History.Watch_History import Watch_History as Watch_History

import string

class Music_Database(object):
	def __init__(self, parameter_switches = None):
		# Verbose variable
		self.verbose = False

		self.testing_script = False

		self.parameter_switches = parameter_switches

		self.Watch_History = Watch_History()

		self.Define_Basic_Variables()
		self.Define_Lists()
		self.Define_Folders()

	def Define_Basic_Variables(self):
		self.option = True

		# Global Switches dictionary
		self.global_switches = {
		"write_to_file": self.option,
		"create_files": self.option,
		"create_folders": self.option,
		"move_files": self.option,
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
		self.dash_separator = " - "
		self.comma_separator = ", "

	def Define_Lists(self):
		self.letters = string.ascii_uppercase

	def Define_Folders(self):
		self.media_network_folder = self.Watch_History.media_network_folder
		self.media_data_folder = self.media_network_folder + "Media Data/"
		self.music_data_folder = self.media_data_folder + "Music/"
		self.music_library_folder = self.music_data_folder + "Music Library/"
		self.music_database_folder = self.music_library_folder + "Database/"
		self.mega_music_folder = mega_music_folder

		self.list_of_symbols_file = self.music_database_folder + "List of Symbols" + self.dot_text
		Create_Text_File(self.list_of_symbols_file, self.global_switches)

		self.music_letter_folders = {}
		self.database_music_letter_folders = {}

		for letter in self.letters:
			self.music_letter_folders[letter] = self.mega_music_folder + letter + "/"

			if is_a_folder(self.music_letter_folders[letter]) == True:
				self.database_music_letter_folders[letter] = self.music_database_folder + letter + "/"
				Create_Folder(self.database_music_letter_folders[letter], self.global_switches)

				self.list_of_items_file = self.database_music_letter_folders[letter] + "List of Items" + self.dot_text
				Create_Text_File(self.list_of_items_file, self.global_switches)

				self.folders = List_Folder(self.music_letter_folders[letter])

				if "Rubbish" in self.folders:
					self.folders.remove("Rubbish")

				if self.folders != []:
					self.list_ = self.folders

				# Soundtracks
				if Read_String(self.list_of_items_file) != Stringfy_Array(self.list_, add_line_break = True):
					Write_To_File(self.list_of_items_file, Stringfy_Array(self.list_, add_line_break = True), self.global_switches)	

				if self.folders != []:
					# Artists and Soundtracks
					for folder in self.list_:
						self.item_folder = self.database_music_letter_folders[letter] + folder + "/"
						Create_Folder(self.item_folder, self.global_switches)

						self.music_item_folder = self.music_letter_folders[letter] + folder + "/"

						self.item_sub_folders = sorted(List_Folder(self.music_item_folder, add_none = False))

						self.files = sorted(List_Files(self.music_item_folder, add_none = False))

						if self.files != []:
							list_ = []

							for file in self.files:
								file = file.replace(self.music_item_folder, "")
								list_.append(file)

							self.files = sorted(list_)

							if "desktop.ini" in self.files:
								self.files.remove("desktop.ini")

							self.list_of_items_file = self.item_folder + "List of Items" + self.dot_text
							Create_Text_File(self.list_of_items_file, self.global_switches)

							if Read_String(self.list_of_items_file) != Stringfy_Array(self.files, add_line_break = True):
								Write_To_File(self.list_of_items_file, Stringfy_Array(self.files, add_line_break = True), self.global_switches)

						list_ = ["Rubbish", "JSONs", "Covers", "PICs"]

						for item in list_:
							if item in self.item_sub_folders:
								self.item_sub_folders.remove(item)

						# Artists' albums and/or singles folders
						if self.item_sub_folders != []:
							self.folders_file = self.item_folder + "Folders" + self.dot_text
							Create_Text_File(self.folders_file, self.global_switches)

							if Read_String(self.folders_file) != Stringfy_Array(self.item_sub_folders, add_line_break = True):
								Write_To_File(self.folders_file, Stringfy_Array(self.item_sub_folders, add_line_break = True), self.global_switches)

							for self.item_sub_folder_name in self.item_sub_folders:
								self.item_sub_folder = self.item_folder + self.item_sub_folder_name + "/"
								Create_Folder(self.item_sub_folder, self.global_switches)

								self.item_music_sub_folder = self.music_item_folder + self.item_sub_folder_name + "/"

								self.item_sub_folder_files_file = self.item_sub_folder + "Files" + self.dot_text
								Create_Text_File(self.item_sub_folder_files_file, self.global_switches)

								self.item_sub_folder_files = List_Files(self.item_music_sub_folder, add_none = False)

								if "desktop.ini" in self.item_sub_folder_files:
									self.item_sub_folder_files.remove("desktop.ini")

								list_ = []

								for file in self.item_sub_folder_files:
									file = file.replace(self.item_music_sub_folder, "")
									list_.append(file)

								self.item_sub_folder_files = sorted(list_)

								if Read_String(self.item_sub_folder_files_file) != Stringfy_Array(self.item_sub_folder_files, add_line_break = True):
									Write_To_File(self.item_sub_folder_files_file, Stringfy_Array(self.item_sub_folder_files, add_line_break = True), self.global_switches)

		if Read_String(self.list_of_symbols_file) != Stringfy_Array(self.letters, add_line_break = True):
			Write_To_File(self.list_of_symbols_file, Stringfy_Array(self.letters, add_line_break = True), self.global_switches)