 # import random things to make code work
import re
import datetime
import requests
import pygal




def generateGraph(stonkSymbol, chartType, timeSeries,beginDate,endDate):
    
    # if not re.match("^[A-Z0-9]+$", stonkSymbol):
    #     return 0
    
    # if chartType not in ['1', '2']:
    #     return 0

    # if timeSeries not in ['1', '2', '3', '4']:
    #     return 0

    # if len(beginDate) != 10 or len(endDate) != 10:
    #     return 0

    begin_year = int(beginDate[:4])
    end_year = int(endDate[:4])

    # Ensure that the month has no more than 2 digits
    begin_month = int(beginDate[5:7])
    end_month = int(endDate[5:7])

    # Ensure that the day has no more than 2 digits
    begin_day = int(beginDate[8:10])
    end_day = int(endDate[8:10])

    # if not (1000 <= begin_year <= 9999 and 1000 <= end_year <= 9999):
    #     return 0
    #     print("Year should have 4 digits.")
    # elif not (1 <= begin_month <= 12 and 1 <= end_month <= 12):
    #     return 0
    #     print("Month should have 2 digits or be in the range 1-12.")
    # elif not (1 <= begin_day <= 31 and 1 <= end_day <= 31):
    #     return 0
    #     print("Day should have 2 digits or be in the range 1-31.")
    # elif endDate < beginDate:
    #     return 0
    #     print("End date should not be before the begin date.")

    #apiKey = 'DRG582I7BHG1JLI6'
    apiKey = 'JQDCJ9W4UP3840QP'

    #Pulling from api based on time series
    if timeSeries=="1: Intraday":
        #intraday is a little more tricky because there's an interval, and an optional month
        currentMonth=begin_month
        currentYear=begin_year
        intraday_data={}

        #Okay so
        #First step is to assign begin month and year to other variables so I can add to them willy nilly
        #Also create a dictionary I think called data to make the processing easier
        #Then, make a loop, probably while true, I can break it later
        while(True):
            #Check if the month is greater than 12. This way, I can make sure I'm not trying to find like, Franuary or whatever the 13th month would be
            # If it is, set it to 1 and then increase the year by 1
            if(currentMonth>12):
                currentMonth=1
                currentYear+=1
            #Next, check if the month is greater than the end month and the end year is greater than the end year
            #Has to be and because month is probably gonna get there faster
            #   If it is, break
            if(currentMonth>=end_month and currentYear>=end_year):
                break

            month=""+str(currentYear)+"-"+str(currentMonth)
        
            print(month)
            url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+stonkSymbol+'&interval=5min&month='+month+'outputsize=full&apikey='+apiKey
            r = requests.get(url)
            data = r.json()
            print(data)
            print(data.keys())

            #could I iterate through by item, then use the single as the key to add the data to the intraday dictionary?
            #I dunno it sounds logical loll
            data=data['Time Series (5min)']
            for dat in data:
                print(dat)
                intraday_data[dat]=data[dat]
            currentMonth +=1
        
        
        
        
        

        #After that, make a string in the format 'currentYear' + "-" + 'currentMonth'

        #then slap a month in the url, run through the processing, extract the data dictionary, and then either append the data dictionary or loop through it and append each entry
        #Check both

        #And then increase month by one


        
        
        sorted_data = sorted(intraday_data.items(), key=lambda x: x[0])
        filtered_data = [(date, values) for date, values in sorted_data if beginDate <= date <= endDate]

        if chartType == "1: Bar":
            chart = pygal.Bar(title='Stock Data for ' + stonkSymbol + ': ' + beginDate + ' to ' + endDate, x_label_rotation=90, show_minor_x_labels=True)
            chart.x_labels = [date for date, _ in filtered_data]
            chart.add('Open', [float(values['1. open']) for _, values in filtered_data])
            chart.add('Close', [float(values['4. close']) for _, values in filtered_data])
            chart.add('High', [float(values['2. high']) for _, values in filtered_data])
            chart.add('Low', [float(values['3. low']) for _, values in filtered_data])
            #chart.render_in_browser()
        # Create the chart
        if chartType == "2: Line":
            chart = pygal.Line(title='Stock Data for ' + stonkSymbol + ': ' + beginDate + ' to ' + endDate, x_label_rotation=90, show_minor_x_labels=True)
            chart.x_labels = [date for date, _ in filtered_data]
            chart.add('Open', [float(values['1. open']) for _, values in filtered_data])
            chart.add('Close', [float(values['4. close']) for _, values in filtered_data])
            chart.add('High', [float(values['2. high']) for _, values in filtered_data])
            chart.add('Low', [float(values['3. low']) for _, values in filtered_data])
            #chart.render_in_browser()
    elif timeSeries=="2: Daily":
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+stonkSymbol+'&outputsize=full&apikey='+apiKey
        r = requests.get(url)
        data = r.json()

        print(data)
        #Started architecture for filtering, the first line is to get to the actual data, which looks like a dictionary inside a dictionary 
        daily_data = data['Time Series (Daily)']
        sorted_data = sorted(daily_data.items(), key=lambda x: x[0])
        filtered_data = [(date, values) for date, values in sorted_data if beginDate <= date <= endDate]

        if chartType == "1":
            chart = pygal.Bar(title='Stock Data for ' + stonkSymbol + ': ' + beginDate + ' to ' + endDate, x_label_rotation=90, show_minor_x_labels=True)
            chart.x_labels = [date for date, _ in filtered_data]
            chart.add('Open', [float(values['1. open']) for _, values in filtered_data])
            chart.add('Close', [float(values['4. close']) for _, values in filtered_data])
            chart.add('High', [float(values['2. high']) for _, values in filtered_data])
            chart.add('Low', [float(values['3. low']) for _, values in filtered_data])
            #chart.render_in_browser()
        # Create the chart
        if chartType == "2: Line":
            chart = pygal.Line(title='Stock Data for ' + stonkSymbol + ': ' + beginDate + ' to ' + endDate, x_label_rotation=90, show_minor_x_labels=True)
            chart.x_labels = [date for date, _ in filtered_data]
            chart.add('Open', [float(values['1. open']) for _, values in filtered_data])
            chart.add('Close', [float(values['4. close']) for _, values in filtered_data])
            chart.add('High', [float(values['2. high']) for _, values in filtered_data])
            chart.add('Low', [float(values['3. low']) for _, values in filtered_data])
            #chart.render_in_browser()
    elif timeSeries=="3: Weekly":
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol='+stonkSymbol+'&apikey='+apiKey
        r = requests.get(url)
        data = r.json()

        print(data)
        weekly_data = data['Weekly Time Series']
        sorted_data = sorted(weekly_data.items(), key=lambda x: x[0])
        filtered_data = [(date, values) for date, values in sorted_data if beginDate <= date <= endDate]

        if chartType == "1: Bar":
            chart = pygal.Bar(title='Stock Data for ' + stonkSymbol + ': ' + beginDate + ' to ' + endDate, x_label_rotation=90, show_minor_x_labels=True)
            chart.x_labels = [date for date, _ in filtered_data]
            chart.add('Open', [float(values['1. open']) for _, values in filtered_data])
            chart.add('Close', [float(values['4. close']) for _, values in filtered_data])
            chart.add('High', [float(values['2. high']) for _, values in filtered_data])
            chart.add('Low', [float(values['3. low']) for _, values in filtered_data])
            #chart.render_in_browser()
        # Create the chart
        if chartType == "2: Line":
            chart = pygal.Line(title='Stock Data for ' + stonkSymbol + ': ' + beginDate + ' to ' + endDate, x_label_rotation=90, show_minor_x_labels=True)
            chart.x_labels = [date for date, _ in filtered_data]
            chart.add('Open', [float(values['1. open']) for _, values in filtered_data])
            chart.add('Close', [float(values['4. close']) for _, values in filtered_data])
            chart.add('High', [float(values['2. high']) for _, values in filtered_data])
            chart.add('Low', [float(values['3. low']) for _, values in filtered_data])
            #chart.render_in_browser()
    elif timeSeries=="4: Monthly":
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol='+stonkSymbol+'&apikey='+apiKey
        r = requests.get(url)
        data = r.json()

        print(data)
        monthly_data = data['Monthly Time Series']
        sorted_data = sorted(monthly_data.items(), key=lambda x: x[0])
        filtered_data = [(date, values) for date, values in sorted_data if beginDate <= date <= endDate]

        if chartType == "1: Bar":
            chart = pygal.Bar(title='Stock Data for ' + stonkSymbol + ': ' + beginDate + ' to ' + endDate, x_label_rotation=90, show_minor_x_labels=True)
            chart.x_labels = [date for date, _ in filtered_data]
            chart.add('Open', [float(values['1. open']) for _, values in filtered_data])
            chart.add('Close', [float(values['4. close']) for _, values in filtered_data])
            chart.add('High', [float(values['2. high']) for _, values in filtered_data])
            chart.add('Low', [float(values['3. low']) for _, values in filtered_data])
            
        # Create the chart
        if chartType == "2: Line":
            chart = pygal.Line(title='Stock Data for ' + stonkSymbol + ': ' + beginDate + ' to ' + endDate, x_label_rotation=90, show_minor_x_labels=True)
            chart.x_labels = [date for date, _ in filtered_data]
            chart.add('Open', [float(values['1. open']) for _, values in filtered_data])
            chart.add('Close', [float(values['4. close']) for _, values in filtered_data])
            chart.add('High', [float(values['2. high']) for _, values in filtered_data])
            chart.add('Low', [float(values['3. low']) for _, values in filtered_data])
    print(type(chart))

    return chart



