from flask import Flask, render_template, request, redirect, url_for, flash
from forms import LoginForm
import requests
import database
import sys
import time
from itertools import compress
from multiprocessing import Pool
import logging
import interests
from config import Config
from flask_login import LoginManager, current_user, login_user

# todo -- naming conventions and docstrings


app = Flask(__name__)
app.config.from_object(Config)
# login = LoginManager(app)

logging.basicConfig(filename='main.log',
                    format='%(asctime)s - %(process)d - %(levelname)s - %(message)s', level=logging.DEBUG)


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

    element = database.fetch_new_entry()
    # todo use `index_of_parent_category`
    category_id = element.get('category_id')
    category_name_string = element.get('category name')
    category_names = [x.strip() for x in category_name_string.split(',')]

    start = time.time()
    try:
        categories = interests.parse_categories(category_names, include_sub=False)
    except requests.ConnectionError:
        print('Get exception in broad!!!: ', file=sys.stdout, flush=True)
        categories = []

    print('Get categories: ' + str(time.time() - start), file=sys.stdout, flush=True)

    start = time.time()
    try:
        r = requests.get('http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=' + category_id)
        images = r.text.splitlines()
    except requests.ConnectionError:
        print("Got connection error", file=sys.stdout, flush=True)
        images = []
    print('Get images:' + str(time.time() - start), file=sys.stdout, flush=True)

    return render_template("index.html", words=category_names, images=images[:40], categories=list(categories),
                           category_id=category_id)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#
#         if not database.validate_user(username=form.username.data, password=form.password.data):
#             flash('Invalid username or password')
#             return redirect(url_for('login'))
#         login_user(user, remember=form.remember_me.data)
#         return redirect(url_for('index'))
#     return render_template('login.html', title='Sign In', form=form)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
