'''
Author: Aditi Nair
Date: December 4th 2015
'''

import math
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from school import *


class InvalidSummaryWriterError(Exception):

	'''This exception is raised if you try to create an instance of a SummaryWriter without passing it a list of School objects and a valid outbuf.'''
	pass


class SummaryWriter(object):

	'''Each instance of this object will create a single PDF file that contains aggregated summary statistics for all schools in the attribute list schools.'''
	def __init__(self, filename, mode, schools, first_user_param = None, second_user_param = None, third_user_param = None):

		if all(isinstance(school, School) for school in schools):

			#the following define the report content
			self.filename = filename
			self.schools = schools
			self.mode = mode

			if first_user_param and second_user_param:
				
				#Location mode requires exactly two user parameters - the location and the radius
				if mode == 'location':

					if not third_user_param:
						self.location = first_user_param
						self.radius = second_user_param

					else:
						raise InvalidSummaryWriterError

				#Top 10 mode requires exactly three user parameters - the features, the weights, and the scores
				elif mode == 'top10':

					if third_user_param:
						self.features = first_user_param
						self.weights = second_user_param
						self.scores = third_user_param

					else:
						raise InvalidSummaryWriterError

				#First_user_param and second_user_param should only be defined when mode is 'location' or 'top10', not 'name' mode
				else:
					raise InvalidSummaryWriterError


			#the following define the report formatting
			self.styles = getSampleStyleSheet()
			self.small_spacer = Spacer(1,0.05*inch)
			self.medium_spacer = Spacer(1,0.25*inch)
			self.big_spacer = Spacer(1,defaultPageSize[1]/4.0)

		#Raise an error if all of the items in schools are not School objects
		else:
			raise InvalidSummaryWriterError



	def get_title(self):

		'''Returns a new paragraph object containing the report titles'''

		return Paragraph("NYC Public High School Performance Report", self.styles["Heading1"])


	
	def get_authors(self):

		'''Returns a new paragraph object containing the author names.'''
		return Paragraph("Authors: Aditi Nair (asn264@nyu.edu) and Akash Shah (ass502@nyu.edu)", self.styles['Normal'])


	def get_mode(self):

		'''Creates a new paragraph object presenting the mode.'''
		return Paragraph("This report was generated in " + self.mode.title() + " mode.", self.styles['Normal'])


	def describe_location_query(self):

		'''In location mode, creates a new paragraph object representing the location query.'''
		pass


	def get_schools(self):

		'''creates a new paragraph object containing the names of the schools in the report.'''
		return Paragraph("The schools evaluated in this report are: " + ", ".join([str(school) for school in self.schools]) + ".", self.styles['Normal'])


	def get_title_page(self):

		'''Creates a template for the first page using the flowable objects: Spacer, Paragraph, PageBreak. Includes location query information in location mode.'''
		if self.mode == 'location':
			return [self.big_spacer, self.get_title(), self.get_authors(), self.medium_spacer, self.get_mode(), self.describe_location_query(), self.get_schools(), PageBreak()]
		else:
			return [self.big_spacer, self.get_title(), self.get_authors(), self.medium_spacer, self.get_mode(), self.get_schools(), PageBreak()]


	def get_basic_info(self,school):

		'''Returns a list of paragraph objects containing the school name, address, and a small spacer'''

		basic_info = [Paragraph(str(school), self.styles['Heading3'])] 
		basic_info.append(Paragraph('Address: ' + school.get_column_value('address') + ", " + school.get_column_value('city') + ", NY", self.styles['Normal']))
		basic_info.append(self.small_spacer)
		return basic_info


	def add_section_heading(self, metric):

		'''Creates section headings for each section of data.'''

		if metric == 'Num of SAT Test Takers':
			return Paragraph('SAT Results:', self.styles['Heading4'])

		elif metric == 'Regents Pass Rate - June':
			return Paragraph('Regents Results:', self.styles['Heading4'])

		elif metric == 'Graduation Ontrack Rate - 2013':
			return Paragraph('2013 Graduation Results:', self.styles['Heading4'])

		elif metric == 'Graduation Ontrack Rate - 2012':
			return Paragraph('2012 Graduation Results:', self.styles['Heading4'])
		else:
			return None


