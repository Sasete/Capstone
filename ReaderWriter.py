import base64
from subprocess import Popen
import os

# Portfolio sınıfı
class Portfolio:

    name : str

    money : float

    date : str

    stockDatas : list = []

    valueDatas : list = []

    # Constructor
    def __init__(self, name = None):

        if name is not None:
            self.name = name

        money = 0
        self.date = ""

    def Initialize(self):

        self.name = ""
        self.date = ""
        money = 0
        self.stockDatas.clear()
        self.valueDatas.clear()
        
    # Stock u kolayca ekleyebilmek için
    def AddStock(self, stock):

        self.stockDatas.append(stock)

        return
    # Stock u kolayca silebilmek için
    def RemoveStock(self, stock):

        for stockData in self.stockDatas:

            if stockData is None:
                continue

            if stockData.name == stock.name:

                stockData.amount -= stock.amount

                if stockData.amount <= 0:

                    self.stockDatas.remove(stockData)

        return
    # Value bilgisini ekleyebilmek için
    def AddValueData(self, value):

        self.valueDatas.append(value)

        return
    # Value bilgisini kaldırabilmek için
    def RemoveValueData(self, value):

        self.valueDatas.remove(value)

        return
    
    # Bütün sınıfı .portfolio dosyası verisine dönüştürüp kayıt eden fonksiyon
    def Save(self, path, fileName = None):

        # isim alanı girilmediyse dosya adını kendi adı yap
        if fileName is None:
            
            fileName = self.name
        # uzantıyı ekle
        fileName +=  ".portfolio"

        path += fileName
        # tarihten sonra \n ayracını koy
        data = self.date + ':' + str(self.money) + '\n'

        # her stock datasında gez ve bunları data ya ekle
        for stock in self.stockDatas:

            data += stock.name + ":" + str(stock.amount) + ","

        # sondaki fazla , den kurtul
        data = data[:-1]
        # stock datalar bitti \n ayracını koy
        data += "\n"
        # value datalar arasında gez ve bunları data ya ekle
        for value in self.valueDatas:

            data += str(value.date) + ":" + str(value.value) + ","
        # sondaki fazla , den kurtul
        data = data[:-1]
        # veriyi dosyaya yaz
        WriteFile(path, data)


    def GetTextToSave(self):
        
        # tarihten sonra \n ayracını koy
        data = self.date + ':' + str(self.money) + '\n'

        # her stock datasında gez ve bunları data ya ekle
        for stock in self.stockDatas:

            data += stock.name + ":" + str(stock.amount) + ","

        # sondaki fazla , den kurtul
        data = data[:-1]
        # stock datalar bitti \n ayracını koy
        data += "\n"
        # value datalar arasında gez ve bunları data ya ekle
        for value in self.valueDatas:

            data += str(value.date) + ":" + str(value.value) + ","
        # sondaki fazla , den kurtul
        data = data[:-1]

        return data

    # .portfolio verisini okuyup sınıfa çeviren fonksiyon
    def Load(self, path, fileName = None):
        
        # isim alanı girilmediyse dosya adını kendi adı yap
        if fileName is None:
            fileName = self.name
        # uzantıyı ekle
        fileName += ".portfolio"
        # veriyi dosyadan oku
        data = ReadFile(path + fileName)
        # order, sıralama için önemli,
        # order == 0 -> Tarih order == 1 -> stock bilgileri, order == 2 -> value bilgileri
        order = 0
        # veriyi \n ayracından böl ve veriler arasında dolaş
        for info in data.split('\n'):
            # veri 0 sa tarihi oku
            if order == 0:

                
                self.date = info.split(':')[0]
                self.money = float(info.split(':')[1])
                
                order += 1
                continue
            # veri 1 ise, stock bilgilerini okumaya başla
            if order == 1:
                # stocklar , ler ile ayrılıyor. , lere böl ve dolaş
                for stockDat in info.split(','):
                    # eger stock boş ise, bitir
                    if not stockDat:
                        break
                    # stock un bilgisini oku
                    stockData = StockData(stockDat.split(':')[0], int(stockDat.split(':')[1]))
                    # stock u sınıfa ekle
                    self.stockDatas.append(stockData)


                order += 1
                continue

            # veri 2 ise, value bilgilerini okmaya başla
            if order == 2:
                # value data lar , ler ile ayrılıyor. , lere böl ve dolaş
                for valueDat in info.split(','):
                    # value data boş ise bitir
                    if not valueDat:
                        break
                    # value data yı oku
                    valueData = ValueData(valueDat.split(':')[0], float(valueDat.split(':')[1]))

                    self.valueDatas.append(valueData)
                

                order += 1
                continue

    def GetValue(self, functionType = 0):

        value = 0

        if functionType == 0:
    
            order = 0
            for stockData in self.stockDatas:

        
                stock = Stocker.Stock(stockData.name)

                stock.Initialize()

                stock.name = stockData.name

                stock.Load('./Resources/Stocks/')

                stock.Print()

                value += float(stock.stockDates[-1].GetInfo("Close").info) * stockData.amount


                order += 1

            value += self.money


        if functionType == 1:
    
            order = 0
            for stockData in self.stockDatas:

        
                stock = Stocker.Stock(stockData.name)

                stock.Initialize()

                stock.name = stockData.name

                stock.Load('./Resources/Stocks/')

                stock.Print()

                value += float(stock.stockDates[-1].GetInfo("Close").info) * stockData.amount


                order += 1

        if functionType == 2:

            value += self.money


        return value
        


    def SetDate(self, date):

        valueData = ValueData(self.date, self.GetValue(0))

        self.valueDatas.append(valueData)

        self.date = date
           

