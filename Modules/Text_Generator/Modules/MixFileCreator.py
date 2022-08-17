import os
from Folder_Variables import *

testfile = scripts_folder + 'Test File.txt'
gametimesfile = game_times_text_file_enus

filenames = [
game_times_text_filename_enus,
'Current Wills',
'Quantos litros de água bebi no dia',
]

filescollection = filenames

currentwillsfile = notepad_folder + filenames[1] + '.txt'

file = testfile
if not os.path.isfile(file):
	f = open(file, 'w', encoding='utf8')
	f.close()

filetexts = []

array = filenames
textfiles = [
gametimesfile,
currentwillsfile,
notepad_folderwaterfiles + array[2] + '.txt',
]

i = 0
array = textfiles
number = len(array) - 1
while i <= number:
	file = array[i]

	openfile = open(file, 'rt', encoding='utf8')
	filetexts.append(openfile.readlines())
	openfile.close()

	z = 0
	array2 = filetexts[i]
	number2 = len(array2) - 1
	while z <= number2:
		if z != number2:
			array2[z] = array2[z]

		else:
			array2[z] = array2[z].replace("\n", '')

		z += 1

	i += 1

titles = []

i = 0
array = titles
number = len(filescollection) - 1
while i <= number:
	array.append(filescollection[i])

	i += 1

file = testfile
openfile = open(file, 'rt', encoding='utf8')
readfiletexts = openfile.read()

i = 0
array1 = readfiletexts
array2 = filetexts
number = len(array2) - 1
while i <= number:
	if titles[i] not in array1:
		array1 = array1 + "\n" + "\n" + '\\\n"' + titles[i] + '" ' + 'file' + ': ' + "\n"

	z = 0
	while z <= len(array2[i]) - 1:
		if array2[i][z] not in array1 and i != 2:
			array1 = array1 + array2[i][z]
			lastone = True

		else:
			if i == 2:
				array1 = array1 + array2[i][z]
				lastone = True

			else:
				lastone = False

		z += 1

	if lastone == True:
		array1 = array1 + "\n" + '/'

	i += 1

openfile.close()

openfile = open(file, 'wt', encoding='utf8')
openfile.write(array1)
openfile.close()

file = testfile
openfile = open(file, 'rt', encoding='utf8')
filetext = openfile.readlines()
openfile.close()

show = False
#False
#True

if show == True:
	i = 0
	array = filetext
	number = len(array) - 1
	while i <= number:
		text = array[i].replace("\n", '')
		print(text)

		i += 1

print()
print()