from geopy.distance import great_circle
import pandas as pd

school_database = pd.read_csv('database.csv')

def find_schools_in_radius(coordinates,radius):
	#current_location = geolocator.geocode(location)
	#current_coordinates = (current_location.latitude,current_location.longitude)

	names=[]
	for row in range(len(school_database)):
		distance = great_circle(coordinates,school_database.iloc[row]['coordinates']).miles
		if distance <= radius:
			names.append(school_database.iloc[row]['school_name'])
	return names

def generate_report(mode,names=[],location=(0,0),radius=0):
	if mode=='location':
		names = find_schools_in_radius(location,radius)
	for name in names:
		#create instance of class
		school = SchoolData(name)
		#use member functions to create report
		




