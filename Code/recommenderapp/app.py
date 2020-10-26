from flask import Flask, jsonify, render_template, request
from flask_cors import CORS, cross_origin
import json
from search import Search

app = Flask(__name__)
app.secret_key = "secret key"

cors = CORS(app, resources={r"/*": {"origins": "*"}})



@app.route("/")
def landing_page():
    return render_template("landing_page.html")


@app.route("/predictt", methods=["POST"])
def predictt():
    data = json.loads(request.data)#contains movies
    print(data)
    return data

@app.route("/search", methods=["POST"])
def search():
    term = request.form["q"]
    print("term: ", term)

    search = Search()
    filtered_dict = search.resultsTop10(term)

    resp = jsonify(filtered_dict)
    resp.status_code = 200
    return resp

if __name__=='__main__':
    app.run(port = 5000, debug = True)