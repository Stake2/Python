# New_World_Variables.py

import datetime
from Script_Helper import year, current_year
from Language_Variables import global_language, language_en, language_pt

# Creates some universe types, the types of universe that exist in the multiverse
new_world_universe_types = [None, "New World", "Old World"]
new_world_universe_types_small = [None, "nw", "ow"]

# Gets the length of the universe types array
new_world_universe_types_len = len(new_world_universe_types) - 1

# Creates two variables for the New World universe type, one for the normal version and one for the small version
new_world_name = new_world_universe_types[1]
new_world_name_small = new_world_universe_types_small[1]

# Creates two variables for the Old World universe type, one for the normal version and one for the small version
old_world_name = new_world_universe_types[2]
old_world_name_small = new_world_universe_types_small[2]

most_oldest_person_age = 90

# Creates an array of ages between 3 and 90
ages = []
for i in range(3, most_oldest_person_age + 1):
	ages.append(i)

# Gets the length of the ages array
ages_len = len(ages) - 1

# Defines the "being genres" arrays
genres_enus = [None, "Male", "Female"]
genres_ptbr = [None, "Masculino", "Feminino"]

# Gets the length of the being genres arrays
genres_enus_len = len(genres_enus) - 1
genres_ptbr_len = len(genres_ptbr) - 1

# Defines two variables for each genre, one for the female one and one for the male one
i = 1

genre_enus_male = genres_enus[i]
genre_ptbr_male = genres_ptbr[i]

i += 1

genre_enus_female = genres_enus[i]
genre_ptbr_female = genres_ptbr[i]

if global_language == language_en:
	races_array = [
	None,
	"Human",
	"Dragon",
	"Angel",
	"Snake",
	"Dinosaur",
	"Bird",
	"Hawk",
	"Phoneix",
	"Mouse",
	"Dog",
	"Cat",
	"Bat",
	"Elephant",
	]

	races_extended_array = [
	None,
	"Human (Homo Sapiens Sapiens)",
	"Dragon",
	"Angel",
	"Snake",
	"Dinosaur",
	"Bird",
	"Hawk",
	"Phoneix",
	"Mouse",
	"Dog",
	"Cat",
	"Bat",
	"Elephant",
	]

if global_language == language_pt:
	races_array = [
	None,
	"Humano",
	"Dragão",
	"Anjo",
	"Cobra",
	"Dinossauro",
	"Pássaro",
	"Águia",
	"Fênix",
	"Rato",
	"Cachorro",
	"Gato",
	"Morcego",
	"Elefante",
	]

	races_extended_array = [
	None,
	"Humano (Homo Sapiens Sapiens)",
	"Dragão",
	"Anjo",
	"Cobra",
	"Dinossauro",
	"Pássaro",
	"Águia",
	"Fênix",
	"Rato",
	"Cachorro",
	"Gato",
	"Morcego",
	"Elefante",
	]

races_small_array = [
None,
"hmn",
"drg",
"ang",
"snk",
"din",
"bird",
"hawk",
"phx",
"mse",
"dog",
"cat",
"bat",
"elent",
]

mars_years_array = {
"2019": "35/90",
"2020": "35/359",
"2021": "36/90",
"2022": "37/0",
"2023": "37/90",
"2024": "38/0",
"2025": "38/180",
"2026": "39/0",
"2027": "39/180",
"2028": "40/0",
"2029": "40/180",
"2030": "40/359",
}

mars_year = mars_years_array[str(current_year)]

planets_array = [
None,
"Earth_MW(7B_2020)",
"Mars_MW(0K_" + mars_year + ")",
]

planet_earth = planets_array[1]
planet_mars = planets_array[2]

if global_language == language_en:
	planet_id_earth = planet_earth + ''':

Given Name By The Local Species: Planet Earth
Resides On The Galaxy: Milky Way
Number Of Beings: 7 Billions
Current Year In The Planet's Calendar: ''' + str(current_year)

	planet_id_mars = planet_mars + ''':

Given Name By The Local Species: Mars
Resides On The Galaxy: Milky Way
Number Of Beings: 0
Current Year In The Planet's Calendar: ''' + str(mars_year)

if global_language == language_pt:
	planet_id_earth = planet_earth + ''':

Nome Dado Pela Espécie Local: Planeta Terra
Fica Na Galáxia: Via Láctea
Número De Seres: 7 Bilhões
Ano Atual No Calendário Do Planeta: ''' + str(current_year)

	planet_id_mars = planet_mars + ''':

Nome Dado Pela Espécie Local: Marte
Fica Na Galáxia: Via Láctea
Número De Seres: 0
Ano Atual No Calendário Do Planeta: ''' + str(mars_year)

race_human = races_array[1]
race_human_extended = races_extended_array[1]

race_dragon = races_array[2]

races_array_len = len(races_array) - 1