import dbinterface
import re
from tkinter import *
import logging
import time

root = Tk()
root.title("Temp Drinkatron Work")
mainframe = Frame(root)
sortNameRadio = Radiobutton(root)
mainframe.grid(column = 0, row = 0)
drinkLister = drinkScrollList = Listbox(root)
drinkScrollList.grid(column = 0, row = 0)
#root.mainloop()


class GUIWork:
    def __init__(self):
        self.db = dbinterface.DB()
        self.drinkList = []
        logging.basicConfig(file="runLog.txt", level=logging.INFO)
        self.log = logging.getLogger("GUI")

    def populateList(self):
        self.drinkList = self.db.listDrinksByName()
        self.cloneList = list(self.drinkList)

        self.log.info(type(self.drinkList))
        self.reloadList()

    def reloadList(self):
        self.log.info("Entering -> reloadList()")
        self.log.info(self.drinkList)
        #self.drinkList = self.cloneList[:]
        #todo need to push to GUI LISTBOX
        self.log.info("Leaving  -> reloadList()")

    def sortByName(self):
        self.log.info("Entering -> sortByName()")
        self.drinkList = sorted(self.drinkList, key=lambda derf : derf[1])
        self.reloadList()
        self.log.info("Leaving -> sortByName()")

    def sortByPopularity(self):
        self.log.info("Entering -> sortByPopularity")
        self.drinkList = sorted(self.drinkList, key=lambda derf : derf[17], reverse=True)
        self.reloadList()
        self.log.info("Leaving -> sortByPopularity")

    def sortByDispenseCount(self):
        self.log.info("Entering -> sortByDispenseCount")
        self.drinkList = sorted(self.drinkList, key=lambda derf : derf[19], reverse=True)
        self.reloadList()
        self.log.info("Leaving -> sortByDispenseCount")


if __name__=='__main__':
    gui = GUIWork()
    gui.populateList()
    gui.sortByDispenseCount()
    gui.sortByPopularity()

