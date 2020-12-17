# This is Final Project for course MIS 3500
# Project chosen for the Final project is '1'
# The project is based on Stock Market

# Pre-requisites of the Project
# 1. Getting Data from web JSON API
# 2. Storing data in CSV files
# 3. Auto-update
# 4. Three Analysis on the data
# 5. Results inside results.json

import requests  # three request library is used to use api to request for data
# path is called for checking if the file exists and that helps in calling different functions
from os import path
import time  # time library is used for the sleep to avoid api max out
import json  # json is called to be used for creating json file
API_KEY = 'NG9C9EPVYBMQT0C8'
# API KEY for the data

# RESOURCES USED:
# Class lectures
# Content Videos
# Old hw to get idea of dict syntax

# Library imports
# json import to handle the json files
# requests imported to handle API key
# wait for 1 sec

mean_reversion_dict = {}
simple_average_dict = {}
bb_dict = {}
# These dictonaries are not used for the highest data returns but for the json dump file

#


def append(ticker):
    # the append function is created for the situation where the file has already been created
    # the data can be outdated and thus this function can check if the data is outdated or new
    # if the data is outdated this fucntion will find the latest data using api and update the files
    # this helps save time as searching and gathering all the data each time takes a lot of time and internet
    # this function's basic usage is resource saving
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + \
        ticker+'&outputsize=full&apikey=' + API_KEY
    req = requests.get(url)
    time.sleep(13)
    # sleep is required or else the api key will max out its ability to send data

    req_dict = json.loads(req.text)
    # the load funtion takes the text encoding format and makes a dictionary out of it
    print(req_dict.keys())
    # this will print the keys of the dict which can help determine the keys to be used in json file filter process

    key1 = 'Time Series (Daily)'  # dictionary with all prices by date
    key2 = '4. close'
    # the keys to be used to define and filter the jscon file and derive what is fruitful for the project
    # the below csv file is onlu possible after the keys are identified and the appropriate data is identified
    csv_file = open(ticker + ".csv", "r")
    lines = csv_file.readlines()
    last_date = lines[-1].split(",")[0]
    # last date checks if there is any latest data that needs to be appended
    new_lines = []
    # new lines is for creating the array with new data that needs to be appeneded in already created file
    for date in req_dict[key1]:
        if date == last_date:
            break
        print(date + "," + req_dict[key1][date][key2])  # print key, value
        new_lines.append(date + "," + req_dict[key1][date][key2]+"\n")

    # new lines is used here to make the whole series of data in an well arranged order to be used by the algorithms
    new_lines = new_lines[::-1]
    csv_file = open("/home/ubuntu/environment/final_project/" +
                    ticker + ".csv", "a")  # opening the file to append data
    csv_file.writelines(new_lines)  # appending new data
    csv_file.close()

    # Return the CSV file for further usage
    return csv_file
    # function ends here


def process_json(ticker):
    # this function is used in a situation where the ticker file does not exist
    # this fucntion creates a file in the scenario the user puts the ticker name & is not present to the algorithms for analysis
    # in that scenario using the api this function will gather all the dat and create a file and make it available for analysis
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + \
        ticker+'&outputsize=full&apikey=' + API_KEY
    req = requests.get(url)
    time.sleep(13)

    req_dict = json.loads(req.text)

    print(req_dict.keys())

    key1 = 'Time Series (Daily)'  # dictionary with all prices by date
    key2 = '4. close'
    # the keys will help seperate and help in filter of the json file to create csv files

    csv_file = open(ticker + ".csv", "w")
    csv_file.write("Date,AAPL\n")
    # file writing process
    write_lines = []
    for date in req_dict[key1]:
        print(date + "," + req_dict[key1][date][key2])  # print key, value
        write_lines.append(date + "," + req_dict[key1][date][key2]+"\n")
    # algo to write data into the files
    # the keys inside are used to filte the data
    write_lines = write_lines[::-1]
    csv_file.writelines(write_lines)
    csv_file.close()

    # this will make the function csv file created for the analysis
    return csv_file

# --------------------------------------------------------------------------------------------------------------------------------
# ///////////////////////////////////////////////////

# Function for Mean Reversion Strategy


