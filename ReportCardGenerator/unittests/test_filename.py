'''
Authors: Aditi Nair (asn264) and Akash Shah (ass502)

This class tests the functionality of the filename module. 
It mainly ensures that existing files in the reports directory are recognized by the program, 
and that the program only validates user input meeting our requirements.
'''

from unittest import TestCase
from filename import *

class Existing_Filename_Test(TestCase):

	#Want to ensure that the function recognizes existing files
	def test_rejects_existing(self):
		self.assertTrue(check_filename_exists('report_cards.py'))

	#This text will only fail if someone goes and manually creates a file with the following name. 
	def test_accepts_new(self):
		self.assertFalse(check_filename_exists('alsdkjfa.txt'))

class Legal_Filename_Test(TestCase):

	#Check an illegal filename prefix
	def test_illegal(self):
		self.assertFalse(check_legal_filename('@#$'))

	#This file name prefix is obviously legal 
	def test_legal(self):
		self.assertTrue(check_legal_filename('legal09'))

	#Check a filename with underscores
	def test_legal_underscores(self):
		self.assertTrue(check_legal_filename('legal_09'))

	#This file name prefix is legal but an edgecase in the implementation
	def test_legal_underscore_endpoints(self):
		self.assertTrue(check_legal_filename('_legal_09_'))