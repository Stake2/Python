import pyperclip
from Script_Helper import *

current_year = current_year
now = time.strftime("%H:%M %d/%m/%Y")

global_create_file = True

author_name = "Izaque Sanvezzo (ow_h_m_18_2002) (stake2, Funkysnipa Cat)"

'''
Escrito por: Izaque Sanvezzo (ow_h_m_18_2002) (stake2, Funkysnipa Cat)
Data de criação: 21:11 18/03/2020
Data de edição: 20:50 25/10/2020

---

Coisas feitas em 2020: 273
(722 junto com comentários e pessoas conhecidas)

Coisas produtivas: 46
Coisas assistidas: 205
Novas histórias: 1
Progresso das histórias: 4
Novos sites: 12
Pessoas que conheci: 100
Comentários no site Super Animes: 349 (#532)

---

Coisas produtivas: 46
Nem todas as coisas produtivas estão aqui.
Transformar o 2019.html no 2019.php
Fiz o Watch.py renomear e mover os arquivos de vídeo
Consertei o Core.py fazendo ele mais bonito e adicionei uma função para publicar histórias
Consertei as abas de ler capítulo do SpaceLiving.php e adicionei uma margem
Fiz o script de AutoHotKey chamado 'PlayPause.ahk' perguntar se você quer controlar o Youtube, YTMusic ou o Soundcloud
Fiz o script de Python 'Publicar um site' perguntar se você quer a versão simples ou não (Sómente 'Git init' ou com servidor PHP e código fonte)
Fiz o Framework de PHP

Coisas assistidas: 205
Animes: 81
Desenhos: 37
Séries: 27
Filmes: 4
Vídeos: 56

Novas histórias: 1
1 - O Segredo dos Cristais

Progresso das histórias: 4
A Vida de Pequenata, capítulos: 1, palavras: 617, caracteres: 3.391
SpaceLiving, capítulos: 1, palavras: 3.098, caracteres: 17.098
A História dos Irmãos Nazzevo, capítulos: 7, palavras: 9.311, caracteres: 4.9658
O Segredo dos Cristais, capítulos: 0, palavras: 19.309, caracteres: 102.430

Novos sites: 12
1 - My Little Pony
2 - Tarefas
3 - Coisas Que Eu Faço
4 - Anos
5 - 2018
6 - 2019
7 - 2020
8 - A História dos Irmãos Nazzevo
9 - Ilha Deserta
10 - Histórias Solitárias
11 - Frameworks Mentais
12 - Modelo de Site

Pessoas que conheci: 100

Comentários no site SuperAnimes: 349 (#532)
'''

def Define_Year_Summary_Texts_Array():
	global selected_year_summary_texts_array_enus
	global selected_year_summary_texts_array_ptbr

	selected_year_summary_texts_array_enus = [
	None,
	"Written by: {}" + "\n",
	"Creation date: {}" + "\n",
	"Edit date: {}" + "\n",

	"Things made in {}: {}\n({} along with comments and people met)",

	"Productive things: {}",

	"Watched things: {}",

	"New stories: {}",

	"Story progress: {}",

	"New websites: {}",

	"People that I have met: {}",

	"Comments on the SuperAnimes website: {} ({})",

	"chapters: ",
	"words: ",
	"characters: ",
	]

	selected_year_summary_texts_array_ptbr = [
	None,
	"Escrito por: {}" + "\n",
	"Data de criação: {}" + "\n",
	"Data de edição: {}" + "\n",

	"Coisas feitas em {}: {}\n({} junto com comentários e pessoas conhecidas)",

	"Coisas produtivas: {}",

	"Coisas assistidas: {}",

	"Novas histórias: {}",

	"Progresso das histórias: {}",

	"Novos sites: {}",

	"Pessoas que conheci: {}",

	"Comentários no site SuperAnimes: {} ({})",

	"capítulos: ",
	"palavras: ",
	"caracteres: ",
	]

