from Folder_Lister import *
import subprocess
import webbrowser
import win32clipboard
import win32com.client
import psutil
import pyperclip
import datetime
import time

global_yes_choice_texts = [
None,
1,
"1",
"yes",
"Yes",
"y",
"Y",
"sim",
"Sim",
"s",
"S",
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
]

def Define_Yes_Or_No(value):
	value = str(value)

	if value in global_yes_choice_texts:
		value = True

	if value in global_no_choice_texts:
		value = False

	return value

def Get_Clipboard():
	win32clipboard.OpenClipboard()
	clipboard_data = win32clipboard.GetClipboardData()
	win32clipboard.CloseClipboard()

	return clipboard_data

def Copy_Text(text):
	pyperclip.copy(text)

def Lower_Text(text):
	return text.lower()

def Replace_Space_By_Underline(text):
	return text.replace(" ", "_")

def Replace_Space_By_Dash(text):
	return text.replace(" ", "-")

def Remove_Dot(text):
	return text.replace(".", "")

def Remove_Duplicates(list_):
	return list(dict.fromkeys(list_))

def range_one(start, end):
	return range(start, end + 1)

def Split_And_Add_Text(text, separator = " - ", new_separator = ": "):
	if separator in text:
		string = ""

		i = 0
		split = text.split(separator)
		for item in split:
			string += item

			if item != split[-1]:
				if type(new_separator) == dict:
					found_number = False
					for number in new_separator:
						if i == number:
							string += new_separator[number]

							found_number = True

					if found_number == False:
						string += new_separator[0]

				if type(new_separator) != dict:
					string += new_separator

			i += 1

		text = string

	return text

def Text_Replacer(text_to_use = None, text_to_replace = None, replace_with = None, copy_text = None, ask = None):
	if text_to_use == None:
		text_to_use = Select_Choice("Type the text to use", second_space = False)

	if text_to_replace == None:
		text_to_replace = Select_Choice("Type the text to replace", second_space = False)

	if replace_with == None and ask == True:
		replace_with = Select_Choice("Type the text to put in place of the text to replace", second_space = False)

	if replace_with == None and ask == False:
		text_to_use = text_to_use.replace(text_to_replace, "")

	if replace_with != None:
		text_to_use = text_to_use.replace(text_to_replace, replace_with)

	text_to_use = str(text_to_use)

	if copy_text == True:
		copy(text_to_use)

	else:
		return text_to_use

def Sanitize_File_Path(file_path_to_sanitize = None, add_file = None, copy_text = None):
	if file_path_to_sanitize == None:
		file_path_to_sanitize = Select_Choice("Type the file path to sanizite")

	file_path_to_sanitize = Text_Replacer(file_path_to_sanitize, text_to_replace = "\\", replace_with = "/")

	if "/" not in file_path_to_sanitize[-1]:
		file_path_to_sanitize += "/"

	if add_file == True:
		sanizited_file_path = Text_Replacer(file_path_to_sanitize, " ", "%20")
		sanizited_file_path = "file:///" + sanizited_file_path

	if copy_text == True:
		print("New file path: " + file_path_to_sanitize)

	if copy_text == True:
		copy(sanizited_file_path)

	else:
		return file_path_to_sanitize

def Define_Array(array_to_define):
	global selected_array
	global array_length

	selected_array = array_to_define
	array_length = len(array_to_define) - 1

	return selected_array, array_length

def o(file, mode, encoding = "utf8"):
	return open(file, mode, encoding = encoding)

def Read_Lines(file, custom_encoding = "utf8"):
	return o(file, "r", encoding = custom_encoding).readlines()

def Read_String(file, custom_encoding = "utf8"):
	return o(file, "r", encoding = custom_encoding).read()

def Write(file, text, mode, global_switches):
	if global_switches == None:
		write_to_file = o(file, mode)
		write_to_file.write(text)
		write_to_file.close()

	else:
		if "verbose" in global_switches and global_switches["verbose"] == True:
			print()
			print("-----")
			print()
			print("File: " + file)

			if type(text) == str:
				if "\n" not in text:
					print("Text: " + text)

				if "\n" in text:
					print("Text:")
					print("[" + text + "]")

			if type(text) == list:
				print("Text:")
				print(text)

		if global_switches["write_to_file"] == True:
			write_to_file = o(file, mode)
			write_to_file.write(text)
			write_to_file.close()

