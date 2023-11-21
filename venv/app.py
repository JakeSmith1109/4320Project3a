import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort
#import pygal

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

#flash  the secret key to secure sessions
app.config['SECRET_KEY'] = 'your secret key'

# use flask's app.route decorate to map the url to that function
@app.route("/")

# function that returns content or string
def home():
    return "Hello bitch"

app.run(host="0.0.0.0", port=5001)