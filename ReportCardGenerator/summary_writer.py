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
	def __init__(self, filename, mode, schools, user_params = []):

		if all(isinstance(school, School) for school in schools):

			#The following attributes define the report content, including attributes in the if/elif clauses below.
			self.filename = filename
			self.schools = schools
			self.mode = mode
			self.performance_params = ['Number of SAT Test Takers','SAT Critical Reading Avg', 'SAT Math Avg', 'SAT Writing Avg', 'Regents Pass Rate - June',
 			'Regents Pass Rate - August', 'Graduation Ontrack Rate - 2013', 'Graduation Rate - 2013', 'College Career Rate - 2013', 'Student Satisfaction Rate - 2013','Graduation Ontrack Rate - 2012',
 			'Graduation Rate - 2012', 'College Career Rate - 2012', 'Student Satisfaction Rate - 2012']

			#Only name mode requires no user parameters
			if len(user_params) == 0:
				if mode != 'name':
					raise InvalidSummaryWriterError

			#Only location mode requires two user parameters: the location and the radius
			elif len(user_params) == 2:
				if mode == 'location':
					self.location = user_params[0]
					self.radius = user_params[1]
				else:
					raise InvalidSummaryWriterError

			#Online top10 mode requires three user parameters: the features, the weights, and the scores
			elif len(user_params) == 3:
				if mode == 'top10':
					self.features = user_params[0]
					self.weights = user_params[1]
					self.scores = user_params[2]
				else:
					raise InvalidSummaryWriterError

			else:
				raise InvalidSummaryWriterError


			#The following define the report formatting
			self.styles = getSampleStyleSheet()
			self.small_spacer = KeepTogether(Spacer(1,0.05*inch))
			self.medium_spacer = KeepTogether(Spacer(1,0.40*inch))
			self.big_spacer = KeepTogether(Spacer(1,defaultPageSize[1]/4.0))


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
		return Paragraph("The " + str(len(self.schools)) + " schools in this report are within " + str(self.radius) + " mile(s) of " + self.location + ".", self.styles['Normal'])


	def get_schools(self):

		'''Creates a new paragraph object containing the names of the schools in the report.'''
		return Paragraph("The schools evaluated in this report are: " + ", ".join([str(school) for school in self.schools]) + ".", self.styles['Normal'])


	def get_title_page(self):

		'''Creates a template for the first page using the flowable objects: Spacer, Paragraph, PageBreak. Includes location query information in location mode.'''
		if self.mode == 'location':
			return [self.big_spacer, self.get_title(), self.get_authors(), self.medium_spacer, self.get_mode(), self.describe_location_query(), self.get_schools(), PageBreak()]
		else:
			return [self.big_spacer, self.get_title(), self.get_authors(), self.medium_spacer, self.get_mode(), self.get_schools(), PageBreak()]


	def get_top10_schools_by_rank(self):

		schools_by_rank = []
		for rank in range(len(self.schools)):
			schools_by_rank.append(Paragraph( str(rank + 1) + ". " + str(self.schools[rank]) + " (" + str(self.scores[rank]) + ")", self.styles['Heading4']))

		return schools_by_rank


	def get_top10_ranking_system(self):
		
		ranking_system = [Paragraph('The features used to generate this ranking system and the weight assigned to each feature: ', self.styles['Heading3'])
		features_and_weights = ""
		for curr_feature in range(len(self.features)):
			string += (self.features[curr_feature] + " (" + str(self.weights[curr_feature]) + "); "
		ranking_system.append(Paragraph(features_and_weights, self.styles['Normal']))
		return ranking_system


	def get_top10_page(self):

		'''In top10 mode, this page appears immediately after the title page and lists the top 10 schools and their scores in order,
		as well as the evaluation system that generated the list.'''

		top10_page = [Paragraph('Top 10 Schools by Custom Rank: ', self.styles['Heading3'])]
		top10_page.extend(get_top10_school_by_rank())
		top10_page.append(self.medium_spacer)
		top10_page.append(self.get_top10_ranking_system())
		top10_page.append(PageBreak())
		return top10_page


	def get_basic_info(self,school):

		'''Returns a list of paragraph objects containing the school name, address, and a small spacer'''

		basic_info = [Paragraph(str(school), self.styles['Heading3'])] 
		basic_info.append(Paragraph('Address: ' + school.get_column_value('address') + ", " + school.get_column_value('city') + ", NY", self.styles['Normal']))
		basic_info.append(self.small_spacer)
		return basic_info


	def add_section_heading(self, metric):

		'''Creates section headings for each section of data.'''

		if metric == 'Number of SAT Test Takers':
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

		if 'Number' in metric or 'SAT' in metric: 

			#If the metric name contains the substring "Number" or "SAT", print it without a decimal value
			return Paragraph(metric + ': ' + str(int(value)), self.styles['Normal'])


		elif 'Regents' in metric:
			#This is a rate so print it with a percent sign
			return Paragraph(metric + ': ' + str(value) + '%', self.styles['Normal'])

		#This is metric necessarily contains information in one of the Graduation Results sections
		else:
			#Strip '- 2012' or "- 2013" from the metric name. Besides student satisfaction rate (scale to 10), they are percents.
			if '2012' in metric:
				if 'Student Satisfaction' in metric:
					return Paragraph(metric.replace('- 2012', '') + ': ' + str(value) + " out of 10.", self.styles['Normal'])
				else:
					return Paragraph(metric.replace('- 2012', '') + ': ' + str(value) + '%', self.styles['Normal'])
			else:
				if 'Student Satisfaction' in metric:
					return Paragraph(metric.replace('- 2013', '' ) + ': ' + str(value) + " out of 10.", self.styles['Normal'])
				else:
					return Paragraph(metric.replace('- 2013', '' ) + ': ' + str(value) + '%', self.styles['Normal'])


	def add_section_spacer(self, metric):

		if metric in ['SAT Writing Avg', 'Regents Pass Rate - August', 'Student Satisfaction Rate - 2013']:
			return self.small_spacer
		else:
			return None


	def get_school_summary(self, school):

		'''Returns a list of Paragraph objects summarizing basic school information.'''

 		#Summary is a list of paragraph objects containing the school name and address, 
		summary = self.get_basic_info(school)

		for metric in self.performance_params:

			value = school.get_column_value(metric)

			#Avoid printing NaN values
			if not np.isnan(value):

				#Add a heading if necessary. section_heading is None if the current metric is not intended to have a heading before it
				section_heading = self.add_section_heading(metric)
				if section_heading:
					summary.append(section_heading)

				#Add the actual metric values, formatted as necessary
				summary.append(self.get_formatted_values(metric, value))

				#At the end of every section, add a small space. section_spacer is None if the current metric is not the end of a section
				section_spacer = self.add_section_spacer(metric)
				if section_spacer:
					summary.append(section_spacer)

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
			elements.extend(self.get_top10_page())

		elements.extend(self.get_summaries())
		doc = SimpleDocTemplate(self.filename)
		doc.build(elements) 


#from location import *
#mode = 'location'
#schools, params = get_schools_by_location()
#test_schools = [School('Henry Street School for International Studies'), School('University Neighborhood High School'), School('East Side Community School')]
#writer = SummaryWriter('test.pdf', 'name', test_schools)
#writer = SummaryWriter('test.pdf', mode, schools, params)
#writer.write_report()



