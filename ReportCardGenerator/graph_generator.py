#import modules/classes
from school import *

#import necessary libraries
import matplotlib.pyplot as plt
import warnings
import os

class InvalidComparisonError(Exception):

	'''This exception is raised when you try to create a graph generator for only one school'''

	def __str__(self):
		return "Cannot compare a school to itself!"

class GraphGenerator(object):
	'''Each instance of this object consists of a list of school objects that we want to compare by generating graphs'''

	def __init__(self, school_database, schools, defaultPageSize):
		if len(schools) > 1:
			self.school_database = school_database
			self.schools = schools
			self.names =[str(school) for school in schools]

			#convert from pixels to inches (80 pixels to an inch)
			self.page_width = defaultPageSize[0]/80
			self.page_height = defaultPageSize[1]/80

			#create directory to save plots
			script_dir = os.path.dirname(__file__)
			plots_dir = os.path.join(script_dir, 'plots/')

			if not os.path.isdir(plots_dir):
				os.makedirs(plots_dir)

		else:
			raise InvalidComparisonError


	def get_distribution_plots(self):

		'''Creates all of the boxplots and returns a list of all their filenames/address.'''
		return [self.create_sat_score_boxplots(), self.create_sat_test_takers_histogram(), self.create_regents_box_plots(), self.create_graduation_and_college_box_plots(), self.create_student_satisfaction_box_plots()]

	def get_bar_plots(self):

		'''For clarity and neatness, we only want barplots to show at most 15 schools and at least 5 schools, so we split the plotting data
		and create multiple plots as necessary.'''

		#Add constraints on how many schools are in a plot and keep track of png files that are generated
		schools_to_plot = self.names
		min_schools_in_plot = 5
		max_schools_in_plot = 15
		#Add an index to each png so they are not overwritten
		fig_index = 1
		figures = []


		#If the list of schools is larger than 15, generate many plots per plot type where each plot contains at most 15 and at least 5 schools
		if len(schools_to_plot) > max_schools_in_plot:

			while len(schools_to_plot) >= max_schools_in_plot + min_schools_in_plot:

				#Generate all the bar plots for the current subset of the list
				figures.append(self.create_sat_score_bar_plot(schools_to_plot[0:15],fig_index))
				figures.append(self.create_sat_test_takers_bar_plot(schools_to_plot[0:15], fig_index))
				figures.append(self.create_regents_bar_plot(schools_to_plot[0:15], fig_index))
				figures.append(self.create_graduation_and_college_bar_plots(schools_to_plot[0:15], fig_index))
				figures.append(self.create_student_satisfaction_bar_plots(schools_to_plot[0:15], fig_index))

				#Delete already-plotted schools from the list and change the index
				schools_to_plot = schools_to_plot[15:]
				fig_index += 1


		#If the list of schools is small enough, generate only one plot per plot type
		figures.append(self.create_sat_score_bar_plot(schools_to_plot, fig_index))
		figures.append(self.create_sat_test_takers_bar_plot(schools_to_plot, fig_index))
		figures.append(self.create_regents_bar_plot(schools_to_plot, fig_index))
		figures.append(self.create_graduation_and_college_bar_plots(schools_to_plot, fig_index))
		figures.append(self.create_student_satisfaction_bar_plots(schools_to_plot, fig_index))

		#Returns a list of filenames indicating the address of the bar plots
		return figures


	def create_sat_score_bar_plot(self, schools_to_plot, fig_index):

		'''Saves a bar plot of the SAT scores by section for each school.'''

		#Get SAT score data for each section, dropping NaN values. Avoid searching the dataframe multiple times.
		math_data = self.school_database.loc[self.school_database['school_name'].isin(schools_to_plot)]['SAT Math Avg'].dropna()
		reading_data = self.school_database.loc[self.school_database['school_name'].isin(schools_to_plot)]['SAT Critical Reading Avg'].dropna()
		writing_data = self.school_database.loc[self.school_database['school_name'].isin(schools_to_plot)]['SAT Writing Avg'].dropna()

		#set size of figure
		plt.figure(figsize=(self.page_width*.6,self.page_height*.6))

		#create a bar for each month
		bar_width = 0.2
		rects1 = plt.bar(np.arange(len(math_data)), math_data, bar_width, color='b', label='Math')
		rects2 = plt.bar(np.arange(len(reading_data)) + bar_width, reading_data, bar_width, color='r', label='Reading')
		rects3 = plt.bar(np.arange(len(writing_data)) + 2 * bar_width, writing_data, bar_width, color='g', label='Writing')

		#set labels, titles, and ticks with school names
		plt.xlabel('Schools')
		plt.ylabel('SAT Score')
		plt.title('SAT Scores by School')
		plt.xticks(np.arange(len(math_data)) + 1.5*bar_width, self.names, fontsize=8)
		plt.xticks(rotation=90)

		#catches user warning rather than printing it
		with warnings.catch_warnings():
			warnings.simplefilter("ignore", UserWarning)
			plt.tight_layout()

		lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

		#save plot
		filename = 'sat_barplot' + str(fig_index)
		plt.savefig('plots/' + filename + '.png',bbox_extra_artists=(lgd,), bbox_inches = 'tight')

		return 'plots/'+ filename + '.png'


	def create_sat_test_takers_bar_plot(self, schools_to_plot, fig_index):
		'''saves a bar plot of the number of students who took the SAT by school'''

		#get data for the number of test takers
		data = self.school_database.loc[self.school_database['school_name'].isin(schools_to_plot)]['Number of SAT Test Takers']
		data = data.dropna()

		#set size of figure
		plt.figure(figsize=(self.page_width*.8,self.page_height*.6))

		plt.bar(np.arange(len(data)),data,align='center')
		plt.xlabel('Schools')
		plt.ylabel('Number of Students')
		plt.xticks(np.arange(len(data)), self.names,fontsize=8)
		plt.xticks(rotation=90)
		plt.title('Number of SAT Test Takers by School')

		#catches user warning rather than printing it
		with warnings.catch_warnings():
			warnings.simplefilter("ignore", UserWarning)
			plt.tight_layout()

		#save plot
		filename = 'sat_test_takers_barplot' + str(fig_index)
		plt.savefig('Plots/' + filename +'.png', bbox_inches='tight')

		return 'plots/'+filename+'.png'



	def create_regents_bar_plot(self, schools_to_plot, fig_index):
		'''Saves a bar plot of the percent of students that passed the Regents exam in June and August'''

		#get Regents data for each month
		june_data = self.school_database.loc[self.school_database['school_name'].isin(schools_to_plot)]['Regents Pass Rate - June']
		august_data = self.school_database.loc[self.school_database['school_name'].isin(schools_to_plot)]['Regents Pass Rate - August']
		june_data = june_data.dropna()
		august_data = august_data.dropna()

		#set size of figure
		plt.figure(figsize=(self.page_width*.6,self.page_height*.6))

		#create a bar for each month
		bar_width = 0.35
		rects1 = plt.bar(np.arange(len(june_data)), june_data, bar_width,color='b',label='June')
		rects2 = plt.bar(np.arange(len(august_data))+bar_width, august_data, bar_width,color='r',label='August')

		#set labels, titles, and ticks with school names
		plt.xlabel('Schools')
		plt.ylabel('Regents Pass Rate (%)')
		plt.title('Regents Pass Rate by School')
		plt.xticks(np.arange(len(june_data)) + bar_width, self.names,fontsize=8)
		plt.xticks(rotation=90)

		#catches user warning rather than printing it
		with warnings.catch_warnings():
			warnings.simplefilter("ignore", UserWarning)
			plt.tight_layout()

		lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

		#save plot
		filename = 'regents_barplot' + str(fig_index)
		plt.savefig('plots/'+filename+'.png',bbox_extra_artists=(lgd,), bbox_inches='tight')

		return 'plots/'+filename+'.png'


	def create_graduation_and_college_bar_plots(self, schools_to_plot, fig_index):
		'''saves bar plots of ontrack graduation, graduation, and college career rates for each school'''

		years = ['2012','2013']

		#make bar plot for each year
		for year in years:
			#get the student rates for each category
			ontrack_data = self.school_database.loc[self.school_database['school_name'].isin(schools_to_plot)]['Graduation Ontrack Rate - '+year]
			graduation_data = self.school_database.loc[self.school_database['school_name'].isin(schools_to_plot)]['Graduation Rate - '+year]
			college_data = self.school_database.loc[self.school_database['school_name'].isin(schools_to_plot)]['College Career Rate - '+year]

			#drop schools that have any of the the three rates missing
			rows_to_drop=[]
			for i in range (0,len(schools_to_plot)):
				if np.isnan(college_data.iloc[i]) or np.isnan(college_data.iloc[i]) or np.isnan(college_data.iloc[i]):
					row_index = ontrack_data.index.values[i]
					rows_to_drop.append(row_index)
			ontrack_data = ontrack_data.drop(rows_to_drop)
			graduation_data = graduation_data.drop(rows_to_drop)
			college_data = college_data.drop(rows_to_drop)

			#clear plot
			plt.clf()

			#set size of figure
			plt.figure(figsize=(self.page_width*.6,self.page_height*.6))

			#create a bar for each category
			bar_width = 0.2
			rects1 = plt.bar(np.arange(len(ontrack_data)), ontrack_data, bar_width,color='b',label='Ontrack')
			rects2 = plt.bar(np.arange(len(graduation_data))+bar_width, graduation_data, bar_width,color='r',label='Graduation')
			rects3 = plt.bar(np.arange(len(college_data))+2*bar_width, college_data, bar_width,color='g',label='College')

			#set labels, titles, and ticks with school names
			plt.xlabel('Schools')
			plt.ylabel('Rate (%)')
			plt.title('Graduation and College Rates by School in '+year)
			plt.xticks(np.arange(len(graduation_data)) + 1.5*bar_width, self.names,fontsize=8)
			plt.xticks(rotation=90)

			#catches user warning rather than printing it
			with warnings.catch_warnings():
				warnings.simplefilter("ignore", UserWarning)
				plt.tight_layout()

			lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

			#save plot
			filename = 'graduation_and_college_barplots' + str(fig_index)
			plt.savefig('plots/'+filename+'.png',bbox_extra_artists=(lgd,), bbox_inches='tight')

			return 'plots/'+filename+'.png'


	def create_student_satisfaction_bar_plots(self, schools_to_plot, fig_index):
		'''saves a bar plot of the student satisfaction scores by school'''

		#get Regents data for each month
		data_2012 = self.school_database.loc[self.school_database['school_name'].isin(schools_to_plot)]['Student Satisfaction Rate - 2012']
		data_2013 = self.school_database.loc[self.school_database['school_name'].isin(schools_to_plot)]['Student Satisfaction Rate - 2013']

		#drop schools that have any of the the two years missing
		rows_to_drop=[]
		for i in range (0,len(schools_to_plot)):
			if np.isnan(data_2012.iloc[i]) or np.isnan(data_2013.iloc[i]):
				row_index = data_2012.index.values[i]
				rows_to_drop.append(row_index)
		data_2012 = data_2012.drop(rows_to_drop)
		data_2013 = data_2013.drop(rows_to_drop)

		#set size of figure
		plt.figure(figsize=(self.page_width*.6,self.page_height*.6))

		#create a bar for each month
		bar_width = 0.35
		rects1 = plt.bar(np.arange(len(data_2012)), data_2012, bar_width,color='b',label='2012')
		rects2 = plt.bar(np.arange(len(data_2013))+bar_width, data_2013, bar_width,color='r',label='2013')

		#set labels, titles, and ticks with school names
		plt.xlabel('Schools')
		plt.ylabel('Satisfaction (out of 10)')
		plt.title('Student Satisfaction by School')
		plt.xticks(np.arange(len(data_2012)) + bar_width, self.names,fontsize=8)
		plt.xticks(rotation=90)

		#catches user warning rather than printing it
		with warnings.catch_warnings():
			warnings.simplefilter("ignore", UserWarning)
			plt.tight_layout()

		lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

		#save plot
		filename = 'student_satisfaction_barplots' + str(fig_index)
		plt.savefig('plots/'+filename+'.png',bbox_extra_artists=(lgd,), bbox_inches='tight')

		return 'plots/'+filename+'.png'


	def create_sat_score_boxplots(self):
		'''saves boxplots showing the distribution of SAT scores for each of the 3 sections'''
		
		data=[]
		sections = ['Math','Critical Reading','Writing']

		#append data from each section of the SAT
		for section in sections:
			section_data = self.school_database.loc[self.school_database['school_name'].isin(self.names)]['SAT '+section+' Avg']
			data.append(section_data)

		#set size of figure
		plt.figure(figsize=(self.page_width*.8,self.page_height*.5))
		
		plt.boxplot(data)

		#set xticks for each section, with the section name
		plt.xticks(np.arange(1,len(sections)+1),sections)

		#set axis labels and title
		plt.xlabel('SAT Sections',fontsize=16)
		plt.ylabel('Score',fontsize=16)
		plt.title('SAT Score Distribution',fontsize=20)

		#save plot
		filename = 'sat_boxplots'
		plt.savefig('plots/'+filename+'.png', bbox_inches='tight')

		return 'plots/'+filename+'.png'


	def create_sat_test_takers_histogram(self):
		'''saves a histogram showing the distribution of the number of SAT test takers'''
		
		
		#get data for the number of test takers
		data = self.school_database.loc[self.school_database['school_name'].isin(self.names)]['Number of SAT Test Takers']
		data = data.reset_index(drop=True)
		
		#set size of figure
		plt.figure(figsize=(self.page_width*.8,self.page_height*.5))

		#dynamically set number of bins based on number of school
		plt.hist(data.dropna().values,bins=max(10,int(len(self.names)/10)))
		#plt.hist(list(data.dropna()), bins=10)

		#set axis labels and title
		plt.xlabel('Number of SAT Test Takers',fontsize=16)
		plt.ylabel('Number of Schools',fontsize=16)
		plt.title('Distribution of Number of SAT Test Takers',fontsize=20)

		#save plot
		filename = 'sat_test_takers_histogram'
		plt.savefig('plots/'+filename+'.png', bbox_inches='tight')

		return 'plots/'+filename+'.png'
	



	def create_regents_box_plots(self):
		'''saves boxplots showing the distribution of Regents pass rates for each of the 2 months'''
		
		data=[]
		months = ['June','August']

		#append data from each month of the Regents data
		for month in months:
			month_data = self.school_database.loc[self.school_database['school_name'].isin(self.names)]['Regents Pass Rate - '+month]
			data.append(month_data)

		#set size of figure
		plt.figure(figsize=(self.page_width*.8,self.page_height*.5))

		plt.boxplot(data)

		#set xticks for each section, with the section name
		plt.xticks(np.arange(1,len(months)+1),months)

		#set axis labels and title
		plt.xlabel('Months',fontsize=16)
		plt.ylabel('Pass Rate (%)',fontsize=16)
		plt.title('Regents Pass Rate by Month',fontsize=20)
		
		#save plot
		filename = 'regents_boxplots'
		plt.savefig('plots/'+filename+'.png', bbox_inches='tight')

		return 'plots/'+filename+'.png'



	def create_graduation_and_college_box_plots(self):
		'''saves boxplots showing the distribution of ontrack graduation, graduation, and college career rates'''
		
		data=[]
		categories = ['Graduation Ontrack','Graduation','College Career']
		years = ['2012','2013']
		tick_labels = []

		#append data from each category
		for category in categories:
			for year in years:
				category_data = self.school_database.loc[self.school_database['school_name'].isin(self.names)][category + ' Rate - ' + year]
				data.append(category_data)
				tick_labels.append(category + ' - '+year)

		#set size of figure
		plt.figure(figsize=(self.page_width*.8,self.page_height*.6))

		plt.boxplot(data)

		#set xticks for each section, with the section name
		plt.xticks(np.arange(1,len(categories)*len(years)+1),tick_labels)
		plt.xticks(rotation=90)

		#set axis labels and title
		plt.xlabel('Categories',fontsize=16)
		plt.ylabel('Rate (%)',fontsize=16)
		plt.title('Graduation and College Career Rates',fontsize=20)

		#catches user warning rather than printing it
		with warnings.catch_warnings():
			warnings.simplefilter("ignore", UserWarning)
			plt.tight_layout()

		#save plot
		filename = 'graduation_and_college_boxplots'
		plt.savefig('plots/'+filename+'.png', bbox_inches='tight')

		return 'plots/'+filename+'.png'


	def create_student_satisfaction_box_plots(self):
		'''saves boxplots showing the distribution of student satisfaction scores'''
		
		data=[]
		years = ['2012','2013']

		#append data from each month of the Regents data
		for year in years:
			year_data = self.school_database.loc[self.school_database['school_name'].isin(self.names)]['Student Satisfaction Rate - '+year]
			data.append(year_data)

		#set size of figure
		plt.figure(figsize=(self.page_width*.8,self.page_height*.5))

		plt.boxplot(data)

		#set xticks for each section, with the section name
		plt.xticks(np.arange(1,len(years)+1),years)

		#set axis labels and title
		plt.xlabel('Years',fontsize=16)
		plt.ylabel('Satisfaction (out of 10)',fontsize=16)
		plt.title('Student Satisfaction by Year',fontsize=20)
		
		#save plot
		filename = 'student_satisfaction_boxplots'
		plt.savefig('plots/'+filename+'.png', bbox_inches='tight')

		return 'plots/'+filename+'.png'

'''
from utilities import *
from reportlab.rl_config import defaultPageSize
school_database,school_names,valid_features = load_session()
schools = [School(school_database, school_names, 'Henry Street School for International Studies'), School(school_database, school_names, 'University Neighborhood High School'), School(school_database, school_names, 'East Side Community School')]
graph_generator = GraphGenerator(school_database,schools, defaultPageSize)
x = graph_generator.get_distribution_plots()
print x 
'''


