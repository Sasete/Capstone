import tkinter
import ReaderWriter as Stocker
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import ttk
import datetime
import time
import yfinance as yf
import requests, json
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import os
import numpy as np
import pandas as pd
import math
import random
from fiscalyear import *

# isWorking uygulamanin acik olma durumu
isWorking = False


portfolio = Stocker.Portfolio('')

path = ''
fileName = ''

functionThread = ''
killThread = False

stockUpdater = ''
stockUpdate = True

todayDate = datetime.datetime(2021,1,1)
dateChanger = ''
dateChanged = False

pulling = False

progressBar = ''
progressLabel = ''

def Start():


    stockUpdate = True
    stockUpdater = threading.Thread(target=lambda: UpdateAllStocks())

    #stockUpdater.start()

    dateChanged = False
    dateChanger = threading.Thread(target=lambda: TimeCounter())

    dateChanger.start()
    
    NewFile()

def UpdateAllStocks():

    global stockUpdater
    global stockUpdate

    while True:

        if stockUpdate == False:
            stockUpdater.join()
            break
        
            

        stocks = Stocker.ReadFile('./Resources/StockList.txt')

        newStocks = ''

        pullStocks = []

        startTime = time.monotonic()
        for stock in stocks.split('\n'):

            #PullStock(stock)
            pullStocks.append(stock)

        PullStocks(pullStocks)
        
        totalTime = time.monotonic() - startTime

        print("Total elapsed time: " + str(totalTime))

        waitTime = 600
        debug = 'Waiting for ' + str(waitTime) + ' seconds.'
        print(debug)
        time.sleep(waitTime)

    return None

def TimeCounter():


    global dateChanged
    
    while True:

        time.sleep(5)

        dateChanged = True


    return None

def NewFile():

    global path
    global fileName
    global portfolio
    global todayDate

    date = todayDate

    path = './'
    fileName = simpledialog.askstring("Name", "Portfolio name:", parent = main)

    
    portfolio.Initialize()

    portfolio.date = str(date.year) + '-' + str(date.month).zfill(2) + '-' + str(date.day).zfill(2)
    answer = simpledialog.askfloat("Amount", "Start amount:", parent = main, minvalue=0.0)

    if answer is not None:
        portfolio.money = answer
    else:
        portfolio.money = 1000
        
    PortfolioToUI()
    
# dosya çalışmaları için fonksiyonlar oluşturuluyor
def OpenFile():
    
    filetypes = [ ('Portfolio Files', '*.portfolio') ]

    global path
    global fileName
    
    path = tkinter.filedialog.askopenfilename(title = "Open File", initialdir = './', filetypes = filetypes)
    fileName = path.split('/')[-1]    
    path = path[:len(path) - len(fileName)]


    

    extention = fileName.split('.')[-1]
    fileName = fileName[:len(fileName) - (len(extention)+1)]

    global portfolio

    portfolio.Initialize()

    portfolio.name = fileName

    portfolio.Load(path)
    
    PortfolioToUI()
    

def SaveFile():


    global path
    global fileName
    global portfolio

    portfolio.Save(path, fileName)

    print('Saved File!')

def SaveAsFile():
    
    filetypes = [ ('Portfolio Files', '*.portfolio') ]
    
    path = tkinter.filedialog.asksaveasfile(mode='w', title = "Save File", initialdir = './', defaultextension=".portfolio", filetypes = filetypes)

    if path is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    
    global portfolio


    data = portfolio.GetTextToSave()

    path.write(data)
    path.close()

    print('Saved File!')

def PortfolioToUI():

    global portfolio

    print(portfolio.name)

    main.title(portfolio.name)

    #dateText = str(date.year) + '-' + str(date.month).zfill(2) + '-' + str(date.day).zfill(2)
    
    canvasLabel.config(text = portfolio.date)

    GetPortfolioItems()

    value = "{:.2f}".format(portfolio.GetValue(1))

    money = "{:.2f}".format(portfolio.GetValue(2))
    
    stringValue = str(money) + '₺ money + ' + str(value) + '₺ stocks'

    valueLabel.config(text = stringValue)

    PrepareGraph()


def PrepareGraph():

    global portfolio

    dates = []
    values = []
    

    for value in portfolio.valueDatas:

        #print(str(value.date) + ':' + str(value.value))

        #date = datetime.datetime.strptime(value.date,'%Y-%m-%d-%H-%M-%S')

        date = datetime.datetime.strptime(value.date, '%Y-%m-%d')
        
        dates.append(date)
        values.append(value.value)

    dates.append(portfolio.date)
    values.append(portfolio.GetValue(0))

    graphRange = 5

    if len(dates) > graphRange:

        length = len(dates)
        
        dates = dates[length - graphRange: length]
        values = values[length - graphRange: length]
    
    data = {'Dates' : dates, 'Values' : values}
    df = DataFrame(data, columns = ['Dates', 'Values'])

    figure.clear()
    ax = figure.add_subplot(111)
    ax.set_facecolor(systemColor)
    df = df[['Dates', 'Values']].groupby('Dates').sum()
    df.plot(kind='line', legend=True, ax=ax,color='r',marker='o',fontsize=10)
    ax.set_title('Value History')

    line.draw()
    

