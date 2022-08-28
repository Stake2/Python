# Folder_Variables.py

import sys
import time
import datetime
import locale
import subprocess
import webbrowser

from Folder_Lister import *
from Global_Functions import o, is_a_folder, is_a_file, Define_Array, Create_Text_File, Read_Lines, Create_Array_Of_File, Define_True_Or_False
from Language_Variables import global_yes_choice_texts, global_no_choice_texts, global_language, language_en, language_pt, full_language_en, full_language_pt, true_array, false_array

locale_variable = locale.getlocale()
default_locale = locale.getdefaultlocale()
default_language = default_locale[0]

# Defines the current year
now_2 = datetime.datetime.now()
current_year = str(now_2.year)
year = str(current_year)

hard_drive_letter = "{}:/".format("C")
program_files_folder = hard_drive_letter + "Program Files/"
program_files_x86_folder = hard_drive_letter + "Program Files (x86)/"
programs_folder = hard_drive_letter + "Programas/"
scripts_folder = hard_drive_letter + "Apps/"

if is_a_folder(scripts_folder) == False:
	hard_drive_letter = "{}:/".format("D")
	program_files_folder = hard_drive_letter + "Program Files/"
	program_files_x86_folder = hard_drive_letter + "Program Files (x86)/"
	programs_folder = hard_drive_letter + "Programas/"
	scripts_folder = hard_drive_letter + "Apps/"

project_64_folder = program_files_x86_folder + "Project64 3.0/"
project_64 = project_64_folder + "Project64.exe"

snes9x_folder = programs_folder + "Snes9x/"
snes9x = snes9x_folder + "snes9x-x64.exe"

adobe_flash_player = programs_folder + "Adobe Flash Player/flashplayer_32_sa.exe"

script_shortcuts_folder = scripts_folder + "Atalhos/"
script_shortcuts_shortcuts_folder = script_shortcuts_folder + "Atalhos/"
script_shortcuts_white_icons_folder = script_shortcuts_shortcuts_folder + "Com Ícone Branco/"
script_shortcuts_black_icons_folder = script_shortcuts_shortcuts_folder + "Com Ícone Preto/"

vegas_files_folder = hard_drive_letter + "Sony Vegas Files/"
sony_vegas_render_folder = vegas_files_folder + "Render/"
story_covers_vegas_files_folder = vegas_files_folder + "Story Covers/"

path = sys.path[0].replace("\\", "/") + "/"

script_text_files_folder = scripts_folder + "Script Text Files/"
scripts_modules_folder = scripts_folder + "Modules/"

if is_a_folder(script_text_files_folder) == False:
	Create_Folder(script_text_files_folder)

medias_folder = hard_drive_letter + "Mídias/"

mega_folder_name = "Mega/"
mega_folder = hard_drive_letter + mega_folder_name

notepad_folder_name = "Bloco De Notas/"
notepad_folder_name_effort = "Dedicação/"

notepad_folder = mega_folder + notepad_folder_name
notepad_folder_effort = notepad_folder + notepad_folder_name_effort

if is_a_folder(medias_folder) == False:
	Create_Folder(medias_folder)

local_version = False

if is_a_folder(notepad_folder) == False:
	local_version = True

settings_filename = "Settings"
settings_file = scripts_folder + settings_filename + ".txt"

if is_a_file(settings_file) == False:
	settings_filename = "Configurações"
	settings_file = scripts_folder + settings_filename + ".txt"

settings_file = scripts_folder + settings_filename + ".txt"

if is_a_file(settings_file) == False:
	Create_Text_File(settings_file)

script_settings = Create_Array_Of_File(settings_file)
settings = {}

for line in script_settings:
	split_line = line.split("=")

	setting = split_line[0]
	value = split_line[1]

	settings[setting] = value

local_version = Define_True_Or_False(settings["local_version"])

