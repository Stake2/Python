# New_World_NameID_Generator_Module.py

import pathlib
import random
import datetime

from Script_Helper import *
from Text_Generator.New_World_NameID_Generator_Module.New_World_Variables import *

option = True

global_switches = {
"write_to_file": option,
"create_folders": option,
"create_files": option,
"move_files": option,
}

# Surname array
surnames = ["Sanvezzo", "Yorkishire", "Bezerra", "Rubens", "Silva", "Lins", "Martins", "Hernandes", "De Assis"]

# Male name arrays
male_names = ["Marcos", "Felipe", "João", "Angelo", "Izaque", "John", "Isaac", "Kevin", "Yudi"]

# Female name arrays
female_names = ["Angélica", "Sofia", "Ana", "Gabrielle", "Gabriele", "Gabriela", "Gabriella", "Patrícia", "Rosana"]

def New_World_Get_Random_Parameters():
	global name_array
	global full_race
	global full_hybrid_race
	global full_genre
	global full_universe_type
	global name
	global surname
	global now
	global parameters_array
	global surnames
	global male_names
	global female_names
	global has_hybrid_race
	global has_hybrid_race_choice
	global hybrid_race
	global races_array_len

	true_false_array = [True, False]

	true_false_array_len = len(true_false_array) - 1

	true_false = true_false_array[random.randint(0, true_false_array_len)]

	genres_enus_len = len(genres_enus) - 1

	# Defines the genre of the person using a random integer between 0 and 1
	number = random.randint(0, genres_enus_len)

	while number == 0:
		number = random.randint(0, genres_enus_len)
	
	genre = genres_enus[number]

	# If the genre is female then it will use the female names and surnames arrays, it will set the genre as "f" for female
	if genre == genre_enus_female:
		name_array = female_names

		full_genre = genre_enus_female
		genre = "f"

	# If the genre is male then it will use the male names and surnames arrays, it will set the genre as "m" for male
	if genre == genre_enus_male:
		name_array = male_names

		full_genre = genre_enus_male
		genre = "m"

	# Defines the name and surname of the being using a random integer between 0 and the total length of the names and surnames arrays
	name = name_array[random.randint(0, len(name_array) - 1)]
	surname = surnames[random.randint(0, len(surnames) - 1)]

	# Concatenates the name and surname strings together
	full_name = name + " " + surname

	# Create the universe_selector which is a random integer between 0 and the total length of the universe types array
	number = random.randint(0, new_world_universe_types_len)

	while number == 0:
		number = random.randint(0, new_world_universe_types_len)

	universe_selector = number

	# Selects a universe type between New World and Old World using the random integer created in the universe_selector variable
	universe_type = new_world_universe_types_small[universe_selector]
	full_universe_type = new_world_universe_types[universe_selector]

	number = random.randint(0, new_world_universe_types_len)

	while number == 0:
		number = random.randint(0, new_world_universe_types_len)

	planet_born = planets_array[number]

	number = random.randint(0, races_array_len)

	while number == 0:
		number = random.randint(0, races_array_len)

	# Defines the race and small race of the being
	full_race = races_array[number]
	race = races_small_array[number]

	has_hybrid_race = False
	has_hybrid_race_choice = False

	if true_false == True:
		i = 0
		for race_parameter in races_array:
			if race_parameter == full_race:
				races_array.pop(i)

			i += 1

		i = 0
		for race_variable in races_small_array:
			if race_variable == race:
				races_small_array.pop(i)

			i += 1

		races_array_len = len(races_array) - 1

		has_hybrid_race = True
		has_hybrid_race_choice = True

		number = random.randint(1, races_array_len)

		full_hybrid_race = races_array[number]
		hybrid_race = races_small_array[number]

		#while len(hybrid_race) > 2:
		#	hybrid_race = hybrid_race[:-1].lower()

	# Selects the age of the being using a random integer between 0 and the total length of the ages array
	age = ages[random.randint(0, ages_len)]

	if has_hybrid_race == True:
		return [None, full_name, universe_type, race, hybrid_race, genre, age, planet_born]

	if has_hybrid_race == False:
		return [None, full_name, universe_type, race, genre, age, planet_born]

