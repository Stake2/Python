# Unlock.py

from Script_Helper import *

from Block_Websites.Block_Websites import Block_Websites as Block_Websites
from Block_Websites.Block import Block as Block

class Re_Block(Block_Websites):
	def __init__(self):
		super().__init__()

		self.websites_to_block_backup_file = self.database_websites_folder + "To Block (Backup)" + self.dot_text
		self.websites_to_block_backup = Create_Array_Of_File(self.websites_to_block_backup_file)
		Write_To_File(self.websites_to_block_file, Stringfy_Array(self.websites_to_block_backup, add_line_break = True))
		Remove_File(self.websites_to_block_backup_file)

		Block()

		scheduler = win32com.client.Dispatch("Schedule.Service")
		scheduler.Connect()
		root_folder = scheduler.GetFolder("\\Stake2")
		root_folder.DeleteTask(self.task_name, 0)

if __name__ == "__main__":
	Re_Block()