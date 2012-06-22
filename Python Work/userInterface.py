from Tkinter import *
import constants
import tkMessageBox
import logging
import thread

logging.basicConfig(file="runLog.txt", level=logging.INFO)
log = logging.getLogger("master")

class UI:
    def __init__(self):
        self.currentListSelection = 0
        log.info("Entering -> GUI -> Constructor()")

        #TOPLEVEL FRAMEWORK
        self.root = Tk()
        self.root.title("Drinkatron v%s"%constants.VERSION)
        self.frame = Frame(self.root, width=800, height=600)
        self.frame.pack()
        
        #MENUWORK
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.fileMenu = Menu(self.menu)
        self.aboutMenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu = self.fileMenu)
        self.menu.add_cascade(label="About", menu = self.aboutMenu)
        self.aboutMenu.add_command(label="About", command=self.aboutMessageBox)
        self.fileMenu.add_command(label="Quit", command=self.menuQuit)
        log.info("Entering -> GUI -> mainLoop()")

        self.root.mainloop()
        log.info("Leaving  -> GUI -> Constructor()")

    def aboutMessageBox(self):
        msgbox = tkMessageBox.showinfo("About", "Drinkatron is a personal bartender\n version: %s\nCopyright 2012"%constants.VERSION) 

    def menuQuit(self):
        log.info("Leaving  -> GUI -> mainLoop, quit was called")
        self.root.destroy()

    def pourIt(self):
        log.info("Entering -> GUI ->  PourIt()"
        #drinkSelected = grab current selection from thing.
        #thread.start_new_thread(drink.dispenseDrink, [drinkSelected.id,])
        log.info("Leaving  -> GUI -> Pourit()")
    
        



app = UI()
        