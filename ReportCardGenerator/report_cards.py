'''
Authors: Aditi Nair (asn264) and Akash Shah (ass502)
Created: November 13 2015

This is the main program that interacts with the user. 
Please consult README.pdf for instructions and additional information.
'''

#import modules/classes
from mode import *
from names_toolkit import *
from location_toolkit import *
from top10_toolkit import *
from filename import *
from summary_writer import *
from utilities import *


def main():

	#load the cleaned database, the school names and the valid features
	school_database, school_names, valid_features = load_session()

	#Ask the user to choose a mode
	mode = get_mode()

	if mode == 'top10':

		#Prompts the user to enter a set of ranking metrics and weights to build a custom school ranking report 
		top10_mode = Top10_Toolkit(school_database,school_names,valid_features)
		schools,user_parameters = top10_mode.get_top10_schools()

	elif mode == 'location':

		#Prompts the user to enter an address and a radius to find all schools in the area and build a report
		location_mode = Location_Toolkit(school_database,school_names)
		schools,user_parameters = location_mode.get_schools_by_location() 
		
	#Here mode is necessarily 'names'
	else:

		#Prompts user to enter a list of school names to build a report
		names_mode = Names_Toolkit(school_database,school_names)
		schools = names_mode.get_schools_by_name()


	#Asks the user to choose a filename. Does not allow overwriting. 
	filename = get_filename()

	#Create an instance of the SummaryWriter
	if mode == 'name':
		writer = SummaryWriter(school_database, valid_features, filename, mode, schools)
	else:
		writer = SummaryWriter(school_database, valid_features, filename, mode, schools, user_parameters)
		
	#Create a PDF report using ReportLab
	writer.write_report()

	#If visualizations were provided, clear the temporary directory containing the .png files.
	if writer.enable_visualizations:
		writer.graph_generator.clear_plots_directory()

	print "\nYour report is complete! Please refer to " + filename + "."

	
#Run the program
if __name__ == "__main__":
	try:
		main()
	except (KeyboardInterrupt, EOFError): #quit the program on ctrl-c and ctrl-d inputs
		sys.exit()	
