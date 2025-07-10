# Convert_History.py

from Diary_Slim.Diary_Slim import Diary_Slim as Diary_Slim

class Convert_History(Diary_Slim):
	def __init__(self, dictionary = {}):
		super().__init__()

		from copy import deepcopy

		# Copy the switches dictionary
		switches_dictionary = deepcopy(self.switches)

		self.years_list = self.years

		# Iterate through years list (of years that contain a "Watch_History" folder)
		for self.year in self.years_list:
			# Convert the year number into a string
			self.year = str(self.year)

			# Define year dictionary with year number and folders
			self.year = {
				"Number": self.year,
				"Folders": {},
				"Year": deepcopy(self.templates["Year"])
			}

			self.year["Folders"] = self.diary_slim["Folders"]["Years"][self.year["Number"]]
			self.year["Folders"]["old"] = {
				"root": self.diary_slim["Folders"]["root"] + self.year["Number"] + "/"
			}

			print()
			print("----------")
			print()
			print(self.Date.language_texts["year, title()"] + ": " + self.year["Number"])
			print()

			# Get the months list
			self.year["Months"] = self.Folder.Contents(self.year["Folders"]["old"]["root"])["folder"]["names"]

			# Iterate through the months list
			for month in self.year["Months"]:
				# Get the month number
				month = int(month.split(" - ")[0])

				# Define the date object of the month
				date = self.Date.Now(self.Date.Date(year = int(self.year["Number"]), month = month, day = 1))

				# Define the month dictionary
				month = deepcopy(self.templates["Month"])

				# Define the month numbers
				month["Numbers"] = {
					"Year": date["Units"]["Year"],
					"Month": date["Units"]["Month"],
					"Days": date["Units"]["Month days"],
					"Diary Slims": 0
				}

				# Define the month names
				month["Names"] = date["Texts"]["Month name"]

				# Define the month key
				month["Formats"]["Diary Slim"] = str(self.Text.Add_Leading_Zeroes(month["Numbers"]["Month"])) + " - " + month["Names"][self.language["Small"]]

				self.year["Year"]["Months"][month["Formats"]["Diary Slim"]] = month

				# Define the month folder
				old_month_folder = self.year["Folders"]["old"]["root"] + self.year["Year"]["Months"][month["Formats"]["Diary Slim"]]["Formats"]["Diary Slim"] + "/"

				# Define the days list
				self.year["Days"] = self.Folder.Contents(old_month_folder)["file"]["names"]

				self.year["Year"]["Months"][month["Formats"]["Diary Slim"]]["Numbers"]["Diary Slims"] = len(self.year["Days"])

				# Iterate through the days list
				for day in self.year["Days"]:
					day_number = int(day.split(" ")[0])

					# Define the date object of the day
					date = self.Date.Now(self.Date.Date(year = int(self.year["Number"]), month = month["Numbers"]["Month"], day = day_number))

					day_file = old_month_folder + day + ".txt"
					day_text = self.File.Contents(day_file)

					self.year["Year"]["Months"][month["Formats"]["Diary Slim"]]["Diary Slims"][day] = deepcopy(self.templates["Day"])

					self.year["Year"]["Months"][month["Formats"]["Diary Slim"]]["Diary Slims"][day]["Day"] = date["Units"]["Day"]
					self.year["Year"]["Months"][month["Formats"]["Diary Slim"]]["Diary Slims"][day]["Names"] = date["Texts"]["Day name"]
					self.year["Year"]["Months"][month["Formats"]["Diary Slim"]]["Diary Slims"][day]["Formats"] = {
						"DD-MM-YYYY": date["Formats"]["DD-MM-YYYY"]
					}

					# Define the creation time
					self.year["Year"]["Months"][month["Formats"]["Diary Slim"]]["Diary Slims"][day]["Creation time"]["HH:MM"] = day_text["lines"][2].split(" ")[0]

					split = self.year["Year"]["Months"][month["Formats"]["Diary Slim"]]["Diary Slims"][day]["Creation time"]["HH:MM"].split(":")

					self.year["Year"]["Months"][month["Formats"]["Diary Slim"]]["Diary Slims"][day]["Creation time"]["Hours"] = int(split[0])
					self.year["Year"]["Months"][month["Formats"]["Diary Slim"]]["Diary Slims"][day]["Creation time"]["Minutes"] = int(split[1])

					has_data = False

					if "Fui dormir " in day_text["lines"][5]:
						string = day_text["lines"][5].split("Fui dormir ")[1]
						string = string[:-(len(string) - 5)]

						self.year["Year"]["Months"][month["Formats"]["Diary Slim"]]["Diary Slims"][day]["Data"]["Sleep times"]["Slept"] = string

						has_data = True

					if "Acordei " in day_text["lines"][5]:
						string = day_text["lines"][5].split("Acordei ")[1]
						string = string[:-(len(string) - 5)]

						self.year["Year"]["Months"][month["Formats"]["Diary Slim"]]["Diary Slims"][day]["Data"]["Sleep times"]["Woke up"] = string

						has_data = True

					elif ", acordei " in day_text["lines"][5]:
						string = day_text["lines"][5].split(", acordei ")[1]
						string = string[:-(len(string) - 5)]

						self.year["Year"]["Months"][month["Formats"]["Diary Slim"]]["Diary Slims"][day]["Data"]["Sleep times"]["Woke up"] = string

						has_data = True

					for item in ["Slept", "Woke up"]:
						if item in self.year["Year"]["Months"][month["Formats"]["Diary Slim"]]["Diary Slims"][day]["Data"]["Sleep times"]:
							string = self.year["Year"]["Months"][month["Formats"]["Diary Slim"]]["Diary Slims"][day]["Data"]["Sleep times"][item]

							if string == "":
								self.year["Year"]["Months"][month["Formats"]["Diary Slim"]]["Diary Slims"][day]["Data"]["Sleep times"].pop(item)

							elif ":" not in string:
								self.System.Open(day_file)
								input()

					if has_data == False:
						self.year["Year"]["Months"][month["Formats"]["Diary Slim"]]["Diary Slims"][day].pop("Data")

				new_month_folder = self.year["Folders"]["root"] + self.year["Year"]["Months"][month["Formats"]["Diary Slim"]]["Formats"]["Diary Slim"] + "/"
				self.Folder.Create(new_month_folder)

				month_file = new_month_folder + "Month.json"
				self.File.Create(month_file)

				# Edit the "Month.json" file
				self.JSON.Edit(month_file, self.year["Year"]["Months"][month["Formats"]["Diary Slim"]])

				# Add to the Diary Slims number
				self.year["Year"]["Numbers"]["Diary Slims"] += int(month["Numbers"]["Diary Slims"])

			self.year["Year"]["Numbers"]["Year"] = int(self.year["Number"])

			# Define the number of months
			self.year["Year"]["Numbers"]["Months"] = len(list(self.year["Year"]["Months"].keys()))

			self.year["Year"]["Numbers"]["Days"] = self.Date.Now(self.Date.Date(year = int(self.year["Number"]), month = 1, day = 1))["Units"]["Year days"]

			# Edit the "Year.json" file
			self.JSON.Edit(self.year["Folders"]["year"], self.year["Year"])

			if self.year["Number"] != list(self.years_list)[-1] and self.switches["Testing"] == True:
				self.Input.Type(self.Language.language_texts["continue, title()"] + " (" + self.Language.language_texts["next, masculine"].title() + " " + self.Date.language_texts["year, title()"] + ")")

		# Update the "History.json" file with the updated "History" dictionary
		self.JSON.Edit(self.diary_slim["Folders"]["Years"]["History"], self.history)