# # Tell em
# print("Stonk Data Visualizer")
# print("----------------------")

# # Ask the user to enter the stock symbol for the company they want data for.
# stonkSymbol = input("\nEnter stonk symbol: ")
# while not re.match("^[A-Z0-9]+$", stonkSymbol):
#     print("Invalid input. Please enter a valid stock symbol.")
#     stonkSymbol = input("Enter stonk symbol: ")

# # Ask the user for the chart type they would like.
# print("Chart Types")
# print("------------")
# print("1. Bar\n2. Line")
# chartType = input("\nEnter the chart type you want (1, 2): ")
# while chartType not in ['1', '2']:
#     print("Invalid input. Please enter either '1' for Bar or '2' for Line chart.")
#     chartType = input("Enter the chart type you want (1, 2): ")

# # Ask the user for the time series function they want the api to use.
# print("Select the Time Series of the chart you want to Generate")
# print("---------------------------------------------------------")
# print("1. Intraday\n2. Daily\n3. Weekly\n4. Monthly")
# timeSeries = input("\nEnter the time series option (1, 2, 3, 4): ")
# while timeSeries not in ['1', '2', '3', '4']:
#     print("Invalid input. Please enter a valid time series option (1, 2, 3, 4).")
#     timeSeries = input("Enter the time series option (1, 2, 3, 4): ")

