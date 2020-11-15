def reuter_data(stock, data, period, new_name, folder_name):
    url = "https://www.reuters.com/companies/" + stock + "/financials/" + data + "-" + period
    print(url)
    read_data = urlopen(url).read()
    soup = BeautifulSoup(read_data, 'html.parser')
    table = soup.find_all("tr")

    final_list = []
    index = 0

    while index < len(table): # iteration of loop depends on number of rows in table
        temp_list = [] # Start loop with an empty list
        for line in table[index]: # iteration of loop depends on number of item in a row (or number of column)
            temp_list.append(line.text) # append all item in current row in a list
        final_list.append(temp_list) # append temp list and forms a row
        print(final_list[index])
        index += 1 # index increment to go to the next row
    file_name = new_name + "_" + data + "_" + period + ".csv" # determine file name after data frame is completed
    print("Storing data to", file_name)
    new_file_name = os.path.join(folder_name, file_name) # path for new file
    df = pd.DataFrame(final_list[1:]) # store data into data frame starting from row 1 until the end
    df.to_csv(new_file_name, index=False) # store data frame in .csv form
    print(file_name, "saved to", folder_name)

def company_name(stock):
    stock_name=[]
    url = "https://www.reuters.com/companies/" + stock + "/financials/"
    read_data = urlopen(url).read()
    soup = BeautifulSoup(read_data, 'html.parser')
    item = soup.find_all("h1") # find header of the url
    for i in item:
        stock_name = (i.text)
    return stock_name

def create_folder():
    try:
        os.mkdir(folder_name)
        print("Create folder for", folder_name)
    except FileExistsError:
        print(stock, "folder already exist")

import os, re, os.path
import pandas as pd
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

target = "D:\\Stocks_Financial_Data\\Reuter\\"

stock = input("Please enter stock: ")
stock_name = company_name(stock)
print("Scraping data for", stock_name)
folder_name = os.path.join(target, stock_name)

create_folder()

new_name = stock_name.replace(" " , "_")
new_name = new_name.replace("-" , "_") # new_name is name used for naming files later
data_list = ["income-statement", "balance-sheet", "cash-flow"]
period_list = ["annual", "quarterly"]



for data in data_list:
    for period in period_list:
        reuter_data(stock, data, period, new_name, folder_name)



