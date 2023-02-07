# Set.py

from Utility.Modules import Modules as Modules

class Set(Modules):
	def __init__(self):
		super().__init__()

	def Set(self, object, modules_list = None, utility_modules = []):
		if modules_list != None:
			modules_list.extend([
				"Global_Switches",
				"Define_Folders"
			])

		if modules_list == None:
			modules_list = self.modules["utility"]["list"]

		if utility_modules != []:
			modules_list.extend(utility_modules)

		self.object_name = type(object).__name__

		if "." in type(object).__name__ or object.__module__.split(".")[0] in self.modules["usage"]["list"]:
			self.object_name = object.__module__.split(".")[0]

		for title in modules_list:
			if title not in ["Modules", self.object_name]:
				if title in self.modules["utility"]:
					module = self.modules["utility"][title]["module"]

				else:
					module = self.modules["usage"][title]["sub_module"]

				class_ = getattr(module, title)

				if hasattr(class_, "Modules") == False:
					setattr(class_, "Modules", Set())

				if title != "Define_Folders":
					class_ = class_()

				set = False

				if hasattr(object, title) == False:
					setattr(object, title, class_)

				if hasattr(class_, "export") == True:
					self.Import_Variables(object, class_)

		return self.modules

	def Import_Variables(self, object, class_):
		export = class_.export

		for key in class_.__dict__:
			value = class_.__dict__[key]

			if value in export:
				setattr(object, key, value)

		if self.object_name not in self.modules["utility"]["list"]:
			import inspect

			for method in inspect.getmembers(class_, predicate = inspect.ismethod):
				title = method[0]
				method = method[1]

				if method in export:
					setattr(object, title, method)