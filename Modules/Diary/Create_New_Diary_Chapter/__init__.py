# Create_New_Diary_Chapter.py

from Diary.Diary import Diary as Diary

from Diary.Write_On_Diary import Write_On_Diary as Write_On_Diary

class Create_New_Diary_Chapter(Diary):
	def __init__(self):
		super().__init__()

		# Add to Diary (chapter) number
		self.diary_number = int(self.File.Contents(self.diary_number_file)["lines"][0])
		self.diary_number = str(self.diary_number + 1)

		# Create the new Diary file
		self.new_diary_chapter_file = self.diary_chapters_folder + self.diary_number + ".txt"
		self.File.Create(self.new_diary_chapter_file)

		# Open the new Diary file
		self.File.Open(self.new_diary_chapter_file)

		# Update Diary number file
		text_to_write = str(self.diary_number)

		if text_to_write != self.File.Contents(self.diary_number_file)["string"]:
			self.File.Edit(self.diary_number_file, text_to_write, "w")

		# Update current Diary chapter file
		text_to_write = str(self.new_diary_chapter_file)

		if text_to_write != self.File.Contents(self.current_diary_file)["string"]:
			self.File.Edit(self.current_diary_file, text_to_write, "w")

		# Write on the new Diary chapter
		Write_On_Diary()