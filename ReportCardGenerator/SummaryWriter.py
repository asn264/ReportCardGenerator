'''
Author: Aditi Nair
Date: December 4th 2015
'''

from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
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


	def get_title(self):
		return Paragraph("NYC Public High School Performance Report", self.styles["Heading1"])

	
	def get_authors(self):
		return Paragraph("Authors: Aditi Nair (asn264@nyu.edu) and Akash Shah (ass502@nyu.edu)", self.styles['Normal'])


	#Go back and add different things for Location Mode and Top 10 Mode if possible
	def get_mode(self):
		return Paragraph("This report was generated in " + self.mode.title() + " mode.", self.styles['Normal'])


	def get_schools(self):
		comma = ", "
		return Paragraph("The schools evaluated in this report are: " + comma.join([str(school) for school in self.schools]) + ".", self.styles['Normal'])


	def get_school_summary():
		pass

	def get_summaries(self):

		#A list of summaries for each school. Each item in summaries is itself a list of Paragraph objects. 
		summaries = []
		for school in self.schools:
			#for each attribute that we want to describe create a new paragraph object and append it to summaries
			#after each school, add two line breaks or spacers
			pass 

		return summaries
		#return Paragraph("aklsdjf;alkjsd;flkajsd;kfja <br/> aksfjda;klsjd", self.styles['Normal'])

	def write_report(self):

		#Eventually write it so that Elements is evenutally populated and then written two

		PAGE_HEIGHT=defaultPageSize[1]
		s = Spacer(1,PAGE_HEIGHT/4.0)
		Elements = [Spacer(1,PAGE_HEIGHT/4.0), self.get_title(), self.get_authors(), Spacer(1,0.25*inch), self.get_mode(), self.get_schools(), PageBreak(), self.get_summaries()]
		doc = SimpleDocTemplate(self.filename)
		doc.build(Elements) 


test_schools = [School('Henry Street School for International Studies'), School('University Neighborhood High School'), School('East Side Community School')]
writer = SummaryWriter('test.pdf', 'name', test_schools)
writer.write_report()


