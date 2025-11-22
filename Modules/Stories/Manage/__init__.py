# Manage.py

# Import the root class
from Stories.Stories import Stories as Stories

class Manage(Stories):
	def __init__(self):
		# Run the root class of the "Modules" module
		self.Modules(object = self, select_class = True)