from utilities import *


class InvalidSchoolNameError(Exception):

	'''This exception is raised when you try to create a school object using a name that is not in the database.'''

	def __str__(self):
		return "School name not found in database."


class School(object):
	'''Each instance of the schoolReport represents all of the performance data in the database pertaining to a single school name.'''
	
	def __init__(self, name):
		'''Raises an error if name is not the name of a school in the database. Otherwise simply uses the name to later choose a row in the database dateframe.'''

		if name.lower() in school_names:
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

	def get_address(self):
		pass

	def get_SAT_scores(self):
		pass

	def get_regents_pass_rate_june(self):
		pass

	def get_regents_pass_rate_august(self):
		pass

	def ontrack_rate_2012(self):
		pass

	def graduation_rate_2012(self):
		pass

	def college_career_rate_2012(self):
		pass

	def student_satisfaction_rate_2012(self):
		pass

	def ontrack_rate_2013(self):
		pass

	def graduation_rate_2013(self):
		pass

	def college_career_rate_2013(self):
		pass

	def student_satisfaction_rate_2012(self):
		pass







