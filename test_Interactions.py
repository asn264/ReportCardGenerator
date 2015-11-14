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

class Interpret_Location_Test(TestCase):

	#Need to write function and understand GeoPy behavior first
	pass

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

