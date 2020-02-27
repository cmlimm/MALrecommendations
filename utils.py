import pandas as pd
import requests
import bs4
import re

clear_HTML_re = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
def clear_HTML(text):
    return re.sub(clear_HTML_re, '', text)

def get_anime_page(id):
    url = 'https://myanimelist.net/anime/' + str(id) + '/'
    html = requests.get(url)
    soup = bs4.BeautifulSoup(html.text, features="lxml")
    return soup

def get_image_synopsis(id):
    soup = get_anime_page(id)
    image = soup.find('img', itemprop="image")['data-src']
    synopsis = clear_HTML(str(soup.find('span', itemprop="description")))
    return (image, synopsis)

'''
loads user's scores from MAL xml file converted to csv
'''
def load_user_list(path):
    userDF = pd.read_csv(path)
    return userDF[['series_animedb_id', 'my_score']][userDF['my_score']!=0]

genre_list = ['Action', 'Adventure', 'Cars', 'Comedy', 'Dementia', 'Demons', 'Drama', 'Ecchi', 'Fantasy', 'Game', 'Harem', 'Historical', 'Horror', 'Josei', 'Magic', 'Martial Arts', 'Mecha', 'Military', 'Music', 'Mystery', 'Parody', 'Police', 'Psychological', 'Romance', 'Samurai', 'School', 'Sci-Fi', 'Seinen', 'Shoujo', 'Shoujo Ai', 'Shounen', 'Shounen Ai', 'Slice of Life', 'Space', 'Sports', 'Super Power', 'Supernatural', 'Thriller', 'Vampire']
