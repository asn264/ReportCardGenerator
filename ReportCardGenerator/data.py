#! /data/anaconda/bin/python

import pandas as pd
import numpy as np

schools = pd.read_csv('data/DOE_High_School_Directory_2014-2015.csv')
relevant_cols = ['dbn','school_name','primary_address_line_1','city']
schools=schools[relevant_cols]
#dbn uniquely identifies schools
schools.set_index('dbn')

sat_scores = pd.read_csv('data/SAT_Results.csv')
sat_scores.columns = [col.lower() for col in sat_scores.columns]
sat_scores.set_index('dbn')
sat_scores.drop('school name',axis=1,inplace=True)
#null values in the original table are s
sat_scores.replace('s',np.nan,inplace=True)

regents_performance = pd.read_csv('data/Graduation_Outcomes_-_Class_Of_2010_-_Regents-based_Math-_ELA_APM_-_School_Level.csv')
regents_performance.columns = [col.lower() for col in regents_performance.columns]
regents_performance.set_index('dbn')
#filter table to only include stats for all students
regents_performance = regents_performance[regents_performance['demographic'] == 'All Students']
regents_performance.drop(['demographic','name'],axis=1,inplace=True)
#null values in the original table were s and .
regents_performance.replace(['s','.'],np.nan,inplace=True)

school_performance = pd.read_csv('data/DOE_High_School_Performance-Directory_2014-2015.csv')
school_performance.set_index('dbn')
school_performance.drop(['quality_review_rating','quality_review_year','ontrack_year1_historic_avg_similar_schls','graduation_rate_historic_avg_similar_schls','college_career_rate_historic_avg_similar_schls','student_satisfaction_historic_avg_similar_schls'],axis=1,inplace=True)
#null values in the original table were N/A
school_performance.replace('N/A',np.nan,inplace=True)

#do a left join on the tables starting with school, on the dbn column which uniquely identifies the school
dfs = [schools,sat_scores,regents_performance,school_performance]
school_database = reduce(lambda left,right: pd.merge(left,right,how='left',on='dbn'),dfs) 

school_database.to_csv('database.csv')
school_database['school_name'].to_csv('school_names.csv')
