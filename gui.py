from PyQt5 import QtCore, QtGui, QtWidgets

import os
import importlib
import pickle

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
        if module not in ("Action", "__init__"): actionsList.append(modClass)




class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setObjectName("MainWindow")
        self.resize(800, 600)

        self.path = ""

        self.gridLayoutWidget = QtWidgets.QWidget()
        #self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        
        self.mainLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.mainLayout.setObjectName("mainLayout")

        # ActionMethodInput Section
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.actionMethodInput = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.actionMethodInput.setMaximumSize(QtCore.QSize(16777215, 50))
        self.actionMethodInput.setPlaceholderText("Please select an action from the dropdown to the right")
        self.mainLayout.addWidget(self.actionMethodInput, 0, 0, 1, 1)

        sizePolicy.setHeightForWidth(self.actionMethodInput.sizePolicy().hasHeightForWidth())

        # ActionDropdown section
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.actionDropdown = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.actionDropdown.setSizePolicy(sizePolicy)
        self.actionDropdown.setMaximumSize(QtCore.QSize(100, 50))

        sizePolicy.setHeightForWidth(self.actionDropdown.sizePolicy().hasHeightForWidth())

        # ActionAdd section
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.actionAdd = QtWidgets.QPushButton(self.gridLayoutWidget)
        # TODO: Add icon to actionAdd
        self.actionAdd.setSizePolicy(sizePolicy)
        self.actionAdd.setMaximumSize(QtCore.QSize(50, 50))

        sizePolicy.setHeightForWidth(self.actionAdd.sizePolicy().hasHeightForWidth())


        self.actionList = QtWidgets.QListWidget(self.gridLayoutWidget)
        self.actionList.workSpace = []

        self.mainLayout.addWidget(self.actionDropdown, 0, 1, 1, 1)
        self.mainLayout.addWidget(self.actionAdd, 0, 2, 1, 1)
        self.mainLayout.addWidget(self.actionList, 1, 0, 1, 3)
        
        

        self.menubar = QtWidgets.QMenuBar(self)
        self.openMenu = QtWidgets.QMenu(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.runFile = QtWidgets.QAction(self)
        self.editFile = QtWidgets.QAction(self)

        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))

        # Status bar names
        self.menubar.setObjectName("menubar")
        self.openMenu.setObjectName("openMenu")
        self.statusbar.setObjectName("statusbar")
        self.runFile.setObjectName("runFile")
        self.editFile.setObjectName("editFile")

        self.actionMethodInput.setObjectName("actionMethodInput")
        self.actionDropdown.setObjectName("actionDropdown")
        self.actionList.setObjectName("actionList")


        self.setCentralWidget(self.gridLayoutWidget)
        self.setStatusBar(self.statusbar)
        self.setMenuBar(self.menubar)

        self.actionAdd.clicked.connect(self.addButtonClick)
        self.editFile.triggered.connect(self.openFile)
        self.runFile.triggered.connect(self.runWorkspaceFile)

        self.openMenu.addAction(self.runFile)
        self.openMenu.addAction(self.editFile)
        self.menubar.addAction(self.openMenu.menuAction())

        self.retranslateUi()
        self.initializeDropdown()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "CobaltWorkshop"))
        self.actionMethodInput.setToolTip(_translate("MainWindow", "<p>Specify the directions you want to take when using an action</p>"))
        self.actionDropdown.setToolTip(_translate("MainWindow", "<p>Select the action type you want to take here</p>"))
        self.openMenu.setTitle(_translate("MainWindow", "Open"))
        self.runFile.setText(_translate("MainWindow", "Run Workshop File"))
        self.editFile.setText(_translate("MainWindow", "Edit Workshop File"))
    
    def createListItemFromDataclass(self, dataclass : DataClass):
        item = QtWidgets.QListWidgetItem(self.actionList)
        custom = ListItem(self.actionList, item)

        itemClass = actionsList.getFromString(dataclass.bridgeClass)
        custom.completeInfo(itemClass(dataclass))

        # These are both important variables for accessing and changing things from inside of 'ListItem'
        item.connection = custom
        item.parent = self.actionList

        item.setSizeHint(custom.sizeHint())
    
        self.actionList.addItem(item)
        self.actionList.setItemWidget(item, custom)

    def initializeDropdown(self):
        self.actionDropdown.addItems([action.__name__ for action in actionsList])
        self.actionDropdown.activated[str].connect(self.onDropdownSelectionChange)
    
    def onDropdownSelectionChange(self):
        item = actionsList[self.actionDropdown.currentIndex()]
        self.actionMethodInput.setPlaceholderText(item.hintText)
    
    def addButtonClick(self):
        itemClass = actionsList[self.actionDropdown.currentIndex()]
        itemData = DataClass(itemClass.__name__, self.actionMethodInput.toPlainText())
        self.actionMethodInput.clear()
        self.actionList.workSpace.append(itemData)
        self.createListItemFromDataclass(itemData)
    
    def closeEvent (self, QCloseEvent):
        if len(self.actionList.workSpace) > 0:
            self.saveFile()
        return super(MainWindow, self).closeEvent(QCloseEvent)
    
    def saveFile(self):
        filepath = self.path
        if len(self.path) == 0:
            filepath = QtWidgets.QFileDialog.getSaveFileName(None, "Save a workspace File", filter = "Cobalt Workspace File (*.coblt)")[0]
        
        if len(filepath) == 0:
            return # Break when filepath does not exist
        
        with open(filepath, 'wb') as filename:
            #TODO Fix listItem object so it can be pickled
            pickle.dump(self.actionList.workSpace, filename)

    def openFile(self):
        self.path = QtWidgets.QFileDialog.getOpenFileName(None, "Open a workspace File", filter = "Cobalt Workspace File (*.coblt)")[0]
        if len(self.path) == 0:
            return
        with open(self.path, 'rb') as picklefile:
            
            self.actionList.workSpace = pickle.load(picklefile)
            
            for dataclass in self.actionList.workSpace:
                self.createListItemFromDataclass(dataclass)
    
    def runWorkspaceFile(self):
        for dataclass in self.actionList.workSpace:
            itemClass = actionsList.getFromString(dataclass.bridgeClass)
            itemClass(dataclass).run()

    





