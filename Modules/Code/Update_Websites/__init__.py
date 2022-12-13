# Update_Websites.py

from Code.Code import Code as Code

class Update_Websites(Code):
	def __init__(self, parameter_switches = None, update_one_website = False, module_website = None):
		super().__init__(parameter_switches)

		self.update_one_website = update_one_website
		self.module_website = module_website

		if self.module_website != None:
			self.update_one_website = True

		self.Define_Variables()
		self.Select_Website()

		self.Open_And_Close_XAMPP(open = True)
		self.Update_Website()

		if self.update_one_website == False:
			self.update_more_websites = True
			self.first_time = False

			i = 0
			while self.update_more_websites == True:
				self.update_more_websites = self.Input.Yes_Or_No(self.language_texts["update_more_websites"])

				if self.update_more_websites == True:
					print()

					self.Select_Website()

					print()

					self.Update_Website(open = True, close = False)

					i += 1

				if self.update_more_websites == False:
					self.Open_And_Close_XAMPP(close = True)

		if self.update_one_website == True:
			self.Open_And_Close_XAMPP(close = True)

		self.Open_Git_Console_Window()

	def Define_Variables(self):
		self.small_languages_backup = self.small_languages.copy()

		self.languages = [
			"general",
			self.translated_languages["en"]["en"],
			self.translated_languages["pt"]["en"],
		]

		self.translated_languages["general"] = {}

		for language in self.small_languages:
			self.translated_languages["general"][language] = self.texts["general"][language]

		self.small_languages.insert(0, "general")
		self.full_languages["general"] = self.language_texts["general"]

		self.xampp_programs = [
			"xampp-control",
			"httpd",
			"mysql",
		]

		self.websites = {
			"list": self.Language.JSON_To_Python(self.mega_folders["php"]["website"])["list"],
		}

		for language in self.small_languages:
			if language != "general":
				self.websites[language] = self.websites["list"][language]

		self.websites["general"] = self.websites["en"]

		self.websites["url"] = self.Language.JSON_To_Python(self.mega_folders["php"]["json"]["url"])

	def Select_Website(self):
		if self.module_website == None:
			self.show_text = self.language_texts["websites"]
			self.select_text = self.language_texts["select_a_website_to_update_its_html_contents"]

			self.website_number = self.Input.Select(self.websites["en"], self.websites[self.user_language], show_text = self.show_text, select_text = self.select_text)["number"]

		if self.module_website != None:
			self.websites_number = 0
			for website in self.websites["en"]:
				if self.module_website == website:
					self.website_number = self.websites_number

				self.websites_number += 1

		self.website = {}

		for language in self.small_languages:
			self.website[language] = self.websites[language][self.website_number]

	def Open_And_Close_XAMPP(self, open = False, close = False):
		if open == True:
			if self.global_switches["testing"] == False:
				self.File.Open(self.root_folders["xampp"]["xampp-control"])

				self.Date.Sleep(3)

		if close == True:
			if self.global_switches["testing"] == False:
				for program in self.xampp_programs:
					self.File.Close(program)

	def Update_Website(self, open = True, close = True):
		print()
		print(self.large_bar)
		print()
		print(self.language_texts["updating_this_website"] + ":")
		print(self.website[self.user_language])

		self.website["links"] = {}

		for language in self.small_languages:
			full_language = self.full_languages[language]

			self.website["links"][language] = self.websites["url"]["generate_template"].format(self.website[language], full_language)

			print()
			print("-")
			print()
			print(self.language_texts["website_link"] + ":")
			print(self.website["links"][language])
			print()
			print(self.Language.language_texts["language, title()"] + ":")
			print(self.translated_languages[language][self.user_language])

			if self.global_switches["testing"] == False:
				self.File.Open(self.website["links"][language])

				self.Date.Sleep(5)

		print()
		print(self.large_bar)

		self.Input.Type(self.language_texts["press_enter_when_the_pages_finish_loading"])

	def Open_Git_Console_Window(self):
		files = self.Folder.Contents(self.apps_folders["shortcuts"]["white_shortcuts"])["file"]["list"]

		for file in files:
			if "GitHub" in file:
				git_bat_file = file

		if self.global_switches["testing"] == False:
			self.Text.Open_Link(git_bat_file)