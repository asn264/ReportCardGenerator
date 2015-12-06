'''
Authors: Aditi Nair (asn264) and Akash Shah (ass502)
Created: November 13 2015

'''

from mode import *
from names import *
from location import *
from top10 import *
from filename import *
from comparison_writer import *
import sys


def main():

	#Ask the user to choose a mode
	mode = get_mode()

	if mode == 'top10':

		#Prompts the user to enter a set of ranking metrics and weights to build a custom school ranking report 
		schools = get_top10_schools()

	else:

		#Allows the user to choose schools either by location, or explicitly by name
		schools = get_schools_by_location() if mode=='location' else get_schools_by_name()


	#Asks the user to choose a filename. Does not allow overwriting. 
	filename = get_filename()

	#Create a PDF report 
	#writer = SummaryWriter(filename, mode, schools)
	#writer.write_report()

	writer = ComparisonWriter(mode,schools)
	writer.write_report()
		
	
#Run the program
if __name__ == "__main__":
	try:
		main()
	except (KeyboardInterrupt, EOFError): #quit the program on ctrl-c and ctrl-d inputs
		sys.exit()	
