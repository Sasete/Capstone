import tkinter

isWorking = False

def GetPortfolioItems():

    itemList.insert(tkinter.END, "TSLA")
    itemList.insert(tkinter.END, "MSFL")
    itemList.insert(tkinter.END, "MCRSFT")


def CalculateValue():

    null


def AddItem():

    null
    
def EditItem():

    null
    
def RemoveItem():

    null


def GetValue():

    return '0'

def Start():

    global isWorking

    if isWorking:
        isWorking = False
        StartButton.config(text = "Start")
    else:
        isWorking = True
        StartButton.config(text = "Stop")



    print(isWorking)


main = tkinter.Tk()
main.title("Portfolio")
main.resizable(False, False)



themeColor = "gray"
systemColor = "black"
userColor = "white"



m_height = 100
m_width = 200



sideSpace = 50
topBottomSpace = 125


mainFrame = tkinter.Frame(main, bg = themeColor, height = m_height, width = m_width)
mainFrame.pack(side = tkinter.LEFT, fill = tkinter.Y)


titleFrame = tkinter.Frame(mainFrame, bg = themeColor, width = m_width, height = 30)
titleFrame.pack(side = tkinter.TOP, fill = tkinter.X)

bottomFrame = tkinter.Frame(mainFrame, bg = themeColor, width = m_width, height = 30)
bottomFrame.pack(side = tkinter.BOTTOM, fill = tkinter.X)

scrollbar = tkinter.Scrollbar(mainFrame)
scrollbar.pack(side = tkinter.LEFT, fill = tkinter.Y)


itemList = tkinter.Listbox(mainFrame, bg = themeColor, width = 30,font = 20, height = 10, yscrollcommand = scrollbar.set, justify = tkinter.CENTER)
itemList.pack()


s_height= 100
s_width = 200

sideFrame = tkinter.Frame(main, bg = themeColor, height = s_height, width = s_width)
sideFrame.pack(side = tkinter.RIGHT , fill = tkinter.Y)

divider = tkinter.Frame(main, bg = "black", height = s_height, width = 2)
divider.pack(side = tkinter.RIGHT, fill = tkinter.Y)

itemName = tkinter.StringVar()
itemName.set('Item Shortcut')

valueText = tkinter.StringVar()
valueText.set('Value: ' + GetValue())

EntryField = tkinter.Entry(sideFrame, bg = themeColor, fg = userColor, font = 24, textvariable = itemName, justify = tkinter.CENTER)
EntryField.pack(side = tkinter.TOP)

addItemButton = tkinter.Button(sideFrame, bg = themeColor, fg = systemColor, text = "Add Item", font = 24, width = 10, height = 2, command = AddItem)
addItemButton.pack(side = tkinter.TOP)

editItemButton = tkinter.Button(sideFrame, bg = themeColor, fg = systemColor, text = "Edit Item", font = 24, width = 10, height = 2, command = EditItem)
editItemButton.pack(side = tkinter.TOP)

removeItemButton = tkinter.Button(sideFrame, bg = themeColor, fg = systemColor, text = "Remove Item", font = 24, width = 10, height = 2, command = RemoveItem)
removeItemButton.pack(side = tkinter.TOP)


valueLabel = tkinter.Label(titleFrame, bg = themeColor, fg = userColor, font = 18, text = valueText.get())
valueLabel.pack()


StartButton = tkinter.Button(sideFrame, bg = themeColor, fg = systemColor, text = "Start", font = 24, width = 10, height = 2, command = Start)
StartButton.pack(side = tkinter.TOP)


GetPortfolioItems()


        
        
    
