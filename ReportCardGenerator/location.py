import sys
import pandas as pd
from geopy import geocoders
from geopy.distance import vincenty
from geopy.exc import GeocoderTimedOut, GeocoderParseError, GeocoderQueryError, GeocoderQuotaExceeded, GeocoderUnavailable

school_database = pd.read_csv('database.csv')

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


def sort_schools_by_distance(names,distances):
	"""modified implementation of bubble sort, sorting names based on distance"""
	
	for i in range(len(distances)):
		for j in range(len(distances)-1-i):
			if distances[j]>distances[j+1]:
				distances[j],distances[j+1]=distances[j+1],distances[j]
				names[j],names[j+1]=names[j+1],names[j]
	
	return names


def find_schools_in_radius(coordinates,radius):
	"""function that returns the names of all schools within a specified radius of a location, sorted by distance"""

	names=[]
	distances=[]
	for row in range(len(school_database)):
		distance = vincenty(coordinates,school_database.iloc[row]['coordinates']).miles
		if distance <= radius:
			names.append(school_database.iloc[row]['school_name'])
			distances.append(distance)
	return sort_schools_by_distance(names,distances)