from flask import Flask, render_template, request
import re
import requests
import pygal
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        stonkSymbol = request.form['stonkSymbol']
        chartType = request.form['chartType']
        timeSeries = request.form['timeSeries']
        beginDate = request.form['beginDate']
        endDate = request.form['endDate']

        # Your existing code for input validation and API calls
        # ...
        apiKey = 'BQXXFJR3NUAO20QT'

        # API call and chart generation
        chart = generate_chart(stonkSymbol, chartType, timeSeries, beginDate, endDate)

        return render_template('index.html', chart=chart)

    return render_template('index.html', chart=None)


def generate_chart(stonkSymbol, chartType, timeSeries, beginDate, endDate):
    apiKey = 'JQDCJ9W4UP3840QP'

    # Your existing code for API calls and data processing
    if timeSeries == "1":
        # Code for intraday time series

    elif timeSeries == "2":
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stonkSymbol}&outputsize=full&apikey={apiKey}'
        r = requests.get(url)
        data = r.json()
        daily_data = data['Time Series (Daily)']
        # ...

    elif timeSeries == "3":
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={stonkSymbol}&apikey={apiKey}'
        r = requests.get(url)
        data = r.json()
        weekly_data = data['Weekly Time Series']
        # ...

    elif timeSeries == "4":
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={stonkSymbol}&apikey={apiKey}'
        r = requests.get(url)
        data = r.json()
        monthly_data = data['Monthly Time Series']
        # ...

    # Your existing code for data filtering and sorting
    sorted_data = sorted(data.items(), key=lambda x: x[0])
    filtered_data = [(date, values) for date, values in sorted_data if beginDate <= date <= endDate]

    # Your existing code for chart creation
    if chartType == "1":
        chart = pygal.Bar(title=f'Stock Data for {stonkSymbol}: {beginDate} to {endDate}', x_label_rotation=90, show_minor_x_labels=True)
        chart.x_labels = [date for date, _ in filtered_data]
        chart.add('Open', [float(values['1. open']) for _, values in filtered_data])
        chart.add('Close', [float(values['4. close']) for _, values in filtered_data])
        chart.add('High', [float(values['2. high']) for _, values in filtered_data])
        chart.add('Low', [float(values['3. low']) for _, values in filtered_data])

    elif chartType == "2":
        chart = pygal.Line(title=f'Stock Data for {stonkSymbol}: {beginDate} to {endDate}', x_label_rotation=90, show_minor_x_labels=True)
        chart.x_labels = [date for date, _ in filtered_data]
        chart.add('Open', [float(values['1. open']) for _, values in filtered_data])
        chart.add('Close', [float(values['4. close']) for _, values in filtered_data])
        chart.add('High', [float(values['2. high']) for _, values in filtered_data])
        chart.add('Low', [float(values['3. low']) for _, values in filtered_data])

    return chart

if __name__ == '__main__':
    app.run(debug=True)
