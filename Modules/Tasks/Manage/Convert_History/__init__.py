# Convert_History.py

from Tasks.Tasks import Tasks as Tasks

class Convert_History(Tasks):
	def __init__(self):
		super().__init__()

		self.Create_Per_Task_Type()

	def Create_Per_Task_Type(self):
		from copy import deepcopy

		# Copy the switches dictionary
		switches_dictionary = deepcopy(self.switches)

		# Import the Register class
		from Tasks.Register import Register as Register

		self.Register = Register

		# Get the History dictionary to update the entries number
		self.dictionaries["History"] = self.JSON.To_Python(self.folders["task_history"]["history"])

		self.years_list = range(2018, 2022 + 1)

		self.task_types_list = []

		# Iterate through years list (of years that contain a "Task_History" folder)
		for self.year in self.years_list:
			# Convert the year number into a string
			self.year = str(self.year)

			# Define year dictionary with year number and folders
			self.year = {
				"Number": self.year,
				"folders": {
					"root": self.folders["task_history"]["root"] + self.year + "/"
				},
				"Entries dictionary": deepcopy(self.template),
				"Lists": {}
			}

			# Define the history folders
			for folder_name in ["Per Task Type"]:
				key = folder_name.lower().replace(" ", "_")

				# Define the folder
				self.year["folders"][key] = {
					"root": self.year["folders"]["root"] + folder_name + "/"
				}

				self.Folder.Create(self.year["folders"][key]["root"])

			# Define and create the "Tasks.json" file
			self.year["folders"]["tasks"] = self.year["folders"]["root"] + "Tasks.json"
			self.File.Create(self.year["folders"]["tasks"])

			self.year["Entries dictionary"] = self.JSON.To_Python(self.year["folders"]["tasks"])

			for task_type in self.year["Entries dictionary"]["Numbers"]["Per Task Type"]:
				self.year["folders"][task_type] = {
					"root": self.year["folders"]["per_task_type"]["root"] + task_type + "/"
				}

				self.Folder.Create(self.year["folders"][task_type]["root"])

				self.year["folders"][task_type]["tasks"] = self.year["folders"][task_type]["root"] + "Tasks.json"
				self.File.Create(self.year["folders"][task_type]["tasks"])

				self.JSON.Edit(self.year["folders"][task_type]["tasks"], self.template)

				self.year["folders"][task_type]["entry_list"] = self.year["folders"][task_type]["root"] + "Entry list.txt"
				self.File.Create(self.year["folders"][task_type]["entry_list"])

				if self.File.Exist(self.year["folders"][task_type]["tasks"]) == True:
					self.year[task_type] = self.JSON.To_Python(self.year["folders"][task_type]["tasks"])

			print()
			print("----------")
			print()
			print(self.Date.language_texts["year, title()"] + ": " + self.year["Number"])

			# Iterate through the English Tasks list
			i = 1
			for entry in self.year["Entries dictionary"]["Entries"]:
				entry = self.year["Entries dictionary"]["Dictionary"][entry]

				task_type = entry["Type"]

				# Add to the Total Number
				self.year[task_type]["Numbers"]["Total"] += 1

				# Add to the Entries list
				self.year[task_type]["Entries"].append(entry["Entry"])

				# Add to the Dictionary
				self.year[task_type]["Dictionary"][entry["Entry"]] = entry

				i += 1

			# "Per Task Type/[Task Type]/Tasks.json"
			for task_type in self.year["Entries dictionary"]["Numbers"]["Per Task Type"]:
				self.JSON.Edit(self.year["folders"][task_type]["tasks"], self.year[task_type])

				# "Entry list.txt"
				self.File.Edit(self.year["folders"][task_type]["entry_list"], self.Text.From_List(self.year[task_type]["Entries"]), "w")

			if self.year["Number"] != list(self.years_list)[-1]:
				self.Input.Type(self.JSON.Language.language_texts["continue, title()"] + " (" + self.JSON.Language.language_texts["next, masculine"].title() + " " + self.Date.language_texts["year, title()"] + ")")