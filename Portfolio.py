import tkinter
import ReaderWriter as Stocker
from tkinter import filedialog
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

# isWorking uygulamanin acik olma durumu
isWorking = False


portfolio = Stocker.Portfolio('')

path = ''
fileName = ''

functionThread = ''
killThread = False

stockUpdater = ''
stockUpdate = True

todayDate = datetime.datetime(2020,1,1)
dateChanger = ''
dateChanged = False


def Start():

    #stockUpdate = True
    #stockUpdater = threading.Thread(target = UpdateAllStocks)

    #stockUpdater.start()

    dateChanged = False
    dateChanger = threading.Thread(target = TimeCounter)

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

        for stock in stocks.split('\n'):
            
            pullStocks.append(stock)

        PullStocks(pullStocks)


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
    fileName = 'MyPortfolio'

    
    portfolio.Initialize()

    portfolio.date = str(date.year) + '-' + str(date.month).zfill(2) + '-' + str(date.day).zfill(2)
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

    stockData = yf.download(tickers = stockNames, start = startDate, end = endDate, progress = False)
    #stockData.head()

    #print(stockData)

    stocks = []

    for stock in stockList:

        stockFrame = stockData.iloc[:, stockData.columns.get_level_values(1) == stock]

        #print(stockFrame)

        currentStock = Stocker.Stock(stock)
        
        currentStock.Initialize()
        currentStock.name = stock


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
        
            
            short_avg = GetAverage(shortList, "Close")
            long_avg = GetAverage(longList, "Close")
            twenty_avg = GetAverage(twentyList, "Close")
            sigma = GetSigma(twentyList, "Close")
            lowerBand, upperBand = (twenty_avg - (2 * sigma) , twenty_avg + (2 * sigma))

            rs = GetRS(rsList)
            rsi = 100 - (100 / ( 1 + rs ))

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


            
        currentStock.Save('./Resources/Stocks/')

        
            

def PullStock(stockName, daysBefore = 0):

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

    stockData = yf.download(stockName, start = startDate, end = endDate, progress = False)

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

            rsi = 100 - (100 / ( 1 + rs ))

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
        
                
        
        stock.Save('./Resources/Stocks/')
            
        return stock

    else:
            
        print('Couldn\'t find stock...')
        return None
            
    
    #except:
        #print('Couldn\'t find stock...')
        #return None
    
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

    average = 0
    count = 0

    for i in range(len(values)):

        column = values.iloc[i,]
        
        #date = str(column).split('Name:')[1].split(' ')[1]

        order = 0
        for dat in values.iloc[i]:

            data = str(column).split('\n')[order].split(' ')[0]

            if data == dataType:

                average += dat

                count += 1

            
            order += 1
                


    return average / count

def GetSigma(values, dataType):

    average = 0
    count = 0

    for i in range(len(values)):

        column = values.iloc[i,]
        
        #date = str(column).split('Name:')[1].split(' ')[1]

        order = 0
        for dat in values.iloc[i]:

            data = str(column).split('\n')[order].split(' ')[0]

            if data == dataType:

                average += dat

                count += 1

            
            order += 1
                

    average = average / count
    
    val = 0
    for i in range(len(values)):

        column = values.iloc[i,]

        order = 0

        for dat in values.iloc[i]:
            data = str(column).split('\n')[order].split(' ')[0]


            if data == dataType:

                val += (dat - average) ** 2



            order += 1

    sigma = math.sqrt(val / count)

    return sigma
    

    

def GetRS(values):

    closeList = []
    rsList = []

    for i in range(len(values)):

        column = values.iloc[i,]

        order = 0
        for dat in values.iloc[i]:

            data = str(column).split('\n')[order].split(' ')[0]

            if data == "Close":
                closeList.append(dat)
    
            
            order += 1


    upSum = 0
    lowSum = 0
        
    for i in range(len(closeList)):

        #print(closeList[i])

        if i == 0:

            continue

        rs = closeList[i] - closeList[i - 1]

        # Mutlak deger kodunu hatırlayamadım
        if rs < 0:
            lowSum += rs*-1
        else:
            upSum += rs
            

    try:
        rs = upSum / lowSum
    except:
        rs = upSum / (lowSum + 1)


    return rs

def BollingerBand(stock):

    global portfolio

    twentyAvg = float(stock.GetDate(portfolio.date).GetInfo('TwentyAverage').info)
    
    sigma = float(stock.GetDate(portfolio.date).GetInfo('Sigma').info)

    upperBand = twentyAvg + (2 * sigma)
    lowerBand = twentyAvg - (2 * sigma)


    return (lowerBand, upperBand)

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

def LowRiskSuggest():

    global portfolio
    itemList.delete(0, tkinter.END)

    portfolio.stockDatas.clear()
    
    AddStockItem('ARCLK.is')
    AddStockItem('YATAS.is')
    AddStockItem('DOHOL.is')

    return None

def MediumRiskSuggest():

    global portfolio
    itemList.delete(0, tkinter.END)

    portfolio.stockDatas.clear()
    
    AddStockItem('TUKAS.is')
    AddStockItem('AEFES.is')
    AddStockItem('KARSN.is')
    

    return None

def HighRiskSuggest():

    global portfolio
    itemList.delete(0, tkinter.END)

    portfolio.stockDatas.clear()
    
    stocks = Stocker.ReadFile('./Resources/StockList.txt')


    poolStocks = []

    for stock in stocks.split('\n'):
            
        poolStocks.append(stock)

    stockNo1 = int(random.randint(0, len(poolStocks)))
    stockNo2 = int(random.randint(0, len(poolStocks)))
    stockNo3 = int(random.randint(0, len(poolStocks)))

    AddStockItem(poolStocks[stockNo1])
    AddStockItem(poolStocks[stockNo2])
    AddStockItem(poolStocks[stockNo3])

    print("HighRiskSuggest")

    return None

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

        if bollingerValue < 0.25:
            
            print(stock.name + ' bought x3!')

            portfolio.Buy(stock, 3)

            return

            
        print(stock.name + ' bought!')

        portfolio.Buy(stock)

        return
    

    if macd > 0 and rsi > 70:

        if bollingerValue > 0.75:

            print(stock.name + ' sold x3!')

            portfolio.Sell(stock, 3)

            return


        print(stock.name + ' sold!')

        portfolio.Sell(stock)
        

        return
        
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

    
