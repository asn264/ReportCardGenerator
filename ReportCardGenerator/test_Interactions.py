from unittest import TestCase
from Interactions import *

class Interpret_Mode_Test(TestCase):

	'''Tests interpret_mode function for valid and invalid inputs including "quit".'''

	def test_valid_mode(self):
		self.assertEqual(interpret_mode(' LoCaTion '), 'location')

	def test_invalid_mode(self):
		self.assertEqual(interpret_mode(' abc '), None)

	def test_quit(self):
		self.assertRaises(SystemExit, validate_radius, 'quit')

class Validate_Names_Test(TestCase):
	''' validate_names returns two lists: the first is all of the comma-separated strings provided
	the second is the ones not matched in the database. Test both lists are complete.'''

	def test_validate_names(self):
		#The output should be a list of lists. The first list is strings of the comma-separated entries. The second list is strings with no match in the names column of the school directory. 
		self.assertEqual(validate_names("Henry Street School for International Studies, University Neighborhood High School, East Side Community School, TEST, nyc"), [['Henry Street School for International Studies', 'University Neighborhood High School', 'East Side Community School', 'TEST', 'nyc'], ['TEST', 'nyc']])

	def test_quit(self):
		self.assertRaises(SystemExit, validate_names, 'quit')


class Ignore_Invalid_Names_Test(TestCase):
	'''Tests the function that allows the user to proceed with a subset of the names that they 
	provided in names mode (the subset that was found in the database).'''

	def test_yes(self):
		self.assertEqual(ignore_invalid_names('yes'), True)
	def test_no(self):
		self.assertEqual(ignore_invalid_names('sldjf'), False)
	def test_quits(self):
		self.assertRaises(SystemExit, ignore_invalid_names, 'quit')

class Validate_Location_Test(TestCase):

	'''Test that validate_location behaves properly when geopy does not find a location or when the 
	location is not in the same city as the schools in the database.'''

	def test_no_location_found(self):
		self.assertEqual(validate_location("dsjfa9302jsd"), None)

	def test_wrong_city(self):
		self.assertEqual(validate_location("33 Deerfield Rd Whippany NJ 07981"), None)

class Interpret_Radius_Test(TestCase):

	'''Tests validate_radius function for valid and invalid inputs including: positive ints and floats, 
	negative ints and floats, nonnumeric strings, and "quit".'''

	def test_positive_int(self):
		self.assertEqual(validate_radius('1'), 1)

	def test_nonpositive_int(self):	
		self.assertEqual(validate_radius('0'), None)

	def test_positive_float(self):
		self.assertEqual(validate_radius('1.2'), 1.2)

	def test_nonpositive_float(self):
		self.assertEqual(validate_radius('-1.0'), None)

	def test_nonnumeric_float(self):
		self.assertEqual(validate_radius('abc'), None)

	def test_quit(self):
		self.assertRaises(SystemExit, validate_radius, 'quit')

