# Write_On_Diary.py

from Script_Helper import *

from Diary.Diary import Diary as Diary

class Write_On_Diary(Diary):
	def __init__(self, custom_file = None):
		super().__init__()

		self.custom_file = custom_file

		self.diary_chapter_file = self.current_diary_file

		if self.custom_file != None:
			self.diary_chapter_file = self.custom_file

		print()
		print(Language_Item_Definer("Current Diary file", "Arquivo atual do Diário") + ":")
		print(self.current_diary_text_file)

		self.Select()

	def Select(self):
		self.choice_text = Language_Item_Definer("Select a character to write as", "Selecione um personagem para escrever como ele")
		self.selected_character = Select_Choice_From_List(self.characters.values(), local_script_name, self.choice_text, second_choices_list = self.characters, return_second_item_parameter = True, add_none = True, return_number = True)[0]

		self.Type(self.selected_character)

	def Type(self, character):
		self.character = self.characters[character]

		self.character_format_text = self.character_format_texts[self.character]
		self.character_format_text_no_dot = self.character_format_text.replace(".", "")

		self.character_text = None

		while self.character_text not in self.finish_texts:
			self.character_text = Text_Writer(self.character + ": ", finish_text = "default_list", capitalize_lines = True, auto_add_dots = False, accept_enter = False, first_space = False)

			if self.character_text not in self.characters.values():
				self.local_character_format_text = self.character_format_text

				if self.character_text[-1] in ["?", "!", ":", ";"]:
					self.local_character_format_text = self.character_format_text_no_dot

				text_to_append = time.strftime("%H:%M %d/%m/%Y") + ":" + "\n" + self.local_character_format_text.format(self.character, Capitalize_First_Letter(self.character_text))

				if len(Create_Array_Of_File(self.diary_chapter_file)) != 0:
					text_to_append = "\n" + text_to_append

				Append_To_File(self.diary_chapter_file, text_to_append, self.global_switches, check_file_length = True)

			if self.character_text in self.characters.values():
				self.Type(self.character_text)