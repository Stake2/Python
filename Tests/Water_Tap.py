#  Water_Tap.py

from Water_Pipe import Water

water_tap_is_open = True

i = 0
while water_tap_is_open == True and i <= len(Water) - 1:
	print(Water[i])

	i += 1

	if water_tap_is_open == False:
		quit()