def Append_To_File(file, text, global_switches = None, check_file_length = None):
	mode = "a"

	file_length = len(Read_Lines(file))

	space_variable = ""

	if check_file_length == True:
		if file_length != 0:
			space_variable = "\n"

	text = space_variable + text

	Write(file, text, mode, global_switches)

def Write_To_File(file, text, global_switches = None):
	mode = "w"

	Write(file, text, mode, global_switches)

def Create_Array_Of_File(file, add_none = False, double_empty_lines = False, custom_encoding = "utf8"):
	verbose = False

	if is_a_file(file) == True:
		result = Read_Lines(file, custom_encoding = custom_encoding)

		if add_none == False:
			array_to_return = []

		if add_none == True:
			array_to_return = [None]

		if verbose == True:
			print(double_empty_lines)

		i = 1
		for line in result:
			if double_empty_lines == False:
				line = line.replace("\n", "")

			if double_empty_lines == True:
				if line == "":
					line = "\n\n"

					if verbose == True:
						print(line)

				if "\n" in line and "\r\n" not in line:
					line = line.replace("\n", "\n\n")

				if "\r\n" in line:
					line = line.replace("\r\n", "\r\n\r\n")

				if verbose == True:
					print(str(i) + " - " + line)

			array_to_return.append(line)

			i += 1

		return array_to_return

	if is_a_file(file) == False:
		print()
		print("-----")
		print()
		print("Este arquivo não foi encontrado:")
		print(file)
		print()
		print("Você provavelmente está executando este script em modo de teste, então o arquivo não pôde ser criado.")
		print("Desative o modo de teste para que o script funcione corretamente.")
		print('Mude a variável testing_script na classe raíz deste script para False: "self.testing_script = False".')
		print()
		print("-----")
		quit()

def Replace_In_Array(array_of_file, text_to_replace, replace_with = None, read_file = False, add_none = False, Reader = None, double_empty_lines_parameter = False):
	if read_file == True:
		if Reader == Read_Lines:
			array_of_file = Reader(array_of_file)

		if Reader == Create_Array_Of_File:
			array_of_file = Reader(array_of_file, add_none, double_empty_lines = double_empty_lines_parameter)

	if replace_with == None:
		replace_with = ""

	array = []

	for item in array_of_file:
		if item != None:
			item = item.replace(text_to_replace, replace_with)

			array.append(item)

	return array

def Print_Lines(lines, remove_none = False):
	if remove_none == True:
		new_array = []
		new_array.extend(lines)
		new_array.pop(0)

		lines = new_array

	i = 0
	while i <= len(lines) - 1:
		print(lines[i])

		i += 1

def Stringfy_Array(array, add_line_break = False, custom_separator = None):
	string_to_return = ""

	for text in array:
		if text != None:
			string_to_return += text

			if text != array[-1]:
				if add_line_break == True:
					string_to_return += "\n"

				if custom_separator != None:
					string_to_return += custom_separator

	return string_to_return

def Stringfy_Dict(dict, add_line_break = True, add_colon = True):
	dict_keys = list(dict.keys())
	dict_values = list(dict.values())

	string_to_return = ""

	i = 0
	for value in dict_values:
		key = dict_keys[i]

		string_to_return += key

		if add_colon == True:
			string_to_return += ": "

		string_to_return += value

		if key != dict_keys[-1] and add_line_break == True:
			string_to_return += "\n"

		i += 1

	return string_to_return

def Convert_Array_Item_Type(array, type_ = str):
	i = 0
	for item in array:
		array[i] = type_(item)

		i += 1

	return array

def Open_Link(link):
	webbrowser.open(link)

def Close_Program(program_name):
	for process in (process for process in psutil.process_iter() if program_name.split("\\")[program_name.count("\\")] in process.name()):
		process.kill()

def Language_Item_Definer_2(global_language_parameter, item_enus, item_ptbr):
	language_en = "en"
	full_language_en = "English"

	language_pt = "pt"
	full_language_pt = "Português"

	if global_language_parameter == language_en or global_language_parameter == full_language_en:
		item = item_enus

	if global_language_parameter == language_pt or global_language_parameter == full_language_pt:
		item = item_ptbr

	return item

def Add_Leading_Zeros(number):
	number = int(number)

	if number <= 9:
		number = str("0" + str(number))

	return number

def Remove_Leading_Zeros(number):
	if int(number) <= 9 and "0" in str(number):
		number = str(number)[1:]

	return number

