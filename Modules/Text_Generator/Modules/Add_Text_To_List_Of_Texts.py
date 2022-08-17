import pyperclip, win32clipboard
from Script_Helper import global_yes_or_no_string, yes_array, no_array

def ATTLOT_Choose():
	global has_two_texts

	has_two_texts_choice = input(global_yes_or_no_string.format("Has two texts to add to list"))

	choice = has_two_texts_choice
	try:
		choice = str(choice)

	except TypeError:
		choice = int(choice)

	if choice in yes_array:
		has_two_texts = True

	if choice in no_array:
		has_two_texts = False

	if has_two_texts == True:
		print()
		first_left_text = str(input("Type the first text on the left: "))

		if first_left_text == "":
			first_left_text = None

		print()
		second_right_text = str(input("Type the second text on the: "))

		if second_right_text == "":
			second_right_text = None

		Add_Text_To_List_Of_Texts(first_left_text, second_right_text)

	if has_two_texts == False:
		Add_Text_To_List_Of_Texts()

def Add_Text_To_List_Of_Texts(first_left_text = None, second_right_text = None):
	win32clipboard.OpenClipboard()
	clipboard_data = win32clipboard.GetClipboardData()
	win32clipboard.CloseClipboard()

	clipboard_data = clipboard_data.splitlines()

	first_run = False

	for line in clipboard_data:
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

		line = left_text_to_use + line + right_text_to_use + "\n"

		clipboard_data.append(line)

	string_to_copy = ""

	for line in clipboard_data:
		string_to_copy += line

	pyperclip.copy(string_to_copy)