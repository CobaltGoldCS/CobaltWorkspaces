from PyQt5 import QtCore, QtGui, QtWidgets

import os
import importlib
import pickle
from multiprocessing import Process


from customClasses.DataClass import DataClass
from customClasses.Item import ListItem
from customClasses.CustomList import CustomList

# Import everything from actions folder
actionsList = CustomList()
for name in os.listdir("actions"):
    if name.endswith(".py"):
        #strip the extension
        module = name[:-3]
        # set the module name in the current global name space:
        mod = importlib.import_module(f"actions.{module}")
        modClass = getattr(mod, module)
        # Add the class to the list of actions (the list can automatically pick one)
        if module not in ("Action", "__init__"): actionsList.append(modClass)

class GuiActions:

    def __init__(self, window: QtWidgets.QMainWindow):
        self.window = window
    def createListItemFromDataclass(self, dataclass : DataClass):
        item = QtWidgets.QListWidgetItem(self.window.actionList)
        custom = ListItem(self.window.actionList, item)

        itemClass = actionsList.getFromString(dataclass.bridgeClass)
        custom.completeInfo(itemClass(dataclass))

        # These are both important variables for accessing and changing things from inside of 'ListItem'
        item.connection = custom
        item.parent = self.window.actionList

        item.setSizeHint(custom.sizeHint())
    
        self.window.actionList.addItem(item)
        self.window.actionList.setItemWidget(item, custom)

    def initializeDropdown(self):
        self.window.actionDropdown.addItems([action.__name__ for action in actionsList])
        self.window.actionDropdown.activated[str].connect(self.onDropdownSelectionChange)
    
    def onDropdownSelectionChange(self):
        item = actionsList[self.window.actionDropdown.currentIndex()]
        self.window.actionMethodInput.setPlaceholderText(item.hintText)
    
    def addButtonClick(self):
        itemClass = actionsList[self.window.actionDropdown.currentIndex()]
        itemData = DataClass(itemClass.__name__, self.window.actionMethodInput.toPlainText())
        self.window.actionMethodInput.clear()
        self.window.actionList.workSpace.append(itemData)
        self.createListItemFromDataclass(itemData)
    
    def saveFile(self):
        filepath = self.path
        if len(self.path) == 0:
            filepath = QtWidgets.QFileDialog.getSaveFileName(None, "Save a workspace File", filter = "Cobalt Workspace File (*.coblt);;All Files (*.*)")[0]
        
        if len(filepath) == 0: return # Break when filepath does not exist
        
        with open(filepath, 'wb') as filename:
            pickle.dump(self.actionList.workSpace, filename)

    def openFile(self):
        self.path = QtWidgets.QFileDialog.getOpenFileName(None, "Open a workspace File", filter = "Cobalt Workspace File (*.coblt);;All Files (*.*)")[0]
        if len(self.path) == 0:
            return
        with open(self.path, 'rb') as picklefile:
            self.window.actionList.workSpace = pickle.load(picklefile)
            self.window.actionList.clear()
            for dataclass in self.window.actionList.workSpace:
                self.createListItemFromDataclass(dataclass)
    
    def runWorkspaceFile(self):
        for dataclass in self.window.actionList.workSpace:
            process = Process(target = self.executeAction(dataclass))
            process.start()
            process.join()
    
    def executeAction(self, dataclass : DataClass):
            itemClass = actionsList.getFromString(dataclass.bridgeClass)
            itemClass(dataclass).run()