# Write_On_Diary_Slim.py

from Script_Helper import *

from Diary_Slim.Diary_Slim import Diary_Slim as Diary_Slim

from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

class Write_On_Diary_Slim(Diary_Slim):
	def __init__(self, custom_option = None):
		super().__init__()

		self.current_diary_slim_file = Create_Array_Of_File(self.current_diary_slim_file)[0]

		self.custom_option = custom_option

		self.use_text_file = False

		self.Define_Texts()
		self.Select()
		self.Write()

	def Define_Texts(self):
		self.today = datetime.datetime.today()
		self.week_day = self.today.weekday()

		self.today_task_done_text = Create_Array_Of_File(self.diary_slim_things_done_texts_file)[self.week_day]

		self.diary_slim_texts = {
			"Water": "Bebi dois litros de água",
			"Lunch": "Almocei",
			"Dinner": "Jantei",
			"Bike": "Andei de bicicleta pela cidade",
			"Bath": "Tomei um banho, lavei o rosto, escovei os dentes",
			"Python": "Programei em Python um pouco, programando o meu módulo" + "...",
			"PHP": "Programei meus sites em PHP um pouco" + "...",
			"FreeFileSync": "Sincronizei os arquivos deste computador para o computador da sala usando o programa FreeFileSync",
			"Drawings - Desenhos": "Desenhei um pouco no" + "...",
			"Videos - Vídeos": "Editei um pouco um vídeo no Sony Vegas" + "...",
			"Udemy Course": "Assisti {} {} do meu curso de PHP 7 na Udemy, totalizando {} de curso",
		}

		self.english_diary_slim_texts = {
			self.diary_slim_texts["Water"]: "Drank two bottles of water",
			self.diary_slim_texts["Lunch"]: "I had lunch",
			self.diary_slim_texts["Dinner"]: "I had dinner",
			self.diary_slim_texts["Bike"]: "I cycled through the city",
			self.diary_slim_texts["Bath"]: "I took a shower, washed my face, brushed my teeth",
			self.diary_slim_texts["FreeFileSync"]: "Synchronized the files of this computer to the living room computer using the program FreeFileSync",
			self.diary_slim_texts["Python"]: "Programmed in Python a little, coding my module",
			self.diary_slim_texts["PHP"]: "Programmed my websites in PHP a little",
			self.diary_slim_texts["Drawings - Desenhos"]: "I drew a little on",
			self.diary_slim_texts["Videos - Vídeos"]: "I edited a video a little on Sony Vegas",
			self.diary_slim_texts["Udemy Course"]: "Watched {} {} of my course of PHP 7 on Udemy, totaling {} of course"
		}

		self.deactivate_food = True

		if self.deactivate_food == True:
			self.diary_slim_texts.pop("Lunch")
			self.diary_slim_texts.pop("Dinner")

			self.english_diary_slim_texts.pop("Almocei")
			self.english_diary_slim_texts.pop("Jantei")

		self.module_current_state = self.current_state

		for state in self.state_names:
			self.current_state_file = self.state_files[state]["Current State"]
			english_state = self.english_states[state]
			portuguese_state = self.portuguese_states[state]
			mixed_state = english_state + ", " + portuguese_state

			self.file_current_state = Create_Array_Of_File(self.current_state_file)

			self.state_position_name = self.state_position_names[state][mixed_state]

			if self.file_current_state != []:
				self.file_current_state = self.file_current_state[0]

			if self.file_current_state != self.state_texts[state]["Second State"]:
				self.diary_slim_texts[state] = portuguese_state + " (" + self.state_position_name + ")"
				self.english_diary_slim_texts[portuguese_state] = english_state + " (" + self.state_position_name + ")"

		if self.today_task_done_text != "":
			if ", " not in self.today_task_done_text:
				self.diary_slim_texts["Today Task"] = self.today_task_done_text

			if ", " in self.today_task_done_text:
				self.diary_slim_texts["First Today Task"] = self.today_task_done_text.split(", ")[0]
				self.diary_slim_texts["Second Today Task"] = self.today_task_done_text.split(", ")[1]

		self.Define_Double_State_Texts()

		self.diary_slim_module_texts = [
			"Udemy Course",
		]

		self.diary_slim_name_texts = {
			"Python": Language_Item_Definer("Python module", "módulo de Python"),
			"PHP": Language_Item_Definer("PHP website", "site em PHP"),
			"Drawings - Desenhos": Language_Item_Definer("drawing", "desenho"),
			"Videos - Vídeos": Language_Item_Definer("video", "vídeo"),
		}

		self.diary_slim_data_name_texts = {
			"Python": Language_Item_Definer("Type the name of the module", "Digite o nome do módulo"),
			"Drawings - Desenhos": Language_Item_Definer("Type the name of the drawing program", "Digite o nome do programa de desenho"),
			"Udemy Course": Language_Item_Definer("Type how much course classes you watched (1, one)", "Digite quantas aulas de curso você assistiu (1, uma)"),
		}

		self.diary_slim_action_name_texts = {
			"Python": Language_Item_Definer("Say what you did on the {}", "Diga o que você fez no {}"),
			"Python English": Language_Item_Definer("Say what you did on the {}, but in English", "Diga o que você fez no {}, mas em Inglês"),
			"PHP": Language_Item_Definer("Say what you did on the {}", "Diga o que você fez no {}"),
			"PHP English": Language_Item_Definer("Say what you did on the {}, but in English", "Diga o que você fez no {}, mas em Inglês"),
			"Drawings - Desenhos": Language_Item_Definer("Say what you did on the {}", "Diga o que você fez no {}"),
			"Drawings - Desenhos English": Language_Item_Definer("Say what you did on the {}, but in English", "Diga o que você fez no {}, mas em Inglês"),
			"Videos - Vídeos": Language_Item_Definer("Say what you did on the {}", "Diga o que você fez no {}"),
			"Videos - Vídeos English": Language_Item_Definer("Say what you did on the {}, but in English", "Diga o que você fez no {}, mas em Inglês"),
		}

		self.format_texts = [
			"Python",
			"PHP",
			"Drawings - Desenhos",
			"Videos - Vídeos",
		]

		self.ask_for_text = [
			"Python",
			"Drawings - Desenhos",
		]

		self.text_file_names = {
			"Python": "",
			"PHP": ".php",
			"Drawings - Desenhos": "",
			"Videos - Vídeos": "",
		}

		for key in self.diary_slim_module_texts:
			if key in self.diary_slim_texts and self.custom_option == None:
				value = self.diary_slim_texts[key]

				self.diary_slim_texts.pop(key)
				self.english_diary_slim_texts.pop(value)

	def Replace_Selected_Text(self, selected_text):
		for state in self.state_names:
			state_texts = self.state_texts[state]

			self.selected_text_items_to_remove = [
				" (" + self.language_first_state_text + ")",
				" (" + self.language_second_state_text + ")",
			]

			for item in self.selected_text_items_to_remove:
				if item in selected_text:
					selected_text = selected_text.replace(item, "")

		return selected_text

	def Select(self):
		if self.custom_option == None:
			self.choice_text = Language_Item_Definer("Select a text to write", "Selecione um texto para escrever")
			self.selected_text = Select_Choice_From_List(self.diary_slim_texts.values(), local_script_name, self.choice_text, second_choices_list = self.diary_slim_texts, return_second_item_parameter = True, add_none = True, return_number = True, first_space = False)[0]

		else:
			self.selected_text = self.custom_option

			print("---")
			print()
			print(Language_Item_Definer("You selected the \"{}\" option to register on current Diary Slim", "Você selecionou a opção \"{}\" para registrar no Diário Slim atual").format(self.custom_option) + ".")

		self.selected_text_key = self.selected_text
		self.selected_text = self.diary_slim_texts[self.selected_text_key]

		self.selected_text = self.Replace_Selected_Text(self.selected_text)

		self.english_selected_text = self.english_diary_slim_texts[self.selected_text]
		self.selected_text_replaced = self.selected_text.replace("...", "") + "\n"

		if self.selected_text_key in self.format_texts:
			self.text_name = self.diary_slim_name_texts[self.selected_text_key]

			self.selected_text_replaced = self.selected_text_replaced.replace("\n", "")

			if self.selected_text_key in self.ask_for_text:
				self.text_data = Select_Choice(self.diary_slim_data_name_texts[self.selected_text_key], first_space = False) + self.text_file_names[self.selected_text_key]
				self.english_text_data = self.text_data

				if ", " in self.text_data:
					self.text_data_split = self.text_data.split(", ")

					new_text_data = ""

					for item in self.text_data_split:
						if item == self.text_data_split[-1]:
							new_text_data += "e "

						new_text_data += '"' + item + '"'

						if item != self.text_data_split[-1]:
							new_text_data += ", "

					self.text_data = new_text_data
					self.english_text_data = self.text_data.replace("e ", "and ")

					self.selected_text_replaced = self.selected_text_replaced.replace("o meu módulo", "os meus módulos")
					self.english_selected_text = self.english_selected_text.replace("my module", "my modules")

				else:
					self.text_data = '"' + self.text_data + '"'

				self.selected_text_replaced = self.selected_text_replaced + " " + self.text_data
				self.english_selected_text = self.english_selected_text + " " + self.english_text_data

			print(self.diary_slim_action_name_texts[self.selected_text_key].format(self.text_name) + ": ")

			show_text = "\n" + "---"

			print(show_text)

			self.use_text_file = Yes_Or_No_Definer(Language_Item_Definer("Use text file to write description", "Usar arquivo de texto para escrever descrição"), second_space = False)

			if self.use_text_file == True:
				self.Use_Text_File()
				self.action_description = self.descriptions[full_language_pt] + "a"
				self.english_action_description = self.descriptions[full_language_en] + "a"

			if self.use_text_file == False:
				self.action_description = Text_Writer(self.selected_text_replaced, finish_text = "default_list", capitalize_lines = True, auto_add_dots = True, first_space = False)

				print("-----")
				print()

				print(self.diary_slim_action_name_texts[self.selected_text_key + " English"].format(self.text_name) + ": ")

				show_text = "\n" + "---"

				print(show_text)

				self.english_action_description = Text_Writer(self.english_selected_text, finish_text = "default_list", capitalize_lines = True, auto_add_dots = True, first_space = False)

			self.text_to_write = self.selected_text_replaced + ".\n" + self.action_description

		if self.selected_text_key == "Udemy Course":
			print()

			self.how_much_classes = Select_Choice(self.diary_slim_data_name_texts[self.selected_text_key], first_space = False, accept_enter = False)

			self.choice_text = Language_Item_Definer("Type how much time you spent watching those classes", "Digite quanto tempo você passou assistindo essas aulas")
			self.how_much_time = Select_Choice(self.choice_text, first_space = False, accept_enter = False)

			self.class_singular_plural_text = "aulas"

			if self.how_much_classes in ["uma", "um", 1, "1"]:
				self.class_singular_plural_text = "aula"

			self.text_to_write = self.selected_text.format(self.how_much_classes, self.class_singular_plural_text, self.how_much_time) + "."

		if self.selected_text_key not in self.format_texts and self.selected_text_key != "Udemy Course":
			self.text_to_write = self.selected_text

	def Write(self):
		self.current_time = time.strftime("%H:%M %d/%m/%Y")

		if self.selected_text_key in self.format_texts:
			self.experienced_media_type = self.selected_text_key
			self.english_task_description = self.english_selected_text + ".\n" + self.english_action_description[:-1]
			self.portuguese_task_description = self.selected_text_replaced + ".\n" + self.action_description[:-1]
			self.experienced_media_time = self.current_time

			from Tasks.Register_Task_Module import Register_Task_Module as Register_Task_Module

			Register_Task_Module(self.experienced_media_type, self.english_task_description, self.portuguese_task_description, self.experienced_media_time, skip_input = False, parameter_switches = self.global_switches)

		if self.selected_text_key not in self.format_texts:
			if "." not in self.text_to_write[-1]:
				self.text_to_write += "."

			Write_On_Diary_Slim_Module(self.text_to_write, self.current_time, self.global_switches)

		if self.use_text_file == True and self.global_switches["testing_script"] == False:
			Remove_File(self.backup_file)

		self.Change_Double_State_Texts(self.module_current_state)

	def Use_Text_File(self):
		self.description_files = {}
		self.description_files[full_language_en] = self.diary_slim_folder + "Description in " + full_language_en + self.dot_text
		self.description_files[full_language_pt] = self.diary_slim_folder + "Descrição em " + full_language_pt + self.dot_text

		for language in list(self.description_files.keys()):
			file = self.description_files[language]
			Create_Text_File(file, self.global_switches)
			Open_Text_File(file)

		Select_Choice(Language_Item_Definer("Press Enter when you finish writing and saving the description in {} and {}", "Pressione Enter quando você terminar de escrever e salvar a descrição em {} e {}").format(full_languages_translated_dict[full_language_en][Language_Item_Definer(1, 2)], full_languages_translated_dict[full_language_pt][Language_Item_Definer(1, 2)]), enter_equals_empty = True)

		self.descriptions = {}

		self.backup_file = self.diary_slim_folder + "Action Description Backup" + self.dot_text
		Create_Text_File(self.backup_file, self.global_switches)

		for language in list(self.description_files.keys()):
			file = self.description_files[language]

			self.descriptions[language] = Read_String(file)

			if self.global_switches["testing_script"] == False:
				Append_To_File(self.backup_file, self.descriptions[language] + "\n", self.global_switches)

			print(language + ": ")
			print("[" + self.descriptions[language] + "]")

			if self.global_switches["testing_script"] == False:
				Remove_File(file)

			if language != list(self.description_files.keys())[-1]:
				print()