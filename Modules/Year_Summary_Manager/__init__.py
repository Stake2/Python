# Year_Summary_Manager.py

from Script_Helper import *

from Year_Summary_Manager.Manage_Year_Data import Manage_Year_Data as Manage_Year_Data

local_script_name = "Year_Summary_Manager.py"
local_script_language_name = Language_Item_Definer("Year Summary Manager", "Gerenciador de Sumário de Ano")

if " " in local_script_language_name:
	local_script_language_name = "\"" + local_script_language_name + "\""

def Function_Choose():
	Manage_Year_Data()

if __name__ == "__main__":
	Function_Choose()