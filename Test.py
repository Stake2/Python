import pyperclip
import pyautogui
import webbrowser
import subprocess
import random
import re
from beautifultable import BeautifulTable
from time import sleep
from Script_Helper import *
import datetime
from datetime import timedelta, datetime
from nptime import nptime
from os.path import expanduser
from zipfile import ZipFile

global_write_to_file = True

file = scripts_folder + "Test.py"
#execfile(file)2

script_name = "Test.py"

now = time.strftime("%H:%M %d/%m/%Y")

sides_array = [
None,
"Left",
"Right",
]

left = sides_array[1]
right = sides_array[2]

copy = pyperclip.copy

def Format_Website_Link_Parameters(website_name, make_source_links_option):
	global website_type
	global source_website_link_parameters_string_formatted
	global source_website_links_string

	source_website_link_parameters_string = "view-source:localhost/index.php?no-redirect=true&website_language={}&website={}&website_type={}"

	main_webiste_link = "https://diario.netlify.app/"
	online_website_link_parameters_string = main_webiste_link + "{}/{}/?no-redirect=true"

	site_websites_array = [
	'pocb',
	'diario',
	'mlp',
	'watch%20👁',
	'music',
	'games',
	'fa',
	'terrariatalk',
	'tasks',
	'thingsido',
	'years',
	'2018',
	'2019',
	'2020',
	'nw',
	'mf',
	'wt',
	'stake2',
	]

	story_websites_array = [
	'stories',
	'izaquemultiverse',
	'pequenata',
	'spaceliving',
	'nazzevo',
	'desertisland',
	'lonelystories',
	'yourstrulyizaque',
	]

	if make_source_links_option == True:
		if website_name in site_websites_array:
			website_type = "site"

		if website_name in story_websites_array:
			website_type = "story"

		source_website_links_string = ""

		i = 1
		for language in languages_with_global:
			if language != None:
				source_website_link_parameters_string_formatted = source_website_link_parameters_string.format(language, website_name, website_type)

				if i == len(languages_with_global):
					source_website_links_string += source_website_link_parameters_string_formatted

				if i != len(languages_with_global):
					source_website_links_string += source_website_link_parameters_string_formatted + "\n"

			i += 1

	if make_source_links_option == False or make_source_links_option == None:
		online_website_links_string = ""

		if website_name == "desertisland":
			website_name = "desert_island"

		global_website_link = main_webiste_link + "{}".format(website_name) + "/?no-redirect=true"

		online_website_links_string += global_website_link + "\n"

		webbrowser.open(global_website_link)

		i = 1
		for language in languages_with_hyphen:
			if language != None:
				online_website_link_parameters_string_formatted = online_website_link_parameters_string.format(website_name, language)

				if i == len(languages_with_hyphen):
					online_website_links_string += online_website_link_parameters_string_formatted

				if i != len(languages_with_hyphen):
					online_website_links_string += online_website_link_parameters_string_formatted + "\n"

				webbrowser.open(online_website_link_parameters_string_formatted)

			i += 1

	print()

	if make_source_links_option == True:
		print("The view-source website links are these ones: ")
		print(source_website_links_string)

		source_website_links_array = source_website_links_string.split("\n")

		for link in source_website_links_array:
			input("Press any key to copy link: ")
			pyperclip.copy(link)

	if make_source_links_option == False or make_source_links_option == None:
		print("The online website links are these ones: ")
		print(online_website_links_string)
		pyperclip.copy(online_website_links_string)

def Make_Numbered_List():
	finish_string = "f"

	print("\\")

	i = 1
	text_input = str(input(str(i) + ": "))
	text_input = str(i) + ": " + text_input

	i += 1
	type_more = str(input(str(i) + ": "))
	type_more = str(i) + ": " + type_more

	typing_more = False
	finished_adding_texts = False

	if type_more != finish_string:
		typing_more = True

		text_input = text_input + "\n" + type_more

		if text_input == finish_string:
			typing_more = False
			finished_adding_texts = True

		i += 1
		while typing_more == True:
			type_more = str(input(str(i) + ": "))

			if type_more == finish_string:
				typing_more = False

			else:
				text_input = text_input + "\n" + str(i) + ": " + type_more

			i += 1

		final_text = text_input

	if type_more == finish_string and typing_more == False and finished_adding_texts == False:
		final_text = text_input

	pyperclip.copy(final_text)

	print("/")

