'''

Program a Python script that gives the user a list of strings:
"Fiquei {} enquanto {}."
"Fiquei conversando com {} enquanto {}."

And let the user select one of the strings.
Then asks for the user to type the first and second text.
After that, it formats the selected string.
And prints the formatted string to the console, it also copies it to the clipboard with the pyperclip module.
The script also has to print what it is doing at the time of execution, the print is active when the verbose variable is True.
The script must be done in English and translated into Portuguese using the "Language" folder and the "Set_Language()" function of the Script_Helper.py script.

'''

from Script_Helper import *
import pyperclip

verbose = True

if verbose == True:
	print('Defining the "script_name" and "strings_to_format_array" variables...')

script_name = "Format And Copy Text String.py"

strings_to_format_array = [
None,
"Fiz um {} e um {} para comer enquanto assisto {}",
]

if verbose == True:
	print("Showing list of text strings to be formatted...")

print()
string_choice = Make_Choices(strings_to_format_array, strings_to_format_array, '"' + script_name + '"', extra_option = None, run = False, show_selected_text = None, double_extra_option = None, alternative_choice_list_text = None, alternative_array = None, export_number = False, return_choice = True)

if verbose == True:
	print("Splitting the selected text string into two parts by finding the {} in the text strings...")
	print()

input_texts = string_choice.split("{}")

if verbose == True:
	print("Defining the two separated text strings as first_input_text and second_input_text...")
	print("Replacing the spaces on the two variables mentioned above...")
	print()

first_input_text = input_texts[0].replace("um ", "um")
second_input_text = input_texts[1].replace("um ", "um")
second_input_text = second_input_text.replace(" e", "e")
third_input_text = input_texts[2].replace("assisto ", "assisto")
third_input_text = third_input_text.replace(" para", "para")

if verbose == True:
	print("Asking for two texts to use to format the selected text string...")
	print()

first_text = str(input(first_input_text + ": "))
second_text = str(input(second_input_text + ": "))
third_text = str(input(third_input_text + ": "))

print()

if verbose == True:
	print("Formatting the text string...")
	print()

string_choice_formatted = string_choice.format(first_text, second_text, third_text) + "."

if verbose == True:
	print("Showing the formatted string on the console...")
	print()

print("The formatted string is: ")
print(string_choice_formatted)

if verbose == True:
	print()
	print("Copying the text string to the clipboard...")

pyperclip.copy(string_choice_formatted)

'''
from translate import Translator

translator = Translator(from_lang="english", to_lang="portuguese")
hello_translated_ptbr = translator.translate("Hello")

print(hello_translated_ptbr)
'''