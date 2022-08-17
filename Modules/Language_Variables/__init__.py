import locale

from Global_Functions import o, is_a_folder, is_a_file, Create_Text_File, Create_Array_Of_File, Define_True_Or_False

locale_variable = locale.getlocale()
default_locale = locale.getdefaultlocale()

default_language = default_locale[0]

if "_" in default_locale[0]:
	default_language = str(default_language).split("_")[0]

hard_drive_letter = "{}:/".format("C")
program_files_folder = hard_drive_letter + "Program Files/"
scripts_folder = hard_drive_letter + "Apps/"

if is_a_folder(scripts_folder) == False:
	hard_drive_letter = "{}:/".format("D")
	program_files_folder = hard_drive_letter + "Program Files/"
	scripts_folder = hard_drive_letter + "Apps/"

settings_filename = "Settings"
settings_file = scripts_folder + settings_filename + ".txt"

if is_a_file(settings_file) == False:
	settings_filename = "Configurações"
	settings_file = scripts_folder + settings_filename + ".txt"

if is_a_file(settings_file) == False:
	settings_filename = "Opções"
	settings_file = scripts_folder + settings_filename + ".txt"

if is_a_file(settings_file) == False:
	Create_Text_File(settings_file)

script_settings = Create_Array_Of_File(settings_file)

settings = {}

true_array = [
"True",
"true",
]

false_array = [
"False",
"false",
]

for line in script_settings:
	split_line = line.split("=")

	setting = split_line[0]
	value = split_line[1]

	settings[setting] = value

use_custom_language_text = "use_custom_language"

if use_custom_language_text in settings:
	use_custom_language = Define_True_Or_False(settings[use_custom_language_text])

else:
	use_custom_language = False

if use_custom_language == False:
	global_language_text = default_language

else:
	global_language_text = settings["language"]

dot_text = ".txt"

# Defines language variables
global_languages_array_enus = [
None,
"en",
"EN",
"english",
"English",
"English - Inglês",
"Inglês",
"inglês",
"ingles",
]

global_languages_array_ptbr = [
None,
"pt",
"PT",
"português",
"portugues",
"portuguese",
"Português",
"Portugues",
"Portuguese",
]

languages_array = [
None,
"en",
"pt",
]

languages_with_global = [
None,
"geral",
"en",
"pt",
]

full_languages_with_global = [
None,
"Geral",
"English",
"Português",
]

languages_with_hyphen = [
None,
"en",
"pt",
]

full_languages = [
None,
"English",
"Português",
]

full_languages_not_none = [
"English",
"Português",
]

full_languages_translated = [
None,
"English - Inglês",
"Português - Portuguese",
]

language_numbers = [
None,
1,
2,
]

enus_lang = languages_array[1]
ptbr_lang = languages_array[2]

language_en = languages_array[1]
language_pt = languages_array[2]

full_language_en = full_languages[1]
full_language_pt = full_languages[2]

hyphen_separated_enus = languages_with_hyphen[1]
hyphen_separated_ptbr = languages_with_hyphen[2]

translated_enus = full_languages_translated[1]
translated_ptbr = full_languages_translated[2]

if global_language_text in global_languages_array_enus:
	global_language = language_en
	language_number = 1

if global_language_text in global_languages_array_ptbr:
	global_language = language_pt
	language_number = 2

full_languages_translated_dict = {
"English": [None, "English", "Inglês"],
"Português": [None, "Portuguese", "Português"],
}

english_for_portuguese = translated_enus.split(" - ")[1]
portuguese_for_english = translated_ptbr.split(" - ")[1]

if global_language == language_en:
	global_texts = [
	None,
	"Is",
	"Name",
	"Surname",
	"Full name",
	"Race",
	"Hybrid",
	"Sex",
	"Age",
	"Years Old",
	"In Planet Years",
	"Born In The Year",
	"Born In The Planet",
	"Name Given By The Local Species",
	"Resides On The Galaxy",
	"Number Of Beings",
	"Current Year In The Planet\"s Calendar",
	"This text was copied to the clipboard",
	"This text was written in the \"{}\" file",
	"The file was created, opening it",
	"The file already existed, opening it",
	"The file was open",
	"Can not find that function",
	"Running {} Functions",
	"Script execution ended",
	"The function \"{}\" was executed",
	"This variable is not defined",
	"Choose",
	"Choose file",
	"Open this file",
	"Open all files",
	"Opening this file",
	"Open this link",
	"Opening this link",
	"This file was created",
	"This folder was created",
	]

