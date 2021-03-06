import tkinter
import ReaderWriter as Stocker
from tkinter import filedialog
import datetime
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time


stock = Stocker.Stock('')

path = ''
fileName = ''

graphState = 0

updaterThread = ''

# degeri arayüz için alan fonksiyon
def GetValue():

    return '0'
    

# dosya çalışmaları için fonksiyonlar oluşturuluyor
def OpenFile():
    
    global path
    global fileName
    
    filetypes = [ ('Stock Files', '*.stock') ]
    path = tkinter.filedialog.askopenfilename(title = "openFile", initialdir = './', filetypes = filetypes)
    fileName = path.split('/')[-1]    
    path = path[:len(path) - len(fileName)]


    extention = fileName.split('.')[-1]
    fileName = fileName[:len(fileName) - (len(extention)+1)]

    global stock

    stock.Initialize()

    stock.name = fileName
    
    stock.Load(path)

    StockToUI()
    
def SaveFile():

    global path
    global fileName
    global stock

    stock.Save(path, fileName)

    print('Saved File!')

def SaveAsFile():
    
    filetypes = [ ('Portfolio Files', '*.portfolio') ]
    
    # TODO SHOULD SAVE FILE
    path = tkinter.filedialog.asksaveasfile(mode='w', title = "Save File", initialdir = './', defaultextension=".portfolio", filetypes = filetypes)

    if path is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    
    global stock


    data = stock.GetTextToSave()

    path.write(data)
    path.close()

    print('Saved File!')
    

def Start():

    print("Start fonksiyonu aktif")

    # temp dosyasından stock un adını okuduk.
    stringValue = Stocker.ReadFile('./Temp.txt')

    # global deki stock u kullanıcaz
    global stock
    global fileName
    global path
    global updaterThread
    

    # stock u yeni bir stock olarak oluştur
    stock = Stocker.Stock(stringValue)

    path = './Resources/Stocks/'

    # stock u load et
    stock.Load(path)

    # ./Temp.txt yi sil
    Stocker.RemoveFile('./Temp.txt')

    # Stock a göre arayüzü düzenle.
    StockToUI()

    updaterThread = threading.Thread(target = Updater)
    updaterThread.start()
    

def Updater():


    try:
        
        global path
        global fileName
        global stock
    
        while True:

            oldInfo = stock.GetTextToSave()
        
            stock.Load(path)

            if oldInfo != stock.GetTextToSave():        

                StockToUI()

            time.sleep(5)

    except:
        print('Thread end.')

def UIToStock():



    null

def StockToUI():

    global stock

    main.title(stock.name);

    stringVar = 'Name:\t ' + stock.name + '\n' + '\n'
    stringVar += 'Date:\t ' + stock.stockDates[len(stock.stockDates) - 1].date + '\n' + '\n'
    

    for data in stock.stockDates[len(stock.stockDates) - 1].infos:

        # istisna deger olmamalı bunlar sınıfın içinde belirtilmeli.
        if data.name == "Volume":
            stringVar += data.name + ':\t ' + Stocker.HumanFormat(float(data.info)) + '\n' + '\n' 
            continue

        if data.name == "RSI":
            stringVar += data.name + ':\t ' + "{:.2f}".format(float(data.info)) + '%' + '\n' + '\n'
            continue

        stringVar += data.name + ':\t ' + "{:.2f}".format(float(data.info)) + '₺' + '\n' + '\n' 
        

    stringVar = stringVar[:-1]


    infoText.set(stringVar)
    infoLabel.config(text = infoText.get())

    PrepareDropdownGraphMenu()
    PrepareGraph()



def PrepareGraph():

    
    global stock
    global graphState

    dates = []
    values = []

    graphName = ''


    for value in stock.stockDates:

        date = datetime.datetime.strptime(value.date,'%Y-%m-%d')

        graphName = value.infos[graphState].name

        dates.append(date)
        #print('Value: ' + value.infos[graphState].info)
        values.append(float(value.infos[graphState].info))

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
    ax.set_title(graphName)

    line.draw()

def PrepareDropdownGraphMenu():


    global stock

    editMenu.delete(0, tkinter.END)

    exampleStock = stock.stockDates[0]

    lambdaList = []
    listint = []

    for i in range(len(exampleStock.infos)):

        value = exampleStock.infos[i]


        lambdaList.append(lambda i=i: SetGraphState(i))
        listint.append(i)
        
        editMenu.add_command(label = value.name, command = lambdaList[i])


