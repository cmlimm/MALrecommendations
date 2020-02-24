import pandas as pd
import requests
import bs4
import re

clear_HTML_re = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
def clear_HTML(text):
    return re.sub(clear_HTML_re, '', text)


recommendations = pd.read_csv('../../../Downloads/myanimelist/resultDF.csv')
title_list = list(recommendations['title'])

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
