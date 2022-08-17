# Fill_Diary_Slim_Database_Files.py

from Script_Helper import *

from Diary_Slim.Diary_Slim import Diary_Slim as Diary_Slim

local_script_name = "Fill_Diary_Slim_Database_Files.py"

class Fill_Diary_Slim_Database_Files(Diary_Slim):
	def __init__(self):
		super().__init__()

		self.diary_slim_file_names = {}
		self.diary_slim_year_sub_folders = {}
		self.diary_slim_year_sub_folders_no_folder_path = {}
		self.diary_slim_month_files = {}

		self.Get_Folders()
		self.Get_Files()
		self.Write_To_Files()

		if self.global_switches["testing_script"] == True:
			self.Open_Diary_Slims()

	def Get_Folders(self):
		for folder in self.diary_slim_year_folders:
			year = folder

			folder = self.diary_slim_year_folders[folder]

			self.diary_slim_year_sub_folders[year] = List_Folder(folder, add_folder_path = True)
			self.diary_slim_year_sub_folders_no_folder_path[year] = List_Folder(folder, add_folder_path = False)

	def Get_Files(self):
		for folder in self.diary_slim_year_folders:
			year = folder

			folders = self.diary_slim_year_sub_folders[year]

			array = []

			i = 0
			while i <= len(folders) - 1:
				month = self.diary_slim_year_sub_folders_no_folder_path[year][i] 

				array.extend(List_Files(folders[i], add_none = False, add_folder_path = False))

				self.diary_slim_month_files[month] = List_Files(folders[i], add_none = False, add_folder_path = False)

				i += 1

			self.diary_slim_file_names[year] = array

		for folder in self.diary_slim_year_folders:
			year = folder

			i = 0
			while i <= len(self.diary_slim_file_names[year]) - 1:
				self.diary_slim_file_names[year][i] = self.diary_slim_file_names[year][i].replace(".txt", "")

				i += 1

			i = 0
			while i <= len(self.diary_slim_year_sub_folders_no_folder_path[year]) - 1:
				month = self.diary_slim_year_sub_folders_no_folder_path[year][i]

				c = 0
				while c <= len(self.diary_slim_month_files[month]) - 1:
					self.diary_slim_month_files[month][c] = self.diary_slim_month_files[month][c].replace(".txt", "")

					c += 1

				self.diary_slim_database_month_folder = self.diary_slim_database_year_folders[year] + month + "/"
				Create_Folder(self.diary_slim_database_month_folder, self.global_switches["create_folders"])

				self.diary_slim_database_month_file_names_file = self.diary_slim_database_month_folder + "File Names" + self.dot_text
				Create_Text_File(self.diary_slim_database_month_file_names_file, self.global_switches["create_files"])

				i += 1

	def Write_To_Files(self):
		for folder in self.diary_slim_year_folders:
			year = folder

			self.database_folder = self.diary_slim_database_year_folders[year]
			Create_Folder(self.database_folder)
			self.file_name_file = self.database_folder + "Slim File Names" + self.dot_text

			text_to_write = Stringfy_Array(self.diary_slim_file_names[year], add_line_break = True)

			if Read_String(self.file_name_file) != text_to_write:
				Write_To_File(self.file_name_file, text_to_write, self.global_switches)

		for folder in self.diary_slim_year_folders:
			year = folder

			i = 0
			while i <= len(self.diary_slim_year_sub_folders_no_folder_path[year]) - 1:
				month = self.diary_slim_year_sub_folders_no_folder_path[year][i]
				month_folder = self.diary_slim_database_year_folders[year] + month + "/"
				month_file = month_folder + "File Names" + self.dot_text
				month_files_text = Stringfy_Array(self.diary_slim_month_files[month], add_line_break = True)

				text_to_write = month_files_text

				if Read_String(month_file) != text_to_write:
					Write_To_File(month_file, text_to_write, self.global_switches)

				i += 1

		self.all_file_names = []
		self.all_year_folder_names = ""
		self.all_month_folder_names = ""

		for folder in self.diary_slim_year_folders:
			year = folder

			i = 0
			while i <= len(self.diary_slim_file_names[year]) - 1:
				split = self.diary_slim_file_names[year][i].split(", ")[1].split("-")

				local_year = split[2] + "/"
				month = split[1] + " - " + month_names_ptbr[int(split[1])] + "/"

				self.all_year_folder_names += local_year
				self.all_month_folder_names += month

				if i <= len(self.diary_slim_file_names[year]) - 1:
					self.all_year_folder_names += "\n"
					self.all_month_folder_names += "\n"

				if self.global_switches["verbose"] == True:
					print()
					print(month)
					print(year)

				i += 1

			self.all_file_names.extend(self.diary_slim_file_names[year])

		self.all_year_folder_names = self.all_year_folder_names[:-1]
		self.all_month_folder_names = self.all_month_folder_names[:-1]

		self.file_name_file = self.all_file_names_file

		text_to_write = Stringfy_Array(self.all_file_names, add_line_break = True)

		if Read_String(self.file_name_file) != text_to_write:
			Write_To_File(self.file_name_file, text_to_write, self.global_switches)

		text_to_write = self.all_year_folder_names

		if Read_String(self.all_year_folders_file) != text_to_write:
			Write_To_File(self.all_year_folders_file, text_to_write, self.global_switches)

		text_to_write = self.all_month_folder_names

		if Read_String(self.all_month_folders_file) != text_to_write:
			Write_To_File(self.all_month_folders_file, text_to_write, self.global_switches)

	def Open_Diary_Slims(self):
		print()

		for diary_slim in self.all_file_names:
			diary_slim_backup = diary_slim

			month = diary_slim.split("-")[-2]
			year = diary_slim.split("-")[-1]

			month_name = month_names_ptbr[int(month)]

			year_folder = self.diary_slim_year_folders[year]

			month_folder = year_folder + month + " - " + month_name + "/"

			diary_slim = month_folder + diary_slim + self.dot_text

			print()
			print(Language_Item_Definer("Opening this Diary Slim", "Abrindo esse Diário Slim") + ": ")
			print(diary_slim)

			Open_Text_File(diary_slim)

			input(Language_Item_Definer("Next", "Próximo") + ": ")