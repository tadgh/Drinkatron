from tkinter import * #need Tkinter for 2.7 and before
import constants
#import tkMessageBox
from tkinter import messagebox
import logging
import arduinocomm
import dbinterface
import drinks
import random
import os


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
        self.drinkObjArray = []

        logging.basicConfig(file="runLog.txt", level=logging.INFO)
        self.log = logging.getLogger("GUI ")
        self.currentListSelection = 0
        self.log.info("Entering -> GUI -> Constructor()")


        #TOPLEVEL FRAMEWORK
        self.root = Tk()
        self.root.title("Drinkatron v%s"%constants.VERSION)
        self.root.geometry("800x600")
        self.frame = Frame(self.root, width=800, height=600)

        self.status = StatusBar(self.root)
        self.status.set("Initializing UI...")

        #LISTBOX WORK
        self.listboxDrinkList = Listbox(self.root, font = ("Helvetica", 24 ), height=13)
        self.listboxDrinkList.grid(row=0,column = 0)
        self.listboxDrinkList.bind('<<ListboxSelect>>', self.refreshDetailView)#This is some wonky code that binds self.refreshDetailView as a callback when the ListBoxSelect TKAction is called.
        self.populateList()

        #star image loading
        self.stars = []
        self.initStars()

        #TODO this isn't really a toolbar i don't know why I named it that. Fix this once we find out what UI should look like.
        #toolbar work
        self.toolbar = Frame(self.frame)
        self.buttonAddDrink = Button(self.toolbar,text="Add Drink", width = 9, command = self.createNewDrink)
        self.buttonAddDrink.grid(column = 0, row = 2)
        self.toolbar.grid(column = 0, row = 1, columnspan=10, rowspan=15)

        #detail view work
        self.detailViewFrame = Frame(self.root)
        self.drinkImage = PhotoImage(file = os.path.join(os.path.dirname(__file__),"..","Resources","Images", "vodka.gif"))
        self.drinkImageLabel = Label(self.detailViewFrame, image=self.drinkImage, anchor=W)
        self.starImageLabel = Label(self.detailViewFrame, image=self.stars[0], anchor=W)
        self.nameLabel = Label(self.detailViewFrame, text="Placeholder",wraplength=300 , font = ("Helvetica", 24), anchor=W)
        self.descLabel = Label(self.detailViewFrame, text="Placeholder", wraplength=150, anchor=W)



        #gridding
        self.drinkImageLabel.grid(row = 1, column = 0, sticky = W)
        self.nameLabel.grid(row = 0, column = 0, sticky = W)
        self.starImageLabel.grid(row=3, column = 0, columnspan=2, sticky = W)
        self.descLabel.grid(row=2, column =0, sticky = W)
        self.detailViewFrame.grid(row = 0, column = 1, sticky=N+W)

        #slider view work
        self.sliderFrame = Frame(self.root)
        self.sliderFrame.grid(row = 1, column = 1, sticky = N+W)





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
        self.frameSortButtons.grid(column=0,row=5, sticky= N+W)

        self.status.grid(column=0,row=5)


        self.root.mainloop()
        self.log.info("Leaving  -> GUI -> Constructor()")

    def aboutMessageBox(self):
        msgbox = messagebox.showinfo("About", "Drinkatron is a personal bartender\n version: %s\nCopyright 2012"%constants.VERSION) 
    def menuQuit(self):
        self.log.info("Leaving  -> GUI -> mainLoop, quit was called")
        self.arduino.disconnect()
        self.root.destroy()


    def pourIt(self):
        self.log.info("Entering -> GUI ->  PourIt()")
        if messagebox.askyesno("Drinkin' Time?", "Are you sure the cup is in place and this is the drink you want?"):
            pass
        selection = self.listboxDrinkList.curselection()[0]
        selection = int(selection)
        drinkToPour = self.drinkObjArray[selection]
        self.log.info("Information -> GUI -> Drink to Pour is: %s" %drinkToPour.drinkName)
        self.arduino.sendDrink(drinkToPour)
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

    def refreshDetailView(self, temp):
        selection = self.listboxDrinkList.curselection()[0]
        selection = int(selection)
        selectedDrink = self.drinkObjArray[selection]
        self.descLabel.config(text=selectedDrink.description)
        self.nameLabel.config(text=selectedDrink.drinkName)
        self.drinkImageLabel.config(image=selectedDrink.image)
        self.starImageLabel.config(image=self.stars[random.randrange(0,6)])
        self.starImageLabel.config(image=self.stars[selectedDrink.starRating])

        #adding stiffness sliders
        currentRow = 0
        drinkIndex = 0
        sliderList = []
        currentSlider = 0
        totalSize = 0
        for ingredient in selectedDrink.ingredientListCleaned:
            totalSize += ingredient;
        for ingredient in selectedDrink.ingredientListCleaned:
            if ingredient != 0:
                Label(self.sliderFrame, text = "\n" + constants.INGREDIENTLIST[drinkIndex]).grid(row = currentRow, column = 0, sticky=N+W)
                sliderList.append(Scale(self.sliderFrame, from_ = 0, to = 100, orient = HORIZONTAL))
                sliderList[currentSlider].grid(row = currentRow, column = 1, sticky = N+W)
                currentRow += 1
                currentSlider += 1
            elif ingredient == 0:
                pass
            drinkIndex += 1






    def populateList(self):
        self.drinkList = self.db.listDrinksByName()
        ########################################
        #THIS IS CRUCIAL. this code initializes ALL drinks into an array, all at once. DO NOT FUCK WITH THIS CODE.
        for currentDrink in range(len(self.drinkList)):
            self.drinkObjArray.append(drinks.drink(*self.drinkList[currentDrink]))
            self.log.info(self.drinkObjArray[currentDrink].drinkName)
        #######################################


        self.log.info(type(self.drinkList))
        self.reloadList()

    def reloadList(self):
        self.log.info("Entering -> GUI -> reloadList()")
        
        #empty the list
        self.listboxDrinkList.delete(0, END)
        #Refill the list with now sorted data
        #for drink in self.drinkList:
        #    self.listboxDrinkList.insert(END,drink[1])#1 is the drink's name

        for drink in self.drinkObjArray:
            self.listboxDrinkList.insert(END,drink.drinkName)

        self.listboxDrinkList.select_set(0)

        self.log.info("Leaving  -> GUI -> reloadList()")

    def sortByName(self):
        self.log.info("Entering -> sortByName()")
        #self.drinkList = sorted(self.drinkList, key=lambda derf : derf[1]) # The first column when it draws from DB is the name
        self.drinkObjArray = sorted(self.drinkObjArray, key=lambda derf : derf.drinkName)#grabs Drink Name
        self.log.info(self.drinkObjArray)

        self.reloadList()
        self.refreshDetailView("")
        self.log.info("Leaving -> sortByName()")
        for button in self.buttonList:
            button.config(relief=RAISED)
        self.buttonNameSort.config(relief = SUNKEN)

    def sortByPopularity(self):
        self.log.info("Entering -> sortByPopularity")
       #self.drinkList = sorted(self.drinkList, key=lambda derf : derf[17], reverse=True) #Key 17 is popularity in the columns
        self.drinkObjArray = sorted(self.drinkObjArray, key=lambda derf : derf.positiveVoteCount, reverse = True)#grabs Drink Name
        self.log.info(self.drinkObjArray)
        self.reloadList()
        self.refreshDetailView("")
        self.log.info("Leaving -> sortByPopularity")
        for button in self.buttonList:
            button.config(relief=RAISED)
        self.buttonPopularitySort.config(relief = SUNKEN)

    def sortByDispenseCount(self):
        self.log.info("Entering -> sortByDispenseCount")
        #self.drinkList = sorted(self.drinkList, key=lambda derf : derf[19], reverse=True)
        self.drinkObjArray = sorted(self.drinkObjArray, key=lambda derf : derf.dispenseCount, reverse = True)#grabs Drink Name
        self.log.info(self.drinkObjArray)

        self.reloadList()
        self.refreshDetailView("")
        self.log.info("Leaving -> sortByDispenseCount")
        for button in self.buttonList:
            button.config(relief=RAISED)
        self.buttonDispenseCountSort.config(relief = SUNKEN)

    def initStars(self):
        self.stars.append(PhotoImage(file = os.path.join(os.path.dirname(__file__),"..","Resources","Images", "zeroStars.gif")))
        self.stars.append(PhotoImage(file = os.path.join(os.path.dirname(__file__),"..","Resources","Images", "oneStar.gif")))
        self.stars.append(PhotoImage(file = os.path.join(os.path.dirname(__file__),"..","Resources","Images", "twoStars.gif")))
        self.stars.append(PhotoImage(file = os.path.join(os.path.dirname(__file__),"..","Resources","Images", "threeStars.gif")))
        self.stars.append(PhotoImage(file = os.path.join(os.path.dirname(__file__),"..","Resources","Images", "fourStars.gif")))
        self.stars.append(PhotoImage(file = os.path.join(os.path.dirname(__file__),"..","Resources","Images", "fiveStars.gif")))




app = UI()

        