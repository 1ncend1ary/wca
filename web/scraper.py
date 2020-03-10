import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os


def download_google(word):
    url = 'https://www.google.com/search?q=' + word + '&client=opera&hs=cTQ&source=lnms&tbm=isch&sa=X&ved' \
                                                      '=0ahUKEwig3LOx4PzKAhWGFywKHZyZAAgQ_AUIBygB&biw=1920&bih=982 '
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')

    links = []
    for raw_img in soup.find_all('img')[:10]:
        link = raw_img.get('src')
        links += link
    print(links[:5])
    return links[:5]