def SetGraphState(state):

    global graphState

    graphState = int(state)

    PrepareGraph()

# Tkinter arayüz kurulumu
main = tkinter.Tk()
main.title("Stock")
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
fileMenu.add_command(label = "Open", command = OpenFile)
#fileMenu.add_separator()   #cizgi olusturuyor
#fileMenu.add_command(label = "Save As", command = SaveAsFile)
#fileMenu.add_command(label = "Save", command = SaveFile)


editMenu = tkinter.Menu(Menu, tearoff = 0)
Menu.add_cascade(label = "Graph", menu = editMenu)
editMenu.add_command(label = "Open", command = lambda: SetGraphState(0))
editMenu.add_command(label = "High", command = lambda: SetGraphState(1))
editMenu.add_command(label = "Low", command = lambda: SetGraphState(2))
editMenu.add_command(label = "Close", command = lambda: SetGraphState(3))
editMenu.add_command(label = "Adj", command = lambda: SetGraphState(4))
editMenu.add_command(label = "Volume", command = lambda: SetGraphState(5))
#editMenu.add_separator()   #cizgi olusturuyor
#editMenu.add_command(label = "")


# arayüzün üst text kismi frame
#textFrame = tkinter.Frame(main, bg = themeColor, width = m_width, height = 120)
#textFrame.pack(side = tkinter.TOP, fill = tkinter.X)

# arayüzün yan text kismi frame
#texttFrame = tkinter.Frame(main, bg = themeColor, width = 60, height = m_height)
#texttFrame.pack(side = tkinter.LEFT, fill = tkinter.Y)

# arayüzün tamami
mainFrame = tkinter.Frame(main, bg = themeColor, height = m_height, width = m_width)
mainFrame.pack(side = tkinter.LEFT, fill = tkinter.Y)

# arayüzün baslik kismi
leftFrame = tkinter.Frame(mainFrame, bg = themeColor, width = m_width, height = 30)
leftFrame.pack(side = tkinter.LEFT, fill = tkinter.X)

# arayüzün alt kismi
rightFrame = tkinter.Frame(mainFrame, bg = themeColor, width = m_width, height = 30)
rightFrame.pack(side = tkinter.RIGHT, fill = tkinter.X)

# canvas için LEFTLeftFrame oluşturma
leftLeftFrame = tkinter.Frame(leftFrame, bg = themeColor, width = 30, height = 30)
leftLeftFrame.pack(side = tkinter.LEFT, fill = tkinter.Y)


# canvas için BottomFrame oluşturma
leftRightFrame = tkinter.Frame(leftFrame, bg = themeColor, width = 30, height = 30)
leftRightFrame.pack(side = tkinter.RIGHT, fill = tkinter.Y)

# kenar alani için arayüz boyutlari
s_height= 100
s_width = 200


# canvas oluşturulan alan 
canvasLabel = tkinter.Label(rightFrame, bg = themeColor, fg = systemColor, font = 24, text = "Value Graph")
canvasLabel.pack(side = tkinter.TOP, fill = tkinter.X)

# name deger gösterilmesi için veriye ataniyor
infoText = tkinter.StringVar()
infoText.set('Name: ' + GetValue())

# name degeri gösterecek olan alan 
infoLabel = tkinter.Label(leftFrame, bg = themeColor, fg = systemColor, font = 18, text = infoText.get(), justify = tkinter.LEFT)
infoLabel.pack()

# Canvas grafikler için
canvas = tkinter.Canvas(rightFrame, bg = themeColor, height = 500, width = 800)
canvas.pack()

#filetypes = ( ('Portfolio Files', '*.portfolio'), ('Stock Files', '*.stock') )
#fileName = tkinter.filedialog.askopenfilename(title = "openFile", initialdir = './', filetypes = filetypes)

#print(fileName)

figure = plt.Figure(figsize=(5,4), dpi=100,facecolor = themeColor)
#ax = figure.add_subplot(111)
line = FigureCanvasTkAgg(figure, canvas)
line.get_tk_widget().pack()
#df = df[['Dates', 'Values']].groupby('Dates').sum()
#df.plot(kind='line', legend=True, ax=ax,color='r',marker='o',fontsize=10)
#ax.set_title('Values')


Start()




#uygulamayı baslatıyor
#from subprocess import Popendef Open(path):
#Popen('py ' + path, shell = True)
#def Exit():
#Open('./Entrance.pyw')
#sys.exit(0)


tkinter.mainloop()