def Select_Language(language_to_select = None):
	global selected_language
	global selected_year_summary_texts_array
	global selected_media_type_array
	global selected_story_names_array
	global selected_story_names_dict
	global selected_website_names_array
	global selected_website_names_dict
	global story_names
	global media_type_texts_array

	if language_to_select == None:
		selected_language = language_ptbr

	if language_to_select != None:
		selected_language = language_to_select

	if selected_language == language_enus:
		selected_year_summary_texts_array = selected_year_summary_texts_array_enus
		selected_media_type_array = media_type_names_enus_plural
		selected_story_names_array = story_names_array_enus
		selected_story_names_dict = story_names_dict_enus
		selected_website_names_array = website_names_array_enus
		selected_website_names_dict = website_names_dict_enus

	if selected_language == language_ptbr:
		selected_year_summary_texts_array = selected_year_summary_texts_array_ptbr
		selected_media_type_array = media_type_names_ptbr_plural
		selected_story_names_array = story_names_array_ptbr
		selected_story_names_dict = story_names_dict_ptbr
		selected_website_names_array = website_names_array_ptbr
		selected_website_names_dict = website_names_dict_ptbr

	story_names = selected_story_names_array

	media_type_texts_array = [
	None,
	selected_media_type_array[1] + ": {}",
	selected_media_type_array[2] + ": {}",
	selected_media_type_array[3] + ": {}",
	selected_media_type_array[4] + ": {}",
	selected_media_type_array[5] + ": {}",
	]

def Define_Text_Files():
	global year_numbers_text_file
	global new_stories_text_file
	global story_progress_file
	global new_websites_file
	global year_numbers_text
	global new_stories_text
	global story_progress_text
	global new_websites_text
	global watched_episodes_text
	global watched_things_number
	global watched_episodes_mediatype_text
	global selected_watched_episodes_mediatype_file
	global current_year_folder
	global task_names_enus_file
	global task_names_ptbr_file
	global selected_task_names_file_text
	global task_names_enus_text
	global task_names_ptbr_text
	global task_locations_file
	global number_of_tasks
	global year_stuff_text_file

	from Watch import watched_episodes_file, watched_episodes_mediatype_enus, watched_episodes_mediatype_ptbr

	from Tasks import task_names_enus_file, task_names_ptbr_file, task_locations_file, number_of_tasks

	task_names_enus_text = open(task_names_enus_file, 'r', encoding='utf8').readlines()
	task_names_ptbr_text = open(task_names_ptbr_file, 'r', encoding='utf8').readlines()

	if selected_language == language_enus:
		selected_watched_episodes_mediatype_file = watched_episodes_mediatype_enus
		selected_task_names_file_text = task_names_enus_text

	if selected_language == language_ptbr:
		selected_watched_episodes_mediatype_file = watched_episodes_mediatype_ptbr
		selected_task_names_file_text = task_names_ptbr_text

	current_year_folder = notepad_folder_years + str(current_year) + "/"

	year_numbers_text_file = current_year_folder + "Year Numbers.txt"
	new_stories_text_file = current_year_folder + "New Stories.txt"
	story_progress_file = current_year_folder + "Story Progress.txt"
	new_websites_file = current_year_folder + "New Websites.txt"
	year_stuff_text_file = current_year_folder + "Year Stuff.txt"

	year_summary_maker_files_array = [
	None,
	current_year_folder + "Year Numbers.txt",
	current_year_folder + "New Stories.txt",
	current_year_folder + "Story Progress.txt",
	current_year_folder + "New Websites.txt",
	]

	year_numbers_text_file_text = o(year_numbers_text_file, 'r').readlines()

	if global_create_file == True:
		for file in year_summary_maker_files_array:
			if file != None:
				if is_a_file(file) == False:
					if file == year_numbers_text_file:
						write_file = o(file, 'w')
						write_file.write(author_name + "\n")
						write_file.write(now + "\n")
						write_file.write(now + "\n")

					else:
						Create_Text_File(file)

	year_numbers_text = open(year_numbers_text_file, 'r', encoding='utf8').readlines()
	new_stories_text = open(new_stories_text_file, 'r', encoding='utf8').readlines()
	story_progress_text = open(story_progress_file, 'r', encoding='utf8').readlines()
	new_websites_text = open(new_websites_file, 'r', encoding='utf8').readlines()
	watched_episodes_text = open(watched_episodes_file, 'r', encoding='utf8').readlines()
	watched_things_number = len(watched_episodes_text)

	watched_episodes_mediatype_text = open(selected_watched_episodes_mediatype_file, 'r', encoding='utf8').readlines()