def Change_Wattpad_Inbox_HTML_Filename():
	file_path = str(input("Type the file path: "))
	file_path = file_path.replace("\\", "/")
	file_path = file_path + "/"

	old_filename = str(input("Type the filename: "))

	old_file = file_path + old_filename

	first_replace = "Messages between you and "
	second_replace = " - Wattpad"

	new_filename = old_filename.replace(first_replace, "")
	new_filename = new_filename.replace(second_replace, " Inbox")

	new_file = file_path + new_filename

	Move_File(old_file, new_file)

	print()
	print("This file: \n" + old_filename + "\n\n" + "Has been renamed to: \n" + new_filename)

def Create_A_Lot_Of_Text_Files_From_List():
	folder_to_create_files = str(input("Press [Enter] to paste the location of the folder where you want to create text files: "))

	clipboard_data = Get_Clipboard()

	folder_to_create_files = clipboard_data + "\\"

	number_of_text_files = input("Press [Enter] to paste the list of file names that you want to create: ")

	clipboard_data = Get_Clipboard()

	list_of_file_names_to_create = clipboard_data.split("\r\n")

	print()
	print("The number of files to create is: " + str(len(list_of_file_names_to_create)))
	print()

	i = 1
	for file_name in list_of_file_names_to_create:
		file_name = file_name.replace("MLP Natal/", "My Little Pony Christmas - ")
		file_name = str(i) + ". " + file_name.replace("y:", "y;")

		while len(file_name) > 159:
			file_name = file_name[:-1]

		text_file_to_create = folder_to_create_files + file_name + ".txt"
		text_file_to_create = text_file_to_create.replace("y:", "y;")

		Create_Text_File(text_file_to_create)

		print("File number: " + str(i))
		print("This file was created: " + "\n" + text_file_to_create + "\n")

		i += 1

