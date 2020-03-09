import secret
import requests
import word2vec
import sys


# https://medium.com/@interestexplorerio/how-to-use-the-facebook-marketing-api-to-reveal-1000s-of-interests-that-are-hidden-in-the-facebook-e20ee5bdcd17
def get_interests(category):
    try:
        r = requests.get('https://graph.facebook.com/search?type=adinterest&q=[\'' +
                         category +
                         '\']&limit=10000&locale=en_US&access_token=' + secret.token)
    except requests.ConnectionError:
        print("Got connection error", file=sys.stdout, flush=True)
        return []
    data = r.json()['data']
    interests = [x['name'] for x in data]
    return interests


def parse_categories(category_names, include_sub=False):
    categories = []
    for category_name in category_names:
        interest = get_interests(category_name)
        if include_sub and len(interest) < 1:
            print("Parsing split interests:", file=sys.stdout, flush=True)
            for x in category_name.split():
                categories += word2vec.sort_interests(category_name, get_interests(x))
        else:
            print("Parsing 1 interest:", file=sys.stdout, flush=True)
            categories += word2vec.sort_interests(category_name, interest)
    return categories


# print(parse_categories(['coupons', 'marketing coupons']))
