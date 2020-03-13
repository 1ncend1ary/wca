# -*- coding: utf-8 -*-
"""
Flask application main module

Programmer: Aleksei Seliverstov <alexseliverstov@yahoo.com>
"""
from flask import Flask, render_template, request, redirect, url_for, flash
import database
import interests
from config import Config
import scraper

app = Flask(__name__)
app.config.from_object(Config)

db = database.Categories()
requester = interests.FacebookRequest()


@app.route("/", methods=['GET', 'POST'])
def index():
    """
    Flask index page render
    """
    if request.method == 'POST':
        category_id = request.form.get('category_id')
        annotations = request.form.getlist('checkbox')
        # print(annotations, category_id, file=sys.stdout, flush=True)
        if len(annotations) > 0:
            db.add_annotations(category_id, annotations)
        return redirect(url_for('index'))

    rnd = db.get_random()
    category_id = rnd.get('category_id')
    category_names = [x.strip() for x in rnd.get('category name').split(',')]

    categories = requester.get_annotations(category_names)
    images = scraper.i_supply_images(category_id)

    if len(categories) == 0:
        flash("You should get new categories")
    if len(images) == 0:
        flash('Get google images')
        images = [scraper.g_supply_images(cn) for cn in category_names]

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
