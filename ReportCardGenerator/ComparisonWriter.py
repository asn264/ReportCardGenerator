from utilities import *
from School import *

import matplotlib.pyplot as plt

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
		pass

def sat_boxplots():
	names = ['Stuyvesant High School', 'Brooklyn Technical High School','East Side Community School','Essex Street Academy','NYC iSchool','Urban Assembly Maker Academy']
	
	data=[]
	sections = ['Math','Critical Reading','Writing']

	for section in sections:
		section_data = school_database.loc[school_database['school_name'].isin(names)]['SAT '+section+' Avg']
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

def sat_test_takers_histogram():
	#names = ['Stuyvesant High School', 'Brooklyn Technical High School','East Side Community School','Essex Street Academy','NYC iSchool','Urban Assembly Maker Academy']
	names = school_database['school_name'].values.ravel()

	data = school_database.loc[school_database['school_name'].isin(names)]['Num of SAT Test Takers'].head(n=99)
	data = data.reset_index(drop=True)

	#dynamically set number of bins based on number of schools
	plt.hist(data.dropna(),bins=max(10,int(len(names)/10)))

	#set axis labels and title
	plt.xlabel('Number of SAT Test Takers',fontsize=16)
	plt.ylabel('Number of Schools',fontsize=16)
	plt.title('Distribution of Number of SAT Test Takers',fontsize=20)

	plt.show()