# stock sınıfı
class Stock:

    name : str

    stockDates : list = []
    
    # Constructor
    def __init__(self, name):

        self.name = name

    def Initialize(self):

        self.name = ""
        self.stockDates.clear()

    # stock date i eklemek için olan fonksiyon
    def AddStockDate(self, stockDate):

        self.stockDates.append(stockDate)

        return
    # stock date i silmek için olan fonksiyon
    def RemoveStockDate(self, stockDate):

        stockDates.remove(stockDate)

        return
    # sınıfı .stock olarak dosyaya kayıt eden fonksiyon
    def Save(self, path, fileName = None):
        # eger isim verilmediyse, sınıftaki adı kullan
        if fileName is None:
            
            fileName = self.name

        fileName +=  ".stock"

        path += fileName
        # isim bilgisini sınıfa ekle
        data = self.name + "\n"
        # her stock date için bu kodları oku, stock date ler içinde dolaş
        for stockDate in self.stockDates:
            # date verisini data ya koy : ayracıyla ayır ve infolara geç
            data += stockDate.date + ":"
            # order kaçıncı veriyi yazdığımı tutmak için gerekli
            order = 0
            # infolar arasında gez ve order da olanı yaz
            for info in stockDate.infos:
                # info boşsa bitir
                if info is None:
                    break
                # info yu data ya yaz
                data += stockDate.infos[order].Write() + ","
                order += 1
            # sondaki gereksiz , den kurtul, yerine ; koy
            data = data[:-1] + ";"
        # sondaki gereksiz ; den kurtul
        data = data[:-1]
        # sınıfı dosyaya yaz
        WriteFile(path, data)


    # .stock dosyayı okuyup sınıfa çeviren fonksiyon
    def Load(self, path, fileName = None):
        # isim verilmemisse sınıf ismini kullan
        if fileName is None:
            
            fileName = self.name

        fileName +=  ".stock"

        path += fileName
        # veriyi oku
        data = ReadFile(path)

        # line ilk satır da olup olmadığımızı algılıyor
        line = 0
        for infoData in data.split('\n'):
            # eger satır bossa, atla
            if infoData is None:

                continue
            
            # ilk satırdaysak, ismi ilk satırdan alıyoruz
            if line == 0:
                self.name = infoData
                line += 1
                continue
            
            # degilsek,
            if line == 1:
                # veriyi ; lerden ayırıyoruz
                for dateData in infoData.split(';'):
                    # eger veri bossa atla
                    if dateData is None:

                        continue
                    # her bir data için sınıfı initialize ediyoruz
                    stockDateData = StockDateData()
                    # ve o sınıfa veriyi verip kendini oku diyoruz
                    stockDateData.Read(dateData)
                    # okunan veriyi kendi stock verilerimize ekliyoruz
                    self.stockDates.append(stockDateData)
                    
                continue

    def GetTextToSave():

        stringVal = self.name + "\n"


        for dateData in self.stockDates:

            if dateData is None:
                continue

            stringVal += dateData.date + ":"

            for info in dateData.infos:

                if info is None:
                    continue

                stringVal += info.Write()

            stringVal = stringVal[:-1]


        stringVal = stringVal[:-1]

        return stringVal
        

    # Stock u ekrana basan fonksiyon
    def Print(self):

        stringVal = self.name + "\n"

        for dateData in self.stockDates:

            if dateData is None:
                continue

            stringVal += dateData.date + ":"

            for info in dateData.infos:

                if info is None:
                    continue

                stringVal += info.Write() + ","

            stringVal = stringVal[:-1]

            stringVal += ";"


        stringVal = stringVal[:-1]

        print("line 254:" + stringVal)

