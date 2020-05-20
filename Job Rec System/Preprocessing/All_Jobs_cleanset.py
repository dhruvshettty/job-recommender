# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 10:54:41 2020

@author: Shiva
"""

import numpy as np
import pandas as pd
from itertools import chain

dataset = pd.read_csv('All_Jobs_data')

def chainer(s):
    return list(chain.from_iterable(s.str.split(',')))

# calculate lengths of splits
lens = dataset['location'].str.split(',').map(len)

# create new dataframe, repeating or chaining as appropriate using numpy.repeat
# and itertools.chain
res = pd.DataFrame({'title': np.repeat(dataset['title'], lens),
                    'location': chainer(dataset['location']),
                    'company': np.repeat(dataset['company'], lens),
                    'salary': np.repeat(dataset['salary'], lens),
                    'experience': np.repeat(dataset['experience'], lens),
                    'description': np.repeat(dataset['description'], lens),
                    'keywords': np.repeat(dataset['keywords'], lens),
                    'trending': np.repeat(dataset['trending'], lens),
                    'sponsored': np.repeat(dataset['sponsored'], lens)
                    })

# Replacing the data "(...)" with ""
res['location'] = res['location'].str.replace(r"\(.*\)","")
res['title'] = res['title'].str.replace(r"\(.*\)","")

# Replacing the data " xyz" with "xyz"
res['location'] = res['location'].str.replace(r" ","")

res['location'] = res['location'].str.replace(r"DelhiNCR","Delhi")
res['location'] = res['location'].str.replace(r"NaviMumbai","Mumbai")

# Drop a row by condition
res =res[res.location != 'India']
res =res[res.location != 'india']
res =res[res.location != '0']

# Delete duplicates if all the values of columns match
res = res.drop_duplicates()

# Considering only the first character of the values in 'experience' column
res['experience'] = res['experience'].str[:1]

# Renaming the column
res.rename(columns={"experience": "experience(in yrs)"},inplace=True)

#Deleting rows satisfying the specified condition
res = res.drop(res[(res.trending <= 0) & (res.sponsored > 0)].index)

# Dataframe to csv file
res.to_csv('ALl_Jobs_Data.csv',index=False)
