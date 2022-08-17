# Generate CSS Selectors.py

import win32clipboard
from Script_Helper import *

colors_array = [
"grey",
"white",
"black",
"red",
"dark-red",
"blue",
"darker-blue",
"dark-blue",
"super-dark-blue",
"cyan",
"green",
"green-water",
"dark-green-water",
"yellow",
"yellow-sand",
"light-brown",
"brown",
"darker-brown",
"dark-brown",
"pink",
"dark-pink",
]

colors_array_length = len(colors_array) - 1

colors_css_array = []

selectors = [
".border_1px_solid_{}",
".border_3px_solid_{}",
".border_4px_solid_{}",
".border_color_{}",
".background_hover_{}:hover",
".text_hover_{}:hover",
".background_{}",
".text_{}",
]

css_contents = [
"(tab)border: 1px solid var(--{}-color);",
"(tab)border: 3px solid var(--{}-color);",
"(tab)border: 4px solid var(--{}-color);",
"(tab)border-color: var(--{}-color);",
"(tab)background-color: var(--{}-color);",
"(tab)color: var(--{}-color)!important;",
"(tab)background-color: var(--{}-color);",
"(tab)color: var(--{}-color);",
]

def Generate_CSS_Strings(selector, css_content):
	global colors_array
	global color_css_string
	global formatted_color_css_string
	global colors_css_array

	i = 0
	while i <= colors_array_length:
		color_css_string = selector + " (\n" + css_content + "\n)\n\n"
		formatted_color_css_string = color_css_string.format(colors_array[i].replace("-", "_"), colors_array[i])
		formatted_color_css_string = formatted_color_css_string.replace("(tab)", "\t")
		formatted_color_css_string = formatted_color_css_string.replace(" (", " {")
		formatted_color_css_string = formatted_color_css_string.replace("\n)", "\n}")

		colors_css_array.append(formatted_color_css_string)

		i += 1

i = 0
for selector in selectors:
	Generate_CSS_Strings(selector, css_contents[i])

	i += 1

full_text_string = ""
for text in colors_css_array:
	full_text_string += text

Copy_Text(full_text_string)