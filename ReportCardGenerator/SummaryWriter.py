class InvalidSummaryWriter(Exception):

	'''This exception is raised if you try to create an instance of a SummaryWriter without passing it a list of School objects and a valid outbuf.'''

	pass

class SummaryWriter(object):

	'''Each instance of this object will create a single PDF file that contains aggregated summary statistics for all schools in the attribute list schools.'''
	def __init__(self, outbuf, schools):
		#check the type of everything

	def write_report(self):
		pass 
		#Name, address, and city
		#SAT Results
		#Figure out what math/ela apm instance
		#2013 Results: ontrack, graduation, college, student satisfaction