# portfolio daki itemlari listeye listeleyecek fonksiyon
def GetPortfolioItems():

    global portfolio


    itemList.delete(0, tkinter.END)


    # burada PortfolioToUI() çalışması gerek. Şimdilik sadece stockları yerine koyuyor.
    for stockData in portfolio.stockDatas:

        itemList.insert(tkinter.END, stockData.name + '\tx' + str(stockData.amount))



# portfolio nun toplam degerini hesaplayacak fonksiyon
def CalculateValue():

    global portfolio

    value= 0
    
    order = 0
    for stockData in portfolio.stockDatas:

        
        stock = Stocker.Stock(stockData.name)

        stock.Initialize()

        stock.name = stockData.name

        stock.Load('./Resources/Stocks/')

        #stock.Print()

        value += float(stock.stockDates[-1].infos[0].info) * stockData.amount


        order += 1


    return value

def CalculateValueAsOne():

    global portfolio

    value= portfolio.money
    
    order = 0
    for stockData in portfolio.stockDatas:

        
        stock = Stocker.Stock(stockData.name)

        stock.Initialize()

        stock.name = stockData.name

        stock.Load('./Resources/Stocks/')

        #stock.Print()

        value += float(stock.stockDates[-1].infos[0].info) * stockData.amount


        order += 1


    return value


# portfolio ya belirtilen item i ekleyecek fonksiyon
def AddItem():

    item_name = itemName.get().upper()

    print(item_name)
    
    if item_name == 'Item Shortcut' or item_name.isspace():

        print('You need an item name')

        return


    stockInfo = PullStock(item_name)

    if stockInfo is None:

        return

    if DoesStockExist():

        print('Stock is already exist...')
        
        return
    global portfolio
    
    # Add Amount is the second parameter.
    stockData = Stocker.StockData(item_name, 0)

    portfolio.AddStock(stockData)

    #date = datetime.datetime.now()

    #dateString = str(date.year) + '-' + str(date.month).zfill(2) + '-' + str(date.day).zfill(2) + '-' + str(date.hour).zfill(2) + '-' + str(date.minute).zfill(2) + '-' + str(date.second).zfill(2)

    #value = CalculateValueAsOne()

    #valueData = Stocker.ValueData(dateString, float(value))

    #portfolio.AddValueData(valueData)

    PortfolioToUI()

    #SaveFile()

def AddStockItem(stockName):

    item_name = stockName.upper()

    print(item_name)
    
    if item_name == 'Item Shortcut' or item_name.isspace():

        print('You need an item name')

        return


    stockInfo = PullStock(item_name)

    if stockInfo is None:

        return

    if DoesStockExist():

        print('Stock is already exist...')
        
        return
    global portfolio
    
    # Add Amount is the second parameter.
    stockData = Stocker.StockData(item_name, 0)

    portfolio.AddStock(stockData)

    #date = datetime.datetime.now()

    #dateString = str(date.year) + '-' + str(date.month).zfill(2) + '-' + str(date.day).zfill(2) + '-' + str(date.hour).zfill(2) + '-' + str(date.minute).zfill(2) + '-' + str(date.second).zfill(2)

    #value = CalculateValueAsOne()

    #valueData = Stocker.ValueData(dateString, float(value))

    #portfolio.AddValueData(valueData)

    PortfolioToUI()

    #SaveFile()
    

def DoesStockExist():

    retVal = False
    
    global portfolio

    stockName = itemName.get()

    for item in itemList.get(0,tkinter.END):
        
        item_name = item.split('\t')[0]

        if item_name == stockName:

            retVal = True
            



    return retVal