def Create_Experienced_Medias_Song():
	global remix_artist_name

	verbose = False
	write_to_file_switch = True

	type_the_text = Language_Item_Definer("Type the", "Digite o")

	soundcloud_playlist_id = "stake2/sets/dubstep-2021"
	youtube_playlist_id = "PLh4DEvPQ2wKM2Jqz95-o6u6pRtLyfdVp9"

	experienced_medias_song_number_file_enus = notepad_folder_year_experienced_music_enus + "Song Number.txt"

	Create_Text_File(experienced_medias_song_number_file_enus)

	song_number = str(int(Read_Lines(experienced_medias_song_number_file_enus)[0]) + 1)

	song_parameter_names = [
	None,
	Language_Item_Definer("song name", "nome da música"),
	Language_Item_Definer("artist links", "links do(s) artista(s)"),
	Language_Item_Definer("account name", "nome da conta"),
	Language_Item_Definer("account link", "link da conta"),
	Language_Item_Definer("song link", "link da música"),
	]

	i = 1

	song_name_key = song_parameter_names[i]
	i += 1

	artist_links_key = song_parameter_names[i]
	i += 1

	account_name_key = song_parameter_names[i]
	i += 1

	account_link_key = song_parameter_names[i]
	i += 1

	song_link_key = song_parameter_names[i]
	i += 1

	song_parameters = {"None": None}

	for parameter in song_parameter_names:
		if parameter != None:
			song_parameters[parameter] = Select_Choice(type_the_text + " " + parameter, first_space = False)

			if verbose == True:
				print(song_parameters[parameter])

	song_name = song_parameters[song_name_key]
	artist_links = song_parameters[artist_links_key]
	account_name = song_parameters[account_name_key]
	account_link = song_parameters[account_link_key]
	song_link = song_parameters[song_link_key]
	backup_song_link = song_parameters[song_link_key]

	if ", " in song_link:
		backup_song_link = song_link.split(", ")

	if type(backup_song_link) == list:
		soundcloud_link = backup_song_link[0]
		youtube_link = backup_song_link[1]

		song_link = soundcloud_link + "\n" + youtube_link

		has_soundcloud_artist = True

	if type(backup_song_link) == str:
		has_soundcloud_artist = False

	artist_links = artist_links.splitlines()
	artist_links_2 = []
	artist_links_3 = []

	texts_to_replace = [
	"» Follow ",
	"● Follow ",
	"Follow ",
	"\nFollow ",
	"» Connect with ",
	"\r\n---\r\n",
	"---",
	" 🎧",
	" 🎤",
	" 💿",
	" ►",
	"▼ ",
	" 📢",
	"\u200b\u200b",
	]

	i = 0
	for line in artist_links:
		c = 0
		while c <= len(texts_to_replace) - 1:
			line = line.replace(texts_to_replace[c], "")

			c += 1

		artist_links_2.append(line)

		i += 1

	for line in artist_links_2:
		line = line.replace(" | ", ": ")
		line = line.replace(" →", ":")

		artist_links_3.append(line)

	artist_links = ""

	for line in artist_links_3:
		artist_links += line + "\n"

	has_remix_artist = False

	if "(VIP)" not in song_name and "(vip)" not in song_name:
		try:
			remix_artist_name = "(" + re.split("[(]", song_name)[1]

			if "ft. " in remix_artist_name:
				remix_artist_name.replace("ft. ", "")

			has_remix_artist = True

		except IndexError:
			has_remix_artist = False	

	if has_remix_artist == True:
		remix_artist_name = remix_artist_name.replace("(", "")
		remix_artist_name = remix_artist_name.replace(")", "")
		remix_artist_name = remix_artist_name.replace(" Remix", "")

	artist_name = song_name.split(" - ")[0]

	if has_soundcloud_artist == True:
		youtube_playlist_link = youtube_link + "&list=" + youtube_playlist_id + "&index=" + song_number
		soundcloud_playlist_link = soundcloud_link + "?in=" + soundcloud_playlist_id

		playlist_link = soundcloud_playlist_link + "\n" + youtube_playlist_link

	if has_soundcloud_artist == False:
		youtube_link = song_link

		youtube_playlist_link = youtube_link + "&list=" + youtube_playlist_id + "&index=" + song_number
		playlist_link = youtube_playlist_link

	if verbose == True:
		print(playlist_link)

	text_array_enus = [
	None,
	"Name",
	"Artist",
	"Account",
	"Link",
	"Playlist",
	]

	text_array_ptbr = [
	None,
	"Nome",
	"Artista",
	"Conta",
	"Link da Playlist",
	"Playlist",
	]

	song_file_enus = notepad_folder_year_experienced_music_enus + str(song_number) + ". " + song_name + ".txt"
	song_file_ptbr = notepad_folder_year_experienced_music_ptbr + str(song_number) + ". " + song_name + ".txt"

	Create_Text_File(song_file_enus)
	Create_Text_File(song_file_ptbr)

	text_arrays = {
	full_language_enus: text_array_enus,
	full_language_ptbr: text_array_ptbr,
	}

	song_files = {
	full_language_enus: song_file_enus,
	full_language_ptbr: song_file_ptbr,
	}

	for language_number in language_numbers:
		if language_number != None:
			text_to_write = ""

			full_language = full_languages[language_number]

			text_array = text_arrays[full_language]
			song_file = song_files[full_language]

			#artist_name_text = Language_Item_Definer("Artist", "Artista", full_language)
			song_link_text = Language_Item_Definer("Song Link", "Link da Música", full_language)
			playlist_link_text = Language_Item_Definer("Playlist Link", "Link da Playlist", full_language)

			text_to_write += text_array[1] + ":\n"
			text_to_write += song_name + "\n"
			text_to_write += "\n"
			text_to_write += text_array[2] + ":\n"
			text_to_write += artist_name + "\n"

			if has_remix_artist == True:
				text_to_write += remix_artist_name + "\n\n"

			text_to_write += artist_links + "\n"
			text_to_write += text_array[3] + ":\n"
			text_to_write += account_name + "\n"
			text_to_write += account_link + "\n"
			text_to_write += "\n"
			text_to_write += song_link_text + ":\n"
			text_to_write += song_link + "\n"
			text_to_write += "\n"
			text_to_write += playlist_link_text + ":" + "\n"
			text_to_write += playlist_link

			if verbose == True:
				print(text_to_write)

			Write_To_File(song_file, text_to_write, write_to_file_switch)

	Write_To_File(experienced_medias_song_number_file_enus, str(song_number), write_to_file_switch)

	# To-do: Replace the "text_to_write += " with a string format using the right text of the language

