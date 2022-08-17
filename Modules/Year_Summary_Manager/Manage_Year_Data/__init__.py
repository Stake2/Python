# Manage_Year_Data.py

from Script_Helper import *

from Year_Summary_Manager.Year_Summary_Manager import Year_Summary_Manager as Year_Summary_Manager

from Year_Summary_Manager.Manage_Year_Data.Create_First_Of_The_Year import Create_First_Of_The_Year as Create_First_Of_The_Year
from Year_Summary_Manager.Manage_Year_Data.Manage_Experienced_Media import Manage_Experienced_Media as Manage_Experienced_Media

class Manage_Year_Data(Year_Summary_Manager):
	def __init__(self):
		super().__init__()

		functions = [
		Create_First_Of_The_Year,
		Manage_Experienced_Media,
		]

		descriptions = [
		Language_Item_Definer("Create first of the Year", "Criar primeiro do Ano"),
		Language_Item_Definer("Manage Experienced Media", "Gerenciar Mídias Experimentadas"),
		]

		self.choice_text = Language_Item_Definer("Select one function to execute", "Selecione uma função para executar")
		Choose_Function(functions, descriptions, local_script_name, self.choice_text, parameter = self.variables_dict, first_space = False)