def Define_Story_Variables():
	global littletato_storyname
	global spaceliving_storyname
	global secret_of_the_crystals_storyname
	global desert_island_storyname
	global nazzevo_storyname
	global to_be_invincible_storyname
	global my_little_pony_the_visit_of_izaque_storyname
	global my_little_pony_rise_to_equestria_storyname
	global lonely_stories_a_perfect_world_storyname

	i = 1

	littletato_storyname = selected_story_names_array[i]

	i += 1

	spaceliving_storyname = selected_story_names_array[i]

	i += 1

	secret_of_the_crystals_storyname = selected_story_names_array[i]

	i += 1

	desert_island_storyname = selected_story_names_array[i]

	i += 1

	nazzevo_storyname = selected_story_names_array[i]

	i += 1

	to_be_invincible_storyname = selected_story_names_array[i]

	i += 1

	my_little_pony_the_visit_of_izaque_storyname = selected_story_names_array[i]

	i += 1

	my_little_pony_rise_to_equestria_storyname = selected_story_names_array[i]

	i += 1

	lonely_stories_a_perfect_world_storyname = selected_story_names_array[i]

def Define_Year_Global_Texts():
	global written_by
	global creation_date_text
	global edit_date_text
	global things_made_in_year
	global productive_things_header
	global watched_things_header
	global new_stories_header
	global stories_progress_header
	global chapters_text
	global words_text
	global characters_text
	global new_websites_header
	global people_that_i_met_header
	global comments_on_superanimes_header
	global first_media_type
	global second_media_type
	global third_media_type
	global fourth_media_type
	global fifth_media_type
	global new_stories_text_length
	global story_names_length
	global new_websites_text_length
	global new_stories_header
	global year_data_dict_names
	global year_data_text
	global things_made_in_year_number
	global author_name
	global creation_date
	global edition_date
	global things_made_in_year_text
	global top_year_info_texts
	global my_year_texts_array
	global author_name_key
	global creation_date_key
	global edition_date_key
	global productive_things_key
	global watched_things_key
	global first_media_type_key
	global second_media_type_key
	global third_media_type_key
	global fourth_media_type_key
	global fifth_media_type_key
	global new_websites_key
	global people_that_i_met_key
	global comments_on_superanimes_key

	my_year_texts_array = [
	"My {}",
	"Meu {}",
	]

	i = 1
	written_by = selected_year_summary_texts_array[i]

	i += 1
	creation_date_text = selected_year_summary_texts_array[i]
	i += 1
	edit_date_text = selected_year_summary_texts_array[i]
	i += 1

	things_made_in_year = selected_year_summary_texts_array[i]
	i += 1

	productive_things_header = selected_year_summary_texts_array[i]
	i += 1

	watched_things_header = selected_year_summary_texts_array[i]
	i += 1

	new_stories_header = selected_year_summary_texts_array[i]
	i += 1

	stories_progress_header = selected_year_summary_texts_array[i]
	i += 1

	i = 12
	chapters_text = selected_year_summary_texts_array[i]
	i += 1
	words_text = selected_year_summary_texts_array[i]
	i += 1
	characters_text = selected_year_summary_texts_array[i]

	i = 9
	new_websites_header = selected_year_summary_texts_array[i]
	i += 1

	people_that_i_met_header = selected_year_summary_texts_array[i]
	i += 1

	comments_on_superanimes_header = selected_year_summary_texts_array[i]

	first_media_type = media_type_texts_array[1]
	second_media_type = media_type_texts_array[2]
	third_media_type = media_type_texts_array[3]
	fourth_media_type = media_type_texts_array[4]
	fifth_media_type = media_type_texts_array[5]

	new_stories_text_length = len(new_stories_text)

	story_names_length = len(selected_story_names_array)

	new_websites_text_length = len(new_websites_text)

	new_stories_header = selected_year_summary_texts_array[7].format(new_stories_text_length)

	year_data_dict_names = [
	"author_name_key",
	"creation_date_key",
	"edition_date_key",
	"productive_things_key",
	"watched_things_key",
	first_media_type,
	second_media_type,
	third_media_type,
	fourth_media_type,
	fifth_media_type,
	"new_websites_key",
	"people_that_i_met_key",
	"comments_on_superanimes_key",
	]

	i = 0
	author_name_key = year_data_dict_names[i]
	i += 1
	creation_date_key = year_data_dict_names[i]
	i += 1
	edition_date_key = year_data_dict_names[i]
	i += 1
	productive_things_key = year_data_dict_names[i]
	i += 1
	watched_things_key = year_data_dict_names[i]
	i += 1
	first_media_type_key = year_data_dict_names[i]
	i += 1
	second_media_type_key = year_data_dict_names[i]
	i += 1
	third_media_type_key = year_data_dict_names[i]
	i += 1
	fourth_media_type_key = year_data_dict_names[i]
	i += 1
	fifth_media_type_key = year_data_dict_names[i]
	i += 1
	new_websites_key = year_data_dict_names[i]
	i += 1
	people_that_i_met_key = year_data_dict_names[i]
	i += 1
	comments_on_superanimes_key = year_data_dict_names[i]

	year_data_text = {}

	i = 0
	for line in year_numbers_text:
		if i == 3:
			year_data_text[people_that_i_met_key] = line.replace("\n", "")

		else:
			year_data_text[year_data_dict_names[i]] = line.replace("\n", "")

		i += 1

	#i = 3
	#things_made_in_year_number = int(year_data_text[year_data_dict_names[i]])

	i = 3
	watched_things_header_replaced = watched_things_header.replace("{}", "")
	#watched_things_number = int(year_data_text[year_data_dict_names[i]].replace(watched_things_header_replaced, ""))

	i = 0
	#author_name = year_data_text[year_data_dict_names[i]]

	i += 1
	creation_date = year_data_text[year_data_dict_names[i]]

	i += 1
	edition_date = year_data_text[year_data_dict_names[i]]

	i += 1

	#things_made_in_year_text = things_made_in_year.format(str(current_year), str(things_made_in_year_number))

	i += 1

	top_year_info_texts = written_by.format(author_name) + creation_date_text.format(creation_date) + edit_date_text.format(now)

