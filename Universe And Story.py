import random
import inspect

def Dict_Print(**kwargs):
	keys = list(kwargs.keys())
	values = list(kwargs.values())

	dict_name = list(keys)[0]
	dict = list(values)[0]
	dict_values = list(dict.values())

	string_format = "{}:\n{}"

	print(dict_name + ":")

	for key in dict:
		value = dict.get(key)

		text = ""

		if value == dict_values[0]:
			text += "["

		text += string_format.format(key.title(), value)

		if value == dict_values[-1]:
			text += "]"

		print(text)

		if value != dict_values[-1]:
			print()

class Universe():
	def __init__(self, universe, type):
		self.values = {}
		self.unique_universe_types = ["Video", "Literature"]

		self.universe = universe
		self.values["universe"] = self.universe

		if type in self.unique_universe_types:
			universe_id = self.Get_Universe_ID(self.universe)

		if type not in self.unique_universe_types:
			universe_id = self.Generate_Random_Universe_ID()

		self.universe_id = universe_id
		self.values["universe_id"] = self.universe_id

	def Get_Universe_ID(self, universe):
		return "3404973513361802831952646265596793989524956793686677631761418455315373318805160377194"

	def Generate_Random_Universe_ID(self, length = 85):
		numbers = "0123456789"
		numbers_length = len(numbers)

		universe_id = ""

		i = 0
		while i < length:
			universe_id += numbers[random.randrange(0, numbers_length - 1)]

			i += 1

		while universe_id[0] == "0":
			universe_id = "".join(random.sample(universe_id, len(universe_id)))

		return universe_id

	def Get_Values(self):
		return self.values

class Story():
	def __init__(self, story):
		self.values = {}

		self.story = story
		self.characters = ["Character One"]
		self.author = "Author Name"

		self.values["story"] = self.story
		self.values["characters"] = self.characters
		self.values["author"] = self.author

	def Get_Values(self):
		return self.values

literature_universe = Universe(universe = "The Life of Littletato", type = "Literature")
literature_universe_name = literature_universe.universe
universe_id = literature_universe.universe_id

story = Story(story = "The Life of Littletato")
story_title = story.story
characters = story.characters
author = story.author

Dict_Print(literature_universe = literature_universe.Get_Values())
print()
Dict_Print(story = story.Get_Values())