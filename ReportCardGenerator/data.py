"""Author: Akash Shah(ass502)

This module contains a function and code used to load the necessary data from data frames and clean them. 
Then, they are all merged into one single database based on the unique school identification number (dbn).
An additional column which contains the coordinates of the address is calculated and added."""


import pandas as pd
import numpy as np

def loadDataframe(filename,relevant,columns,nullValues):
	"""function to load data from csv and do some basic cleaning"""

	data_df = pd.read_csv(filename)
	data_df.columns = [col.lower() for col in data_df.columns]
        
	#determine whether to keep each column in columns or drop each 
	if relevant:
		data_df = data_df[columns]
	else:
		data_df.drop(columns,axis=1,inplace=True)

	#set index to the unique school identification number
	data_df.set_index('dbn')
	#standardize null vlaues
	data_df.replace(nullValues,np.nan,inplace=True)

	return data_df


nullValues=['s','.','N/A']

schools = loadDataframe('data/DOE_High_School_Directory_2014-2015.csv',True,['dbn','school_name','primary_address_line_1','city'],nullValues)

sat_scores = loadDataframe('data/SAT_Results.csv',False,'school name',nullValues)

regents_performance = loadDataframe('data/Graduation_Outcomes_-_Class_Of_2010_-_Regents-based_Math-_ELA_APM_-_School_Level.csv',False,'name',nullValues)
regents_performance = regents_performance[regents_performance['demographic'] == 'All Students']
regents_performance.drop(['demographic'],axis=1,inplace=True)

school_performance = loadDataframe('data/DOE_High_School_Performance-Directory_2014-2015.csv',False,['quality_review_rating','quality_review_year','ontrack_year1_historic_avg_similar_schls','graduation_rate_historic_avg_similar_schls','college_career_rate_historic_avg_similar_schls','student_satisfaction_historic_avg_similar_schls'],nullValues)

#do a left join on the tables starting with school, on the dbn column which uniquely identifies the school
dfs = [schools,sat_scores,regents_performance,school_performance]
school_database = reduce(lambda left,right: pd.merge(left,right,how='left',on='dbn'),dfs)

#create column that contains geopy coordinates
geolocator = geocoders.GoogleV3()
coordinates=[]
for school in school_database['school_name']:
	address=school_database.primary_address_line_1.where(school_database.school_name == school).max()
	city = school_database.city.where(school_database.school_name == school).max()
	school_location = geolocator.geocode(address+','+city,timeout=10)
	school_coordinates = (school_location.latitude,school_location.longitude)
	coordinates.append(school_coordinates)
school_database['coordinates'] = coordinates

school_database.to_csv('database.csv')
school_database['school_name'].to_csv('school_names.csv')