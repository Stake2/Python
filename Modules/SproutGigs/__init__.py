# SproutGigs.py

class Run():
	def __init__(self):
		from SproutGigs.Work import Work as Work

		# If the "Do not run class" variable is not present in this class
		if hasattr(self, "do_not_run_class") == False:
			Work()

if __name__ == "__main__":
	Run()