def Difference_Between_Two_Times(old_time):
	from datetime import datetime
	from dateutil import relativedelta

	old_time = old_time.split(", ")
	hour = int(old_time[0])
	minute = int(old_time[1])

	day = int(time.strftime("%d"))
	month = int(time.strftime("%m"))
	year = int(time.strftime("%Y"))

	##Aug 7 1989 8:10 pm
	date_1 = datetime(year, month, day, hour, minute)

	##Dec 5 1990 5:20 am
	date_2 = datetime.now()

	#This will find the difference between the two dates
	difference = relativedelta.relativedelta(date_2, date_1)

	years = difference.years
	months = difference.months
	days = difference.days
	hours = difference.hours
	minutes = difference.minutes

	if years == 0 and months == 0 and days == 0:
		if minutes > 1:
			minute_text = "minutos"

		if minutes <= 1:
			minute_text = "minuto"

		if hours > 1:
			hour_text = "horas"

		if hours <= 1:
			hour_text = "hora"

		if hours == 0 and minutes != 0:
			print("A Diferença é de {} ".format(minutes) + minute_text + ".")

		if hours != 0 and minutes != 0:
			print(str("A Diferença é de {} {}".format(hours, hour_text)) + str(", e {} ".format(minutes)) + minute_text + ".")
																    
		if hours != 0 and minutes == 0:                             
			print(str("A Diferença é de {} {}".format(hours, hour_text)) + str(", e {} ".format(minutes)) + minute_text + ".")

def Make_Book_Text():
	book_number = str(input("Type the book number: "))

	book_text = "**Livro " + book_number + ": \n\n-**\n\n{}"

	input("Press any key to paste story text: ")

	story_text = Get_Clipboard()

	book_text = book_text.format(story_text)

	pyperclip.copy(book_text)

def Remove_Number():
	number = int(input("Type the number that you have: "))
	number_to_reach = 0

	while number >= number_to_reach:
		number_to_remove = int(input("\nNumber to remove: "))

		number = number - number_to_remove
		print(str(number))

def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : 'bytes', 1: 'kilobytes', 2: 'megabytes', 3: 'gigabytes', 4: 'terabytes'}

    while size > power:
        size /= power
        n += 1

    return size, power_labels[n]

def File_Size():
	url = Select_Choice("Type the URL")

	import urllib
	from urllib.request import urlopen as urlopen

	f = urlopen(url)
	size = f.headers["Content-Length"]
	size = format_bytes(int(size))

	size_text = size[1]
	size = size[0]

	if size >= 2:
		plural_text = "s"

	else:
		plural_text = ""

	if size_text == "bytes":
		size_text = "byte" + plural_text

	if size_text == "kilobytes":
		size_text = "KB" + plural_text

	if size_text == "megabytes":
		size_text = "MB" + plural_text

	if size_text == "gigabytes":
		size_text = "GB" + plural_text

	if size_text == "terabytes":
		size_text = "TB" + plural_text

	size = round(size)
	size_with_power_label = str(size) + " " + size_text

	print()
	print("Size: " + size_with_power_label)

	return str(size) + " " + size_text

