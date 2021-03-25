import tkinter
import ReaderWriter as Stocker
from tkinter import filedialog

# isWorking uygulamanin acik olma durumu
isWorking = False


portfolio = Stocker.Portfolio('')

def Start():

    OpenFile()
    
# dosya çalışmaları için fonksiyonlar oluşturuluyor
def OpenFile():
    
    filetypes = [ ('Portfolio Files', '*.portfolio') ]
    path = tkinter.filedialog.askopenfilename(title = "openFile", initialdir = './', filetypes = filetypes)
    fileName = path.split('/')[-1]    
    path = path[:len(path) - len(fileName)]


    extention = fileName.split('.')[-1]
    fileName = fileName[:len(fileName) - (len(extention)+1)]

    global portfolio

    # TODO SHOULD INITIALIZE PORTFOLIO

    portfolio.name = fileName

    portfolio.Load(path)
    
    PortfolioToUI()
    

def SaveFile():

    print("Saved File!")

    return

    # TODO SHOULD SAVE FILE
    path = tkinter.filedialog.asksaveasfile(mode='w')
    fileName = path.split('/')[-1]    
    path = path[:len(path) - len(fileName)]


    extention = fileName.split('.')[-1]
    fileName = fileName[:len(fileName) - (len(extention)+1)]

    global portfolio

    portfolio.Save(path, fileName)


def UIToPortfolio():

    null

def PortfolioToUI():

    global portfolio

    print(portfolio.name)

    main.title(portfolio.name)

    canvasLabel.config(text = portfolio.date)

    GetPortfolioItems()

    value = CalculateValue()

    valueLabel.config(text = str(value))

# portfolio daki itemlari listeye listeleyecek fonksiyon
def GetPortfolioItems():

    global portfolio

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

        stock.Load('./Resources/Stocks/')

        stock.Print()


        value = float(stock.stockDates[-1].infos[0]) * stockData.amount

        order += 1


    return value


# portfolio ya belirtilen item i ekleyecek fonksiyon
def AddItem():

    null

# listedeki seçili item in arayüzünü açacak fonksiyon
def EditItem():

    stringValue = itemList.get(tkinter.ACTIVE).split('\t')[0]

    Stocker.WriteFile('./Temp.txt', stringValue)

    Stocker.Open('./Stock.py', True)
    

# listedeki seçili item i portfolio dan çikaracak olan fonksiyon 
def RemoveItem():

    null

# degeri arayüz için alan fonksiyon
def GetValue():

    return '0'

# uygulamanýn alim satimini baslatan fonksiyon
def StartCalculation():

    global isWorking

    # global deki isWorking degerini degistir arayüzü ona göre güncelle
    if isWorking:
        isWorking = False
        StartButton.config(text = "Start")
    else:
        isWorking = True
        StartButton.config(text = "Stop")






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
fileMenu.add_command(label = "New")
fileMenu.add_command(label = "Open", command = OpenFile)
fileMenu.add_separator()   #cizgi olusturuyor
fileMenu.add_command(label = "Save", command = SaveFile)


editMenu = tkinter.Menu(Menu, tearoff = 0)
Menu.add_cascade(label = "Edit", menu = editMenu)
#editMenu.add_command(label = "")
#editMenu.add_command(label = "")
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

canvasLabel = tkinter.Label(rightSideFrame, bg = themeColor, fg = userColor, font = 24, text = "Current Date")
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


# item ekleme tusu   
addItemButton = tkinter.Button(sideFrame, bg = themeColor, fg = systemColor, text = "Add Item", font = 24, width = 15, height = 3, command = AddItem)
addItemButton.pack(side = tkinter.TOP)

# item düzenleme tusu   
editItemButton = tkinter.Button(sideFrame, bg = themeColor, fg = systemColor, text = "Edit Item", font = 24, width = 15, height = 3, command = EditItem)
editItemButton.pack(side = tkinter.TOP)

# item silme tusu     
removeItemButton = tkinter.Button(sideFrame, bg = themeColor, fg = systemColor, text = "Remove Item", font = 24, width = 15, height = 3, command = RemoveItem)
removeItemButton.pack(side = tkinter.TOP)

# degeri gösterecek olan alan 
valueLabel = tkinter.Label(titleFrame, bg = themeColor, fg = userColor, font = 18, text = valueText.get())
valueLabel.pack()

# baslat tusu
StartButton = tkinter.Button(sideFrame, bg = themeColor, fg = systemColor, text = "Start", font = 24, width = 15, height = 3, command = StartCalculation)
StartButton.pack(side = tkinter.TOP)

# Canvas grafikler için
canvas = tkinter.Canvas(rightSideFrame, bg = themeColor, height = 500, width = 800)
canvas.pack()


Start()

tkinter.mainloop()

    
