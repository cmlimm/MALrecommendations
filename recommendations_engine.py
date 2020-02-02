import pandas as pd
from math import sqrt
import datetime
import numpy as np

def get_user_scores(scoresDF, viewer):
    '''Return all user scores in pandas DataFrame.'''
    return scoresDF.loc[(scoresDF['username'] == viewer)]


def sim_pearson(scoresDF, anime1_id, anime2_id):
    '''Return the Pearson correlation coefficient for anime1 and anime2.'''
    scores_anime1DF = scoresDF[scoresDF.anime_id == anime1_id]
    scores_anime2DF = scoresDF[scoresDF.anime_id == anime2_id]
    # get the list of shared viewers
    shared_viewers = 0
    scores1 = []
    scores2 = []
    for index, row in scores_anime1DF.iterrows():
        viewer = get_user_scores(scores_anime2DF, row['username'])
        if not viewer.empty:
            shared_viewers += 1
            scores1.append(row['my_score'])
            scores2.append(int(viewer['my_score']))

    # if no ratings in common, return 0
    if shared_viewers == 0:
        return 0

    # add up all the preferences
    sum1 = sum(scores1)
    sum2 = sum(scores2)

    # sum up the squares
    sum1Sq = sum([pow(score, 2) for score in scores1])
    sum2Sq = sum([pow(score, 2) for score in scores2])

    # sum up the products
    pSum = sum([score1*score2 for score1, score2 in zip(scores1, scores2)])

    # calculate Pearson score
    num = pSum - (sum1 * sum2)/shared_viewers
    den = sqrt((sum1Sq - pow(sum1, 2)/shared_viewers) * (sum2Sq - pow(sum2, 2)/shared_viewers))
    if den == 0:
        return 0
    else:
        return num/den # between(-1, 1)


def get_similarity_table(scoresDF, anime_ids):
    '''Return similarity table - matrix NxN, N - number of animes.
    First row and first column - indexes of animes.
    a[i][j] - similarity of the shows with ids: anime_ids[i-1] and anime_ids[j-1].
    '''
    similarity_table = np.zeros((len(anime_ids)+1, len(anime_ids)+1))
    similarity_table[1:, 0] = anime_ids
    similarity_table[0, 1:] = anime_ids
    n = len(anime_ids)
    count = 0
    for anime1_id in anime_ids:
        for anime2_id in anime_ids:
            if anime1_id != anime2_id:
                similarity = sim_pearson(scoresDF, anime1_id, anime2_id)
                x = np.where(similarity_table == anime1_id)[0][1]
                y = np.where(similarity_table == anime2_id)[0][1]
                similarity_table[x][y] = similarity
                similarity_table[y][x] = similarity
        np.save('similarity_table', similarity_table)
        count += 1
        print('Processed {} out of {} animes :: {}'.format(count, n, datetime.datetime.now()))
    return similarity_table


def load_user_list(path):
    '''Return user scores from MAL xml file converted to csv in pandas DataFrame'''
    userDF = pd.read_csv(path)
    return userDF[['series_animedb_id', 'my_score']][userDF['my_score']!=0]


def user_shows_in_db(userDF, animesDF):
    '''Return user shows that exist in MAL dataset'''
    return userDF[userDF[['series_animedb_id']].isin(animesDF.anime_id.unique()).any(1)]


def top_matches(similarity_table, user_show_scores, n):
    '''
    Return top-n matches based on shows similarities in form of numpy array [anime_id, predicted_score].
    user_show_scores - numpy array [anime_id, score]

    '''
    result = np.empty((0,2), int)
    user_shows = user_show_scores[:, 0]
    user_scores = user_show_scores[:, 1]
    to_delete = []
    for show in user_shows:
        y = np.where(similarity_table == show)[0][1]
        to_delete.append(y)
    similarity_table = np.delete(similarity_table, to_delete, 1)
    to_delete = []
    for show in similarity_table[1:, 0]:
        if show not in user_shows:
            x = np.where(similarity_table == show)[0][1]
            to_delete.append(x)
    similarity_table = np.delete(similarity_table, to_delete, 0)
    for column in similarity_table.T[1:]:
        result = np.append(result, [[column[0], np.dot(column[1:], user_scores)/np.sum(column[1:])]], axis=0)
    return result[result[:,1].argsort()][::-1][:n]
