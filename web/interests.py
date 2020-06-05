# -*- coding: utf-8 -*-
"""
Facebook API interaction module

Programmer: Aleksei Seliverstov <alexseliverstov@yahoo.com>
"""
import secret
import word2vec
import requests
# import faster_than_requests as fr
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

        Uses a fast requests library, faster_than_requests
        """
        url = self.__url.format(category, secret.token)
        try:
            # r = fr.get2str(url)
            r = requests.get(url).text
            r = json.loads(r)
            json_data = r['data']
        except Exception:
            # any error caught while reading from the web, returning no ad_interests
            return []

        ad_interests = [[jd['name'], jd['path']] for jd in json_data]
        return ad_interests

    def get_annotations(self, categories, recursive=False):
        """
        Get a list of annotations to a list of categories using Facebook API.

        Optional keyword arguments:
        recursive:  a boolean indicating whether categories should be looked up recursively if no annotations are found
        """
        annotations = []
        for category in categories:
            ad_interests = self.__get_ad_interests(category)
            if recursive and len(ad_interests) < 1:
                for c in category.split():
                    annotations += vectoriser.sort_with_f(category, self.__get_ad_interests(c), lambda x: x[0])
            else:
                annotations += vectoriser.sort_with_f(category, ad_interests, lambda x: x[0])
                # todo error prone
        return annotations

    def __new__(cls):
        """
        Declare this class as singleton

        This method is initiated before __init__ and check whether an instance of this class already exists
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(FacebookRequest, cls).__new__(cls)
        return cls.instance
