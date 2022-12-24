# Work.py

from SproutGigs.SproutGigs import SproutGigs as SproutGigs

from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

class Work(SproutGigs):
	def __init__(self):
		super().__init__()

		self.first_time = True
		self.finish_working = False
		self.category = None

		while self.finish_working == False:
			if self.category != None:
				print("---")

			first_space = True

			if self.category == None:
				self.Select_Category()	

				if self.category["name"] in self.Social_Networks.social_networks:
					first_space = False

			self.first_time = False

			show_text = self.language_texts["category_data"] + ' "' + self.category["name"] + '"'
			select_text = self.language_texts["select_a_category_data_to_copy"]

			data_name = self.Input.Select(list(self.category["data"].keys()), show_text = show_text, select_text = select_text, first_space = first_space)["option"]

			category_data = self.category["data"][data_name]

			if data_name == "[" + self.language_texts["change_category"] + "]":
				self.Select_Category()

				if self.language_texts["finish_working"] not in data_name and self.language_texts["username"] in self.category["data"]:
					print(self.language_texts["username_of"] + " " + self.category["name"] + ":")
					print(self.category["data"][self.language_texts["username"]])
					print()

				if self.category["name"] in self.Social_Networks.social_networks:
					first_space = False

			if data_name == "[" + self.language_texts["open_category_page"] + "]":
				self.Open_Category_Tab(self.category, open = True)

				print()

			if data_name not in self.additional_options:
				if "{username}" in category_data:
					category_data = category_data.replace("username", "").format(self.category["data"][self.language_texts["username"]])

				self.Text.Copy(category_data)

				print()

			if data_name == "[" + self.language_texts["finish_working"] + "]":
				print()
				print("-----")
				print()

				print(self.language_texts["you_finished_working_on"] + ":")
				print(self.website["name"])
				print()

				Write_On_Diary_Slim_Module("Trabalhei um pouco no " + self.website["name"])

				self.finish_working = True

				quit()