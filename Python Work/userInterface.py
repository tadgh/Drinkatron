from tkinter import * #need Tkinter for 2.7 and before
import constants
#import tkMessageBox
from tkinter import messagebox
import logging
import arduinocomm



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
        self.arduino = arduinocomm.Connection()

        logging.basicConfig(file="runLog.txt", level=logging.INFO)
        self.log = logging.getLogger("master")
        self.currentListSelection = 0
        self.log.info("Entering -> GUI -> Constructor()")


        #TOPLEVEL FRAMEWORK
        self.root = Tk()
        self.root.title("Drinkatron v%s"%constants.VERSION)
        self.root.geometry("800x600")
        self.frame = Frame(self.root, width=800, height=550)

        self.status = StatusBar(self.root)
        self.status.set("Initializing UI...")



        #toolbar work
        self.toolbar = Frame(self.frame)
        self.exitButton = Button(self.toolbar,text="Add Drink", width = 9, command = self.createNewDrink)
        self.exitButton.pack(side=LEFT, padx=2, pady=2)

        self.toolbar.pack(side=BOTTOM)

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
        self.frame.pack(fill=X)
        self.status.pack(side=BOTTOM, fill=X)


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
        #drinkSelected = grab current selection from thing.
        #thread.start_new_thread(arduino.dispenseDrink, [drinkSelected.id,])
        self.log.info("Leaving  -> GUI -> Pourit()")
        pass
    
    def createNewDrink(self):
        var = self.arduino.readDrinkResponse() #this is temp in order to see if comms are working.
        self.log.info("Arduino sent back : %s" %var)

        pass



app = UI()

        