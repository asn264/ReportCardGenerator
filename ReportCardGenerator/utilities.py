import pandas as pd
import numpy as np

school_database = pd.read_csv('database.csv')
#Note there are no duplicates in this list. We cast it to lower-case so that we can build more flexibility in accepting user input with different capitalizations. 
school_names = school_database['school_name'].str.lower().values.ravel()