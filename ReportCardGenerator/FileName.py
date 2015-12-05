'''
Author: Aditi Nair (asn264)
Date: December 5 2015
'''

import sys
import os.path

def prompt_for_filename():

	'''Asks the user to choose a filename. Concatenates ".pdf" and returns the string.'''
	return raw_input("Please enter a filename for your report. Entering \"report\" will generate the file \"report.pdf\".")+ ".pdf"

def check_filename_exists(user_input):

	'''Returns true if user_input already exists in the directory.  Otherwise returns false.'''

	return os.path.exists(user_input)

def get_filename(user_input):

	'''Takes a filename - usually user input. If the file exists, warns the user and forces them to choose another filename.'''

	if check_filename_exists(user_input):
		print "This file already exists in the current directory. Please enter another filename."
		return get_filename()
		
	else:
		return user_input

print check_filename_exists(prompt_for_filename())