def PullStocks(stockList, daysBefore = 0):

    global pulling

    if pulling == True:
        return None

    pulling = True
    
    stockNames = ""

    for stock in stockList:

        stockNames += stock + " "


    stockNames = stockNames[:-1]

    global todayDate
    date = todayDate

    starty = 60
    b = datetime.timedelta(days = starty)
    a = datetime.timedelta(days = daysBefore)
    
    dateA = date - a
    dateB = date - b

    while np.busday_count(dateB.date(), dateA.date()) > 37:

        #print(np.busday_count(dateB.date(), dateA.date()))

        starty -= 1

        b = datetime.timedelta(days = starty)
    
        dateB = date - b

    startDate = str(dateB.year) + '-' + str(dateB.month).zfill(2) + '-' + str(dateB.day).zfill(2)
    endDate = str(dateA.year) + '-' + str(dateA.month).zfill(2) + '-' + str(dateA.day).zfill(2)

    startTime = time.monotonic()
    stockData = yf.download(tickers = stockNames, start = startDate, end = endDate, progress = False)
    downloadTime = time.monotonic()

    #print(stockData)

    print(str(len(stockList)) + "x stocks downloaded in " + str(downloadTime - startTime))
    #stockData.head()

    #print(stockData)

    stocks = []

    elapseTime = downloadTime
    
    for stock in stockList:

        stockFrame = stockData.iloc[:, stockData.columns.get_level_values(1) == stock]

        #print(stockFrame)

        currentStock = Stocker.Stock(stock)
        
        currentStock.Initialize()
        currentStock.name = stock

        # Timer starts
        
        for i in range(len(stockFrame[:])):
            
            # First 26 value should be passed
            if i <= 26:
                continue
        
            stringVal = str(str(stockFrame.iloc[i].name).split(' ')[0]) + ":"


            #stockDate = Stocker.StockDateData()

            #stockDate.date = str(str(stockFrame.iloc[i].name).split(' ')[0])


            for j in range(len(stockFrame.iloc[i][:])):


                dataName = str(stockFrame.columns[j][0])
                data = str(stockFrame.iloc[i][j])
                #dateInfo = Stocker.DateInfo()

                stringVal += "\"" + dataName + "\"" + data + ","
                
                #dateInfo.name = str(stockFrame.columns[j][0])
                #dateInfo.info = str(stockFrame.iloc[i][j])

                #stockDate.infos.append(dateInfo)


            
            longList = stockFrame.iloc[i - 26: i]
            shortList = stockFrame.iloc[i - 12: i]
            rsList = stockFrame.iloc[i - 15: i]
            twentyList = stockFrame.iloc[i-20:i]
        
            
            tS = time.monotonic()
            
            short_avg = GetAverage(shortList, "Close")
            long_avg = GetAverage(longList, "Close")
            twenty_avg = GetAverage(twentyList, "Close")
            sigma = GetSigma(twentyList, "Close")
            lowerBand, upperBand = (twenty_avg - (2 * sigma) , twenty_avg + (2 * sigma))
            

            rs = GetRS(rsList)
            
            #print("StockTime: " + str(time.monotonic() - tS))
            
            rsi = float(100 - (100 / ( 1 + rs )))
            

            stringVal += "\"LongAverage\"" + str(long_avg) + ","
            stringVal += "\"ShortAverage\"" + str(short_avg) + ","
            stringVal += "\"TwentyAverage\"" + str(twenty_avg) + ","
            stringVal += "\"Sigma\"" + str(sigma) + ","
            stringVal += "\"UpperBand\"" + str(upperBand) + ","
            stringVal += "\"LowerBand\"" + str(lowerBand) + ","
            stringVal += "\"RSI\"" + str(rsi) + ","
            

            stringVal = stringVal[:-1]

            stockDate = Stocker.StockDateData()

            #print(stringVal)
            
            stockDate.Read(stringVal)

            #longInfo = Stocker.DateInfo("LongAverage", str(long_avg))
            #shortInfo = Stocker.DateInfo("ShortAverage", str(short_avg))
            #rsiInfo = Stocker.DateInfo("RSI", str(rsi))

            #stockDate.infos.append(longInfo)
            #stockDate.infos.append(shortInfo)
            #stockDate.infos.append(rsiInfo)


            currentStock.AddStockDate(stockDate)

        #timer ends
        elapsedTime = time.monotonic()

        passedTime = elapsedTime - elapseTime
        elapseTime = elapsedTime
        #timer starts again
        
        print(currentStock.name + ' prepared in ' + str(passedTime))


            
        currentStock.Save('./Resources/Stocks/')
    print("Pull Success!")

    pulling = False
        
            