def Check_If_Number_Is_Plural(number):
	if number <= 1:
		is_plural = False

	if number >= 2:
		is_plural = True

	return is_plural

def Define_Text_By_Text(text_to_use, singular_text, plural_text):
	if "s" not in text_to_use[-1]:
		return singular_text

	if "s" in text_to_use[-1]:
		return plural_text

def Change_Number(number, action, action_quantity = 1):
	number = int(number)

	more = "more"
	less = "less"

	if action == more:
		return str(number + action_quantity)

	if action == less:
		return str(number - action_quantity)

def Define_Text_By_Number(number, singular_text, plural_text):
	if Check_If_Number_Is_Plural(number) == False:
		defined_text = singular_text

	if Check_If_Number_Is_Plural(number) == True:
		defined_text = plural_text

	return defined_text

def Remove_Non_File_Characters(file, custom_replace_list = None):
	replace_list = [
	":",
	"?",
	"\"",
	"\\",
	"/",
	"|",
	"*",
	"<",
	">",
	]

	if custom_replace_list != None:
		replace_list = custom_replace_list

	for text in replace_list:
		if text in file:
			file = file.replace(text, "")

	if " " in file.split("/")[len(file.split("/")) - 1][0]:
		file_name = file.split("/")[len(file.split("/")) - 1][1:]
		folder = file.split("/")
		folder.pop(-1)
		folder = "/".join(folder) + "/"

		file = folder + file_name

	return file

def Remove_Value_From_Array(array, remove):
	i = 0
	for value in array:
		if value != None:
			if remove in value:
				array.pop(i)

		i += 1

def Add_To_Dict_With_Key(dict_variable, keys, values):
	i = 0
	while i <= len(values) - 1:
		current_key = keys[i]
		current_values = values[i]

		dict_variable[current_key] = current_values

		i += 1

def For_Append(source_array, append_array, value = None, Function = None, function_parameter = None):
	for item in source_array:
		if Function == None:
			if value == None:
				append_array.append(item)

			if value != None:
				append_array.append(value)

		if Function != None and value == None:
			if function_parameter == None:
				append_array.append(Function(item))

			if function_parameter != None:
				append_array.append(Function(item, function_parameter))

def For_Append_With_Key(keys_array, append_array, value = None, value_string = None, append_entire_array = False, number_of_key_arrays = None, remove = None, pop_none = False):
	verbose = False
	is_array = False
	multiple_key_arrays = False

	new_array = []
	new_array.extend(keys_array)

	if pop_none == True:
		new_array.pop(0)

	if type(value) == list:
		is_array = True

	if verbose == True:
		print()
		print("Value: ")
		print(value)
		print()
		print("Value String: ")
		print(value_string)

	if number_of_key_arrays != None:
		number_of_key_arrays = number_of_key_arrays - 1

		key_array_one = new_array[0]
		key_array_two = new_array[1]

		multiple_key_arrays = True

	if multiple_key_arrays == False:
		i = 0
		for key in new_array:
			if value_string != None:
				if remove != None:
					value_string = value_string.replace(remove, "")

				append_array[key] = value_string.format(key)

			if value != None:
				if is_array == True and append_entire_array == False:
					if remove != None:
						value[i] = value[i].replace(remove, "")

					append_array[key] = value[i]

				if is_array == True and append_entire_array == True:
					if remove != None:
						value = value.replace(remove, "")

					append_array[key] = value

				if is_array == False:
					if remove != None:
						value = value.replace(remove, "")

					append_array[key] = value

			i += 1

	if multiple_key_arrays == True:
		i = 0
		for key in key_array_one:
			if value_string != None:
				if remove != None:
					value_string = value_string.replace(remove, "")

				second_key = key_array_two[i]

				if remove != None and second_key != None:
					second_key = second_key.replace(remove, "")

				append_array[key] = value_string.format(key, second_key)

			i += 1

def Replace_Setting_Text(array, line_number, text):
	return array[line_number].replace(text, "")

def Return_Setting_Name_And_Value(setting_line, setting_splitter):
	split = setting_line.split(setting_splitter)

	setting = split[0]

	value = split[setting_line.count(setting_splitter)]

	if setting_line.count(setting_splitter) == 2:
		value = split[1] + setting_splitter + value

	if setting_line.count(setting_splitter) >= 3:
		split.pop(0)
		value = ""

		for item in split:
			value += item

			if item != split[-1]:
				value += setting_splitter

	return [setting, value]

