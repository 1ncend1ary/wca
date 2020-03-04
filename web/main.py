from flask import Flask, render_template, request, redirect, url_for, flash
from forms import LoginForm
import requests
import database
import sys
import time
from itertools import compress
from multiprocessing import Pool
import logging
import os
import interests
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# app.config.from_object('config.Config')

# https://medium.com/@interestexplorerio/how-to-use-the-facebook-marketing-api-to-reveal-1000s-of-interests-that-are-hidden-in-the-facebook-e20ee5bdcd17
logging.basicConfig(filename='main.log',
                    format='%(asctime)s - %(process)d - %(levelname)s - %(message)s', level=logging.DEBUG)

# def url_is_alive(url):
#     """
#     Checks that a given URL is reachable.
#     :param url: A URL
#     :rtype: bool
#     """
#     rr = urllib.request.Request(url)
#     rr.get_method = lambda: 'HEAD'
#
#     try:
#         urllib.request.urlopen(rr)
#         return True
#     except Exception:
#         return False


@app.route("/", methods=['GET', 'POST'])
def index():
    # todo post method form resubmission
    if request.method == 'POST':
        aa = request.form.get('category_id')
        inter = request.form.getlist('checkbox')
        print(inter, aa, file=sys.stdout, flush=True)
        if len(inter) > 0:
            database.write_interests(aa, inter)
        return redirect(url_for('index'))
        # return 'Done'

    element = database.fetch_new_entry()
    # todo use `index_of_parent_category`
    category_id = element.get('category_id')
    category_name_string = element.get('category name')
    category_names = [x.strip() for x in category_name_string.split(',')]

    start = time.time()
    categories = interests.parse_categories(category_names, include_sub=False)
    logging.debug('Get categories: ' + str(time.time() - start))

    start = time.time()
    r = requests.get('http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=' + category_id)
    images = r.text.splitlines()[:20]
    logging.debug('Get images:' + str(time.time() - start))

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
    return render_template("index.html", words=category_names, images=images, categories=set(categories[:10]),
                           category_id=category_id)


@app.route("/contacts", methods=['GET', 'POST'])
def contacts():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))

    return render_template('contacts.html', title='Sign In', form=form)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