def PullStock(stockName, daysBefore = 0):
    
    global pulling

    if pulling == True:
        return None

    pulling = True
    
    global todayDate

    #print(todayDate)

    #try:
    date = todayDate


    starty = 60

    b = datetime.timedelta(days = starty)
    a = datetime.timedelta(days = daysBefore)
    

    dateA = date - a
    dateB = date - b

    while np.busday_count(dateB.date(), dateA.date()) > 37:

        #print(np.busday_count(dateB.date(), dateA.date()))

        starty -= 1

        b = datetime.timedelta(days = starty)
    
        dateB = date - b


    startDate = str(dateB.year) + '-' + str(dateB.month).zfill(2) + '-' + str(dateB.day).zfill(2)
    endDate = str(dateA.year) + '-' + str(dateA.month).zfill(2) + '-' + str(dateA.day).zfill(2)

    #stockData = yfTicker.history(start = startDate, end = endDate)

    startTime = time.monotonic()
    stockData = yf.download(stockName, start = startDate, end = endDate, progress = False)
    downloadTime = time.monotonic()

    print(stockName + " downloaded in " + str(downloadTime - startTime))

    

    #print(startDate + ':' + endDate + ':' + str(np.busday_count(dateB.date(), dateA.date())))

    #stockData.head()

    #print(stockData)

    if len(stockData.head().index) > 0:
        
        stock = Stocker.Stock(stockName)

        stock.Initialize()
        stock.name = stockName
    
        for i in range(len(stockData)):

            column = stockData.iloc[i,]
            
            if i <= 26:
                    
                #date = str(column).split('Name:')[1].split(' ')[1]

                #print(date + ' passed!')
    
                continue



            
            date = str(column).split('Name:')[1].split(' ')[1]

            #print("Pulled Date: " + date)

            stringVal = date + ":"

            order = 0
            for dat in stockData.iloc[i]:

                data = str(column).split('\n')[order].split(' ')[0]
            
                #print("DATA" + data)
            
                stringVal += "\"" + data + "\"" + str(dat) + ","

                #print(dat)
            
                order += 1

            #TODO RSI RS SHORT_AVG ve LONG_AVG kayıt etmemiz gerekiyor.

            longList = stockData.iloc[i - 26: i]
            shortList = stockData.iloc[i - 12: i]
            rsList = stockData.iloc[i - 15: i]
            twentyList = stockData.iloc[i-20:i]

            short_avg = GetAverage(shortList, "Close")
            long_avg = GetAverage(longList, "Close")
            twenty_avg = GetAverage(twentyList, "Close")
            sigma = GetSigma(twentyList, "Close")
            lowerBand, upperBand = (twenty_avg - (2 * sigma) , twenty_avg + (2 * sigma))
            #rsHigh_avg = GetAverage(rsList, "High")
            #rsLow_avg = GetAverage(rsList, "Low")

            rs = GetRS(rsList)

            rsi = float(100 - (100 / ( 1 + rs )))

            stringVal += "\"LongAverage\"" + str(long_avg) + ","
            stringVal += "\"ShortAverage\"" + str(short_avg) + ","
            stringVal += "\"TwentyAverage\"" + str(twenty_avg) + ","
            stringVal += "\"Sigma\"" + str(sigma) + ","
            stringVal += "\"UpperBand\"" + str(upperBand) + ","
            stringVal += "\"LowerBand\"" + str(lowerBand) + ","
            stringVal += "\"RSI\"" + str(rsi) + ","

            stringVal = stringVal[:-1]

            stockDate = Stocker.StockDateData()
            stockDate.Read(stringVal)

            stock.AddStockDate(stockDate)
        

        elapsedTime = time.monotonic()

        print(stockName + " prepared in " + str(elapsedTime - downloadTime))
        
        stock.Save('./Resources/Stocks/')
        print("Pull Success!")
        pulling = False
        return stock

    else:
            
        pulling = False
        print('Couldn\'t find stock...')
        return None
            
    
    #except:
        #print('Couldn\'t find stock...')
        #return None


def PullStocks4Matrix(stockList, daysBefore = 0):

    global pulling

    if pulling == True:
        return None

    pulling = True
    
    stockNames = ""

    for stock in stockList:

        stockNames += stock + " "


    stockNames = stockNames[:-1]

    global todayDate
    date = todayDate

    starty = 130
    b = datetime.timedelta(days = starty)
    a = datetime.timedelta(days = daysBefore)
    
    dateA = date - a
    dateB = date - b

    while np.busday_count(dateB.date(), dateA.date()) > 100:

        #print(np.busday_count(dateB.date(), dateA.date()))

        starty -= 1

        b = datetime.timedelta(days = starty)
    
        dateB = date - b

    startDate = str(dateB.year) + '-' + str(dateB.month).zfill(2) + '-' + str(dateB.day).zfill(2)
    endDate = str(dateA.year) + '-' + str(dateA.month).zfill(2) + '-' + str(dateA.day).zfill(2)

    startTime = time.monotonic()
    stockData = yf.download(tickers = stockNames, start = startDate, end = endDate, progress = False, group_by = "ticker", threads = True)
    downloadTime = time.monotonic()

    #print(stockData)

    print(str(len(stockList)) + "x stocks downloaded in " + str(downloadTime - startTime))
    #stockData.head()

    #print(stockData
    
    elapseTime = downloadTime

    lastDataFrame = DataFrame()

    dataFrame = {}

    #dataFrame["index"] = stockData.index

    rate = 0
    for stock in stockList:


        closeValues = stockData[stock]["Close"].values

        cashFlow = [None] * len(closeValues)

        for i in range(len(closeValues)):

            if i == 0:

                cashFlow[i] = 0

                continue

            cashFlow[i] = closeValues[i] - closeValues[i - 1]

            
        dataFrame[stock] = cashFlow

        rate += 1

        UpdateProgressBar( 100 * (rate / len(stockList)) / 3, 'Pulling stock data...')


    
    lastDataFrame = pd.DataFrame.from_dict(dataFrame)
    lastDataFrame.index = stockData.index

    #print(lastDataFrame)

    #pd.concat(dataFrames, axis = 1)
    
    print("Pull Success!")

    pulling = False

    return lastDataFrame

