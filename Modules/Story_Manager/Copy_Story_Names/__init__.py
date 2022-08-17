# Copy_Story_Names.py

# Script Helper importer
from Script_Helper import *

from Story_Manager.Story_Manager import *

import re

class Copy_Story_Names(Story_Manager):
	def __init__(self):
		super().__init__(select_story = False)

		self.Define_Variables()
		self.Define_Copy_Modes()
		self.Make_Story_Names_List()

		self.Select_Copy_Mode()

		while self.story_name != self.quit_text:
			if self.join_story_names == False:
				self.Select_And_Copy_Story_Name()

			if self.join_story_names == True:
				self.Join_Story_Names()

	def Define_Variables(self):
		self.select_one_to_text_template = Language_Item_Definer("Select {} to {}", "Selecione {} para {}")

		self.action_names = [
			Language_Item_Definer("Change mode", "Mudar modo"),
			Language_Item_Definer("Join {}", "Juntar {}"),
			Language_Item_Definer("Deactivate joining mode", "Desativar modo de junção"),
			Language_Item_Definer("Quit", "Sair"),
		]

		self.action_list = []

		for action_name in self.action_names:
			self.action_list.append("[" + action_name + "]")

		self.change_mode_text = self.action_list[0]
		self.join_name_text = self.action_list[1]
		self.unjoin_name_text = self.action_list[2]
		self.quit_text = self.action_list[-1]

		self.filler_text = Language_Item_Definer("Filler", "Preenchedor")
		self.filler_formated_text = "[ ] (" + self.filler_text + ")"

		self.join_story_names = False
		self.first_space = True
		self.first_mode_change = True
		self.choice_text = None

	def Define_Copy_Modes(self):
		self.copy_modes = {
			"Normal": "Normal",
			"With quotes": Language_Item_Definer("With quotes", "Com aspas"),
			"Acronym": Language_Item_Definer("Acronym", "Acrônimo"),
		}

		self.english_copy_modes = [
			item for item in self.copy_modes
		]

		self.copy_mode_texts = {
			"Normal": Language_Item_Definer("Story Name", "Nome de História"),
			"With quotes": Language_Item_Definer("Story Name", "Nome de História"),
			"Acronym": Language_Item_Definer("Story Acronym", "Acrônimo de História"),
		}

		self.plural_copy_mode_texts = {
			"Normal": Language_Item_Definer("Story Names", "Nomes de História"),
			"With quotes": Language_Item_Definer("Story Names", "Nomes de História"),
			"Acronym": Language_Item_Definer("Story Acronyms", "Acrônimos de História"),
		}

	def Make_Story_Names_List(self):
		self.story_names.pop(0)

		self.mixed_story_names = []

		i = 0
		for english_story_name in self.english_story_names:
			portuguese_story_name = self.portuguese_story_names[i]

			self.mixed_story_names.append(english_story_name)

			if english_story_name != portuguese_story_name:
				self.mixed_story_names.append(portuguese_story_name)

			i += 1

		self.story_names_list = {}

		from string import ascii_uppercase as ascii_uppercase

		for copy_mode in self.copy_modes:
			self.story_names_list[copy_mode] = []

		for self.story_name in self.mixed_story_names:
			for copy_mode in self.copy_modes:
				if copy_mode == "With quotes":
					self.story_name = '"{}"'.format(self.story_name)

				if copy_mode == "Acronym":
					self.story_name = self.story_name.split(" ")

					string = ""
					for word in self.story_name:
						uppercase_letters = sum(1 for i in word if i.isupper())

						# If there are only one uppercase character in word
						if uppercase_letters in [0, 1]:
							if word[0] != '"':
								string += word[0]

							else:
								string += word[1]

						# If there are more than one uppercase character in word
						for character in word:
							if character in ascii_uppercase and uppercase_letters > 1 and character != '"':
								string += character

					self.story_name = string

				self.story_names_list[copy_mode].append(self.story_name)

		for copy_mode in self.copy_modes:
			self.story_names_list[copy_mode] = list(dict.fromkeys(self.story_names_list[copy_mode]))

	def Select_Copy_Mode(self, second_space = False):
		self.copy_mode_choice_text = Language_Item_Definer("Select a Copy Mode to use", "Selecione um Modo de Cópia para utilizar")
		self.choice_info = Select_Choice_From_List(choices_list = self.copy_modes.values(), alternative_choice_text = self.copy_mode_choice_text, second_choices_list = self.english_copy_modes, return_second_item_parameter = True, return_number = True, add_none = True, first_space = False, second_space = second_space)

		self.copy_mode = self.copy_modes[self.choice_info[0]]
		self.english_copy_mode = self.choice_info[0]
		self.copy_mode_text = self.copy_mode_texts[self.english_copy_mode]
		self.plural_copy_mode_text = self.plural_copy_mode_texts[self.english_copy_mode]

		self.story_names_list_with_action = list(self.story_names_list[self.english_copy_mode])

		self.story_names_lists = list(self.story_names_list.values())

		self.current_list_len = len(self.story_names_list_with_action) + 3

		if len(self.story_names_list_with_action) != len(self.story_names_lists[0]):
			while len(self.story_names_list_with_action) != len(self.story_names_lists[0]):
				self.story_names_list_with_action.append(self.filler_formated_text)

		if self.first_mode_change == True:
			self.first_list_len = len(self.story_names_lists[0]) + 3

			self.no_filler_text = Language_Item_Definer(
				"You select a " + self.filler_text + "." + "\n" +
				"It is utilized to make the lengths of the other story name lists the same as the first list." + "\n" +
				"The length of the first list (Normal) is {}".format(self.first_list_len) + ", the selected list ({}) had {} of length".format(self.copy_modes[self.english_copy_mode], self.current_list_len) + " before the " + self.filler_text + "s." + "\n" + 
				"Please select {} to {}",

				"Você selecionou um " + self.filler_text + "." + "\n" +
				"Ele é utilizado para tornar os comprimentos das outras listas de nomes de histórias iguais aos da primeira lista." + "\n" + 
				"O comprimento da primeira lista (Normal) é {}".format(self.first_list_len) + ", a lista selecionada ({}) tinha {} de comprimento".format(self.copy_modes[self.english_copy_mode], self.current_list_len) + " antes dos " + self.filler_text + "es." + "\n" + 
				"Por favor selecione {} para {}",
			)

			self.action_names_format = {
				"Actions": [
					self.join_name_text,
					self.unjoin_name_text,
				],

				"Formatted": [
				
				],

				"Formatted Dict": {
				
				},

				"Parameters": {
					self.join_name_text: self.plural_copy_mode_text,
				},
			}

		for action in self.action_list:
			action_backup = action

			if self.first_mode_change == True:
				list_check = self.action_names_format["Actions"]

			if self.first_mode_change == False:
				list_check = self.action_names_format["Formatted"]

			if action_backup not in list_check and action_backup not in self.action_names_format["Formatted Dict"]:
				self.story_names_list_with_action.append(action)

			if action_backup in list_check or action_backup in self.action_names_format["Formatted Dict"]:
				if "{}" in action:
					parameter = self.action_names_format["Parameters"][action]
					action = action.format(parameter)

				if "{}" not in action and action_backup in self.action_names_format["Formatted Dict"]:
					action = self.action_names_format["Formatted Dict"][action_backup]

				if self.first_mode_change == True:
					self.action_names_format["Formatted"].append(action)
					self.action_names_format["Formatted Dict"][action_backup] = action				

				if action_backup == self.action_names_format["Actions"][0]:
					self.story_names_list_with_action.append(action)

					self.join_name_text = action

				if action_backup == self.action_names_format["Actions"][1]:
					self.unjoin_name_text = action

	def Select_And_Copy_Story_Name(self, select_text = None, show_text = None, select = True, copy = True, first_space = True, second_space = True):
		if select_text == None:
			self.choice_text_parameters = Language_Item_Definer("one", "um") + " " + self.copy_mode_text, Language_Item_Definer("copy", "copiar")

			select_text = self.select_one_to_text_template.format(*self.choice_text_parameters)

		if self.choice_text != None:
			select_text_backup = select_text

			select_text = self.choice_text

			select_text = select_text.format(*self.choice_text_parameters)

			self.choice_text = None

		if show_text == None:
			show_text = Language_Item_Definer("Copied", "Copiado")

		if self.first_space == False:
			first_space = False

			self.first_space = True

		if select == True:
			self.story_name = Select_Choice_From_List(choices_list = self.story_names_list_with_action, alternative_choice_text = select_text, second_choices_list = self.story_names_list_with_action, return_second_item_parameter = True, return_number = True, add_none = True, first_space = first_space, second_space = second_space)[0]

			self.Check_Story_Name()

		self.negative_lists = []
		self.negative_lists.extend(self.action_list)
		self.negative_lists.append(self.action_names_format["Formatted"])
		self.negative_lists.append(self.story_names_list[self.english_copy_mode])
		self.negative_lists.append(self.filler_formated_text)

		if self.story_name not in self.negative_lists and copy == True:
			Copy_Text(self.story_name)

			print(show_text + ": " + self.story_name)
			print()
			print("-----")

		if self.story_name == self.filler_formated_text:
			self.first_space = False

			self.choice_text = self.no_filler_text

	def Check_Story_Name(self):
		if self.story_name == self.change_mode_text:
			self.first_mode_change = False

			self.Select_Copy_Mode(second_space = True)

			self.first_space = False

			self.Select_And_Copy_Story_Name()

		if self.story_name == self.join_name_text:
			self.join_story_names = True

			self.action_list[-2] = self.unjoin_name_text
			self.story_names_list_with_action[-2] = self.unjoin_name_text

		if self.story_name == self.unjoin_name_text:
			self.join_story_names = False

			self.action_list[-2] = self.join_name_text
			self.story_names_list_with_action[-2] = self.join_name_text

			self.first_space = False

		if self.story_name == self.quit_text:
			self.Finish_Copying()

	def Join_Story_Names(self):
		self.show_text = Language_Item_Definer("Join", "Juntado")

		self.join_text = Language_Item_Definer("join", "juntar")

		self.join_story_name = ""

		self.the_number_text = Language_Item_Definer("the", "o") + " " + Language_Item_Definer("first", "primeiro")
		self.select_text = self.select_one_to_text_template.format(self.the_number_text + " " + self.copy_mode_text, self.join_text)

		self.Select_And_Copy_Story_Name(select_text = self.select_text, copy = False, first_space = False, second_space = True)

		if self.story_name != self.unjoin_name_text:
			self.join_story_name += self.story_name

			self.the_number_text = Language_Item_Definer("the", "o") + " " + Language_Item_Definer("second", "segundo")
			self.select_text = self.select_one_to_text_template.format(self.the_number_text + " " + self.copy_mode_text, self.join_text)

			self.Select_And_Copy_Story_Name(select_text = self.select_text, copy = False, first_space = False, second_space = True)

			self.join_story_name += " - " + self.story_name

			self.story_name = self.join_story_name

			self.Select_And_Copy_Story_Name(show_text = self.show_text, select = False, copy = True)

			print()

		if self.story_name == self.unjoin_name_text:
			self.join_story_names = False

	def Finish_Copying(self):
		print("-----")
		print()
		print(Language_Item_Definer("Finished copying {}", "Terminou de copiar {}").format(self.plural_copy_mode_text.lower()) + ".")
		quit()