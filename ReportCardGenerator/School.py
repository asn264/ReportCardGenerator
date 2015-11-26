import pandas as pd

database = pd.read_csv('database.csv')

class InvalidSchoolNameError(Exception):

	'''This exception is raised when you try to create a school object using a name that is not in the database.'''

	def __str__(self):
		return "School name not found in database."

class School(object):
	'''Each instance of the schoolReport represents all of the performance data in the database pertaining to a single school name.'''
	
	def __init__(self, name):
	'''Raises an error if name is not the name of a school in the database. Otherwise simply uses the name to later choose a row in the database dateframe.'''
		if name in pd.unique(school_database['school_name'].values.ravel()):
				self.name = name
		else:
			raise InvalidSchoolNameError


class AggregateReportWriter(object):
	'''Each instance of this object will create a single PDF file that contains aggregated summary statistics for all schools in the attribute list schools.'''
	def __init__(self, outbuf, schools):
		pass

	def write_report(self):
		pass 
		#Name, address, and city
		#SAT Results
		#Figure out what math/ela apm instance
		#2013 Results: ontrack, graduation, college, student satisfaction



class InvalidComparisonReportWriter(Exception):

	'''This exception is raised when you try to create a school object using a name that is not in the database.'''

	def __str__(self):
		return "Cannot compare a school to itself!"

class ComparisonReportWriter(object):
	'''Each instance of this object will create a single PDF file that contains aggregated summary statistics for all schools in the attribute list schools.'''
	def __init__(self, outbuf, schools):
		if len(schools) > 1:
			self.schools = schools
		else:
			raise InvalidComparisonReportWriter

	def write_report(self):
		pass

