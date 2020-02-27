import pandas as pd
import numpy as np
from utils import *

animesDF = pd.read_csv('animesDF.csv')
anime_ids = np.sort(animesDF.anime_id.unique())
similarity_table = np.load('similarity_table.npy')

'''
find user's shows that exist in MAL dataset, as some shows aired after dataset was created
'''
def user_shows_in_db(userDF, animesDF):
    return userDF[userDF[['series_animedb_id']].isin(animesDF.anime_id.unique()).any(1)]

'''
finds top matches based on shows similarities
'''
def top_matches(similarity_table, user_show_scores, anime_ids):
    result = np.empty((0,2), int)
    user_shows = user_show_scores[:, 0]
    user_scores = user_show_scores[:, 1]
    rows = np.where(np.isin(anime_ids, user_shows))[0]
    columns = np.setdiff1d(np.arange(len(anime_ids)), rows)
    matches_table = similarity_table[rows][:, columns]
    for i in range(len(columns)):
        if np.sum(matches_table[:, i]) > 0:
            result = np.append(result, [[int(anime_ids[columns[i]]), np.dot(matches_table[:, i], user_scores)/np.sum(matches_table[:, i])]], axis=0)
        else:
            result = np.append(result, [[int(anime_ids[columns[i]]), 0]], axis=0)
    return result[result[:,1].argsort()][::-1]

def show_names(matches):
    data = {'anime_id': [], 'pred_score':[]}
    for show in matches:
        try:
            if show[1] >= 7:
                data['anime_id'].append(int(show[0]))
                data['pred_score'].append(show[1])
        except:
            pass
    return data

def get_recommendations_dataframe(userDF, animesDF, similarity_table, anime_ids):
    user_rec = show_names(top_matches(similarity_table, np.array(user_shows_in_db(userDF, animesDF)), anime_ids))
    user_recDF = pd.DataFrame(data=user_rec)
    resultDF = pd.merge(user_recDF, animesDF, on=['anime_id'])
    return resultDF
