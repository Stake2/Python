# Tasks.py

from Script_Helper import *

from Tasks.Register_Task import Register_Task as Register_Task
from Tasks.Register_Task_Module import Register_Task_Module as Register_Task_Module

def Function_Choose():
	functions = [
	Register_Task,
	]

	descriptions = [
	Language_Item_Definer("Register a Task", "Registrar uma Tarefa"),
	]

	choice_text = Language_Item_Definer("Manage Productive Network", "Gerenciar Rede Produtiva (Productive Network)")

	Choose_Function(functions, descriptions, local_script_name, choice_text, second_space = False)