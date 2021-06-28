import sys
from PyQt5 import QtWidgets
from gui import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    input() # Just here to avoid closing the window as soon as it runs