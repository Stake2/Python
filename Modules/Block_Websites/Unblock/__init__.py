# Unblock.py

from Block_Websites.Block_Websites import Block_Websites as Block_Websites
from Block_Websites.Block import Block as Block

class Unblock(Block_Websites):
	def __init__(self, options = None, time = None, first_space = True, second_space = True):
		super().__init__()

		self.options = options

		if self.options != None:
			self.website_to_unlock = self.options

			if type(self.website_to_unlock) == str:
				self.website_to_unlock = [self.website_to_unlock]

			if type(self.website_to_unlock) == dict:
				self.website_to_unlock = [self.website_to_unlock["Website"]]

		self.time = time

		if self.time == None:
			self.time = self.hour_config["Update time"]

		if first_space == True:
			print()

		self.in_working_hours = Block(show_text = False, block = False).in_working_hours

		if self.in_working_hours == True:
			self.Choose_Website()
			self.Unblock()

		if self.in_working_hours == False:
			print(self.language_texts["you_are_not_in_working_time_all_websites_are_unlocked"] + ".")

		if second_space == True:
			print()

	def Choose_Website(self):
		if self.options == None:
			show_text = self.language_texts["websites, title()"]
			select_text = self.language_texts["select_a_website_to_unlock"]

			for website in self.websites_to_block:
				if website not in self.File.Contents(self.hosts_file)["string"]:
					self.websites_to_block.remove(website)

			self.website_to_unlock = self.Input.Select(self.websites_to_block, show_text = show_text, select_text = select_text)["option"]

		self.text = self.language_texts["this_website_is_unblocked_for_{}"]

		if len(self.website_to_unlock) > 1:
			self.text = self.language_texts["these_websites_are_unblocked_for_{}"]

		if self.time < 60:
			self.text += " " + self.language_texts["minutes"]

		time = self.time

		if self.time >= 60:
			time = self.time // 60

			self.text += " "

			if time == 1:
				self.text += self.language_texts["hour"]

			if time > 1:
				self.text += self.language_texts["hours"]

		self.text = self.text.format(time) + ":" + "\n"

		for website in self.website_to_unlock:
			self.text += "\t" + website

			if website != self.website_to_unlock[-1]:
				self.text += "\n"

		print(self.text)

	def Unblock(self):
		Block(show_text = False, website_to_unlock = self.website_to_unlock, time = self.time, text = self.text)