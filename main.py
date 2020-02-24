from recommendations_engine import *

usersDF = pd.read_csv('../../../Downloads/myanimelist/users_cleaned.csv')
animesDF = pd.read_csv('../../../Downloads/myanimelist/animesDF.csv')
scoresDF = pd.read_csv('../../../Downloads/myanimelist/scores_sample.csv')

anime_ids = np.sort(animesDF.anime_id.unique())
