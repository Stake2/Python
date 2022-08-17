# Python_Module_Manager.py

# Script Helper importer
from Script_Helper import *

from Python_Module_Manager.Create_New_Module import Create_New_Module as Create_New_Module

local_script_name = "Python_Module_Manager.py"

def Function_Choose():
	functions = [
	Create_New_Module,
	]

	descriptions = [
	Language_Item_Definer("Create new module", "Criar novo módulo")
	]

	choice_text = Language_Item_Definer("Manage Python Modules", "Gerenciar Módulos de Python")

	Choose_Function(functions, descriptions, local_script_name, choice_text, second_space = False)

if __name__ == "__main__":
	Function_Choose()