# # get those damn dates
# while True:
#     beginDate = input("\nEnter the start Date (YYYY-MM-DD): ")
#     endDate = input("Enter the end Date (YYYY-MM-DD): ")

#     try:
#         # Ensure that the year has no more than 4 digits
#         if len(beginDate) != 10 or len(endDate) != 10:
#             print("Invalid date format. Please use YYYY-MM-DD format for dates.")
#             continue

#         begin_year = int(beginDate[:4])
#         end_year = int(endDate[:4])

#         # Ensure that the month has no more than 2 digits
#         begin_month = int(beginDate[5:7])
#         end_month = int(endDate[5:7])

#         # Ensure that the day has no more than 2 digits
#         begin_day = int(beginDate[8:10])
#         end_day = int(endDate[8:10])

#         if not (1000 <= begin_year <= 9999 and 1000 <= end_year <= 9999):
#             print("Year should have 4 digits.")
#         elif not (1 <= begin_month <= 12 and 1 <= end_month <= 12):
#             print("Month should have 2 digits or be in the range 1-12.")
#         elif not (1 <= begin_day <= 31 and 1 <= end_day <= 31):
#             print("Day should have 2 digits or be in the range 1-31.")
#         elif endDate < beginDate:
#             print("End date should not be before the begin date.")
#         else:
#             break
#     except ValueError:
#         print("Invalid date format. Please use YYYY-MM-DD format for dates.")
    

#     chart=generateGraph(stonkSymbol, chartType, timeSeries,beginDate,endDate)
#     chart.render_in_browser()
    


