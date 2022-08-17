# Unified_Remote_Manager.py

# Script Helper importer
from Script_Helper import *

from Unified_Remote_Manager.Add_Python_Apps_To_Remote import Add_Python_Apps_To_Remote as Add_Python_Apps_To_Remote

local_script_name = "Unified_Remote_Manager.py"

def Function_Choose():
	functions = [
	Add_Python_Apps_To_Remote,
	]

	descriptions = [
	Language_Item_Definer("Add Python apps to remote", "Adicionar aplicativos Python ao remote"),
	]

	choice_text = Language_Item_Definer("Manage Unified Remote", "Gerenciar Unified Remote")

	Choose_Function(functions, descriptions, local_script_name, choice_text)

Add_Python_Apps_To_Remote()