def New_World_Generate_NameID(print_things = True, copy_nameid = True, language_number = None):
	global now
	global name_array
	global rance
	global full_race
	global full_hybrid_race
	global genre
	global full_genre
	global age
	global full_universe_type
	global name
	global surname
	global full_name
	global birthday_year
	global now
	global parameters_array
	global surnames
	global male_names
	global female_names
	global has_hybrid_race_choice
	global has_hybrid_race
	global use_random_parameters
	global choosen_random_parameters_choice
	global full_new_world_nameid
	global planet_born
	global detailed_nameid

	if language_number != None:
		language, full_language = Language_And_Full_Language_Definer(language_number)

	else:
		language, full_language = Language_And_Full_Language_Definer(Language_Item_Definer(1, 2))

	# Variable to declare if the detailed info of the NameID will be displayed
	detailed_info = True

	# Gets the now time
	now = datetime.datetime.now()

	# Gets the current year
	current_year = int(now.year)

	full_name = ""
	universe_type = ""
	race = ""
	genre = ""
	age = ""

	use_random_parameters_choice_string = global_yes_or_no_string.format("Use random parameters")

	if choosen_random_parameters_choice == False:
		use_random_parameters = Yes_Or_No_Definer(Language_Item_Definer("Use random parameters", "Usar parâmetros aleatórios"), first_space = False)

		choosen_random_parameters_choice = True

	if use_random_parameters == True:
		parameters_array = New_World_Get_Random_Parameters()

		if has_hybrid_race == True:
			full_name = parameters_array[1]
			universe_type = parameters_array[2]
			race_parameter = parameters_array[3]
			hybrid_race = parameters_array[4]
			genre = parameters_array[5]
			age = parameters_array[6]
			planet_born = parameters_array[7]

			race = race_parameter + "-" + hybrid_race

		if has_hybrid_race == False:
			full_name = parameters_array[1]
			universe_type = parameters_array[2]
			race = parameters_array[3]
			genre = parameters_array[4]
			age = parameters_array[5]
			planet_born = parameters_array[6]

	# Select typed parameters
	if use_random_parameters == False:
		name = Select_Choice(Language_Item_Definer("Type the name of person", "Digite o nome da pessoa")).title()
		surname = Select_Choice(Language_Item_Definer("Type the surname of person", "Digite o sobrenome da pssoa")).title()

		# Concatenates the name and surname strings together
		full_name = name + " " + surname

		print()
		race = Make_Choices(races_array, races_array, run = False, alternative_choice_list_text = Language_Item_Definer("Select a race from the race list", "Selecione uma raça na lista de raças"), export_number = True, return_choice = True)[0]

		full_race = race

		while len(race) > 1:
			race = race[:-1].lower()

		old_race = race

		has_hybrid_race_choice = Yes_Or_No_Definer(Language_Item_Definer("Has hybrid race", "Tem raça híbrida"), first_space = False)

		print()

		if has_hybrid_race_choice == True:
			i = 0

			for race in races_array:
				if race == full_race:
					races_array.pop(i)

				i += 1

		if has_hybrid_race_choice == True:
			hybrid_race = Make_Choices(races_array, races_array, run = False, alternative_choice_list_text = Language_Item_Definer("Select a hybrid race from the hybrid race list", "Selecione uma raça híbrida da lista de raças híbridas"), export_number = True, return_choice = True)[0]

			full_hybrid_race = hybrid_race

			while len(hybrid_race) > 1:
				hybrid_race = hybrid_race[:-1].lower()

			race = old_race + "-" + hybrid_race

		choice_info = Make_Choices(genres_enus, genres_enus, run = False, alternative_choice_list_text = Language_Item_Definer("Select a genre from the genre list", "Selecione um gênero da lista de gêneros"), export_number = True, return_choice = True)

		genre = choice_info[0]
		full_genre = choice_info[0]

		while len(genre) > 1:
			genre = genre[:-1].lower()

		age = Select_Choice("Type your age", "Digite sua idade")
		print()

		universe_type = Make_Choices(new_world_universe_types, new_world_universe_types_small, run = False, alternative_choice_list_text = Language_Item_Definer("Select an universe type from the universe types list", "Selecione um tipo de universo da lista de tipos de universo"), export_number = True, return_choice = True)[0]

		full_universe_type = universe_type

		universe_type = universe_type.split(" ")
		first_word = universe_type[0]
		second_word = universe_type[1]

		while len(first_word) > 1:
			first_word = first_word[:-1].lower()

		while len(second_word) > 1:
			second_word = second_word[:-1].lower()

		universe_type = first_word + second_word

		planet_born = Make_Choices(planets_array, planets_array, run = False, alternative_choice_list_text = Language_Item_Definer("Select a planet from the planets list", "Selecione um planeta da lista de planetas"), export_number = True, return_choice = True)[0]

	# Concatenates the race string with the genre string
	race_and_sex = race + "_" + genre

	# Calculates the birthday year of the being by subtracting the age from the current year
	birthday_year = current_year - age

	planet_born_small = planet_born.split("(")[0].lower()
	planet_born_small = planet_born_small.replace("_", "")
	planet_born_name = planet_born.split("(")[0].replace("_MW", "")

	# Concatenates the full name, universe type, small race, genre, age, and birthday year together
	full_new_world_nameid = full_name + "(" + universe_type + "_" + race_and_sex + "_" + str(age) + "_" + str(birthday_year) + "_" + planet_born_small + ")"

	number = Language_Item_Definer(1, 2, language)

	Generate_Detailed_Info(Language_Item_Definer(1, 2, language))

	# Shows the full detailed info of the NameID on the console if the detailed_info variable is True
	if detailed_info == True and print_things == True:
		print(Language_Item_Definer("Detailed info is on, showing detailed info of NameID", "Informações detalhadas estão ativadas, mostrando informações detalhadas do NameID") + ": ")
		print()

		print(detailed_nameid)
		print()

	if copy_nameid == True:
		Copy_Text(full_new_world_nameid)

