from geopy.distance import vincenty
import pandas as pd

school_database = pd.read_csv('database.csv')

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

def generate_report(names):
	#for name in names:
		#create instance of class
		#school = SchoolData(name)
		#use member functions to create report

def sort_schools_by_distance(names,distances):
	"""modified implementation of bubble sort, sorting names based on distance"""
	
	for i in range(len(distances)):
		for j in range(len(distances)-1-i):
			if distances[j]>distances[j+1]:
				distances[j],distances[j+1]=distances[j+1],distances[j]
				names[j],names[j+1]=names[j+1],names[j]
	
	return names
		




