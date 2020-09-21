import pandas as pd
import numpy as np
import time
import re
import sys
import warnings

warnings.filterwarnings("ignore")
col_name = ['user_id','item_id','ratings','timestamp']
df = pd.read_csv('ratings.csv')
movies = pd.read_csv('movies.csv')
df = pd.merge(df,movies,on='movieId')
avg_rating_df = pd.DataFrame(df.groupby('title')['rating'].mean())
avg_rating_df['no_of_ratings'] = df.groupby('title')['rating'].count()
avg_rating_df.head()
um_rating = df.pivot_table(index='title',columns='userId',values='rating')
rec_mov = pd.DataFrame()
def recommend(userID):
    user_movies=[]
    for k in range(len(um_rating[userID])):
            if(str(um_rating[userID].iloc[k])!="nan"):
                user_movies.append(um_rating[userID].index[k])
    rec = pd.DataFrame()
    rec = []
    rating = um_rating[userID]
    similar = um_rating.corrwith(rating)
    corr = pd.DataFrame(similar,columns=['correlation'])
    corr.dropna(inplace=True)
    movie_list=[]
    for j in corr.index:
        if corr.loc[j]['correlation'] >= 0.95 and j not in rec:
            rec.extend([j])
    for m in rec:        
        for k in range(len(um_rating[m])):
            if(um_rating[m].iloc[k]>4 and um_rating[m].index[k] not in user_movies):
                movie_list.append(um_rating[m].index[k])
    return set(movie_list)  
    
userID = int(sys.argv[1])
if len(sys.argv) > 2:
    print ('Error: Provide one user ID at a time as input on the command line!')
    sys.exit(1)
if userID > 610:
    print ('Error: Wrong user ID!')
    sys.exit(1)

rec= recommend(userID)
for z in rec:
    print(z)
print("\n")
print("Number of movies recommended for this user : "+str(len(rec)))
