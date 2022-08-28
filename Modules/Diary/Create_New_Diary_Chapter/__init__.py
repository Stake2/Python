# Create_New_Diary_Chapter.py

from Script_Helper import *

from Diary.Diary import Diary as Diary

from Diary.Write_On_Diary import Write_On_Diary as Write_On_Diary

class Create_New_Diary_Chapter(Diary):
	def __init__(self):
		super().__init__()

		self.diary_number = int(Create_Array_Of_File(self.diary_number_file)[0])
		self.diary_number = str(self.diary_number + 1)

		self.new_diary_chapter_file = self.diary_chapters_folder + self.diary_number + self.dot_text
		Create_Text_File(self.new_diary_chapter_file, self.global_switches)

		Open_Text_File(self.new_diary_chapter_file)

		text_to_write = str(self.diary_number)

		if text_to_write != Read_String(self.diary_number_file):
			Write_To_File(self.diary_number_file, text_to_write, self.global_switches)

		text_to_write = str(self.new_diary_chapter_file)

		if text_to_write != Read_String(self.current_diary_file):
			Write_To_File(self.current_diary_file, text_to_write, self.global_switches)

		Write_On_Diary(self.new_diary_chapter_file)