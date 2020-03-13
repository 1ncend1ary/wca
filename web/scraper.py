# -*- coding: utf-8 -*-
"""
Get supplementary images from google search module

Programmer: Aleksei Seliverstov <alexseliverstov@yahoo.com>
"""
import faster_than_requests as fr
from bs4 import BeautifulSoup

_google_url = 'https://www.google.com/search?q={}&client=opera&hs=cTQ&source=lnms&tbm=isch&sa=X&ved' \
              '=0ahUKEwig3LOx4PzKAhWGFywKHZyZAAgQ_AUIBygB&biw=1920&bih=982 '

_imagenet_url = 'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid={}'


def g_supply_images(keyword):
    """
    Get list of supplementary images from google search by keyword
    """
    url = _google_url.format(keyword)
    bs = BeautifulSoup(fr.get2str(url), 'html.parser')

    images = [i.get('src') for i in bs.find_all('img')[:10]]
    print(images[:5])
    return images[:5]


def i_supply_images(category_id):
    """
    Get list of images from image-net by category_id
    """
    url = _imagenet_url.format(category_id)
    return fr.get2str(url).splitlines()
