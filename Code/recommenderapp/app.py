from flask import Flask, jsonify, render_template, request
from flask_cors import CORS, cross_origin
import json
import sys
from utils import *
sys.path.append("../../")
from Code.prediction_scripts.item_based import recommend_for_new_user
from search import Search

app = Flask(__name__)
app.secret_key = "secret key"

cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def landing_page():
    return render_template("landing_page.html")


@app.route("/predict", methods=["POST"])
def predict():
    # contains movies
    data = json.loads(request.data)
    data1 = data["movie_list"]
    training_data = []
    for movie in data1:
        movie_with_rating = {"title": movie, "rating": 5.0}
        if (movie_with_rating not in training_data):
            training_data.append(movie_with_rating)
    recommendations = recommend_for_new_user(training_data)
    recommendations = recommendations[:10]
    resp = {"recommendations": recommendations}
    return resp


@app.route("/search", methods=["POST"])
def search():
    term = request.form["q"]
    search = Search()
    filtered_dict = search.resultsTop10(term)
    resp = jsonify(filtered_dict)
    resp.status_code = 200
    return resp


@app.route("/feedback", methods=["POST"])
def feedback():
    data = json.loads(request.data)
    user_email = "ananyamantravadi@gmail.com"
    send_email_to_user(user_email, str(beautify_feedback_data(data)))
    return data


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
