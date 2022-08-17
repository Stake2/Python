# Create_New_Character_Diary_Text_File.py

from Script_Helper import *

from Project_Zomboid_Manager.Project_Zomboid_Manager import Project_Zomboid_Manager as Project_Zomboid_Manager

class Create_New_Character_Diary_Text_File(Project_Zomboid_Manager):
	def __init__(self):
		super().__init__()

		self.diary_template_text = "Hoje é dia {} de {} de {}, {}.\nÉ {} {}.\n\n"

		self.predefined_values = {
		"City": "West Point, KY",
		"Character": "Barbara Hodgetts",
		}

		self.used_predefined_values = False

		self.i = 1
		self.Select_City()
		self.Define_Date_Folders()
		self.Define_Date_Variables()
		self.Write_To_Files()
		self.Open_File()
		self.Show()

	def Select_City(self, first_space = False):
		i = 0
		array = []
		for city in self.kentucky_cities:
			if self.characters_dict[city] != []:
				array.append(city)

			i += 1

		self.kentucky_cities = array

		try:
			self.city = self.predefined_values["City"]
			self.used_predefined_values = True

		except AttributeError:
			self.choice_text = Language_Item_Definer("Select a Kentucky city to use", "Selecione uma cidade de Kentucky para usar")
			self.city = Select_Choice_From_List(self.kentucky_cities, local_script_name, self.choice_text, second_choices_list = self.kentucky_cities, return_second_item_parameter = True, return_number = True, add_none = True, first_space = first_space)[0]

		self.city_folder = self.kentucky_cities_folders[self.city]
		self.city_database_folder = self.kentucky_cities_database_folders[self.city]
		self.characters = self.characters_dict[self.city]

		self.Select_Character()

	def Select_Character(self):
		try:
			self.character = self.predefined_values["Character"]

		except AttributeError:
			self.choice_text = Language_Item_Definer('Select a character from "{}" to use', 'Selecione um personagem de "{}" para usar').format(self.city)
			self.character = Select_Choice_From_List(self.characters, local_script_name, self.choice_text, second_choices_list = self.characters, return_second_item_parameter = True, return_number = True, add_none = True, first_space = False)[0]

		self.character_folder = self.city_folder + self.character + "/"
		Create_Folder(self.character_folder, self.global_switches["create_folders"])

		self.character_database_folder = self.character_folder + "Database/"
		Create_Folder(self.character_database_folder, self.global_switches["create_folders"])

		self.character_date_files = {}

		self.character_date_files["Year"] = self.character_database_folder + "Year" + self.dot_text
		Create_Text_File(self.character_date_files["Year"], self.global_switches["create_files"])

		self.character_date_files["Month"] = self.character_database_folder + "Month" + self.dot_text
		Create_Text_File(self.character_date_files["Month"], self.global_switches["create_files"])

		self.character_date_files["Day"] = self.character_database_folder + "Day" + self.dot_text
		Create_Text_File(self.character_date_files["Day"], self.global_switches["create_files"])

		self.character_date_files["Survival Day"] = self.character_database_folder + "Survival Day" + self.dot_text
		Create_Text_File(self.character_date_files["Survival Day"], self.global_switches["create_files"])

	def Define_Date_Folders(self):
		self.date_info = {}
		self.date_folders = {}

		for key in self.character_date_files:
			self.date_info[key] = Create_Array_Of_File(self.character_date_files[key])

			if (Create_Array_Of_File(self.character_date_files[key]) != []):
				self.date_info[key] = int(Create_Array_Of_File(self.character_date_files[key])[0])

		folder = self.character_folder
		for key in self.date_info:
			if key != "Day" and key != "Survival Day":
				date_info = self.date_info[key]

				if key == "Month":
					date_info = Add_Leading_Zeros(self.date_info[key]) + " - " + month_names_ptbr[int(self.date_info[key])]

				folder += str(date_info) + "/"
				self.date_folders[key] = folder

	def Define_Date_Variables(self):
		day_names_ptbr.pop(0)

		self.date_info["Survival Day"] = str(int(Create_Array_Of_File(self.character_date_files["Survival Day"])[0]) + 1)
		self.date_info["Day"] = int(Create_Array_Of_File(self.character_date_files["Day"])[0]) + 1

		self.day_file_name_template = "Dia {}, {}, {}"
		self.full_date_template = "{}-{}-{}"

		try:
			self.full_day_datetime = datetime.datetime(self.date_info["Year"], self.date_info["Month"], self.date_info["Day"], 0, 0)

		except ValueError:
			self.date_info["Month"] += 1
			self.date_info["Day"] = 1

			self.full_day_datetime = datetime.datetime(self.date_info["Year"], self.date_info["Month"], self.date_info["Day"], 0, 0)

		self.full_date = self.full_date_template.format(Add_Leading_Zeros(self.date_info["Day"]), Add_Leading_Zeros(self.date_info["Month"]), str(self.date_info["Year"]))

		self.week_day = self.full_day_datetime.weekday()

		self.day_name = day_names_ptbr[int(self.week_day)]

		self.survival_diary_day_file_name = self.day_file_name_template.format(self.date_info["Survival Day"], self.day_name, self.full_date)

		self.month_name = month_names_ptbr[int(self.date_info["Month"])]
		self.month_folder = Add_Leading_Zeros(self.date_info["Month"]) + " - " + self.month_name

		self.diary_text = self.diary_template_text.format(number_names_pt[self.date_info["Day"]], self.month_name, self.date_info["Year"], self.full_date.replace("-", "/"), portuguese_day_gender_words[self.day_name], self.day_name)

		self.full_year_folder = self.date_folders["Year"]
		Create_Folder(self.full_year_folder, self.global_switches["create_folders"])

		self.full_month_folder = self.full_year_folder + self.month_folder + "/"
		Create_Folder(self.full_month_folder, self.global_switches["create_folders"])

		self.survival_diary_file = self.full_month_folder + self.survival_diary_day_file_name + self.dot_text
		Create_Text_File(self.character_date_files["Year"], self.global_switches["create_files"])

	def Write_To_Files(self):
		for key in self.date_info:
			self.file_to_write = self.character_date_files[key]
			self.text_to_write = str(self.date_info[key])

			if self.text_to_write != Read_String(self.file_to_write):
				Write_To_File(self.file_to_write, self.text_to_write, self.global_switches)

		self.text_to_write = self.diary_text
		Write_To_File(self.survival_diary_file, self.text_to_write, self.global_switches)

	def Open_File(self):
		Open_File_With_Program("C:/Windows/System32/notepad.exe", self.survival_diary_file, self.global_switches["open_files"])

	def Show(self):
		self.large_bar = "-----"

		print(self.large_bar)
		print()

		if self.used_predefined_values == True:
			print(Language_Item_Definer("The class used predefined city and character", "A classe utilizou cidade e personagem pré-definidos") + ".")
			print(Language_Item_Definer("City", "Cidade") + ": " + self.city)
			print(Language_Item_Definer("Character", "Personagem") + ": " + self.character)
			print()

		print(Language_Item_Definer("This diary file was created", "Este arquivo de diário de sobrevivência foi criado") + ":")
		print(self.survival_diary_day_file_name)
		print(self.survival_diary_file)

		print()
		print(self.large_bar)