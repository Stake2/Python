# PicoWorkers.py

from Script_Helper import *

from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

class PicoWorkers():
	def __init__(self, parameter_switches = None):
		# Verbose variable
		self.verbose = False

		self.testing_script = False

		self.parameter_switches = parameter_switches

		self.Define_Basic_Variables()
		self.Define_Data()
		self.Help_With_Jobs()

	def Define_Basic_Variables(self):
		self.option = True

		self.global_switches = {
		"write_to_file": self.option,
		"create_files": self.option,
		"create_folders": self.option,
		"move_files": self.option,
		"verbose": self.verbose,
		"testing_script": self.testing_script,
		}

		if self.parameter_switches != None:
			self.global_switches = self.parameter_switches
			self.testing_script = self.global_switches["testing_script"]

		if self.global_switches["testing_script"] == True:
			print(Language_Item_Definer("Testing script: Yes", "Testando script: Sim"))

		if self.global_switches["verbose"] == True:
			print(Language_Item_Definer("Verbose on", "Verbose ligado") + ".")

		if self.global_switches["testing_script"] == True:
			self.global_switches["write_to_file"] = False
			self.global_switches["create_files"] = False

		self.dot_text = ".txt"

	def Define_Data(self):
		self.picoworkers_link = "https://picoworkers.com/jobs.php"

		name = __name__

		if "." in __name__:
			name = __name__.split(".")[0]

		self.module_text_files_folder = script_text_files_folder + name + "/"
		Create_Folder(self.module_text_files_folder, self.global_switches["create_folders"])

		self.youtube_data_file = self.module_text_files_folder + "YouTube Data" + self.dot_text
		Create_Text_File(self.youtube_data_file, self.global_switches["create_files"])

		self.reddit_username_file = self.module_text_files_folder + "Reddit Username" + self.dot_text
		Create_Text_File(self.reddit_username_file, self.global_switches["create_files"])

		self.youtube_data = Create_Array_Of_File(self.youtube_data_file)
		self.youtube_username = self.youtube_data[0]
		self.youtube_channel_link = self.youtube_data[1]

		self.reddit_username = Create_Array_Of_File(self.reddit_username_file)[0]

		self.picoworkers_category_link_template = self.picoworkers_link + "?&category={}&sub_category="

	def Open_PicoWorkers(self, category_name, category_number, first_space, second_space = False):
		if first_space == True:
			print()

		print(Language_Item_Definer("Opening", "Abrindo") + " PicoWorkers " + Language_Item_Definer('on "{}" category to work', 'na categoria "{}" para trabalhar').format(category_name) + "...")

		Open_Link(self.picoworkers_category_link_template.format(category_number))

		if second_space == True:
			print()

	def Change_Website(self, first_space, second_space):
		self.choice_text = Language_Item_Definer("Select a category of jobs to work", "Selecione uma categoria de trabalhos para trabalhar")
		self.chosen_list_name = Select_Choice_From_List(self.lists_of_options, local_script_name, self.choice_text, second_choices_list = self.lists_of_options, return_second_item_parameter = True, return_number = True, add_none = True, first_space = first_space, second_space = second_space)[0]
		self.chosen_list = self.lists_of_options[self.chosen_list_name]
		self.username = self.usernames[self.chosen_list_name]
		self.category_name = self.chosen_list_name
		self.category_number = self.categories[self.chosen_list_name]
		self.chosen_list[Language_Item_Definer("Change website", "Mudar site")] = ""
		self.chosen_list[Language_Item_Definer("Finish working", "Terminar de trabalhar")] = ""

	def Help_With_Jobs(self):
		self.youtube_choices = {
		Language_Item_Definer("YouTube Username", "Nome de Usuário do YouTube"): self.youtube_username,
		Language_Item_Definer("YouTube Channel Link", "Link do Canal do YouTube"): self.youtube_channel_link,
		}

		self.reddit_choices = {
		Language_Item_Definer("Reddit Username", "Nome de Usuário do Reddit"): self.reddit_username,
		Language_Item_Definer("Reddit Profile Link", "Link de Perfil do Reddit"): "https://www.reddit.com/user/" + self.reddit_username,
		Language_Item_Definer("Cut Reddit Profile Link", "Link de Perfil do Reddit Cortado"): "reddit.com/user/" + self.reddit_username,
		}

		self.lists_of_options = {
		"YouTube": self.youtube_choices,
		"Reddit": self.reddit_choices,
		}

		self.usernames = {
		"YouTube": self.youtube_username,
		"Reddit": self.reddit_username,
		}

		self.categories = {
		"YouTube": "20",
		"Reddit": "37",
		}

		self.data_to_copy = {
		Language_Item_Definer("Finish working", "Terminar de trabalhar"): "",
		}

		self.finish_working = False
		self.chosen_list = None

		while self.finish_working == False:
			if self.chosen_list != None:
				print("---")

			if self.chosen_list == None:
				self.Change_Website(True, False)
				self.Open_PicoWorkers(self.category_name, self.category_number, True)

			if self.chosen_list != None:
				print()

			print(Language_Item_Definer("{} Username", "Nome de Usuário do {}").format(self.chosen_list_name) + ": " + self.username)

			self.choice_text = Language_Item_Definer("Select an option to copy the text", "Selecione uma opção para copiar o texto")
			self.choice = Select_Choice_From_List(self.chosen_list, local_script_name, self.choice_text, second_choices_list = self.chosen_list, return_second_item_parameter = True, return_number = True, add_none = True)[0]
			self.text_to_copy = self.chosen_list[self.choice]

			if self.choice == Language_Item_Definer("Change website", "Mudar site"):
				self.Change_Website(False, True)
				self.Open_PicoWorkers(self.category_name, self.category_number, False, True)

			if self.choice not in [Language_Item_Definer("Finish working", "Terminar de trabalhar"), Language_Item_Definer("Change website", "Mudar site")]:
				print(Language_Item_Definer("Copied", "Copiado") + ": " + self.text_to_copy)
				Copy_Text(self.text_to_copy)
				print()

			if self.choice == Language_Item_Definer("Finish working", "Terminar de trabalhar"):
				print(Language_Item_Definer("Finished working", "Terminou de trabalhar") + ".")
				print()

				Write_On_Diary_Slim_Module("Trabalhei um pouco no PicoWorkers")

				self.finish_working = True

				quit()