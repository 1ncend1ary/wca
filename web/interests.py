#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Facebook API interaction module.

__author__ = "Aleksei Seliverstov"
__license__ = "MIT"
__email__ = "alexseliverstov@yahoo.com"
"""
from web import word2vec, secret, logger
import requests
import json

vectoriser = word2vec.Vectoriser()


class FacebookRequest:
    """
    Facebook API requests handling class
    """
    __url = 'https://graph.facebook.com/search?type=adinterest&q=[\'{}\']&limit=10000&locale=en_US&access_token={}'

    def __get_ad_interests(self, category):
        """
        Fetch advertisment interests via Facebook API method

        :returns: set of tuples containing interests
        """
        url = self.__url.format(category, secret.token)
        try:
            r = json.loads(requests.get(url).text)
            json_data = r['data']
            ad_interests = {(jd.get('name', ''), jd.get('topic', 'Unknown category')) for jd in json_data}
            return ad_interests
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            # any error caught while reading from the web, returning no ad_interests
            logger.exception(e)
            return set()

    def get_annotations(self, categories):
        """
        Get a list of annotations to a list of categories using Facebook API.

        All annotations are unique.

        :param categories: list of categories that should be annotated
        :returns: list of annotations sorted by distance from categories
        """
        ad_interests = set()
        for category in categories:
            ad_interests.update(self.__get_ad_interests(category))

        ad_interests = list(ad_interests)
        annotations = vectoriser.sort_with_f(categories, ad_interests, lambda x: x[0])
        logger.info('Got a list of annotations using Facebook.')
        return annotations

    def __new__(cls):
        """
        Declare this class as singleton

        This method is initiated before __init__ and check whether an instance of this class already exists
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(FacebookRequest, cls).__new__(cls)
        return cls.instance
