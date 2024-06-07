# Media_Type_Classes.py

from Watch_History.Watch_History import Watch_History as Watch_History

import os
import importlib

class Media_Type_Classes(Watch_History):
	def __init__(self):
		super().__init__()

		# Define the root dictionary and ask the user to select a media type
		self.dictionary = {
			"Media type": self.Select_Media_Type()
		}

	def Define_Classes(self):
		# Get the current folder
		current_folder = self.Language.Current_Folder(__file__)

		# Get the descriptions file
		descriptions_file = current_folder + "Descriptions.json"

		# Get the descriptions dictionary
		descriptions = self.JSON.To_Python(descriptions_file)

		# Define the user language version of the show text
		descriptions["Show text"] = self.Language.Item(descriptions["Show text"])

		# Define the classes dictionary
		classes = {
			"Dictionary": {},
			"Descriptions": []
		}

		# Define the list of keys to remove
		remove_list = [
			"Show text",
			"Remove list"
		]

		# Iterate through the descriptions dictionary
		for key, class_description in descriptions.items():
			# If the key is not in the remove list
			if key not in remove_list:
				# If the "Remove list" is not present
				# Or it is and the key is not in the remove list
				if (
					"Remove list" not in descriptions or
					"Remove list" in descriptions and
					key not in descriptions["Remove list"]
				):
					# Get the class object
					module = importlib.import_module("." + key, self.__module__)
					object = getattr(module, key)

					# Create the class dictionary and add it to the "Classes" dictionary, with the class descriptions
					classes["Dictionary"][key] = {
						"Descriptions": class_description,
						"Description": self.Language.Item(class_description),
						"Object": object
					}

		# Fill the list of class descriptions
		for class_ in classes["Dictionary"].values():
			classes["Descriptions"].append(class_["Description"])

	def Run_Class(self):
		# Define the parameters dictionary for the "Input.Select" method
		parameters = {
			"options": list(classes["Dictionary"].values()),
			"language_options": classes["Descriptions"],
			"show_text": descriptions["Show text"],
			"select_text": self.Language.language_texts["select_one_class_to_execute"]
		}

		# Ask the user to select a class
		class_ = self.Input.Select(**parameters)["option"]

		# Run the object of the class
		class_["Object"]()