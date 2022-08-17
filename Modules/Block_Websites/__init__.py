# Block_Websites.py

# Script Helper importer
from Script_Helper import *

from Block_Websites.Block import Block as Block
from Block_Websites.Unblock import Unblock as Unblock

local_script_name = "Block_Websites.py"

def Function_Choose():
	functions = [
	Block,
	Unblock,
	]

	descriptions = [
	Language_Item_Definer("Block", "Bloquear"),
	Language_Item_Definer("Unblock", "Desbloquear"),
	]

	choice_text = Language_Item_Definer("Block websites", "Bloquear sites")

	Choose_Function(functions, descriptions, local_script_name, choice_text)

if __name__ == "__main__":
	Function_Choose()