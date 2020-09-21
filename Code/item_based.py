import pandas as pd
import numpy as np
import time
col_name = ['user_id','item_id','ratings','timestamp']
df = pd.read_csv('ratings.csv')
movies = pd.read_csv('movies.csv')
df = pd.merge(df,movies,on='movieId')
# print(df)
# print(type(df))
avg_rating_df = pd.DataFrame(df.groupby('title')['rating'].mean())
avg_rating_df['no_of_ratings'] = df.groupby('title')['rating'].count()
avg_rating_df.head()
um_rating = df.pivot_table(index='userId',columns='title',values='rating')
print(um_rating.to_string())
rec_mov = pd.DataFrame()
def recommend(userID):
    global rec_mov
    user_rating = []
    for i in um_rating.columns:  # picking up movies rated well by particular user
        if um_rating[i][userID] >= 4:
            user_rating.extend([i])
            
    user_rating_final = []
    for movie in user_rating:  # picking movies with >100 ratings
        if avg_rating_df.loc[movie]['no_of_ratings'] > 100:
            user_rating_final.extend([movie])
    
    rec = pd.DataFrame()
    rec = []
    for i in user_rating_final:
        rating = um_rating[i]
        print(rating)
        similar = um_rating.corrwith(rating)
        corr = pd.DataFrame(similar,columns=['correlation'])
        #print(corr.to_string())
        corr.dropna(inplace=True)
        for j in corr.index:
            if corr.loc[j]['correlation'] >= 0.95 and j not in rec and j not in user_rating:
                rec.extend([j])
                r = {'movie': [j], 'correlation': [round(corr.loc[j]['correlation'],2)]}
                record = pd.DataFrame(data=r)
                rec_mov = rec_mov.append(record, ignore_index = True)
                rec_mov = rec_mov.sort_values(by=['correlation'], ascending=False)
    return user_rating, rec_mov['movie'] #returning a dataframe of recommended movies with correlation

watched, rec = recommend(547)
#print(rec.to_string())
print(watched)
