import base64
from subprocess import Popen
import os

# Portfolio sınıfı
class Portfolio:

    name : str

    date : str

    stockDatas : list = []

    valueDatas : list = []

    # Constructor
    def __init__(self, name = None):

        if name is not None:
            self.name = name
        
        self.date = ""
        
    # Stock u kolayca ekleyebilmek için
    def AddStock(self, stock):

        self.stockDatas.append(stock)

        return
    # Stock u kolayca silebilmek için
    def RemoveStock(self, stock):

        self.stockDatas.remove(stock)

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
        data = self.date + "\n"

        # her stock datasında gez ve bunları data ya ekle
        for stock in self.stockDatas:

            data += stock.name + ":" + str(stock.amount) + ","

        # sondaki fazla , den kurtul
        data = data[:-1]
        # stock datalar bitti \n ayracını koy
        data += "\n"
        # value datalar arasında gez ve bunları data ya ekle
        for value in self.valueDatas:

            data += value.date + ":" + str(value.value) + ","
        # sondaki fazla , den kurtul
        data = data[:-1]
        # veriyi dosyaya yaz
        WriteFile(path, data)

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
                self.date = info
                
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
       

# stock sınıfı
class Stock:

    name : str

    stockDates : list = []
    
    # Constructor
    def __init__(self, name):

        self.name = name

    # stock date i eklemek için olan fonksiyon
    def AddStockDate(self, stockDate):

        stockDates.append(stockDate)

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
                data += stockDate.infos[order] + ","
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


    # Stock u ekrana basan fonksiyon
    def Print(self):

        stringVal = self.name + "\n"

        for dateData in self.stockDates:

            stringVal += dateData.date + ":"

            for info in dateData.infos:

                stringVal += info + ","

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

                    self.infos.append(infoData)
                
        
        
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