def Generate_Detailed_Info(language_number):
	global detailed_nameid

	language, full_language = Language_And_Full_Language_Definer(language_number)

	# Generates the "detailed_nameid" string
	detailed_nameid = ""

	if full_universe_type == new_world_name:
		detailed_nameid += Language_Item_Definer("New World NameID", "NameID do New World", language) + ":" + "\n" + full_new_world_nameid + "\n"

	if full_universe_type == old_world_name:
		detailed_nameid += Language_Item_Definer("Old World NameID", "NameID do Old World", language) + ":" + "\n" + full_new_world_nameid + "\n"

	detailed_nameid += "\n"
	detailed_nameid += Language_Item_Definer("Name", "Nome", language) + ": " + name + "\n"
	detailed_nameid += Language_Item_Definer("Surname", "Sobrenome", language) + ": " + surname + "\n"
	detailed_nameid += Language_Item_Definer("Full name", "Nome completo", language) + ": " + full_name + "\n"

	i = 1

	is_new_worlder_text = Language_Item_Definer("Is New Worlder", "É um New Worlder", language)

	if full_universe_type == new_world_name:
		detailed_nameid += is_new_worlder_text + ": " + Language_Item_Definer("Yes", "Sim", language) + "\n"

	if full_universe_type == old_world_name:
		detailed_nameid += is_new_worlder_text + ": " + Language_Item_Definer("No", "Não", language) + "\n"

	detailed_nameid += "\n"

	new_world_race_text = Language_Item_Definer("New World Race", "Raça do New World", language)
	old_world_race_text = Language_Item_Definer("Old World Race", "Raça do Old World", language)
	hybrid_race_text = Language_Item_Definer("Hybrid Race", "Raça Híbrida", language)
	race_sex_text = Language_Item_Definer("Race Sex", "Sexo da Raça", language)

	if full_universe_type == new_world_name:
		if full_race == race_human:
			detailed_nameid += new_world_race_text + ": " + race_human_extended + "\n"

		else:
			detailed_nameid += new_world_race_text + ": " + full_race + "\n"

	if full_universe_type == old_world_name:
		if full_race == race_human:
			detailed_nameid += old_world_race_text + ": " + race_human_extended + "\n"

		else:
			detailed_nameid += old_world_race_text + ": " + full_race + "\n"

	if has_hybrid_race_choice == True:
		detailed_nameid += hybrid_race_text + ": " + full_hybrid_race + "\n"

	detailed_nameid += race_sex_text + ": " + full_genre + "\n"
	detailed_nameid += "\n"

	age_in_planet_years_text = Language_Item_Definer("Age In Planet Years", "Idade Em Anos Do Planeta Terra", language)
	years_old_in_planet_earth_years_text = Language_Item_Definer("Years Old In Planet Earth Years", "Anos De Idade Em Anos Do Planeta Terra", language)

	age_string_to_format = age_in_planet_years_text + ": {} ({} " + years_old_in_planet_earth_years_text + ")"
	age_text = str(age)
	age_formatted_string = age_string_to_format.format(age_text, age_text)

	born_in_the_text = Language_Item_Definer("Born In The", "Nascido No", language)
	born_in_the_year_text = born_in_the_text + " " + Language_Item_Definer("Year", "Ano", language)
	born_in_the_planet_text = born_in_the_text + " " + Language_Item_Definer("Planet", "Planeta", language)
	in_planet_earth_years_text = Language_Item_Definer("In Planet Earth Years", "Em Anos Do Planeta Terra", language)

	year_born_string_to_format = born_in_the_year_text + ": {} (" + in_planet_earth_years_text + ")"
	year_born_text = str(birthday_year)
	year_born_string_formatted = year_born_string_to_format.format(year_born_text)

	planet_born_string_to_format = born_in_the_planet_text + ": {}"
	planet_born_string_formatted = planet_born_string_to_format.format(planet_born)

	detailed_nameid += age_formatted_string + "\n"
	detailed_nameid += year_born_string_formatted + "\n"
	detailed_nameid += planet_born_string_formatted + "\n"
	detailed_nameid += "\n" + "\n"

	if planet_born == planet_earth:
		detailed_nameid += planet_id_earth

	if planet_born == planet_mars:
		detailed_nameid += planet_id_mars

