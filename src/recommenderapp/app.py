"""
Copyright (c) 2023 Nathan Kohen, Nicholas Foster, Brandon Walia, Robert Kenney
This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks
"""
# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=import-error
import json
import sys
import os
from flask import Flask, jsonify, render_template, request, g
from flask_cors import CORS
import mysql.connector
from dotenv import load_dotenv
from utils import (
    beautify_feedback_data,
    send_email_to_user,
    create_account,
    login_to_account,
    submit_review,
    get_wall_posts,
    get_recent_movies,
    get_username,
    add_friend,
    get_friends,
    get_recent_friend_movies,
    add_to_watchlist,
    get_imdb_id_by_name,
)
from search import Search
from datetime import datetime

sys.path.append("../../")
from src.prediction_scripts.item_based import (
    recommend_for_new_user_g,
    recommend_for_new_user_d,
    recommend_for_new_user_a,
    recommend_for_new_user_all,
)

sys.path.remove("../../")


app = Flask(__name__)
app.secret_key = "secret key"

cors = CORS(app, resources={r"/*": {"origins": "*"}})
user = {1: None}


@app.route("/")
def login_page():
    """
    Renders the login page.
    """
    return render_template("login.html")


@app.route("/profile")
def profile_page():
    """
    Renders the login page.
    """
    if user[1] is not None:
        return render_template("profile.html")
    return render_template("login.html")


@app.route("/wall")
def wall_page():
    """
    Renders the wall page.
    """
    if user[1] is not None or user[1] == "guest":
        return render_template("wall.html")
    return render_template("login.html")


@app.route("/review")
def review_page():
    """
    Renders the review page.
    """
    if user[1] is not None or user[1] == "guest":
        return render_template("review.html")
    return render_template("login.html")


@app.route("/landing")
def landing_page():
    """
    Renders the landing page.
    """
    if user[1] is not None or user[1] == "guest":
        return render_template("landing_page.html")
    return render_template("login.html")


@app.route("/search_page")
def search_page():
    """
    Renders the search page.
    """
    if user[1] is not None or user[1] == "guest":
        return render_template("search_page.html")
    return render_template("login.html")


@app.route("/genreBased", methods=["POST"])
def predict_g():
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
    recommendations, genres, imdb_id = recommend_for_new_user_g(training_data)
    recommendations, genres, imdb_id = recommendations[:10], genres[:10], imdb_id[:10]
    resp = {"recommendations": recommendations, "genres": genres, "imdb_id": imdb_id}
    print(resp)
    return resp


@app.route("/dirBased", methods=["POST"])
def predict_d():
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
    recommendations, genres, imdb_id = recommend_for_new_user_d(training_data)
    recommendations, genres, imdb_id = recommendations[:10], genres[:10], imdb_id[:10]
    resp = {"recommendations": recommendations, "genres": genres, "imdb_id": imdb_id}
    return resp


@app.route("/actorBased", methods=["POST"])
def predict_a():
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
    recommendations, genres, imdb_id = recommend_for_new_user_a(training_data)
    recommendations, genres, imdb_id = recommendations[:10], genres[:10], imdb_id[:10]
    resp = {"recommendations": recommendations, "genres": genres, "imdb_id": imdb_id}
    return resp


@app.route("/all", methods=["POST"])
def predict_all():
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
    recommendations, genres, imdb_id = recommend_for_new_user_all(training_data)
    recommendations, genres, imdb_id = recommendations[:10], genres[:10], imdb_id[:10]
    resp = {"recommendations": recommendations, "genres": genres, "imdb_id": imdb_id}
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
def create_acc():
    """
    Handles creating a new account
    """
    data = json.loads(request.data)
    create_account(g.db, data["email"], data["username"], data["password"])
    return request.data


@app.route("/out", methods=["POST"])
def signout():
    """
    Handles signing out the active user
    """
    user[1] = None
    return request.data


@app.route("/log", methods=["POST"])
def login():
    """
    Handles logging in the active user
    """
    data = json.loads(request.data)
    resp = login_to_account(g.db, data["username"], data["password"])
    if resp is None:
        return 400
    user[1] = resp
    return request.data


@app.route("/friend", methods=["POST"])
def friend():
    """
    Handles adding a new friend
    """
    data = json.loads(request.data)
    add_friend(g.db, data["username"], user[1])
    return request.data


