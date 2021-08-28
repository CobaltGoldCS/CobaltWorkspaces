from PyQt5 import QtCore, QtGui, QtWidgets

import os
import importlib
import pickle
from multiprocessing import Process


from customClasses.CustomList import CustomList
from guiActions import GuiActions





class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        """Sets up the initial Ui Components

        Args:
            parent (QtWidgets.QWidget, optional): The parent of this window. Defaults to None.
        """
        super(MainWindow, self).__init__(parent)
        self.setObjectName("MainWindow")
        self.resize(800, 600)

        self.path = str("")
        self.controller = GuiActions(self)

        
        self.gridLayoutWidget = QtWidgets.QWidget()
        #self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        
        self.mainLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.mainLayout.setObjectName("mainLayout")

        # ActionMethodInput Section
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.actionMethodInput = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.actionMethodInput.setMaximumSize(QtCore.QSize(17725, 50))
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
        icon = QtGui.QIcon(os.path.join("icons", "addItem.png"))
        self.actionAdd.setIcon(icon)
        self.actionAdd.setIconSize(QtCore.QSize(50, 50))
        self.actionAdd.setSizePolicy(sizePolicy)
        self.actionAdd.setStyleSheet("QPushButton {border-radius: 10px}")
        self.actionAdd.setMaximumSize(QtCore.QSize(50, 50))

        sizePolicy.setHeightForWidth(self.actionAdd.sizePolicy().hasHeightForWidth())


        self.actionList = QtWidgets.QListWidget(self.gridLayoutWidget)
        self.actionList.workSpace = []

        self.mainLayout.addWidget(self.actionDropdown, 0, 1, 1, 1)
        self.mainLayout.addWidget(self.actionAdd, 0, 2, 1, 1)
        self.mainLayout.addWidget(self.actionList, 1, 0, 1, 3)
        
        # Set up Menu Bar

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

        self.actionAdd.clicked.connect(self.controller.addButtonClick)
        self.editFile.triggered.connect(self.controller.openFile)
        self.runFile.triggered.connect(self.controller.runWorkspaceFile)

        self.openMenu.addAction(self.runFile)
        self.openMenu.addAction(self.editFile)
        self.menubar.addAction(self.openMenu.menuAction())

        self.retranslateUi()
        self.controller.initializeDropdown()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        """Adds a lot of string information pertaining to items like tooltips and menu items
        """
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "CobaltWorkshop"))
        self.actionMethodInput.setToolTip(_translate("MainWindow", "<p>Specify the directions you want to take when using an action</p>"))
        self.actionDropdown.setToolTip(_translate("MainWindow", "<p>Select the action type you want to take here</p>"))
        
        self.openMenu.setTitle(_translate("MainWindow", "Open"))
        self.runFile.setText(_translate("MainWindow", "Run Workshop File"))
        self.editFile.setText(_translate("MainWindow", "Edit Workshop File"))

        self.actionMethodInput.setPlaceholderText("Please select an action from the dropdown to the right")

    def closeEvent (self, QCloseEvent):
        if len(self.actionList.workSpace) > 0:
            self.controller.saveFile()
        return super(MainWindow, self).closeEvent(QCloseEvent)