import sys

def prompt_for_mode():

	'''Asks the user to choose a mode. Accepts KeyboardInterrupt and EOFError.'''
	try:
		return raw_input("Enter 'location' to generate reports by proximity and 'name' to search schools by name.")
	except (KeyboardInterrupt, EOFError):
		sys.exit()	


def interpret_mode(str):
	
	'''Interprets str as a mode. Accepts "quit".'''
	if str.strip().lower() == 'quit':
		sys.exit()	
	elif str.strip().lower() in ['location', 'name'] :
		return str.strip().lower()
	else:
		print "Invalid Mode."
		return None


def get_mode(str):

	'''Recursively asks the user to choose a mode and interprets it.'''
	mode = interpret_mode(prompt_for_mode())
	if mode is not None:
		return mode
	else:
		return get_mode()


def prompt_for_loc():

	'''Asks the user to provide a location. Accepts KeyboardInterrupt and EOFError.'''
	try:
		return raw_input("Enter an address or a set of coordinates.")
	except (KeyboardInterrupt, EOFError):
		sys.exit()


def interpret_loc(str):

	'''Validate the location provided using GeoPy. Verify the location is in NYC.'''
	if str.strip().lower() == 'quit':
		sys.exit()
	else:
		pass


def get_loc():

	'''Recursively asks the user to enter a location and validates it.'''
	loc = interpret_loc(prompt_for_loc())
	if loc is not None:
		return loc
	else:
		print "Invalid location."
		return get_loc()
	

def prompt_for_radius():

	'''Asks the user to provide a positive-valued radius. Accepts KeyboardInterrupt and EOFError.'''
	try: 
		return raw_input("Enter a radius.")
	except(KeyboardInterrupt, EOFError):
		sys.exit()


def validate_radius(str):

	'''Ensure that the radius is a positive int or float.'''
	if str.lower() == 'quit':
		sys.exit()

	else:

		try:

			#If no error is raised then str is an int but not necessarily positive.
			return int(str) if int(str) > 0 else None

		except ValueError:

			#If no error is raised then str is a float but not necessarily positive.
			try:

				return float(str) if float(str) > 0 else None

			#This only occurs if str is neither an int nor a float
			except ValueError:
				return None
		

def get_radius():

	'''Recursively asks the user to enter a radius. Only accepts positive numeric values.'''
	rad = validate_radius(prompt_for_radius())
	if rad is not None:
		return rad
	else:
		print "Invalid radius."
		return get_radius()



	

	


	

		

