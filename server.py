from model import AirportCode, Campsite, connect_to_db, db
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








if __name__ == "__main__":

	connect_to_db(app)
	PORT = int(os.environ.get("PORT", 5000))
	DebugToolbarExtension(app)

	DEBUG = "NO_DEBUG" not in os.environ

	app.run(debug=DEBUG, host="0.0.0.0", port=PORT)
