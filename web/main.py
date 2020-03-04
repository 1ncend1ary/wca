from flask import Flask, render_template, request
import requests
import database
import sys
import time
import urllib.request
import secret
from itertools import compress
from multiprocessing import Pool
import logging

app = Flask(__name__)

# https://medium.com/@interestexplorerio/how-to-use-the-facebook-marketing-api-to-reveal-1000s-of-interests-that-are-hidden-in-the-facebook-e20ee5bdcd17
logging.basicConfig(filename='main.log', filemode='w',
                    format='%(asctime)s - %(process)d - %(levelname)s - %(message)s')

# todo: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms


def get_interests(category):
    r = requests.get('https://graph.facebook.com/search?type=adinterest&q=[\'' +
                     category +
                     '\']&limit=10000&locale=en_US&access_token=' + secret.token)
    data = r.json()['data']
    interests = [x['name'] for x in data]
    subcategories = category.split()
    if len(subcategories) > 1:
        for subcategory in subcategories:
            interests += get_interests(subcategory)
    return interests


def url_is_alive(url):
    """
    Checks that a given URL is reachable.
    :param url: A URL
    :rtype: bool
    """
    rr = urllib.request.Request(url)
    rr.get_method = lambda: 'HEAD'

    try:
        urllib.request.urlopen(rr)
        return True
    except Exception:
        return False


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # print('get post request', file=sys.stdout, flush=True)
        # logging.info('adfadsasdfs')
        print(request.form.getlist('checkbox'), file=sys.stdout, flush=True)
        # return 'Done'

    element = database.fetch_new_entry()
    category_id = element.get('category_id')
    category_name_string = element.get('category name')
    category_names = [x.strip() for x in category_name_string.split(',')]

    start = time.time()
    categories = []
    for category_name in category_names:
        categories += get_interests(category_name)
    print('Get categories:', time.time() - start, file=sys.stdout, flush=True)

    start = time.time()
    r = requests.get('http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=' + category_id)
    images = r.text.splitlines()[:10]
    print('Get images:', time.time() - start, file=sys.stdout, flush=True)

    # start = time.time()
    # try:
    #     with Pool(5) as p:
    #         booleans = p.map(url_is_alive, images)
    # except Exception:
    #     print('WOWOOWOWO you all failed', file=sys.stdout, flush=True)
    #
    # images = list(compress(images, booleans))
    # print('Filter images:', time.time() - start, file=sys.stdout, flush=True)

    # images = [images[i: i + 3] for i in range(0, len(images), 3)]
    return render_template("index.html", words=category_names, images=images, categories=set(categories[:10]))


@app.route("/contacts")
def contacts():
    return render_template("contacts.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
