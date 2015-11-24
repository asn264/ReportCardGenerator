'''
Authors: Aditi Nair (asn264) and Akash Shah (ass502)
Created: November 13 2015

'''

#Consider explaining the program to the user
#Finish writing validate_loc
#What kind of radii does GeoPy accept

from Interactions import *
from generate import *


def main():

	#Ask the user to choose a mode
	mode = get_mode()

	if mode == 'location':
	
		#Ask the user to provide a location
		loc = get_location()
		
		#Ask the user to provide a radius
		rad = get_radius()

		#Get all schools in the radius
		schools = find_schools_in_radius(loc,rad)
		
		#Create a report
		generate_report(mode,location=loc,radius = rad)
	
	#Here the mood is necessarily 'name'
	else:
	
		'''To Do: names = get_names, a list. 
		And validate names from a backend list somewhere'''

		#Ask the user to provide names
		names = get_names()
		
		#Create a report 
		generate_report(mode, names) 
		
	
#Run the program
if __name__ == "__main__":
	main()