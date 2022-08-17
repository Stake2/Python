# Help_With_Studying.py

from Script_Helper import *

from Study.Study import Study as Study

from Code.Help_With_Coding import Help_With_Coding as Help_With_Coding

class Help_With_Studying(Study):
	def __init__(self):
		super().__init__()

		self.Select()
		self.Open_Course()
		self.Register_On_Diary_Slim()

	def Select(self):
		self.choice_text = self.module_texts["Select one course"]
		self.course = Select_Choice_From_List(self.courses, alternative_choice_text = self.choice_text, return_first_item = True, add_none = True, first_space = False, second_space = False)

		self.course_data = self.course_data_list[self.course]

		self.course_dict = {}
		self.course_dict["Programming Language"] = self.course_data["Programming Language"]
		self.course_dict["Mode"] = self.course, self.course_data["Mode Number"]
		self.course_dict["Helper"] = self.course, self.course_data["Helper"]
		print()

	def Open_Course(self):
		if self.course_data["Helper"] == "Help_With_Coding":
			Help_With_Coding(self.global_switches, self.course_dict)

		if self.course_data["Helper"] == "":
			if self.global_switches["testing_script"] == False:
				globals()[self.course_data["Mode Number"]](self.course_dict["Programming Language"])

	def Register_On_Diary_Slim(self):
		from Diary_Slim.Write_On_Diary_Slim import Write_On_Diary_Slim as Write_On_Diary_Slim

		if self.global_switches["testing_script"] == False:
			Write_On_Diary_Slim(self.course)