@app.route("/guest", methods=["POST"])
def guest():
    """
    Sets the user to be a guest user
    """
    data = json.loads(request.data)
    user[1] = data["guest"]
    return request.data


@app.route("/review", methods=["POST"])
def review():
    """
    Handles the submission of a movie review
    """
    data = request.get_json()
    movie_name = data.get("movie")
    data["imdb_id"] = get_imdb_id_by_name(g.db, movie_name)
    submit_review(g.db, user[1], movie_name, data.get("score"), data.get("review"))
    return request.data


@app.route("/getWallData", methods=["GET"])
def wall_posts():
    """
    Gets the posts for the wall
    """
    return get_wall_posts(g.db)


@app.route("/getRecentMovies", methods=["GET"])
def recent_movies():
    """
    Gets the recent movies of the active user
    """
    return get_recent_movies(g.db, user[1])


@app.route("/getRecentFriendMovies", methods=["POST"])
def recent_friend_movies():
    """
    Gets the recent movies of a certain friend
    """
    data = json.loads(request.data)
    return get_recent_friend_movies(g.db, str(data))


@app.route("/getUserName", methods=["GET"])
def username():
    """
    Gets the username of the active user
    """
    return get_username(g.db, user[1])


@app.route("/getFriends", methods=["GET"])
def get_friend():
    """
    Gets the friends of the active user
    """
    return get_friends(g.db, user[1])


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
    user_email = data["email"]
    send_email_to_user(user_email, beautify_feedback_data(data))
    return data


@app.route("/add_to_watchlist", methods=["POST"])
def add_movie_to_watchlist():
    """
    Adds a movie to the user's watchlist.
    """
    print("Entered func")
    data = request.get_json()
    print(data)
    movie_name = data.get("movieName")
    print(movie_name)
    imdb_id = (
        get_imdb_id_by_name(g.db, movie_name) if movie_name else data.get("imdb_id")
    )
    print("Got imdb id")
    if not imdb_id:
        return jsonify({"status": "error", "message": "Movie not found"}), 404
    print("imdb id is present")

    cursor = g.db.cursor()
    cursor.execute("SELECT idMovies FROM Movies WHERE imdb_id = %s", [imdb_id])
    movie_id_result = cursor.fetchone()
    print("Selected movie.")
    if movie_id_result:
        movie_id = movie_id_result[0]
        user_id = user[1]  # Assuming 'user' holds the currently logged-in user's ID
        print("Before was added.")
        # Add to watchlist and check if it was added successfully
        was_added = add_to_watchlist(g.db, user_id, movie_id)
        print(was_added)
        if was_added:
            return (
                jsonify({"status": "success", "message": "Movie added to watchlist"}),
                200,
            )
        else:
            return (
                jsonify({"status": "info", "message": "Movie already in watchlist"}),
                200,
            )
    else:
        return jsonify({"status": "error", "message": "Movie not found"}), 404


@app.route("/watchlist", methods=["GET"])
def watchlist_page():
    """
    Renders the watchlist page.
    """
    if user[1] is not None or user[1] == "guest":
        return render_template("watchlist.html")
    return render_template("login.html")


