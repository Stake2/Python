import datetime
import os

is_a_folder = os.path.isdir
is_a_file = os.path.isfile

def o(file, mode):
	return open(file, mode, encoding="utf8")

def Read_Lines(file):
	return o(file, "r").readlines()

def Create_Array_Of_File(file):
	if is_a_file(file) == True:
		result = Read_Lines(file)
		array_to_return = []

		for line in result:
			line = line.replace("\n", "")

			array_to_return.append(line)

		return array_to_return

	if is_a_file(file) == False:
		quit("Este arquivo não existe: " + file)

hard_drive_letter = "{}:/".format("C")
program_files_folder = hard_drive_letter + "Program Files/"
scripts_folder = hard_drive_letter + "Apps/"

if is_a_folder(scripts_folder) == False:
	hard_drive_letter = "{}:/".format("D")
	program_files_folder = hard_drive_letter + "Program Files/"
	scripts_folder = hard_drive_letter + "Apps/"

mega_folder_name = "Mega/"
mega_folder = hard_drive_letter + mega_folder_name

notepad_folder_name = "Bloco De Notas/"
notepad_folder_name_effort = "Dedicação/"

notepad_folder = mega_folder + notepad_folder_name
notepad_folder_effort = notepad_folder + notepad_folder_name_effort

mega_stories_folder = mega_folder + "Stories/"
notepad_story_database_folder = mega_stories_folder + "Story Database/"

story_names_text_file = notepad_story_database_folder + "Names.txt"
story_wattpad_ids_text_file = notepad_story_database_folder + "Wattpad IDs.txt"

mega_php_folder = mega_folder + "PHP/"
mega_php_tabs_folder = mega_php_folder + "Websites/"
mega_php_variables_folder = mega_php_folder + "Variables/"
mega_php_variables_global_files_folder = mega_php_variables_folder + "Global Files/"
mega_php_variables_website_php_files_folder = mega_php_variables_folder + "Website PHP Files/"
websites_list_folder = mega_php_variables_website_php_files_folder + "Websites List/"

websites_text_file = websites_list_folder + "Websites.txt"
websites = Create_Array_Of_File(websites_text_file)

websites_text_file_ptbr = websites_list_folder + "Sites.txt"
websites_ptbr = Create_Array_Of_File(websites_text_file)

old_year_variable = 2018

now_2 = datetime.datetime.now()
current_year = str(now_2.year)

brazilian_portuguese_accents = [
	"á",
	"à",
	"ã",
	"â",
	"é",
	"è",
	"ê",
	"í",
	"ì",
	"ó",
	"ò",
	"õ",
	"ú",
	"ù",
	"û",
]

brazilian_portuguese_accents_helper = [
	"a",
	"a",
	"a",
	"a",
	"e",
	"e",
	"e",
	"i",
	"i",
	"o",
	"o",
	"o",
	"u",
	"u",
	"u",
]

story_names = Create_Array_Of_File(story_names_text_file)
wattpad_ids = Create_Array_Of_File(story_wattpad_ids_text_file)

story_names_array_enus = [None]
story_names_array_ptbr = [None]

for story_name in story_names:
	if ", " in story_name:
		story_name = story_name.split(", ")[0]

	story_names_array_enus.append(story_name)

for story_name in story_names:
	if ", " in story_name:
		story_name = story_name.split(", ")[1]

	story_names_array_ptbr.append(story_name)

story_names_dict_keys = [None]

for story_name in story_names_array_enus:
	if story_name != None:
		if " - " in story_name:
			story_name = story_name.split(" - ")[1]

		story_name = story_name.replace(story_name, story_name.lower().replace(" ", "_"))

		story_names_dict_keys.append(story_name)

story_names_dict_enus = {}
story_names_dict_ptbr = {}

i = 1
dict = story_names_dict_enus
array = story_names_array_enus
for key in story_names_dict_keys:
	if key != None:
		dict[key] = array[i]

		i += 1

i = 1
dict = story_names_dict_ptbr
array = story_names_array_ptbr
for key in story_names_dict_keys:
	if key != None:
		dict[key] = array[i]

		i += 1

def Year_Text_Generator(array_to_append, mode = None, less_one = False):
	global current_year

	year_variable = old_year_variable

	local_current_year = current_year

	if less_one == True:
		local_current_year = str(int(local_current_year) - 1)

	while year_variable <= int(local_current_year):
		if mode == str:
			year_variable_to_use = str(year_variable)

		if mode == int:
			year_variable_to_use = int(year_variable)

		array_to_append.append(year_variable_to_use)

		year_variable += 1

website_names_array_enus = [None]

for website in websites:
	website = website.split(", ")[0]

	if website == "Years":
		website_names_array_enus.append(website)

		Year_Text_Generator(website_names_array_enus, str)

	else:
		website_names_array_enus.append(website)

website_names_array_ptbr = [None]

for website in websites_ptbr:
	website = website.split(", ")[0]

	if website == "Years":
		website_names_array_ptbr.append(website)

		Year_Text_Generator(website_names_array_ptbr, str)

	else:
		website_names_array_ptbr.append(website)

website_names_dict_keys = [None]

for website_name in website_names_array_enus:
	if website_name != None:
		website_name = website_name.replace(website_name, website_name.lower().replace(" ", "_"))

		website_names_dict_keys.append(website_name)

website_names_dict_ptbr = {"None": None}
website_names_dict_enus = {"None": None}