# stock data, portfolio da saklanacak olan stockData
class StockData:

    name : str

    amount : int

    def __init__(self, name, amount):

        self.name = name

        self.amount = amount

        

# valueData, portfolio da saklanacak olan valueData
class ValueData:

    date : str

    value : float

    def __init__(self, date, value):

        self.date = date

        self.value = value

# stockDateData, stock ta saklanacak olan stockDate verileri
class StockDateData:

    date : str

    infos : list = []

    def __init__(self):

        self.date = ""

        self.infos = []
        
    # verilen veriden StockDateData yı okumak için fonksiyon
    # örnek veri: 2011:105,100,90
    def Read(self, data):

        order = 0
        for info in data.split(':'):

            if info is None:
                
                continue

            if order == 0:

                self.date = info
                
                order += 1
                continue

            if order == 1:

                for infoData in info.split(','):

                    info = DateInfo()

                    info.Read(infoData)

                    self.infos.append(info)

    def Write(self):

        stringVal = ''

        for data in self.infos:

            stringVal += data.Write() + ','


        stringVal = stringVal[:-1] + ';'
        
        return stringVal

    def GetInfo(self, name):

        for info in self.infos:

            if info.name == name:

                return info

# StockDateData daki info listteki datalar
class DateInfo():

    name : str

    info : str

    def __init__(self):

        self.name = ""
        self.info = ""


    def Initialize(self):

        self.name = ""
        self.info = ""

    def Read(self, stringInfo):

        # string info söyle bir veri: "VerininAdi"Veridegeri
        self.name = stringInfo.split('"')[1]

        self.info = stringInfo.split('"')[2]
        
    def Write(self):

        return "\"" + self.name + "\"" + self.info

    def Load(self, name, info):

        self.name = name
        self.info = info
    
        
# Dosya okumak için
def ReadFile(path):

    file = open(path, "r")

    data = file.read()

    # TODO Data should be encoded here

    return data

# Dosyaya yazmak için
def WriteFile(path, data):

    # TODO Data should be decoded here

    f = open(path, "w")

    f.write(data)

    f.close()

def RemoveFile(path):

    os.remove(path)

def Open(path, hideShell = False):
    Popen('py ' + path, shell = hideShell)

def HumanFormat(num, round_to=2):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num = round(num / 1000.0, round_to)
    return '{:.{}f}{}'.format(round(num, round_to), round_to, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
