from unittest import TestCase
from filename import *

class Validate_Filename_Test(TestCase):

	#Want to ensure that the function recognizes existing files
	def test_rejects_existing(self):
		self.assertTrue(check_filename_exists('ReportCards.py'))

	#This text will only fail if someone goes and manually creates a file with the following name. 
	def test_accepts_new(self):
		self.assertFalse(check_filename_exists('alsdkjfa.txt'))