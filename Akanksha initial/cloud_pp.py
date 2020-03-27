# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 16:04:01 2020

@author: Akanksha
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import chain

df = pd.read_csv('cloud_computing.csv')

def chainer(s):
    return list(chain.from_iterable(s.str.split(',')))

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

#Dealing with multivalued attr in 'location'
# calculate lengths of splits
lens = df['location'].str.split(',').map(len)

# create new df, repeating or chaining as appropriate using numpy.repeat
# and itertools.chain
new_df = pd.DataFrame({'title': np.repeat(df['title'], lens),
                    'location': chainer(df['location']),
                    'company': np.repeat(df['company'], lens),
                    'salary': np.repeat(df['salary'], lens),
                    'experience': np.repeat(df['experience'], lens),
                    'description': np.repeat(df['description'], lens),
                    'keywords': np.repeat(df['keywords'], lens),
                    'trending': np.repeat(df['trending'], lens),
                    'sponsored': np.repeat(df['sponsored'], lens),
                    'salary_pp': np.repeat(df['salary_pp'], lens),
                    'experience_pp(in yrs)': np.repeat(df['experience_pp(in yrs)'], lens)
                    })


# Replacing the data "(...)" with ""
new_df['location'] = new_df['location'].str.replace(r"\(.*\)","")

# Replacing the data " xyz" with "xyz"
new_df['location'] = new_df['location'].str.replace(r" ","")
new_df['location'] = new_df['location'].str.replace(r"DelhiNCR","Delhi")
new_df['location'] = new_df['location'].str.replace(r"NaviMumbai","Mumbai")
new_df['location'] = new_df['location'].str.replace(r"BhubaneswarBhubaneswar","Bhubaneswar")
new_df['location'] = new_df['location'].str.replace(r"MohaliPunjab","Mohali")
new_df['location'] = new_df['location'].str.replace(r"GurgaonHaryana","Gurgaon")


new_df.drop(['experience'] , axis='columns', inplace=True)

new_df.to_csv('DS_NewData.csv',index=False)


#works if there is one column dependent on the modified one
"""# Step 1
# We start with creating a new dataframe from the series with title as the index
new_df = pd.DataFrame(df.location.str.split(',').tolist(), index=df.title).stack()

# Step 2
# We now want to get rid of the secondary index
# To do this, we will make title as a column (it can't be an index since the values will be duplicate)
new_df = new_df.reset_index([(0, 'title'),(1, 'company'),(2, 'salary'),(3,'experience'),(4,'description')
                            (5, 'keywords'),(6, 'trending'),(7, 'sponsored')
                            (8, 'salary_pp'),(9, 'experience_pp(in yrs)')])
# Step 3
# The final step is to set the column names as we want them
new_df.columns = ['title', 'location_pp']
"""
