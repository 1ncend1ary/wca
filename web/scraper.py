# -*- coding: utf-8 -*-
"""
Get supplementary images from google search module

Programmer: Aleksei Seliverstov <alexseliverstov@yahoo.com>
"""
import requests
from bs4 import BeautifulSoup
import web.secret as secret
from web import logger

_google_url = 'https://www.google.com/search?q={}&client=opera&hs=cTQ&source=lnms&tbm=isch&sa=X&ved' \
              '=0ahUKEwig3LOx4PzKAhWGFywKHZyZAAgQ_AUIBygB&biw=1920&bih=982 '

_imagenet_url = 'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid={}'

_bing_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"


def g_supply_images(keyword):
    """
    WARNING: DEPRECATED

    Get list of supplementary images from google search by keyword
    """
    url = _google_url.format(keyword)

    bs = BeautifulSoup(requests.get(url).text, 'html.parser')

    images = [i.get('src') for i in bs.find_all('img')[:10]]
    return images[:5]


def bing_suppy_images(keyword, number_of_images):
    """
    Get list of supplementary images from bing search by keyword
    """
    headers = {'Ocp-Apim-Subscription-Key': secret.subscription_key}
    params = {'q': keyword, 'license': 'public', 'imageType': 'photo'}

    response = requests.get(_bing_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    logger.info('Got a list of images from Bing.')
    return [img['thumbnailUrl'] for img in search_results['value'][:number_of_images]]


def i_supply_images(category_id):
    """
    Get list of images from image-net by category_id
    """
    url = _imagenet_url.format(category_id)

    try:
        logger.info('Got a list of images from image-net.')
        return requests.get(url).text.splitlines()
    except requests.exceptions.RequestException as e:
        # any error caught while reading from the web, returning no images
        logger.exception(e)
        return []


def supply_images(category_id, category_names):
    """
    Get list of images from both Bing and image-net

    :returns: list of images
    """
    images = i_supply_images(category_id)
    for cn in category_names:
        images = bing_suppy_images(cn, 2) + images
    return images