def Make_Setting_Dictionary(settings_list, setting_splitter = ": ", convert_to = None, define_yes_or_no = False, define_true_or_false = False, read_file = False, return_three_lists = False):
	settings = {}

	if read_file == True:
		settings_list = Create_Array_Of_File(settings_list)

	if return_three_lists == True:
		setting_names = []
		setting_values = []

	for setting_line in settings_list:
		setting, value = Return_Setting_Name_And_Value(setting_line, setting_splitter)

		if define_yes_or_no == True:
			value = Define_Yes_Or_No(value)

		if define_true_or_false == True:
			value = Define_True_Or_False(value)

		if convert_to != None:
			value = convert_to(value)

		settings[setting] = value

		if return_three_lists == True:
			setting_names.append(setting)
			setting_values.append(value)

	if return_three_lists == False:
		return settings

	if return_three_lists == True:
		return [settings, setting_names, setting_values]

def Capitalize_First_Letter(text):
	text = list(text)
	text[0] = text[0].upper()
	text = "".join(text)

	return text

Create_Array_Of_File = Create_Array_Of_File

def Get_Function_Name(function, replace_underline = False, lower = False, title = False, capitalize = False):
	function_name = function.__name__

	if replace_underline == True:
		function_name = function_name.replace("_", " ")

	if lower == True:
		function_name = function_name.lower()

	if title == True:
		function_name = function_name.title()

	if capitalize == True:
		function_name = function_name.capitalize()

	return function_name

def Get_File_Encoding(file):
	"""
	Get the encoding type of a file
	:param file: file path
	:return: str - file encoding type
	"""

	with open(file) as src_file:
		return src_file.encoding

def Get_File_Encoding_Chardet(file):
	"""
	Get the encoding of a file using chardet package
	:param file_path:
	:return:
	"""

	import chardet

	with open(file, "rb") as f:
		result = chardet.detect(f.read())
		return result["encoding"]

def Define_True_Or_False(value):
	true_array = [
	"True",
	"true",
	]

	false_array = [
	"False",
	"false",
	]

	if value in true_array:
		value = True

	if value in false_array:
		value = False

	return value

def Dict_Print(dict, new_line_title = True, space_separator = True, first_space = True, second_space = True):
	if new_line_title == True:
		string_format = "{}:\n{}"

	if new_line_title == False:
		string_format = "{}: {}"

	if first_space == True:
		print()

	for key in dict:
		print(string_format.format(key, dict.get(key)))

		if space_separator == True and key != list(dict)[-1]:
			print()

	if second_space == True:
		print()

def Split_Text_And_Backup(text, splitter, number = 0):
	text_backup = text

	if splitter in text:
		text = text.split(splitter)[number]

	return text_backup, text

def Split_Text_By_Language(global_language, text, custom_language_number = None):
	text = text.split(", ")

	if custom_language_number == None:
		text = text[Language_Item_Definer_2(global_language, 0, 1)]

	if custom_language_number != None:
		text = text[custom_language_number]

	return text

def Add_Years_To_Array(array, mode = None, add_mode = "list", format_string = None, custom_year_variable = None, less_one = False):
	now_2 = datetime.datetime.now()
	current_year = str(now_2.year)

	year_variable = 2018

	if custom_year_variable != None:
		year_variable = custom_year_variable

	local_current_year = current_year

	if less_one == True:
		local_current_year = str(int(local_current_year) - 1)

	while year_variable <= int(local_current_year):
		if mode == str:
			year_variable_to_use = str(year_variable)

		if mode == int:
			year_variable_to_use = int(year_variable)

		year_variable_backup = year_variable_to_use

		if format_string != None:
			year_variable_to_use = format_string.format(year_variable_to_use)

		if add_mode == "list":
			array.append(year_variable_to_use)

		if add_mode == "dict":
			array[year_variable_backup] = year_variable_to_use

		year_variable += 1