if local_version == True:
	mega_folder = hard_drive_letter + "Apps/" + mega_folder_name

	notepad_folder = mega_folder + notepad_folder_name
	notepad_folder_effort = notepad_folder + notepad_folder_name_effort

	if is_a_folder(mega_folder) == False:
		Create_Folder(mega_folder)

	if is_a_folder(notepad_folder) == False:
		Create_Folder(notepad_folder)

	if is_a_folder(notepad_folder_effort) == False:
		Create_Folder(notepad_folder_effort)

if local_version == False:
	mega_folder = hard_drive_letter + "Mega/"

	notepad_folder = mega_folder + "Bloco De Notas/"
	notepad_folder_effort = notepad_folder + "Dedicação/"

mega_music_folder = mega_folder + "Music/"

notepad_plus_plus = program_files_folder + "Notepad++/notepad++.exe"

vlc_media_player = program_files_folder + "VideoLAN/VLC/vlc.exe"

sony_vegas_eleven = program_files_x86_folder + "Sony/Vegas Pro 11.0/vegas110.exe"

vegas_eighteen = program_files_folder + "VEGAS/VEGAS Pro 18.0/vegas180.exe"

xampp = hard_drive_letter + "xampp/xampp-control.exe"

mega_stories_folder = mega_folder + "Stories/"

notepad_learning_everything_folder = notepad_folder_effort + "Learning Everything - Aprendendo Tudo/"
notepad_learning_izaque_sanvezzo_folder = notepad_learning_everything_folder + "Izaque Sanvezzo/"
notepad_learning_izaque_mwot_folder = notepad_learning_izaque_sanvezzo_folder + "My way of thinking - Meu jeito de pensar/"
notepad_learning_izaque_frameworks_folder = notepad_learning_izaque_mwot_folder + "Frameworks/"
notepad_learning_izaque_frameworks_digital_acquisition_folder = notepad_learning_izaque_frameworks_folder + "Digital Acquisition Frameworks - Frameworks de Aquisição Digital/"
notepad_learning_izaque_frameworks_experiencing_folder = notepad_learning_izaque_frameworks_folder + "'Experiencing Frameworks/"
notepad_learning_izaque_frameworks_producing_folder = notepad_learning_izaque_frameworks_folder + "Producing Frameworks/"

notepad_diary_folder = notepad_folder_effort + "Diary/"
notepad_diary_chapters_folder = notepad_diary_folder + "Chapters/"
diary_slim_folder = notepad_folder_effort + "Diary Slim/"

notepad_folder_years = notepad_folder_effort + "Years/"
current_notepad_year_folder = notepad_folder_years + str(current_year) + "/"
current_year_experienced_media_folder = current_notepad_year_folder + "Experienced Media - Mídias Experimentadas/"

notepad_folder_year_experienced_media_enus = current_notepad_year_folder + full_language_en + "/Experienced Media/"
notepad_folder_year_experienced_music_enus = notepad_folder_year_experienced_media_enus + "Music/"
notepad_folder_year_experienced_media_ptbr = current_notepad_year_folder + full_language_pt + "/Mídias Experimentadas/"
notepad_folder_year_experienced_music_ptbr = notepad_folder_year_experienced_media_ptbr + "Música/"

notepad_new_world_folder = notepad_folder_effort + "New World/"
notepad_new_world_nameids_folder = notepad_new_world_folder + "NameIDs/"
notepad_new_world_nameids_nw_folder = notepad_new_world_nameids_folder + "New World/"
notepad_new_world_nameids_ow_folder = notepad_new_world_nameids_folder + "Old World/"

notepad_food_and_water_registers = notepad_folder_effort + "Food and Water Registers/"
water_amount_folder_name = "Water Amount"
notepad_folder_water_files = notepad_food_and_water_registers + "Water Amount/"
notepad_folder_food_files = notepad_food_and_water_registers + "Food Times/"

mega_image_folder = mega_folder + "Image/"
mega_screenshot_folder = mega_image_folder + "Screenshot/"
mega_not_movie_like_folder = mega_screenshot_folder + "Not Movie Like/"

