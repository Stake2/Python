# Block.py

from Block_Websites.Block_Websites import Block_Websites as Block_Websites

class Block(Block_Websites):
	def __init__(self, show_text = True, block = True, website_to_unlock = None, time = None, text = None):
		super().__init__()

		self.show_text = show_text
		self.block = block
		self.website_to_unlock = website_to_unlock
		self.time = time
		self.text = text

		if self.time == None:
			self.time = self.hour_config["Update time"]

		self.Check_Time()
		self.Mount_Text_String()

		if self.block == True:
			self.Write_To_Hosts_File()
			self.Log()

			if self.show_text == True:
				self.Show()

		self.Update_Python_File()

	def Check_Time(self):
		self.current_hour = int(self.date["hour"])
		self.week_day = int(self.date["weekday"])

		self.in_working_hours = False

		if self.current_hour >= self.hour_config["Start blocking"] and self.current_hour <= self.hour_config["Stop blocking"]:
			self.in_working_hours = True

	def Mount_Text_String(self):
		self.text_to_write = self.hosts_file_header + self.texts["header"]

		# Add first maps, getting them from "self.map_dict"
		for map_dict in self.map_dict:
			map_list = self.map_dict[map_dict]

			if map_list != []:
				self.text_to_write += "# " + map_dict + "\n"

				for map in map_list:
					self.text_to_write += self.texts["redirect_ip_space"] + map

					if map != map_list[-1]:
						self.text_to_write += "\n"

					if map == map_list[-1] and map_dict != list(self.map_dict.keys())[-1]:
						self.text_to_write += "\n\n"

		if self.website_to_unlock != None:
			if type(self.website_to_unlock) == str:
				self.websites_to_block.remove(self.website_to_unlock)

			if type(self.website_to_unlock) == list:
				for website in self.website_to_unlock:
					if website in self.websites_to_block:
						self.websites_to_block.remove(website)

		self.websites_to_block_text = ""

		if self.websites_to_block == []:
			self.websites_to_block_text = self.texts["all_websites_are_unlocked_header"]

		# Add maps of websites to block from "self.websites_to_block"
		for website in self.websites_to_block:
			self.websites_to_block_text += "# " + website + "\n"

			domains = self.domains[website]

			for domain in domains:
				self.websites_to_block_text += self.texts["redirect_ip_space"] + domain

				if domain != domains[-1]:
					self.websites_to_block_text += "\n"

			if website != self.websites_to_block[-1]:
				self.websites_to_block_text += "\n\n"

	def Write_To_Hosts_File(self):
		if self.in_working_hours == True:
			self.text_to_write += "\n\n" + self.websites_to_block_text

		self.File.Edit(self.hosts_file, self.text_to_write, "w")

	def Log(self):
		self.key = "blocked"
		self.not_text = ""

		if self.in_working_hours == False:
			self.key = "unlocked"
			self.not_text = " " + self.language_texts["not"]

		self.log_text = self.texts["log"].format(self.language_texts[self.key + "_websites"], self.time, self.date["%H:%M %d/%m/%Y"])

		if self.website_to_unlock != None:
			self.log_text += "\n\n" + self.text

		self.File.Edit(self.log_file, self.log_text, "w")

	def Show(self):
		print()
		print(self.language_texts["blocking_state"] + ":")
		print(self.language_texts["the_websites_are_{}_because_you_are{}_in_working_time"].format(self.language_texts[self.key], self.not_text) + ".")

	def Update_Python_File(self):
		self.block_python_code = self.File.Contents(self.apps_folders["modules"][self.module["key"]]["block"]["__init__"])["string"]

		text = self.block_python_code + "\n\n" + 'if __name__ == "__main__":' + "\n\t" + "Block()"

		self.File.Edit(self.apps_folders["modules"][self.module["key"]]["block"]["block"], text, "w")

		self.texts["task_name"] = "Block Websites"

		self.Date.Schedule_Task(self.texts["task_name"], self.apps_folders["modules"][self.module["key"]]["block"]["block"], time_from_now = self.time)

if __name__ == "__main__":
	Block()