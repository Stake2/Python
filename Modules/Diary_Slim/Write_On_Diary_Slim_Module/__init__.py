# Write_On_Diary_Slim_Module.py

from Script_Helper import *

from Diary_Slim.Diary_Slim import Diary_Slim as Diary_Slim

class Write_On_Diary_Slim_Module(Diary_Slim):
	def __init__(self, text_to_write, custom_time = None, parameter_switches = None, show_text = True, add_dot = True, add_time = True, write = False, return_show_text = False):
		super().__init__()

		self.current_diary_slim_file = Create_Array_Of_File(self.current_diary_slim_file)[0]

		self.text_to_write = text_to_write

		self.custom_time = custom_time
		self.parameter_switches = parameter_switches
		self.show_text = show_text
		self.add_dot = add_dot
		self.add_time = add_time
		self.write = write
		self.return_show_text = return_show_text

		self.local_switches = self.global_switches

		if self.parameter_switches != None:
			self.local_switches["write_to_file"] = self.parameter_switches["write_to_file"]

		if self.add_dot == True and self.text_to_write[-1] != ".":
			self.text_to_write += "."

		self.Write()

	def Write(self):
		self.current_time = time.strftime("%H:%M %d/%m/%Y")

		if self.custom_time != None:
			self.current_time = self.custom_time

		self.current_time = self.current_time + ":\n"

		if self.add_time == False:
			self.current_time = ""

		text_to_append = self.current_time + self.text_to_write

		if self.write == False:
			text_to_append = "\n\n" + text_to_append

		Append_To_File(self.current_diary_slim_file, text_to_append, self.local_switches, check_file_length = False)

		self.text_to_show = Language_Item_Definer("This text was written on the current Diary Slim", "Este texto foi escrito no Diário Slim atual") + ":"

		if self.local_switches["write_to_file"] == False:
			self.text_to_show = self.text_to_show.replace(Language_Item_Definer("was", "foi"), Language_Item_Definer("was not", "não foi"))
			self.text_to_show = self.text_to_show.replace(":", ' ("write_to_file" ' + Language_Item_Definer('is "False"', 'é "False"') + "):")

		self.text_to_show += "\n" + "[" + self.current_time + self.text_to_write + "]"

		if self.show_text == True:
			print(self.text_to_show)

	def __str__(self):
		if self.return_show_text == True:
			return self.text_to_show