# Unblock.py

from Script_Helper import *

from Block_Websites.Block_Websites import Block_Websites as Block_Websites
from Block_Websites.Block import Block as Block

class Unblock(Block_Websites):
	def __init__(self, module_execution = False, options = None):
		super().__init__()

		self.mode = "User"

		self.module_execution = module_execution
		self.options = options

		if self.module_execution == True:
			self.mode = "Modules"

			if type(self.options) == dict:
				self.website_to_unlock = self.options["Website"]

			if type(self.options) == str:
				self.website_to_unlock = self.options

		if Block(False).in_working_hours == True:
			self.Choose_Website()
			self.Unblock()

		if Block(False).in_working_hours == False:
			print(self.not_in_working_hours_text + ".")
			print()

	def Choose_Website(self):
		self.allowed_to_unlock = self.allowed_to_unlock[self.mode]

		self.websites_allowed_to_unlock = []

		for website in self.websites_to_block:
			if website in list(self.allowed_to_unlock.keys()):
				self.websites_allowed_to_unlock.append(website)

		if self.module_execution == False:
			self.choice_text = Language_Item_Definer("Select a website to unlock", "Selecione um site para liberar")
			self.website_to_unlock = Select_Choice_From_List(self.websites_allowed_to_unlock, local_script_name, self.choice_text, second_choices_list = self.websites_allowed_to_unlock, return_second_item_parameter = True, return_number = True, add_none = True, first_space = False, second_space = False)[0]

		self.reason_to_unlock = self.allowed_to_unlock[self.website_to_unlock].split(", ")[Language_Item_Definer(0, 1)]

		if self.module_execution == False:
			print()

		print(self.website_unblocked_text + ": ")
		print(self.website_to_unlock)
		print()
		print(self.reason_to_unlock_text + ": ")
		print(self.reason_to_unlock + ".")

		if self.module_execution == True:
			print()

	def Unblock(self):
		self.module_folder_class = self.module_folder + "Unblock/"

		self.reblock_python_window_file = self.module_folder_class + "Re-Block.pyw"
		Create_Text_File(self.reblock_python_window_file, self.global_switches["create_files"])

		self.websites_to_block_backup_file = self.database_websites_folder + "To Block (Backup)" + self.dot_text
		Create_Text_File(self.websites_to_block_backup_file, self.global_switches["create_files"])

		Write_To_File(self.websites_to_block_backup_file, Stringfy_Array(self.websites_to_block, add_line_break = True))

		for website in self.websites_to_block:
			if website == self.website_to_unlock:
				self.websites_to_block.remove(website)

		Write_To_File(self.websites_to_block_file, Stringfy_Array(self.websites_to_block, add_line_break = True), self.global_switches)

		Block(show_text = False)
		Create_Scheduled_Task(self.task_name, self.reblock_python_window_file)