def meanReversionStrategy(prices, file):
    print("")
    print("\t !!!!!Starting Mean Reversion Strategy for!!!!!", file)
    print("")
    buy = 0
    iterative_profit = 0
    total_profit = 0
    first_buy = 0
    # Getting back to Moving Average
    i = 0
    for price in prices:
        if i >= 5:
            current_price = price
            moving_average = (prices[i-1] + prices[i-2] +
                              prices[i-3] + prices[i-4] + prices[i-5]) / 5

            # the algorithm and logic to analysis

            if (current_price > 0.95*moving_average) and buy == 0:
                if i == len(prices) - 1:
                    # this does satisfy the project requirement
                    # checking if the buy of sell should happen at the last day
                    print("")
                    print("        YOU SHOULD BUY TODAY")
                    print("")
                buy = current_price
                print("Buying the Stock", buy)
                if first_buy == 0:
                    first_buy = buy
                    # saves the first buy
                    # in a situation where the program starts and satisfies the condition
                    print("The first buy is at: ", first_buy)

            elif (current_price < 1.05*moving_average) and buy != 0:
                if i == len(prices) - 1:
                    # this does satisfy the project requirement
                    # checking if the buy of sell should happen at the last day
                    print("")
                    print("        YOU SHOULD SELL TODAY")
                    print("")
                print("Selling stock at: ", current_price)
                iterative_profit = current_price - buy
                buy = 0
                print("This trade Profit is: ", iterative_profit)
                total_profit += iterative_profit
                print("")

        i += 1  # Iteration changes the loop process

    # Now processing the profits
    print("-----------------------MEAN REVERSION total profits earned from the first buy----------------------")
    final_profit_percent = (total_profit/first_buy) * 100
    print("")
    print("For the Ticker: ", file)
    print("The total profit percentage is: ", final_profit_percent)
    print("The total Profit is: ", total_profit)
    print("")
    print("-----------------------------------------------------------------------------------------------------")

    # the dict will store data for the various profits
    mean_reversion_dict[file] = {
        'total profit': total_profit,
        'profit percent': final_profit_percent}
    return total_profit, final_profit_percent
    # this will return the total and percent of profit of various ticker

# //////////////////////////////////////////////////

# Function for simple moving average


def simpleMovingAverage(prices, file):
    print("")
    print("\t !!!!!Starting Simple Moving Average for!!!!!", file)
    print("")
    buy = 0
    iterative_profit = 0
    total_profit = 0
    first_buy = 0

    # Getting back to Moving Average
    i = 0
    for price in prices:
        if i >= 5:
            current_price = price
            moving_average = (
                prices[i-1] + prices[i-2] + prices[i-3] + prices[i-4] + prices[i-5]) / 5
            # print("The Moving Average for last 5 days is", moving_average)

            if (current_price > moving_average) and buy == 0:
                if i == len(prices) - 1:
                    print("")
                    print("        YOU SHOULD BUY TODAY")
                    print("")
                buy = current_price
                print("Buying the Stock", buy)
                if first_buy == 0:
                    first_buy = buy
                    print("The first buy is at: ", first_buy)

            # the conditions are the algorithmic logics to make the simple moving avg work
            elif (current_price < moving_average) and buy != 0:
                if i == len(prices) - 1:
                    print("")
                    print("      YOU SHOULD SELL TODAY")
                    print("")
                print("Selling stock at: ", current_price)
                iterative_profit = current_price - buy
                buy = 0
                print("This trade Profit is: ", iterative_profit)
                total_profit += iterative_profit
                print("")

        i += 1  # Iteration changes the loop process

    # Now processing the profits
    print("-----------------------SIMPLE MOVING AVERAGE total profits earned from the first buy----------------------")
    # this will provide the profit percent since the first buy
    final_profit_percent = (total_profit/first_buy) * 100
    print("")
    print("For the Ticker: ", file)
    print("The total profit percentage is: ", final_profit_percent)
    print("The total Profit is: ", total_profit)
    print("")
    print("-----------------------------------------------------------------------------------------------------")

    # this will make this dict store all the iterative changes along the for loop for various tickers
    simple_average_dict[file] = {
        'total profit': total_profit,
        'profit percent': final_profit_percent}
    return total_profit, final_profit_percent
    # this function will return the profit and percent which will be later on used inside the other functions

# ///////////////////////////////////////////////////////////

# This is a Bollinger bands algorithm analysis


def bb(prices, file):
    print("")
    print("\t !!!!!!Starting Bollinger Bands Strategy for!!!!!!", file)
    print("")
    buy = 0
    iterative_profit = 0
    total_profit = 0
    first_buy = 0

    # Getting back to Moving Average
    i = 0
    for price in prices:
        if i >= 5:
            current_price = price
            moving_average = (prices[i-1] + prices[i-2] +
                              prices[i-3] + prices[i-4] + prices[i-5]) / 5
            # print("The Moving Average for last 5 days is", moving_average)
            # this point provides the moving average, where the 5 places inside an array makes sure that the avg is of only 5

            if (current_price < 0.95*moving_average) and buy == 0:
                if i == len(prices) - 1:
                    # the print statement above does satisfy the condition for the project
                    # the condition checks if the last data point is the place where it needs to be sold or bought
                    print("")
                    print("       YOU SHOULD BUY TODAY")
                    # the print statement above does satisfy the condition for the project
                    # the condition checks if the last data point is the place where it needs to be sold or bought
                    print("")
                buy = current_price
                print("Buying the Stock", buy)
                if first_buy == 0:
                    first_buy = buy
                    print("The first buy is at: ", first_buy)

            # the algo of bollinger bands working
            elif (current_price > 1.05*moving_average) and buy != 0:
                # the print statement above does satisfy the condition for the project
                # the condition checks if the last data point is the place where it needs to be sold or bought
                if i == len(prices) - 1:
                    print("")
                    print("      YOU SHOULD SELL TODAY")
                    # the print statement above does satisfy the condition for the project
                    # the condition checks if the last data point is the place where it needs to be sold or bought
                    print("")
                print("Selling stock at: ", current_price)
                iterative_profit = current_price - buy
                buy = 0
                print("This trade Profit is: ", iterative_profit)
                total_profit += iterative_profit
                print("")

        i += 1  # Iteration changes the loop process

    # Now processing the profits
    print("-----------------------BOLLINGER BANDS total profits earned from the first buy----------------------")
    final_profit_percent = (total_profit/first_buy) * 100
    print("")
    print("For the Ticker: ", file)
    print("The total profit percentage is: ", final_profit_percent)
    print("The total Profit is: ", total_profit)
    print("")
    print("-----------------------------------------------------------------------------------------------------")

    # this global dict is used to store the values, such later on it is easy to be used inside the json dump
    bb_dict[file] = {
        'total profit': total_profit,
        'profit percent': final_profit_percent}

    return total_profit, final_profit_percent
    # this function will return the profit and percent which will be later on used inside the other functions


