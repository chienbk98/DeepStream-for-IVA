from myUI import Ui_MainWindow
import myUI
from PyQt5 import QtWidgets
import sys
import cv2

if __name__ == "__main__":
    myUI.image_result = cv2.imread("/home/yoona/Desktop/learn_python/PyQt5/home.jpg")
    App = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(App.exec_())