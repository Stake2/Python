# Watch_History.py

# Script Helper importer
from Script_Helper import *

# Script name and Media History name
local_script_name = "Watch_History.py"
media_network_name = "Audiovisual Media Network"

from Watch_History.Watch_Media import *
from Watch_History.Start_Watching_A_New_Media import Start_Watching_A_New_Media as Start_Watching_A_New_Media
from Watch_History.Media_Info_Database_Manager import Media_Info_Database_Manager as Manage_Media_Info_Database

def Function_Choose():
	functions = [
	Watch_Media,
	Start_Watching_A_New_Media,
	Manage_Media_Info_Database,
	]

	descriptions = [
	Language_Item_Definer(Get_Function_Name(functions[0], replace_underline = True, lower = True, capitalize = True), "Assistir mídia"),
	Language_Item_Definer(Get_Function_Name(functions[1], replace_underline = True, lower = True, capitalize = True), "Comece a assistir uma nova mídia"),
	Language_Item_Definer("Manage Media Info Database", "Gerenciar Banco de Dados de Informações de Mídia (Media Info)"),
	]

	choice_text = Language_Item_Definer("Manage Audiovisual Media Network", "Gerenciar Rede de Mídias Audiovisuais (Audiovisual Media Network)")

	Choose_Function(functions, descriptions, local_script_name, choice_text, second_space = False)

if __name__ == "__main__":
	Function_Choose()