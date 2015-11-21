from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from data import *
import pandas as pd

geolocator = Nominatim()

def find_schools_in_radius(location,radius):
	current_location = geolocator.geocode(location)
	names=[]
	for school in school_database['school_name']:
		school_data = school_database.loc[school_database['school_name']==school]
		school_location = geolocator.geocode(school_data['primary_address_line_1'])
		#print school
		distance = vincenty(current_location,school_location)
		if distance < radius:
			names.append(school)
	return names

print(find_schools_in_radius("175 5th Avenue NYC",1))
