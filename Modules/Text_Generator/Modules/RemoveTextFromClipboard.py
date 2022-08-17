import re
import pyperclip
import win32clipboard

texts_to_replace = ["(", ")", "2019", "	", ]

win32clipboard.OpenClipboard()
clipboard_data = win32clipboard.GetClipboardData()
win32clipboard.CloseClipboard()

clipboard_data = clipboard_data.splitlines()

string_to_add = ""

new_data = clipboard_data
i = 0
while i <= len(new_data) - 1:
	if new_data[i] == "":
		i += 1

	for text in texts_to_replace:
		new_data[i] = new_data[i].replace(text, "")

	new_data[i] = re.split('"*.""', new_data[i])[0] + "\n"
	string_to_add += new_data[i]

	i += 1

print("Old data: " + "\n" + clipboard_data[0] + "\n")
print("New data: ")
print(string_to_add)

pyperclip.copy(string_to_add)