# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 16:04:01 2020

@author: Akanksha
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('cloud_computing.csv')

#Dealing with multivalued attr in 'location'

# Step 1
# We start with creating a new dataframe from the series with title as the index
new_df = pd.DataFrame(df.location.str.split(',').tolist(), index=df.title).stack()

# Step 2
# We now want to get rid of the secondary index
# To do this, we will make title as a column (it can't be an index since the values will be duplicate)
new_df = new_df.reset_index([0, 'title'])

# Step 3
# The final step is to set the column names as we want them
new_df.columns = ['title', 'location_pp']


#to set the experience to the min req
df['experience_pp'] = df['experience'].str[:1]
#to change the 'none' values to 0
mymap = {'N':0}
df['experience_pp']= df['experience_pp'].map(lambda s: mymap.get(s) if s in mymap else s)
#rename experience column to mention time as yrs
df.rename(columns={"experience_pp": "experience_pp(in yrs)"},inplace=True)

#setting the unknown salaries to an average of the salary of a clound engineer in India
my_map = {'Not disclosed':780000}
df['salary_pp']= df['salary_pp'].map(lambda s: my_map.get(s) if s in my_map else s)

#dropping duplicate columns
#df.drop(['title'], axis=1, inplace=True)

horizontal_stack = pd.concat([new_df, df], axis=1)
