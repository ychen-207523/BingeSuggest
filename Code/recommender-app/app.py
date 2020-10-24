from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
from search import Search


app = Flask(__name__)
app.secret_key = "secret key"

# app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
# app.config['CORS_HEADERS'] = 'Content-Type'

# CORS(app)


@app.route("/")
def landing_page():
    return render_template("landing_page.html")

@app.route("/search", methods=["POST"])
def search():
    term = request.form["q"]
    print("term: ", term)

    search = Search()
    filtered_dict = search.resultsTop10(term)

    resp = jsonify(filtered_dict)
    resp.status_code = 200
    return resp

@app.route("/predict", methods=["POST"])
def predict():
    movie_list = request.form["movie_list"]
    print(movie_list)

    return movie_list

if __name__=='__main__':
    app.run(port = 5000, debug = True)