def Make_Productive_Things():
	global task_locations_file_text
	global task_locations_file_text_length
	global productive_things_string
	global productive_things_number
	global productive_things_list
	global productive_things_header

	task_locations_file_text = o(task_locations_file, 'r').readlines()

	productive_things_list = ""

	if selected_language == language_enus:
		productive_things_list += "Not every productive thing is here." + "\n"

	if selected_language == language_ptbr:
		productive_things_list += "Nem todas as coisas produtivas estão aqui." + "\n"

	if len(selected_task_names_file_text) >= 10:
		i = 0
		while i <= 10:
			if i != len(selected_task_names_file_text) - 1:
				productive_things_list += selected_task_names_file_text[i].replace("\n", "") + "\n"

			if i == len(selected_task_names_file_text) - 1:
				productive_things_list += selected_task_names_file_text[i].replace("\n", "")

			i += 1

	if len(selected_task_names_file_text) < 10:
		i = 0
		while i <= len(selected_task_names_file_text) - 1:
			if i != len(selected_task_names_file_text) - 1:
				productive_things_list += selected_task_names_file_text[i].replace("\n", "") + "\n"

			if i == len(selected_task_names_file_text) - 1:
				productive_things_list += selected_task_names_file_text[i].replace("\n", "")

			i += 1

	task_locations_file_text_length = len(task_locations_file_text)
	productive_things_number = task_locations_file_text_length

	if productive_things_number == 1:
		productive_things_header = productive_things_header.replace("Coisas", "Coisa")
		productive_things_header = productive_things_header.replace("produtivas", "produtiva")
		productive_things_header = productive_things_header.replace("things", "thing")

	productive_things_string = productive_things_header.format(productive_things_number)

