# Script_Helper.py

import sys
import datetime

local_script_name = "Script_Helper.py"

from Global_Variables import *

# Defines the current year
now_2 = datetime.datetime.now()
current_year = str(now_2.year)
year = str(current_year)

quit_texts_array = ["q", "quit", "Quit", "QUIT", "e", "exit", "Exit", "EXIT", "stop", "Stop", "STOP", "s", "sair", "Sair", "SAIR", "f", "fechar", "Fechar", "FECHAR", "p", "parar", "Parar", "PARAR", "/q", "/quit", "/Quit", "/QUIT", "/e", "/exit", "/Exit", "/EXIT", "/stop", "/Stop", "/STOP", "/s", "/sair", "/Sair", "/SAIR", "/f", "/fechar", "/Fechar", "/FECHAR", "/p", "/parar", "/Parar", "/PARAR"]

def Define_Array(array_to_define):
	global selected_array
	global array_length

	selected_array = array_to_define
	array_length = len(array_to_define) - 1

	return selected_array, array_length

global_yes_or_no_string = "{}" + "?: \n[1] - /" + yes_array[2] + " - " + yes_array[3] + "\n[2] - /" + no_array[2] + " - " + no_array[3] + "\n\n[" + global_texts_choose + "]: "

def Yes_Or_No_Definer(question, convert_to_yes_or_no = False, first_space = True, second_space = True):
	yes_or_no_string = global_yes_or_no_string.format(question)
	choose_yes_or_no_text = Language_Item_Definer("Choose yes or no, 1 or 2", "Escolha sim ou não, 1 ou 2")

	if first_space == True:
		print()

	yes_or_no_choice = input(yes_or_no_string + "/")

	try:
		yes_or_no_choice = str(yes_or_no_choice)

	except TypeError:
		yes_or_no_choice = int(yes_or_no_choice)

	if yes_or_no_choice == "":
		i = 1
		while yes_or_no_choice == "":
			if i == 1:
				yes_or_no_string = global_yes_or_no_string.format(question).replace("?", "? " + choose_yes_or_no_text)

			if i != 1:
				yes_or_no_string = global_yes_or_no_string.format(question).replace("?", "? " + choose_yes_or_no_text + " (" + str(i) + "x)")

			print()
			yes_or_no_choice = input(yes_or_no_string + "/")

			try:
				yes_or_no_choice = str(yes_or_no_choice)

			except TypeError:
				yes_or_no_choice = int(yes_or_no_choice)

			i += 1

	if yes_or_no_choice not in yes_array and yes_or_no_choice not in no_array:
		i = 1
		while yes_or_no_choice not in yes_array and yes_or_no_choice not in no_array:
			if i == 1:
				yes_or_no_string = global_yes_or_no_string.format(question).replace("?", "? " + choose_yes_or_no_text)

			if i != 1:
				yes_or_no_string = global_yes_or_no_string.format(question).replace("?", "? " + choose_yes_or_no_text + " (" + str(i) + "x)")

			print()
			yes_or_no_choice = input(yes_or_no_string + "/")

			try:
				yes_or_no_choice = str(yes_or_no_choice)

			except TypeError:
				yes_or_no_choice = int(yes_or_no_choice)

			i += 1

	if yes_or_no_choice in yes_array:
		yes_or_no = True

	if yes_or_no_choice in no_array:
		yes_or_no = False

	if convert_to_yes_or_no == True:
		if yes_or_no == True:
			yes_or_no = "Yes"

		if yes_or_no == False:
			yes_or_no = "No"

	if second_space == True:
		print()

	return yes_or_no

def Define_Yes_Or_No(value):
	value = str(value)

	if value in global_yes_choice_texts:
		yes_or_no = True

	if value in global_no_choice_texts:
		yes_or_no = False

	return yes_or_no

