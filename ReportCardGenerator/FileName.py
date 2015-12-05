'''
Author: Aditi Nair (asn264)
Date: December 5 2015
'''

import sys
import os.path

def prompt_for_filename():

	'''Asks the user to choose a filename.'''
	return raw_input("Please enter a filename for your report. Entering \"report\" will generate the file \"report.pdf\".")

def get_filename():

	'''Asks the user to enter a filename. If the file exists, warns the user and forces them to choose another filename.'''
	user_input = prompt_for_filename()

	if os.path.exists(user_input):
		print "This file already exists in the current directory. Please enter another filename."
		return get_filename()
		
	else:
		return user_input
