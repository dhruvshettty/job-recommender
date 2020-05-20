# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 13:47:19 2020

@author: Shiva
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import csv


dataset = pd.read_csv('ALL_JOBS.csv')

# Renaming the column
dataset.rename(columns={"experience(in yrs)": "experience_yrs"},inplace=True)

#Select features
features = ['title','location','experience_yrs']

dataset['experience_yrs'] = dataset['experience_yrs'].apply(str)

#Create a column in DF which combines all selected features
def combine_features(row):
    return row['title']+" "+row['location']+" "+row['experience_yrs']
dataset["combined_features"] = dataset.apply(combine_features,axis=1)

#Create count matrix from this new combined column
cv = CountVectorizer()
count_matrix = cv.fit_transform(dataset["combined_features"])

#Compute the Cosine Similarity based on the count_matrix
cosine_sim = cosine_similarity(count_matrix)

#Features requested by the user
User_job='Data Scientist'
User_loc='Bengaluru'
User_exp='5'

def get_job_from_index(index):
 	return dataset[dataset.index == index]["company"].values[0],dataset[dataset.index == index]["title"].values[0],dataset[dataset.index == index]["location"].values[0],dataset[dataset.index == index]["experience_yrs"].values[0]
def get_index_from_job(title,location,experience_yrs):
 	return dataset[dataset.title == title]["index"].values[0]

#Get index of this job from its choice
User_choice= get_index_from_job(User_job,User_loc,User_exp)
jobs_available = list(enumerate(cosine_sim[User_choice]))

#Get a list of similar jobs in descending order of similarity score
sorted_jobs_available= sorted(jobs_available,key=lambda x:x[1],reverse=True)



#Print the details of first 5 jobs
i=0
with open('Result.csv','w') as file:
    csv_output = csv.writer(file)
    csv_output.writerow(['company','title', 'city', 'exp'])
    for job in sorted_jobs_available:    
        data=get_job_from_index(job[0])
        csv_output.writerow(data)
        i=i+1
        if i>10:
            break

with open('cosine_result.csv','w') as file1:
    csv_output = csv.writer(file1)
    csv_output.writerow(cosine_sim)

