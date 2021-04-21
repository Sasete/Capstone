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

    stockUpdate = True
    stockUpdater = threading.Thread(target = UpdateAllStocks)

    stockUpdater.start()

    dateChanged = False
    dateChanger = threading.Thread(target = TimeCounter)

    dateChanger.start()

    #UpdateAllStocks()
    
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

        for stock in stocks.split('\n'):

            print(stock)
        
            PullStock(stock)

            return None


        waitTime = 600
        debug = 'Waiting for ' + str(waitTime) + ' seconds.'
        print(debug)
        time.sleep(waitTime)

    return None

def TimeCounter():


    global dateChanged
    
    while True:

        time.sleep(10)

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

def DoesStockExist():

    retVal = False
    
    global portfolio

    stockName = itemName.get()

    for item in itemList.get(0,tkinter.END):
        
        item_name = item.split('\t')[0]

        if item_name == stockName:

            retVal = True
            



    return retVal


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
    
    stockData = yf.download(stockName, start = startDate, end = endDate, progress = False)

    #print(startDate + ':' + endDate + ':' + str(np.busday_count(dateB.date(), dateA.date())))

    stockData.head()

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
            rsList = stockData.iloc[i - 14: i]

            short_avg = GetAverage(shortList, "Close")
            long_avg = GetAverage(longList, "Close")
            rsHigh_avg = GetAverage(rsList, "High")
            rsLow_avg = GetAverage(rsList, "Low")

            rs = rsHigh_avg / rsLow_avg

            rsi = 100 - (100 / ( 1 + rs ))

            stringVal += "\"LongAverage\"" + str(long_avg) + ","
            stringVal += "\"ShortAverage\"" + str(short_avg) + ","
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

        CheckStocks()

        PortfolioToUI()
    
    return

def CheckStocks():
    
    global portfolio
    global todayDate
    
    for stockData in portfolio.stockDatas:
        
        stock = PullStock(stockData.name, -1)
        #stock.Initialize()
        #stock.name = stockData.name
        #stock.Load('./Resources/Stocks/')


        #stock.Print()

        macd = float(stock.GetDate(portfolio.date).GetInfo('ShortAverage').info) - float(stock.GetDate(portfolio.date).GetInfo('LongAverage').info)

        if macd > 0 and float(stock.GetDate(portfolio.date).GetInfo('RSI').info) < 30:

            print(stock.name + ' bought!')

            portfolio.Buy(stock)

        if macd < 0 and float(stock.GetDate(portfolio.date).GetInfo('RSI').info) > 70:

            print(stock.name + ' sold!')

            portfolio.Sell(stock)

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
editMenu.add_command(label = "Low Risk Suggestion")
editMenu.add_command(label = "Medium Risk Suggestion")
editMenu.add_command(label = "High Risk Suggestion")
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

    
