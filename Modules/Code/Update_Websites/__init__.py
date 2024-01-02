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

		if (
			self.update_one_website == False and
			self.create_website_list_to_update == False
		):
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

		if (
			self.update_one_website == True or
			self.update_one_website == False and
			self.create_website_list_to_update == True
		):
			self.Open_And_Close_XAMPP(close = True)

		self.Open_Git_Console_Window()

		print()
		print(self.large_bar)
		print()

		website = self.websites["Updated website"]

		text = self.language_texts["you_finished_updating_the_website"] + ' "' + website + '".'

		if len(self.websites["Update"]) > 1:
			text = self.language_texts["you_finished_updating_these_websites"] + ":" + "\n"

			for key, website in self.websites["Update"].items():
				text += "\t" + website[self.user_language]

				if key != list(self.websites["Update"].keys())[-1]:
					text += "\n"

		print(text)

	def Define_Variables(self):
		self.small_languages_backup = self.languages["small"].copy()

		self.languages["full_translated"]["General"] = {}

		for language in self.languages["small"]:
			self.languages["full_translated"]["General"][language] = self.JSON.Language.texts["general, title()"][language]

		self.languages["small"].insert(0, "General")
		self.languages["full"]["General"] = "General"

		self.xampp_programs = [
			"xampp-control",
			"httpd",
			"mysql"
		]

		self.websites = self.JSON.To_Python(self.folders["Mega"]["php"]["json"]["websites"])
		self.websites["Update"] = {}

		for language in self.languages["small"]:
			if language != "General":
				for website in self.websites["List"][language]:
					if website in self.websites["Remove from websites tab"]:
						self.websites["List"][language].remove(website)

		self.websites["List"]["General"] = self.websites["List"]["en"]

		self.websites["URL"] = self.JSON.To_Python(self.folders["Mega"]["php"]["json"]["url"])

	def Select_Website(self):
		self.websites["Numbers"] = []

		if self.module_website == None:
			first_space = True

			if self.update_more_websites == True:
				first_space = False

			self.create_website_list_to_update = self.Input.Yes_Or_No(self.language_texts["create_website_list_to_update"], first_space = first_space)

			self.show_text = self.language_texts["websites, title()"]

			if self.create_website_list_to_update == False:
				self.select_text = self.language_texts["select_a_website_to_update_its_html_contents"]

				number = self.Input.Select(self.websites["List"]["en"], language_options = self.websites["List"][self.user_language], show_text = self.show_text, select_text = self.select_text)["number"]

				self.websites["Numbers"].append(number)

			if self.create_website_list_to_update == True:
				self.Create_Websites_List()

		if self.module_website != None:
			# If the module website is a string or an integer, find the number of that website
			if type(self.module_website) in [str, int]:
				number = 0
				for website in self.websites["List"]["en"]:
					if self.module_website == website or self.module_website == number:
						self.websites["Numbers"].append(number)

					number += 1

			# If the module website is a list, make the website numbers list as the module website
			if type(self.module_website) == list:
				self.websites["Numbers"] = self.module_website

		# Add websites to update dictionary in websites dictionary
		for number in self.websites["Numbers"]:
			website = self.websites["List"]["en"][number]

			# Add key
			self.websites["Update"][website] = {
				"Number": number
			}

			# Add website titles per language
			for language in self.languages["small"]:
				self.websites["Update"][website][language] = self.websites["List"][language][number]

			# Add website links per language
			self.websites["Update"][website]["links"] = {}

			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				self.websites["Update"][website]["links"][language] = self.websites["URL"]["generate_template"].format(self.websites["Update"][website]["en"], full_language)

	def Create_Websites_List(self):
		# Define local websites dictionary
		websites = {
			"List": {
				"en": self.websites["List"]["en"].copy(),
				self.user_language: self.websites["List"][self.user_language].copy()
			},
			"Numbers": [],
			"Select list": []
		}

		# Add "finish_selection" text to local websites dictionary
		websites["List"]["en"].append("[" + self.texts["finish_selection"]["en"] + "]")
		websites["List"][self.user_language].append("[" + self.language_texts["finish_selection"] + "]")

		# Define select text
		self.select_text = self.language_texts["select_a_website_to_add_it_to_the_list"]

		# Wait for user to finish selecting websites
		dictionary = {
			"option": ""
		}

		while dictionary["option"] != "[" + self.texts["finish_selection"]["en"] + "]":
			print()
			print(self.large_bar)
			print()
			print(self.JSON.Language.language_texts["list, title()"] + ":")

			for website in websites["Select list"]:
				print("\t" + website)

			# Select website from the list and return its number
			dictionary = self.Input.Select(websites["List"]["en"], language_options = websites["List"][self.user_language], show_text = self.show_text, select_text = self.select_text)

			if dictionary["option"] != "[" + self.texts["finish_selection"]["en"] + "]":
				# Add selected website number to website numbers list
				# (It haves to iterate through the English websites list to find the correct number because the local website list is of a different length)
				number = 0
				for website in self.websites["List"]["en"]:
					if dictionary["option"] == website:
						websites["Numbers"].append(number)

					number += 1

				# Add selected website to select list
				websites["Select list"].append(dictionary["language_option"])

				# Remove selected website from list
				websites["List"]["en"].remove(dictionary["option"])
				websites["List"][self.user_language].remove(dictionary["language_option"])

		# Define the "numbers" key of the "website" dictionary as the list that the user created
		self.websites["Numbers"] = websites["Numbers"]

	def Open_And_Close_XAMPP(self, open = False, close = False):
		if open == True:
			if self.switches["testing"] == False:
				self.System.Open(self.folders["root"]["xampp"]["xampp-control"])

				self.Date.Sleep(4)

		if close == True:
			if self.switches["testing"] == False:
				for program in self.xampp_programs:
					self.File.Close(program)

	def Update_Website(self, open = True, close = True):
		text = self.language_texts["updating_this_website"]

		if len(self.websites["Update"]) > 1:
			text = self.language_texts["updating_these_websites"]

		# Show website info
		print()
		print(self.large_bar)
		print()
		print(text + ":")

		self.websites["Updated website"] = ""

		if len(self.websites["Update"]) == 1:
			key = list(self.websites["Update"].keys())[0]

			website = self.websites["Update"][key][self.user_language]

			self.websites["Updated website"] = website

			print("\t" + website)

		if len(self.websites["Update"]) > 1:
			for key in self.websites["Update"]:
				website_title = self.websites["Update"][key][self.user_language]

				print("\t" + website_title)

		# Open website links to update them
		i = 1
		for key in self.websites["Update"]:
			website = self.websites["Update"][key]

			self.websites["Updated website"] = website[self.user_language]

			if len(self.websites["Update"]) > 1:
				# Show website info for current website
				print()
				print(self.large_bar)
				print()
				print(self.language_texts["website, title()"] + ":")
				print("\t" + str(i) + "/" + str(len(list(self.websites["Update"].keys()))))
				print()
				print(self.language_texts["updating_this_website"] + ":")
				print("\t" + website[self.user_language])

			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				link = website["links"][language]

				if self.switches["testing"] == False:
					self.System.Open(link, verbose = False)

				self.Date.Sleep(1)

			if key != list(self.websites["Update"].keys())[-1]:
				self.Input.Type(self.JSON.Language.language_texts["continue, title()"])

			i += 1

		print()
		print(self.large_bar)

		self.Input.Type(self.language_texts["press_enter_when_the_pages_finish_loading"])

	def Open_Git_Console_Window(self):
		files = self.Folder.Contents(self.folders["apps"]["shortcuts"]["root"])["file"]["list"]

		for file in files:
			if "GitHub" in file:
				git_bat_file = file

		if self.switches["testing"] == False:
			self.Text.Open_Link(git_bat_file)