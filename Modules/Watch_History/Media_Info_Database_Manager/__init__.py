# Media_Info_Database_Manager.py

from Watch_History.Media_Info_Database_Manager.Create_New_Media_Info_Entry import Create_New_Media_Info_Entry as Create_New_Media_Info_Entry
from Watch_History.Media_Info_Database_Manager.Open_Data_File_Of_Media import Open_Data_File_Of_Media as Open_Data_File_Of_Media
from Watch_History.Media_Info_Database_Manager.Fill_Episode_Titles_File import Fill_Episode_Titles_File as Fill_Episode_Titles_File
from Watch_History.Media_Info_Database_Manager.Update_Media_Info_Details import Update_Media_Info_Details as Update_Media_Info_Details

from Language import Language as Language
from Input import Input as Input

class Media_Info_Database_Manager():
	def __init__(self):
		# Global Switches dictionary
		self.global_switches = {
			"verbose": False,
		}

		self.Language = Language(self.global_switches)

		classes = [
			Create_New_Media_Info_Entry,
			Open_Data_File_Of_Media,
			Fill_Episode_Titles_File,
		]

		names_per_language = [
			{
				"en": "Add new media to Media Info Database",
				"pt": "Adicionar nova mídia ao Banco de Dados de Informações de Mídia",
			},
			{
				"en": "Open media data file",
				"pt": "Abrir arquivo de dados de mídia",
			},
			{
				"en": "Fill episode titles file",
				"pt": "Preencher arquivo de títulos de episódio",
			},
		]

		names = []

		for name in names_per_language:
			names.append(self.Language.Item(name))

		self.texts = {
			"show_text": {
				"en": "Manage Media Info Database",
				"pt": "Gerenciar Banco de Dados de Informações de Mídia",
			},
			"select_one_class_to_execute": {
				"en": "Select one class to execute",
				"pt": "Selecione uma classe para executar",
			},
		}

		self.language_texts = self.Language.Item(self.texts)

		Input().Select(classes, language_options = names, show_text = self.language_texts["show_text"], select_text = self.language_texts["select_one_class_to_execute"], function = True)

#Update_Media_Info_Details()