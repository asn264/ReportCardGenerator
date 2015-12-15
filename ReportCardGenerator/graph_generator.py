'''
Authors: Aditi Nair (asn264) and Akash Shah (ass502)

This file generates visualizations of reportlab data using matplotlib.
There are two categories of plots: distribution plots and bar plots. Distribution plots consist of boxplots and histograms. 
There are two helper functions, one for each category, that call each individual plot function to save that plot and 
return all of the filenames, which are then used in the summary writer class.
'''

#import modules/classes
from school import *

#import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import os
import errno
import shutil


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

			#convert defaultPageSize from pixels to inches (80 pixels to an inch)
			self.page_width = defaultPageSize[0]/80
			self.page_height = defaultPageSize[1]/80

			#create a directory to store the plot png files in
			script_dir = os.path.dirname(__file__)
			self.plots_dir = os.path.join(script_dir, 'plots/')
			#if the directory doesn't already exist, make it
			if not os.path.isdir(self.plots_dir): 
				os.makedirs(self.plots_dir)

		else:
			raise InvalidComparisonError

	def clear_plots_directory(self):
		'''Deletes the plots directory as well as its contents.'''

		try:
			shutil.rmtree(self.plots_dir)
		except OSError: #catch exception if directory doesn't exist
			pass

	def get_distribution_plots(self):

		'''Creates all of the boxplots/histograms and returns a list of all their filenames/address.'''

		plots = [self.create_sat_score_boxplots(), self.create_sat_test_takers_histogram(), self.create_regents_box_plots(), self.create_graduation_and_college_box_plots(), self.create_student_satisfaction_box_plots()]
		return [plot for plot in plots if plot is not None]

	def get_bar_plots(self):

		'''For clarity and neatness, we only want barplots to show at most 15 schools and at least 5 schools, so we split the plotting data
		and create multiple plots as necessary.'''

		#Add constraints on how many schools are in a plot and keep track of png files that are generated
		schools_to_plot = self.names
		min_schools_in_plot = 5
		max_schools_in_plot = 15

		#Add an index to each png so they are not overwritten
		fig_index = 1

		plots = []

		#If the list of schools is larger than 15, generate many plots per plot type where each plot contains at most 15 and at least 5 schools
		if len(schools_to_plot) > max_schools_in_plot:

			while len(schools_to_plot) >= max_schools_in_plot + min_schools_in_plot:

				#Generate all the bar plots for the current subset of the list
				plots.append(self.create_sat_score_bar_plot(schools_to_plot[0:15],fig_index))
				plots.append(self.create_sat_test_takers_bar_plot(schools_to_plot[0:15], fig_index))
				plots.append(self.create_regents_bar_plot(schools_to_plot[0:15], fig_index))
				plots.extend(self.create_graduation_and_college_bar_plots(schools_to_plot[0:15], fig_index))
				plots.append(self.create_student_satisfaction_bar_plots(schools_to_plot[0:15], fig_index))

				#Delete already-plotted schools from the list and change the index
				schools_to_plot = schools_to_plot[15:]
				fig_index += 1


		#If the list of schools is small enough, generate only one plot per plot type. 
		#Functions below return file addresses if graphs were generated or None if the necessary data was sparse
		plots.append(self.create_sat_score_bar_plot(schools_to_plot, fig_index))
		plots.append(self.create_sat_test_takers_bar_plot(schools_to_plot, fig_index))
		plots.append(self.create_regents_bar_plot(schools_to_plot, fig_index))
		plots.extend(self.create_graduation_and_college_bar_plots(schools_to_plot, fig_index))
		plots.append(self.create_student_satisfaction_bar_plots(schools_to_plot, fig_index))

		#Returns a list of filenames indicating the address of the bar plots
		return [plot for plot in plots if plot is not None]


	def create_sat_score_bar_plot(self, schools_to_plot, fig_index):

		'''Saves a bar plot of the SAT scores by section for each school.'''

		#get SAT score data for all three sections, dropping rows with missing data for all of the sections
		data = self.school_database.loc[self.school_database['school_name'].str.lower().isin([school.lower() for school in schools_to_plot])][['school_name','SAT Math Avg','SAT Critical Reading Avg','SAT Writing Avg']].dropna(thresh=2)

		#don't do bar plot if there is only one school
		if len(data)<=1:
			return None

		#set size of figure
		plt.figure(figsize=(self.page_width*.6,self.page_height*.6))

		#create a bar for each month
		bar_width = 0.2
		rects1 = plt.bar(np.arange(len(data)), data['SAT Math Avg'], bar_width, color='b', label='Math')
		rects2 = plt.bar(np.arange(len(data)) + bar_width, data['SAT Critical Reading Avg'], bar_width, color='r', label='Reading')
		rects3 = plt.bar(np.arange(len(data)) + 2 * bar_width, data['SAT Writing Avg'], bar_width, color='g', label='Writing')

		#set labels, titles, and ticks with school names
		plt.xlabel('Schools')
		plt.ylabel('SAT Score')
		plt.title('SAT Scores by School')
		plt.xticks(np.arange(len(data)) + 1.5*bar_width, data['school_name'].tolist(), fontsize=8)
		plt.xticks(rotation=90)

		#catches user warning rather than printing it
		with warnings.catch_warnings():
			warnings.simplefilter("ignore", UserWarning)
			plt.tight_layout()

		#put legend outside of plot
		lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

		#save plot
		filename = 'sat_barplot' + str(fig_index)
		plt.savefig('plots/' + filename + '.png',bbox_extra_artists=(lgd,), bbox_inches = 'tight')

		#close plot to free up memory
		plt.close()

		return 'plots/'+ filename + '.png'


	def create_sat_test_takers_bar_plot(self, schools_to_plot, fig_index):
		'''saves a bar plot of the number of students who took the SAT by school'''

		#get data for the number of test takers, dropping rows with missing data
		data = self.school_database.loc[self.school_database['school_name'].str.lower().isin([school.lower() for school in schools_to_plot])][['school_name','Number of SAT Test Takers']].dropna()

		#don't do bar plot if there is only one school
		if len(data)<=1:
			return None

		#set size of figure
		plt.figure(figsize=(self.page_width*.8,self.page_height*.6))

		plt.bar(np.arange(len(data)),data['Number of SAT Test Takers'],align='center')

		#set labels, titles, and ticks with school names
		plt.xlabel('Schools')
		plt.ylabel('Number of Students')
		plt.xticks(np.arange(len(data)), data['school_name'].tolist(),fontsize=8)
		plt.xticks(rotation=90)
		plt.title('Number of SAT Test Takers by School')

		#catches user warning rather than printing it
		with warnings.catch_warnings():
			warnings.simplefilter("ignore", UserWarning)
			plt.tight_layout()

		#save plot
		filename = 'sat_test_takers_barplot' + str(fig_index)
		plt.savefig('plots/' + filename +'.png', bbox_inches='tight')

		#close plot to free up memory
		plt.close()

		return 'plots/'+filename+'.png'


	def create_regents_bar_plot(self, schools_to_plot, fig_index):
		'''Saves a bar plot of the percent of students that passed the Regents exam in June and August'''

		#get Regents data for both months, dropping rows with both months missing
		data = self.school_database.loc[self.school_database['school_name'].str.lower().isin([school.lower() for school in schools_to_plot])][['school_name','Regents Pass Rate - June','Regents Pass Rate - August']].dropna(thresh=2)

		#don't do bar plot if there is only one school
		if len(data)<=1:
			return None

		#set size of figure
		plt.figure(figsize=(self.page_width*.6,self.page_height*.6))

		#create a bar for each month
		bar_width = 0.35
		rects1 = plt.bar(np.arange(len(data)), data['Regents Pass Rate - June'], bar_width,color='b',label='June')
		rects2 = plt.bar(np.arange(len(data))+bar_width, data['Regents Pass Rate - August'], bar_width,color='r',label='August')

		#set labels, titles, and ticks with school names
		plt.xlabel('Schools')
		plt.ylabel('Regents Pass Rate (%)')
		plt.title('Regents Pass Rate by School')
		plt.xticks(np.arange(len(data)) + bar_width, data['school_name'].tolist(),fontsize=8)
		plt.xticks(rotation=90)

		#catches user warning rather than printing it
		with warnings.catch_warnings():
			warnings.simplefilter("ignore", UserWarning)
			plt.tight_layout()

		#put legend outside of plot
		lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

		#save plot
		filename = 'regents_barplot' + str(fig_index)
		plt.savefig('plots/'+filename+'.png',bbox_extra_artists=(lgd,), bbox_inches='tight')


		#close plot to free up memory
		plt.close()

		return 'plots/'+filename+'.png'


	def create_graduation_and_college_bar_plots(self, schools_to_plot, fig_index):
		'''saves bar plots of ontrack graduation, graduation, and college career rates for each school, for 2012 and 2013'''

		years = ['2012','2013']

		#store filename of the plot for each year
		filenames = []

		#make bar plot for each year
		for year in years:
			#get the student rates for all 3 categories, dropping the rows which have missing data for all 3 categories
			data = self.school_database.loc[self.school_database['school_name'].str.lower().isin([school.lower() for school in schools_to_plot])][['school_name','Graduation Ontrack Rate - '+year,'Graduation Rate - '+year,'College Career Rate - '+year]].dropna(thresh=2)

			#if there is one school or less, don't do the bar plot
			if len(data)<=1:
				pass

			else:
				#clear plot
				plt.clf()

				#set size of figure
				plt.figure(figsize=(self.page_width*.6,self.page_height*.6))

				#create a bar for each category
				bar_width = 0.2
				rects1 = plt.bar(np.arange(len(data)), data['Graduation Ontrack Rate - '+year], bar_width,color='b',label='Ontrack')
				rects2 = plt.bar(np.arange(len(data))+bar_width, data['Graduation Rate - '+year], bar_width,color='r',label='Graduation')
				rects3 = plt.bar(np.arange(len(data))+2*bar_width, data['College Career Rate - '+year], bar_width,color='g',label='College')

				#set labels, titles, and ticks with school names
				plt.xlabel('Schools')
				plt.ylabel('Rate (%)')
				plt.title('Graduation and College Rates by School in '+year)
				plt.xticks(np.arange(len(data)) + 1.5*bar_width, data['school_name'].tolist(),fontsize=8)
				plt.xticks(rotation=90)

				#catches user warning rather than printing it
				with warnings.catch_warnings():
					warnings.simplefilter("ignore", UserWarning)
					plt.tight_layout()

				#put legend outside of plot
				lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

				#save plot
				filename = year+'_graduation_and_college_barplots' + str(fig_index)
				plt.savefig('plots/'+filename+'.png',bbox_extra_artists=(lgd,), bbox_inches='tight')
				filenames.append('plots/'+filename+'.png')

		#close plot to free up memory
		plt.close()

		return filenames


	def create_student_satisfaction_bar_plots(self, schools_to_plot, fig_index):
		'''saves a bar plot of the student satisfaction scores by school'''

		#get get student satisfaction rates for both years, dropping rows with both years missing
		data = self.school_database.loc[self.school_database['school_name'].str.lower().isin([school.lower() for school in schools_to_plot])][['school_name','Student Satisfaction Rate - 2012','Student Satisfaction Rate - 2013']].dropna(thresh=2)

		#if there is one school or less, don't do the bar plot
		if len(data)<=1: 
			return None

		#set size of figure
		plt.figure(figsize=(self.page_width*.6,self.page_height*.6))

		#create a bar for each month
		bar_width = 0.35
		rects1 = plt.bar(np.arange(len(data)), data['Student Satisfaction Rate - 2012'], bar_width,color='b',label='2012')
		rects2 = plt.bar(np.arange(len(data))+bar_width, data['Student Satisfaction Rate - 2013'], bar_width,color='r',label='2013')

		#set labels, titles, and ticks with school names
		plt.xlabel('Schools')
		plt.ylabel('Satisfaction (out of 10)')
		plt.title('Student Satisfaction by School')
		plt.xticks(np.arange(len(data)) + bar_width, data['school_name'].tolist(),fontsize=8)
		plt.xticks(rotation=90)

		#catches user warning rather than printing it
		with warnings.catch_warnings():
			warnings.simplefilter("ignore", UserWarning)
			plt.tight_layout()

		#put legend outside of plot
		lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

		#save plot
		filename = 'student_satisfaction_barplots' + str(fig_index)
		plt.savefig('plots/'+filename+'.png',bbox_extra_artists=(lgd,), bbox_inches='tight')


		#close plot to free up memory
		plt.close()

		return 'plots/'+filename+'.png'


	def create_sat_score_boxplots(self):
		'''saves boxplots showing the distribution of SAT scores for each of the 3 sections'''
		
		data=[]
		sections = ['Math','Critical Reading','Writing']

		#append data from each section of the SAT
		for section in sections:
			section_data = self.school_database.loc[self.school_database['school_name'].str.lower().isin([school.lower() for school in self.names])]['SAT '+section+' Avg']

			#don't create boxplot if there are less than 5 data points
			if len(section_data.dropna()) < 5:
				return None

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


		#close plot to free up memory
		plt.close()

		return 'plots/'+filename+'.png'


	def create_sat_test_takers_histogram(self):
		'''saves a histogram showing the distribution of the number of SAT test takers'''
		
		#get data for the number of test takers
		data = self.school_database.loc[self.school_database['school_name'].str.lower().isin([school.lower() for school in self.names])]['Number of SAT Test Takers']
		data = data.reset_index(drop=True)

		#don't create histogram if there is less than 1 data point
		if len(data.dropna()) < 1:
			return None
		
		#set size of figure
		plt.figure(figsize=(self.page_width*.8,self.page_height*.5))

		#dynamically set number of bins based on number of school
		plt.hist(data.dropna().values,bins=max(10,int(len(self.names)/10)))

		#set axis labels and title
		plt.xlabel('Number of SAT Test Takers',fontsize=16)
		plt.ylabel('Number of Schools',fontsize=16)
		plt.title('Distribution of Number of SAT Test Takers',fontsize=20)

		#save plot
		filename = 'sat_test_takers_histogram'
		plt.savefig('plots/'+filename+'.png', bbox_inches='tight')


		#close plot to free up memory
		plt.close()

		return 'plots/'+filename+'.png'
	

	def create_regents_box_plots(self):
		'''saves boxplots showing the distribution of Regents pass rates for each of the 2 months'''
		
		data=[]
		months = ['June','August']

		#append data from each month of the Regents data
		for month in months:
			month_data = self.school_database.loc[self.school_database['school_name'].str.lower().isin([school.lower() for school in self.names])]['Regents Pass Rate - '+month]
			
			#don't create boxplot if there are less than 5 data points
			if len(month_data.dropna()) < 5:
				return None

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

		#close plot to free up memory
		plt.close()

		return 'plots/'+filename+'.png'


	def create_graduation_and_college_box_plots(self):
		'''saves boxplots showing the distribution of ontrack graduation, graduation, and college career rates'''
		
		data=[]
		categories = ['Graduation Ontrack','Graduation','College Career']
		years = ['2012','2013']
		tick_labels = []

		#keep track of whether there is at least one valid boxplot
		valid_plot = False

		#append data from each category and year
		for category in categories:
			for year in years:
				category_data = self.school_database.loc[self.school_database['school_name'].str.lower().isin([school.lower() for school in self.names])][category + ' Rate - ' + year]
				
				#if there is enough data for at least one type of boxplot, the entire group of plots is valid
				data_copy = category_data.copy()
				if len(data_copy.dropna())>=5:
					valid_plot=True

				data.append(category_data)

				#create tick label for the current plot based on the category and year
				tick_labels.append(category + ' - '+year)

		if not valid_plot:
			return None

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

		#close plot to free up memory
		plt.close()

		return 'plots/'+filename+'.png'


	def create_student_satisfaction_box_plots(self):
		'''saves boxplots showing the distribution of student satisfaction scores'''
		
		data=[]
		years = ['2012','2013']

		#keep track of whether there is at least one valid boxplot
		valid_plot = False

		#append data from each month of the Regents data
		for year in years:
			year_data = self.school_database.loc[self.school_database['school_name'].str.lower().isin([school.lower() for school in self.names])]['Student Satisfaction Rate - '+year]
			
			##if there is enough data for at least one year's boxplot, the entire group of plots is valid
			data_copy = year_data.copy()
			if len(data_copy.dropna())>=5:
				valid_plot=True

			data.append(year_data)

		if not valid_plot:
			return None

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

		#close plot to free up memory
		plt.close()

		return 'plots/'+filename+'.png'


