# Update_Websites.py

from Code.Code import Code as Code

class Update_Websites(Code):
	def __init__(self, update_one_website = False, module_website = None):
		super().__init__()

		self.update_one_website = update_one_website
		self.module_website = module_website

		if self.module_website != None:
			self.update_one_website = True

		self.update_more_websites = False
		self.first_time = True

		self.Define_Variables()
		self.Select_Website()

		self.Open_And_Close_XAMPP(open = True)
		self.Update_Website()

		if self.update_one_website == False and self.create_website_list_to_update == False:
			self.update_more_websites = True

			i = 0
			while self.update_more_websites == True:
				self.update_more_websites = self.Input.Yes_Or_No(self.language_texts["update_more_websites"])

				if self.update_more_websites == True:
					print()

					self.Select_Website()

					print()

					self.Update_Website(open = True, close = False)

					i += 1

					self.first_time = False

				if self.update_more_websites == False:
					self.Open_And_Close_XAMPP(close = True)

		if self.update_one_website == True:
			self.Open_And_Close_XAMPP(close = True)

		self.Open_Git_Console_Window()

		print()
		print(self.large_bar)
		print()

		text = self.language_texts["you_finished_updating_the_website"]

		if len(self.websites["update"]) > 1:
			text = self.language_texts["you_finished_updating_the_websites"]

		print(text + ".")

	def Define_Variables(self):
		self.small_languages_backup = self.languages["small"].copy()

		self.languages = [
			"general",
			self.languages["full_translated"]["en"]["en"],
			self.languages["full_translated"]["pt"]["en"]
		]

		self.languages["full_translated"]["general"] = {}

		for language in self.languages["small"]:
			self.languages["full_translated"]["general"][language] = self.texts["general, title()"][language]

		self.languages["small"].insert(0, "general")
		self.languages["full"]["general"] = "General"

		self.xampp_programs = [
			"xampp-control",
			"httpd",
			"mysql",
		]

		self.websites = {
			"list": self.JSON.To_Python(self.folders["mega"]["php"]["json"]["websites"]),
			"update": {},
		}

		for language in self.languages["small"]:
			if language != "general":
				self.websites[language] = self.websites["list"][language]

		self.websites["general"] = self.websites["en"]

		self.websites["url"] = self.JSON.To_Python(self.folders["mega"]["php"]["json"]["url"])

	def Select_Website(self):
		self.websites["numbers"] = []

		if self.module_website == None:
			first_space = True

			if self.update_more_websites == True:
				first_space = False

			self.create_website_list_to_update = self.Input.Yes_Or_No(self.language_texts["create_website_list_to_update"], first_space = first_space)

			self.show_text = self.language_texts["websites, title()"]

			if self.create_website_list_to_update == False:
				self.select_text = self.language_texts["select_a_website_to_update_its_html_contents"]

				number = self.Input.Select(self.websites["en"], language_options = self.websites[self.user_language], show_text = self.show_text, select_text = self.select_text)["number"]

				self.websites["numbers"].append(number)

			if self.create_website_list_to_update == True:
				self.Create_Websites_List()

		if self.module_website != None:
			# If the module website is a string find the number of that website
			# If the module website is an integer, add it to the website numbers list
			if type(self.module_website) in [str, int]:
				number = 0
				for website in self.websites["en"]:
					if self.module_website == website or self.module_website == number:
						self.websites["numbers"].append(number)

					number += 1

			# If the module website is a list, make the website numbers list as the module website
			if type(self.module_website) == list:
				self.websites["numbers"] = self.module_website

		# Add websites to update dictionary in websites dictionary
		for number in self.websites["numbers"]:
			website = self.websites["en"][number]

			# Add key
			self.websites["update"][website] = {
				"number": number,
			}

			# Add website titles per language
			for language in self.languages["small"]:
				self.websites["update"][website][language] = self.websites[language][number]

			# Add website links per language
			self.websites["update"][website]["links"] = {}

			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				self.websites["update"][website]["links"][language] = self.websites["url"]["generate_template"].format(full_language, self.websites["update"][website]["en"])

	def Create_Websites_List(self):
		# Define local websites dictionary
		websites = {
			"en": self.websites["en"].copy(),
			self.user_language: self.websites[self.user_language].copy(),
			"numbers": [],
			"select_list": [],
		}

		# Add "finish_selection" text to local websites dictionary
		websites["en"].append("[" + self.texts["finish_selection"]["en"] + "]")
		websites[self.user_language].append("[" + self.language_texts["finish_selection"] + "]")

		# Define select text
		self.select_text = self.language_texts["select_a_website_to_add_it_to_the_list"]

		# Wait for user to finish selecting websites
		dictionary = {
			"option": "",
		}

		while dictionary["option"] != "[" + self.texts["finish_selection"]["en"] + "]":
			print()
			print(self.Language.language_texts["list, title()"] + ":")
			self.JSON.Show(websites["select_list"])

			# Select website from the list and return its number
			dictionary = self.Input.Select(websites["en"], language_options = websites[self.user_language], show_text = self.show_text, select_text = self.select_text)

			if dictionary["option"] != "[" + self.texts["finish_selection"]["en"] + "]":
				# Add selected website number to website numbers list
				# (It haves to iterate through the English websites list to find the correct number because the local website list is of a different length)
				number = 0
				for website in self.websites["en"]:
					if dictionary["option"] == website:
						websites["numbers"].append(number)

					number += 1

				# Add selected website to select list
				websites["select_list"].append(dictionary["language_option"])

				# Remove selected website from list
				websites["en"].remove(dictionary["option"])
				websites[self.user_language].remove(dictionary["language_option"])

		# Define the "numbers" key of the "website" dictionary as the list that the user created
		self.websites["numbers"] = websites["numbers"]

	def Open_And_Close_XAMPP(self, open = False, close = False):
		if open == True:
			if self.switches["testing"] == False:
				self.File.Open(self.root_folders["xampp"]["xampp-control"])

				self.Date.Sleep(4)

		if close == True:
			if self.switches["testing"] == False:
				for program in self.xampp_programs:
					self.File.Close(program)

	def Update_Website(self, open = True, close = True):
		text = self.language_texts["updating_this_website"]

		if len(self.websites["update"]) > 1:
			text = self.language_texts["updating_these_websites"]

		# Show website info
		print()
		print(self.large_bar)
		print()
		print(text + ":")

		if len(self.websites["update"]) == 1:
			key = list(self.websites["update"].keys())[0]
			website = self.websites["update"][key][self.user_language]

			print("\t" + website)

		if len(self.websites["update"]) > 1:
			for key in self.websites["update"]:
				website_title = self.websites["update"][key][self.user_language]

				print("\t" + website_title)

		# Open website links to update them
		for key in self.websites["update"]:
			website = self.websites["update"][key]

			if len(self.websites["update"]) > 1:
				# Show website info for current website
				print()
				print(self.large_bar)
				print()
				print(self.language_texts["updating_this_website"] + ":")
				print(website[self.user_language])

			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				link = website["links"][language]

				print()
				print("-")
				print()
				print(self.language_texts["website_link"] + ":")
				print(link)
				print()
				print(self.Language.language_texts["language, title()"] + ":")
				print(self.languages["full_translated"][language][self.user_language])

				if self.switches["testing"] == False:
					self.File.Open(link)

					self.Date.Sleep(5)

		print()
		print(self.large_bar)

		self.Input.Type(self.language_texts["press_enter_when_the_pages_finish_loading"])

	def Open_Git_Console_Window(self):
		files = self.Folder.Contents(self.folders["apps"]["shortcuts"]["white_shortcuts"])["file"]["list"]

		for file in files:
			if "GitHub" in file:
				git_bat_file = file

		if self.switches["testing"] == False:
			self.Text.Open_Link(git_bat_file)