def Make_Watched_Things():
	global watched_things_header
	global first_watched_media
	global second_watched_media
	global third_watched_media
	global fourth_watched_media
	global fifth_watched_media
	global watched_media_texts
	global watched_media_texts_length
	global all_watched_things
	global top_year_info_texts
	global first_media_type_number
	global second_media_type_number
	global third_media_type_number
	global fourth_media_type_number
	global fifth_media_type_number

	first_media_type_number = 1
	second_media_type_number = 0
	third_media_type_number = 0
	fourth_media_type_number = 0
	fifth_media_type_number = 0

	first_media_type_replace = first_media_type.replace("s: {}", "")
	second_media_type_replace = second_media_type.replace("s: {}", "")
	third_media_type_replace = third_media_type.replace("s: {}", "")
	fourth_media_type_replace = fourth_media_type.replace("s: {}", "")
	fifth_media_type_replace = fifth_media_type.replace("s: {}", "")

	if watched_things_number == 1:
		watched_things_header = watched_things_header.replace("assistidas", "assistida")
		watched_things_header = watched_things_header.replace("things", "thing")
		watched_things_header = watched_things_header.replace("Coisas", "Coisa")

	watched_things_header = watched_things_header.format(str(watched_things_number))

	for line in watched_episodes_mediatype_text:
		line = line.replace("\n", "")

		if line == first_media_type_replace:
			first_media_type_number += 1

	for line in watched_episodes_mediatype_text:
		line = line.replace("\n", "")

		if line == second_media_type_replace:
			second_media_type_number += 1

	for line in watched_episodes_mediatype_text:
		line = line.replace("\n", "")

		if line == third_media_type_replace:
			third_media_type_number += 1

	for line in watched_episodes_mediatype_text:
		line = line.replace("\n", "")

		if line == fourth_media_type_replace:
			fourth_media_type_number += 1

	for line in watched_episodes_mediatype_text:
		line = line.replace("\n", "")

		if line == fifth_media_type_replace:
			fifth_media_type_number += 1

	first_watched_media = first_media_type.format(first_media_type_number)

	second_watched_media = second_media_type.format(second_media_type_number)

	third_watched_media = third_media_type.format(third_media_type_number)

	fourth_watched_media = fourth_media_type.format(fourth_media_type_number)

	fifth_watched_media = fifth_media_type.format(fifth_media_type_number)

	watched_media_texts = [None]
	watched_media_texts.append(first_watched_media)
	watched_media_texts.append(second_watched_media)
	watched_media_texts.append(third_watched_media)
	watched_media_texts.append(fourth_watched_media)
	watched_media_texts.append(fifth_watched_media)

	watched_media_texts_length = len(watched_media_texts)

	all_watched_things = ""

	i = 1
	for media_text in watched_media_texts:
		if i != watched_media_texts_length and media_text != None:
			all_watched_things += media_text + "\n"

		if i == watched_media_texts_length and media_text != None:
			all_watched_things += media_text

		i += 1