# /////////////////////////////////////////////////
# results function will be the one using and calling all other functions in this project
def results():
    # final result is the huge dict under which other dics will come together
    final_result = {}
    # the variable to check the max profit ticker
    high_returns = 0
    high_returns_ticker = ""
    high_returns_strategy = ""
    high_returns_percent = 0
    print("")
    print("")
    print("!!!The final project API requests are at an interval of 13 seconds each!!!")
    print("")
    # tickers are the name of the companies that the api can undertand
    tickers = ['AAPL', 'CSCO', 'FB', 'GOOGL',
               'JPM', 'MSFT', 'TMUS', 'TSLA', 'TTM', 'XOM']
    for ticker in tickers:
        if path.isfile(ticker + ".csv"):
            append(ticker)
        else:
            process_json(ticker)
        # the if and else statement above is the backbone of this program, providing the data from api
        # the functions append and process_json work quite differently
        # if the file exists - append with check for latest data and update it if the file is outdated
        # if the file is not available the process_json will create a new file and write all the data in it
        file = open(ticker+".csv")
        # the ticker are the various other companies
        # the open function opens the files and performs the function as described
        # lines in here is the lines inside the file
        lines = file.readlines()[1:]
        # prices is used to create an array of float values of data inside file
        # split function is used to remove the date part of the file
        prices = [float(line.split(",")[1]) for line in lines]

        # The for loop provides an env where all the strategies are ran and the values are compared making it very easy for the user
        total_profit, final_profit_percent = simpleMovingAverage(
            prices,ticker+".csv")
        if total_profit > high_returns:
            high_returns = total_profit
            high_returns_ticker = ticker
            high_returns_percent = final_profit_percent
            high_returns_strategy = "Simple Moving Average"
        # the if condition helps in checking the values and finding the max, with each loop the values change
        total_profit, final_profit_percent = meanReversionStrategy(
            prices,ticker+".csv")
        if total_profit > high_returns:
            high_returns = total_profit
            high_returns_ticker = ticker
            high_returns_percent = final_profit_percent
            high_returns_strategy = "Mean Reversion"
        # The return values from various functions are recorded here to get the max return value
        total_profit, final_profit_percent = bb(
            prices, ticker+".csv")
        if total_profit > high_returns:
            high_returns = total_profit
            high_returns_ticker = ticker
            high_returns_percent = final_profit_percent
            high_returns_strategy = "Simple Moving Average"

    # The final result is used as a big dictionary containing all the other dict values
    final_result["simpleMovingAverage"] = simple_average_dict
    # final result dict is filled with keys and adjacent needed values which can be further modified
    final_result["meanReversionStrategy"] = mean_reversion_dict
    final_result["bb"] = bb_dict

    # The final result is the dict, the max profit key holds the value of the max return
    final_result["MAX PROFIT"] = {"ticker": high_returns_ticker,
                                  "strategy": high_returns_strategy,
                                  "returns": high_returns,
                                  "percent": high_returns_percent}

    print("")
    print("CHECK THE JSON FILE")
    print("")

    # JSON FILE results.json
    with open('results.json', 'w', encoding='utf8') as json_file:

        # the json file is dumped with indent and divided values and information, which makes it easy to read
        json_file.write('Simple Moving Average')
        json.dump(simple_average_dict, json_file, indent=6, ensure_ascii=True)
        json_file.write('\n')

        json_file.write('Mean Reversion')
        json.dump(mean_reversion_dict, json_file, indent=6, ensure_ascii=True)
        json_file.write('\n')

        json_file.write('Bollinger Bands')
        json.dump(bb_dict, json_file, indent=6, ensure_ascii=True)
        json_file.write('\n')

        json_file.write('Max Return')
        json.dump(final_result["MAX PROFIT"], json_file,
                  indent=6, ensure_ascii=True)
        json_file.write('\n')

    json_file.close
    # after writing the details inside the file, it needs to be closed


# The program runs from here
results()