if global_language == language_pt:
	global_texts = [
	None,
	"É",
	"Nome",
	"Sobrenome",
	"Nome completo",
	"Raça",
	"Híbrida",
	"Sexo",
	"Idade",
	"Anos De Idade",
	"Em Anos Planetários",
	"Nascido No Ano",
	"Nascido No Planeta",
	"Nome Dado Pela Espécie Local",
	"Fica Na Galáxia",
	"Número De Seres",
	"Ano Atual No Calendário Do Planeta",
	"Esse texto foi copiado para a área de transferência",
	"Esse texto foi escrito no arquivo \"{}\"",
	"O arquivo foi criado, abrindo ele",
	"O arquivo já existia, abrindo ele",
	"O arquivo foi aberto",
	"Não consigo encontrar essa função",
	"Execução do script encerrada",
	"Executando as funções do {}",
	"A função \"{}\" foi executada",
	"Essa variável não está definida",
	"Escolha",
	"Escolher arquivo",
	"Abrir este arquivo",
	"Abrir todos os arquivos",
	"Abrindo este arquivo",
	"Abrir este link",
	"Abrindo este link",
	"Este arquivo foi criado",
	"Esta pasta foi criada",
	]

i = 1

global_texts_is = global_texts[i]
i += 1

global_texts_name = global_texts[i]
i += 1

global_texts_sur_name = global_texts[i]
i += 1

global_texts_full_name = global_texts[i]
i += 1

global_texts_race = global_texts[i]
i += 1

global_texts_hybrid = global_texts[i]
i += 1

global_texts_sex = global_texts[i]
i += 1

global_texts_age = global_texts[i]
i += 1

global_texts_years_old = global_texts[i]
i += 1

global_texts_in_planet_years = global_texts[i]
i += 1

global_texts_born_in_the_year = global_texts[i]
i += 1

global_texts_born_in_the_planet = global_texts[i]
i += 1

global_texts_given_name_by_the_local_species = global_texts[i]
i += 1

global_texts_resides_on_the_galaxy = global_texts[i]
i += 1

global_texts_number_of_beings = global_texts[i]
i += 1

global_texts_current_year_in_the_planets_calendar = global_texts[i]
i += 1

global_texts_copied_clipboard = global_texts[i]
i += 1

global_texts_text_written_to_file = global_texts[i]
i += 1

global_texts_file_was_created_opening = global_texts[i]
i += 1

global_texts_file_already_existed_opening = global_texts[i]
i += 1

global_texts_file_open = global_texts[i]
i += 1

global_texts_can_not_find_function = global_texts[i]
i += 1

global_texts_script_execution_ended = global_texts[i]
i += 1

global_texts_running_functions = global_texts[i]
i += 1

global_texts_function_executed = global_texts[i]
i += 1

global_texts_variable_not_defined = global_texts[i]
i += 1

global_texts_choose = global_texts[i]
i += 1

global_texts_choose_file = global_texts[i]
i += 1

global_texts_open_file = global_texts[i]
i += 1

global_texts_open_all_files = global_texts[i]
i += 1

global_texts_opening_file = global_texts[i]
i += 1

global_texts_open_link = global_texts[i]
i += 1

global_texts_opening_link = global_texts[i]
i += 1

global_texts_file_was_created = global_texts[i]
i += 1

global_texts_folder_was_created = global_texts[i]
i += 1

global_yes_choice_texts = [
None,
1,
"1",
"yes",
"Yes",
"y",
"Y",
"yy",
"YY",
"sim",
"Sim",
"s",
"S",
"ss",
"SS",
]

global_no_choice_texts = [
None,
2,
"2",
"no",
"No",
"n",
"N",
"não",
"Não",
"n",
"N",
"nn",
"NN",
]

global_yes_choice_texts_enus = [
None,
1,
"yes",
"Yes",
"y",
"Y",
"yy",
"YY",
"1",
]

global_no_choice_texts_enus = [
None,
2,
"no",
"No",
"n",
"N",
"nn",
"NN",
"2",
]

global_yes_choice_texts_ptbr = [
None,
1,
"sim",
"Sim",
"s",
"S",
"ss",
"SS",
"1",
]

global_no_choice_texts_ptbr = [
None,
2,
"não",
"Não",
"n",
"N",
"nn",
"NN",
"2",
]

if global_language == language_en:
	yes_choice_texts_array = global_yes_choice_texts_enus
	no_choice_texts_array = global_no_choice_texts_enus

if global_language == language_pt:
	yes_choice_texts_array = global_yes_choice_texts_ptbr
	no_choice_texts_array = global_no_choice_texts_ptbr

yes_array = yes_choice_texts_array
no_array = no_choice_texts_array

chapters_text = "Chapters"
covers_text = "Covers"
story_info_text = "Story Info"