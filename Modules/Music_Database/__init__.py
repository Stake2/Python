# Music_Database.py

# Script Helper importer
from Script_Helper import *

from Music_Database.Update_Database import Update_Database as Update_Database

local_script_name = "Music_Database.py"

def Function_Choose():
	functions = [
	Update_Database,
	]

	descriptions = [
	Language_Item_Definer("Update database", "Atualizar Banco de Dados"),
	]

	choice_text = Language_Item_Definer("Register info about music, artists, and sountracks in the Mega Music folder", "Registrar informações sobre música, artistas, e trilhas sonoras na pasta de Músicas do Mega")

	Choose_Function(functions, descriptions, local_script_name, choice_text)

if __name__ == "__main__":
	Function_Choose()