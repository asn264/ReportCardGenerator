'''

Authors: Aditi Nair (asn264) and Akash Shah (ass502)

These tests ensure that the program validates school names correctly in names mode, and that
the program interacts with the user correctly when allowing the user to bypass invalid names. 

Because the School class's custom exception was designed to validate input at this stage, 
the tests in Validate_Names_Test also provide testing for the School class.

'''

from unittest import TestCase

from names_toolkit import *
from utilities import *

#load the cleaned database, the school names, and the valid features
school_database,school_names,valid_features = load_session()
names_mode = Names_Toolkit(school_database,school_names)

class Validate_Names_Test(TestCase):
	''' validate_names returns two lists: the first is all of the comma-separated strings provided
	the second is the ones not matched in the database. Test both lists are complete.'''

	def test_validate_names(self):
		#The output should be a list of lists. The first list is valid School objects. The second list is strings with no match in the names column of the school directory. 
		real_schools = [School(school_database, school_names,name) for name in ['University Neighborhood High School', 'East Side Community School']]
		self.assertEqual(names_mode.validate_names("University Neighborhood High School, East Side Community School, TEST, nyc"), [real_schools, ['TEST', 'nyc']])

	def test_quit(self):
		self.assertRaises(SystemExit, names_mode.validate_names, 'quit')


class Ignore_Invalid_Names_Test(TestCase):
	'''Tests the function that allows the user to proceed with a subset of the names that they 
	provided in names mode (the subset that was found in the database).'''

	def test_yes(self):
		self.assertEqual(names_mode.ignore_invalid_names('yes'), True)
	def test_no(self):
		self.assertEqual(names_mode.ignore_invalid_names('sldjf'), False)
	def test_quits(self):
		self.assertRaises(SystemExit, names_mode.ignore_invalid_names, 'quit')
