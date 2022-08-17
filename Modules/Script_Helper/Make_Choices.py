import os
import locale

locale_variable = locale.getlocale()
default_locale = locale.getdefaultlocale()
default_language = default_locale[0]

if "_" in default_locale[0]:
	default_language = str(default_language).split("_")[0]

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

def Language_Item_Definer(en_item = "", pt_item = "", user_language = "pt"):
	global default_language

	if user_language != "":
		user_language = default_language

	language_en = "en"
	full_language_en = "English"

	language_pt = "pt"
	full_language_pt = "Português"

	if user_language == language_en or user_language == full_language_en:
		item = en_item

	if user_language == language_pt or user_language == full_language_pt:
		item = pt_item

	return item

def Run_Function(function_name):
	function_was_run = False

	if function_name in functions_to_run_array:
		functions_to_run_array[function_name]()

		function_was_run = True

	if function_name not in functions_to_run_array and function_was_run == False:
		print(global_texts_can_not_find_function + ".")

def Make_Choices(choice_descriptions_array, choice_functions_array, script_name = None, extra_option = None, run = None, show_selected_text = True, double_extra_option = None, alternative_choice_list_text = None, custom_selected_text = None, alternative_array = None, export_number = None, return_choice = None, return_first_item = False, return_second_item = False, first_space = True, second_space = True):
	global functions_to_run_array
	global selected_choice
	global selected_folder
	global choice_number
	global double_extra_option_text
	global option_to_export
	global exported_choice_number

	choice_list_text = Language_Item_Definer("Choice list for", "Lista de escolhas para")
	select_choice_text = Language_Item_Definer("Select the choice", "Selecione a opção")

	function_was_run = False

	functions_to_run_array = {
		"None": None
	}

	choice_numbers = [None]

	choice_list = choice_descriptions_array
	choice_list_length = len(choice_descriptions_array) - 1

	if script_name == None:
		script_name = os.path.basename(__file__)

	i = 1
	while i <= choice_list_length:
		if run != False:
			functions_to_run_array[choice_list[i]] = choice_functions_array[i]

		i += 1

	i = 1
	while i <= choice_list_length:
		choice_numbers.append(i)

		i += 1

	if alternative_choice_list_text == None or alternative_choice_list_text == False:
		choice_text = choice_list_text + " " + script_name + ":"

	if alternative_choice_list_text != None and alternative_choice_list_text != False:
		choice_text = alternative_choice_list_text + ":"

	if first_space == True:
		print()

	print(choice_text)

	i = 1
	while i <= choice_list_length:
		print("[" + str(i) + "]" + " - " + choice_list[i])

		i += 1

	print()

	choice = input(select_choice_text + ": ")

	print()

	try:
		choice = int(choice)
		is_number = True

	except ValueError:
		choice = str(choice)
		is_number = False

	choice_list_range = range(1, len(choice_list))

	if is_number == False:
		if choice == "" or choice == " ":
			c = 0
			while choice == "" or choice == " ":
				print()

				if c <= 0:
					new_choice_text = choice_text

				if c != 0:
					new_choice_text = choice_text.replace(":", " (" + str(c) + "x):")

				print(new_choice_text)

				i = 1
				while i <= choice_list_length:
					print("[" + str(i) + "]" + " - " + choice_list[i])

					i += 1

				print()
				choice = input(select_choice_text + ": ")

				try:
					choice = int(choice)

				except ValueError:
					choice = str(choice)

				c += 1

	if is_number == True:
		if choice not in choice_list_range:
			c = 0
			while choice not in choice_list_range:
				print()

				if c <= 0:
					new_choice_text = choice_text

				if c != 0:
					new_choice_text = choice_text.replace(":", " (" + str(c) + "x):")

				print(new_choice_text)

				i = 1
				while i <= choice_list_length:
					print("[" + str(i) + "]" + " - " + choice_list[i])

					i += 1

				print()
				choice = int(input(select_choice_text + ": "))

				c += 1

	selected_choice_text = custom_selected_text

	if custom_selected_text == None:
		selected_choice_text = Language_Item_Definer('You selected the [{}] option', 'Você selecionou a opção [{}]') + "."

	c = 1
	i = 1
	while c <= choice_list_length:
		backup_supposed_choice = choice_list[c]
		supposed_choice = choice_list[c]
		replaced_choice = choice

		if type(replaced_choice) != int:
			list_number = 0
			for accent in brazilian_portuguese_accents:
				supposed_choice = supposed_choice.replace(accent, brazilian_portuguese_accents_helper[list_number])
				replaced_choice = replaced_choice.replace(accent, brazilian_portuguese_accents_helper[list_number])

				list_number += 1

			different_choice_list = [
				replaced_choice,
				replaced_choice.lower(),
				replaced_choice.title(),
				replaced_choice.capitalize(),
				replaced_choice.lower().title(),
				replaced_choice.title(),
				replaced_choice.capitalize(),
			]

		else:
			different_choice_list = [replaced_choice]

		if replaced_choice is choice_numbers[c] and function_was_run == False:
			selected_choice = backup_supposed_choice

			if show_selected_text == True:
				print(selected_choice_text.format(selected_choice))

				if second_space == True:
					print()

			if extra_option == True and return_choice == None:
				selected_folder = selected_choice

				if alternative_array != None:
					option_to_export = alternative_array[c]

			if export_number == True:
				exported_choice_number = c

			if run != False:
				Run_Function(selected_choice)

				function_was_run = True

			if extra_option != True:
				if return_choice == True and export_number == None or return_choice == True and export_number == False:
					return selected_choice

				if return_choice == True and export_number == True and double_extra_option != True:
					exported_choice_number = c
					return selected_choice, exported_choice_number

				if return_choice == True and export_number == None and double_extra_option == True:
					return selected_choice, choice_functions_array[c]

			if extra_option == True and return_choice == True:
				if export_number == True and return_second_item == False:
					exported_choice_number = c
					option_to_export = alternative_array[c]

					return selected_choice, exported_choice_number, option_to_export

				if export_number == None and double_extra_option != True and return_second_item == False:
					return selected_choice

				if export_number == None and double_extra_option == True and return_second_item == False:
					return selected_choice, choice_functions_array[c]

				if return_second_item == True and export_number == False and return_first_item == False:
					return choice_functions_array[c]

				if return_second_item == True and export_number == True and return_first_item == False:
					return choice_functions_array[c], c

				if return_second_item == True and return_first_item == True:
					return selected_choice, choice_functions_array[c]

			i += 1

		if supposed_choice in different_choice_list and function_was_run == False:
			selected_choice = backup_supposed_choice

			if show_selected_text == True:
				print(selected_choice_text.format(selected_choice))

				if second_space == True:
					print()

			if extra_option == True and return_choice == None:
				selected_folder = selected_choice

				if alternative_array != None:
					option_to_export = alternative_array[c]

			if export_number == True:
				exported_choice_number = c

			if run != False:
				Run_Function(selected_choice)

				function_was_run = True

			if extra_option != True:
				if return_choice == True and export_number == None or return_choice == True and export_number == False:
					return selected_choice

				if return_choice == True and export_number == True and double_extra_option != True:
					exported_choice_number = c
					return selected_choice, exported_choice_number

				if return_choice == True and export_number == None and double_extra_option == True:
					return selected_choice, choice_functions_array[c]

			if extra_option == True and return_choice == True:
				if export_number == True and return_second_item == False:
					exported_choice_number = c
					option_to_export = alternative_array[c]

					return selected_choice, exported_choice_number, option_to_export

				if export_number == None and double_extra_option != True and return_second_item == False:
					return selected_choice

				if export_number == None and double_extra_option == True and return_second_item == False:
					return selected_choice, choice_functions_array[c]

				if return_second_item == True and export_number == False and return_first_item == False:
					return choice_functions_array[c]

				if return_second_item == True and export_number == True and return_first_item == False:
					return choice_functions_array[c], c

				if return_second_item == True and return_first_item == True:
					return selected_choice, choice_functions_array[c]

			i += 1

		c += 1

def Mostrar():
	print("Mostrar")

descrições = [
None,
"Um",
"Dois",
]

funções = [
None,
Mostrar,
Mostrar,
]

Make_Choices(descrições, funções, alternative_array = descrições, alternative_choice_list_text = Language_Item_Definer("Select one of the options", "Selecione uma das opções"), return_choice = True, export_number = True, extra_option = True, show_selected_text = True, second_space = False)