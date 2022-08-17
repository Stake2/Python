# Create_First_Of_The_Year.py

from Script_Helper import *

from Year_Summary_Manager.Year_Summary_Manager import Year_Summary_Manager as Year_Summary_Manager

class Create_First_Of_The_Year(Year_Summary_Manager):
	def __init__(self, language_year_folders):
		super().__init__(select_year = False)

		self.language_year_folders = language_year_folders

		self.firsts_of_the_year_folders = {}

		self.firsts_of_the_year_folders[full_language_en] = self.language_year_folders[full_language_en] + self.firsts_of_the_year_folder_names[full_language_en] + "/"
		self.firsts_of_the_year_folders[full_language_pt] = self.language_year_folders[full_language_pt] + self.firsts_of_the_year_folder_names[full_language_pt] + "/"

		self.Ask_For_Caterogies()
		self.Ask_For_Thing_Info()

	def Ask_For_Caterogies(self):
		self.full_language = Language_Item_Definer(full_language_en, full_language_pt)
		self.firsts_of_the_year_sub_folder_names_language = self.firsts_of_the_year_sub_folder_names[self.full_language]
		self.firsts_of_the_year_sub_folder_names_english = self.firsts_of_the_year_sub_folder_names[full_language_en]
		self.firsts_of_the_year_sub_folder_names_portuguese = self.firsts_of_the_year_sub_folder_names[full_language_pt]

		self.sub_folders = {}

		self.choice_text = Language_Item_Definer("Select a sub folder to create the First in the Year", "Selecione uma sub pasta para criar o Primeiro no Ano")
		self.sub_folder = Select_Choice_From_List(self.firsts_of_the_year_sub_folder_names_language, local_script_name, self.choice_text, second_choices_list = self.firsts_of_the_year_sub_folder_names_portuguese, return_second_item_parameter = True, return_number = True, add_none = True, first_space = False)[0]

		self.sub_folders[full_language_en] = self.firsts_of_the_year_sub_folder_translated_names[self.sub_folder]
		self.sub_folders[full_language_pt] = self.sub_folder

		self.firsts_of_the_year_sub_sub_folder_names_language = self.firsts_of_the_year_sub_sub_folder_names[self.firsts_of_the_year_sub_folder_translated_names[self.sub_folder]][self.full_language]
		self.firsts_of_the_year_sub_sub_folder_names_portuguese = self.firsts_of_the_year_sub_sub_folder_names[self.sub_folders[full_language_en]][full_language_pt]

		self.choice_text = Language_Item_Definer("Select a sub sub folder to create the First in the Year", "Selecione uma sub sub pasta para criar o Primeiro no Ano")
		self.sub_folder = Select_Choice_From_List(self.firsts_of_the_year_sub_sub_folder_names_language, local_script_name, self.choice_text, second_choices_list = self.firsts_of_the_year_sub_sub_folder_names_portuguese, return_second_item_parameter = True, return_number = True, add_none = True, first_space = False)
		self.sub_folder_number = self.sub_folder[1]
		self.sub_folder = self.sub_folder[0]

		self.sub_folders[full_language_en] = self.sub_folders[full_language_en] + "/" + self.firsts_of_the_year_sub_sub_folder_names[self.sub_folders[full_language_en]][full_language_en][self.sub_folder_number - 1]
		self.sub_folders[full_language_pt] = self.sub_folders[full_language_pt] + "/" + self.sub_folder		

		self.final_folders = {}
		self.final_folders[full_language_en] = self.firsts_of_the_year_folders[full_language_en] + self.sub_folders[full_language_en] + "/"
		self.final_folders[full_language_pt] = self.firsts_of_the_year_folders[full_language_pt] + self.sub_folders[full_language_pt] + "/"

	def Ask_For_Thing_Info(self):
		self.describe_thing_text = Language_Item_Definer("Describe the Task in {}", "Descreva a Tarefa em {}")

		translated_language = full_languages_translated_dict["English"][language_number]
		self.choice_text = self.describe_thing_text.format(translated_language)
		self.english_thing_description = Text_Writer(self.choice_text + ":", finish_text = "default_list", second_space = False, capitalize_lines = True, auto_add_dots = True, accept_enter = True, first_space = False)

		translated_language = full_languages_translated_dict["Português Brasileiro"][language_number]
		self.choice_text = self.describe_thing_text.format(translated_language)
		self.portuguese_thing_description = Text_Writer(self.choice_text + ":", finish_text = "default_list", second_space = False, capitalize_lines = True, auto_add_dots = True, accept_enter = True)
		self.experienced_media_time = time.strftime("%H:%M %d/%m/%Y")

		self.english_thing_name = self.english_thing_description.splitlines()[0].replace(".", "")
		self.portuguese_thing_name = self.portuguese_thing_description.splitlines()[0].replace(".", "")
		self.thing_name = Language_Item_Definer(self.english_thing_name, self.portuguese_thing_name)

		self.thing_descriptions = {
		"English": self.english_thing_description,
		"Português Brasileiro": self.portuguese_thing_description,
		}

		print(self.thing_descriptions)