def Make_Time_Text(time_string, language, add_original_time = False):
	time_string = time_string.split(":")
	hour = time_string[0]
	minute = time_string[1]
	second = time_string[2]

	language_en = "enus"
	language_pt = "ptbr"

	hour_text = ""

	has_hours = False

	if hour != "0":
		hour_text = Define_Text_By_Number(int(hour), Language_Item_Definer_2(language, "hour", "hora"), Language_Item_Definer_2(language, "hours", "horas"))
		has_hours = True

	minute_text = ""

	has_minutes = False

	if minute != "00":
		minute_text = Define_Text_By_Number(int(minute), Language_Item_Definer_2(language, "minute", "minuto"), Language_Item_Definer_2(language, "minutes", "minutos"))
		has_minutes = True

	second_text = ""

	has_seconds = False

	if second != "00":
		second_text = Define_Text_By_Number(int(second), Language_Item_Definer_2(language, "second", "segundo"), Language_Item_Definer_2(language, "seconds", "segundos"))
		has_seconds = True

	time_text = ""

	if has_hours == True:
		time_text += Remove_Leading_Zeros(hour) + " " + hour_text

	if has_hours == True and has_minutes == True:
		time_text += ", "

	if has_minutes == True:
		time_text += Remove_Leading_Zeros(minute) + " " + minute_text

	if has_minutes == True and has_seconds == True:
		time_text += ", "

	if has_seconds == True:
		time_text += Remove_Leading_Zeros(second) + " " + second_text

	if add_original_time == True:
		time_text += " " + "("

		if has_hours == True:
			time_text += str(Add_Leading_Zeros(hour)) + ":"

		if has_minutes == True:
			time_text += str(Add_Leading_Zeros(minute)) + ":"

		if has_seconds == True:
			time_text += str(Add_Leading_Zeros(second))

		time_text += ")"

	return time_text

def Make_Time_Difference(file_to_write, first_time = True, language = "", input_text = "", show_texts = True):
	Create_Text_File(file_to_write)

	if first_time == True:
		before = str(datetime.datetime.now())[:-7][11:]
		Write_To_File(file_to_write, str(before))
		before = datetime.datetime.strptime(before, '%H:%M:%S')

	if first_time == False:
		before = Create_Array_Of_File(file_to_write)[0]
		before = datetime.datetime.strptime(before, '%H:%M:%S')

	current_time = datetime.datetime.now()

	if show_texts == True:
		print(Language_Item_Definer_2(language, "Now", "Agora") + ": " + str(current_time)[:-7][11:])
		print(Language_Item_Definer_2(language, "Waiting for some time", "Esperando por algum tempo") + "...")

	print()

	if input_text == "":
		input_text = Language_Item_Definer_2(language, "Press any key to stop waiting", "Pressione qualquer tecla para parar de esperar")

	input(input_text + ": ")

	time_difference_now = datetime.datetime.now() - current_time

	now_now = datetime.datetime.now()

	now_time = datetime.datetime(now_now.year, now_now.month, now_now.day, hour = now_now.hour, minute = now_now.minute, second = now_now.second)

	time_difference = now_time - before
	time_difference_now_and_then = str(time_difference_now + time_difference).split(", ")[1][:-7]

	before = str(before).split(" ")[1]

	if show_texts == True:
		print()
		print(Language_Item_Definer_2(language, "Before", "Antes") + ": " + before)
		print(Language_Item_Definer_2(language, "Now", "Agora") + ": " + str(now_time)[11:])
		print(Language_Item_Definer_2(language, "Time difference", "Diferença de tempo") + ": " + str(time_difference).split(", ")[1])
		print(Language_Item_Definer_2(language, "Current writing time", "Tempo de escrita atual") + ": " + str(time_difference_now)[:-7])
		print(Language_Item_Definer_2(language, "Total time", "Tempo total") + ": " + time_difference_now_and_then)

	difference_time_text = Make_Time_Text(str(time_difference).split(", ")[1], language, add_original_time = True)

	total_time_text = ""

	if first_time == False:
		total_time_text = Make_Time_Text(str(time_difference_now_and_then), language, add_original_time = True)

	Write_To_File(file_to_write, before + "\n" + time_difference_now_and_then)

	return difference_time_text, total_time_text, str(time_difference_now)[:-7]

Time_Jumper = Make_Time_Difference

