'''
Authors: Aditi Nair (asn264) and Akash Shah (ass502)

This module loads the cleaned data into a dataframe and creates the list of valid features used throughout the program, 
as well as a list of the school names found in the database.
'''

#import necessary libraries
import pandas as pd
import numpy as np
import sys

def load_session():
	'''loads a dataframe containing the cleaned data, and a dataframe containing the unique school names'''

	try:
		school_database = pd.read_csv('data/database.csv')

		#Note there are no duplicates in this list. We cast it to lower-case so that we can build more flexibility in accepting user input with different capitalizations. 
		school_names = pd.unique(school_database['school_name'].str.lower().values.ravel())

		#Array containing valid features that the user can choose from to create a top 10 ranking
		valid_features = ['Number of SAT Test Takers','SAT Critical Reading Avg','SAT Math Avg', 'SAT Writing Avg', 'Regents Pass Rate - June','Regents Pass Rate - August', 'Graduation Ontrack Rate - 2013','Graduation Rate - 2013', 'College Career Rate - 2013', 'Student Satisfaction Rate - 2013','Graduation Ontrack Rate - 2012','Graduation Rate - 2012', 'College Career Rate - 2012', 'Student Satisfaction Rate - 2012']

		return school_database,school_names,valid_features

	except IOError: #catch exception if the dataframe cannot be loaded, inform user and exit the program
		print "\nCould not locate/read the file database.csv"
		sys.exit()