import os
import win32com.client
import shutil
from os import listdir
from os.path import isfile, join
from os import walk
import re

is_a_folder = os.path.isdir
is_a_file = os.path.isfile
Text_File_Length = os.stat

def Create_Folder(folder, global_switches = None):
	create = False

	if global_switches == None:
		create = True

	else:
		if global_switches["create_folders"] == True:
			create = True

	if create == True and is_a_folder(folder) == False:
		os.mkdir(folder)

		if global_switches != None and "verbose" in global_switches and global_switches["verbose"] == True:
			print()
			print("-----")
			print()
			print("Created folder: " + folder)

def Create_File(file, global_switches = None):
	create = False

	if global_switches == None:
		create = True

	else:
		if global_switches["create_files"] == True:
			create = True

	if create == True and is_a_file(file) == False:
		file_write = open(file, "w", encoding="utf8")
		file_write.close()

		if global_switches != None and "verbose" in global_switches and global_switches["verbose"] == True:
			print()
			print("-----")
			print()
			print("Created file: " + file)

def Move_File(old_file, new_file, global_switches = None):
	move = False

	if global_switches == None:
		move = True

	else:
		if global_switches["move_files"] == True:
			move = True

	if move == True and is_a_file(old_file) == True:
		shutil.move(old_file, new_file)

		if global_switches != None and "verbose" in global_switches and global_switches["verbose"] == True:
			print()
			print("-----")
			print()
			print("Old file:")
			print(old_file)
			print()
			print("New file:")
			print(new_file)

def Copy_File(old_file, new_file, global_switches = None):
	copy = False

	if global_switches == None:
		copy = True

	else:
		if global_switches["move_files"] == True:
			copy = True

	if copy == True and is_a_file(old_file) == True:
		shutil.copy(old_file, new_file)

		if global_switches != None and "verbose" in global_switches and global_switches["verbose"] == True:
			print()
			print("-----")
			print()
			print("Original file:")
			print(old_file)
			print()
			print("Copied file:")
			print(new_file)

def Remove_File(file, global_switches = None):
	remove = False

	if global_switches == None:
		remove = True

	else:
		if global_switches["move_files"] == True:
			remove = True

	if remove == True and is_a_file(file) == True:
		os.remove(file)

		if global_switches != None and "verbose" in global_switches and global_switches["verbose"] == True:
			print()
			print("-----")
			print()
			print("Removed file:")
			print(file)

def Remove_Folder(folder, global_switches = None):
	remove = False

	if global_switches == None:
		remove = True

	else:
		if global_switches["move_files"] == True:
			remove = True

	if remove == True and is_a_folder(folder) == True:
		try:
			# Empty
			os.rmdir(folder)

		except OSError:
			# Not empty
			shutil.rmtree(folder)

		if global_switches != None and "verbose" in global_switches and global_switches["verbose"] == True:
			print()
			print("-----")
			print()
			print("Removed folder:")
			print(folder)

def Sanitize_Folder(folder):
	folder = str(folder)

	if type(folder) == list:
		new_folders = []

		for folder_unit in folder:
			if "\\" in str(folder_unit):
				folder_unit = folder_unit.replace("\\", "/")

			if folder_unit[-1] != "/":
				folder_unit += "/"

			new_folders.append(folder_unit)

		return new_folders

	if type(folder) != list:
		if "\\" in str(folder):
			folder = str(folder).replace("\\", "/")

		if str(folder[-1]) != "/":
			folder = str(folder) + "/"

		return folder

def List_Files(folder, add_none = True, add_folder_path = True, bind_shortcuts = True):
	folder = Sanitize_Folder(str(folder))

	spare_files = []
	files_with_folder = []

	if add_none == True:
		spare_files.append(None)
		files_with_folder.append(None)

	for file in listdir(folder):
		file_with_folder = folder + file

		if is_a_file(file_with_folder) == True:
			if add_folder_path == True:
				spare_files.append(file_with_folder)

			if add_folder_path == False:
				spare_files.append(file)

			files_with_folder.append(file_with_folder)

	i = 0

	if add_none == True:
		i = 1

	while i <= len(spare_files) - 1:
		if ".lnk" in spare_files[i] and add_folder_path == True and bind_shortcuts == True:
			path = files_with_folder[i]
			shell = win32com.client.Dispatch("WScript.Shell")
			shortcut = shell.CreateShortCut(path)
			target_path = shortcut.Targetpath.replace("\\", "/")

			spare_files[i] = target_path

		i += 1

	files = spare_files

	return files

def Read_Lines(file, custom_encoding = "utf8"):
	return open(file, "r", encoding = custom_encoding).readlines()

def Map_Link(file):
	if ".lnk" in file:
		path = Read_Lines(file)[1]
		shell = win32com.client.Dispatch("WScript.Shell")
		shortcut = shell.CreateShortCut(path)
		target_path = shortcut.Targetpath.replace("\\", "/")

		return target_path

def List_Filenames(folder, add_none = True, test = False):
	folder = Sanitize_Folder(folder)

	file_names = []

	files = List_Files(folder, add_none, add_folder_path = False)

	i = 0

	if add_none == True:
		i = 1

	while i <= len(files) - 1:
		file_name, file_extension = os.path.splitext(files[i])
		file_names.append(file_name)

		i += 1

	return file_names

def List_Folder(folder, add_none = False, add_folder_path = False):
	if is_a_folder("C:/") == True:
		hard_drive_letter = "C:/"

	else:
		if is_a_folder("D:/") == True:
			hard_drive_letter = "D:/"

	folder = Sanitize_Folder(folder)

	spare_folders = []

	if add_none == True:
		spare_folders.append(None)

	for (dirpath, dirnames, filenames) in walk(folder):
		spare_folders.extend(dirnames)
		break

	if add_folder_path == True:
		second_spare_folders = []

		if add_none == True:
			second_spare_folders.append(None)

		for folder_variable in spare_folders:
			full_folder = folder + folder_variable + "/"
			second_spare_folders.append(full_folder)

		folders = second_spare_folders

	else:
		folders = spare_folders

	return folders

def List_Subfolders_And_Files(folder, extension, ignore_item = None, add_none = False):
	sub_folders, files = [], []

	if add_none == True:
		sub_folders.append(None)
		files.append(None)

	folder = Sanitize_Folder(folder)

	for file in os.scandir(folder):
		if file.is_dir():
			if ignore_item != None:
				if ignore_item not in str(file):
					sub_folders.append(file.path)

			else:
				sub_folders.append(file.path)

		if file.is_file():
			if os.path.splitext(file.name)[1].lower() in extension:
				files.append(file.path)

	for folder in list(sub_folders):
		sf, f = List_Subfolders_And_Files(folder, extension, ignore_item, add_none)
		sub_folders.extend(sf)
		files.extend(f)

	return sub_folders, files

Create_Text_File = Create_File