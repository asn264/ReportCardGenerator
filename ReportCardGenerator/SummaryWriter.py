'''
Author: Aditi Nair
Date: December 4th 2015
'''

from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from School import *


class InvalidSummaryWriterError(Exception):

	'''This exception is raised if you try to create an instance of a SummaryWriter without passing it a list of School objects and a valid outbuf.'''

	pass


class SummaryWriter(object):

	'''Each instance of this object will create a single PDF file that contains aggregated summary statistics for all schools in the attribute list schools.'''
	def __init__(self, filename, mode, schools):
		if all(isinstance(school, School) for school in schools):
			self.filename = filename
			self.schools = schools
			self.mode = mode
			self.styles = getSampleStyleSheet()

		else:
			raise InvalidSummaryWriterError


	def Title(self):
		return Paragraph("NYC Public High School Performance Report", self.styles["Heading1"])


	#Go back and add different things for Location Mode and Top 10 Mode if possible
	def Mode(self):
		return Paragraph("Report generated in " + self.mode.title() + " mode.", self.styles['Normal'])


	def Schools(self):
		comma = ", "
		return Paragraph("The schools evaluated in this report are: " + comma.join([str(school) for school in self.schools]) + ".", self.styles['Normal'])


	#Make this a footer, then incorporate into the file
	def Authors(self):
		return Paragraph("Authors: Aditi Nair (asn264@nyu.edu) and Akash Shah (ass502@nyu.edu)", self.styles['Normal'])


	def Summaries(self):

		#A list of summaries for each school. Each item in summaries is itself a list of Paragraph objects. 
		Summaries = []
		for school in schools:
			pass 


	def write_report(self):
		PAGE_HEIGHT=defaultPageSize[1]
		Elements = [self.Title(), self.Mode(), self.Schools()]
		doc = SimpleDocTemplate(self.filename)
		doc.build(Elements) 


test_schools = [School('Henry Street School for International Studies'), School('University Neighborhood High School'), School('East Side Community School')]
writer = SummaryWriter('test', 'name', test_schools)
writer.write_report()


