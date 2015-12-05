'''
Author: Aditi Nair
Date: December 4th 2015
'''

from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

class InvalidSummaryWriterError(Exception):

	'''This exception is raised if you try to create an instance of a SummaryWriter without passing it a list of School objects and a valid outbuf.'''

	pass

class SummaryWriter(object):

	'''Each instance of this object will create a single PDF file that contains aggregated summary statistics for all schools in the attribute list schools.'''
	def __init__(self, mode, schools):
		if all(isinstance(school, School) for school in schools):
			self.schools = schools
			self.mode = mode

		else:
			raise InvalidSummaryWriterError
			
	#Consider making a static method
	def format(self):
		PAGE_HEIGHT=defaultPageSize[1]
		styles = getSampleStyleSheet()

	#Consider making a static method
	def Title(self):
		return Paragraph("NYC Public High School Performance Report")

	#Consider making a static method
	def Authors(self):
		return Paragraph("Aditi Nair (asn264) and Akash Shah (ass502)")

	def Mode(self):
		#Go back and add different things for Location Mode and Top 10 Mode if possible
		return Paragraph(self.mode.upper() + "Mode")

	def Schools(self):
		comma = ", "
		return Paragraph("The schools evaluated in this report are " + comma.join([str(school) for school in self.schools]))


	def write_report(self):
		self.format()
		Elements = [self.Title(), self.Authors(), self.Mode(), self.Schools()]
		doc = SimpleDocTemplate('idk.pdf')
		doc.build(Elements) 
		#Name, address, and city
		#SAT Results
		#Figure out what math/ela apm instance
		#2013 Results: ontrack, graduation, college, student satisfaction


