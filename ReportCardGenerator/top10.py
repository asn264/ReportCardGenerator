#import relevant modules/classes
from School import *
from utilities import *

#import libraries used
import sys
import numpy as np

#array containing valid features that the user can choose from to create a top 10 ranking
valid_features = ['Num of SAT Test Takers','SAT Critical Reading Avg',
'SAT Math Avg', 'SAT Writing Avg', 'Regents Pass Rate - June',
 'Regents Pass Rate - August', 'Graduation Ontrack Rate - 2013',
 'Graduation Rate - 2013', 'College Career Rate - 2013', 'Student Satisfaction Rate - 2013','Graduation Ontrack Rate - 2012',
 'Graduation Rate - 2012', 'College Career Rate - 2012', 'Student Satisfaction Rate - 2012']

#array containing weights that are accepted by the program
valid_weights = np.arange(1,101)

def prompt_for_initial_feature():
	'''prompts the user to input a feature along with an integer weight between 1 and 100, separated by a comma'''

	return raw_input("\nEnter a feature followed by an integer weight between 1 and 100, separated by a comma: ")

def prompt_for_additional_feature():
	'''prompts the user to input another feature along with an integer weight between 1 and 100, separated by a comma'''

	return raw_input("\nEnter another feature followed by an integer weight between 1 and 100, separated by a comma. Type finish to calculate the top 10: ")


def validate_feature(input,current_features):
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

		if feature not in valid_features:
			print "\nInvalid feature"
			return None

		if feature in current_features: #check that a feature isn't being repeated
			print "\nWe already have a weight for that feature"
			return None

		try: #check that the weight is an integer
			weight = int(weight)
		except ValueError:
			print "\nWeight must be an integer"
			return None

		if int(weight) not in valid_weights:
			print "\nInvalid weight"
			return None

		return [feature,int(weight)]

def get_features():
	'''creates a list of valid features and valid weights by prompting the user for them and validating them'''

	features=[]
	weights=[]
	
	feature_weight_pair = validate_feature(prompt_for_initial_feature(),features)

	#while the user has not typed finish, which is signaled by a -1, we prompt for additional features/weights
	while feature_weight_pair!=-1:
		if feature_weight_pair is not None: #if both the feature and weight are valid
			feature,weight=feature_weight_pair
			#append feature and weight
			features.append(feature)
			weights.append(weight)

		if len(features)==0:
			feature_weight_pair = validate_feature(prompt_for_initial_feature(),features)
		else:
			feature_weight_pair = validate_feature(prompt_for_additional_feature(),features)

	return features,weights

def get_top10_schools():
	'''gets valid features and weights from the user and then finds the 10 schools with the highest score
	with respect to the features and weights given. A list of the 10 school objects is returned'''

	features,weights = get_features()
	names = calculate_top10(features,weights)

	#instantiate each school object and store all of the schools we want in a list
	schools=[]
	for name in names:
		schools.append(School(name))

	return schools

def calculate_top10(features,weights):
	'''calculates the top 10 schools based on the input features and weights. returns a list of the 10 school names'''

	database_copy = school_database

	#normalize data
	database_copy[valid_features] = database_copy[valid_features].apply(lambda x: (x - x.mean()) / (x.max() - x.min()))

	#compute score of each school
	database_copy['score']=0
	for i in range(0,len(features)):
		database_copy['score']+=database_copy[features[i]]*weights[i]

	#sort by score
	database_copy.sort('score',ascending=False,inplace=True)

	#return the names of the top 10 schools
	return database_copy['school_name'][:10].tolist()


