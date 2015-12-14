'''
Authors: Aditi Nair (asn264) and Akash Shah (ass502)

This module contains the Names_Toolkit class, an instance of which represents an iteration of names mode. 
In names mode, the user can provide a list of NYC high schools. If some of the user-provided schools are not 
available in our database, we present the user with the option of continuing with the schools that are in
our database, or with the option of presenting an entirely new list of schools. 

'''

from school import *
import sys

class Names_Toolkit(object):

	def __init__(self, school_database, school_names):
		'''create instance of top10 mode, instance variables contain the relevant data'''

		self.school_database = school_database
		self.school_names = school_names

	@staticmethod
	def prompt_for_names():
		'''Asks for a list of names.'''

		return raw_input("\nEnter a list of comma-separated, high school names. If needed, see school_directory.csv for reference: ")


	def validate_names(self,input):

		'''Takes a string containing a list of school names and makes sure that these schools are in the directory.'''

		if input.strip().lower() == 'quit':
			sys.exit()

		else:

			#Split the input string into a list of strings on the comma indices
			names = [name.strip() for name in input.split(",")]

			passed = []
			failed = []

			for name in names:
		
				try:
					passed.append(School(self.school_database, self.school_names,name))
		
				#Cannot construct a school object if the provided name is not in the global list school_names
				except InvalidSchoolNameError:
					failed.append(name)

			return [passed, failed]

	@staticmethod
	def prompt_to_ignore_invalid_names():

		return raw_input('''\nWould you like to generate reports for the schools that were in our directory? \nType 'yes' to proceed. Press any other key to enter another list of schools: ''')

	@staticmethod
	def ignore_invalid_names(input):

		if input.strip().lower() == 'quit':
			sys.exit()
		elif input.strip().lower() == "yes":
			return True
		else:
			return False



	def get_schools_by_name(self):
		'''Recursively asks the user to provide a list of names. If there are invalid names in the list, 
		the user has the option to re-enter the list or continue with the valid ones in the provided list.'''

		passed, failed = self.validate_names(self.prompt_for_names())

		#If at least one of the comma-separated substrings does not match a school name, or if the user simply presses enter at the prompt.
		if len(failed) > 0:
			
			if len(passed) == 0:
				print "\nNone of the schools you have provided are in our directory."
				return self.get_schools_by_name()

			else:

				print "\nThe following schools are not available in our directory: \n", 
				for school in failed:
					print school+"\n",

				#Give the user the option to continue if there are some valid names in the list. 			
				return list(set(passed)) if self.ignore_invalid_names(self.prompt_to_ignore_invalid_names()) == True else self.get_schools_by_name()

		else:
			#Even though the user is allowed to enter non-unique schools, we will ignore duplicates. 
			return list(set(passed))

