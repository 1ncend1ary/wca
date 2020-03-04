import secret
import requests
import sys


def get_interests(category):
    r = requests.get('https://graph.facebook.com/search?type=adinterest&q=[\'' +
                     category +
                     '\']&limit=10000&locale=en_US&access_token=' + secret.token)
    data = r.json()['data']
    interests = [x['name'] for x in data]
    # subcategories = category.split()
    # if len(subcategories) > 1:
    #     for subcategory in subcategories:
    #         interests += get_interests(subcategory)
    return interests


def parse_categories(category_names, include_sub=False):
    categories = []
    for category_name in category_names:
        interest = get_interests(category_name)
        # print('Interest:', interest, file=sys.stdout, flush=True)
        if include_sub and len(interest) < 1:
            for x in category_name.split():
                # print('Sub Interest:', x, 'is:', get_interests(x), file=sys.stdout, flush=True)
                categories += get_interests(x)
        else:
            categories += interest
    return categories
