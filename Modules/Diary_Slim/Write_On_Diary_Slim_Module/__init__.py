# Write_On_Diary_Slim_Module.py

from Diary_Slim.Diary_Slim import Diary_Slim as Diary_Slim

class Write_On_Diary_Slim_Module(Diary_Slim):
	def __init__(self, text, time = None, add_time = True, show_text = True, add_dot = True, check_file_length = True):
		super().__init__()

		self.current_diary_slim_file = self.File.Contents(self.current_diary_slim_file)["lines"][0]

		self.text = text
		self.time = time
		self.add_time = add_time
		self.show_text = show_text
		self.check_file_length = check_file_length

		if self.text[-1] != "." and add_dot == True:
			self.text += "."

		self.Write()

	def Write(self):
		if self.time == None:
			self.time = self.Date.Now()["%H:%M %d/%m/%Y"]

		text_to_append = ""

		if self.add_time == True:
			text_to_append += self.time + ":\n"

		text_to_append += self.text

		if self.check_file_length == True:
			text_to_append = "\n\n" + text_to_append

		self.File.Edit(self.current_diary_slim_file, text_to_append, "a", next_line = False)

		if self.switches["global"]["verbose"] == True:
			print()

		self.text_to_show = self.language_texts["this_text_was_written_to_the_current_diary_slim"] + ":"

		if self.switches["global"]["testing"] == True:
			self.text_to_show = self.text_to_show.replace(self.language_texts["was"], self.language_texts["was_not"])
			self.text_to_show = self.text_to_show.replace(":", " (" + self.language_texts["testing_is_true"] + "):")

		if text_to_append[0] == "\n":
			text_to_append = text_to_append[2:]

		self.text_to_show += "\n" + "[" + text_to_append + "]"

		if self.show_text == True:
			print(self.text_to_show)

	def __str__(self):
		return self.text_to_show