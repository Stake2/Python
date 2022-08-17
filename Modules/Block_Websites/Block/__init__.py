# Block.py

from Script_Helper import *

from datetime import datetime as dt

from Block_Websites.Block_Websites import Block_Websites as Block_Websites

class Block(Block_Websites):
	def __init__(self, show_text = True, module_execution = False):
		super().__init__()

		self.show_text = show_text
		self.module_execution = module_execution

		self.Check_Time()
		self.Mount_Text_String()
		self.Write_To_Hosts_File()
		self.Log()

		if self.show_text == True:
			self.Show()

		self.Update_Python_File()

	def Check_Time(self):
		self.current_hour = int(dt.now().hour)
		self.week_day = int(dt.now().weekday())

		self.in_working_hours = False

		if self.current_hour >= self.hour_config["Start Blocking"] and self.current_hour <= self.hour_config["Stop Blocking"]:
			self.in_working_hours = True

	def Mount_Text_String(self):
		self.text_to_write = self.hosts_file_header

		# Add first maps, getting them from "self.map_dict"
		for map_dict in self.map_dict:
			map_list = self.map_dict[map_dict]

			if map_list != []:
				self.text_to_write += "# " + map_dict + "\n"

				for map in map_list:
					self.text_to_write += self.redirect_ip_space + map

					if map != map_list[-1]:
						self.text_to_write += "\n"

					if map == map_list[-1] and map_dict != list(self.map_dict.keys())[-1]:
						self.text_to_write += "\n\n"

		self.websites_to_block_text = self.websites_to_block_header

		# Add maps of websites to block from "self.websites_to_block"
		for website in self.websites_to_block:
			self.domain_file = self.domain_files[website]
			self.domains = Create_Array_Of_File(self.domain_file)

			self.websites_to_block_text += "# " + website + "\n"

			for domain in self.domains:
				self.websites_to_block_text += self.redirect_ip_space + domain

				if domain != self.domains[-1]:
					self.websites_to_block_text += "\n"

				if domain == self.domains[-1] and website != self.websites_to_block[-1]:
					self.websites_to_block_text += "\n\n"

	def Write_To_Hosts_File(self):
		if self.in_working_hours == True:
			self.text_to_write += "\n" + self.websites_to_block_text

		if Read_String(self.hosts_file) != self.text_to_write:
			Write_To_File(self.hosts_file, self.text_to_write, self.global_switches)

	def Log(self):
		self.key = "Unlocked"

		if self.in_working_hours == True:
			self.key = "Blocked"

		self.now = time.strftime("%H:%M %d/%m/%Y")

		self.log_text = self.log_texts["Log"].format(self.log_texts[self.key], self.hour_config["Update Time"], self.now)

		if Read_String(self.log_file) != self.log_text:
			Write_To_File(self.log_file, self.log_text, self.global_switches)

	def Show(self):
		print(self.log_texts["Blocking State"][:-1])
		print(self.log_texts[self.key] + ".")

	def Update_Python_File(self):
		self.module_folder_class = self.module_folder + "Block/"

		self.block_python_window_file = self.module_folder_class + "Block.pyw"
		Create_Text_File(self.block_python_window_file, self.global_switches["create_files"])

		self.block_python_file = self.module_folder_class + "__init__.py"

		self.block_python_code = Read_String(self.block_python_file)

		text = self.block_python_code + "\n\n" + 'if __name__ == "__main__":' + "\n\t" + "Block()"

		if Read_String(self.block_python_window_file) != text:
			Write_To_File(self.block_python_window_file, text, self.global_switches)

		self.task_name = "Block Websites"
		Create_Scheduled_Task(self.task_name, self.block_python_window_file, self.hour_config["Update Time"])