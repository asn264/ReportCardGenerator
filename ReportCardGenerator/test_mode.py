from unittest import TestCase
from mode import *

class Interpret_Mode_Test(TestCase):

	'''Tests interpret_mode function for valid and invalid inputs including "quit".'''

	def test_valid_mode(self):
		self.assertEqual(interpret_mode(' LoCaTion '), 'location')

	def test_invalid_mode(self):
		self.assertEqual(interpret_mode(' abc '), None)

	def test_quit(self):
		self.assertRaises(SystemExit, interpret_mode, 'quit')