# Unblock.py

from Block_Websites.Block_Websites import Block_Websites as Block_Websites
from Block_Websites.Block import Block as Block

class Unblock(Block_Websites):
	def __init__(self, options = None):
		super().__init__()

		self.options = options

		if self.options != None:
			self.website_to_unlock = self.options

			if type(self.options) == dict:
				self.website_to_unlock = [self.website_to_unlock["Website"]]

		self.in_working_hours = Block(show_text = False, block = False).in_working_hours

		if self.in_working_hours == True:
			self.Choose_Website()
			self.Unblock()

		if self.in_working_hours == False:
			print(self.language_texts["you_are_not_in_working_time_all_websites_are_unlocked"] + ".")
			print()

	def Choose_Website(self):
		if self.options == None:
			show_text = self.language_texts["websites, title()"]
			select_text = self.language_texts["select_a_website_to_unlock"]

			for website in self.websites_to_block:
				if website not in self.File.Contents(self.hosts_file)["string"]:
					self.websites_to_block.remove(website)

			self.website_to_unlock = self.Input.Select(self.websites_to_block, show_text = show_text, select_text = select_text)["option"]

		if self.options == None:
			print()

		text = self.language_texts["this_website_is_unblocked_for_{}_minutes"]

		if len(self.website_to_unlock) > 1:
			text = self.language_texts["these_websites_are_unblocked_for_{}_minutes"]

		print(text.format(self.hour_config["Update time"]) + ":")

		if len(self.website_to_unlock) == 1:
			print("\t" + self.website_to_unlock[0])

		if len(self.website_to_unlock) > 1:
			for website in self.website_to_unlock:
				print("\t" + website)

		if self.options != None:
			print()

	def Unblock(self):
		Block(show_text = False, website_to_unlock = self.website_to_unlock)