def Make_Table():
	table_column_headers = ["Story Name", "Creation Date", "Chapter Number", "Synopsis", "Template"]

	column_header_len = len(table_column_headers)

	# To-Do: Read Story files to get story info and make the info as rows

	rows = [["anaasdasds", "sadasd", "sdadsa", "sadadasasd", "sadasaasd"],
	["hello", "Hi", "Hello22", "hello 3", "hello 4"]]

	row_len = len(rows)

	table = BeautifulTable()
	table.columns.header = table_column_headers

	for row in rows:
		table.rows.append(row)

	table = str(table)

	table_lines = table.splitlines()

	full_table = ""
	full_table += table_lines[1] + "\n"
	full_table += table_lines[2].replace("+", "|") + "\n"

	i = 3
	c = 0
	while c <= row_len - 1:
		if c != row_len - 1:
			full_table += table_lines[i] + "\n"

		if c == row_len - 1:
			full_table += table_lines[i]

		c += 1
		i += 2

	print(full_table)
	copy(full_table)

def Check_File_Type():
	folder = Select_Choice("Type the folder or get it from the clipboard")
	folder = Sanitize_File_Path(path = str(input("Type the file path: ")))

	files = []

	for file in List_Files(folder):
		if file != None:
			files.append(file)

	i = 0
	for file in files:
		print(str(i + 1) + ": " + file)

		i += 1

def Rename_File():
	list_folder = Yes_Or_No_Definer("List files from the folder", second_space = False)

	folder = Select_Choice("Type the folder or get it from the clipboard")
	folder = Sanitize_File_Path(folder)

	if list_folder == True:
		files = List_Files(folder)

		#file_names = Make_Array_With_Filenames(files)

		old_file = Make_Choices(files, files, '"' + local_script_name + '"', extra_option = None, run = False, show_selected_text = None, double_extra_option = None, alternative_choice_list_text = "Choose a file to rename", alternative_array = None, export_number = None, return_choice = True)

	else:
		old_file = folder + Select_Choice("Type the file to rename or get it from the clipboard", first_space = False, second_space = False)

	replace_text_from_file_name = Yes_Or_No_Definer("Replace text from filename", first_space = False, second_space = False)

	add_to_file_name = False

	if replace_text_from_file_name == True:
		text_to_replace = Select_Choice("Type the text to replace", second_space = False)
		replace_with = Select_Choice("Type the text to replace the text above with", second_space = False)
		new_file = Text_Replacer(old_file, text_to_replace, replace_with)

	if replace_text_from_file_name == False:
		add_to_file_name = Yes_Or_No_Definer("Add text to filename", second_space = False)

	if add_to_file_name == True:
		print()
		side = Make_Choices(sides_array, sides_array, '"' + local_script_name + '"', extra_option = None, run = False, show_selected_text = None, double_extra_option = None, alternative_choice_list_text = "Select the side of the filename that you want to add text to", alternative_array = None, export_number = None, return_choice = True)

		text_to_add_to_filename = Select_Choice("Type the text to add to filename", first_space = False, second_space = False)

		if side == left:
			new_file_name = text_to_add_to_filename + old_file

		if side == right:
			new_file_name = old_file.split(".")[0].replace(folder, "") + text_to_add_to_filename

		extension = "." + old_file.split(".")[1]
		new_file = folder + new_file_name + extension

	if add_to_file_name == False and replace_text_from_file_name == False:
		new_file_name = Select_Choice("Type the new filename", second_space = False).replace('"', "")
		extension = "." + old_file.split(".")[1]
		new_file = folder + new_file_name + extension

	Move_File(old_file, new_file)

	print("This file: " + "\n" + old_file)
	print()
	print("Has been renamed to this one: " + "\n" + new_file)

