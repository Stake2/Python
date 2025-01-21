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
		self.dictionaries["History"] = self.JSON.To_Python(self.tasks["Folders"]["Task History"]["History"])

		self.years_list = range(2018, 2022 + 1)

		self.task_types_list = []

		# Iterate through years list (of years that contain a "Task_History" folder)
		for self.year in self.years_list:
			# Convert the year number into a string
			self.year = str(self.year)

			# Define year dictionary with year number and folders
			self.year = {
				"Number": self.year,
				"Folders": {
					"root": self.tasks["Folders"]["Task History"]["root"] + self.year + "/"
				},
				"Entries dictionary": deepcopy(self.template),
				"Lists": {}
			}

			# Define the history folders
			for folder_name in ["Per Task Type"]:
				key = folder_name.lower().replace(" ", "_")

				# Define the folder
				self.year["Folders"][key] = {
					"root": self.year["Folders"]["root"] + folder_name + "/"
				}

				self.Folder.Create(self.year["Folders"][key]["root"])

			# Define and create the "Tasks.json" file
			self.year["Folders"]["tasks"] = self.year["Folders"]["root"] + "Tasks.json"
			self.File.Create(self.year["Folders"]["tasks"])

			self.year["Entries dictionary"] = self.JSON.To_Python(self.year["Folders"]["tasks"])

			for task_type in self.year["Entries dictionary"]["Numbers"]["Per Task Type"]:
				self.year["Folders"][task_type] = {
					"root": self.year["Folders"]["Per Task Type"]["root"] + task_type + "/"
				}

				self.Folder.Create(self.year["Folders"][task_type]["root"])

				self.year["Folders"][task_type]["tasks"] = self.year["Folders"][task_type]["root"] + "Tasks.json"
				self.File.Create(self.year["Folders"][task_type]["tasks"])

				self.JSON.Edit(self.year["Folders"][task_type]["tasks"], self.template)

				self.year["Folders"][task_type]["entry_list"] = self.year["Folders"][task_type]["root"] + "Entry list.txt"
				self.File.Create(self.year["Folders"][task_type]["entry_list"])

				if self.File.Exist(self.year["Folders"][task_type]["tasks"]) == True:
					self.year[task_type] = self.JSON.To_Python(self.year["Folders"][task_type]["tasks"])

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
				self.JSON.Edit(self.year["Folders"][task_type]["tasks"], self.year[task_type])

				# "Entry list.txt"
				self.File.Edit(self.year["Folders"][task_type]["entry_list"], self.Text.From_List(self.year[task_type]["Entries"], next_line = True), "w")

			if self.year["Number"] != list(self.years_list)[-1]:
				self.Input.Type(self.Language.language_texts["continue, title()"] + " (" + self.Language.language_texts["next, masculine"].title() + " " + self.Date.language_texts["year, title()"] + ")")