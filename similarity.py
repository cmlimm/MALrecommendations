import pandas as pd
import math

def get_viewer(scoresDF, viewer):
    return scoresDF.loc[(scoresDF['username'] == viewer)]


# change to numpy arrays??
def sim_pearson(scores, anime1_id, anime2_id):
    '''Return the Pearson correlation coefficient for anime1 and anime2.'''
    scores_anime1 = scores[scoresDF.anime_id == anime1_id]
    scores_anime2 = scores[scoresDF.anime_id == anime2_id]
    # get the list of shared viewers
    shared_viewers = 0
    scores1 = []
    scores2 = []
    for index, row in scores_anime1.iterrows():
        viewer = get_viewer(scores_anime2, row['username'])
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
