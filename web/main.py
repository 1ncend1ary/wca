#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flask application main module.

__author__ = "Aleksei Seliverstov"
__license__ = "MIT"
__email__ = "alexseliverstov@yahoo.com"
"""
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user

from web import app, login_manager, db, requester, logger
import web.scraper as scraper
from web.forms import LoginForm
from web.database import User
import ast


@login_manager.user_loader
def load_user(user_id):
    """
    Required user loader method definition
    """
    return User.get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Flask login page render method
    """
    logger.info('Requested login.')
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid login or password.')
            logger.info('Invalid authentication credentials.')
            return render_template('login.html', title='Sign In', form=form)
        else:
            flash('Logged in user {}'.format(form.username.data))
            logger.info('Successfully logged in user {}.'.format(form.username.data))
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    """
    Flask logout page render method
    """
    logger.info('Requested logout.')
    logout_user()
    return redirect(url_for('login'))


@login_manager.unauthorized_handler
def unauth_handler():
    """
    Flask unauthorized access to documents handler
    """
    return render_template('401.html'), 401


def get_more_interests(req):
    """
    Flask index page POST request render method
    """
    if req.form.get('type') == 'submit_categories':
        category_id = req.form.get('category_id')
        annotations = req.form.getlist('checkbox')
        if len(annotations) > 0:
            db.add_annotations(category_id, annotations)
        return redirect(url_for('index'))
    elif req.form.get('type') == 'add_category':
        def convert_to_list(string):
            try:
                return ast.literal_eval(string)
            except ValueError:
                return []

        category_names = req.form.get('words')
        category_names = convert_to_list(category_names)

        categories = req.form.get('categories')
        categories = convert_to_list(categories)

        category_id = req.form.get('category_id')
        images = scraper.supply_images(category_id, category_names)

        text = req.form.get('text')
        new_categories = requester.get_annotations([text])

        new_categories += categories

        if len(new_categories) == 0:
            message = "No new categories found, you should consider changing your search term."
            flash(message)
            logger.info(message)

        num_of_images = 30
        return render_template("index.html", words=category_names, images=list(images)[:num_of_images],
                               categories=list(set(new_categories)), category_id=category_id, isfunny=False)


def get_interests():
    """
    Get random category interests and render the 'index' template
    """
    rnd = db.get_random()
    category_id = rnd.get('category_id')
    category_names = [x.strip() for x in rnd.get('category name').split(',')]

    categories = requester.get_annotations(category_names)
    images = scraper.supply_images(category_id, category_names)

    if len(categories) == 0:
        message = "No categories found, you should consider finding them yourself using the 'Get categories' field."
        flash(message)
        logger.info(message)

    num_of_images = 30
    return render_template("index.html", words=category_names, images=images[:num_of_images],
                           categories=list(categories), category_id=category_id, isfunny=False)


@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    """
    Flask index page render method
    """
    logger.info('Requested index page.')
    if request.method == 'POST':
        return get_more_interests(request)
    else:
        return get_interests()


if __name__ == "__main__":
    app.run(ssl_context='adhoc')
