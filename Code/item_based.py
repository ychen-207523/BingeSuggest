#!/usr/bin/python
# -*- coding: utf-8 -*-
# Importing the required modules
import pandas as pd
import numpy as np
import time
import sys
import warnings

# To make sure warnings are filtered out
warnings.filterwarnings("ignore")
col_name = ['user_id', 'item_id', 'ratings', 'timestamp']
# Reading from input csv files and storing in data frames
df = pd.read_csv('../SE21-project/data/ratings.csv')
movies = pd.read_csv('../SE21-project/data/movies.csv')
df = pd.merge(df, movies, on='movieId')
avg_rating_df = pd.DataFrame(df.groupby('title')['rating'].mean())
avg_rating_df['no_of_ratings'] = df.groupby('title')['rating'].count()
avg_rating_df.head()
um_rating = df.pivot_table(index='userId', columns='title',
                           values='rating')
rec_mov = pd.DataFrame()

# Recommend function to output movies according to correlation 
# to the movies present in database
def recommend(userID):
    global rec_mov
    user_rating = []
    for i in um_rating.columns:
        if um_rating[i][userID] >= 4:# Picking rating >4 movies
            user_rating.extend([i])

    user_rating_final = []
    for movie in user_rating:  # picking movies with >100 ratings
        if avg_rating_df.loc[movie]['no_of_ratings'] > 100:
            user_rating_final.extend([movie])

    rec = pd.DataFrame()
    rec = []
    for i in user_rating_final:
        rating = um_rating[i]
        similar = um_rating.corrwith(rating)
        corr = pd.DataFrame(similar, columns=['correlation'])
        corr.dropna(inplace=True)
        for j in corr.index:
            # Correlation is taken as 0.95 and not watched
            if corr.loc[j]['correlation'] >= 0.95 and j not in rec and j \
               not in user_rating:
                rec.extend([j])
                r = {'movie': [j],
                     'correlation': [round(corr.loc[j]['correlation'], 2)]}
                record = pd.DataFrame(data=r)
                rec_mov = rec_mov.append(record, ignore_index=True)
                rec_mov = rec_mov.sort_values(by=['correlation'],
                    ascending=False)
    return (user_rating, rec_mov['movie'])

userID = int(sys.argv[1])
if len(sys.argv) > 2:
    print ('Error:Provide one user ID at a time as input on the command line!')
    sys.exit(1)
if userID > 610:
    print ('Error: Wrong user ID!')
    sys.exit(1)

(watched, rec) = recommend(547)
rec_list = []
for y in rec:
    rec_list.append(str(y))
final_rec_list = []
for z1 in rec_list:
    print(z1)
print('\n')
print('Number of movies recommended for this user : ' + str(len(rec_list)))
