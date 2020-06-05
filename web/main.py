# -*- coding: utf-8 -*-
"""
Flask application main module

Programmer: Aleksei Seliverstov <alexseliverstov@yahoo.com>
"""
from flask import Flask, render_template, request, redirect, url_for, flash, abort, jsonify
import database
import interests
from config import Config
import scraper
import sys
import ast
from forms import LoginForm
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from models import User

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)

db = database.Categories()
requester = interests.FacebookRequest()


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid login or password.')
            return redirect(url_for('login'))
        else:
            flash('Logged in user {}'.format(form.username.data))
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@login_manager.unauthorized_handler
def unauth_handler():
    return render_template('401.html'), 401


@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    """
    Flask index page render
    """
    if request.method == 'POST':
        if request.form.get('type') == 'submit_categories':
            category_id = request.form.get('category_id')
            annotations = request.form.getlist('checkbox')
            # print(annotations, category_id, file=sys.stdout, flush=True)
            if len(annotations) > 0:
                db.add_annotations(category_id, annotations)
            return redirect(url_for('index'))
        elif request.form.get('type') == 'add_category':
            category_names = request.form.get('words')
            category_id = request.form.get('category_id')
            images = scraper.i_supply_images(category_id)
            categories = request.form.get('categories')
            print(category_names, category_id, categories, type(categories), file=sys.stdout, flush=True)

            def convert_to_list(string, regex):
                return ast.literal_eval(string)

            category_names = convert_to_list(category_names, '[]\'')
            if len(categories) > 0:  # todo remove crook
                categories = convert_to_list(categories, '[]\'')
            print('Attempt 2:', category_names, category_id, categories, type(categories), file=sys.stdout, flush=True)

            text = request.form.get('text')
            new_categories = requester.get_annotations([text])
            for i, category in enumerate(new_categories):
                print(category[1])
                new_categories[i][1] = '->\n'.join(category[1])
            new_categories += categories

            print('Attempt 3[text, new categories]:', text, new_categories, file=sys.stdout, flush=True)
            images = list(images)
            # todo add set
            # todo add different category trees
            return render_template("index.html", words=category_names, images=images, categories=new_categories,
                                   category_id=category_id)

    rnd = db.get_random()
    category_id = rnd.get('category_id')
    category_names = [x.strip() for x in rnd.get('category name').split(',')]

    categories = requester.get_annotations(category_names)

    for i, category in enumerate(categories):
        print(category[1])
        categories[i][1] = '->\n'.join(category[1])

    images = scraper.i_supply_images(category_id)

    # todo normal logging
    if len(categories) == 0:
        flash("No categories found, you should consider finding them yourself.")

    if len(images) == 0:
        flash('No images provided, queried Bing for related images.')
        # todo work with lists correctly
        for cn in category_names:
            images += scraper.bing_suppy_images(cn)

    return render_template("index.html", words=category_names, images=images[:20], categories=list(categories),
                           category_id=category_id)


if __name__ == "__main__":
    app.run(ssl_context='adhoc')  # host="0.0.0.0", debug=True
