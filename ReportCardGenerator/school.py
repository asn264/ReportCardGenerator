'''Author: Aditi Nair (asn264)

Contains the school class, an instance of which represents one school in our school database,
as well as the user defined exception InvalidSchoolNameError'''

from utilities import *


class InvalidSchoolNameError(Exception):

	'''This exception is raised when you try to create a school object using a name that is not in the database.'''

	def __str__(self):
		return "School name not found in database."


class School(object):
	'''Each instance of the schoolReport represents all of the performance data in the database pertaining to a single school name.'''
	
	def __init__(self, school_database, school_names, name):
		'''Raises an error if name is not the name of a school in the database. Otherwise simply uses the name to later choose a row in the database dateframe.'''

		if name.lower() in school_names:
			self.school_database = school_database
			self.name = name
		else:
			raise InvalidSchoolNameError


	def __str__(self):
		'''We can uniquely define each School object by its name.'''
		return self.name


	def __eq__(self, other):
		'''Two School objects with the same attribute are equivalent.'''

		if isinstance(other, self.__class__):
			return self.name == other.name
		else:
			return False

	def get_name(self):
		return self.name

	def get_column_value(self, column_name):
		return self.school_database[self.school_database['school_name']==self.name][column_name].values[0]







