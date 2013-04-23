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


        #TOPLEVEL FRAMES
        self.root = Tk()
        self.detailViewFrame = Frame(self.root, bd=1,bg="yellow",width = 400,height=520,relief=SUNKEN)
        self.sliderFrame = Frame(self.root,bd=1,bg="blue",width=400, height = 280 ,relief=RAISED)
        self.buttonFrame = Frame(self.root,bd=1,bg="red",relief=SUNKEN)


        self.root.title("Drinkatron v%s"%constants.VERSION)
        self.root.geometry("1280x800")


        self.status = StatusBar(self.root)
        self.status.set("Initializing UI...")

        #LISTBOX WORK
        self.listboxDrinkList = Listbox(self.root, font = ("Helvetica", 42 ), height=12, width=20)

        self.listboxDrinkList.bind('<<ListboxSelect>>', self.refreshDetailView)#This is some wonky code that binds self.refreshDetailView as a callback when the ListBoxSelect TKAction is called.
        self.populateList()
        self.listboxDrinkList.select_set(0)#testing

        #star image loading
        self.stars = []
        self.initStars()


        #detail view work
        self.drinkImage = PhotoImage(file = os.path.join(os.path.dirname(__file__),"..","Resources","Images", "vodka.gif"))
        self.drinkImageLabel = Label(self.detailViewFrame, image=self.drinkImage, anchor=W)
        self.starImageLabel = Label(self.detailViewFrame, image=self.stars[0], anchor=W)
        self.nameLabel = Label(self.detailViewFrame, text="Placeholder",wraplength=500 , font = ("Helvetica", 24), anchor=W)
        self.descLabel = Label(self.detailViewFrame, text="Placeholder", anchor=W,height = 1)
        self.dummyDescLabel = Label(self.detailViewFrame,text="\n\n\n")

        #gridding
        self.drinkImageLabel.grid(row = 1, column = 0,columnspan=10)#padx=50)#to allow space for the dispense button
        self.nameLabel.grid(row = 0, column = 0,sticky = N)
        self.starImageLabel.grid(row=3, column = 0, columnspan=2, sticky = W, padx=50)
        #self.dummyDescLabel.grid(row=2,column=0, sticky=W, padx=50)
        self.descLabel.grid(row=2, column =0, sticky = W, padx=53)


        #slider view work
        self.sliderList = []
        self.sliderLabelList = []
        self.sliderVariables = [DoubleVar, DoubleVar, DoubleVar, DoubleVar, DoubleVar]
        #Slider Labels
        fsl1 = Label(self.sliderFrame,font=("Helvetica", 24), text =  "Placeholder",justify=LEFT,padx=10)
        fsl1.grid(row = 0, column = 0, sticky=N+W)
        fsl2 = Label(self.sliderFrame,font=("Helvetica", 24), text =  "Placeholder",justify=LEFT,padx=10)
        fsl2.grid(row = 1, column = 0, sticky=N+W)
        fsl3 = Label(self.sliderFrame,font=("Helvetica", 24), text =  "Placeholder",justify=LEFT,padx=10)
        fsl3.grid(row = 2, column = 0, sticky=N+W)
        fsl4 = Label(self.sliderFrame,font=("Helvetica", 24), text =  "Placeholder",justify=LEFT,padx=10)
        fsl4.grid(row = 3, column = 0, sticky=N+W)
        fsl5 = Label(self.sliderFrame,font=("Helvetica", 24), text =  "Placeholder",justify=LEFT,padx=10)
        fsl5.grid(row = 4, column = 0, sticky=N+W)
        #Actual sliders

        s1 = Scale(self.sliderFrame,variable = self.sliderVariables[0], from_ = 0, to = 100, orient = HORIZONTAL, showvalue=0, length = 400)
        s1.grid(row = 0, column = 1, sticky=N+E)
        s2 = Scale(self.sliderFrame,variable = self.sliderVariables[1], from_ = 0, to = 100, orient = HORIZONTAL, showvalue=0, length = 400)
        s2.grid(row = 1, column = 1, sticky=N+E)
        s3 = Scale(self.sliderFrame,variable = self.sliderVariables[2], from_ = 0, to = 100, orient = HORIZONTAL, showvalue=0, length = 400)
        s3.grid(row = 2, column = 1, sticky=N+E)
        s4 = Scale(self.sliderFrame,variable = self.sliderVariables[3], from_ = 0, to = 100, orient = HORIZONTAL, showvalue=0, length = 400)
        s4.grid(row = 3, column = 1, sticky=N+E)
        s5 = Scale(self.sliderFrame,variable = self.sliderVariables[4], from_ = 0, to = 100, orient = HORIZONTAL, showvalue=0, length = 400)
        s5.grid(row = 4, column = 1, sticky=N+E)

        self.sliderLabelList = [fsl1, fsl2, fsl3, fsl4, fsl5]
        self.sliderList = [s1,s2,s3,s4,s5]


        #TODO reminder: These are not gridded because we swapped to a dropdown.
        #Sorting button work
        #self.frameSortButtons = Frame(self.root)
        #self.buttonNameSort = Button(self.frameSortButtons,text = "A-Z",width = 9,height = 4, command = self.sortByName)
        #self.buttonPopularitySort = Button(self.frameSortButtons,text = "Popularity",width = 9,height = 4, command = self.sortByPopularity)
        #self.buttonDispenseCountSort = Button(self.frameSortButtons,text = "Dispenses",width = 9,height = 4, command = self.sortByDispenseCount)
        #list of buttons in order to change relief and colour.
        #self.buttonList = [self.buttonNameSort,self.buttonDispenseCountSort,self.buttonPopularitySort]
        #self.buttonNameSort.grid(column=0, row=0)
        #self.buttonPopularitySort.grid(column=1, row=0)
        #self.buttonDispenseCountSort.grid(column=2, row=0)


        #frame for all current buttons

        #All buttons and dropdown initialization
        self.varSort = StringVar()
        self.varSort.set("A-Z")
        self.sortMenu = OptionMenu(self.buttonFrame, self.varSort, "A-Z", "Popularity", "Dispense Count")
        self.sortMenu.config(font=("Helvetica", 20),width=len("Dispense Count"))
        #this trace follows the value of self.varSort and binds it to self.sortingChanged
        self.varSort.trace('w', self.sortingChanged)
        #random button
        self.randomButton = Button(self.buttonFrame, text='Random', command=self.chooseRandomDrink)
        self.randomButton.config(font=("Helvetica", 20),width=len("Dispense Count"))
        #'Surprise me' button
        self.surpriseButton = Button(self.buttonFrame, text='Surprise me!', command=self.chooseSurpriseDrink)
        self.surpriseButton.config(font=("Helvetica", 20),width=len("Dispense Count"))
        #dispenseButton
        self.dispenseButton = Button(self.buttonFrame, text='dispense', command=self.pourIt)
        self.dispenseButton.config(font=("Helvetica", 20),width=len("Dispense Count"))

        #BUTTONFRAME GRIDDING
        self.sortMenu.grid(sticky=W)
        self.randomButton.grid(sticky=W)
        self.surpriseButton.grid(sticky=W)
        self.dispenseButton.grid(sticky=W)



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
        self.listboxDrinkList.grid(row=0,column = 0,rowspan=2, sticky=N+W)
        self.detailViewFrame.grid(row = 0, column = 1)
        self.detailViewFrame.grid_propagate(False)
        self.sliderFrame.grid(row = 1, column = 1, sticky = N+W)
        self.sliderFrame.grid_propagate(False)#propagate(False) prevents the frame from resizing based on widget size.
        self.buttonFrame.grid(row = 0, column = 2,sticky=N+W)

        #self.frameSortButtons.grid(column=0,row=1, sticky= N+W) THIS IS COMMENTED AS IT IS BUTTON RELATED AND NOT DROPDOWN RELATED
        self.status.set("Ready...")
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
        sliderIndex = 0
        dispenseArray = []
        for i in drinkToPour.ingredientListCleaned:
            if i != 0:
                dispenseArray.append(self.sliderList[sliderIndex].get())
                sliderIndex += 1
            else:
                dispenseArray.append(0)
        self.log.info(dispenseArray)
        self.log.info("Information -> GUI -> Drink to Pour is: %s" %drinkToPour.drinkName)
        self.arduino.sendDrink(dispenseArray)
        self.log.info("Leaving  -> GUI -> Pourit()")

    def createNewDrink(self):
        selection = self.listboxDrinkList.curselection()[0]
        selection = int(selection)
        self.log.info("SELECTED INDEX: %s "%selection)
        self.log.info("DRINK SELECTED: %s " %self.drinkList[selection][1])
        self.log.info("DRINK Description: %s " %self.drinkList[int(self.listboxDrinkList.curselection()[0])][15])

    def refreshDetailView(self, temp):
        selection = self.listboxDrinkList.curselection()[0]
        selection = int(selection)
        selectedDrink = self.drinkObjArray[selection]
        self.descLabel.config(text=selectedDrink.description)
        self.nameLabel.config(text=selectedDrink.drinkName)
        self.drinkImageLabel.config(image=selectedDrink.image)
        self.starImageLabel.config(image=self.stars[selectedDrink.starRating])

        #adding stiffness sliders
        #this hides all current sliders and sets them all to 0
        for i in range(0,5):
            try:
                self.sliderList[i].set(0)
                self.sliderLabelList[i].grid_forget()
                self.sliderList[i].grid_forget()
            except IndexError:
                pass

        currentRow = 0
        drinkIndex = 0

        #This for block relabels all the sliders and populates the necessary amount of sliders with appropriate proportions
        for ingredient in selectedDrink.ingredientListCleaned:

            if ingredient != 0:
                self.sliderLabelList[currentRow].config(text =  constants.INGREDIENTLIST[drinkIndex])
                #self.sliderLabelList[currentRow].grid(column = 0, row = currentRow, sticky=W ) #TODO temp comment out to test Label Functionality of Scale widgets.
                self.sliderList[currentRow].config(label=constants.INGREDIENTLIST[drinkIndex], font=("Arial", 24))
                self.sliderList[currentRow].grid(column = 1, row=currentRow,sticky=E)

                proportion = DoubleVar()
                proportion = ingredient / float(selectedDrink.totalSize)
                self.sliderList[currentRow].set(proportion * 100)
                currentRow += 1
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

        self.initDrinkImages()
        #######################################


        self.log.info(type(self.drinkList))
        self.reloadList()

    def reloadList(self):
        self.log.info("Entering -> GUI -> reloadList()")

        #empty the list
        self.listboxDrinkList.delete(0, END)

        for drink in self.drinkObjArray:
            self.listboxDrinkList.insert(END,drink.drinkName)

        self.log.info("Leaving  -> GUI -> reloadList()")

    def chooseRandomDrink(self): #function called when 'Random' button is selected
        num_drinks = self.listboxDrinkList.size()
        which_drink = random.randint(0, num_drinks-1)
        self.reloadList()
        self.listboxDrinkList.select_set(which_drink)
        self.listboxDrinkList.see(which_drink)
        self.refreshDetailView("")

    def chooseSurpriseDrink(self): #function called when 'Surprise me!' button is selected
        num_drinks = self.listboxDrinkList.size()
        which_drink = random.randint(0, num_drinks-1)
        self.pourIt()

    def sortingChanged(self,t1,t2,t3):#these are garbage variables due to the widget returning 4 positional args
        #This gets callbacked when the dropdown changes.
        self.whichSort = self.varSort.get()
        if self.whichSort == "A-Z":
            self.sortByName()
        elif self.whichSort == "Popularity":
            self.sortByPopularity()
        elif self.whichSort == "Dispense Count":
            self.sortByDispenseCount()

    def sortByName(self):
        self.log.info("Entering -> sortByName()")
        #self.drinkList = sorted(self.drinkList, key=lambda derf : derf[1]) # The first column when it draws from DB is the name
        self.drinkObjArray = sorted(self.drinkObjArray, key=lambda derf : derf.drinkName)#grabs Drink Name
        self.log.info(self.drinkObjArray)

        self.reloadList()
        self.listboxDrinkList.select_set(0)
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
        self.listboxDrinkList.select_set(0)
        self.refreshDetailView("") #requires garbage argument
        self.log.info("Leaving -> sortByPopularity")
        for button in self.buttonList:
            button.config(relief=RAISED)
        self.buttonPopularitySort.config(relief = SUNKEN)

    def sortByDispenseCount(self):
        self.log.info("Entering -> sortByDispenseCount")
        #self.drinkList = sorted(self.drinkList, key=lambda derf : derf[19], reverse=True)
        self.drinkObjArray = sorted(self.drinkObjArray, key=lambda derf : derf.dispenseCount, reverse = True)#grabs Drink Name
        self.log.info(self.drinkObjArray)

    def sortByIngredient(self, ingredient):
        self.reloadList()
        self.listboxDrinkList.select_set(0)
        self.refreshDetailView("")
        self.log.info("Leaving -> sortByDispenseCount")
        for button in self.buttonList:
            button.config(relief=RAISED)
        self.buttonDispenseCountSort.config(relief = SUNKEN)

    def sortByKey(self, key):
        self.log.info("Entering -> sortByKey")
        #todo actually write this shit and figure out how to pass a
        self.log.info("Leaving -> sortByKey")

    def initDrinkImages(self):
        for drink in self.drinkObjArray:
            drink.image = PhotoImage(file = os.path.join(os.path.dirname(__file__),"..", "Resources", "Images", drink.imagePath))

    def initStars(self):
        self.stars.append(PhotoImage(file = os.path.join(os.path.dirname(__file__),"..","Resources","Images", "zeroStars.gif")))
        self.stars.append(PhotoImage(file = os.path.join(os.path.dirname(__file__),"..","Resources","Images", "oneStar.gif")))
        self.stars.append(PhotoImage(file = os.path.join(os.path.dirname(__file__),"..","Resources","Images", "twoStars.gif")))
        self.stars.append(PhotoImage(file = os.path.join(os.path.dirname(__file__),"..","Resources","Images", "threeStars.gif")))
        self.stars.append(PhotoImage(file = os.path.join(os.path.dirname(__file__),"..","Resources","Images", "fourStars.gif")))
        self.stars.append(PhotoImage(file = os.path.join(os.path.dirname(__file__),"..","Resources","Images", "fiveStars.gif")))

app = UI()