def Make_Story_Progress():
	global all_story_progress_string
	global story_chapters_number
	global story_name_number
	global story_name
	global stories_progress_text
	global stories_progress_header
	global chapters_text
	global do_not_add_story_progress
	global has_story_progress

	all_story_progress_string = ""
	story_chapters_number = 0

	if len(story_progress_text) != 0:
		story_progress_text_length = len(story_progress_text) - 1

	if len(story_progress_text) == 0:
		story_progress_text_length = len(story_progress_text)

	do_not_add_story_progress = False
	has_story_progress = False

	if len(story_progress_text) == 0:
		do_not_add_story_progress = True

	if do_not_add_story_progress == False:
		has_story_progress = True

		i = 0
		while i <= len(story_progress_text) - 1:
			story_array = story_progress_text[i]
			story_array = story_array.split(", ")

			story_name = selected_story_names_dict[story_array[0]]

			if len(story_array) == 4:
				string_to_format = "{}, {}, {}, {}"

				c = 0
				story_chapters = chapters_text + story_array[c + 1].replace("\n", "")
				story_words = words_text + story_array[c + 2].replace("\n", "")
				story_characters = characters_text + story_array[c + 3].replace("\n", "")
				story_chapters_number = story_chapters_number + int(story_array[c + 1].replace("\n", ""))

				if story_chapters_number == 1:
					story_chapters = story_chapters.replace("chapters", "chapter")
					story_chapters = story_chapters.replace("capítulos", "capítulo")

				formatted_string = string_to_format.format(story_name, story_chapters, story_words, story_characters)

				if i != len(story_progress_text) - 1:
					all_story_progress_string += formatted_string + "\n"

				if i == len(story_progress_text) - 1:
					all_story_progress_string += formatted_string

			if len(story_array) == 3:
				string_to_format = "{}, {}, {}"

				c = 0
				story_chapters = chapters_text + story_array[c + 1].replace("\n", "")
				story_words = words_text + story_array[c + 2].replace("\n", "")
				story_chapters_number = story_chapters_number + int(story_array[c + 1].replace("\n", ""))

				if story_chapters_number == 1:
					story_chapters = story_chapters.replace("chapters", "chapter")
					story_chapters = story_chapters.replace("capítulos", "capítulo")

				formatted_string = string_to_format.format(story_name, story_chapters, story_words)

				if i != len(story_progress_text) - 1:
					all_story_progress_string += formatted_string + "\n"

				if i == len(story_progress_text) - 1:
					all_story_progress_string += formatted_string

			i += 1

		if story_progress_text_length + 1 == 1:
			stories_progress_header = stories_progress_header.replace("histórias", "história")
			stories_progress_header = stories_progress_header.replace("das", "da")

		i = 9
		stories_progress_text = stories_progress_header.format(len(story_progress_text))

def Make_New_Stories_Array():
	global full_year_summary_string
	global new_stories_array
	global new_stories_number
	global new_stories_string
	global has_new_stories

	new_stories_number = len(new_stories_text)

	new_stories_string = ""

	new_stories_array = [None]

	do_not_add_new_stories = False
	has_new_stories = False

	if len(new_stories_text) == 0:
		do_not_add_new_stories = True

	if do_not_add_new_stories == False:
		has_new_stories = True

		i = 0
		c = 0
		while i <= len(new_stories_text) - 1:
			if selected_language == language_enus:
				new_story_number = 0

			if selected_language == language_ptbr:
				new_story_number = 1

			new_stories_text[c] = new_stories_text[c].split(", ")[new_story_number].replace("\n", "")

			new_story_text = str(i + 1) + " - " + new_stories_text[c].replace("\n", "")

			new_stories_array.append(new_story_text)

			if i != new_stories_text_length - 1:
				new_stories_string += new_story_text + "\n"

			if i == new_stories_text_length - 1:
				new_stories_string += new_story_text

			c += 1
			i += 1

