import dbinterface
import re
from tkinter import *



root = Tk()
root.title("Temp Drinkatron Work")
mainframe = Frame(root)

mainframe.grid(column = 0, row = 0)
drinkScrollList = Listbox(root)
drinkScrollList.grid(column = 0, row = 0)
root.mainloop()


