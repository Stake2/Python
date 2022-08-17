# Text_Generator.py

from Script_Helper import *
import Script_Helper

from Text_Generator.New_World_NameID_Generator_Module import *
from Text_Generator.Year_Summary_Maker_Module import *
from Text_Generator.Add_Text_To_List_Of_Texts_Module import *
from Text_Generator.Generate_CSS_Selectors import *

text_generator_choice_descriptions = [
None,
Language_Item_Definer("New World NameID Generator", "Gerador de NameID do New World"),
Language_Item_Definer("Year Summary Maker", "Criador de Sumário de Ano"),
Language_Item_Definer("Add Text To List Of Texts", "Adicionar Textos À Lista de Textos"),
Language_Item_Definer("Generate CSS Selectors", "Gerar Seletores de CSS"),
]

text_generator_choice_functions = [
None,
NWNIDG_Choose,
Make_Year_Summary,
ATTLOT_Choose,
GCS_Run,
]

local_script_name = '"' + "Text_Generator.py" + '"'

def Choose():
	print()
	choice_list_text = Language_Item_Definer("Select a Text Generator function to execute", "Selecione uma função do Gerador de Texto para executar")
	Script_Helper.Make_Choices(text_generator_choice_descriptions, text_generator_choice_functions, script_name = local_script_name, extra_option = None, run = True, show_selected_text = True, double_extra_option = False, alternative_choice_list_text = choice_list_text, alternative_array = False, export_number = False, return_choice = False)