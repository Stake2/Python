# Register_Task_Module.py

from Script_Helper import *

from Tasks.Tasks import Tasks as Tasks
from Tasks.Register_Task import Register_Task as Register_Task

class Register_Task_Module(Tasks):
	def __init__(self, experienced_media_type, english_task_description, portuguese_task_description, experienced_media_time, show_text = True, skip_input = False, parameter_switches = None):
		super().__init__(parameter_switches)

		self.parameter_switches = parameter_switches

		self.experienced_media_type = experienced_media_type
		self.english_task_description = english_task_description
		self.portuguese_task_description = portuguese_task_description
		self.experienced_media_time = experienced_media_time
		self.show_text = show_text
		self.skip_input = skip_input

		self.task_data = {
		"experienced_media_type": self.experienced_media_type,
		"english_task_description": self.english_task_description,
		"portuguese_task_description": self.portuguese_task_description,
		"experienced_media_time": self.experienced_media_time,
		}

		Register_Task(run_as_module = True, task_data = self.task_data, show_text = show_text, skip_input = skip_input, parameter_switches = parameter_switches)