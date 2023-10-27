# Generate CSS Selectors.py

class Generate_CSS_Selectors():
	def __init__(self):
		# Define the module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.Define_Basic_Variables()

		self.json = self.JSON.To_Python(self.folders["mega"]["php"]["json"]["colors"])
		self.colors = self.json["names"]
		self.hex = self.json["hex"]

		self.colors_css = []

		self.selectors = [
			".border_1px_solid_{}",
			".border_3px_solid_{}",
			".border_4px_solid_{}",
			".border_color_{}",
			".background_{}",
			".background_hover_{}:hover",
			".text_{}",
			".text_hover_{}:hover",
			".box_shadow_{}",
		]

		self.css_contents = [
			"(tab)border: 1px solid var(--{}-color);",
			"(tab)border: 3px solid var(--{}-color);",
			"(tab)border: 4px solid var(--{}-color);",
			"(tab)border-color: var(--{}-color);",
			"(tab)background-color: var(--{}-color);",
			"(tab)background-color: var(--{}-color);",
			"(tab)color: var(--{}-color);",
			"(tab)color: var(--{}-color);",
			"(tab)box-shadow: var(--box-shadow-{}) !important;",
		]

		self.Create_Box_Shadow()
		self.Generate_And_Copy()

	def Define_Basic_Variables(self):
		from copy import deepcopy

		# Import the JSON module
		from Utility.JSON import JSON as JSON

		self.JSON = JSON()

		# Get the modules list
		self.modules = self.JSON.To_Python(self.folders["apps"]["modules"]["modules"])

		# Import the "importlib" module
		import importlib

		# Create a list of the modules that will not be imported
		remove_list = [
			"Define_Folders",
			"Language",
			"JSON"
		]

		# Iterate through the Utility modules
		for module_title in self.modules["Utility"]["List"]:
			# If the module title is not inside the remove list
			if module_title not in remove_list:
				# Import the module
				module = importlib.import_module("." + module_title, "Utility")

				# Get the sub-class
				sub_class = getattr(module, module_title)

				# Add the sub-clas to the current module
				setattr(self, module_title, sub_class())

		# Make a backup of the module folders
		self.module_folders = {}

		for item in ["modules", "module_files"]:
			self.module_folders[item] = deepcopy(self.folders["apps"][item][self.module["key"]])

		# Define the local folders dictionary as the Folder folders dictionary
		self.folders = self.Folder.folders

		self.links = self.Folder.links

		# Restore the backup of the module folders
		for item in ["modules", "module_files"]:
			self.folders["apps"][item][self.module["key"]] = self.module_folders[item]

		# Get the switches dictionary from the "Global Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# Get the Languages dictionary
		self.languages = self.JSON.Language.languages

		# Get the user language and full user language
		self.user_language = self.JSON.Language.user_language
		self.full_user_language = self.JSON.Language.full_user_language

		# Get the Sanitize method of the File class
		self.Sanitize = self.File.Sanitize

		# Get the current date from the Date module
		self.date = self.Date.date

	def Generate_CSS_Strings(self, selector, css_content):
		for color in self.colors:
			color_css_string = selector + " (\n" + css_content + "\n)"

			if color != self.colors[-1]:
				color_css_string += "\n\n"

			color_css_string = color_css_string.format(color.replace("-", "_"), color)
			color_css_string = color_css_string.replace("(tab)", "\t")
			color_css_string = color_css_string.replace(" (", " {")
			color_css_string = color_css_string.replace("\n)", "\n}")

			if color == self.colors[-1] and selector != self.selectors[-1]:
				color_css_string = color_css_string.replace("\n}", "\n}\n\n")

			self.colors_css.append(color_css_string)

	def Generate_And_Copy(self):
		i = 0
		for selector in self.selectors:
			self.Generate_CSS_Strings(selector, self.css_contents[i])

			i += 1

		self.string += "\n\n"

		for text in self.colors_css:
			self.string += text

		self.Text.Copy(self.string)

	def Create_Box_Shadow(self):
		format_string = "\t--box-shadow-{}: 0 -8px 20px var(--spread-btn) {}60," + "\n" + \
		"\t" + "0 8px 20px var(--spread-btn) {}60," + "\n" + \
		"\t" + "0 6px 20px var(--spread-btn) {}60," + "\n" + \
		"\t" + "0 -6px 20px var(--spread-btn) {}60 !important;"

		self.string = "body {\n"
		i = 0
		for color in self.colors:
			color = color.replace("_", "-")
			hex_color = self.hex[i]

			self.string += format_string.format(color, hex_color, hex_color, hex_color, hex_color)

			if i != len(self.colors) - 1:
				self.string += "\n\n"

			i += 1

		self.string += "\n}"