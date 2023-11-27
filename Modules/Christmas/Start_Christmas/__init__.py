# Start_Christmas.py

from Christmas.Christmas import Christmas as Christmas

from calendar import monthrange

class Start_Christmas(Christmas):
	def __init__(self):
		super().__init__()

		print()
		print(self.large_bar)
		print()

		if self.today_is_christmas == False:
			self.months_left = abs((self.date["Units"]["Year"] - self.christmas["Units"]["Year"]) * 12 + self.date["Units"]["Month"] - self.christmas["Units"]["Month"])
			self.days_left = abs(abs((self.date["Object"] - self.christmas["Object"]).days - 1) - (self.months_left * monthrange(self.date["Units"]["Year"], self.date["Units"]["Month"])[1]))

			print(self.language_texts["today_is_not_christmas_day_wait_until"] + " " + self.christmas["Formats"]["DD/MM/YYYY"] + ".")

			print()
			print(self.language_texts["current_date"] + ":")
			print(self.date["Formats"]["DD/MM/YYYY"])

			print()
			print(self.language_texts["christmas_date"] + ":")
			print(self.christmas["Formats"]["DD/MM/YYYY"])

			if self.months_left != 0:
				print()
				print(self.Text.By_Number(self.months_left, self.language_texts["month_left"], self.language_texts["months_left"]) + ":")
				print(str(self.months_left) + " " + self.Text.By_Number(self.months_left, self.language_texts["month"], self.language_texts["months"]))

			if self.days_left != 0:
				print()
				print(self.Text.By_Number(self.days_left, self.language_texts["day_left"], self.language_texts["days_left"]) + ":")
				print(str(self.days_left) + " " + self.Text.By_Number(self.days_left, self.language_texts["day"], self.language_texts["days"]))

		if self.today_is_christmas == True:
			self.Execute_Steps()

			print(self.language_texts["your_christmas_of_{}_is_finished_congratulations!"].format(self.date["Units"]["Year"]))

		print()
		print(self.large_bar)

	def Execute_Steps(self):
		self.planning = self.File.Contents(self.planning_file)["lines"]
		self.objects = self.File.Contents(self.objects_file)["lines"]

		print(self.language_texts["starting_{}_of_{}..."].format(self.language_texts["christmas, title()"], self.date["Units"]["Year"]))
		print()
		print("-")
		print()

		self.System.Open(self.planning_file)

		self.planning_steps = ""

		i = 0
		for text in self.planning:
			object = self.objects[i]

			text_backup = text

			text = str(i + 1) + ". " + text

			if object != "None":
				function = self.functions[object.split(": ")[0]]
				object_data = object.split(": ")[1]

				print(text + ".")

			if object == "None":
				self.Input.Type(text, first_space = False)

			if object != "None":
				function(object_data)

			print()
			print("-----")
			print()

			self.planning_steps += text

			if text != self.planning[-1]:
				self.planning_steps += "\n"

			i += 1