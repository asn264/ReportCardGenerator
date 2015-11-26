import sys
import pandas as pd
from geopy import geocoders
from geopy.exc import GeocoderTimedOut, GeocoderParseError, GeocoderQueryError, GeocoderQuotaExceeded, GeocoderUnavailable

school_database = pd.read_csv('database.csv')

def prompt_for_mode():

	'''Asks the user to choose a mode. Accepts KeyboardInterrupt and EOFError.'''
	try:
		return raw_input("Enter 'location' to generate reports by proximity and 'name' to search schools by name: ")
	except (KeyboardInterrupt, EOFError):
		sys.exit()	


def interpret_mode(input):
	
	'''Interprets str as a mode. Accepts "quit".'''
	if input.strip().lower() == 'quit':
		sys.exit()	
	elif input.strip().lower() in ['location', 'name'] :
		return input.strip().lower()
	else:
		print "Invalid Mode."
		return None


def get_mode():

	'''Recursively asks the user to choose a mode and interprets it.'''
	mode = interpret_mode(prompt_for_mode())
	if mode is not None:
		return mode
	else:
		return get_mode()


def prompt_for_location():

	'''Asks the user to provide a location. Accepts KeyboardInterrupt and EOFError.'''
	try:
		return raw_input("Enter an address or a set of coordinates: ")
	except (KeyboardInterrupt, EOFError):
		sys.exit()


def validate_location(input):

	'''Makes a best guess of user provided input using Google Maps. 
	Complains if the (best-guess) city is not a city that appears in the school database.'''

	g = geocoders.GoogleV3()

	if input.strip().lower() == 'quit':
		sys.exit()

	else:

		cities = pd.unique(school_database['city'].values.ravel())
		
		try:

			#place.address is in unicode. Cast it as string and split into a list of strings. 
			place = g.geocode(input, timeout=30)
			components = str(place.address).split(", ")
			for c in components:
				if c in cities:
					return (place.latitude, place.longitude)

			#This code gets executed if there is no match in str for any of the cities in the database.
			print "Invalid location."
			return None

		#AttributeError occurs if the service could not find a best-match place for the string and place = None.
		except AttributeError:
			print "Invalid location."
			return None
		#The following errors all pertain to errors with GeoPy and Google's geocoding service. 
		except GeocoderTimedOut:
			print "Remote geocoding service timed out. Try again or enter another location."
			return None
		except GeocoderParseError:
			print "Geopy could not parse service's response. Try again or enter another location."
			return None
		except GeocoderQueryError:
			print "Geopy detected a bad request. Try again or enter another location."
			return None
		except GeocoderQuotaExceeded: 
			print "You have exceeded your quota for requests to the geocoding service."
			return None
		except GeocoderUnavailable:
			print "Remote geocoding service is unavailable. Try again or enter another location."
			return None


def get_location():

	'''Recursively asks the user to enter a location and validates it.'''
	location = validate_location(prompt_for_location())
	if location is not None:
		return location
	else:
		return get_location()
	

def prompt_for_radius():

	'''Asks the user to provide a positive-valued radius. Accepts KeyboardInterrupt and EOFError.'''
	try: 
		return raw_input("Enter a radius: ")
	except(KeyboardInterrupt, EOFError):
		sys.exit()


def validate_radius(input):

	'''Ensure that the radius is a positive int or float.'''
	if input.lower() == 'quit':
		sys.exit()

	else:

		try:

			#If no error is raised then str is an int but not necessarily positive.
			return int(input) if int(input) > 0 else None

		except ValueError:

			#If no error is raised then str is a float but not necessarily positive.
			try:

				return float(input) if float(input) > 0 else None

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


def prompt_for_names():

	'''Asks for a list of names.'''
	try:
		return raw_input("Enter a list of comma-separated, high school names. If needed, see SchoolDirectory.txt for reference: ")
	except(KeyboardInterrupt,EOFError):
		sys.exit()


def validate_names(input):

	'''Takes a string containing a list of school names and makes sure that these schools are in the directory.'''

	if input.strip().lower() == 'quit':
		sys.exit()

	else:

		#Split the input string into a list of strings on the comma indices
		names = [name.strip() for name in input.split(",")]
		failed = []
		schools = pd.unique(school_database['school_name'].values.ravel())

		for i in range(len(names)):
				if names[i] not in schools:
					failed.append(names[i])

		return [names, failed]


def prompt_to_ignore_invalid_names():

	try:
		return raw_input('''Would you like to generate reports for the schools that were in our directory? Type 'yes' to proceed. Press any other key to enter another list of schools: ''')

	except (KeyboardInterrupt,EOFError):
		sys.exit()

def ignore_invalid_names(input):

	if input.strip().lower() == 'quit':
		sys.exit()
	elif input.strip().lower() == "yes":
		return True
	else:
		return False


def get_names():
	'''Recursively asks the user to provide a list of names. If there are invalid names in the list, 
	the user has the option to re-enter the list or continue with the valid ones in the provided list.'''

	names, failed = validate_names(prompt_for_names())

	if len(failed):
		
		if len(names) == len(failed):
			print "None of the schools you have provided are in our directory."
			return get_names()

		else:

			print "The following schools are not available in our directory: ", 
			for name in range(len(failed)):
				print failed[name],
			print "\n"

			#Give the user the option to continue if there are some valid names in the list. 			
			return [s for s in names if s not in failed] if ignore_invalid_names(prompt_to_ignore_invalid_names()) == True else get_names()

	else:
		return names


def no_schools():
	'''Alerts the user when no schools are found within the distance of the given location'''

	print "There were no schools found within the radius you specified of the input location."
	get_location()

	
def prompt_for_number():
	'''Asks for he number of schools the user wants.'''
	try:
		return raw_input("There are "+str(length)+" schools in this radius.\n How many of the closest schools do you want to generate a report of? ")
	except(KeyboardInterrupt,EOFError):
		sys.exit()


def validate_number(input,length):
	'''Ensure that the input is a positive integer not greater than the length of names'''
	
	if input.lower() == 'quit':
		sys.exit()
	else:
		try:

			#validates input
			return int(input) if (int(input) > 0 and int(input<=length)) else None
		except ValueError:
				return None


def get_number(length):
	'''Recursively asks the user how many of the schools within the radius they want to get a report on. 
	Verifies that the input is valid'''

	number = validate_number(prompt_for_number(length),length)

	if number is not None:
		return number
	else:
		print "Invalid number."
		return get_number()




	

	


	

		

