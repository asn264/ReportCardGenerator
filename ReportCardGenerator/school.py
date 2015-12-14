'''
Authors: Aditi Nair (asn264) and Akash Shah (ass502)

Contains the school class. Each instance of the class represents one school in our school database.
There is a corresponding custom exception InvalidSchoolNameError for schools that are not in the database. 
'''


class InvalidSchoolNameError(Exception):

	'''This exception is raised when you try to create a school object using a name that is not in the database.'''

	def __str__(self):
		return "School name not found in database."


class School(object):
	'''Each instance of the School object represents a single school identified uniquely by name. 
	It provides the functionality to access all of the available performance data for that school.'''
	
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
		'''Two School objects with the same name attribute are equivalent.'''

		if isinstance(other, self.__class__):
			return self.name == other.name
		else:
			return False

	#Looks in school_database in the column called column_name for the school with the name in self.name and returns the value
	def get_column_value(self, column_name): 
		return self.school_database[self.school_database['school_name'].str.lower()==self.name.lower()][column_name].values[0]







