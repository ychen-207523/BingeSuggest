"""
Copyright (c) 2023 Aditya Pai, Ananya Mantravadi, Rishi Singhal, Samarth Shetty
This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks
"""

import json
import sys

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from search import Search
from utils import beautify_feedback_data, send_email_to_user

sys.path.append("../../")
#pylint: disable=wrong-import-position
from src.prediction_scripts.item_based import recommend_for_new_user
#pylint: enable=wrong-import-position


app = Flask(__name__)
app.secret_key = "secret key"

cors = CORS(app, resources={r"/*": {"origins": "*"}})


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
    return render_template("wall.html")

@app.route("/review")
def review_page():
    """
    Renders the review page.
    """
    return render_template("review.html")

@app.route("/landing")
def landing_page():
    """
    Renders the landing page.
    """
    return render_template("landing_page.html")


@app.route("/search_page")
def search_page():
    """
    Renders the search page.
    """
    return render_template("search_page.html")


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


if __name__ == "__main__":
    app.run(port=5000)
