'''
Authors: Aditi Nair (asn264) and Akash Shah (ass502)

This module contains the Location_Toolkit class, an instance of which represents an iteration of location mode. 
In location mode, the user can provide an address or coordinates and a radius. The starting location must be in one 
of the cities that appears in our database.
The user is shown how many New York City high schools are within that radius of the address, and then the user provides 
how many of the closest schools they want to generate a report of.
'''

#import modules/classes
from school import *

#import necessary libraries
import pandas as pd
import sys

#import relevant geopy libraries
from geopy import geocoders
from geopy.distance import vincenty
from geopy.exc import GeocoderTimedOut, GeocoderParseError, GeocoderQueryError, GeocoderQuotaExceeded, GeocoderUnavailable


class Location_Toolkit(object):

	def __init__(self, school_database, school_names):

		'''Create instance of location mode, instance variables contain the relevant data'''

		self.school_database = school_database
		self.school_names = school_names
		self.cities = pd.unique(school_database['city'].values.ravel())


	def get_schools_by_location(self):
		'''Uses helper functions in the location module to prompt the user for a location and radius, 
		and the number of schools within that radius to generate a report of. A list of school objects is returned.'''

		#Get location from the user
		location,input_location = self.get_location()

		#Get all schools within the input radius of the specified location
		names,input_radius = self.find_schools_in_radius(location,self.get_radius())

		while len(names)==0: #if there are no schools in the radius
			self.no_schools()
			names,input_radius = self.find_schools_in_radius(location,self.get_radius())

		#Get the number of schools the user wants to generate reports of
		num = self.get_number(len(names))
		#Only use the closest schools
		names=names[:num]

		#instantiate each school object and store all of the schools we want in a list
		schools=[]
		for name in names:
			schools.append(School(self.school_database,self.school_names,name))

		return schools,[input_location,input_radius]


	def find_schools_in_radius(self,coordinates,radius):

		'''Function that returns the names of all schools within a specified radius of a location, sorted by distance.'''

		#Add a new column which shows the distance of each school from the coordinates
		self.school_database['distances'] = self.school_database['coordinates'].apply(lambda x: vincenty(coordinates, x).miles)

		#Sort the dataframe by distance
		self.school_database.sort('distances', inplace=True)

		#Return a list of the schools with radius distance of the coordinates and the actual radius
		return self.school_database['school_name'][self.school_database['distances']<radius].tolist(), radius


	@staticmethod
	def prompt_for_location():
		'''Asks the user to provide a location'''

		return raw_input("\nEnter an address or a set of coordinates. If needed, see school_directory.csv for reference. ")


	def validate_location(self,input):
		'''Makes a best guess of user provided input using Google Maps. 
		Complains if the (best-guess) city is not a city that appears in the school database.'''

		#uses GoogleV3 API to validate addresses
		g = geocoders.GoogleV3()

		if input.strip().lower() == 'quit':
			sys.exit()

		else:
			
			try:

				#place.address is in unicode. Cast it as string and split into a list of strings. 
				place = g.geocode(input, timeout=30)
				components = str(place.address).split(", ")
				for c in components:
					if c in self.cities:
						return (place.latitude, place.longitude),input

				#This code gets executed if there is no match in str for any of the cities in the database.
				print "\nThe location is not in the New York City area."
				return None

			#AttributeError occurs if the service could not find a best-match place for the string and place = None.
			except (AttributeError,UnicodeEncodeError):
				print "\nInvalid location."
				return None
			#The following errors all pertain to errors with GeoPy and Google's geocoding service. 
			except GeocoderTimedOut:
				print "\nRemote geocoding service timed out. Try again or enter another location."
				return None
			except GeocoderParseError:
				print "\nGeopy could not parse service's response. Try again or enter another location."
				return None
			except GeocoderQueryError:
				print "\nGeopy detected a bad request. Try again or enter another location."
				return None
			except GeocoderQuotaExceeded: 
				print "\nYou have exceeded your quota for requests to the geocoding service."
				return None
			except GeocoderUnavailable:
				print "\nRemote geocoding service is unavailable. Try again or enter another location."
				return None


	def get_location(self):
		'''Recursively asks the user to enter a location and validates it.'''

		user_location = self.validate_location(self.prompt_for_location())
		if user_location is not None:
			return user_location
		else:
			return self.get_location()
		
	@staticmethod
	def prompt_for_radius():
		'''Asks the user to provide a positive-valued radius'''

		return raw_input("\nEnter a radius in miles: ")

	@staticmethod
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
			
	def get_radius(self):
		'''Recursively asks the user to enter a radius. Only accepts positive numeric values.'''

		rad = self.validate_radius(self.prompt_for_radius())
		if rad is not None:
			return rad
		else:
			print "\nInvalid radius."
			return self.get_radius()


	@staticmethod
	def no_schools():
		'''Alerts the user when no schools are found within the distance of the given location'''

		print "\nThere were no schools found within the radius you specified of the input location."

	@staticmethod	
	def prompt_for_number(length):
		'''Asks for the number of schools the user wants.'''

		return raw_input("\nThere are "+str(length)+" schools in this radius.\nHow many of the closest schools do you want to generate a report of? ")

	@staticmethod
	def validate_number(input,length):
		'''Ensure that the input is a positive integer not greater than the length of names'''
		
		if input.lower() == 'quit':
			sys.exit()
		else:
			try:
				#validates input
				return int(input) if (int(input) > 0 and int(input)<=length) else None
			except ValueError:
					return None

	def get_number(self,length):
		'''Recursively asks the user how many of the schools within the radius they want to get a report on. 
		Verifies that the input is valid'''

		number = self.validate_number(self.prompt_for_number(length),length)

		if number is not None:
			return number
		else:
			print "\nInvalid number."
			return self.get_number(length)



