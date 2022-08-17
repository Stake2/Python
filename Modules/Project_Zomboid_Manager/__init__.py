# Project_Zomboid_Manager.py

# Script Helper importer
from Script_Helper import *

from Project_Zomboid_Manager.Create_New_Character_Diary_Text_File import Create_New_Character_Diary_Text_File as Create_New_Character_Diary_Text_File

local_script_name = "Project_Zomboid_Manager.py"

def Function_Choose():
	functions = [
	Create_New_Character_Diary_Text_File,
	]

	descriptions = [
	Language_Item_Definer("Create new character diary text file", "Criar novo arquivo de texto de diário de personagem"),
	]

	choice_text = Language_Item_Definer("", "Gerenciador de Project Zomboid")

	Choose_Function(functions, descriptions, local_script_name, choice_text)

if __name__ == "__main__":
	Function_Choose()