def Make_New_Websites_Text():
	global all_new_websites_string
	global website_name
	global new_websites_header_text
	global new_websites_number
	global do_not_add_new_websites
	global new_websites_header
	global has_new_websites

	new_websites_number = len(new_websites_text)

	all_new_websites_string = ""

	do_not_add_new_websites = False
	has_new_websites = False

	if new_websites_number == 0:
		do_not_add_new_websites = True

	if do_not_add_new_websites == False:
		has_new_websites = True

		i = 0
		for text in new_websites_text:
			new_websites_text[i] = new_websites_text[i].replace("\n", "")

			i += 1

		i = 0
		while i <= len(new_websites_text) - 1:
			website_name = selected_website_names_dict[new_websites_text[i]]
			website_name = str(i + 1) + " - " + website_name

			if i != len(new_websites_text) - 1:
				all_new_websites_string += website_name + "\n"

			if i == len(new_websites_text) - 1:
				all_new_websites_string += website_name

			i += 1

	if new_websites_number == 1:
		new_websites_header = new_websites_header.replace("Novos", "Novo")
		new_websites_header = new_websites_header.replace("sites", "site")

		new_websites_header = new_websites_header.replace("websites", "website")

	new_websites_header_text = new_websites_header.format(str(new_websites_number))

def Make_People_That_I_Met_Text():
	global people_that_i_met_text
	global people_that_i_met_number
	global people_that_i_met_header

	people_that_i_met_number = year_data_text[people_that_i_met_key].replace("\n", "")

	if int(people_that_i_met_number) == 1:
		people_that_i_met_header = people_that_i_met_header.replace("Pessoas", "Pessoa")
		people_that_i_met_header = people_that_i_met_header.replace("People", "Person")

	people_that_i_met_text = year_data_text[people_that_i_met_key].replace("\n", "")
	people_that_i_met_text = people_that_i_met_header.format(people_that_i_met_text.replace("\n", ""))

from Comment_Writer import *

def Make_Comments_On_SuperAnimes_Text():
	global comments_on_superanimes_text
	global year_comment_number
	global last_comment_number
	global comments_on_superanimes_header

	year_comment_number = Get_Comment_Number(return_year_comment_number = True)[0]
	last_comment_number = Get_Comment_Number(return_year_comment_number = True)[1].replace("\n", "")

	if year_comment_number == 1:
		comments_on_superanimes_header = comments_on_superanimes_header.replace("Comments", "Comment")
		comments_on_superanimes_header = comments_on_superanimes_header.replace("Comentários", "Comentário")

	comments_on_superanimes_text = comments_on_superanimes_header.format(year_comment_number, last_comment_number)