def get_formatted_values(self, metric, value):

	if 'Num' in metric or 'SAT' in metric: 

		#If the metric name contains the substring "Num" or "SAT", print it without a decimal value
		summary.append(Paragraph(metric + ': ' + str(int(value)), self.styles['Normal']))


		else:

			if 'Regents' in metric:
				#This is a rate so print it with a percent sign
				summary.append(Paragraph(metric + ': ' + str(value) + '%', self.styles['Normal']))

			#This is metric contains information in one of the Graduation Results sections
			else:
				#Strip '- 2012' or "- 2013" from the metric name. These are all rates so print them with a percent sign.
				if '2012' in metric:
					summary.append(Paragraph(metric.replace('- 2012', '') + ': ' + str(value) + '%', self.styles['Normal']))
				else:
					summary.append(Paragraph(metric.replace('- 2013', '' ) + ': ' + str(value) + '%', self.styles['Normal']))


	def get_school_summary(self, school):

		'''Returns a list of Paragraph objects summarizing basic school information.'''

		params = ['Num of SAT Test Takers','SAT Critical Reading Avg', 'SAT Math Avg', 'SAT Writing Avg', 'Regents Pass Rate - June',
 		'Regents Pass Rate - August', 'Graduation Ontrack Rate - 2013', 'Graduation Rate - 2013', 'College Career Rate - 2013', 'Student Satisfaction Rate - 2013','Graduation Ontrack Rate - 2012',
 		'Graduation Rate - 2012', 'College Career Rate - 2012', 'Student Satisfaction Rate - 2012']

 		#Summary is a list of paragraph objects containing the school name and address, 
		summary = self.get_basic_info(school)

		for metric in params:

			value = school.get_column_value(metric)

			#Avoid printing NaN values
			if not np.isnan(value):

				#Add a heading if necessary. section_heading is None if the current metric is not intended to have a heading before it
				section_heading = self.add_section_heading(metric)
				if section_heading:
					summary.append(section_heading)

				#Add the actual metric values, formatted as necessary
				summary.append(self.get_formatted_values(metric))

				'''
				#Now handle the formatting of the actual metric values
				if 'Num' in metric or 'SAT' in metric: 

					#If the metric name contains the substring "Num" or "SAT", print it without a decimal value
					summary.append(Paragraph(metric + ': ' + str(int(value)), self.styles['Normal']))


				else:

					if 'Regents' in metric:
						#This is a rate so print it with a percent sign
						summary.append(Paragraph(metric + ': ' + str(value) + '%', self.styles['Normal']))

					#This is metric contains information in one of the Graduation Results sections
					else:
						#Strip '- 2012' or "- 2013" from the metric name. These are all rates so print them with a percent sign.
						if '2012' in metric:
							summary.append(Paragraph(metric.replace('- 2012', '') + ': ' + str(value) + '%', self.styles['Normal']))
						else:
							summary.append(Paragraph(metric.replace('- 2013', '' ) + ': ' + str(value) + '%', self.styles['Normal']))

				'''

				#At the end of every section, add a small space
				if metric in ['SAT Writing Avg', 'Regents Pass Rate - August', 'Student Satisfaction Rate - 2013']:
					summary.append(self.small_spacer)

		#At the end of the summary, add a space to separate from the next school's summary
		summary.append(self.medium_spacer)

		return summary 


	def get_summaries(self):

		#A list of summaries for each school. Each item in summaries is itself a list of Paragraph objects. 
		summaries = []
		for school in self.schools:
			summaries.extend(self.get_school_summary(school))
		return summaries 


	def write_report(self):

		elements = self.get_title_page()

		if self.mode == 'top10':
			#elements.extend(self.get_top10_page())
			pass

		elements.extend(self.get_summaries())
		doc = SimpleDocTemplate(self.filename)
		doc.build(elements) 



test_schools = [School('Henry Street School for International Studies'), School('University Neighborhood High School'), School('East Side Community School')]
writer = SummaryWriter('test.pdf', 'name', test_schools)
writer.write_report()




