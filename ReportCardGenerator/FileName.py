'''
Author: Aditi Nair (asn264)
Date: December 5 2015
'''

import sys
import os.path

def prompt_for_filename():

	'''Asks the user to choose a filename.'''
	return raw_input("Please enter a filename for your report using only alphanumeric characters and/or underscores. Entering \"report\" will generate the file \"report.pdf\".")


def check_filename_exists(user_input):

	'''Returns true if user_input already exists in the directory.  Otherwise returns false.'''

	return os.path.exists(user_input)


def check_legal_filename(user_input):

	'''Ensures that filenames are safe. Conservatively, we will force the user to only use filenames that have alphanumeric characters and underscores.'''
	
	#If the string is fully alphanumeric, return True - it *is* legal.
	if user_input.isalnum():
		return True

	#If there are characters besides alphanumeric characters, we will only allow underscores.
	else:

		#Check if the first element is an underscore. If so ignore it below.
		if user_input[0] == "_":
			user_input = user_input[1:]

		#Check if the last element is an underscore. If so ignore it below.
		if user_input[-1] == "_":
			user_input = user_input[0:-1]

		#Try splitting by "_" and seeing if the substrings are alphanumeric. Return True if all of the substrings are alphanumeric.
		return all([substring.isalnum() for substring in user_input.split("_")])


def get_filename():

	'''Takes user input for a filename. If the file exists, warns the user and forces them to choose another filename. Only allows legal filenames.
	Returns passing filenames with .pdf concatenated.'''

	user_input = prompt_for_filename()

	if user_input == "quit":
		sys.exit()

	else:
		#At this point, we have not concatenated ".pdf" to user_input. We check that the prefix is legal.
		if not check_legal_filename(user_input):
			print "Illegal filename: enter a string containing only alphanumeric characters and/or underscores."
			return get_filename()

		#In order to check whether the file exists, we need to concatenate .pdf
		user_input = user_input + ".pdf"
		if check_filename_exists(user_input): 
			print "This file already exists in the current directory. Please enter another filename."
			return get_filename()

		return user_input