i = 1
for key in website_names_dict_keys:
	if key != None:
		website_names_dict_enus[key] = website_names_array_enus[i]

		i += 1

i = 1
for key in website_names_dict_keys:
	if key != None:
		website_names_dict_ptbr[key] = website_names_array_ptbr[i]

		i += 1

day_names_ptbr = [
	None,
	"Segunda-Feira",
	"Terça-Feira",
	"Quarta-Feira",
	"Quinta-Feira",
	"Sexta-Feira",
	"Sábado",
	"Domingo",
]

portuguese_day_gender_words = {
	"Segunda-Feira": "uma",
	"Terça-Feira": "uma",
	"Quarta-Feira": "uma",
	"Quinta-Feira": "uma",
	"Sexta-Feira": "uma",
	"Sábado": "um",
	"Domingo": "um",
}

day_names_enus = [
	None,
	"Monday",
	"Tuesday",
	"Wednesday",
	"Thursday",
	"Friday",
	"Saturday",
	"Sunday",
]

month_names_ptbr = [
	None,
	"Janeiro",
	"Fevereiro",
	"Março",
	"Abril",
	"Maio",
	"Junho",
	"Julho",
	"Agosto",
	"Setembro",
	"Outubro",
	"Novembro",
	"Dezembro",
]

def Number_Name_Generator(array_to_extend = None, extend_array = None, return_array = None, copy = None, language = "enus"):
	if language in ["pt", "ptbr"]:
		first_numbers = [
			None,
			"um",
			"dois",
			"três",
			"quatro",
			"cinco",
			"seis",
			"sete",
			"oito",
			"nove",
			"dez",
		]

		ten_names = [
			None,
			"dez",
			"vinte",
			"trinta",
			"quarenta",
			"cinquenta",
			"sessenta",
			"setenta",
			"oitenta",
			"noventa",
			"cem",
		]

		number_separator = " e "

	if language in ["en", "enus"]:
		first_numbers = [
			None,
			"one",
			"two",
			"three",
			"four",
			"five",
			"six",
			"seven",
			"eight",
			"nine",
			"ten",
			"eleven",
			"twelve",
			"thirteen",
			"fourteen",
			"fifteen",
			"sixteen",
			"seventeen",
			"eighteen",
			"nineteen",
		]

		ten_names = [
			None,
			"teen",
			"twenty",
			"thirty",
			"fourty",
			"fifty",
			"sixty",
			"seventy",
			"eighty",
			"ninety",
			"hundred",
		]

		ten_number_names = [
			None,
			"one",
			"two",
			"three",
			"four",
			"five",
			"six",
			"seven",
			"eight",
			"nine",
			"ten",
			"eleven",
			"twelve",
			"thirteen",
			"fourteen",
			"fifteen",
			"sixteen",
			"seventeen",
			"eighteen",
			"nineteen",
		]

		number_separator = " "

	number_names = [None]

	i = 1
	while i <= 100:
		if i <= 10:
			number_names.append(first_numbers[i])

		if language in ["pt", "ptbr"]:
			if i == 11:
				number_names.append("onze")

			if i == 12:
				number = first_numbers[2][:-2]
				number_names.append(number + "ze")

			if i == 13:
				number = first_numbers[3][:-1].replace("ê", "e")
				number_names.append(number + "ze")

			if i == 14:
				number = first_numbers[4].replace("ro", "or")
				number_names.append(number + "ze")

			if i == 15:
				number_names.append("quinze")

			if i >= 16 and i <= 17:
				number = str(i).replace("1", "")
				number = first_numbers[10] + "es" + first_numbers[int(number)]
				number_names.append(number)

			if i >= 18 and i <= 19:
				number = str(i).replace("1", "")
				number = first_numbers[10] + first_numbers[int(number)]

				if i == 19:
					number = number.replace(first_numbers[10], first_numbers[10] + "e")

				number_names.append(number)

			if i > 19 and i < 100:
				number = str(i)[:-1]

				if int(str(i)[1]) != 0:
					number = ten_names[int(number)] + number_separator + first_numbers[int(str(i)[1])]

				else:
					number = ten_names[int(number)]

				number_names.append(number)

		if language in ["en", "enus"]:
			if i >= 11 and i <= 19:
				number_names.append(first_numbers[i])

			if i >= 20 and "0" in str(i)[1]:
				first_number = int(str(i)[:-1])

				number_names.append(ten_names[first_number])

			if i >= 20 and "0" not in str(i)[1]:
				first_number = int(str(i)[:-1])
				second_number = int(str(i)[1:])

				number_names.append(ten_names[first_number] + number_separator + first_numbers[second_number])

		i += 1

	number_string = ""

	i = 1
	for number_name in number_names:
		if number_name != None:
			if number_name != number_names[-1]:
				number_string += number_name + "\n"

			else:
				number_string += number_name

			i += 1

	numbers_array = [None]
	numbers_array.extend(number_string.splitlines())

	numbers_array_without_none = []
	numbers_array_without_none.extend(number_string.splitlines())

	if extend_array == True and array_to_extend != None:
		array_to_extend.extend(numbers_array_without_none)

	if return_array == True:
		return numbers_array

	if copy == True:
		pyperclip.copy(number_string)

number_names_pt = Number_Name_Generator(return_array = True, language = "pt")
number_names_en = Number_Name_Generator(return_array = True, language = "en")