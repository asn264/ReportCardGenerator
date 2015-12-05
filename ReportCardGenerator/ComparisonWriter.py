from utilities import *
from School import *

class InvalidComparisonWriter(Exception):

	'''This exception is raised when you try to do a comparison report for only one school'''

	def __str__(self):
		return "Cannot compare a school to itself!"

class ComparisonWriter(object):
	'''Each instance of this object will create a single PDF file that contains aggregated summary statistics for all schools in the attribute list schools.'''

	def __init__(self, mode, schools):
		if len(schools) > 1:
			self.schools = schools
		else:
			raise InvalidComparisonWriter

	def write_report(self):
		pass

	def sat_boxplots(self):
		for school in schools:
			
