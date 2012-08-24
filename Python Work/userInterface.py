from tkinter import * #need Tkinter for 2.7 and before
import constants
#import tkMessageBox
from tkinter import messagebox
import logging
import arduinocomm
import dbinterface
import threading
import drinks



class StatusBar(Frame):
    def __init__(self, master):

        Frame.__init__(self, master)
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

class UI:
    def __init__(self):



        self.db = dbinterface.DB()
        self.drinkList = []
        self.arduino = arduinocomm.Connection()
        self.currentDrink = None

        logging.basicConfig(file="runLog.txt", level=logging.INFO)
        self.log = logging.getLogger("GUI ")
        self.currentListSelection = 0
        self.log.info("Entering -> GUI -> Constructor()")


        #TOPLEVEL FRAMEWORK
        self.root = Tk()
        self.root.title("Drinkatron v%s"%constants.VERSION)
        self.root.geometry("800x600")
        self.frame = Frame(self.root, width=800, height=550)

        self.status = StatusBar(self.root)
        self.status.set("Initializing UI...")

        #LISTBOX WORK
        self.listboxDrinkList = Listbox(self.root, font = ("Helvetica", 24 ))
        self.listboxDrinkList.grid(row=0,column = 0)
        self.listboxDrinkList.bind('<<ListboxSelect>>', self.refreshDetailView)#This is some wonky code that binds self.refreshDetailView as a callback when the ListBoxSelect TKAction is called.
        self.populateList()

        #star image loading
        self.stars = []
        self.initStars()

        #toolbar work
        self.toolbar = Frame(self.frame)
        self.buttonAddDrink = Button(self.toolbar,text="Add Drink", width = 9, command = self.createNewDrink)
        self.buttonAddDrink.grid(column = 0, row = 2)
        self.toolbar.grid(column = 0, row = 1, columnspan=10)

        #detail view work
        self.detailViewFrame = Frame(self.root)
        self.drinkImage = PhotoImage(file = "C:\\Users\\Tadgh\Documents\GitHub\Drinkatron\Resources\Images\\vodka.gif")
        self.drinkImageLabel = Label(self.detailViewFrame, image=self.drinkImage, anchor=W)
        self.starImageLabel = Label(self.detailViewFrame, image=self.stars[0], anchor=W)
        self.nameLabel = Label(self.detailViewFrame, text="Placeholder", font = ("Helvetica", 24), anchor=W)
        self.descLabel = Label(self.detailViewFrame, text="Placeholder", wraplength=150, anchor=W)


        #gridding
        self.drinkImageLabel.grid(row = 0, column = 0, sticky = W)
        self.nameLabel.grid(row = 0, column = 1, sticky = W)
        self.starImageLabel.grid(row=2, column = 0, columnspan=2, sticky = W)
        self.descLabel.grid(row=1, column =0, sticky = W)
        self.detailViewFrame.grid(row = 0, column = 1, sticky=N+W)





        #Sorting button work
        self.frameSortButtons = Frame(self.root)
        self.buttonNameSort = Button(self.frameSortButtons,text = "A-Z",width = 9,height = 4, command = self.sortByName)
        self.buttonPopularitySort = Button(self.frameSortButtons,text = "Popularity",width = 9,height = 4, command = self.sortByPopularity)
        self.buttonDispenseCountSort = Button(self.frameSortButtons,text = "Dispenses",width = 9,height = 4, command = self.sortByDispenseCount)
        #list of buttons in order to change relief and colour.
        self.buttonList = [self.buttonNameSort,self.buttonDispenseCountSort,self.buttonPopularitySort]

        self.buttonNameSort.grid(column=0, row=0)
        self.buttonPopularitySort.grid(column=1, row=0)
        self.buttonDispenseCountSort.grid(column=2, row=0)

        #dispenseButton
        self.dispenseButton = Button(self.root, text='dispense', command=self.pourIt)
        self.dispenseButton.grid(column=0, row=6)

        #MENUWORK
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.fileMenu = Menu(self.menu)
        self.aboutMenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu = self.fileMenu)
        self.menu.add_cascade(label="About", menu = self.aboutMenu)
        self.aboutMenu.add_command(label="About", command=self.aboutMessageBox)
        self.fileMenu.add_command(label="Quit", command=self.menuQuit)
        self.log.info("Entering -> GUI -> mainLoop()")


        #pack the frame first as both frame and status bar are children to root, this sets them up well.
        self.frame.grid()
        self.frameSortButtons.grid(column=0,row=5)

        self.status.grid(column=0,row=5)


        self.root.mainloop()
        self.log.info("Leaving  -> GUI -> Constructor()")

    def aboutMessageBox(self):
        msgbox = messagebox.showinfo("About", "Drinkatron is a personal bartender\n version: %s\nCopyright 2012"%constants.VERSION) 
        #fix for 3.2
    def menuQuit(self):
        self.log.info("Leaving  -> GUI -> mainLoop, quit was called")
        self.root.destroy()

    def pourIt(self):
        self.log.info("Entering -> GUI ->  PourIt()")
        if messagebox.askyesno("Drinkin' Time?", "Are you sure the cup is in place and this is the drink you want?"):
            pass
        selection = self.listboxDrinkList.curselection()[0]
        selection = int(selection)
        theDrink = drinks.drink(*self.drinkList[selection])
        theDrink.printDrink()
        #self.currentDrink
        #self.arduino.sendDrink()
        self.log.info("Leaving  -> GUI -> Pourit()")
        pass
    
    def createNewDrink(self):
        selection = self.listboxDrinkList.curselection()[0]
        selection = int(selection)
        self.log.info("SELECTED INDEX: %s "%selection)
        self.log.info("DRINK SELECTED: %s " %self.drinkList[selection][1])
        self.log.info("DRINK Description: %s " %self.drinkList[int(self.listboxDrinkList.curselection()[0])][15])
        #var = self.arduino.readDrinkResponse() #this is temp in order to see if comms are working.
        #self.log.info("Arduino sent back : %s" %var)

    def refreshDetailView(self,garbage):
        selection = self.listboxDrinkList.curselection()[0]
        selection = int(selection)
        selectedDrink = self.drinkList[selection]
        self.descLabel.config(text=selectedDrink[15])
        self.nameLabel.config(text=selectedDrink[1])

    def populateList(self):
        self.drinkList = self.db.listDrinksByName()
        
        self.cloneList = list(self.drinkList)

        self.log.info(type(self.drinkList))
        self.reloadList()

    def reloadList(self):
        self.log.info("Entering -> GUI -> reloadList()")
        self.log.info(self.drinkList)
        
        #empty the list
        self.listboxDrinkList.delete(0, END)
        #Refill the list with now sorted data
        for drink in self.drinkList:
            self.listboxDrinkList.insert(END,drink[1])
        self.listboxDrinkList.select_set(0)

        self.log.info("Leaving  -> GUI -> reloadList()")

    def sortByName(self):
        self.log.info("Entering -> sortByName()")
        self.drinkList = sorted(self.drinkList, key=lambda derf : derf[1]) # The first column when it draws from DB is the name
        self.reloadList()
        self.log.info("Leaving -> sortByName()")
        for button in self.buttonList:
            button.config(relief=RAISED)
        self.buttonNameSort.config(relief = SUNKEN)

    def sortByPopularity(self):
        self.log.info("Entering -> sortByPopularity")
        self.drinkList = sorted(self.drinkList, key=lambda derf : derf[17], reverse=True) #Key 17 is popularity in the columns
        self.reloadList()
        self.log.info("Leaving -> sortByPopularity")
        for button in self.buttonList:
            button.config(relief=RAISED)
        self.buttonPopularitySort.config(relief = SUNKEN)

    def sortByDispenseCount(self):
        self.log.info("Entering -> sortByDispenseCount")
        self.drinkList = sorted(self.drinkList, key=lambda derf : derf[19], reverse=True)
        self.reloadList()
        self.log.info("Leaving -> sortByDispenseCount")
        for button in self.buttonList:
            button.config(relief=RAISED)
        self.buttonDispenseCountSort.config(relief = SUNKEN)

    def initStars(self):
        self.stars.append(PhotoImage(file = "C:\\Users\\Tadgh\Documents\GitHub\Drinkatron\Resources\Images\\zeroStars.gif"))
        self.stars.append(PhotoImage(file = "C:\\Users\\Tadgh\Documents\GitHub\Drinkatron\Resources\Images\\oneStar.gif"))
        self.stars.append(PhotoImage(file = "C:\\Users\\Tadgh\Documents\GitHub\Drinkatron\Resources\Images\\twoStars.gif"))
        self.stars.append(PhotoImage(file = "C:\\Users\\Tadgh\Documents\GitHub\Drinkatron\Resources\Images\\threeStars.gif"))
        self.stars.append(PhotoImage(file = "C:\\Users\\Tadgh\Documents\GitHub\Drinkatron\Resources\Images\\fourStars.gif"))
        self.stars.append(PhotoImage(file = "C:\\Users\\Tadgh\Documents\GitHub\Drinkatron\Resources\Images\\fiveStars.gif"))




app = UI()

        