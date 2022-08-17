# Diary.py

from Script_Helper import *

from Diary.Write_On_Diary import Write_On_Diary as Write_On_Diary
from Diary.Create_New_Diary_Chapter import Create_New_Diary_Chapter as Create_New_Diary_Chapter

local_script_name = "Diary.py"

def Function_Choose():
	functions = [
	Write_On_Diary,
	Create_New_Diary_Chapter,
	]

	descriptions = [
	Language_Item_Definer("Write on Diary", "Escrever no Diário"),
	Language_Item_Definer("Create new Diary chapter", "Criar novo capítulo do Diário"),
	]

	select_function_text = Language_Item_Definer("Select a {} function to execute", "Selecione uma função do {} para executar")
	choice_text = select_function_text.format(Language_Item_Definer("Diary", "Diário"))

	Choose_Function(functions, descriptions, local_script_name, choice_text, second_space = False)

if __name__ == "__main__":
	Function_Choose()