def GetMarkovitzMatrix(dataFrame, stockNames):

    m = len(stockNames)

    markovitzMatrix = np.zeros((m, m))


    rate = 0
    
    y = 0
    for firstStock in stockNames:

        x = 0
        r = 0
        for secondStock in stockNames:

            bothTop = 0
            xTop = 0
            yTop = 0
            x2Top = 0
            y2Top = 0
            n = len(dataFrame)


            for date in range(len(dataFrame)):


                bothTop += (float(dataFrame[firstStock][date]) * float(dataFrame[secondStock ][date]))

                xTop += float(dataFrame[firstStock][date])
                yTop += float(dataFrame[secondStock][date])

                x2Top += float(dataFrame[firstStock][date]) ** 2
                y2Top += float(dataFrame[secondStock][date]) ** 2


            


            r = ((n * bothTop) - (xTop * yTop)) / math.sqrt( ( (n * x2Top) - (xTop ** 2) ) * ( (n * y2Top) - (yTop ** 2) ) )

            #print( firstStock + 'x' + secondStock + ' R = ' + str(r))
            
            markovitzMatrix[x][y] = r

            rate += 1


            UpdateProgressBar( 33 + (100 * (rate / (len(stockNames) ** 2)) / 3), 'Calculating CashFlow Matrix...')
            
            x += 1

        rate += 1
        
        UpdateProgressBar( 33 + (100 * (rate / (len(stockNames) ** 2)) / 3), 'Calculating CashFlow Matrix...')

        y += 1
        
    dataFrame = DataFrame(markovitzMatrix, columns = stockNames)
    dataFrame.index = stockNames

    print(dataFrame)

    return dataFrame

def Markovitz(markovitzMatrix ,state = "LowRisk", stockAmount = 3):

    stocks = []

    if state == "LowRisk":

        stocks.append('ARCLK.IS')
        stocks.append('DOHOL.IS')
        stocks.append('YATAS.IS')

    if state == "MediumRisk":

        stocks.append('KARSN.IS')
        stocks.append('AEFES.IS')
        stocks.append('ALBRK.IS')

    if state == "HighRisk":

        stocks.append('BERA.IS')
        stocks.append('BIMAS.IS')
        stocks.append('BRISA.IS')




    return stocks
    
# listedeki seçili item in arayüzünü açacak fonksiyon
def EditItem():

    stringValue = itemList.get(tkinter.ACTIVE).split('\t')[0]

    Stocker.WriteFile('./Temp.txt', stringValue)

    Stocker.Open('./Stock.py', True)
    

# listedeki seçili item i portfolio dan çikaracak olan fonksiyon 
def RemoveItem():

    stringValue = itemList.get(tkinter.ACTIVE)

    stockName = stringValue.split('\t')[0]
    stockAmount = int(stringValue.split('\t')[1].split('x')[1])
    
    stockData = Stocker.StockData(stockName, stockAmount)

    global portfolio

    portfolio.RemoveStock(stockData)

    PortfolioToUI()

    #SaveFile()

# degeri arayüz için alan fonksiyon
def GetValue():

    return '0'

def GetAverage(values, dataType):
    
    stockFrame = values.iloc[:, values.columns.get_level_values(0) == dataType]

    average = float(stockFrame[dataType].mean())
    
    return average

def GetSigma(values, dataType):
    
    stockFrame = values.iloc[:, values.columns.get_level_values(0) == dataType]

    average = float(stockFrame[dataType].mean())

    count = float(stockFrame[dataType].count())

    data = stockFrame[dataType].values

    val = 0
    for dat in data:
        val += (dat - average) ** 2

    if count >= 1:
        sigma = math.sqrt(val / count)
    else:
        sigma = math.sqrt(val / 1)

    return sigma
    

def GetRS(values):
    
    data = values["Close"].values

    upSum = 0
    lowSum = 0
        
    for i in range(len(data)):

        #print(closeList[i])

        if i == 0:

            continue

        rs = data[i] - data[i - 1]

        if rs < 0:
            lowSum += -rs
        else:
            upSum += rs
            

    if lowSum >= 1:
        rs = upSum / lowSum
    else:
        rs = upSum / (lowSum + 1)


    return rs

def BollingerBand(stock):

    global portfolio

    twentyAvg = float(stock.GetDate(portfolio.date).GetInfo('TwentyAverage').info)
    
    sigma = float(stock.GetDate(portfolio.date).GetInfo('Sigma').info)

    upperBand = twentyAvg + (2 * sigma)
    lowerBand = twentyAvg - (2 * sigma)


    return (lowerBand, upperBand)


