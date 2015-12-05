from School import *
import sys

def prompt_for_names():
	'''Asks for a list of names.'''

	return raw_input("Enter a list of comma-separated, high school names. If needed, see SchoolDirectory.txt for reference: ")


def validate_names(input):

	'''Takes a string containing a list of school names and makes sure that these schools are in the directory.'''

	if input.strip().lower() == 'quit':
		sys.exit()

	else:

		#Split the input string into a list of strings on the comma indices
		names = [name.strip() for name in input.split(",")]

		passed = []
		failed = []

		for i in range(len(names)):
	
			try:
				passed.append(School(names[i]))
	
			#Cannot construct a school object if the provided name is not in the global list school_names
			except InvalidSchoolNameError:
				failed.append(names[i])

		return [passed, failed]


def prompt_to_ignore_invalid_names():

	return raw_input('''Would you like to generate reports for the schools that were in our directory? Type 'yes' to proceed. Press any other key to enter another list of schools: ''')


def ignore_invalid_names(input):

	if input.strip().lower() == 'quit':
		sys.exit()
	elif input.strip().lower() == "yes":
		return True
	else:
		return False


def get_schools_by_name():
	'''Recursively asks the user to provide a list of names. If there are invalid names in the list, 
	the user has the option to re-enter the list or continue with the valid ones in the provided list.'''

	passed, failed = validate_names(prompt_for_names())

	if len(failed) > 0:
		
		if len(passed) == 0:
			print "None of the schools you have provided are in our directory."
			return get_schools_by_name()

		else:

			print "The following schools are not available in our directory: ", 
			for school in range(len(failed)):
				print failed[school]+",",
			print "\n"

			#Give the user the option to continue if there are some valid names in the list. 			
			return passed if ignore_invalid_names(prompt_to_ignore_invalid_names()) == True else get_schools_by_name()

	else:
		#Even though the user is allowed to enter non-unique schools, we will ignore duplicates. 
		return list(set(passed))

