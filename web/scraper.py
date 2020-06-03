# -*- coding: utf-8 -*-
"""
Get supplementary images from google search module

Programmer: Aleksei Seliverstov <alexseliverstov@yahoo.com>
"""
# import faster_than_requests as fr
import requests  # todo remove requests
from bs4 import BeautifulSoup
import secret
import sys  # todo remove

_google_url = 'https://www.google.com/search?q={}&client=opera&hs=cTQ&source=lnms&tbm=isch&sa=X&ved' \
              '=0ahUKEwig3LOx4PzKAhWGFywKHZyZAAgQ_AUIBygB&biw=1920&bih=982 '

_imagenet_url = 'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid={}'

_bing_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"


def g_supply_images(keyword):
    """
    Get list of supplementary images from google search by keyword
    """
    url = _google_url.format(keyword)

    # print(fr.get2str(url), requests.get(url).text, file=sys.stdout, flush=True)

    bs = BeautifulSoup(requests.get(url).text, 'html.parser')

    images = [i.get('src') for i in bs.find_all('img')[:10]]
    print(images[:5])
    return images[:5]


def bing_suppy_images(keyword):
    """
    Get list of supplementary images from bing search by keyword
    """
    headers = {'Ocp-Apim-Subscription-Key': secret.subscription_key}
    params = {'q': keyword, 'license': 'public', 'imageType': 'photo'}

    response = requests.get(_bing_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    thumbnail_urls = [img['thumbnailUrl'] for img in search_results['value'][:16]]
    print(thumbnail_urls, file=sys.stdout, flush=True)
    return thumbnail_urls


def i_supply_images(category_id):
    """
    Get list of images from image-net by category_id
    """
    url = _imagenet_url.format(category_id)
    # todo catch and format all exceptions
    # print('FR:', fr.get2str(url)[:40], 'REQ:', requests.get(url).text[:40], file=sys.stdout, flush=True)
    # print(fr.get2str(url) == requests.get(url).text, file=sys.stdout, flush=True)

    return requests.get(url).text.splitlines()
