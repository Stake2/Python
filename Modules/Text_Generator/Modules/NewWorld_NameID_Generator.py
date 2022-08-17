from Script_Helper import *
import random
from random import *
import datetime

# Gets the now time
now = datetime.datetime.now()

# Gets the current year
current_year = int(now.year)

# Female names and surnames arrays
female_names = ["Angélica", "Sofia", "Ana"]
female_surnames = ["Rubens", "Silva", "Linz"]

# Male names and surnames arrays
male_names = ["Marcos", "Felipe", "João", "Angelo", "Izaque"]
male_surnames = ["Sanvezzo", "Yorkishire", "Bezerra"]

# Generates one new NameID
def Generate_New_NameID():
	global universe_type
	global universe_type_full
	global full_genre
	global genre
	global age
	global birthday_year
	global name
	global surname
	global full_name
	global race
	global race_and_sex
	global full_new_world_nameid

	# Defines the genre of the person using a random integer between 0 and 1
	genre = genres_enus[randint(0, genres_enus_len)]

	# If the genre is female then it will use the female names and surnames arrays, it will set the genre as "f" for female
	if genre == genre_female:
		name_array = female_names
		surname_array = female_surnames

		full_genre = genre_female
		genre = "f"

	# If the genre is male then it will use the male names and surnames arrays, it will set the genre as "m" for male
	if genre == genre_male:
		name_array = male_names
		surname_array = male_surnames

		full_genre = genre_male
		genre = "m"

	# Defines the name and surname of the being using a random integer between 0 and the total length of the names and surnames arrays
	name = name_array[randint(0, len(name_array) - 1)]
	surname = surname_array[randint(0, len(surname_array) - 1)]

	# Concatenates the name and surname strings together
	full_name = name + " " + surname

	# Create the universe_selector which is a random integer between 0 and the total length of the universe types array
	universe_selector = randint(0, new_world_universe_types_len)

	# Selects a universe type between New World and Old World using the random integer created in the universe_selector variable
	universe_type = new_world_universe_types_small[universe_selector]
	universe_type_full = new_world_universe_types[universe_selector]

	# Defines the race and small race of the being
	race = "Human"
	small_race = "h"

	# Concatenates the race string with the genre string
	race_and_sex = small_race + genre

	# Selects the age of the being using a random integer between 0 and the total length of the ages array
	age = ages[randint(0, ages_len)]

	# Calculates the birthday year of the being by subtracting the age from the current year
	birthday_year = current_year - age

	# Concatenates the full name, universe type, small race, genre, age, and birthday year together
	full_new_world_nameid = full_name + "(" + universe_type + "_" + race_and_sex + "_" + str(age) + "_" + str(birthday_year) + ")"

# Generates a list of new NameIDs, append them to an array, and print all of them
def Generate_List_Of_NameIDs():
	global name_ids

	# The number of new NameIDs to generate
	random_name_id_range = 5

	print()
	print("---")
	print()

	# Prints the amount of new NameIDs that will be displayed
	print("Showing {} random NameIDs:".format(random_name_id_range))

	name_ids = []
	for i in range(1, random_name_id_range + 1):
		# Generates the new NameID
		Generate_New_NameID()

		# Appends the new NameID to the name_ids array
		name_ids.append(full_new_world_nameid)

		# Shows some additional text if the NameID contains certain features (deactivated)
		'''
		if universe_type == old_world_name_small:
			print("The being is an Old World being.")

		if birthday_year == 2002:
			print("Birthday year is: " + str(birthday_year))

		if age == 19 or age == 18:
			print("Age is: " + str(age))

		if genre == genre_female:
			print("The being is a female.")
		'''

		# Shows the new NameID
		print(full_new_world_nameid)
		print()

# Variable to declare if the detailed info of the NameID will be displayed
detailed_info = True

# Variable to declare if the list of new NameIDs will be generated
generate_list_of_nameids = False

# Runs the Generate_New_NameID function
#Generate_New_NameID()

# Shows the full New World NameID on the console
print("Full New World NameID is: " + full_new_world_nameid)

# Shows the full detailed info of the NameID on the console if the detailed_info variable is True
if detailed_info == True:
	print()
	print("Name is: " + name)
	print("Surname is: " + surname)
	print()
	print("Full name is: " + full_name)
	print()
	print("Universe type is: " + universe_type_full)
	print()
	print("Race is: " + race)
	print("Genre is: " + full_genre)
	print()
	print("Age is: " + str(age))
	print("Birthday year is: " + str(birthday_year))

# Generates the list of new NameIDs if the generate_list_of_nameids variable is True
if generate_list_of_nameids == True:
	Generate_List_Of_NameIDs()