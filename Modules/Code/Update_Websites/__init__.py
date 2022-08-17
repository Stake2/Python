# Update_Websites.py

from Script_Helper import *

from Code.Code import Code as Code

class Update_Websites(Code):
	def __init__(self, parameter_switches = None, update_one_website = False, module_website = None):
		super().__init__(parameter_switches)

		self.update_one_website = update_one_website
		self.module_website = module_website

		if self.module_website != None:
			self.update_one_website = True

		self.Define_Variables()
		self.Select_Website()

		self.Open_And_Close_XAMPP(open = True)
		self.Update_Website()

		if self.update_one_website == False:
			self.update_more_websites = True
			self.first_time = False

			i = 0
			while self.update_more_websites == True:
				self.update_more_websites = Yes_Or_No_Definer(self.update_more_websites_text, second_space = False)

				if self.update_more_websites == True:
					print()
					self.Select_Website()
					print()
					self.Update_Website(open = True, close = False)

					i += 1

				if self.update_more_websites == False:
					self.Open_And_Close_XAMPP(close = True)

		if self.update_one_website == True:
			self.Open_And_Close_XAMPP(close = True)

		self.Open_Git_Console_Window()

	def Define_Variables(self):
		self.languages = [
		"General",
		"English",
		"Portuguese",
		]

		self.beautiful_language_names = {
		"General": Language_Item_Definer("General language", "Idioma Geral"),
		"English": Language_Item_Definer("English", "Inglês"),
		"Portuguese": Language_Item_Definer("Portuguese", "Português"),
		}

		self.xampp_programs = [
		"xampp-control",
		"httpd",
		"mysql",
		]

		self.finished_loading_text = Language_Item_Definer("Press any key when the pages finished loading", "Pressione qualquer tecla quando as páginas terminarem de carregar") + ": "

		self.update_more_websites_text = Language_Item_Definer("Update more websites", "Atualizar mais sites")

		self.english_websites_file = websites_list_folder + "English Websites" + self.dot_text
		self.english_websites = Create_Array_Of_File(self.english_websites_file)

		self.portuguese_websites_file = websites_list_folder + "Portuguese Websites" + self.dot_text
		self.portuguese_websites = Create_Array_Of_File(self.portuguese_websites_file)

		self.language_websites = Language_Item_Definer(self.english_websites, self.portuguese_websites)

		self.update_website_url_template = Create_Array_Of_File(php_url_format_text_file)[1]

	def Select_Website(self):
		if self.module_website == None:
			self.choice_text = Language_Item_Definer("Select a website to update its HTML contents", "Selecione um site para atualizar seus conteúdos de HTML")
			self.choice_info = Select_Choice_From_List(self.language_websites, local_script_name, self.choice_text, second_choices_list = self.english_websites, return_second_item_parameter = True, return_number = True, add_none = True, first_space = False, second_space = False)
			self.website_number = self.choice_info[1] - 1

		if self.module_website != None:
			self.websites_number = 0
			for website in self.english_websites:
				if self.module_website == website:
					self.website_number = self.websites_number

				self.websites_number += 1

		self.website = self.english_websites[self.website_number]
		self.language_website_name = self.language_websites[self.website_number]

	def Open_And_Close_XAMPP(self, open = False, close = False):
		if open == True:
			if self.global_switches["testing_script"] == False:
				Open_File(xampp)
				time.sleep(3)

		if close == True:
			if self.global_switches["testing_script"] == False:
				for program in self.xampp_programs:
					Close_Program(program)

	def Update_Website(self, open = True, close = True):
		print("---")
		print()
		print(Language_Item_Definer("Updating this website", "Atualizando esse site") + ": ")
		print(self.language_website_name)
		print()

		for language in self.languages:
			self.website_url = self.update_website_url_template.format(self.website, language)

			print("---")
			print()
			print(Language_Item_Definer("Website link", "Link do site") + ": ")
			print(self.website_url)
			print()
			print(Language_Item_Definer("Language", "Idioma") + ": " + self.beautiful_language_names[language])
			print()

			if self.global_switches["testing_script"] == False:
				Open_Link(self.website_url)

				time.sleep(5)

		print("---")
		print()

		input(self.finished_loading_text)

	def Open_Git_Console_Window(self):
		files = List_Files(script_shortcuts_white_icons_folder, add_none = False)

		for file in files:
			if "GitHub" in file:
				git_bat_file = file

		if self.global_switches["testing_script"] == False:
			Open_Link(git_bat_file)