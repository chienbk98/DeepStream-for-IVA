from myUI import Ui_MainWindow, Ui_Form
import myUI
from PyQt5 import QtWidgets
import sys
import cv2
import threading
from myPipeline import PipeLine
import gi
gi.require_version("Gst", '1.0')
from gi.repository import GObject, Gst
from gi.repository import GLib
def capture_image(idx, uri):
  cap = cv2.VideoCapture(uri)
  while cap.isOpened():
    _, myUI.image_result[idx] = cap.read()
    if not _:
      break
  else:
    print("End streaming from: {}".format(uri))

def creatingPipeline():
      pp = PipeLine()
      pipeline = pp.pipeline
      print("Starting pipeline")
      pipeline.set_state(Gst.State.PLAYING)
      try:
          pp.loop.run()
      except:
          pass

      # cleanup
      print("Exiting app\n")
      pipeline.set_state(Gst.State.NULL)
if __name__ == "__main__":
    # App = QtWidgets.QApplication(sys.argv)
    # mainWindow = QtWidgets.QWidget()
    # ui = Ui_MainWindow()
    # ui.setupUi(mainWindow)
    # mainWindow.show()

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    # sys.exit(app.exec_())


    pp = PipeLine(on_screen_display=False, tracking=True)
    pipeline = pp.pipeline
    print("Starting pipeline")
    pipeline.set_state(Gst.State.PLAYING)
    try:
        pp.loop.run()
    except:
        pass
    print("Exiting app\n")
    pipeline.set_state(Gst.State.NULL)