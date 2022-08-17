# Diary_Slim.py

from Script_Helper import *

from Diary_Slim.Create_New_Diary_Slim import Create_New_Diary_Slim as Create_New_Diary_Slim
from Diary_Slim.Write_On_Diary_Slim import Write_On_Diary_Slim as Write_On_Diary_Slim

class Function_Choose():
	def __init__(self):
		self.Select_Diary_Slim_Function()

	def Select_Diary_Slim_Function(self):
		self.functions = [
		Create_New_Diary_Slim,
		Write_On_Diary_Slim,
		]

		self.descriptions = [
		Language_Item_Definer("Create new Diary Slim", "Criar novo Diário Slim"),
		Language_Item_Definer("Write on Diary Slim", "Escrever no Diário Slim"),
		]

		select_function_text = Language_Item_Definer("Select a {} function to execute", "Selecione uma função do {} para executar")
		choice_text = select_function_text.format(Language_Item_Definer("Diary Slim", "Diário Slim"))

		Choose_Function(self.functions, self.descriptions, local_script_name, choice_text)