'''
Authors: Aditi Nair (asn264) and Akash Shah (ass502)
Created: November 13 2015

'''

#Consider explaining the program to the user
#Finish writing validate_loc
#What kind of radii does GeoPy accept

from mode import *
from names import *
from location import *


def main():

	#Ask the user to choose a mode
	mode = get_mode()

	if mode == 'location':

		print get_schools_by_location()
	
	#Here the mode is necessarily 'name'
	else:

		#Recursively ask the user to provide names. Validate and return list of School objects. 
		schools = get_schools_by_name()
	
	#Create a report 
	#generate_report(names) 
		
	
#Run the program
if __name__ == "__main__":
	main()