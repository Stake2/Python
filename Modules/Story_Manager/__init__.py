# Story_Manager.py

# Script Helper importer
from Script_Helper import *

from Story_Manager.Story_Manager import Story_Manager as Story_Manager

from Story_Manager.Post_Chapter import Post_Chapter as Post_Chapter
from Story_Manager.Write_Chapter import Write_Chapter as Write_Chapter
from Story_Manager.Add_Story_To_Story_Database import Add_Story_To_Story_Database as Add_Story_To_Story_Database
from Story_Manager.List_Story_Data import List_Story_Data as List_Story_Data
from Story_Manager.Update_Chapter_Covers import Update_Chapter_Covers as Update_Chapter_Covers
from Story_Manager.Copy_Story_Names import Copy_Story_Names as Copy_Story_Names

# Script name
local_script_name = "Story_Manager.py"

def Function_Choose():
	descriptions = [
	Language_Item_Definer("Post", "Postar"),
	Language_Item_Definer("Write", "Escrever"),
	Language_Item_Definer("Add story to Story Database", "Adicionar história ao Banco de Dados de Histórias"),
	Language_Item_Definer("List story data", "Listar dados das histórias"),
	Language_Item_Definer("Update chapter covers", "Atualizar capas de capítulos"),
	Language_Item_Definer("Copy Story Names", "Copiar Nomes de História"),
	]

	functions = [
	Post_Chapter,
	Write_Chapter,
	Add_Story_To_Story_Database,
	List_Story_Data,
	Update_Chapter_Covers,
	Copy_Story_Names,
	]

	choice_text = Language_Item_Definer("Manage Stories", "Gerenciar Histórias")

	Choose_Function(functions, descriptions, local_script_name, choice_text)

if __name__ == "__main__":
	Function_Choose()