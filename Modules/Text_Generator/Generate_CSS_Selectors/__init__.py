# Generate CSS Selectors.py

class Generate_CSS_Selectors():
	def __init__(self):
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
		from Utility.Global_Switches import Global_Switches as Global_Switches

		from Utility.File import File as File
		from Utility.Folder import Folder as Folder
		from Utility.Date import Date as Date
		from Utility.Input import Input as Input
		from Utility.JSON import JSON as JSON
		from Utility.Text import Text as Text

		# Global Switches dictionary
		self.switches = Global_Switches().global_switches

		self.File = File()
		self.Folder = Folder()
		self.Date = Date()
		self.Input = Input()
		self.JSON = JSON()
		self.Text = Text()

		self.languages = self.JSON.Language.languages

		self.user_language = self.JSON.Language.user_language
		self.full_user_language = self.JSON.Language.full_user_language

		self.Sanitize = self.File.Sanitize

		self.folders = self.Folder.folders

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