# Defines the language texts for the current scripts
def Set_Language(language_parameter = None, local_script_name_parameter = None, make_two_language_arrays = None, another_language_folder = None):
	global language_variable
	global texts
	global script_language_texts
	global enus_script_language_texts
	global ptbr_script_language_texts
	global enus_script_texts_file
	global ptbr_script_texts_file
	global local_script_name
	global yes_choice_texts_array
	global no_choice_texts_array
	global yes_array
	global no_array
	global language_folder

	local_script_name = local_script_name_parameter

	if another_language_folder == None:
		language_folder_to_use = language_folder + local_script_name.replace(".py", "") + "/"

	if another_language_folder != None:
		language_folder_to_use = another_language_folder

	script_language_texts = []
	enus_script_language_texts = []
	ptbr_script_language_texts = []

	if language_parameter != None:
		language_variable = language_parameter
		watch_selected_language = language_parameter

	else:
		language_variable = global_language
		watch_selected_language = None

	if language_variable == ptbr_lang:
		function_text = "A função "
		function_text_2 = "foi executada"

	if language_variable == enus_lang:
		function_text = "The function "
		function_text_2 = "has been run"

	function_text_mix = function_text + "{} " + function_text_2 + "."

	if make_two_language_arrays == True:
		enus_script_texts_file = language_folder_to_use + language_en.upper() + ".txt"
		ptbr_script_texts_file = language_folder_to_use + language_pt.upper() + ".txt"

		read_file = Create_Array_Of_File(enus_script_texts_file)

		texts = []

		i = 0
		while i <= len(read_file) - 1:
			texts.append(read_file[i])
			enus_script_language_texts.append(read_file[i])

			i += 1

		read_file = Create_Array_Of_File(ptbr_script_texts_file)

		texts = []

		i = 0
		while i <= len(read_file) - 1:
			texts.append(read_file[i])
			ptbr_script_language_texts.append(read_file[i])

			i += 1

	language_file = language_folder_to_use + language_variable.upper() + ".txt"

	read_file = Create_Array_Of_File(language_file)

	texts = []

	i = 0
	while i <= len(read_file) - 1:
		texts.append(read_file[i])
		script_language_texts.append(read_file[i])

		i += 1

	if make_two_language_arrays == False or make_two_language_arrays == None:
		return script_language_texts

	if make_two_language_arrays == True:
		return [script_language_texts, enus_script_language_texts, ptbr_script_language_texts]

def Run_Function(function_name):
	function_was_run = False

	if function_name in functions_to_run_array:
		functions_to_run_array[function_name]()

		function_was_run = True

	if function_name not in functions_to_run_array and function_was_run == False:
		print(global_texts_can_not_find_function + ".")

def Make_Choices(choice_descriptions_array, choice_functions_array, script_name = None, extra_option = None, run = None, show_selected_text = True, double_extra_option = None, alternative_choice_list_text = None, custom_selected_text = None, alternative_array = None, export_number = None, return_choice = None, return_first_item = False, return_second_item = False, second_space = True):
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

def Choose_Function(functions, descriptions, script_name = None, alternative_choice_text = None, parameter = None, first_space = True, second_space = True):
	functions_array = [None]
	functions_array.extend(functions)

	descriptions_array = [None]
	descriptions_array.extend(descriptions)

	functions = functions_array
	descriptions = descriptions_array

	if first_space == True:
		print()

	if parameter == None:
		Make_Choices(descriptions, functions, script_name, alternative_choice_list_text = alternative_choice_text, second_space = second_space)

	if parameter != None:
		choice_info = Make_Choices(descriptions, functions, script_name, alternative_choice_list_text = alternative_choice_text, run = False, return_choice = True, export_number = True, second_space = second_space)

		choice_number = choice_info[1]

		Function = functions[choice_number]

		Function(parameter)

def Select_Choice_From_List(choices_list, script_name = None, alternative_choice_text = None, custom_selected_text = None, second_choices_list = None, return_number = False, return_first_item = False, return_second_item_parameter = False, return_first_and_second_item = False, add_none = True, show_selected_text = True, first_space = True, second_space = True):
	if add_none == True:
		local_choices_list = [None]
		local_choices_list.extend(choices_list)
		choices_list = local_choices_list

	if second_choices_list != None and add_none == True:
		local_second_choices_list = [None]
		local_second_choices_list.extend(second_choices_list)

		second_choices_list = local_second_choices_list

	if first_space == True:
		print()

	if return_first_item == True:
		return Make_Choices(choices_list, None, script_name = script_name, alternative_choice_list_text = alternative_choice_text, custom_selected_text = custom_selected_text, run = False, return_choice = True, export_number = False, extra_option = False, show_selected_text = show_selected_text, second_space = second_space)

	if return_first_item == False:
		if return_second_item_parameter == False and return_first_and_second_item == False:
			return Make_Choices(choices_list, None, script_name = script_name, alternative_choice_list_text = alternative_choice_text, custom_selected_text = custom_selected_text, run = False, return_choice = True, export_number = return_number, extra_option = True, show_selected_text = show_selected_text, second_space = second_space)

		if return_second_item_parameter == True and return_first_and_second_item == False:
			return Make_Choices(choices_list, second_choices_list, script_name = script_name, alternative_choice_list_text = alternative_choice_text, custom_selected_text = custom_selected_text, run = False, return_choice = True, export_number = return_number, extra_option = True, show_selected_text = show_selected_text, return_second_item = True, second_space = second_space)

		if return_second_item_parameter == True and return_first_and_second_item == True:
			return Make_Choices(choices_list, second_choices_list, script_name = script_name, alternative_choice_list_text = alternative_choice_text,  custom_selected_text = custom_selected_text, run = False, return_choice = True, export_number = return_number, extra_option = True, show_selected_text = show_selected_text, return_first_item = True, return_second_item = True, second_space = second_space)

	else:
		return Make_Choices(choices_list, None, script_name = script_name, alternative_choice_list_text = alternative_choice_text, custom_selected_text = custom_selected_text, run = False, return_choice = True, export_number = None, show_selected_text = show_selected_text, second_space = second_space)

