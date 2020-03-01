from flask import Flask, render_template, request
import requests
import database
import logging
import sys
import time
from multiprocessing import Pool

app = Flask(__name__)
logging.basicConfig(filename='main.log', filemode='w', format='%(asctime)s - %(process)d - %(levelname)s - %(message)s')

# https://medium.com/@interestexplorerio/how-to-use-the-facebook-marketing-api-to-reveal-1000s-of-interests-that-are-hidden-in-the-facebook-e20ee5bdcd17
token = '134360907906848|ij_GtRjQP5nKWJqZANjH6zsSbEw'


def get_interests(r):
    # r = requests.get('https://graph.facebook.com/search?type=adinterest&q=[\'' +
    #                  category +
    #                  '\']&limit=10000&locale=en_US&access_token=' + token)
    data = r.json()['data']
    interests = [x['name'] for x in data]
    # subcategories = category.split()
    # if len(subcategories) > 1:
    #     for subcategory in subcategories:
    #         interests += get_interests(subcategory)
    return interests


def get_request(link):
    return requests.get(link)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        element = database.fetch_new_entry()
        category_id = element.get('category_id')
        category_name_string = element.get('category name')
        category_names = []
        for x in category_name_string.split(','):
            x = x.strip()
            qq = x.split()
            if len(qq) > 1:
                category_names += [x] + qq
            else:
                category_names += x

        # category_names = [x.strip() for x in category_name_string.split(',')]

        start = time.time()
        links = ['https://graph.facebook.com/search?type=adinterest&q=[\'' + x +
                 '\']&limit=10000&locale=en_US&access_token=' + token for x in category_names]
        with Pool(5) as p:
            list_req = p.map(get_request, links)

        categories = list(map(get_interests, list_req))
        print('Get categories:', time.time() - start, file=sys.stdout, flush=True)

        start = time.time()
        r = requests.get('http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=' + category_id)
        images = r.text.splitlines()[:10]
        print('Get images:', time.time() - start, file=sys.stdout, flush=True)

        return render_template("index.html", words=category_names, images=images, categories=set(categories[:10]))
    # elif request.method == 'POST':
    #     print(request.form.getlist('projectFilepath'), file=sys.stdout, flush=True)
    #     return render_template("index.html")


@app.route("/contacts")
def contacts():
    return render_template("contacts.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