@app.route("/getWatchlistData", methods=["GET"])
def get_watchlist():
    """
    Retrieves the current user's watchlist.
    """
    user_id = user[1]  # Assuming 'user' holds the currently logged-in user's ID
    cursor = g.db.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT m.name, m.imdb_id, w.time
        FROM Watchlist w
        JOIN Movies m ON w.movie_id = m.idMovies
        WHERE w.user_id = %s
        ORDER BY w.time DESC;
        """,
        [user_id],
    )
    watchlist = cursor.fetchall()
    return jsonify(watchlist), 200


@app.route("/add_to_watched_history", methods=["POST"])
def add_movie_to_watched_history():
    """
    Adds a movie to the user's watched history.
    """
    print("Entered add_to_watched_history function")
    data = request.get_json()
    print("Request data:", data)

    movie_name = data.get("movieName")
    imdb_id = (
        get_imdb_id_by_name(g.db, movie_name) if movie_name else data.get("imdb_id")
    )

    if not imdb_id:
        return jsonify({"status": "error", "message": "Movie not found"}), 404
    print("IMDb ID obtained:", imdb_id)

    # Use the IMDb ID to fetch the movie_id from the Movies table
    cursor = g.db.cursor()
    cursor.execute("SELECT idMovies FROM Movies WHERE imdb_id = %s", [imdb_id])
    movie_id_result = cursor.fetchone()

    # Verify if the movie exists in the Movies table
    if movie_id_result:
        movie_id = movie_id_result[0]
        user_id = user[1]  # Assuming 'user' holds the currently logged-in user's ID

        # Check if this movie is already in the user's watched history
        cursor.execute(
            "SELECT idWatchedHistory FROM WatchedHistory WHERE user_id = %s AND movie_id = %s",
            [user_id, movie_id]
        )
        if cursor.fetchone():
            return jsonify({"status": "info", "message": "Movie already in watched history"}), 200

        # Insert the movie into the user's watched history
        watched_date = data.get("watched_date") or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            "INSERT INTO WatchedHistory (user_id, movie_id, watched_date) VALUES (%s, %s, %s)",
            [user_id, movie_id, watched_date]
        )
        g.db.commit()
        print("Movie added to watched history")

        return jsonify({"status": "success", "message": "Movie added to watched history"}), 200

    return jsonify({"status": "error", "message": "Movie not found"}), 404

@app.route("/get_api_key", methods=["GET"])
def get_api_key():
    """
    Provides the OMDB API key securely to the frontend.
    """
    if user[1] is not None and user[1] != "guest":
        return jsonify({"apikey": os.getenv("OMDB_API_KEY")})
    return jsonify({"error": "Unauthorized"}), 403

@app.route("/watched_history", methods=["GET"])
def watched_history_page():
    """
    Renders the watched history page.
    """
    if user[1] is not None or user[1] == "guest":
        return render_template("watched_history.html")
    return render_template("login.html")

@app.route("/getWatchedHistoryData", methods=["GET"])
def get_watched_history():
    """
    Retrieves the current user's watched history.
    """
    user_id = user[1]  # Assuming 'user' holds the currently logged-in user's ID
    cursor = g.db.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT m.name AS movie_name, m.imdb_id, wh.watched_date
        FROM WatchedHistory wh
        JOIN Movies m ON wh.movie_id = m.idMovies
        WHERE wh.user_id = %s
        ORDER BY wh.watched_date DESC;
        """,
        [user_id],
    )
    watched_history = cursor.fetchall()
    return jsonify(watched_history), 200

@app.route("/removeFromWatchedHistory", methods=["POST"])
def remove_from_watched_history():
    """
    Removes a movie from the user's watched history.
    """
    print("Entered remove_from_watched_history function")
    data = request.get_json()
    print("Request data:", data)

    imdb_id = data.get("imdb_id")
    if not imdb_id:
        return jsonify({"status": "error", "message": "IMDb ID not provided"}), 400

    cursor = g.db.cursor()
    cursor.execute(
        """
        SELECT idMovies FROM Movies WHERE imdb_id = %s
        """,
        [imdb_id]
    )
    movie_result = cursor.fetchone()

    if not movie_result:
        return jsonify({"status": "error", "message": "Movie not found"}), 404

    movie_id = movie_result[0]
    user_id = user[1]

    # Check if the movie exists in the user's watched history
    cursor.execute(
        """
        SELECT idWatchedHistory FROM WatchedHistory WHERE user_id = %s AND movie_id = %s
        """,
        [user_id, movie_id]
    )
    history_entry = cursor.fetchone()

    if not history_entry:
        return jsonify({"status": "error", "message": "Movie not in watched history"}), 404

    # Delete the movie from watched history
    cursor.execute(
        """
        DELETE FROM WatchedHistory WHERE user_id = %s AND movie_id = %s
        """,
        [user_id, movie_id]
    )
    g.db.commit()
    print("Movie removed from watched history")

    return jsonify({"status": "success", "message": "Movie removed from watched history"}), 200


@app.route("/success")
def success():
    """
    Renders the success page.
    """
    return render_template("success.html")


@app.before_request
def before_request():
    """
    Opens the db connection.
    """
    load_dotenv()
    g.db = mysql.connector.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", 3306),
        database=os.getenv("DB_NAME"),
    )


@app.after_request
def after_request(response):
    """
    Closes the db connection.
    """
    g.db.close()
    return response


if __name__ == "__main__":
    app.run(port=5000, debug=True)
