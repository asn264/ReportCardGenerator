import pandas as pd

school_database = pd.read_csv('database.csv')
school_names = pd.unique(school_database['school_name'].values.ravel())