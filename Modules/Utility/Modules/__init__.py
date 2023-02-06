# Modules.py

class Modules(object):
	def __init__(self):
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

	def Get(self):
		import importlib

		modules = self.JSON_To_Python(self.folders["apps"]["modules"]["modules"])

		for key in ["utility", "usage"]:
			modules[key]["list"] = sorted(modules[key]["list"], key=str.lower)

		self.Edit(self.folders["apps"]["modules"]["modules"], modules)

		for key in ["utility", "usage"]:
			for title in modules[key]["list"]:
				if title != "Modules":
					if key == "utility":
						tuple_ = "." + title, key.title()

					if key == "usage":
						tuple_ = title,

					modules[key][title] = {
						"title": title,
						"key": title.lower(),
						"list": [title.lower()],
						"text_key": "executes_the_{}_module",
						"module": importlib.import_module(*tuple_)
					}

					if key == "usage":
						try:
							modules[key][title]["sub_module"] = importlib.import_module("." + title, title)

						except ModuleNotFoundError:
							pass

		return modules

	def Set(self, object, modules_list = None):
		self.modules = self.Get()

		if modules_list != None:
			modules_list.append("Global_Switches")
			modules_list.append("Define_Folders")

		if modules_list == None:
			modules_list = self.Get()["utility"]

		for title in modules_list:
			if title not in ["list", type(Modules).__name__, type(object).__name__]:
				module = self.modules["utility"][title]["module"]

				class_ = getattr(module, title)

				if title != "Define_Folders":
					class_ = class_()

				set = False

				if type(object).__name__ != "Folder" or type(object).__name__ == "Folder" and title != "Define_Folders":
					set = True

				if set == True:
					setattr(object, title, class_)

					self.Import_Variables(object, class_)

		return self.modules

	def Import_Variables(self, object, class_):
		if hasattr(class_, "export") == True:
			export = class_.export

			for key in class_.__dict__:
				value = class_.__dict__[key]

				if value in export:
					setattr(object, key, value)

			if type(object).__name__ not in self.modules["utility"]["list"]:
				import inspect

				for method in inspect.getmembers(class_, predicate = inspect.ismethod):
					title = method[0]
					method = method[1]

					if method in export:
						setattr(object, title, method)

	def Sanitize(self, path):
		import os

		path = os.path.normpath(path).replace("\\", "/")

		return path

	def Edit(self, file, text):
		import os

		file = self.Sanitize(file)

		text = self.JSON_From_Python(text)

		if os.path.isfile(file) == True:
			edit = open(file, "w", encoding = "UTF8")
			edit.write(text)
			edit.close()

	def JSON_From_Python(self, items):
		import json

		from copy import deepcopy

		items = deepcopy(items)

		return json.dumps(items, indent = 4, ensure_ascii = False)

	def JSON_To_Python(self, file):
		import json

		dictionary = json.load(open(file, encoding = "utf8"))

		return dictionary