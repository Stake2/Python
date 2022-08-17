# Study.py

# Script Helper importer
from Script_Helper import *

from Study.Help_With_Studying import Help_With_Studying as Help_With_Studying

local_script_name = "Study.py"

def Function_Choose():
	functions = [
	Help_With_Studying,
	]

	descriptions = [
	Language_Item_Definer("Help with studying", "Ajuda nos estudos"),
	]

	choice_text = Language_Item_Definer("Study courses", "Estudar cursos")

	Choose_Function(functions, descriptions, choice_text)

if __name__ == "__main__":
	Function_Choose()