#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Get supplementary images from search engines module.

__author__ = "Aleksei Seliverstov"
__license__ = "MIT"
__email__ = "alexseliverstov@yahoo.com"
"""
import requests
from web import logger, secret

_imagenet_url = 'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid={}'

_bing_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"


def bing_suppy_images(keyword, number_of_images):
    """
    Get list of supplementary images from bing search by keyword
    """
    headers = {'Ocp-Apim-Subscription-Key': secret.subscription_key}
    params = {'q': keyword, 'license': 'public', 'imageType': 'photo'}
    try:
        response = requests.get(_bing_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        logger.info('Got a list of images from Bing.')
        return [img['thumbnailUrl'] for img in search_results['value'][:number_of_images]]
    except requests.exceptions.RequestException as e:
        # any error caught while reading from the web, returning no images
        logger.exception(e)
        return []


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
