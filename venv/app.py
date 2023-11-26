import sqlite3
import csv
from flask import Flask, render_template, request, url_for, flash, redirect, abort
import StockDataVizualizer
#import pygal

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

#flash  the secret key to secure sessions
app.config['SECRET_KEY'] = 'your secret key'

#read data from csv file
def read_csv():
    with open('4320Project3a/stocks.csv', 'r') as file:
        reader = csv.DictReader(file)
        symbols = [row['Symbol'] for row in reader]

    return symbols

# use flask's app.route decorate to map the url to that function
@app.route("/")
def index():
    #create info for chart type, time series, and symbols
    
    symbols = read_csv()
    chartTypes = ['1: Bar', '2: Line']
    timeSers = ['1: Intraday', '2: Daily', '3: Weekly', '4: Monthly']
    return render_template('index.html', symbols=symbols, chartTypes=chartTypes, timeSers=timeSers)
    
@app.route('/charts/', methods=('GET', 'POST'))
def charts():
     if request.method=='POST':
        print("Start date "+str(request.form["sDate"]))
        symbols = read_csv()
        chartTypes = ['1: Bar', '2: Line']
        timeSers = ['1: Intraday', '2: Daily', '3: Weekly', '4: Monthly']
        if not(request.form["symbol"] in symbols):
            flash("Please input a Symbol")
        elif not(request.form["chartType"] in chartTypes ):
            flash("Please input a Chart type")
        elif not(request.form["timeSer"] in timeSers):
             flash("Please input a Time series")
        elif(request.form["sDate"]==''):
            flash("Please enter a start date")
        elif(request.form["eDate"]==''):
            flash("Please enter a End date")
        else:
            chart=StockDataVizualizer.generateGraph(request.form["symbol"],request.form["chartType"],request.form["timeSer"],request.form["sDate"],request.form["eDate"])
            chart = chart.render_data_uri()
        
            return render_template( 'charts.html', chart = chart,symbols=symbols, chartTypes=chartTypes, timeSers=timeSers)
        return render_template( 'charts.html',symbols=symbols, chartTypes=chartTypes, timeSers=timeSers)
        
        
   

app.run(host="0.0.0.0", port=5001)