def reuter_data(stock, data, period, folder_name, csv_name):
    url = "https://www.reuters.com/companies/" + stock + "/financials/" + data + "-" + period
    print(url)
    read_data = urlopen(url).read()
    soup = BeautifulSoup(read_data, 'html.parser')
    table = soup.find_all("tr")

    final_list = []
    index = 0

    while index < len(table):  # iteration of loop depends on number of rows in table
        temp_list = []  # Start loop with an empty list
        for line in table[index]:  # iteration of loop depends on number of item in a row (or number of column)
            temp_list.append(line.text)  # append all item in current row in a list
        final_list.append(temp_list)  # append temp list and forms a row
        index += 1  # index increment to go to the next row
    df = pd.DataFrame(final_list[1:])  # store data into data frame starting from row 1 until the end
    print(df)
    print("Storing data to", folder_name)
    new_file_name = os.path.join(folder_name, csv_name)  # path for new file
    df.to_csv(new_file_name, index=False)  # store data frame in .csv form
    print(csv_name, "saved to", folder_name)


class FindStock:

    def __init__(self, stock):
        stock = stock.replace(" ", "+")
        url = "https://www.reuters.com/search/news?blob="
        search = url + stock
        self.stock = stock
        self.url = search
        read_data = urlopen(search).read()
        self.soup = BeautifulSoup(read_data, 'html.parser')
        self.result_list = []



    def company_name(self):
        result_list =[]
        search_results = self.soup.find_all("div", class_='search-stock-ticker')
        for i in search_results:
            result_list.append(i.text)

        return result_list[0]

    def exchange(self):
        result_list = []
        search_results = self.soup.find_all("div", class_='search-stock-exchange')
        for i in search_results:
            result_list.append(i.text.replace("\r\n    ", ""))
        return result_list[0]

    def ticker(self):
        ticker = self.company_name().split(" ")
        ticker = ticker[-1].replace("(","")
        ticker = ticker.replace(")", "")
        return ticker


    def company_name_without_ticker(self):
        split = self.company_name().split(" ")
        comp_name = self.company_name().replace(split[-1],"")
        return comp_name[:-1]

    def file_name(self):
        file_name = self.company_name_without_ticker().replace(" ","_")
        file_name = file_name.replace("-", "_")
        return file_name


def create_folder(company_name):
    folder_name = os.path.join(target, company_name)
    try:
        os.mkdir(folder_name)
        print("Create folder for", folder_name)
    except FileExistsError:
        print(stock, "folder already exist")

def stock_info(name, exchange, ticker):
    print("Company Name:", name)
    print("Stock Exchange:", exchange)
    print("Stock Ticker:", ticker)

def stock_input():
    global symbol, stock, company_name, exchange, ticker, file_name, stock_info
    j = 0
    while j<1:
        try:
            symbol = input("Please enter stock: ")
            stock = FindStock(symbol)
            company_name = stock.company_name_without_ticker()
            exchange = stock.exchange()
            ticker = stock.ticker()
            file_name = stock.file_name()
            j = 1
        except IndexError:
            print("Unable to find", symbol, "in Reuters")
            print("Please enter a valid symbol")
            continue

import os, re, os.path
import pandas as pd
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

target = "D:\\Stocks_Financial_Data\\Reuter\\"
i=0

stock_input()
stock_info(company_name, exchange, ticker)

while i < 1:

    print("\n")
    print("Please select an option\n")
    print("1. Display Stock Profile")
    print("2. Select Stock")
    print("3. Web Scrap Financial Statements")
    print("")

    choice = input("Enter input: ")
    print("\n")

    if choice == '1':
        stock_info(company_name, exchange, ticker)


    elif choice == '2':
        stock_input()
        stock_info(company_name, exchange, ticker)

    elif choice == '3':
        print("Scraping data for", company_name)

        folder_name = os.path.join(target, company_name)
        try:
            os.mkdir(folder_name)
            print("Create folder for", folder_name)
        except FileExistsError:
            print(folder_name, "already exist")

        data_list = ["income-statement", "balance-sheet", "cash-flow"]
        period_list = ["annual", "quarterly"]

        for data in data_list:
            for period in period_list:
                csv_name = file_name + "_" + data + "_" + period + ".csv"  # determine file name after data frame is completed
                reuter_data(ticker, data, period, folder_name, csv_name)
    else:
        print("Please Enter valid choice")


