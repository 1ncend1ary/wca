from flask import Flask, render_template
import time
import redis
import database

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    #count = get_hit_count()
    element = database.fetch_new_entry()
    return render_template("index.html", word=element['category name'], image=None)


@app.route("/contacts")
def contacts():
    return render_template("contacts.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
