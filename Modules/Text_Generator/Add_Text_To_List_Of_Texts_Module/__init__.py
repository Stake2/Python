# Add_Text_To_List_Of_Texts.py

import pyperclip, win32clipboard
from Script_Helper import global_yes_or_no_string, yes_array, no_array, Yes_Or_No_Definer, Get_Clipboard, Select_Choice, Make_Choices, Language_Item_Definer

sides_array = [
None,
"Left",
"Right",
]

left = sides_array[1]
right = sides_array[2]

def ATTLOT_Choose():
	global has_two_texts
	global separator
	global has_separator

	has_two_texts = Yes_Or_No_Definer("Has two texts to add to list", first_space = False)

	is_array = Yes_Or_No_Definer("Add to array", first_space = False)

	has_separator = False

	if is_array == True:
		has_separator = Yes_Or_No_Definer("Has separator", first_space = False)

		if has_separator == True:
			separator = Select_Choice("Please type the separator", first_space = False)

	if has_two_texts == True:
		first_left_text = str(input("Type the first text on the left: "))

		if first_left_text == "":
			first_left_text = None

		print()
		second_right_text = str(input("Type the second text on the right: "))

		if second_right_text == "":
			second_right_text = None

		Add_Text_To_List_Of_Texts(first_left_text, second_right_text, append_array = is_array)

	if has_two_texts == False:
		Add_Text_To_List_Of_Texts(append_array = is_array)

def Add_Text_To_List_Of_Texts(first_left_text = None, second_right_text = None, append_array = None):
	global local_script_name

	local_script_name = "Add_Text_To_List_Of_Texts.py"

	if append_array == True:
		side = Make_Choices(sides_array, sides_array, '"' + local_script_name + '"', extra_option = None, run = False, show_selected_text = None, double_extra_option = None, alternative_choice_list_text = "Select the side of the array that you want to add text to", alternative_array = None, export_number = None, return_choice = True)

	text_to_add_to = Select_Choice("Press enter to paste the origin text from clipboard", first_space = False).splitlines()

	first_run = False

	if append_array == True:
		array_to_add_to_text = Select_Choice("Press enter to paste the array to be added to the text from clipboard", first_space = False).splitlines()

	i = 0
	for line in text_to_add_to:
		if first_run == False:
			clipboard_data = []

			first_run = True

		if has_two_texts == True:
			left_text_to_use = first_left_text
			right_text_to_use = second_right_text

		if first_left_text == None and second_right_text == None:
			left_text_to_use = '"'
			right_text_to_use = '",'

		if first_left_text != None and second_right_text == None:
			left_text_to_use = first_left_text
			right_text_to_use = ""

		if first_left_text == None and second_right_text != None:
			left_text_to_use = ""
			right_text_to_use = second_right_text

		if append_array == True:
			if has_separator == True:
				separator_to_use = separator

			if has_separator == False:
				separator_to_use = ""

			if side == left:
				left_text_to_use = array_to_add_to_text[i] + separator_to_use
				right_text_to_use = ""

			if side == right:
				left_text_to_use = ""
				right_text_to_use = separator_to_use + array_to_add_to_text[i]

		if i == len(text_to_add_to) - 1:
			space_variable = ""

		if i != len(text_to_add_to) - 1:
			space_variable = "\n"

		line = left_text_to_use + line + right_text_to_use + space_variable

		clipboard_data.append(line)

		i += 1

	string_to_copy = ""

	for line in clipboard_data:
		string_to_copy += line

	pyperclip.copy(string_to_copy)