# Manage_Experienced_Media.py

from Script_Helper import *

from Year_Summary_Manager.Year_Summary_Manager import Year_Summary_Manager as Year_Summary_Manager

from Year_Summary_Manager.Manage_Year_Data.Manage_Experienced_Media.Create_New_Experienced_Media import Create_New_Experienced_Media as Create_New_Experienced_Media
#from Year_Summary_Manager.Manage_Year_Data.Manage_Experienced_Media.Fill_Experienced_Media_Files import Fill_Experienced_Media_Files as Fill_Experienced_Media_Files

class Manage_Experienced_Media(Year_Summary_Manager):
	def __init__(self, variables_dict):
		super().__init__(select_year = False)

		#Fill_Experienced_Media_Files(language_year_folders)

		functions = [
		Create_New_Experienced_Media,
		]

		descriptions = [
		Language_Item_Definer("Create new Experienced Media", "Criar nova Mídia Experimentada"),
		]

		self.choice_text = Language_Item_Definer("Select one function to execute", "Selecione uma função para executar")
		Choose_Function(functions, descriptions, local_script_name, self.choice_text, first_space = False, parameter = variables_dict)