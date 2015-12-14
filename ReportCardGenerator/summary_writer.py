'''
Author: Aditi Nair (asn264) and Akash Shah (ass502)
Date: December 4th 2015

The SummaryWriter object uses the open-source ReportLab package (http://www.reportlab.com/) to generate summary reports in PDF format. 
It mainly uses the Paragraph, Spacer, and PageBreak objects to format the file neatly. It relies on the GraphGenerator object to create
visualizations of the data. It uses representations of individual schools as School objects to query their information from the school_database.
The report first contains text summaries of school performance metrics and then it displays the visualizations from GraphGenerator. Each report
is essentially a large list of ReportLab objects which are then passed to ReportLab's 'build' function.
'''

#import necessary libraries
import math
import numpy as np

#import ReportLab libraries
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER

#import classes/modules
from school import *
from graph_generator import *


class SummaryWriter(object):

	'''Each instance of this object creates a single PDF file that contains general performance metrics for all schools in the list self.schools,
	as well as graphs and boxplots using Matplotlib functionality. The PDFs are generated using ReportLab, relying on the Paragraph, Spacer, 
	and PageBreak flowables.'''

	def __init__(self, school_database, valid_features, filename, mode, schools, user_params = []):

		#The following attributes define the report content, including attributes defined in the try/except and if/elif clauses below.
		self.filename = filename
		self.schools = schools
		self.mode = mode
		self.performance_params = valid_features
 			
 		#Create a GraphGenerator object which produces visualizations of the data using matplotlib. 
 		try:
 			self.graph_generator = GraphGenerator(school_database,self.schools, defaultPageSize)
 			self.enable_visualizations = True
 		#This is raised when len(self.schools) is 1. We chose not to provide visualizations in this case.
 		except InvalidComparisonError:
 			self.enable_visualizations = False


 		#if there are less than 5 schools in the database, then distribution plots aren't displayed as there isn't enough data
 		if len(schools) < 5:
 			self.add_distribution_plots = False
 		else: 
 			self.add_distribution_plots = True


		#Here the mode is necessarily location. It requires two user parameters: the location and the radius.
		if len(user_params) == 2:
			self.location = user_params[0]
			self.radius = user_params[1]


		#Here the mode is necessarily top10. It requires three user parameters: the features, the weights, and the scores.
		elif len(user_params) == 3:
			self.features = user_params[0]
			self.weights = user_params[1]
			self.scores = user_params[2]


		#The following attributes are objects from ReportLab that help define the formatting of the PDF report.
		self.styles = getSampleStyleSheet()
		self.small_spacer = KeepTogether(Spacer(1,0.05*inch))
		self.medium_spacer = KeepTogether(Spacer(1,0.40*inch))
		self.big_spacer = KeepTogether(Spacer(1,defaultPageSize[1]/4.0))


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


	def get_visualization_warning(self):

		'''Creates a warning paragraph if only one school is used to generate the report.'''

		return Paragraph("Note: No visualizations were generated because only one school was used to create the report.",self.styles['Normal'])


	def get_distribution_plot_warning(self):
		'''Creates a warning paragraph if less than 5 schools are used to generate the report.'''

		if self.add_distribution_plots:
			return Paragraph("Note: Boxplots are not provided when the corresponding data is sparse. Some standard boxplots may be omitted.", self.styles['Normal'])
		else:
			return Paragraph("Note: No boxplots/histograms were generated because only " + str(len(self.schools)) + " schools were used to create the report.\nAt least 5 schools are needed to generate valuable visualizations showing the distribution of the data.",self.styles['Normal'])

	def get_title_page(self):

		'''Creates a template for the first page using the flowable objects: Spacer, Paragraph, PageBreak. Includes location query information in location mode.'''
		
		title_page = [self.big_spacer, self.get_title(), self.get_authors(), self.medium_spacer, self.get_mode()]

		if self.mode == 'location':
			title_page.append(self.describe_location_query())
		
		title_page.extend([self.get_schools(), self.medium_spacer])
		
		#If there are visualizations, we should say the appropriate boxplot warning W.R.T to the number of schools in the report and nothing else. 
		if self.enable_visualizations:
			#Add a boxplot warning for either no distribution plot or limited distribution plots and a pageBreak
			title_page.extend([self.get_distribution_plot_warning(), PageBreak()])
		
		#If there are no visualizations, we should only say that there are no visualizations and nothing else
		else:
			title_page.extend([self.get_visualization_warning(), PageBreak()])

		return title_page

	def get_top10_schools_by_rank(self):


		'''In top 10 mode, returns 10 Paragraph objects containing the top 10 schools and their scores, in order.'''

		schools_by_rank = []
		for rank in range(len(self.schools)):
			schools_by_rank.append(Paragraph( str(rank + 1) + ". " + str(self.schools[rank]) + " (" + '%.2f'%self.scores[rank] + ")", self.styles['Heading4']))

		return schools_by_rank


	def get_top10_ranking_system(self):

		'''In top 10 mode, returns two Paragraph objects describing the user-generated ranking system.'''
		
		ranking_system = [Paragraph('The features used to generate this ranking system and the weight assigned to each feature: ', self.styles['Heading4'])]
		features_and_weights = ""
		for curr_feature in range(len(self.features)):
			features_and_weights += (self.features[curr_feature] + " (" + str(self.weights[curr_feature]) + ")")
			if curr_feature == len(self.features)-1:
				features_and_weights += "."
			else:
				features_and_weights += ", "
		ranking_system.append(Paragraph(features_and_weights, self.styles['Normal']))
		return ranking_system


	def describe_top10_calculation(self):

		'''Returns a Paragraph describing the ranking algorithm.'''

		return Paragraph('''These scores were generated by normalizing the available data and 
			taking the weighted average with respect to the features and weights provided by the user.''', self.styles['Normal'])


	def get_top10_page(self):

		'''In top10 mode, this page appears immediately after the title page and lists the top 10 schools and their scores in order,
		as well as the evaluation system that generated the list.'''

		top10_page = [Paragraph('Top 10 Schools and Scores by Custom Rank: ', self.styles['Heading3'])]
		top10_page.extend(self.get_top10_schools_by_rank())
		top10_page.append(self.medium_spacer)
		top10_page.append(self.describe_top10_calculation())
		top10_page.extend(self.get_top10_ranking_system())
		top10_page.append(PageBreak())
		return top10_page


	def get_basic_info(self, school, rank):

		'''Returns a list of paragraph objects containing the school name, address, and a small spacer. Includes rank in top10 mode.
		This is a part of each school summary'''

		#Rank is only not None in top10 mode.
		if rank:
			basic_info= [Paragraph(str(rank) + ". " + str(school), self.styles['Heading3'])]

		#rank is None in location mode and names mode.
		else:
			basic_info = [Paragraph(str(school), self.styles['Heading3'])] 
		
		basic_info.append(Paragraph('Address: ' + school.get_column_value('address') + ", " + school.get_column_value('city') + ", NY", self.styles['Normal']))
		basic_info.append(self.small_spacer)
		return basic_info


	def add_section_heading(self, metric):

		'''Creates section headings before each section of data. There are four of these in each school summary.'''

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

		'''For each school summary, this helps print out the metrics in a nicer format.'''

		#If the metric name contains the substring "Number" or "SAT", print it without a decimal value
		if 'Number' in metric or 'SAT' in metric: 
			return Paragraph(metric + ': ' + str(int(value)), self.styles['Normal'])

		#This is a rate so print it with a percent sign
		elif 'Regents' in metric:
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

		'''In each school description, at the end of each section, there should be a space.'''

		if metric in ['SAT Writing Avg', 'Regents Pass Rate - August', 'Student Satisfaction Rate - 2013']:
			return self.small_spacer
		else:
			return None


	def get_school_summary(self, school, rank=None):

		'''Returns a list of Paragraph objects summarizing basic information for a single school. In top10 mode, rank reflects the ranking of the school.'''

 		#Summary is now a list of paragraph objects containing the school name and address.
		summary = self.get_basic_info(school, rank)

		#Loop through each metric that is available in our database
		for metric in self.performance_params:

			#Read the column value for the current school from the database
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

		'''A list of summaries, one for each school. Each item in summaries is itself a list of Paragraph objects, 
		containing headings and spacing as necessary.'''

		summaries = []
		for index, school in enumerate(self.schools):
			if self.mode == 'top10':
				summaries.extend(self.get_school_summary(school,index+1))
			else:
				summaries.extend(self.get_school_summary(school))
		summaries.append(PageBreak())
		return summaries 


	def write_report(self):

		'''Writes the report by appending Paragraph, Spacer, and PageBreak objects as necessary.'''

		#Gets the ReportLab objects necessary for writing the title page
		elements = self.get_title_page()

		#Creates a page that lists the Top 10 schools, their scores, and the user-genereated metric.
		if self.mode == 'top10':
			elements.extend(self.get_top10_page())

		#Add the individual summaries from each school.
		elements.extend(self.get_summaries())

		#If there is more than one school in self.schools, add bar plots using graph generator object
		if self.enable_visualizations:
			elements.extend([Image(png_file) for png_file in self.graph_generator.get_bar_plots()])

		#If there are at least five schools in self.schools, add distribution plots using the graph generator object
		if self.add_distribution_plots:
			elements.extend([Image(png_file) for png_file in self.graph_generator.get_distribution_plots()])

		#Create and save the file.
		doc = SimpleDocTemplate(self.filename)
		doc.build(elements) 


