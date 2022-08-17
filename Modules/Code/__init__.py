# Code.py

# Script Helper importer
from Script_Helper import *

from Code.Help_With_Coding import Help_With_Coding as Help_With_Coding

local_script_name = "Code.py"

def Function_Choose():
	functions = [
	Help_With_Coding,
	]

	descriptions = [
	Language_Item_Definer("Help with coding", "Ajuda com a programação"),
	]

	choice_text = Language_Item_Definer("Code computer scripts", "Programar scripts de computador")

	Choose_Function(functions, descriptions, local_script_name, choice_text)

if __name__ == "__main__":
	Function_Choose()