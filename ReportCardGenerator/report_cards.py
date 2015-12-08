'''
Authors: Aditi Nair (asn264) and Akash Shah (ass502)
Created: November 13 2015

'''

#import modules/classes
from mode import *
from names import *
from location import *
from top10 import *
from filename import *
from summary_writer import *

#import necessary libraries
import sys


def main():

	#Ask the user to choose a mode
	mode = get_mode()

	if mode == 'top10':

		#Prompts the user to enter a set of ranking metrics and weights to build a custom school ranking report 
		schools,user_parameters = get_top10_schools()

	elif mode == 'location':

		#Prompts the user to enter an address and a radius to find all schools in the area and build a report
		schools,user_parameters = get_schools_by_location() 
		

	else:

		#Prompts user to enter a list of school names to build a report
		schools = get_schools_by_name()



	#Asks the user to choose a filename. Does not allow overwriting. 
	filename = get_filename()

	#Create a PDF report 
	try:
		writer = SummaryWriter(filename, mode, schools, user_parameters)
		writer.write_report()

	except InvalidSummaryWriterError:
		print "Something went wrong."
		sys.exit()

		
	
#Run the program
if __name__ == "__main__":
	try:
		main()
	except (KeyboardInterrupt, EOFError): #quit the program on ctrl-c and ctrl-d inputs
		sys.exit()	
