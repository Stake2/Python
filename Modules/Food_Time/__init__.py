# Food_Time.py

from Script_Helper import *

class Food_Time():
	def __init__(self, parameter_switches = None, register_time = True):
		# Verbose variable
		self.verbose = False

		self.testing_script = False

		self.parameter_switches = parameter_switches

		self.register_time = register_time

		self.Define_Basic_Variables()
		self.Define_Texts()
		self.Define_Files()

		if self.register_time == True:
			self.Get_Time()
			self.Define_Times()
			self.Register_Times()

		if self.register_time == False:
			self.Get_Times_From_File()

		self.Show_Times()

	def Define_Basic_Variables(self):
		self.option = True

		# Global Switches dictionary
		self.global_switches = {
			"write_to_file": self.option,
			"create_files": self.option,
			"create_folders": self.option,
			"move_files": self.option,
			"verbose": self.verbose,
			"testing_script": self.testing_script,
		}

		if self.parameter_switches != None:
			self.global_switches = self.parameter_switches
			self.testing_script = self.global_switches["testing_script"]

		if self.global_switches["testing_script"] == True:
			print(Language_Item_Definer("Testing script: Yes", "Testando script: Sim"))

		if self.global_switches["verbose"] == True:
			print(Language_Item_Definer("Verbose on", "Verbose ligado") + ".")

		if self.global_switches["testing_script"] == True:
			self.global_switches["write_to_file"] = False
			self.global_switches["create_files"] = False

		self.dot_text = ".txt"

	def Define_Texts(self):
		self.this_is_the_time_text = "This is the time that you", "Essa é a hora que você"

		self.prefix_text = self.this_is_the_time_text[0] + " "

		self.english_food_time_show_texts = {
			"Ate": self.prefix_text + "ate",
			"Drink Water": self.prefix_text + "can drink water",
			"Hungry": self.prefix_text + "will be hungry",
		}

		self.prefix_text = self.this_is_the_time_text[1] + " "

		self.portuguese_food_time_show_texts = {
			"Ate": self.prefix_text + "comeu",
			"Drink Water": self.prefix_text + "pode beber água",
			"Hungry": self.prefix_text + "irá ter fome",
		}

	def Define_Files(self):
		self.string_to_format = notepad_folder_food_files + "{}" + self.dot_text

		self.food_time_files = {
			"English": self.string_to_format.format("Time that I finished eating"),
			"Portuguese": self.string_to_format.format("Tempo que terminei de comer"),
			"Raw Times": self.string_to_format.format("Raw Times - Tempos Brutos"),
		}

		self.food_time_file = self.food_time_files[Language_Item_Definer("English", "Portuguese")]

		for file in self.food_time_files.values():
			Create_Text_File(file, self.global_switches)

	def Get_Time(self):
		self.now_raw_1 = datetime.datetime.now().time()
		self.now_raw_2 = datetime.datetime.now()
		self.now_string = datetime.datetime(self.now_raw_2.year, self.now_raw_2.month, self.now_raw_2.day, self.now_raw_1.hour, self.now_raw_1.minute)

		self.time_that_ate = time.strftime("%H:%M %d/%m/%Y")

		self.time_to_wait_to_drink_water = 40

		self.when_can_drink_water = (self.now_string + datetime.timedelta(minutes=self.time_to_wait_to_drink_water)).strftime("%H:%M %d/%m/%Y")

		self.when_will_be_hungry = (self.now_string + datetime.timedelta(hours=3)).strftime("%H:%M %d/%m/%Y")

		self.food_times = {
			"Ate": self.time_that_ate,
			"Drink Water": self.when_can_drink_water,
			"Hungry": self.when_will_be_hungry,
		}

	def Define_Times(self):
		self.when_can_drink_water_plus_text = " ({} + {} minutes)".format(self.time_that_ate.split(" ")[0], self.time_to_wait_to_drink_water), " ({} + {} minutos)".format(self.time_that_ate.split(" ")[0], self.time_to_wait_to_drink_water)

		self.language_list = self.english_food_time_show_texts

		self.english_food_time_texts = {
			"Ate": self.language_list["Ate"] + ": " + self.time_that_ate,
			"Drink Water": self.language_list["Drink Water"] + ": " + self.when_can_drink_water + self.when_can_drink_water_plus_text[0],
			"Hungry": self.language_list["Hungry"] + ": " + self.when_will_be_hungry,
		}

		self.language_list = self.portuguese_food_time_show_texts

		self.portuguese_food_time_texts = {
			"Ate": self.language_list["Ate"] + ": " + self.time_that_ate,
			"Drink Water": self.language_list["Drink Water"] + ": " + self.when_can_drink_water + self.when_can_drink_water_plus_text[1],
			"Hungry": self.language_list["Hungry"] + ": " + self.when_will_be_hungry,
		}

		self.food_time_texts = Language_Item_Definer(self.english_food_time_texts, self.portuguese_food_time_texts)

	def Register_Times(self):
		text_to_write = ""

		for food_time_text in self.english_food_time_texts.values():
			text_to_write += food_time_text

			if food_time_text != list(self.english_food_time_texts.values())[-1]:
				text_to_write += "\n"

		Write_To_File(self.food_time_files["English"], text_to_write, self.global_switches)

		# ----- #

		text_to_write = ""

		for food_time_text in self.portuguese_food_time_texts.values():
			text_to_write += food_time_text

			if food_time_text != list(self.portuguese_food_time_texts.values())[-1]:
				text_to_write += "\n"

		Write_To_File(self.food_time_files["Portuguese"], text_to_write, self.global_switches)

		# ----- #

		text_to_write = ""

		for food_time in self.food_times.values():
			text_to_write += food_time

			if food_time != list(self.food_times.values())[-1]:
				text_to_write += "\n"

		Write_To_File(self.food_time_files["Raw Times"], text_to_write, self.global_switches)

	def Get_Times_From_File(self):
		self.key_list = [
			"Ate",
			"Drink Water",
			"Hungry",
		]

		self.food_time_texts = {}

		i = 0
		for food_time in Create_Array_Of_File(self.food_time_file):
			self.food_time_texts[self.key_list[i]] = food_time

			i += 1

	def Show_Times(self):
		print()
		print(Language_Item_Definer("Showing the meal times below", "Mostrando os horários da refeição abaixo") + ": ")
		print()

		for food_time in self.food_time_texts.values():
			print(food_time)