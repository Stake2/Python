# Media_Info_Database_Manager.py

# Script Helper importer
from Script_Helper import *

# Script name and Media History name
local_script_name = "Watch_History.py"
media_network_name = "Audiovisual Media Network"

from Watch_History.Watch_History import Watch_History as Watch_History

from Watch_History.Media_Info_Database_Manager.Create_New_Media_Info_Entry import Create_New_Media_Info_Entry as Create_New_Media_Info_Entry
from Watch_History.Media_Info_Database_Manager.Open_Data_File_Of_Media import Open_Data_File_Of_Media as Open_Data_File_Of_Media
from Watch_History.Media_Info_Database_Manager.Fill_Episode_Titles_File import Fill_Episode_Titles_File as Fill_Episode_Titles_File
from Watch_History.Media_Info_Database_Manager.Update_Media_Info_Details import Update_Media_Info_Details as Update_Media_Info_Details

class Media_Info_Database_Manager(Watch_History):
	def __init__(self):
		super().__init__()

		functions = [
		Create_New_Media_Info_Entry,
		Open_Data_File_Of_Media,
		Fill_Episode_Titles_File,
		]

		descriptions = [
		Language_Item_Definer(Get_Function_Name(Create_New_Media_Info_Entry, replace_underline = True, lower = True, capitalize = True), "Criar nova entrada no Media Info"),
		Language_Item_Definer(Get_Function_Name(Open_Data_File_Of_Media, replace_underline = True, lower = True, capitalize = True), "Abrir arquivo de dados de mídia"),
		Language_Item_Definer(Get_Function_Name(Fill_Episode_Titles_File, replace_underline = True, lower = True, capitalize = True), "Preencher arquivo de títulos de episódio"),
		]

		Choose_Function(functions, descriptions, local_script_name, Language_Item_Definer("Select one function to run", "Selecione uma função para executar"), first_space = True)

Update_Media_Info_Details()