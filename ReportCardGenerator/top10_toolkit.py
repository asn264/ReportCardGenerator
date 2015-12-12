'''
Authors: Akash Shah (ass502) and Aditi Nair (asn264)

This module contains the Top10_Toolkit class, an instance of which represents an iteration of top10 mode. 
In top10 mode, the user can provide features and weights that they care about. A customized report is 
generated containing the 10 schools with the highest score based on those features and weights.
'''

#import modules/classes
from school import *

#import libraries used
import sys
import numpy as np


class Top10_Toolkit(object):

	def __init__(self, school_database, school_names, valid_features):
		'''create instance of top10 mode, instance variables contain the relevant data'''

		self.school_database = school_database
		self.school_names = school_names
		self.valid_features = valid_features

	@staticmethod
	def prompt_for_initial_feature():
		'''prompts the user to input a feature along with an integer weight between 1 and 100, separated by a comma'''

		return raw_input("\nEnter a feature followed by an integer weight between 1 and 100, separated by a comma: ")

	@staticmethod
	def prompt_for_additional_feature():
		'''prompts the user to input another feature along with an integer weight between 1 and 100, separated by a comma'''

		return raw_input("\nEnter another feature followed by an integer weight between 1 and 100, separated by a comma. \nType finish to calculate the top 10: ")


	def validate_feature(self,input,current_features):
		'''validates user input of a feature and a weight'''

		if input.strip().lower() == 'quit':
			sys.exit()
		else:
			if input.strip().lower() == 'finish':
				if len(current_features) == 0: #if the user tries to calculate the top 10 without having input any valid features
					print "\nNeed to have at least one valid feature to calculate the top 10 schools."
					return None
				else:
					#signal that we have a valid list of features and weights, and we are ready to calculate the top 10
					return -1


			split_input = input.split(",")

			if len(split_input) != 2:
				print "\nInput does not consist of two parameters."
				return None

			feature,weight = split_input

			#check that the feature is a valid feature, ignoring case
			if feature.lower() not in [x.lower() for x in self.valid_features]:
				print "\nInvalid feature"
				return None

			#check that a feature isn't being repeated, ignoring case
			if feature.lower() in [x.lower() for x in current_features]:
				print "\nWe already have a weight for that feature"
				return None

			try: #check that the weight is an integer
				weight = int(weight)
			except ValueError:
				print "\nWeight must be an integer"
				return None

			#valid weights are integers between 1 and 100
			if int(weight) not in np.arange(1,101):
				print "\nInvalid weight"
				return None

			return [feature,int(weight)]

	def get_features(self):
		'''creates a list of valid features and valid weights by prompting the user for them and validating them'''

		features=[]
		weights=[]
		
		feature_weight_pair = self.validate_feature(self.prompt_for_initial_feature(),features)

		#while the user has not typed finish, which is signaled by a -1, we prompt for additional features/weights
		while feature_weight_pair!=-1:
			if feature_weight_pair is not None: #if both the feature and weight are valid
				feature,weight=feature_weight_pair

				#append feature and weight
				features.append(feature)
				weights.append(weight)

			if len(features)==0:
				feature_weight_pair = self.validate_feature(self.prompt_for_initial_feature(),features)
			else:
				feature_weight_pair = self.validate_feature(self.prompt_for_additional_feature(),features)

		return features,weights

	def get_top10_schools(self):
		'''gets valid features and weights from the user and then finds the 10 schools with the highest score
		with respect to the features and weights given. A list of the 10 school objects is returned'''

		print "\nThe following features are available to create a ranking metric: "
		print self.valid_features

		features,weights = self.get_features()
		names,scores = self.calculate_top10(features,weights)

		#instantiate each school object and store all of the schools we want in a list
		schools=[]
		for name in names:
			schools.append(School(self.school_database,self.school_names,name))

		return schools,[features,weights,scores]

	def calculate_top10(self,features,weights):
		'''calculates the top 10 schools based on the input features and weights. returns a list of the 10 school names'''

		#create local copy of our database
		database_copy = self.school_database.copy()

		#normalize data
		database_copy[self.valid_features] = database_copy[self.valid_features].apply(lambda x: (x - x.mean()) / (x.max() - x.min()))

		#change column names to lowercase
		database_copy.columns = [x.lower() for x in database_copy.columns]

		#compute score of each school
		database_copy['score']=0
		for i in range(0,len(features)):
			database_copy['score']+=database_copy[features[i].lower()]*weights[i]

		#sort by score
		database_copy.sort('score',ascending=False,inplace=True)

		#return the names and scores of the top 10 schools
		return database_copy['school_name'][:10].tolist(),database_copy['score'][:10].tolist()


