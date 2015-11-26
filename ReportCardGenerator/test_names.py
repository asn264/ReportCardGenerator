from unittest import TestCase
from names import *

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
