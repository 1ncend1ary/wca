import secret
import requests
import word2vec
import sys
import faster_than_requests as fast_requests
import json


# import http.client

# https://medium.com/@interestexplorerio/how-to-use-the-facebook-marketing-api-to-reveal-1000s-of-interests-that-are-hidden-in-the-facebook-e20ee5bdcd17
# interests_connection = http.client.HTTPConnection('graph.facebook.com')


def get_interests(category, quick=True):
    url = 'https://graph.facebook.com/search?type=adinterest&q=[\'' + category + '\']&limit=10000&locale=en_US' \
                                                                                 '&access_token=' + secret.token
    # if quick:
    data = []
    try:
        r = fast_requests.get2str(url)
        r = json.loads(r)
        data = r['data']
        print('Data is.....:', data, file=sys.stdout, flush=True)
    except Exception:
        print("----------Got exception---------- with:", category, file=sys.stdout, flush=True)
        # return []
    # else:
    #     data2 = []
    #     try:
    #         r = requests.get(url)
    #         data2 = r.json()['data']
    #         print('Data 22222 is.....:', data, file=sys.stdout, flush=True)
    #     except requests.ConnectionError:
    #         print("Got connection error", file=sys.stdout, flush=True)
    #         # return []
    #     print('Data equality 33333 is.....:', data == data2, file=sys.stdout, flush=True)
    interests = [x['name'] for x in data]
    return interests


def parse_categories(category_names, include_sub=False, quick=True):
    categories = []
    for category_name in category_names:
        interest = get_interests(category_name, quick)
        if include_sub and len(interest) < 1:
            print("Parsing split interests:", file=sys.stdout, flush=True)
            for x in category_name.split():
                categories += word2vec.sort_interests(category_name, get_interests(x, quick))
        else:
            print("Parsing 1 interest:", file=sys.stdout, flush=True)
            categories += word2vec.sort_interests(category_name, interest)
    return categories


# print(parse_categories(['coupons', 'marketing coupons']))