def Create_Text_File_With_NameID():
	global choosen_random_parameters_choice

	choosen_random_parameters_choice = False

	New_World_Generate_NameID(print_things = True, copy_nameid = False, text_language = language_en)

	universe_type_folders = {
	"New World": notepad_new_world_nameids_nw_folder,
	"Old World": notepad_new_world_nameids_ow_folder,
	}

	universe_type = universe_type_folders[full_universe_type]

	folder_to_use = universe_type
	nameid_text_file = universe_type + full_new_world_nameid + ".txt"

	print(Language_Item_Definer("Creating this text file", "Criando esse arquivo de texto") + ": ")
	print(nameid_text_file)
	print()

	Create_Text_File(nameid_text_file, global_switches["create_files"])

	text_to_write = detailed_nameid
	Write_To_File(nameid_text_file, text_to_write, global_switches["write_to_file"])

	Generate_Detailed_Info(2)

	text_to_append = detailed_nameid + "\n\n---\n\n" + detailed_nameid
	Append_To_File(nameid_text_file, text_to_append, global_switches["write_to_file"])

choosen_random_parameters_choice = False

def NWNIDG_Choose():
	import Script_Helper

	nwnidg_choice_descriptions = [
	None,
	Language_Item_Definer("Generate and copy new NameID", "Gerar e copiar novo NameID"),
	Language_Item_Definer("Create new text file with NameID", "Criar novo arquivo de texto com NameID"),
	]

	nwnidg_choice_functions = [
	None,
	New_World_Generate_NameID,
	Create_Text_File_With_NameID,
	]

	choice_list_text = Language_Item_Definer("Select a New World NameID Generator Function to execute", "Selecione uma função do Gerador de NameID do New World para executar")

	local_script_name = "New_World_NameID_Generator.py"
	Script_Helper.Make_Choices.function_was_run = False
	Script_Helper.Make_Choices(nwnidg_choice_descriptions, nwnidg_choice_functions, script_name = local_script_name, extra_option = None, run = True, show_selected_text = True, double_extra_option = False, alternative_choice_list_text = choice_list_text, alternative_array = False, export_number = False, return_choice = False)