def LowRiskSuggest():

    InitializeProgressBar()
    
    UpdateProgressBar(0, 'Downloading...')

    stockNames = Stocker.ReadFile('./Resources/StockList.txt').split('\n')

    startTime = time.monotonic()

    dataFrame = PullStocks4Matrix(stockNames)
        
    totalTime = time.monotonic() - startTime
    
    UpdateProgressBar(33, 'Net Cash Flow Matrix.')


    markovitzMatrix = GetMarkovitzMatrix(dataFrame, stockNames)

    stockAmount = simpledialog.askinteger("Amount", "Stock amount:", parent = main, minvalue=3, maxvalue=5)

    UpdateProgressBar(67, 'Using Markovitz...')

    # stock_names = yeni alınacak olan stoklar
    stock_names = Markovitz(markovitzMatrix, "LowRisk", stockAmount)

    UpdateProgressBar(100, 'Done')

    time.sleep(0.1)
                                         
    UpdateProgressBar(0, 'Adding Stocks...')

                                         
    order = 0
    for stock_name in stock_names:

        UpdateProgressBar( 100 * order / (len(stock_names)), stock_name)

        AddStockItem(stock_name)

        order += 1

    
    UpdateProgressBar(100, 'Done')

    time.sleep(0.1)
                                         
    EndProgressBar()
    
    return

def MediumRiskSuggest():

    InitializeProgressBar()
    
    UpdateProgressBar(0, 'Downloading...')

    stockNames = Stocker.ReadFile('./Resources/StockList.txt').split('\n')

    startTime = time.monotonic()

    dataFrame = PullStocks4Matrix(stockNames)
        
    totalTime = time.monotonic() - startTime
    
    UpdateProgressBar(33, 'Net Cash Flow Matrix.')


    markovitzMatrix = GetMarkovitzMatrix(dataFrame, stockNames)

    stockAmount = simpledialog.askinteger("Amount", "Stock amount:", parent = main, minvalue=3, maxvalue=5)

    UpdateProgressBar(67, 'Using Markovitz...')

    # stock_names = yeni alınacak olan stoklar
    stock_names = Markovitz(markovitzMatrix, "MediumRisk", stockAmount)

    UpdateProgressBar(100, 'Done!')
                                         
    time.sleep(0.1)
                                         
    UpdateProgressBar(0, 'Adding Stocks...')

                                         
    order = 0
    for stock_name in stock_names:

        UpdateProgressBar( 100 * order / (len(stock_names)), stock_name)

        AddStockItem(stock_name)

        order += 1

    
    UpdateProgressBar(100, 'Done')

    time.sleep(0.1)
                                         
    EndProgressBar()

    return

def HighRiskSuggest():

    InitializeProgressBar()
    
    UpdateProgressBar(0, 'Downloading...')

    stockNames = Stocker.ReadFile('./Resources/StockList.txt').split('\n')

    startTime = time.monotonic()

    dataFrame = PullStocks4Matrix(stockNames)
        
    totalTime = time.monotonic() - startTime
    
    UpdateProgressBar(33, 'Net Cash Flow Matrix.')


    markovitzMatrix = GetMarkovitzMatrix(dataFrame, stockNames)

    stockAmount = simpledialog.askinteger("Amount", "Stock amount:", parent = main, minvalue=3, maxvalue=5)

    UpdateProgressBar(67, 'Using Markovitz...')

    # stock_names = yeni alınacak olan stoklar
    stock_names = Markovitz(markovitzMatrix, "HighRisk", stockAmount)

    UpdateProgressBar(100, 'Done')

    time.sleep(0.1)
                                         
    UpdateProgressBar(0, 'Adding Stocks...')

                                         
    order = 0
    for stock_name in stock_names:

        UpdateProgressBar( 100 * order / (len(stock_names)), stock_name)

        AddStockItem(stock_name)

        order += 1

    
    UpdateProgressBar(100, 'Done')

    time.sleep(0.1)
                                         
    EndProgressBar()

    return

def InitializeProgressBar(title = "Progressing",label = "Progressing"):

    global progressBar
    global progressLabel
    global progress_var
    
    progressBar = tkinter.Toplevel()
    progressBar.title(title)
    progressBar.resizable(False,False)
    
    progressLabel = tkinter.Label(progressBar, bg = themeColor, width = 30, height = 3, text = label, font = 24, justify = tkinter.CENTER)
    progressLabel.pack(side=tkinter.TOP, fill=tkinter.X)

    progress_bar = ttk.Progressbar(progressBar, variable=progress_var, maximum = 100)
    progress_bar.pack(side=tkinter.BOTTOM, expand = 1, fill=tkinter.X)
    progressBar.pack_slaves()

    return None

def UpdateProgressBar(rate, label = "Progress"):

    global progressBar
    global progressLabel
    global progress_var
    
    progress_var.set(rate)
    progressLabel.config(text = label)
    progressBar.update()

    return None

def EndProgressBar():

    global progressBar

    progressBar.destroy()

    return None



# uygulamanýn alim satimini baslatan fonksiyon
def StartCalculation():

    global isWorking

    global functionThread

    
    global killThread

    # global deki isWorking degerini degistir arayüzü ona göre güncelle
    if isWorking:
        
        isWorking = False
        killThread = True
        
        functionThread.join()
        
        StartButton.config(text = "Start")
        
    else:
        isWorking = True
        killThread = False

        functionThread = threading.Thread(target = FunctionMain)


        functionThread.start()
        
        StartButton.config(text = "Stop")

