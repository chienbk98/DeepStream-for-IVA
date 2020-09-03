from myUI import Ui_MainWindow
from PyQt5 import QtWidgets
import myLib
import sys

if __name__ == '__main__':
    App = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(App.exec_())




