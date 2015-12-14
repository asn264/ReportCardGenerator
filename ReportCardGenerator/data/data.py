'''
Authors: Aditi Nair (asn264) and Akash Shah (ass502)

This module contains the functions and code used to load the school performance data from data frames and clean them. 
Then they are all merged into one single database based on the unique school identification number (DBN).
We added an additional column which contains the coordinates of the address, calculated using GeoPy.

We output a csv file called school_database.csv. In the main program, this pre-formatted csv is loaded directly into a dataframe to avoid 
slower runtime and to minimize queries to Google's geolocation services, which impose a strict limit on the number of queries in a 24-hour period.
'''

#import necessary libraries
import pandas as pd
import numpy as np

#import Google API for geopy which validates addresses/coordinates
from geopy.geocoders import GoogleV3

def loadDataframe(filename,relevant,columns,nullValues):
	"""function to load data from csv and do some basic cleaning"""

	data_df = pd.read_csv(filename)
	data_df.columns = map(str.lower, data_df.columns)
        
	#if relevant is True, columns is the list of columns we want so we filter for those 
	if relevant:
		data_df = data_df[columns]
	#if relevant is False, columns is the list of columns we don't want so we drop them
	else:
		data_df.drop(columns,axis=1,inplace=True)

	#set index to the unique school identification number
	data_df.set_index('dbn')
	#standardize null vlaues
	data_df.replace(nullValues,np.nan,inplace=True)

	return data_df


nullValues=['s','.','N/A']

#load dataframes from each of our 4 data sources
schools = loadDataframe('raw_data/DOE_High_School_Directory_2014-2015.csv',True,['dbn','school_name','primary_address_line_1','city'],nullValues)

sat_scores = loadDataframe('raw_data/SAT_Results.csv',False,'school name',nullValues)

regents_performance = loadDataframe('raw_data/Graduation_Outcomes_-_Class_Of_2010_-_Regents-based_Math-_ELA_APM_-_School_Level.csv',False,'name',nullValues)
regents_performance = regents_performance[regents_performance['demographic'] == 'All Students']
regents_performance.drop(['demographic'],axis=1,inplace=True)

school_performance = loadDataframe('raw_data/DOE_High_School_Performance-Directory_2014-2015.csv',False,['quality_review_rating','quality_review_year','ontrack_year1_historic_avg_similar_schls','graduation_rate_historic_avg_similar_schls','college_career_rate_historic_avg_similar_schls','student_satisfaction_historic_avg_similar_schls'],nullValues)


#do a left join on the tables starting with school, on the dbn column which uniquely identifies the school
dfs = [schools,sat_scores,regents_performance,school_performance]
school_database = reduce(lambda left,right: pd.merge(left,right,how='left',on='dbn'),dfs)

#rename columns to user-friendly names
school_database.rename(columns={'primary_address_line_1': 'address', 'num of sat test takers': 'Number of SAT Test Takers', 'sat critical reading avg. score': 'SAT Critical Reading Avg', 'sat math avg. score': 'SAT Math Avg', 'sat writing avg. score': 'SAT Writing Avg', '% of cohort - june': 'Regents Pass Rate - June','% of cohort - august': 'Regents Pass Rate - August','ontrack_year1_2013': 'Graduation Ontrack Rate - 2013', 'graduation_rate_2013': 'Graduation Rate - 2013', 'college_career_rate_2013': 'College Career Rate - 2013', 'student_satisfaction_2013': 'Student Satisfaction Rate - 2013','ontrack_year1_2012': 'Graduation Ontrack Rate - 2012', 'graduation_rate_2012': 'Graduation Rate - 2012', 'college_career_rate_2012': 'College Career Rate - 2012', 'student_satisfaction_2012': 'Student Satisfaction Rate - 2012'}, inplace=True)

#remove commas and unnecessary "the" in school names
school_database['school_name'] = school_database['school_name'].str.replace(',','')
school_database['school_name'] = school_database['school_name'].str.replace('The','')
school_database['school_name'] = school_database['school_name'].str.replace('the','')

#remove % signs from columns that contain percentages and are stored as strings
school_database.ix[:,school_database.dtypes==object] = school_database.ix[:,school_database.dtypes==object].apply(lambda s:s.str.replace('%', ""))
#convert those columns to numeric type
school_database = school_database.convert_objects(convert_numeric=True)

#initialize GoogleV3 API for geolocation
geolocator = GoogleV3()

#define function that calculates coordinates based on the address and city columns
def get_coordinates(df):
	school_location = geolocator.geocode(df['address']+','+df['city'],timeout=10)
	school_coordinates = (school_location.latitude,school_location.longitude)
	return school_coordinates

#create column that contains geopy coordinates
school_database['coordinates'] = school_database.apply(get_coordinates,axis=1)

#remove schools with no performance data
school_database.dropna(thresh=(len(school_database.columns) - 17), axis=0,inplace=True)

#write the dataframe to a csv
school_database.to_csv('database.csv')

