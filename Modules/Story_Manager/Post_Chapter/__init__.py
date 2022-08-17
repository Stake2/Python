# Post_Chapter.py

# Script Helper importer
from Script_Helper import *

from Story_Manager.Story_Manager import *

from Block_Websites.Unblock import Unblock as Unblock
from Code.Update_Websites import Update_Websites as Update_Websites

class Post_Chapter(Story_Manager):
	def __init__(self, run_as_module = False, module_dict = {}):
		self.run_as_module = run_as_module

		self.select_story = True

		if self.run_as_module == True:
			self.select_story = False

		super().__init__(runned_function_name = "Post_Chapter", select_story = self.select_story)

		self.module_dict = module_dict

		self.skip = False
		self.ask_for_skipping = True

		if self.run_as_module == False:
			self.Chapter_Chooser()
			self.copy_title = True

		if self.run_as_module == True:
			self.story_covers_folder = self.module_dict["story_covers_folder"]
			self.website_images_story_covers_folder = self.module_dict["website_images_story_covers_folder"]
			self.story_vegas_files_folder = self.module_dict["story_vegas_files_folder"]

			self.english_chapter_titles = self.module_dict["english_chapter_titles"]
			self.english_chapter_titles_not_none = self.module_dict["english_chapter_titles_not_none"]
			self.portuguese_chapter_titles = self.module_dict["portuguese_chapter_titles"]

			self.copy_title = self.module_dict["copy_title"]

			if "skip_chapter_cover_creation" in self.module_dict:
				self.skip_chapter_cover_creation = self.module_dict["skip_chapter_cover_creation"]

		self.skipped_text = Language_Item_Definer("Skipped the", "Pulou a") + " " + "{}"

		self.Create_Chapter_Cover()

		if self.run_as_module == False:
			self.skip_text = Language_Item_Definer("Story Website Update", "Atualização de Site de História")

			if self.ask_for_skipping == True:
				self.skip = Yes_Or_No_Definer(Language_Item_Definer("Skip", "Pular") + " " + self.skip_text, first_space = False)

			if self.ask_for_skipping == False:
				self.skip = False

			if self.skip == True:
				print(self.skipped_text.format(self.skip_text) + ".")
				print()
				print("---")
				print()

			if self.skip == False:
				Update_Websites(self.global_switches, module_website = self.english_story_name)
				print()

			self.Post_On_Wattpad()

			if self.skip == True:
				print(self.skipped_text.format(self.skip_text) + ".")
				print()
				print("---")
				print()

			self.Make_Social_Network_Publish_Cards()

			if self.skip == True:
				print(self.skipped_text.format(self.skip_text) + ".")
				print()

			self.Mark_Last_Posted_Chapter()

			self.Register_Published_Chapter_Task()

	def Chapter_Chooser(self):
		self.chapter_number = self.last_posted_chapter.split(" - ")[0]

		if self.global_switches["testing_script"] == False:
			Open_Text_File(self.chapter_status_file)

		choice_text = Language_Item_Definer("Select the chapter to", "Selecione o capítulo para") + " " + self.action_text

		local_story_chapter_titles = [None]
		i = 1
		for self.chapter_title in self.story_chapter_titles:
			if self.chapter_title != None:
				self.chapter_title = str(i) + self.dash_separator + self.chapter_title

				local_story_chapter_titles.append(self.chapter_title)

				i += 1

		i = 1
		while i <= int(self.chapter_number):
			local_story_chapter_titles.pop(1)

			i += 1

		self.chapter_title = self.chapter_to_post

		if self.chapter_title != "None":
			self.chapter_number = int(self.chapter_title.split(" - ")[0]) + 1
			self.chapter_title = str(Add_Leading_Zeros(self.chapter_number)) + self.dash_separator + self.english_chapter_titles[self.chapter_number]

		if self.chapter_title == "None":
			choice_info = Make_Choices(local_story_chapter_titles, None, run = False, alternative_choice_list_text = choice_text, return_choice = True, export_number = True)

			self.chapter_title = choice_info[0]
			self.chapter_number = self.chapter_title.split(" - ")[0]

		self.chapter_status[self.chapter_to_post_line_number - 1] = self.chapter_title + "\n"

		self.chapter_status[-1] = self.chapter_title

		self.new_chapter_status = Stringfy_Array(self.chapter_status)

		self.text_to_write = self.new_chapter_status
		Write_To_File(self.chapter_status_file, self.text_to_write, self.global_switches)

		print("---")
		print()
		print(Language_Item_Definer("Chapter to post", "Capítulo para postar") + ": ")
		print(self.chapter_title)
		print()
		print("-")
		print()

	def Chapter_Cover_Mover(self, cover_language, cover_type):
		chapter_number_text = str(Add_Leading_Zeros(self.chapter_number))
		self.chapter_cover_folder_number = Get_Chapter_Cover_Folder_Number(self.chapter_number)

		self.mega_stories_chapter_cover_folder = cover_type + "/" + cover_language + "/" + self.chapter_cover_folder_number 
		self.website_images_chapter_cover_folder = cover_language + "/" + self.chapter_cover_folder_number

		self.story_chapter_covers_folder = self.story_covers_folder + self.mega_stories_chapter_cover_folder + "/"
		self.website_images_story_chapter_covers_folder = self.website_images_story_covers_folder + self.website_images_chapter_cover_folder + "/"

		self.print_language_texts = {
		"Story": Language_Item_Definer("Mega Story", "Histórias do Mega"),
		"Website": Language_Item_Definer("Stake2 Website Images", "Imagens do site Stake2"),
		}

		print_text = Language_Item_Definer("Copying the Chapter Cover to the {} Chapter Covers Folder", "Copiando a Capa de Capítulo para a pasta de Capas de Capítulos de {}")

		self.chapter_cover_file_name = cover_type

		if self.run_as_module == False:
			self.chapter_cover_file_name += "_000000"

		if self.run_as_module == True:
			self.chapter_cover_file_name += "_0000" + chapter_number_text

		self.chapter_cover_file_name += "." + self.extension
		self.old_file = sony_vegas_render_folder + self.chapter_cover_file_name

		print()
		print(self.chapter_cover_file_name)

		self.chapter_cover_file_name = chapter_number_text + "." + self.extension
		self.sony_vegas_render_chapter_cover_file = sony_vegas_render_folder + self.chapter_cover_file_name

		print(self.chapter_cover_file_name)

		if self.global_switches["verbose"] == True:
			print(self.old_file)
			print(self.sony_vegas_render_chapter_cover_file)
			print()

		# [Cover_Type]_000000.jpeg > 01.jpeg
		Move_File(self.old_file, self.sony_vegas_render_chapter_cover_file, self.global_switches)

		# Mega Stories Folder
		self.story_folder_chapter_cover_file = self.story_chapter_covers_folder + self.chapter_cover_file_name

		print(print_text.format(self.print_language_texts["Story"]) + "...")

		if cover_type != self.english_landscape_text:
			print()

		if self.global_switches["verbose"] == True:
			print(self.story_folder_chapter_cover_file)
			print()

		Copy_File(self.sony_vegas_render_chapter_cover_file, self.story_folder_chapter_cover_file, self.global_switches)

		if cover_type == self.english_landscape_text:
			# Stake2 Website Images Story Covers folder
			self.website_images_chapter_cover_file = self.website_images_story_chapter_covers_folder + self.chapter_cover_file_name

			print(print_text.format(self.print_language_texts["Website"]) + "...")

			if self.global_switches["verbose"] == True:
				print(self.website_images_chapter_cover_file)
				print()

			print()

			Copy_File(self.sony_vegas_render_chapter_cover_file, self.website_images_chapter_cover_file, self.global_switches)

		Remove_File(self.sony_vegas_render_chapter_cover_file, self.global_switches)

	def Chapter_Title_Copier(self, language_number):
		self.language_number = language_number

		self.language, self.full_language = Language_And_Full_Language_Definer(self.language_number)

		self.english_chapter_title = self.english_chapter_titles[int(self.chapter_number)]
		self.portuguese_chapter_title = self.portuguese_chapter_titles[int(self.chapter_number)]

		self.chapter_title = Language_Item_Definer(self.english_chapter_title, self.portuguese_chapter_title, self.language)
		self.chapter_number = str(self.chapter_number)

		self.local_chapter_title = self.chapter_number + self.dash_separator + self.chapter_title

		if self.language_number == 1:
			self.local_full_language = full_languages_translated[self.language_number].split(" - ")[self.language_number]

		if self.language_number == 2:
			self.local_full_language = full_languages_translated[self.language_number].split(" - ")[self.language_number - 2]

		self.title_text = Language_Item_Definer("Title", "Título")

		if self.skip == False:
			print(self.title_text + ": " + self.local_chapter_title)
			print()

			if self.copy_title == True:
				self.copy_chapter_title_text = Language_Item_Definer("Press any key to copy the title in {}", "Pressione qualquer tecla para copiar o título em {}")

				print()

				self.input_text = input(self.copy_chapter_title_text.format(self.local_full_language) + ": ")

				copy(self.local_chapter_title)

	def Chapter_Title_Copier_And_Mover(self, cover_type, language_cover_text, chapter_number = None, language_data = None):
		self.cover_type = cover_type
		self.language_cover_text = language_cover_text

		if chapter_number != None:
			self.chapter_number = chapter_number
			copy = False

		self.move_chapter_cover_text = Language_Item_Definer("Press any key to move the chapter cover in {} mode", "Pressione qualquer tecla para mover a capa de capítulo em modo {}")

		if language_data == None:
			language_number = 1
			for language in full_languages_not_none:
				self.Chapter_Title_Copier(language_number)

				self.input_text = input(self.move_chapter_cover_text.format(self.language_cover_text) + ": ")

				self.Chapter_Cover_Mover(language, self.cover_type)

				if language != full_languages_not_none[-1]:
					print("-")
					print()

				language_number += 1

		else:
			language = language_data["language"]
			language_number = language_data["number"]

			self.Chapter_Title_Copier(language_number)

			self.input_text = input(self.move_chapter_cover_text.format(self.language_cover_text) + ": ")

			self.Chapter_Cover_Mover(language, self.cover_type)

	def Create_Chapter_Cover(self):
		self.chapter_cover_function_text = Language_Item_Definer('Executing the "{}" Function', 'Executando a função "{}"') + "."

		self.skip_chapter_cover_creation_text = Language_Item_Definer("Chapter Cover Creation", "Criação De Capa De Capítulo")

		if self.run_as_module == True:
			self.skip_chapter_cover_creation_text = self.skip_chapter_cover_creation_text.replace("De Capa De", "De Capas De")

		try:
			eval("self.skip_chapter_cover_creation")
			self.skip_chapter_cover_creation_defined = True

		except NameError:
			self.skip_chapter_cover_creation_defined = False

		if self.skip_chapter_cover_creation_defined == False:
			self.skip_chapter_cover_creation = False

			if self.ask_for_skipping == True:
				self.skip_chapter_cover_creation = Yes_Or_No_Definer(Language_Item_Definer("Skip", "Pular") + " " + self.skip_chapter_cover_creation_text, first_space = False)

		if self.skip_chapter_cover_creation == True:
			print(self.skipped_text.format(self.skip_text) + ".")
			print()
			print("---")
			print()

		if self.skip_chapter_cover_creation == False:
			print("---")
			print()

			if self.run_as_module == False:
				print()
				print(self.chapter_cover_function_text.format(Language_Item_Definer("Create Chapter Cover", "Criar Capa De Capítulo")))
				print()
				print("-")
				print()

		self.cover_types = [
			self.english_portrait_text,
			self.english_landscape_text,
		]

		self.extensions = {
			self.english_portrait_text: "jpeg",
			self.english_landscape_text: "png",
		}

		self.sony_vegas_files = {
			self.english_portrait_text: self.story_vegas_files_folder + self.english_portrait_text + ".veg",
			self.english_landscape_text: self.story_vegas_files_folder + self.english_landscape_text + ".veg",
		}

		self.cover_type_texts = {
			self.english_portrait_text: self.portrait_text,
			self.english_landscape_text: self.landscape_text,
		}

		opening_vegas_file_text = Language_Item_Definer("Opening the Chapter Covers VEGAS file in [{}] mode.\n" + "Render the chapter cover in [{}] mode with the title in [{}] format.", "Abrindo o arquivo do VEGAS de Capas de Capítulo em modo [{}].\n" + "Renderize a capa de capítulo em modo [{}] com o título em formato [{}].")

		press_any_key_text = Language_Item_Definer("Press any key to copy the chapter titles and paste them on the VEGAS Title Media", "Pressione qualquer tecla para copiar os títulos de capítulos e cole eles na Mídia de Título do VEGAS") + "."

		if self.run_as_module == True:
			opening_vegas_file_text = opening_vegas_file_text.replace("the chapter cover", "the chapter covers")
			opening_vegas_file_text = opening_vegas_file_text.replace("a capa de capítulo", "as capas de capítulo")

		self.skipped_text = Language_Item_Definer("Skipped the", "Pulou a") + " " + "{}"

		if self.skip_chapter_cover_creation == False:
			self.skip_cover_type_creation = False
			for self.cover_type in self.cover_types:
				if self.cover_type == self.cover_types[-1]:					
					print()
					print("---")
					print()

				self.cover_type_text = self.cover_type_texts[self.cover_type]
				self.extension = self.extensions[self.cover_type]
				self.vegas_file = self.sony_vegas_files[self.cover_type]

				self.skip_cover_type_text = self.skip_chapter_cover_creation_text.lower() + " " + Language_Item_Definer("in", "em modo") + " " + "[" + self.cover_type_text + "]" + Language_Item_Definer(" mode", "")

				self.skip_cover_type_creation = False

				if self.ask_for_skipping == True:
					self.skip_cover_type_creation = Yes_Or_No_Definer(Language_Item_Definer("Skip", "Pular") + " " + self.skip_cover_type_text, first_space = False)

				if self.skip_cover_type_creation == True:
					print(self.skipped_text.format(self.skip_cover_type_text) + ".")

				if self.skip_cover_type_creation == False:
					print(opening_vegas_file_text.format(self.cover_type_text, self.cover_type_text, self.extension.upper()))
					print(press_any_key_text)
					print()

					if self.global_switches["testing_script"] == False:
						Open_File_With_Program(sony_vegas_eleven, self.vegas_file)

					if self.run_as_module == False:
						self.Chapter_Title_Copier_And_Mover(self.cover_type, self.cover_type_text)

					if self.run_as_module == True:
						local_language_number = 1
						for language in full_languages_not_none:
							self.language_data = {
								"language": language,
								"language_translated": full_languages_translated_dict[language][language_number],
								"number": local_language_number,
							}

							self.new_cover_type_text = "[" + self.cover_type_text + "] " + Language_Item_Definer("and in", "e em") + " [" + self.language_data["language_translated"] + "]"

							if local_language_number == 2:
								print("---")
								print()

							self.chapter_title_number = 1
							for chapter_title in self.english_chapter_titles_not_none:
								if self.chapter_title_number != 1:
									print("-")
									print()

								self.Chapter_Title_Copier_And_Mover(self.cover_type, self.new_cover_type_text, chapter_number = self.chapter_title_number, language_data = self.language_data)

								self.chapter_title_number += 1

							local_language_number += 1

					if self.global_switches["testing_script"] == False:
						Close_Program("vegas110.exe")

	def Chapter_Text_Copier(self, language_number):
		local_chapter_number = str(Add_Leading_Zeros(self.chapter_number))

		self.chapter_title_enus = self.english_chapter_titles[int(self.chapter_number)]
		self.chapter_title_ptbr = self.portuguese_chapter_titles[int(self.chapter_number)]

		local_chapter_title = Language_Item_Definer(self.chapter_title_enus, self.chapter_title_ptbr, self.language)

		local_chapter_title = local_chapter_number + self.dash_separator + local_chapter_title

		local_chapter_title = local_chapter_title.replace("?", "")

		self.language, self.full_language = Language_And_Full_Language_Definer(language_number)
		local_story_chapters_folder = Language_Item_Definer(self.story_chapters_enus_folder, self.story_chapters_ptbr_folder, self.language)

		chapter_file = local_story_chapters_folder + local_chapter_title + self.dot_text

		self.chapter_text = Stringfy_Array(Replace_In_Array(chapter_file, "", "", read_file = True, Reader = Read_Lines))

		copy(self.chapter_text)

	def Unblock_Wattpad(self):
		Unblock(True, "Wattpad")

	def Post_On_Wattpad(self):
		self.skip_text = Language_Item_Definer("Chapter Posting on Wattpad", "Postagem de Capítulo no Wattpad")

		if self.ask_for_skipping == True:
			self.skip = Yes_Or_No_Definer(Language_Item_Definer("Skip", "Pular") + " " + self.skip_text, first_space = False)

		if self.ask_for_skipping == False:
			self.skip = False

		if self.skip == False:
			self.Unblock_Wattpad()

		function_name = Language_Item_Definer("Post On Wattpad", "Postar No Wattpad")
		function_text = Language_Item_Definer('Executing the "' + function_name + '" Function.\n', 'Executando a função "' + function_name + '".\n')

		if self.skip == False:
			print("---\n\n" + function_text + "\n-\n")

		copied_text = Language_Item_Definer("Copied chapter text.\n", "Texto de capítulo copiado.\n")
		press_any_key_text = Language_Item_Definer("Press any key to copy the chapter text", "Pressione qualquer tecla para copiar o texto do capítulo")
		press_any_key_to_continue_text = Language_Item_Definer("Press any key when finished posting the English chapter", "Pressione qualquer tecla quando você terminar de postar o capítulo em Inglês")

		# English Chapter Posting Helper
		local_language_number = 1

		language_text = Language_Item_Definer("English Wattpad Chapter Posting Helper", "Ajudante de Postagem de Capítulo do Wattpad Em Inglês")

		if self.skip == False:
			Open_Link(self.wattpad_link_enus)

			print(language_text + ":\n")

			self.Chapter_Title_Copier(local_language_number)
			print()

			input(press_any_key_text + ": ")
			self.Chapter_Text_Copier(local_language_number)
			print()
			print(copied_text)

			Select_Choice(press_any_key_to_continue_text, first_space = False, accept_enter = True, enter_equals_empty = True)

			print("---\n")

		# Brazilian Portuguese Chapter Posting Helper
		local_language_number = 2

		language_text = Language_Item_Definer("Brazilian Portuguese Chapter Posting Helper", "Ajudante de Postagem de Capítulo do Wattpad Em Português Brasileiro")
		press_any_key_to_continue_text = Language_Item_Definer("Press any key when finished posting the Brazilian Portuguese chapter", "Pressione qualquer tecla quando você terminar de postar o capítulo em Português Brasileiro")

		if self.skip == False:
			Open_Link(self.wattpad_link_ptbr)

			print(language_text + ":\n")

			self.Chapter_Title_Copier(local_language_number)
			print()

			input(press_any_key_text + ": ")
			self.Chapter_Text_Copier(local_language_number)
			print()
			print(copied_text)

			Select_Choice(press_any_key_to_continue_text, first_space = False, accept_enter = True, enter_equals_empty = True)

	def Make_Social_Network_Publish_Cards(self):
		self.skip_text = Language_Item_Definer("Skip Social Media Card Creation", "Pular Criação De Card De Rede Social")

		if self.ask_for_skipping == True:
			self.skip = Yes_Or_No_Definer(self.skip_text, first_space = False)

		if self.ask_for_skipping == False:
			self.skip = False

		function_name = Language_Item_Definer("Make Publish Cards for Social Media", "Fazer Cards De Publicação Para Redes Sociais")
		function_text = Language_Item_Definer('Executing the "' + function_name + '" Function.\n', 'Executando a função "' + function_name + '".\n')

		if self.skip == False:
			print("---\n\n" + function_text)

		self.wattpad_template = '''Wattpad:

Mais um capítulo postado da minha história #''' + self.story_name_underlined + ''' !
O capítulo {} ({}).
Leiam por favor 😊.

{}


#Artista #ArtistasBR #Escritor #Writer #Escrita #Writing #Wattpad #Fanfiction #Poetry #Poesia #Stake2 #Izaque_Multiverse #''' + self.story_name_underlined

		self.twitter_and_facebook_template = '''Mais um capítulo postado da minha história #''' + self.story_name_underlined + ''' !
O capítulo {} ({}).
Leiam por favor 😊.

{}

#Artista #ArtistasBR #Escritor #Writer #Escrita #Writing #Wattpad #Fanfiction #Poetry #Poesia #Stake2 #Izaque_Multiverse #''' + self.story_name_underlined + '''

+

Também em meu site pessoal! 😊

{}

#Artista #ArtistasBR #Escritor #Writer #Escrita #Writing #Wattpad #Fanfiction #Poetry #Poesia #Stake2 #Izaque_Multiverse #''' + self.story_name_underlined

		if int(self.chapter_number) <= 1:
			self.wattpad_template = self.wattpad_template.replace("Mais um capítulo", "O primeiro capítulo")
			self.twitter_and_facebook_template = self.twitter_and_facebook_template.replace("Mais um capítulo", "O primeiro capítulo")

		if int(self.chapter_number) == len(self.english_chapter_titles) - 1:
			self.wattpad_template = self.wattpad_template.replace("Mais um capítulo", "O último capítulo")
			self.twitter_and_facebook_template = self.twitter_and_facebook_template.replace("Mais um capítulo", "O último capítulo")

		self.first_text = Language_Item_Definer("first", "primeira")
		self.second_text = Language_Item_Definer("second", "segunda")
		self.the_part_of_text = Language_Item_Definer("the {} part of the ", "a {} parte do Card do ")

		self.social_network_card_names = [
		None,
		"Wattpad",
		self.the_part_of_text.format(self.first_text) + "Twitter & Facebook",
		self.the_part_of_text.format(self.second_text) + "Twitter & Facebook",
		]

		self.chapter_number_name = number_names_pt[int(self.chapter_number)]

		self.text = Language_Item_Definer("Paste the Wattpad Chapter URL", "Cole o link do capítulo no Wattpad")

		if self.skip == False:
			Unblock(True, "Twitter")
			Unblock(True, "Facebook")

			self.wattpad_story_chapter_link = Select_Choice(self.text, first_space = False)

			self.social_network_cards = [None]

			self.wattpad_card = self.wattpad_template.format(self.chapter_number_name, str(self.chapter_number), self.wattpad_story_chapter_link)

			self.social_network_cards.append(self.wattpad_card)

			self.social_network_links = [
			None,
			self.wattpad_profile_conversations_url,
			self.twitter_url,
			self.facebook_url,
			]

			self.website_chapter_url = self.story_website_link + "?({})#".format(str(self.chapter_number))

			self.twitter_and_facebook_template = self.twitter_and_facebook_template.split("\n+\n\n")

			self.twitter_and_facebook_card_first_part = self.twitter_and_facebook_template[0].format(self.chapter_number_name, str(self.chapter_number), self.wattpad_story_chapter_link)

			self.twitter_and_facebook_card_second_part = self.twitter_and_facebook_template[1].format(self.website_chapter_url)

			self.twitter_and_facebook_card = self.twitter_and_facebook_card_first_part + "\n+\n\n" + self.twitter_and_facebook_card_second_part

			self.social_network_cards.append(self.twitter_and_facebook_card_first_part)
			self.social_network_cards.append(self.twitter_and_facebook_card_second_part)

			self.backup_press_any_key_text = Language_Item_Definer("Press any key to copy {} card", "Pressione qualquer tecla para copiar o Card do {}")

			i = 1
			for card in self.social_network_cards:
				if card != None:
					if i == 2:
						self.part_text = self.first_text

					if i == 3:
						self.part_text = self.second_text

					if global_language == language_pt and i == 1:
						self.press_any_key_text = self.backup_press_any_key_text.format(self.social_network_card_names[i])

					if global_language == language_pt and i == 2 or i == 3:
						self.press_any_key_text = self.backup_press_any_key_text.replace("o Card do {}", self.social_network_card_names[i])

					if global_language == language_en:
						self.press_any_key_text = self.backup_press_any_key_text.format(self.social_network_card_names[i])

					self.current_social_link = self.social_network_links[i]

					input(self.press_any_key_text + ": ")

					print()

					self.new_social_network_card = self.social_network_cards[i].replace("Wattpad:\n\n", "")

					copy(self.new_social_network_card)

					if i == 1:
						Open_Link(self.current_social_link)

					if i == 2:
						Open_Link(self.social_network_links[2])
						sleep(3)
						Open_Link(self.social_network_links[3])

					i += 1

			Create_Text_File(self.story_template_file, self.global_switches["create_files"])

			self.text_to_write = self.wattpad_card + "\n\n---\n\nTwitter and Facebook:\n\n" + self.twitter_and_facebook_card

			if self.global_switches["verbose"] == True:
				print(text_to_write)

			Write_To_File(self.story_template_file, self.text_to_write, self.global_switches)

			self.text = Language_Item_Definer("The cards were written to the Template text file of this story", "Os cards foram escritos no arquivo de Modelo dessa história")

			print(self.text + ":")
			print(self.story_name)

			print()
			print("---")

	def Mark_Last_Posted_Chapter(self):
		self.chapter_status[self.last_posted_chapter_line_number - 1] = str(Add_Leading_Zeros(self.chapter_number)) + self.dash_separator + self.english_chapter_titles[int(self.chapter_number)]

		self.new_chapter_status = Stringfy_Array(self.chapter_status)

		self.text_to_write = self.new_chapter_status
		Write_To_File(self.chapter_status_file, self.text_to_write, self.global_switches)

	def Register_Published_Chapter_Task(self):
		self.task_name_enus = self.english_published_text + " the chapter {} of my story \"{}\" on Wattpad and Stake2 Website".format(number_names_en[int(self.chapter_number)], self.english_story_name)
		self.task_name_ptbr = self.brazilian_portuguese_published_text + " o capítulo {} da minha história \"{}\" no Wattpad e no Site Stake2".format(number_names_pt[int(self.chapter_number)], self.portuguese_story_name)

		self.experienced_media_type = "Stories - Histórias"
		self.english_task_description = self.task_name_enus
		self.portuguese_task_description = self.task_name_ptbr
		self.experienced_media_time = time.strftime("%H:%M %d/%m/%Y")

		self.Register_Finished_Task(register_task = True, register_on_diary_slim = True)

def Get_Chapter_Cover_Folder_Number(chapter_number):
	if int(chapter_number) <= 10:
		chapter_cover_folder_number = "1 - 10"

	if int(chapter_number) >= 11 and int(chapter_number) <= 20:
		chapter_cover_folder_number = "11 - 20"

	if int(chapter_number) >= 21 and int(chapter_number) <= 30:
		chapter_cover_folder_number = "21 - 30"

	if int(chapter_number) >= 31 and int(chapter_number) <= 40:
		chapter_cover_folder_number = "31 - 40"

	if int(chapter_number) >= 41 and int(chapter_number) <= 50:
		chapter_cover_folder_number = "41 - 50"

	return chapter_cover_folder_number