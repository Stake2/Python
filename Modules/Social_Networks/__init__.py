# Social_Networks.py

# Script Helper importer
from Script_Helper import *

from Social_Networks.Open_Social_Network import Open_Social_Network as Open_Social_Network

def Function_Choose():
	functions = [
		Open_Social_Network,
	]

	descriptions = [
		Language_Item_Definer("Open Social Network", "Abrir Rede Social"),
	]

	choice_text = Language_Item_Definer("Manage Social Networks", "Gerenciar Redes Sociais")

	Choose_Function(functions, descriptions, alternative_choice_text = choice_text)

if __name__ == "__main__":
	Function_Choose()