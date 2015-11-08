from model import AirportCode, connect_to_db, db, Experience
from flask import Flask, render_template, redirect, request, flash, session, jsonify

import requests
import json
import datetime
import pprint
import geojson

import os


# sabre_access_token = os.environ["SABRE_ACCESS_TOKEN"]


app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "ABCDEF")

@app.route("/")
def homepage():
	"""Displays homepage."""

	return render_template("index.html")

@app.route("/experience/<id>")
def get_experience(id):
    experience = Experience.get_experience_by_id(id)
    detail_info = experience.get_detailed_info()
    name = detail_info.get('name', None)
    excerpt = detail_info.get('excerpt', None)
    duration = detail_info.get('duration', None)
    price = detail_info.get('price', None)
    medias = detail_info.get('medias', None)
    photo_src = None
    if medias:
        photo_src = medias[0].get('src', None)

    print name, excerpt, duration, price, photo_src

    return 'hello'


if __name__ == "__main__":

	connect_to_db(app)
	PORT = int(os.environ.get("PORT", 5000))
	# DebugToolbarExtension(app)
	SQLALCHEMY_TRACK_MODIFICATIONS = False


	DEBUG = "NO_DEBUG" not in os.environ

	app.run(debug=DEBUG)