def FunctionStart():

    print('Thread started.')

    return None

def FunctionMain():

    counter = 0

    FunctionStart()
    
    while True:

        global killThread

        if killThread:

            FunctionExit()
            
            break

        #main thread function here
        CheckFunction()
        
    return None

def FunctionExit():

    print('Thread aborted.')
    
    return None

def CheckFunction():

    global dateChanged
    global todayDate
    global portfolio

    if dateChanged == True:

        #print('Date Changed!')

        dateChanged = False

        todayDate = todayDate + datetime.timedelta(days = 1)

        while not np.is_busday(todayDate.date()):
            
            todayDate = todayDate + datetime.timedelta(days = 1)



        date = str(todayDate.year) + '-' + str(todayDate.month).zfill(2) + '-' + str(todayDate.day).zfill(2)

        portfolio.SetDate(date)

        stockDatas = []

        for stockData in portfolio.stockDatas:

            stockDatas.append(stockData.name)

        PullStocks(stockDatas, -1)

        for stockData in portfolio.stockDatas:

            stock = Stocker.Stock(stockData.name)
            stock.Initialize()
            stock.name = stockData.name

            stock.Load('./Resources/Stocks/')
            
            CheckStocks(stock)

        PortfolioToUI()
    
    return

def CheckStocks(stock):
    
    global portfolio
    global todayDate

    price = float(stock.GetDate(portfolio.date).GetInfo('Close').info)
    macd = float(stock.GetDate(portfolio.date).GetInfo('ShortAverage').info) - float(stock.GetDate(portfolio.date).GetInfo('LongAverage').info)
    rsi = float(stock.GetDate(portfolio.date).GetInfo('RSI').info)

    lowerBand, upperBand = BollingerBand(stock)

    bollingerValue = (price - lowerBand) / (upperBand - lowerBand)

    print('MacD: ' + str(macd) + '\nRSI: ' + str(rsi) + '\nPrice: ' + str(price) + '\n(LowerBand: ' + str(lowerBand) + ",UpperBand:" + str(upperBand) + ")")
    print('BollingerValue: ' + str(bollingerValue))
    
    if macd < 0 and rsi < 30:

        #if bollingerValue <= 0.5:

        bollingerRate = (bollingerValue - 0.5) / 0.5

        if bollingerRate > 1:
            bollingerRate = 1

        minAmount, maxAmount = portfolio.GetAmount(stock, True)

        amount =  int(round(maxAmount * bollingerRate))

        if amount < minAmount:
            amount = minAmount

        portfolio.Buy(stock, amount)

        print(stock.name + 'x' + str(amount) + ' bought')

        return

            
        #print(stock.name + ' bought!')

        #portfolio.Buy(stock)

        #return
    

    if macd > 0 and rsi > 70:

        #if bollingerValue >= 0.5:

        bollingerRate = (bollingerValue) / 0.5

        bollingerRate = bollingerRate ** -1

        if bollingerRate < 0:
            bollingerRate = 0

        minAmount, maxAmount = portfolio.GetAmount(stock, False)

        amount = int(round(maxAmount * bollingerRate))

        if amount < minAmount:
            amount = minAmount

        portfolio.Sell(stock, amount)

        print(stock.name + 'x' + str(amount) + ' sold')

        return


        #print(stock.name + ' sold!')

        #portfolio.Sell(stock)
        

        #return
        
    print(stock.name + ' waited!')            

    return



    

# Tkinter arayüz kurulumu
main = tkinter.Tk()
main.title("Portfolio")
main.resizable(False, False)

# Tema renkleri belirleme kismi
themeColor = "gray"
systemColor = "black"
userColor = "white"


# arayüzün boyutlari
m_height = 100
m_width = 200


# arayüz iç boyutlari
sideSpace = 50
topBottomSpace = 125

# menu ekleme alanı
Menu = tkinter.Menu(main)
main.config(menu = Menu)

fileMenu = tkinter.Menu(Menu, tearoff = 0)
Menu.add_cascade(label = "Files", menu = fileMenu)
fileMenu.add_command(label = "New", command = NewFile)
fileMenu.add_command(label = "Open", command = OpenFile)
fileMenu.add_separator()   #cizgi olusturuyor
fileMenu.add_command(label = "Save", command = SaveFile)
fileMenu.add_command(label = "Save as", command = SaveAsFile)


editMenu = tkinter.Menu(Menu, tearoff = 0)
Menu.add_cascade(label = "Portfolio", menu = editMenu)
editMenu.add_command(label = "Low Risk Suggestion", command = LowRiskSuggest)
editMenu.add_command(label = "Medium Risk Suggestion", command = MediumRiskSuggest)
editMenu.add_command(label = "High Risk Suggestion", command = HighRiskSuggest)
#editMenu.add_separator()   #cizgi olusturuyor
#editMenu.add_command(label = "")

