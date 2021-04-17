from flask import Flask, render_template, request
from map_generator import generate_map
from db_work import find

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/map_generation", methods=["POST"])
def wait_for_map_generation():
    country = request.form["country"]
    specialization = request.form["specialization"]
    commitment = request.form["commitment"]
    # print(country,specialization,commitment)
    loc_list = find({"full_location": country, "specialization": specialization,
                     "commitment": commitment})

    if not loc_list:
        return render_template("error.html")


    fl_map = generate_map(loc_list)
    return render_template("map.html", map=fl_map._repr_html_(), len=len(loc_list), loc_list=loc_list)

# FLASK_APP=app.py FLASK_ENV=development flask run