def Image_Spoiler_List_Super_Animes_Comment():
	string_to_format = "[hide={}][img]{}[/img][/hide]"

	spoiler_list = ""

	still_typing = True

	print("Photo number 1")
	description = "1. " + Select_Choice("Type the description of the photo", first_space = False, second_space = False)
	link = Select_Choice("Paste the link of the photo", first_space = False, second_space = False)

	spoiler_list += string_to_format.format(description, link) + "\n"

	i = 2
	while still_typing == True:
		print("\n" + "Photo number " + str(i))

		description = Select_Choice("Type the description of the photo", first_space = False, second_space = False)

		if description == "f":
			still_typing = False

		else:
			description = str(i) + ". " + description
			link = Select_Choice("Paste the link of the photo", first_space = False, second_space = False)
			spoiler_list += string_to_format.format(description, link) + "\n"

		i += 1

	copy(spoiler_list)

def Chapter_Read_Folder_Creator():
	chapter_readers_and_reads_folder = story_folders_dict[spaceliving_key] + "Readers and Reads/"
	global_chapter_read_folder = chapter_readers_and_reads_folder + "Reads/"

	chapter_reads_file = chapter_readers_and_reads_folder + "Leituras.txt"

	file_text = Create_Text_Array_Of_File(chapter_reads_file)

	i = 1
	for line in file_text:
		print()

		chapter_number = Add_Leading_Zeros(file_text[i].split(" - ")[0])

		chapter_read_folder = global_chapter_read_folder + str(chapter_number) + "/"

		if is_a_folder(chapter_read_folder) == False:
			Create_Folder(chapter_read_folder)

		chapter_read_date_file = chapter_read_folder + "Read Date.txt"
		chapter_reader_file = chapter_read_folder + "Reader.txt"

		if is_a_file(chapter_read_date_file) == False:
			Create_Text_File(chapter_read_date_file)

		if is_a_file(chapter_reader_file) == False:
			Create_Text_File(chapter_reader_file)

		chapter = file_text[i]

		print("Título: " + chapter)
		reader = file_text[i - 1]
		print("Leitor: " + reader)
		print("Abrindo arquivo de leitores.")
		copy(reader)
		Open_File_In_Notepad(chapter_reader_file)

		print()
		input("Copiar Data de Leitura?: ")
		print()

		read_date = file_text[i + 1]
		copy(read_date[:-1])
		print("Abrindo arquivo de data de leituras.")
		Open_File_In_Notepad(chapter_read_date_file)
		print(read_date)
		Select_Choice("Próximo?", second_space = False)

		i += 3

format_website_link_parameters = False

if format_website_link_parameters == True:
	source_choice = int(input("1 for online and 2 for source: "))

	if source_choice == 1:
		make_source_links_option = False

	if source_choice == 2:
		make_source_links_option = True

	Make_Choices(website_codes_array, website_codes_array, "Select a website to make the parameter link", extra_option = None, run = False, show_selected_text = True, double_extra_option = None, alternative_choice_list_text = "Select a website to make the parameter link")
	website_name = Choice_Script.choice

	Format_Website_Link_Parameters(website_name, make_source_links_option)

import json
import requests
import secrets

