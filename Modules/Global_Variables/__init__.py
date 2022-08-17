from Global_Arrays import *
from Global_Functions import *
from Language_Variables import *

def Language_Item_Definer(item_enus, item_ptbr, custom_languague = None):
	if custom_languague == None:
		return Language_Item_Definer_2(global_language, item_enus, item_ptbr)

	if custom_languague != None:
		return Language_Item_Definer_2(custom_languague, item_enus, item_ptbr)

def Language_And_Full_Language_Definer(language_number):
	language = languages_array[language_number]
	full_language = full_languages[language_number]

	return language, full_language

story_names = Language_Item_Definer(story_names_array_enus, story_names_array_ptbr)

from Folder_Variables import *