algorithmMenu = tkinter.Menu(Menu, tearoff = 0)
Menu.add_cascade(label = "Algorithm", menu = algorithmMenu)
#algorithmMenu.add_command(label = "")
#algorithmMenu.add_command(label = "")
#algorithmMenu.add_separator()   #cizgi olusturuyor
#algorithmMenu.add_command(label = "")



# arayüzün tamami
mainFrame = tkinter.Frame(main, bg = themeColor, height = m_height, width = m_width)
mainFrame.pack(side = tkinter.LEFT, fill = tkinter.Y)

# arayüzün baslik kismi
titleFrame = tkinter.Frame(mainFrame, bg = themeColor, width = m_width, height = 30)
titleFrame.pack(side = tkinter.TOP, fill = tkinter.X)

# arayüzün alt kismi
bottomFrame = tkinter.Frame(mainFrame, bg = themeColor, width = m_width, height = 30)
bottomFrame.pack(side = tkinter.BOTTOM, fill = tkinter.X)

# liste için scrollbar kismi
scrollbar = tkinter.Scrollbar(mainFrame)
scrollbar.pack(side = tkinter.LEFT, fill = tkinter.Y)

# item larin listelenecegi yer
itemList = tkinter.Listbox(mainFrame, bg = themeColor, width = 30,font = 20, height = 21, yscrollcommand = scrollbar.set, justify = tkinter.CENTER)
itemList.pack()

# kenar alani için arayüz boyutlari
s_height= 100
s_width = 200

# Canvas alani
rightSideFrame = tkinter.Frame(main, bg = themeColor)
rightSideFrame.pack(side = tkinter.RIGHT, fill = tkinter.Y)

canvasLabel = tkinter.Label(rightSideFrame, bg = themeColor, fg = systemColor, font = 24, text = "Current Date")
canvasLabel.pack(side = tkinter.TOP, fill = tkinter.X)

# kenar alani (tuslarin alani)
sideFrame = tkinter.Frame(main, bg = themeColor, height = s_height, width = s_width)
sideFrame.pack(side = tkinter.RIGHT , fill = tkinter.Y)

# iki alani bölecek olan renk katmani
#divider = tkinter.Frame(main, bg = "black", height = s_height, width = 2)
#divider.pack(side = tkinter.RIGHT, fill = tkinter.Y)

#item alanina gelecek placeholder texti ve item text ini
itemName = tkinter.StringVar()
itemName.set('Item Shortcut')  

# deger gösterilmesi için veriye ataniyor
valueText = tkinter.StringVar()
valueText.set('Value: ' + GetValue())


progress_var = tkinter.DoubleVar()

# item adi girme kismi
EntryField = tkinter.Entry(sideFrame, bg = themeColor, fg = userColor, font = 24, textvariable = itemName, justify = tkinter.CENTER)
EntryField.pack(side = tkinter.TOP)

buttonFrame = tkinter.Frame(sideFrame, bg = themeColor, height = 80, width = s_width )
buttonFrame.pack(side = tkinter.TOP , fill = tkinter.X)



def AddItemEvent(event):
    AddItem()
    
# item ekleme tusu   
addItemButton = tkinter.Button(sideFrame, bg = themeColor, fg = systemColor, text = "Add Item", font = 24, width = 15, height = 3, command = AddItem)
addItemButton.bind("<Return>", AddItemEvent)
addItemButton.pack(side = tkinter.TOP)

# item düzenleme tusu   
editItemButton = tkinter.Button(sideFrame, bg = themeColor, fg = systemColor, text = "Edit Item", font = 24, width = 15, height = 3, command = EditItem)
editItemButton.pack(side = tkinter.TOP)

# item silme tusu     
removeItemButton = tkinter.Button(sideFrame, bg = themeColor, fg = systemColor, text = "Remove Item", font = 24, width = 15, height = 3, command = RemoveItem)
removeItemButton.pack(side = tkinter.TOP)

# degeri gösterecek olan alan 
valueLabel = tkinter.Label(titleFrame, bg = themeColor, fg = systemColor, font = 18, text = valueText.get())
valueLabel.pack()

# baslat tusu
StartButton = tkinter.Button(sideFrame, bg = themeColor, fg = systemColor, text = "Start", font = 24, width = 15, height = 3, command = StartCalculation)
StartButton.pack(side = tkinter.TOP)

# Canvas grafikler için
canvas = tkinter.Canvas(rightSideFrame, bg = themeColor, height = 500, width = 800)
canvas.pack()

figure = plt.Figure(figsize=(5,4), dpi=100, facecolor = themeColor)

#rect = figure.patch
#rect.set_facecolor(themeColor)

#ax = figure.add_subplot(111)
line = FigureCanvasTkAgg(figure, canvas)
line.get_tk_widget().pack()
#df = df[['Dates', 'Values']].groupby('Dates').sum()
#df.plot(kind='line', legend=True, ax=ax,color='r',marker='o',fontsize=10)
#ax.set_title('Values')

Start()

tkinter.mainloop()

    
