from myUI import Ui_MainWindow
import myUI
from PyQt5 import QtWidgets
import sys
import cv2
import threading
def capture_image(idx, uri):
  cap = cv2.VideoCapture(uri)
  while cap.isOpened():
    _, myUI.image_result[idx] = cap.read()
    if not _:
      break
  else:
    print("End streaming from: {}".format(uri))

if __name__ == "__main__":
    a = cv2.imread("/home/yoona/Desktop/learn_python/PyQt5/home.jpg")
    b = cv2.imread("/home/yoona/Pictures/84534587_2692473420836014_4507958916096720896_o.jpg")
    c = cv2.imread("/home/yoona/Pictures/81041837_2692472010836155_3651594724206182400_o.jpg")
    myUI.image_result[0] = a
    myUI.image_result[1] = b
    myUI.image_result[2] = c
    
    t1 = threading.Thread(target=capture_image, args=(0, 0, ))
    t1.setDaemon(True)
    t2 = threading.Thread(target=capture_image, args=(1, "rtsp://192.168.1.9:43794", ))
    t2.setDaemon(True)
    t3 = threading.Thread(target=capture_image, args=(2,"rtsp://192.168.1.9:43794", ))
    t3.setDaemon(True)


    t1.start()
    t2.start()
    t3.start()


    App = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(App.exec_())