def MAL_API():
	CLIENT_ID = 'adb826e395aebf3633c760a48c49d88e'
	CLIENT_SECRET = 'Q1MBtrXPOrLb-61iBAZaPGlDe3mUUE0IdxRYoaA2nCbN9lXV4xdNNMLJ29Y35CrLaFhev-YV_Evu3_CWLd3x-xEWvI8WnEPTrc6rf2cwJAdB1CTB_Y3BmcgxaOaxO93Z'

	# 1. Generate a new Code Verifier / Code Challenge.
	def get_new_code_verifier() -> str:
		token = secrets.token_urlsafe(100)
		return token[:128]

	# 2. Print the URL needed to authorise your application.
	def print_new_authorisation_url(code_challenge: str):
		global CLIENT_ID

		url = f'https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={CLIENT_ID}&code_challenge={code_challenge}'
		print(f'Authorise your application by clicking here: {url}\n')

	# 3. Once you've authorised your application, you will be redirected to the webpage you've
	#    specified in the API panel. The URL will contain a parameter named "code" (the Authorisation
	#    Code). You need to feed that code to the application.
	def generate_new_token(authorisation_code: str, code_verifier: str) -> dict:
		global CLIENT_ID, CLIENT_SECRET

		url = 'https://myanimelist.net/v1/oauth2/token'
		data = {
			'client_id': CLIENT_ID,
			'client_secret': CLIENT_SECRET,
			'code': authorisation_code,
			'code_verifier': code_verifier,
			'grant_type': 'authorization_code'
		}

		response = requests.post(url, data)
		response.raise_for_status()  # Check whether the requests contains errors

		token = response.json()
		response.close()
		print('Token generated successfully!')

		with open('token.json', 'w') as file:
			json.dump(token, file, indent = 4)
			print('Token saved in "token.json"')

		return token

	# 4. Test the API by requesting your profile information
	def print_user_info(access_token: str):
		url = 'https://api.myanimelist.net/v2/users/@me'
		response = requests.get(url, headers = {
			'Authorization': f'Bearer {access_token}'
			})
		
		response.raise_for_status()
		user = response.json()
		response.close()

		print(f"\n>>> Greetings {user['name']}! <<<")

	if __name__ == '__main__':
		code_verifier = code_challenge = get_new_code_verifier()
		print_new_authorisation_url(code_challenge)

		authorisation_code = input('Copy-paste the Authorisation Code: ').strip()
		token = generate_new_token(authorisation_code, code_verifier)

		print_user_info(token['access_token'])