def Select_Choice(choice_text_parameter, first_space = True, second_space = True, custom_text = False, enter_equals_empty = False, accept_enter = True):
	if first_space == True:
		print()

	choice_text = choice_text_parameter + ": "

	add_colon = True

	do_not_accept_text = Language_Item_Definer("The choice asker does not accept enter as a choice", "O solicitante da escolha não aceita enter como escolha")

	if custom_text == True:
		choice_text = choice_text_parameter
		add_colon = False

	if add_colon == True:
		choice_text = choice_text_parameter + ": "

	choice = input(choice_text)

	if second_space == True:
		print()

	if accept_enter == True:
		choice = str(choice)

		if choice == "" and enter_equals_empty == False:
			choice = Get_Clipboard()

		if choice == "" and enter_equals_empty == True:
			choice = ""

		if choice == "None":
			choice = None

	if accept_enter == False and choice == "" or accept_enter == False and choice == " ":
		original_choice_text = choice_text_parameter + "[](" + do_not_accept_text + "{})"

		if custom_text == False:
			original_choice_text = original_choice_text.replace("[]", " ")

		if custom_text == True:
			original_choice_text = original_choice_text.replace("[]", "").replace("(", "").replace(")", "") + ": "

		if add_colon == True:
			original_choice_text += ": "

		i = 0
		c = 0
		while choice == "" or choice == " ":
			if i == 0 or c == 0:
				choice_text = original_choice_text.format("")

			if i != 0 or c != 0:
				choice_text = original_choice_text.format(" " + str(number) + "x")

			if choice == "":
				choice_text = choice_text.replace(Language_Item_Definer("space", "espaço"), "enter")
				i += 1
				number = i

			if choice == " ":
				choice_text = choice_text.replace("enter", Language_Item_Definer("space", "espaço"))
				c += 1
				number = c

			choice = input(choice_text)

		if choice == "None":
			choice = None

		if choice != "None" and choice != "" and choice != " ":
			choice = str(choice)

	return choice

def Text_Writer(show_text, finish_text = "t", return_list = False, capitalize_lines = False, auto_add_dots = False, accept_enter = True, enumerate_lines = False, separator = " - ", stop_on_line = None, first_space = True, second_space = True, backup_file = None):
	lines_text = ""
	lines = []

	finish_text_list = []

	if finish_text != "t" and finish_text == "default_list":
		finish_text_list = ["f", "finish", "t", "terminar", "c", "completar", "acabar"]

	if first_space == True:
		print()

	enter_equals_empty = True

	if accept_enter == False:
		enter_equals_empty = False

	select_text = ""

	if enumerate_lines == True:
		select_text = "1" + separator

	if stop_on_line != None:
		stop_on_line = stop_on_line + 1

		if ":" in show_text[-1]:
			show_text = show_text.replace(":", " (" + str(stop_on_line - 1) + "):")

		else:
			show_text += " (" + str(stop_on_line - 1) + ")"

	print(show_text)

	line = ""

	line_number = 1
	while line != finish_text and line not in finish_text_list and line_number != stop_on_line:
		line = Select_Choice(str(select_text), first_space = False, second_space = False, custom_text = True, enter_equals_empty = enter_equals_empty, accept_enter = accept_enter)

		if line != finish_text and line not in finish_text_list and line_number != stop_on_line:
			if capitalize_lines == True:
				line = list(line)

				if line != []:
					line[0] = line[0].upper()

				line = "".join(line)

			if auto_add_dots == True and list(line) != [] and line[-1] not in ["?", "!", ":", ";", "."]:
				line += "."

			lines_text += line + "\n"
			lines.append(line)

			if backup_file != None:
				Append_To_File(backup_file, line, check_file_length = True)

			if select_text != "":
				select_text = str(int(select_text[0]) + 1) + separator

			line_number += 1

	if "\n" in lines_text[-1]:
		lines_text = lines_text[:-1]

	if second_space == True:
		print()

	if return_list == False:
		return lines_text

	if return_list == True:
		return lines