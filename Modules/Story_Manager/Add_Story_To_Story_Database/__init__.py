# Add_Story_To_Story_Database.py

# Script Helper importer
from Script_Helper import *

from Story_Manager.Story_Manager import *

class Add_Story_To_Story_Database(Story_Manager):
	def __init__(self):
		super().__init__(select_story = False)

		self.Define_Story_Parameters()
		self.Ask_For_Story_Data()
		self.Add_Story_To_Files()
		self.Create_Story_Folder_And_Files()

		self.large_bar = "----------"
		self.dash_space = "-"

		print(self.large_bar)
		print()
		print(Language_Item_Definer("This story has been added to the Stories Database", "Essa história foi adicionada ao Banco de Dados de Histórias") + ": ")
		print(self.story_data_dict_to_append["Mixed Story Name"])

		print()
		print(self.dash_space)
		print()
		print(Language_Item_Definer("Story Information", "Informações da História") + ": ")

		self.english_story_parameter_names["Mixed Story Name"] = "Mixed Story Name"
		self.portuguese_story_parameter_names["Mixed Story Name"] = "Nome de História Misturado"

		self.english_story_parameter_names["Wattpad IDs"] = "Wattpad IDs"
		self.portuguese_story_parameter_names["Wattpad IDs"] = "IDs do Wattpad"

		array = Language_Item_Definer(self.english_story_parameter_names, self.portuguese_story_parameter_names)

		self.story_data_dict_to_print = {}

		self.story_data_dict_to_append["Website Link Name"] = mega_stake2_website_link + self.story_data_dict_to_append["Website Link Name"].replace(" ", "%20") + "/"

		for key in self.story_data_dict_to_append:
			new_key = array[key]
			self.story_data_dict_to_print[new_key] = self.story_data_dict_to_append[key]

		Dict_Print(self.story_data_dict_to_print)
		print(self.large_bar)

	def Define_Story_Parameters(self):
		self.story_parameters = [
		Language_Item_Definer("Story Name", "Nome da História"),
		Language_Item_Definer("Creation Date", "Data de Criação"),
		Language_Item_Definer("Author(s)", "Autor(es)"),
		]

		self.story_parameter_names = {
		"English Story Name": Language_Item_Definer("English Story Name", "Nome da História em Inglês"),
		"Portuguese Story Name": Language_Item_Definer("Portuguese Story Name", "Nome da História em Português"),
		"Creation Date": Language_Item_Definer("Creation Date", "Data de Criação"),
		"Author(s)": Language_Item_Definer("Author(s)", "Autor(es)"),
		"Website Link Name": Language_Item_Definer("Website Link Name", "Nome do Link do Site"),
		"Status": "Status",
		}

		self.english_story_parameter_names = {
		"English Story Name": "English Story Name",
		"Portuguese Story Name": "Portuguese Story Name",
		"Creation Date": "Creation Date",
		"Author(s)": "Author(s)",
		"Website Link Name": "Website Link Name",
		"Status": "Status",
		}

		self.portuguese_story_parameter_names = {
		"English Story Name": "Nome da História em Inglês",
		"Portuguese Story Name": "Nome da História em Português",
		"Creation Date": "Data de Criação",
		"Author(s)": "Autor(es)",
		"Website Link Name": "Nome do Link do Site",
		"Status": "Status",
		}

	def Ask_For_Story_Data(self):
		self.story_data_dict = {}

		i = 0
		for parameter_text in self.english_story_parameter_names:
			english_parameter_text = self.english_story_parameter_names[parameter_text]
			portuguese_parameter_text = self.portuguese_story_parameter_names[parameter_text]
			parameter_text_to_show = Language_Item_Definer(english_parameter_text, portuguese_parameter_text)

			if parameter_text != self.english_story_parameter_names["Status"]:
				parameter_data = Select_Choice(parameter_text_to_show, enter_equals_empty = True, first_space = False, second_space = False)

			else:
				parameter_data = Select_Choice_From_List(self.story_status_list.values(), local_script_name, parameter_text_to_show, second_choices_list = self.english_story_status_list, add_none = True, return_second_item_parameter = True, return_number = True)[0]

			self.story_data_dict[english_parameter_text] = parameter_data

			i += 1

		self.created_story_now = time.strftime("%d/%m/%Y")

		self.english_story_name = self.story_data_dict["English Story Name"]
		self.portuguese_story_name = self.story_data_dict["Portuguese Story Name"]
		self.mixed_story_name = self.english_story_name + self.comma_separator + self.portuguese_story_name

		if self.story_data_dict["Creation Date"] == "":
			self.story_data_dict["Creation Date"] = self.created_story_now

		if self.story_data_dict["Author(s)"] == "":
			self.story_data_dict["Author(s)"] = self.default_author

		if self.story_data_dict["Website Link Name"] == "":
			self.story_data_dict["Website Link Name"] = self.english_story_name

		self.story_data_dict_to_append = {}
		self.story_data_dict_to_append["Mixed Story Name"] = self.mixed_story_name
		self.story_data_dict_to_append.update(self.story_data_dict)
		self.story_data_dict_to_append.pop("English Story Name", None)
		self.story_data_dict_to_append.pop("Portuguese Story Name", None)

	def Add_Story_To_Files(self):
		self.new_english_story_parameter_names = {}
		self.new_english_story_parameter_names["Mixed Story Name"] = "Mixed Story Name"
		self.new_english_story_parameter_names["Wattpad IDs"] = "Wattpad IDs"
		self.new_english_story_parameter_names.update(self.english_story_parameter_names)
		self.new_english_story_parameter_names.pop("English Story Name", None)
		self.new_english_story_parameter_names.pop("Portuguese Story Name", None)

		self.story_data_dict_to_append["Wattpad IDs"] = "None"

		for parameter_text in self.new_english_story_parameter_names:
			file_to_append = self.story_database_files[parameter_text]
			text_to_append = self.story_data_dict_to_append[parameter_text]

			Append_To_File(file_to_append, text_to_append, self.global_switches, check_file_length = True)

			if self.global_switches["verbose"] == True:
				print()
				print(Language_Item_Definer("File to add texto", "Arquivo para adicionar texto") + ": " + "\n" + file_to_append)
				print()
				print(Language_Item_Definer("Text to add", "Texto para adicionar") + ": " + "\n" + text_to_append)

		self.new_story_number = str(int(Create_Array_Of_File(self.story_database_files["Number"])[0]) + 1)
		text_to_write = self.new_story_number
		Write_To_File(self.story_database_files["Number"], text_to_write, self.global_switches)

	def Create_Story_Folder_And_Files(self):
		self.story_folder = self.stories_folder + self.english_story_name + "/"
		Create_Folder(self.story_folder)

		self.story_sub_folders = {}

		for folder_name in self.main_story_folders:
			folder = self.story_folder + folder_name + "/"
			Create_Folder(folder, self.global_switches["create_folders"])

			self.story_sub_folders[folder_name] = folder

		self.creation_date_file = self.story_sub_folders["Story Info"] + "Creation Date" + self.dot_text
		Create_Text_File(self.creation_date_file, self.global_switches["create_files"])

		Write_To_File(self.creation_date_file, self.story_data_dict["Creation Date"], self.global_switches)

		self.author_file = self.story_sub_folders["Story Info"] + "Author" + self.dot_text
		Create_Text_File(self.author_file, self.global_switches["create_files"])

		Write_To_File(self.author_file, self.story_data_dict["Author(s)"], self.global_switches)

		self.writing_folder = self.story_folder + "Writing - Escrita/"
		Create_Folder(self.writing_folder, self.global_switches["create_folders"])

		self.chapter_status_file = self.writing_folder + "Chapter Status" + self.dot_text
		Create_Text_File(self.chapter_status_file, self.global_switches["create_files"])