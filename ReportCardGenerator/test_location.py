from unittest import TestCase
from location import *

class Validate_Location_Test(TestCase):

	'''Test that validate_location behaves properly when geopy does not find a location or when the 
	location is not in the same city as the schools in the database.'''

	def test_no_location_found(self):
		self.assertEqual(validate_location("dsjfa9302jsd"), None)

	def test_wrong_city(self):
		self.assertEqual(validate_location("33 Deerfield Rd Whippany NJ 07981"), None)

	def test_quit(self):
		self.assertRaises(SystemExit, validate_location, 'quit')

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

class Interpret_Number_Test(TestCase):
	'''Tests the validate number function for valid and invalid inputs'''

	def test_positive_int(self):
		self.assertEqual(validate_number('1',7), 1)

	def test_upper_bound(self):
		self.assertEqual(validate_number('7',7), 7)

	def test_nonpositive_int(self):	
		self.assertEqual(validate_number('0',7), None)

	def test_positive_float(self):
		self.assertEqual(validate_number('1.2',7), None)

	def test_nonpositive_float(self):
		self.assertEqual(validate_number('-1.0',7), None)

	def test_nonnumeric_float(self):
		self.assertEqual(validate_number('abc',7), None)

	def test_outside_upper_bound(self):
		self.assertEqual(validate_number('8',7),None)

	def test_quit(self):
		self.assertRaises(SystemExit, validate_number, 'quit',7)

