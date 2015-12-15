'''
Authors: Aditi Nair (asn264) and Akash Shah (ass502)

These tests are intended to ensure that the program only accepts valid features in top10 mode. 
'''

from unittest import TestCase

from top10_toolkit import *
from utilities import *

#load the cleaned database, the school names, and the valid features
school_database,school_names,valid_features = load_session()
top10_mode = Top10_Toolkit(school_database,school_names,valid_features)

class Validate_Feature_Test(TestCase):

	'''Test that validate_feature behaves as expected'''

	def test_invalid_input(self):
		self.assertEqual(top10_mode.validate_feature("abc",[]), None)
		self.assertEqual(top10_mode.validate_feature("Graduation Rate - 2013,50,abc",[]), None)

	def test_valid_input(self):
		feature = "Graduation Rate - 2013"
		weight = 10

		self.assertEqual(top10_mode.validate_feature(feature+","+str(weight),[]),[feature,weight])

	def test_invalid_feature(self):
		self.assertEqual(top10_mode.validate_feature("abc,1",[]), None)
		self.assertEqual(top10_mode.validate_feature("Graduation Rate - 2013,1",["Graduation Rate - 2013"]), None)

	def test_invalid_weight(self):
		self.assertEqual(top10_mode.validate_feature("Graduation Rate - 2013,abc",[]), None)
		self.assertEqual(top10_mode.validate_feature("Graduation Rate - 2013,-5",[]), None)
		self.assertEqual(top10_mode.validate_feature("Graduation Rate - 2013,4.7",[]), None)
		self.assertEqual(top10_mode.validate_feature("Graduation Rate - 2013,105",[]), None)

	def test_invalid_finish(self):
		self.assertEqual(top10_mode.validate_feature("finish",[]), None)

	def test_valid_finish(self):
		self.assertEqual(top10_mode.validate_feature("finish",["Graduation Rate - 2013"]), -1)

	def test_quit(self):
		self.assertRaises(SystemExit, top10_mode.validate_feature, "quit",[])