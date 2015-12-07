from unittest import TestCase
from top10 import *

class Validate_Feature_Test(TestCase):

	'''Test that validate_feature behaves as expected'''

	def test_invalid_input(self):
		self.assertEqual(validate_feature("abc",[]), None)
		self.assertEqual(validate_feature("Graduation Rate - 2013,50,abc",[]), None)

	def test_valid_input(self):
		feature = "Graduation Rate - 2013"
		weight = 10

		self.assertEqual(validate_feature(feature+","+str(weight),[]),[feature,weight])

	def test_invalid_feature(self):
		self.assertEqual(validate_feature("abc,1",[]), None)
		self.assertEqual(validate_feature("Graduation Rate - 2013,1",["Graduation Rate - 2013"]), None)

	def test_invalid_weight(self):
		self.assertEqual(validate_feature("Graduation Rate - 2013,abc",[]), None)
		self.assertEqual(validate_feature("Graduation Rate - 2013,-5",[]), None)
		self.assertEqual(validate_feature("Graduation Rate - 2013,4.7",[]), None)
		self.assertEqual(validate_feature("Graduation Rate - 2013,105",[]), None)

	def test_invalid_finish(self):
		self.assertEqual(validate_feature("finish",[]), None)

	def test_valid_finish(self):
		self.assertEqual(validate_feature("finish",["Graduation Rate - 2013"]), -1)

	def test_quit(self):
		self.assertRaises(SystemExit, validate_feature, "quit",[])