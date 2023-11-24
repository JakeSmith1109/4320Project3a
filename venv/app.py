import sqlite3
import csv
from flask import Flask, render_template, request, url_for, flash, redirect, abort
#import pygal

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

#flash  the secret key to secure sessions
app.config['SECRET_KEY'] = 'your secret key'

def read_csv():
    with open('stocks.csv', 'r') as file:
        reader = csv.DictReader(file)
        symbols = [row['Symbol'] for row in reader]

    return symbols

# use flask's app.route decorate to map the url to that function
@app.route("/")
def index():
    symbols = read_csv()
    chartTypes = ['1: Bar', '2: Line']
    timeSers = ['1: Intraday', '2: Daily', '3: Weekly', '4: Monthly']
    return render_template('index.html', symbols=symbols, chartTypes=chartTypes, timeSers=timeSers)

app.run(host="0.0.0.0", port=5001)