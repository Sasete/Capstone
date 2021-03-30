import tkinter
import ReaderWriter as Stocker
from tkinter import filedialog

stock = Stocker.Stock('')

# degeri arayüz için alan fonksiyon
def GetValue():

    return '0'

# dosya çalışmaları için fonksiyonlar oluşturuluyor
def OpenFile():
    
    filetypes = [ ('Stock Files', '*.stock') ]
    path = tkinter.filedialog.askopenfilename(title = "openFile", initialdir = './', filetypes = filetypes)
    fileName = path.split('/')[-1]    
    path = path[:len(path) - len(fileName)]


    extention = fileName.split('.')[-1]
    fileName = fileName[:len(fileName) - (len(extention)+1)]
    
    stock = Stocker.Stock('')
    stock.Load(path, fileName)


    print(stock.stockDates[-1].date + stock.stockDates[-1].infos[-1])

    stock.stockDates[-1].infos[-1] = 'en guncel info'
    stock.Save(path, fileName)

def SaveFile():

    path = asksaveasfile(mode='w')
    saveText = "merhaba dünya"
    path.write(saveText)
    path.close()

def Start():

    print("Start fonksiyonu aktif")

    # temp dosyasından stock un adını okuduk.
    stringValue = Stocker.ReadFile('./Temp.txt')

    # global deki stock u kullanıcaz
    global stock

    # stock u yeni bir stock olarak oluştur
    stock = Stocker.Stock(stringValue)

    # stock u load et
    stock.Load('./Resources/Stocks/')

    # ./Temp.txt yi sil
    Stocker.RemoveFile('./Temp.txt')

    # Stock a göre arayüzü düzenle.
    StockToUI()

def UIToStock():



    null

def StockToUI():

    global stock


    nameText.set(stock.name)
    valueText.set(stock.stockDates[len(stock.stockDates) - 1].infos[0])
    dateText.set(stock.stockDates[len(stock.stockDates) - 1].date)



    nameLabel.config(text = nameText.get())
    valueLabel.config(text = valueText.get())
    dateLabel.config(text = dateText.get())
    















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
canvasLabel = tkinter.Label(rightFrame, bg = themeColor, fg =userColor, font = 24, text = "Value Graph")
canvasLabel.pack(side = tkinter.TOP, fill = tkinter.X)

# name deger gösterilmesi için veriye ataniyor
nameText = tkinter.StringVar()
nameText.set('Name: ' + GetValue())

# value deger gösterilmesi için veriye ataniyor
valueText = tkinter.StringVar()
valueText.set('Value: ' + GetValue())

# nineDayAverage deger gösterilmesi için veriye ataniyor
nineDayAverageText = tkinter.StringVar()
nineDayAverageText.set('Nine Day Average: ' + GetValue())

# fortyDayAverage deger gösterilmesi için veriye ataniyor
fortyDayAverageText = tkinter.StringVar()
fortyDayAverageText.set('Forty Day Average: ' + GetValue())

# date deger gösterilmesi için veriye ataniyor
dateText = tkinter.StringVar()
dateText.set('Date: ' + GetValue())

# name degeri gösterecek olan alan 
nameLabel = tkinter.Label(leftFrame, bg = themeColor, fg = userColor, font = 18, text = nameText.get())
nameLabel.pack()

# value degeri gösterecek olan alan 
valueLabel = tkinter.Label(leftFrame, bg = themeColor, fg = userColor, font = 18, text = valueText.get())
valueLabel.pack()

# nineDayAverage degeri gösterecek olan alan 
nineDayAverageLabel = tkinter.Label(leftFrame, bg = themeColor, fg = userColor, font = 18, text = nineDayAverageText.get())
nineDayAverageLabel.pack()

# fortyDayAverage degeri gösterecek olan alan 
fortyDayAverageLabel = tkinter.Label(leftFrame, bg = themeColor, fg = userColor, font = 18, text = fortyDayAverageText.get())
fortyDayAverageLabel.pack()

# date degeri gösterecek olan alan 
dateLabel = tkinter.Label(leftFrame, bg = themeColor, fg = userColor, font = 18, text = dateText.get())
dateLabel.pack()

# Canvas grafikler için
canvas = tkinter.Canvas(rightFrame, bg = themeColor, height = 500, width = 800)
canvas.pack()

#filetypes = ( ('Portfolio Files', '*.portfolio'), ('Stock Files', '*.stock') )
#fileName = tkinter.filedialog.askopenfilename(title = "openFile", initialdir = './', filetypes = filetypes)

#print(fileName)

Start()




#uygulamayı baslatıyor
#from subprocess import Popendef Open(path):
#Popen('py ' + path, shell = True)
#def Exit():
#Open('./Entrance.pyw')
#sys.exit(0)


tkinter.mainloop()