mega_social_networks_text_folder = notepad_folder_effort + "Social Networks/"

mega_social_networks_images_folder = mega_image_folder + "Social Networks/"

mega_stake2_website_folder = mega_folder + "Websites/"

mega_stake2_subdomain_file = mega_stake2_website_folder + "Subdomain.txt"
netlify_url = "netlify.app"
website_subdomain_name = Read_Lines(mega_stake2_subdomain_file)[0]
mega_stake2_website_link = "https://" + website_subdomain_name + "." + netlify_url + "/"

mega_stake2_website_media_folder = mega_stake2_website_folder + "Images/"
mega_stake2_website_media_story_covers_folder = mega_stake2_website_media_folder + "Story Covers/"

disk_root_story_covers_folder = hard_drive_letter + "Story Book Covers/"

mega_php_folder = mega_folder + "PHP/"
mega_php_tabs_folder = mega_php_folder + "Tabs/"
mega_php_variables_folder = mega_php_folder + "Variables/"
mega_php_variables_global_files_folder = mega_php_variables_folder + "Global Files/"
mega_php_variable_website_php_files_folder = mega_php_variables_folder + "Website PHP Files/"
websites_list_folder = mega_php_variable_website_php_files_folder + "Websites List/"

php_url_format_text_file = mega_php_variable_website_php_files_folder + "PHP URL Format.txt"
html_colors_file = mega_php_variable_website_php_files_folder + "HTML Colors.txt"

networks_folder_name = "Networks"
networks_folder = notepad_folder_effort + networks_folder_name + "/"

Create_Folder(networks_folder)

networks_games_folder = networks_folder + "Games Network/"
networks_game_played_times_folder = networks_games_folder + "Game Played Times - Tempo de Jogatina dos Jogos/"

networks_media_folder = networks_folder + "Media Network/"
networks_comment_writer_folder = networks_media_folder + "Comment_Writer/"
networks_media_comments_folder = networks_media_folder + "Comentários/"
networks_media_comments_animes_folder = networks_media_comments_folder + "Animes/"
networks_media_info_folder = networks_media_folder + "Media Info/"
media_info_folder = networks_media_info_folder
media_info_database_folder = networks_media_info_folder + "Media Info Database/"
media_info_database_media_names_folder = media_info_database_folder + "Media Names/"

watch_history_folder = networks_media_folder + "Watch History/"

folders_list = [
	scripts_folder,
	notepad_folder,
	notepad_folder_effort,
	networks_folder,
	mega_image_folder,
	medias_folder,
]

used_folders_list = [
	scripts_folder,
	notepad_folder,
	notepad_diary_folder,
	notepad_diary_chapters_folder,
	diary_slim_folder,
	notepad_folder_effort,
	notepad_folder_water_files,
	notepad_folder_food_files,
	networks_folder,
	networks_media_folder,
	networks_media_comments_folder,
	medias_folder,
]

for folder in used_folders_list:
	if local_version == True and is_a_folder(folder) == False:
		Create_Folder(folder)

def Open_File(file):
	subprocess.Popen([file])

def Open_File_With_Program(program, file, open_file_switch = None):
	if open_file_switch == None:
		subprocess.Popen([program, file])

	else:
		if open_file_switch == True:
			subprocess.Popen([program, file])

def Open_File_In_Notepad(file):
	subprocess.Popen([notepad_plus_plus, file])

def Open_Video(video_file_to_open):
	subprocess.Popen([vlc_media_player, video_file_to_open])

def Open_Shortcut(shortcut_name):
	files = List_Files(script_shortcuts_white_icons_folder, add_none = False, bind_shortcuts = False)
	shortcuts_folder = List_Files(script_shortcuts_folder, add_none = False, bind_shortcuts = False)
	files = files + shortcuts_folder

	for file in files:
		if shortcut_name in file:
			if ".lnk" in file:
				webbrowser.open(file)

Open_Text_File = Open_File_In_Notepad
Open_File_With_Notepad = Open_File_In_Notepad