def Stopwatch(show_text, language = "", show_current_time = True, show_stopwatch_text = True, make_backup = True, backup_file = "Script Text Files/Time Backup.txt"):
	language_en = "enus"
	full_language_en = "English"

	language_pt = "ptbr"
	full_language_pt = "Português Brasileiro"

	full_languages_not_none = [
	"English",
	"Português Brasileiro",
	]

	time_texts = {
		full_language_en: {
			"hour": "hour",
			"hours": "hours",
			"minute": "minute",
			"minutes": "minutes",
		},

		full_language_pt: {
			"hour": "hora",
			"hours": "horas",
			"minute": "minuto",
			"minutes": "minutos",
		}
	}

	if make_backup == True:
		Create_Text_File(backup_file)

	has_hours = False

	verbose = False

	hours = 0
	minutes = 0

	time_to_wait = 60

	while minutes <= 54000:
		now_time = time.strftime("%H:%M %d/%m/%Y")

		minutes_array = Define_Text_By_Number(minutes, 
		{full_language_en: time_texts[full_language_en]["minute"], full_language_pt: time_texts[full_language_pt]["minute"]},
		{full_language_en: time_texts[full_language_en]["minutes"], full_language_pt: time_texts[full_language_pt]["minutes"]})

		if hours <= 1:
			hours_array = {
			full_language_en: time_texts[full_language_en]["hour"],
			full_language_pt: time_texts[full_language_pt]["hour"],
			}

		if hours > 2:
			hours_array = {
			full_language_en: time_texts[full_language_en]["hours"],
			full_language_pt: time_texts[full_language_pt]["hours"],
			}

		has_minutes = False

		hours_text = str(hours)

		if hours == 0:
			hours_text = "0"

		minutes_text = str(minutes)

		if minutes == 0:
			minutes_text = "00"

		time_text = {}

		time_text[full_language_en] = Make_Time_Text(hours_text + ":" + minutes_text + ":00", full_language_en, add_original_time = False)
		time_text[full_language_pt] = Make_Time_Text(hours_text + ":" + minutes_text + ":00", full_language_pt, add_original_time = False)

		if hours > 0:
			hours_texts = {}

			for language in full_languages_not_none:
				hours_texts[language] = time_text[language]

			array_to_use = hours_texts

			has_minutes = True
			has_hours = True

		else:
			if minutes != 0:
				minutes_texts = {}

				for language in full_languages_not_none:
					minutes_texts[language] = time_text[language]

				array_to_use = minutes_texts

				has_minutes = True

		if has_minutes == True:
			if show_current_time == True:
				stopwatch_time_text = show_text.format(array_to_use[Language_Item_Definer_2(full_language_en, full_language_pt, language)], now_time)

			else:
				stopwatch_time_text = show_text.format(array_to_use[Language_Item_Definer_2(full_language_en, full_language_pt, language)])

		if minutes == 60:
			minutes = 0
			hours += 1

		if has_minutes == True and make_backup == True:
			text_to_write = stopwatch_time_text + "\n" + time_text[full_language_en] + "\n" + time_text[full_language_pt] + "\n"

			if has_hours == True:
				text_to_write += str(hours_texts[full_language_en]) + "\n" + str(hours_texts[full_language_pt]) + "\n"
				text_to_write += str(minutes_texts[full_language_en]) + "\n" + str(minutes_texts[full_language_pt])

			Write_To_File(backup_file, text_to_write)

		minutes += 1

		time.sleep(time_to_wait)

		if has_minutes == True:
			if show_stopwatch_text == True:
				print()	
				print(stopwatch_time_text)

			yield {
			"Stopwatch time text": stopwatch_time_text,
			"Time text": time_text,
			"Current time": now_time,
			}

def Create_Scheduled_Task(task_name, path, time_from_now = 5):
	scheduler = win32com.client.Dispatch("Schedule.Service")
	scheduler.Connect()
	root_folder = scheduler.GetFolder("\\Stake2")
	task_def = scheduler.NewTask(0)

	# Create trigger
	start_time = datetime.datetime.now() + datetime.timedelta(minutes = time_from_now)
	TASK_TRIGGER_TIME = 1
	trigger = task_def.Triggers.Create(TASK_TRIGGER_TIME)
	trigger.StartBoundary = start_time.isoformat()

	# Create action
	TASK_ACTION_EXEC = 0
	action = task_def.Actions.Create(TASK_ACTION_EXEC)
	action.ID = task_name.title()
	action.Path = path

	# Set parameters
	task_def.RegistrationInfo.Description = task_name
	task_def.Settings.Enabled = True
	task_def.Settings.StopIfGoingOnBatteries = False

	# Register task
	# If task already exists, it will be updated
	TASK_CREATE_OR_UPDATE = 6
	TASK_LOGON_NONE = 0
	root_folder.RegisterTaskDefinition(
		task_name, # Task name
		task_def,
		TASK_CREATE_OR_UPDATE,
		"", # No user
		"", # No password
		TASK_LOGON_NONE
	)