def Get_Anime_Info(query):
	url = "https://api.myanimelist.net/v2/anime?q=" + query + "&limit=4"
	thing = requests.get(url, headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjEwNjNmZjViMWYwMTIwOGE4Mjg4ODM4ZDU4MjM5NWE3NDYwMzEyYmY1M2VlODI0MTVmZDI2ZWZhZWFmYTVkZDg2MzRkMDJkYzdhODE4N2FiIn0.eyJhdWQiOiJhZGI4MjZlMzk1YWViZjM2MzNjNzYwYTQ4YzQ5ZDg4ZSIsImp0aSI6IjEwNjNmZjViMWYwMTIwOGE4Mjg4ODM4ZDU4MjM5NWE3NDYwMzEyYmY1M2VlODI0MTVmZDI2ZWZhZWFmYTVkZDg2MzRkMDJkYzdhODE4N2FiIiwiaWF0IjoxNjMyODYzMjY1LCJuYmYiOjE2MzI4NjMyNjUsImV4cCI6MTYzNTQ1NTI2NSwic3ViIjoiNTE1MDY3OSIsInNjb3BlcyI6W119.NcgfOiEvUBy0nwEfDUY598DRPaQIdgpFccEc9KW6QGXzDtPKkrmHax7P6PCuQ32AEcXKZbicCC-U7hIjk2mxjxlqCYTJKzY7H_cWnylln9xQTd3FQnoa2V14UaiXSNAt9dzPE7U68tKRiZqou5tNVbm6G4kAZpNlFfNI7EmPnadJ1Uba0q2gcJ19ZugBKlRh0LpeP9vKVwdvtnkmejVLB2sQrqdG7m86AgJsFAQk0-OogMVYJXJM8441nmjxhouoTUMzTiLOk3dkh3SLE1MbeNyDb44x_pcyN1FmMIktolfaWKzc2Ne1CKHWE9RScx3YWVmvSk0iihbUgSw2cPfDvA"})
	json = thing.json()
	animes = json["data"]

	animes_folder = "C:/Animes/"
	Create_Folder(animes_folder)

	for anime in animes:
		anime = anime["node"]
		anime_name = anime["title"]
		anime_id = anime["id"]
		images = anime["main_picture"]
		medium_picture = images["medium"]
		large_picture = images["large"]

		print()
		print(Language_Item_Definer("Anime name", "Nome do Anime") + ": " + anime_name)
		print(Language_Item_Definer("Anime medium picture", "Imagem média do Anime") + ": " + medium_picture)
		print(Language_Item_Definer("Anime large picture", "Imagem larga do Anime") + ": " + large_picture)

		anime_folder = animes_folder + Remove_Non_File_Characters(anime_name) + "/"
		Create_Folder(anime_folder)

		with open(anime_folder + "Medium Image" + "." + medium_picture.split("/")[-1].split(".")[1], 'wb') as f:
			f.write(requests.get(medium_picture).content)

		with open(anime_folder + "Large Image" + "." + large_picture.split("/")[-1].split(".")[1], 'wb') as f:
			f.write(requests.get(large_picture).content)

		text = ""

		text += anime_name + "\n"

		text += str(anime_id)

		Write_To_File(anime_folder + "Info.txt", text)

import string
import random

query = random.sample(string.ascii_lowercase, 3)
query = Stringfy_Array(query)

#Get_Anime_Info(query)

#old_time = str(input("Type the old time: "))
#Difference_Between_Two_Times(old_time)

#Make_Numbered_List()
#Change_Wattpad_Inbox_HTML_Filename()
#Create_A_Lot_Of_Text_Files_From_List()
#Create_Experienced_Medias_Song()
#Make_Book_Text()
#Remove_Number()
#File_Size()
#Make_Table()
#Check_File_Type()
#Rename_File()
#Image_Spoiler_List_Super_Animes_Comment()
#Chapter_Read_Folder_Creator()

def Remove_Duplicated_Lines(duplicated_file, destination_file = None, copy = False):
	Create_Text_File(duplicated_file)

	if destination_file != None:
		Create_Text_File(destination_file)

	duplicated_lines = Create_Array_Of_File(duplicated_file)

	destination_lines = []

	for line in duplicated_lines:
		if line not in destination_lines:
			destination_lines.append(line)

	for line in destination_lines:
		print(line)

	print()
	print(Language_Item_Definer("Duplicated lines", "Linhas duplicadas") + ": " + str(len(duplicated_lines)))
	print(Language_Item_Definer("Unique lines", "Linhas únicas") + ": " + str(len(destination_lines)))

	text = Stringfy_Array(destination_lines, add_line_break = True)

	if copy == False:
		Write_To_File(destination_file, text)

	if copy == True:
		Copy_Text(text)

duplicated_file = "C:/Mega/Image/Social Networks/Hangouts/Emails Females.txt"
destination_file = "C:/Mega/Image/Social Networks/Hangouts/Emails.txt"
#Remove_Duplicated_Lines(duplicated_file, copy = True)

def For_Each_Copy(array):
	for item in array:
		input(item + ": ")
		Copy_Text(item)

#For_Each_Copy(Create_Array_Of_File("C:/Mega/Image/Social Networks/Hangouts/Emails Females.txt"))

def Count_YouTube_Tags(file):
	tags_number = 0
	tags_number_format = "{}/500"
	tags_line = Create_Array_Of_File(file)[0]
	tags = tags_line.split(",")

	used_words = []

	space_number = 0
	used_word_number = 0

	for tag in tags:
		tag_length = len(tag)

		if " " in tag:
			tag_length = len(tag.replace(" ", ""))

			for word in tag.split(" "):
				if word in used_words:
					tags_number += 1
					used_word_number += 1

				for used_word in used_words:
					if len(word) == len(used_word) and word[0] == used_word[0]:
						tags_number += 1

			for word in tag.split(" "):
				if word not in used_words:
					used_words.append(word)

		if " " not in tag:
			if tag in used_words:
				tags_number += 1
				used_word_number += 1

			if tag not in used_words:
				used_words.append(tag)

			for used_word in used_words:
				if len(tag) == len(used_word) and tag[0] == used_word[0]:
					tags_number += 1

		tags_number += tag_length

		if " " in tag:
			tags_number += 3
			space_number += 3

		print()
		print(tags_number, tag_length, tag)
		print(space_number, used_word_number)

		tags_number_text = tags_number_format.format(str(tags_number))

	print(tags_number_text)

variable = "Batata"
print(variable) # Batata

def Função_Que_Modifica_Variável_Global():
	global variable

	variable = "Cenoura"

Função_Que_Modifica_Variável_Global()
print(variable) # Cenoura