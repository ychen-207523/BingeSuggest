"""
Copyright (c) 2023 Aditya Pai, Ananya Mantravadi, Rishi Singhal, Samarth Shetty
This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks
"""

import json
import sys
import calendar
import time
import datetime
from flask import Flask, jsonify, render_template, request, g
from flask_cors import CORS
from search import Search
from utils import beautify_feedback_data, send_email_to_user, createAccount, logintoAccount, submitReview
import mysql.connector
import os
from dotenv import load_dotenv

sys.path.append("../../")
#pylint: disable=wrong-import-position
from src.prediction_scripts.item_based import recommend_for_new_user
#pylint: enable=wrong-import-position


app = Flask(__name__)
app.secret_key = "secret key"

cors = CORS(app, resources={r"/*": {"origins": "*"}})
user = {
    1:'None'
}

@app.route("/")
def login_page():
    """
    Renders the login page.
    """
    return render_template("login.html")

@app.route("/wall")
def wall_page():
    """
    Renders the wall page.
    """
    if (user[1] != None or user[1] == 'guest'):
        return render_template("wall.html")
    return 400

@app.route("/review")
def review_page():
    """
    Renders the review page.
    """
    if (user[1] != None or user[1] == 'guest'):
        return render_template("review.html")
    return 400

@app.route("/landing")
def landing_page():
    """
    Renders the landing page.
    """
    if (user[1] != None or user[1] == 'guest'):
        return render_template("landing_page.html")
    return 400


@app.route("/search_page")
def search_page():
    """
    Renders the search page.
    """
    if (user[1] != None or user[1] == 'guest'):
        return render_template("search_page.html")
    return 400


@app.route("/predict", methods=["POST"])
def predict():
    """
    Predicts movie recommendations based on user ratings.
    """
    data = json.loads(request.data)
    data1 = data["movie_list"]
    training_data = []
    for movie in data1:
        movie_with_rating = {"title": movie, "rating": 5.0}
        if movie_with_rating not in training_data:
            training_data.append(movie_with_rating)
    recommendations, genres, imdb_id = recommend_for_new_user(training_data)
    recommendations, genres, imdb_id = recommendations[:10], genres[:10], imdb_id[:10]
    resp = {"recommendations": recommendations, "genres": genres, "imdb_id":imdb_id}
    return resp


@app.route("/search", methods=["POST"])
def search():
    """
    Handles movie search requests.
    """
    term = request.form["q"]
    finder = Search()
    filtered_dict = finder.results_top_ten(term)
    resp = jsonify(filtered_dict)
    resp.status_code = 200
    return resp

@app.route("/", methods=["POST"])
def createAcc():
    data = json.loads(request.data)
    createAccount(g.db, data["email"], data["username"], data["password"])
    return request.data

@app.route("/log", methods=["POST"])
def logIn():
    data = json.loads(request.data)
    resp = logintoAccount(g.db, data["username"], data["password"])
    print(resp)
    if (resp == None):
        return 400
    user[1] = resp
    return request.data

@app.route("/guest", methods=["POST"])
def guest():
    data = json.loads(request.data)
    user[1] = data["guest"]
    return request.data

@app.route("/review", methods=["POST"])
def review():
    data = json.loads(request.data)
    d = datetime.datetime.utcnow()
    timestamp = calendar.timegm(d.timetuple())
    submitReview(g.db, 1, data["movie"], data["score"], data["review"], timestamp)
    return request.data


@app.route("/feedback", methods=["POST"])
def feedback():
    """
    Handles user feedback submission and mails the results.
    """
    data = json.loads(request.data)
    return data


@app.route("/sendMail", methods=["POST"])
def send_mail():
    """
    Handles user feedback submission and mails the results.
    """
    data = json.loads(request.data)
    user_email = data['email']
    send_email_to_user(user_email, beautify_feedback_data(data))
    return data

@app.route("/success")
def success():
    """
    Renders the success page.
    """
    return render_template("success.html")

@app.before_request
def before_request():
    print('opening db connection')
    load_dotenv()
    g.db = mysql.connector.connect(user='root', password=os.getenv('DB_PASSWORD'),
                                host='127.0.0.1',
                                database='popcornpicksdb')

@app.after_request
def after_request(response):
    print('closing db connection')
    g.db.close()
    return response

if __name__ == "__main__":
    app.run(port=5000)
