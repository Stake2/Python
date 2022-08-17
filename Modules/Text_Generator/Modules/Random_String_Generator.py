import pyperclip
import win32clipboard
import random

string_variable = ""
usable_string = ""

text_of_length_of_string_to_generate = 50
length_of_string_to_generate = str(text_of_length_of_string_to_generate).replace("0", "")
length_of_string_to_generate = int(length_of_string_to_generate)

a = 1
while a <= length_of_string_to_generate:
	for i in range(10):
		usable_string += str(i)

	a += 1

random_numbers = string_variable.join(random.sample(usable_string, len(usable_string)))
comma_separated_random_numbers = "{:,}".format(int(random_numbers))
dot_separated_random_numbers = str(comma_separated_random_numbers).replace(",", ".")

print("Generating {} characters string...".format(text_of_length_of_string_to_generate))

print()
print("This is the generated string: ")
print(random_numbers)

print()
print("This is the comma separated generated string: ")
print(comma_separated_random_numbers)

print()
print("This is the dot separated generated string: ")
print(dot_separated_random_numbers)

pyperclip.copy(random_numbers + "\n" + comma_separated_random_numbers)