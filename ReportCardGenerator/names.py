import sys
import pandas as pd
from utilities import *

def prompt_for_names():

	'''Asks for a list of names.'''
	try:
		return raw_input("Enter a list of comma-separated, high school names. If needed, see SchoolDirectory.txt for reference: ")
	except(KeyboardInterrupt,EOFError):
		sys.exit()


def validate_names(input):

	'''Takes a string containing a list of school names and makes sure that these schools are in the directory.'''

	if input.strip().lower() == 'quit':
		sys.exit()

	else:

		#Split the input string into a list of strings on the comma indices
		names = [name.strip() for name in input.split(",")]
		failed = []
		schools = pd.unique(school_database['school_name'].values.ravel())

		for i in range(len(names)):
				if names[i] not in schools:
					failed.append(names[i])

		return [names, failed]


def prompt_to_ignore_invalid_names():

	try:
		return raw_input('''Would you like to generate reports for the schools that were in our directory? Type 'yes' to proceed. Press any other key to enter another list of schools: ''')

	except (KeyboardInterrupt,EOFError):
		sys.exit()

def ignore_invalid_names(input):

	if input.strip().lower() == 'quit':
		sys.exit()
	elif input.strip().lower() == "yes":
		return True
	else:
		return False


def get_names():
	'''Recursively asks the user to provide a list of names. If there are invalid names in the list, 
	the user has the option to re-enter the list or continue with the valid ones in the provided list.'''

	names, failed = validate_names(prompt_for_names())

	if len(failed):
		
		if len(names) == len(failed):
			print "None of the schools you have provided are in our directory."
			return get_names()

		else:

			print "The following schools are not available in our directory: ", 
			for name in range(len(failed)):
				print failed[name],
			print "\n"

			#Give the user the option to continue if there are some valid names in the list. 			
			return [s for s in names if s not in failed] if ignore_invalid_names(prompt_to_ignore_invalid_names()) == True else get_names()

	else:
		return names