def Make_Year_Summary_Text():
	global things_made_in_year_number
	global full_year_summary_string

	if new_stories_number != 0:
		things_made_in_year_number = productive_things_number + watched_things_number + new_stories_number + story_chapters_number + new_websites_text_length

	if new_stories_number == 0:
		things_made_in_year_number = productive_things_number + watched_things_number + story_chapters_number + new_websites_text_length

	things_made_in_year_number_2 = things_made_in_year_number + int(people_that_i_met_number) + year_comment_number

	things_made_in_year_text = things_made_in_year.format(str(current_year), str(things_made_in_year_number), things_made_in_year_number_2)

	full_year_summary_string = ""

	full_year_summary_string += top_year_info_texts

	full_year_summary_string += "\n---\n\n"

	full_year_summary_string += things_made_in_year_text + "\n" + "\n"

	full_year_summary_string += productive_things_string + "\n"

	full_year_summary_string += watched_things_header + "\n"

	if new_stories_number != 0:
		full_year_summary_string += new_stories_header + "\n"

	if do_not_add_story_progress == False:
		full_year_summary_string += stories_progress_text + "\n"

	if do_not_add_new_websites == False:
		full_year_summary_string += new_websites_header_text + "\n"

	full_year_summary_string += people_that_i_met_text + "\n"
	full_year_summary_string += comments_on_superanimes_text + "\n" + "\n"

	full_year_summary_string += "---\n\n"

	full_year_summary_string += productive_things_string + "\n"

	full_year_summary_string += productive_things_list + "\n" + "\n"

	full_year_summary_string += watched_things_header + "\n"

	if new_stories_number != 0:
		if do_not_add_story_progress == True:
			full_year_summary_string += all_watched_things + "\n" + "\n"

		if do_not_add_story_progress == False and new_stories_number == 0:
			full_year_summary_string += all_watched_things

		if do_not_add_story_progress == False and new_stories_number != 0:
			full_year_summary_string += all_watched_things + "\n" + "\n"

	if new_stories_number == 0:
		if do_not_add_story_progress == True:
			full_year_summary_string += all_watched_things + "\n" + "\n"

		if do_not_add_story_progress == False:
			full_year_summary_string += all_watched_things

	if new_stories_number != 0:
		full_year_summary_string += new_stories_header + "\n"

		full_year_summary_string += new_stories_string

	if do_not_add_new_websites == False and do_not_add_story_progress == False:
		full_year_summary_string += "\n" + "\n" + stories_progress_text + "\n"

		full_year_summary_string += all_story_progress_string + "\n" + "\n"

	if do_not_add_new_websites == True and do_not_add_story_progress == False:
		full_year_summary_string += "\n" + "\n" + stories_progress_text + "\n"

		full_year_summary_string += all_story_progress_string + "\n" + "\n"

	if do_not_add_new_websites == False:
		full_year_summary_string += new_websites_header_text + "\n"

		full_year_summary_string += all_new_websites_string + "\n" + "\n"

	full_year_summary_string += people_that_i_met_text + "\n" + "\n"

	full_year_summary_string += comments_on_superanimes_text

def Make_New_Year_Summary_Text_File(selected_text_file):
	file = selected_text_file
	open_file = o(file, 'w')
	write_file = open_file.write(full_year_summary_string)
	open_file.close()

def Write_Year_Summary_To_Text_Files():
	Define_Year_Summary_Texts_Array()
	Select_Language(language_enus)
	Define_Text_Files()
	Define_Story_Variables()
	Define_Year_Global_Texts()
	Make_Productive_Things()
	Make_Watched_Things()
	Make_New_Stories_Array()
	Make_Story_Progress()
	Make_New_Websites_Text()
	Make_People_That_I_Met_Text()
	Make_Comments_On_SuperAnimes_Text()
	Make_Year_Summary_Text()

	my_year_text_enus = my_year_texts_array[0]
	my_year_text_ptbr = my_year_texts_array[1]

	selected_my_year_text_file = current_year_folder + my_year_text_enus.format(str(current_year)) + ".txt"
	Make_New_Year_Summary_Text_File(selected_my_year_text_file)

	Define_Year_Summary_Texts_Array()
	Select_Language(language_ptbr)
	Define_Text_Files()
	Define_Story_Variables()
	Define_Year_Global_Texts()
	Make_Productive_Things()
	Make_Watched_Things()
	Make_New_Stories_Array()
	Make_Story_Progress()
	Make_New_Websites_Text()
	Make_People_That_I_Met_Text()
	Make_Comments_On_SuperAnimes_Text()
	Make_Year_Summary_Text()

	selected_my_year_text_file = current_year_folder + my_year_text_ptbr.format(str(current_year)) + ".txt"
	Make_New_Year_Summary_Text_File(selected_my_year_text_file)

def Make_Year_Summary():
	Write_Year_Summary_To_Text_Files()

	print(full_year_summary_string)

	true_or_false_string = str(has_new_stories) + ", " + str(has_story_progress) + ", " + str(has_new_websites)

	file = year_stuff_text_file
	file_write = o(file, 'w')
	file_write.write(true_or_false_string)
	file_write.close()