from utilities import *
from School import *

import matplotlib.pyplot as plt
import warnings

class InvalidComparisonWriter(Exception):

	'''This exception is raised when you try to do a comparison report for only one school'''

	def __str__(self):
		return "Cannot compare a school to itself!"

class ComparisonWriter(object):
	'''Each instance of this object will create a single PDF file that contains aggregated summary statistics for all schools in the attribute list schools.'''

	def __init__(self, mode, schools):
		if len(schools) > 1:
			self.schools = schools
			self.names =[str(school) for school in schools]
		else:
			raise InvalidComparisonWriter

	def write_report(self):
		

	def sat_boxplots(self):
		'''plots boxplots showing the distribution of SAT scores for each of the 3 sections'''
		
		data=[]
		sections = ['Math','Critical Reading','Writing']

		#append data from each section of the SAT
		for section in sections:
			section_data = school_database.loc[school_database['school_name'].isin(self.names)]['SAT '+section+' Avg']
			data.append(section_data)

		plt.figure()
		plt.boxplot(data)

		#set xticks for each section, with the section name
		plt.xticks(np.arange(1,len(sections)+1),sections)

		#set axis labels and title
		plt.xlabel('SAT Sections',fontsize=16)
		plt.ylabel('Score',fontsize=16)
		plt.title('SAT Score Distribution',fontsize=20)
		plt.show()

	def sat_test_takers_histogram(self):
		'''plots a distribution of the number of SAT test takers'''
		
		#get data for the number of test takers
		data = school_database.loc[school_database['school_name'].isin(self.names)]['Num of SAT Test Takers']
		data = data.reset_index(drop=True)

		#dynamically set number of bins based on number of schools
		plt.hist(data.dropna(),bins=max(10,int(len(names)/10)))

		#set axis labels and title
		plt.xlabel('Number of SAT Test Takers',fontsize=16)
		plt.ylabel('Number of Schools',fontsize=16)
		plt.title('Distribution of Number of SAT Test Takers',fontsize=20)

		plt.show()

	def regents_bar_plot():
		'''plots a bar plot of the % of students that passed the Regents exam in June and August'''

		#get Regents data for each month
		june_data = school_database.loc[school_database['school_name'].isin(self.names)]['Regents Pass Rate - June']
		august_data = school_database.loc[school_database['school_name'].isin(self.names)]['Regents Pass Rate - August']
		june_data = june_data.dropna()
		august_data = august_data.dropna()

		#create a bar for each month
		bar_width = 0.35
		rects1 = plt.bar(np.arange(len(june_data)), june_data, bar_width,color='b',label='June')
		rects2 = plt.bar(np.arange(len(august_data))+bar_width, august_data, bar_width,color='r',label='August')

		#set labels, titles, and ticks with school names
		plt.xlabel('Schools')
		plt.ylabel('Regents Pass Rate (%)')
		plt.title('Regents Pass Rate by School')
		plt.xticks(np.arange(len(june_data)) + bar_width, names,fontsize=8)
		plt.xticks(rotation=90)

		#catches user warning rather than printing it
		with warnings.catch_warnings():
			warnings.simplefilter("ignore", UserWarning)
			plt.tight_layout()

		plt.legend()

		plt.show()
