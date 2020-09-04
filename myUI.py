from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QGridLayout, \
    QHBoxLayout, QVBoxLayout, QLabel, QSlider, QStyle, QSizePolicy, QFileDialog
from PyQt5.QtGui import QIcon, QPalette, QImage, QPixmap, QMouseEvent
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QUrl, QTimer
from datetime import datetime
from os import path
import numpy as np
import threading
import myLib
from myLib import warningMethod
import cv2
import os



sample_image = cv2.imread("/home/yoona/Pictures/114437066_588098281851846_8163055224235357808_n.jpg")
image_result = [sample_image] * 3
feature = {
    'car1': True,
    'mpa1': True,
    'person1': True,
    'illegal1': True,

    'car2': True,
    'mpa2': True,
    'person2': True,
    'illegal2': True,   

    'car3': True,
    'mpa3': True,
    'person3': True,
    'illegal3': True
}
MONTH = { 1:'January',
          2:'February',
          3:'March',
          4:'April',
          5:'May',
          6:'June',
          7:'July',
          8:'August',
          9:'September',
          10:'October',
          11:'November',
          12:'December'}

class Ui_MainWindow(QWidget): 
    def __init__(self, feature = feature):
        super().__init__()
        self.feature = feature
        self.points_CAM1 = []
        self.points_CAM2 = []
        self.points_CAM3 = []
        self.numWarning = 0
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1048, 375)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

 # View CAM 1
        self.gridLayout = QtWidgets.QGridLayout(self.tab)
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.CAM1 = QtWidgets.QLabel(self.tab)
        self.CAM1.setMinimumSize(QtCore.QSize(320, 240))
        self.CAM1.setMaximumSize(QtCore.QSize(426, 400))
        self.CAM1.setFrameShape(QtWidgets.QFrame.Box)
        self.CAM1.setObjectName("CAM1")
        self.verticalLayout_3.addWidget(self.CAM1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.startCAM1 = QtWidgets.QPushButton(self.tab)
        self.startCAM1.setObjectName("startCAM1")
        self.horizontalLayout_6.addWidget(self.startCAM1)
        self.carProtectionCAM1 = QtWidgets.QPushButton(self.tab)
        self.carProtectionCAM1.setObjectName("carProtectionCAM1")
        self.horizontalLayout_6.addWidget(self.carProtectionCAM1)
        self.monitorAreaCAM1 = QtWidgets.QPushButton(self.tab)
        self.monitorAreaCAM1.setObjectName("monitorAreaCAM1")
        self.horizontalLayout_6.addWidget(self.monitorAreaCAM1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.stopCAM1 = QtWidgets.QPushButton(self.tab)
        self.stopCAM1.setEnabled(False)
        self.stopCAM1.setObjectName("stopCAM1")
        self.horizontalLayout_7.addWidget(self.stopCAM1)
        self.personSearchingCAM1 = QtWidgets.QPushButton(self.tab)
        self.personSearchingCAM1.setObjectName("personSearchingCAM1")
        self.horizontalLayout_7.addWidget(self.personSearchingCAM1)
        self.illegalCAM1 = QtWidgets.QPushButton(self.tab)
        self.illegalCAM1.setObjectName("illegalCAM1")
        self.horizontalLayout_7.addWidget(self.illegalCAM1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")


 # View CAM 2
        self.CAM2 = QtWidgets.QLabel(self.tab)
        self.CAM2.setMinimumSize(QtCore.QSize(320, 240))
        self.CAM2.setMaximumSize(QtCore.QSize(426, 400))
        self.CAM2.setFrameShape(QtWidgets.QFrame.Box)
        self.CAM2.setObjectName("CAM2")
        self.verticalLayout.addWidget(self.CAM2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.startCAM2 = QtWidgets.QPushButton(self.tab)
        self.startCAM2.setObjectName("startCAM2")
        self.horizontalLayout_2.addWidget(self.startCAM2)
        self.carProtectionCAM2 = QtWidgets.QPushButton(self.tab)
        self.carProtectionCAM2.setObjectName("carProtectionCAM2")
        self.horizontalLayout_2.addWidget(self.carProtectionCAM2)
        self.monitorAreaCAM2 = QtWidgets.QPushButton(self.tab)
        self.monitorAreaCAM2.setObjectName("monitorAreaCAM2")
        self.horizontalLayout_2.addWidget(self.monitorAreaCAM2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.stopCAM2 = QtWidgets.QPushButton(self.tab)
        self.stopCAM2.setEnabled(False)
        self.stopCAM2.setObjectName("stopCAM2")
        self.horizontalLayout_3.addWidget(self.stopCAM2)
        self.personSearchingCAM2 = QtWidgets.QPushButton(self.tab)
        self.personSearchingCAM2.setObjectName("personSearchingCAM2")
        self.horizontalLayout_3.addWidget(self.personSearchingCAM2)
        self.illegalCAM2 = QtWidgets.QPushButton(self.tab)
        self.illegalCAM2.setObjectName("illegalCAM2")
        self.horizontalLayout_3.addWidget(self.illegalCAM2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")


 # View CAM 3
        self.CAM3 = QtWidgets.QLabel(self.tab)
        self.CAM3.setMinimumSize(QtCore.QSize(320, 240))
        self.CAM3.setMaximumSize(QtCore.QSize(426, 400))
        self.CAM3.setFrameShape(QtWidgets.QFrame.Box)
        self.CAM3.setObjectName("CAM3")
        self.verticalLayout_2.addWidget(self.CAM3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.startCAM3 = QtWidgets.QPushButton(self.tab)
        self.startCAM3.setObjectName("startCAM3")
        self.horizontalLayout_4.addWidget(self.startCAM3)
        self.carProtectionCAM3 = QtWidgets.QPushButton(self.tab)
        self.carProtectionCAM3.setObjectName("carProtectionCAM3")
        self.horizontalLayout_4.addWidget(self.carProtectionCAM3)
        self.monitorAreaCAM3 = QtWidgets.QPushButton(self.tab)
        self.monitorAreaCAM3.setObjectName("monitorAreaCAM3")
        self.horizontalLayout_4.addWidget(self.monitorAreaCAM3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.stopCAM3 = QtWidgets.QPushButton(self.tab)
        self.stopCAM3.setEnabled(False)
        self.stopCAM3.setObjectName("stopCAM3")
        self.horizontalLayout_5.addWidget(self.stopCAM3)
        self.personSearchingCAM3 = QtWidgets.QPushButton(self.tab)
        self.personSearchingCAM3.setObjectName("personSearchingCAM3")
        self.horizontalLayout_5.addWidget(self.personSearchingCAM3)
        self.illegalCAM3 = QtWidgets.QPushButton(self.tab)
        self.illegalCAM3.setObjectName("illegalCAM3")
        self.horizontalLayout_5.addWidget(self.illegalCAM3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 2, 1, 1)
        self.tabWidget.addTab(self.tab, "")


 # Media Tab
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videowidget = QVideoWidget()
        self.openBtn = QtWidgets.QPushButton('Open Video')
        self.playBtn = QtWidgets.QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))     
        self.stopBtn = QtWidgets.QPushButton()
        self.stopBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaStop)) 
        self.slowBtn = QtWidgets.QPushButton()
        self.slowBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward)) 
        self.fastBtn = QtWidgets.QPushButton()
        self.fastBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))      
        self.volumeBtn = QtWidgets.QPushButton()
        self.volumeBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))       
        self.fullscreenBtn = QPushButton("Full Screen")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)     
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0,100)
        self.volume_slider.setValue(100)
        self.label_2_1 = QLabel()
        self.label_2_1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.label_2_2 = QLabel()
        hboxLayout_2_1 = QHBoxLayout()
        hboxLayout_2_2 = QHBoxLayout()
        hboxLayout_2_3 = QHBoxLayout()
        hboxLayout_2_1.addWidget(self.slider) 
        hboxLayout_2_2.addWidget(self.openBtn)
        hboxLayout_2_2.addWidget(self.stopBtn)
        hboxLayout_2_2.addWidget(self.slowBtn)
        hboxLayout_2_2.addWidget(self.playBtn)
        hboxLayout_2_2.addWidget(self.fastBtn)
        hboxLayout_2_2.addWidget(self.volumeBtn)
        hboxLayout_2_2.addWidget(self.volume_slider)
        hboxLayout_2_2.addStretch(1)
        hboxLayout_2_2.addWidget(self.fullscreenBtn)      
        hboxLayout_2_3.addWidget(videowidget)
        vboxLayout_2_1 = QVBoxLayout()
        vboxLayout_2_1.addLayout(hboxLayout_2_3)
        vboxLayout_2_1.addLayout(hboxLayout_2_1)
        vboxLayout_2_1.addLayout(hboxLayout_2_2)
        vboxLayout_2_1.addWidget(self.label_2_1)
        self.tab_2.setLayout(vboxLayout_2_1)

 # Setting CAM 1
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_2.setHorizontalSpacing(20)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSpacing(10)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.CAM1_draw = QtWidgets.QLabel(self.tab_3)
        self.CAM1_draw.setMinimumSize(QtCore.QSize(320, 240))
        self.CAM1_draw.setMaximumSize(QtCore.QSize(426, 400))
        self.CAM1_draw.setFrameShape(QtWidgets.QFrame.Box)
        self.CAM1_draw.setObjectName("CAM1_draw")
        self.verticalLayout_5.addWidget(self.CAM1_draw)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.drawCAM1 = QtWidgets.QPushButton(self.tab_3)
        self.drawCAM1.setObjectName("drawCAM1")
        self.horizontalLayout_8.addWidget(self.drawCAM1)
        self.removeCAM1 = QtWidgets.QPushButton(self.tab_3)
        self.removeCAM1.setObjectName("removeCAM1")
        self.horizontalLayout_8.addWidget(self.removeCAM1)
        self.verticalLayout_5.addLayout(self.horizontalLayout_8)
        self.gridLayout_2.addLayout(self.verticalLayout_5, 0, 0, 1, 1)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSpacing(10)
        self.verticalLayout_6.setObjectName("verticalLayout_6")


 # Setting CAM 2
        self.CAM2_draw = QtWidgets.QLabel(self.tab_3)
        self.CAM2_draw.setMinimumSize(QtCore.QSize(320, 240))
        self.CAM2_draw.setMaximumSize(QtCore.QSize(426, 400))
        self.CAM2_draw.setFrameShape(QtWidgets.QFrame.Box)
        self.CAM2_draw.setObjectName("CAM2_draw")
        self.verticalLayout_6.addWidget(self.CAM2_draw)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.drawCAM2 = QtWidgets.QPushButton(self.tab_3)
        self.drawCAM2.setObjectName("drawCAM2")
        self.horizontalLayout_10.addWidget(self.drawCAM2)
        self.removeCAM2 = QtWidgets.QPushButton(self.tab_3)
        self.removeCAM2.setObjectName("removeCAM2")
        self.horizontalLayout_10.addWidget(self.removeCAM2)
        self.verticalLayout_6.addLayout(self.horizontalLayout_10)
        self.gridLayout_2.addLayout(self.verticalLayout_6, 0, 1, 1, 1)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setSpacing(10)
        self.verticalLayout_7.setObjectName("verticalLayout_7")


 # Setting CAM 3 
        self.CAM3_draw = QtWidgets.QLabel(self.tab_3)
        self.CAM3_draw.setMinimumSize(QtCore.QSize(320, 240))
        self.CAM3_draw.setMaximumSize(QtCore.QSize(426, 400))
        self.CAM3_draw.setFrameShape(QtWidgets.QFrame.Box)
        self.CAM3_draw.setObjectName("CAM3_draw")
        self.verticalLayout_7.addWidget(self.CAM3_draw)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.drawCAM3 = QtWidgets.QPushButton(self.tab_3)
        self.drawCAM3.setObjectName("drawCAM3")
        self.horizontalLayout_12.addWidget(self.drawCAM3)
        self.removeCAM3 = QtWidgets.QPushButton(self.tab_3)
        self.removeCAM3.setObjectName("removeCAM3")
        self.horizontalLayout_12.addWidget(self.removeCAM3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_12)
        self.gridLayout_2.addLayout(self.verticalLayout_7, 0, 2, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout_4.addWidget(self.tabWidget)


 # Setup Connect
    # Setup enable
        self.removeCAM1.setEnabled(False)
        self.removeCAM2.setEnabled(False)
        self.removeCAM3.setEnabled(False)
    # Setup choosing feature
        self.carProtectionCAM1.setVisible(self.feature['car1'])
        self.carProtectionCAM2.setVisible(self.feature['car2'])
        self.carProtectionCAM3.setVisible(self.feature['car3'])        

        self.illegalCAM1.setVisible(self.feature['illegal1'])
        self.illegalCAM2.setVisible(self.feature['illegal2'])
        self.illegalCAM3.setVisible(self.feature['illegal3'])

        self.monitorAreaCAM1.setVisible(self.feature['mpa1'])
        self.monitorAreaCAM1.toggle()
        self.monitorAreaCAM1.setCheckable(True)

        self.monitorAreaCAM2.setVisible(self.feature['mpa2'])
        self.monitorAreaCAM2.toggle()
        self.monitorAreaCAM2.setCheckable(True)

        self.monitorAreaCAM3.setVisible(self.feature['mpa3'])
        self.monitorAreaCAM3.toggle()
        self.monitorAreaCAM3.setCheckable(True)

        self.personSearchingCAM1.setVisible(self.feature['person1'])
        self.personSearchingCAM2.setVisible(self.feature['person2'])
        self.personSearchingCAM3.setVisible(self.feature['person3'])
    # setup media player
        self.mediaPlayer.setVideoOutput(videowidget)
        self.openBtn.clicked.connect(self.open_file)
        self.playBtn.clicked.connect(self.play_video)
        self.stopBtn.clicked.connect(self.stop_video)
        self.fastBtn.clicked.connect(self.fast)
        self.slowBtn.clicked.connect(self.slow)
        self.volumeBtn.clicked.connect(self.mute)
        self.fullscreenBtn.clicked.connect(self.fullscreen)
        self.volume_slider.sliderMoved.connect(self.set_volume)
        self.slider.sliderMoved.connect(self.set_position)
        
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    # setup image processing
        #  create a timer
        self.timer = QTimer()
        self.timer2 = QTimer()
        self.timer3 = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam1)
        self.startCAM1.clicked.connect(self.start_view1)
        self.stopCAM1.clicked.connect(self.stop_view1)

        self.timer2.timeout.connect(self.viewCam2)
        self.startCAM2.clicked.connect(self.start_view2)
        self.stopCAM2.clicked.connect(self.stop_view2)

        self.timer3.timeout.connect(self.viewCam3)
        self.startCAM3.clicked.connect(self.start_view3)
        self.stopCAM3.clicked.connect(self.stop_view3)

        self.CAM1_draw.mousePressEvent = self.mouseEventCAM1
        self.CAM2_draw.mousePressEvent = self.mouseEventCAM2
        self.CAM3_draw.mousePressEvent = self.mouseEventCAM3


        self.drawCAM1.clicked.connect(self.startDrawAreaCAM1)
        self.removeCAM1.clicked.connect(self.removeAreaCAM1)

        self.drawCAM2.clicked.connect(self.startDrawAreaCAM2)
        self.removeCAM2.clicked.connect(self.removeAreaCAM2)

        self.drawCAM3.clicked.connect(self.startDrawAreaCAM3)
        self.removeCAM3.clicked.connect(self.removeAreaCAM3)


        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)
 # All function
 # Function retranslateUI
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.CAM1.setText(_translate("Form", "IP CAM 1"))
        self.startCAM1.setText(_translate("Form", "Start"))
        self.carProtectionCAM1.setText(_translate("Form", "Car protection"))
        self.monitorAreaCAM1.setText(_translate("Form", "Monitor prohibited area"))
        self.stopCAM1.setText(_translate("Form", "Stop"))
        self.personSearchingCAM1.setText(_translate("Form", "Person searching"))
        self.illegalCAM1.setText(_translate("Form", "Illegal access action"))
        self.CAM2.setText(_translate("Form", "IP CAM 2"))
        self.startCAM2.setText(_translate("Form", "Start"))
        self.carProtectionCAM2.setText(_translate("Form", "Car protection"))
        self.monitorAreaCAM2.setText(_translate("Form", "Monitor prohibited area"))
        self.stopCAM2.setText(_translate("Form", "Stop"))
        self.personSearchingCAM2.setText(_translate("Form", "Person searching"))
        self.illegalCAM2.setText(_translate("Form", "Illegal access action"))
        self.CAM3.setText(_translate("Form", "IP CAM 3"))
        self.startCAM3.setText(_translate("Form", "Start"))
        self.carProtectionCAM3.setText(_translate("Form", "Car protection"))
        self.monitorAreaCAM3.setText(_translate("Form", "Monitor prohibited area"))
        self.stopCAM3.setText(_translate("Form", "Stop"))
        self.personSearchingCAM3.setText(_translate("Form", "Person searching"))
        self.illegalCAM3.setText(_translate("Form", "Illegal access action"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "3 IP CAMs"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "PLAY RECORD"))
        self.CAM1_draw.setText(_translate("Form", "TextLabel"))
        self.drawCAM1.setText(_translate("Form", "Draw"))
        self.removeCAM1.setText(_translate("Form", "Clear"))
        self.CAM2_draw.setText(_translate("Form", "TextLabel"))
        self.drawCAM2.setText(_translate("Form", "Draw"))
        self.removeCAM2.setText(_translate("Form", "Clear"))
        self.CAM3_draw.setText(_translate("Form", "TextLabel"))
        self.drawCAM3.setText(_translate("Form", "Draw"))
        self.removeCAM3.setText(_translate("Form", "Clear"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "SETTING"))
 # Function for media player
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
    def stop_video(self):
        self.mediaPlayer.stop()

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
            )
        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
            )

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)
        print(position)
    
    def set_volume(self, volume):
        self.mediaPlayer.setVolume(volume)
    
    def mute(self):
        if not self.mediaPlayer.isMuted():
            self.mediaPlayer.setMuted(True)
            self.volumeBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))
        else:
            self.mediaPlayer.setMuted(False)
            self.volumeBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))

    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())
        
        self.startCAM1.clicked.connect(self.start)
        self.stopCAM1.clicked.connect(self.stop)
        
    def fullscreen(self):
        if self.windowState() & Qt.WindowFullScreen:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.showNormal()
            print("no Fullscreen")
        else:
            Form.showFullScreen()
            QApplication.setOverrideCursor(Qt.BlankCursor)
            print("Fullscreen entered")

    def fast(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() + 10*60)

    def slow(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() - 10*60)

 # Function for image processing
    def image_to_QImage(self, image, label: QLabel):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (label.width(), label.height()))
        height , width, channel = image.shape
        step = channel * width
        return QImage(image.data, width, height, step, QImage.Format_RGB888)


    def start_view1(self):
      self.stopCAM1.setEnabled(True)
      self.startCAM1.setEnabled(False)
      global image_result
      if True:
        now = datetime.now()
        self.savePath1 = self.createDir('IP_CAM_1')
        self.startTime1 = str(now.day)+' - '+str(now.hour)+'h'+str(now.minute)+ ' - '
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.outVivdeo = cv2.VideoWriter(self.savePath1+'output.avi', fourcc, 30, (int(image_result[0].shape[1]), int(image_result[0].shape[0])))
        self.timer.start(20)
      else:
        self.startCAM1.setEnabled(True)
        self.stopCAM1.setEnabled(False)
        image = cv2.imread('no-connection.jpg')
        self.CAM1.setPixmap(QPixmap.fromImage(self.image_to_QImage(image, self.CAM1)))
    def viewCam1(self):
      global image_result
      # global center_point
      image = image_result[0].copy()
      self.outVivdeo.write(image)
      flag_warning=0
      if self.monitorAreaCAM1.isChecked():
          flag_warning = myLib.monitorProhibitedArea(points=self.points_CAM1, center_point=myLib.center_point, source_id=0)
      self.CAM1.setPixmap(QPixmap.fromImage(self.image_to_QImage(image, self.CAM1)))
      self.CAM1_draw.setPixmap(QPixmap.fromImage(self.image_to_QImage(self.drawArea(image, self.points_CAM1, self.CAM1_draw, flag_warning), self.CAM1_draw)))
    def stop_view1(self):
      self.startCAM1.setEnabled(True)
      self.stopCAM1.setEnabled(False)
      self.timer.stop()
      self.outVivdeo.release()
      image = cv2.imread('stopVideo.png')
      self.CAM1.setPixmap(QPixmap.fromImage(self.image_to_QImage(image, self.CAM1)))
      now = datetime.now()
      fileName = self.startTime1+str(now.hour)+'h'+str(now.minute)+'.avi'
      os.rename(self.savePath1+'output.avi', self.savePath1+fileName)

    def start_view2(self):
      self.stopCAM2.setEnabled(True)
      self.startCAM2.setEnabled(False)
      global image_result
      if True:
        self.check2 = False
        self.warning2 = None
        now = datetime.now()
        self.savePath2 = self.createDir('IP_CAM_2')
        self.startTime2 = str(now.day)+' - '+str(now.hour)+'h'+str(now.minute)+ ' - '
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.outVivdeo2 = cv2.VideoWriter(self.savePath2+'output2.avi', fourcc, 30,(int(image_result[1].shape[1]), int(image_result[1].shape[0])))
        self.timer2.start(20)

      else:
        self.startCAM2.setEnabled(True)
        self.stopCAM2.setEnabled(False)
        image = cv2.imread('no-connection.jpg')
        self.CAM2.setPixmap(QPixmap.fromImage(self.image_to_QImage(image, self.CAM2)))        
    def viewCam2(self):
      global image_result
      image = image_result[1].copy()
      self.outVivdeo2.write(image)
      flag_warning = 0
      if self.monitorAreaCAM2.isChecked():
          flag_warning = myLib.monitorProhibitedArea(points=self.points_CAM2, center_point=myLib.center_point, source_id=1)
          if flag_warning == None and self.check2 == False:
            pass
          elif flag_warning == 1 and self.check2 == False:
            print("warning 1")
            self.check2 = True
            self.warning2 = warningMethod(camera_idx=2)
            self.t2 = threading.Thread(target=self.warning2.run, args=())
            self.t2.start()
          elif self.check2 == True and flag_warning == None:
            print("terminate")
            self.warning2.terminate()
            self.t2.join()
            self.check2 = False
      else:
        if self.warning2 is not None:
          self.warning2.terminate()
          self.check2 = False


      self.CAM2.setPixmap(QPixmap.fromImage(self.image_to_QImage(image, self.CAM2)))
      self.CAM2_draw.setPixmap(QPixmap.fromImage(self.image_to_QImage(self.drawArea(image, self.points_CAM2, self.CAM2_draw, flag_warning), self.CAM2_draw)))    
    def stop_view2(self):
      self.startCAM2.setEnabled(True)
      self.stopCAM2.setEnabled(False)
      self.outVivdeo2.release()
      self.timer2.stop()
      image = cv2.imread('stopVideo.png')
      self.CAM2.setPixmap(QPixmap.fromImage(self.image_to_QImage(image, self.CAM2)))
      now = datetime.now()
      fileName = self.startTime2+str(now.hour)+'h'+str(now.minute)+'.avi'
      os.rename(self.savePath2+'output2.avi', self.savePath2+fileName)
      if self.warning2 is not None:
        self.warning2.terminate()
        self.check2 = False

    def start_view3(self):
        self.stopCAM3.setEnabled(True)
        self.startCAM3.setEnabled(False)
        global image_result
        if True:
            now = datetime.now()
            self.savePath3 = self.createDir('IP_CAM_3')
            self.startTime3 = str(now.day)+' - '+str(now.hour)+'h'+str(now.minute)+ ' - '
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.outVivdeo3 = cv2.VideoWriter(self.savePath3+'output3.avi', fourcc, 30, (int(image_result[2].shape[1]), int(image_result[2].shape[0])))
            self.timer3.start(20)
        else:
            self.startCAM3.setEnabled(True)
            self.stopCAM3.setEnabled(False)
            image = cv2.imread('no-connection.jpg')
            self.CAM3.setPixmap(QPixmap.fromImage(self.image_to_QImage(image, self.CAM3)))           
    def viewCam3(self):
      global image_result
      image = image_result[2].copy()
      self.outVivdeo3.write(image)
      flag_warning = 0
      if self.monitorAreaCAM3.isChecked():
          flag_warning = myLib.monitorProhibitedArea(points=self.points_CAM3, center_point=myLib.center_point, source_id=2)
      self.CAM3.setPixmap(QPixmap.fromImage(self.image_to_QImage(image, self.CAM3)))
      self.CAM3_draw.setPixmap(QPixmap.fromImage(self.image_to_QImage(self.drawArea(image, self.points_CAM3, self.CAM3_draw, flag_warning), self.CAM3_draw)))             
    def stop_view3(self):
        self.startCAM3.setEnabled(True)
        self.stopCAM3.setEnabled(False)    
        self.timer3.stop()
        self.outVivdeo3.release()
        image = cv2.imread('stopVideo.png')
        self.CAM3.setPixmap(QPixmap.fromImage(self.image_to_QImage(image, self.CAM3)))
        now = datetime.now()
        fileName = self.startTime3+str(now.hour)+'h'+str(now.minute)+'.avi'
        os.rename(self.savePath3+'output3.avi', self.savePath3+fileName) 
        
    def createDir(self, IP_CAM_Number: str):
        now = datetime.now()
        year = now.year
        month = MONTH[now.month]

        curPath = os.getcwd()
        if not path.exists(curPath+'/IVA'):
            os.mkdir(curPath+'/IVA')
        if not path.exists(curPath+'/IVA/'+IP_CAM_Number):
            os.mkdir(curPath+'/IVA/'+IP_CAM_Number)


        # check path exists
        if path.exists(curPath+'/IVA/'+IP_CAM_Number+'/'+str(year)):
            if path.exists(curPath+'/IVA/'+IP_CAM_Number+'/'+str(year)+'/'+month):
                return curPath+'/IVA/'+IP_CAM_Number+'/'+str(year)+'/'+month + '/'
            else:
                os.mkdir(curPath+'/IVA/'+IP_CAM_Number+'/'+str(year)+'/'+month)
                return curPath+'/IVA/'+IP_CAM_Number+'/'+str(year)+'/'+month+'/'
        else:
            os.mkdir(curPath+'/IVA/'+IP_CAM_Number+'/'+str(year))
            if path.exists(curPath+'/IVA/'+IP_CAM_Number+'/'+str(year)+'/'+month):
                return curPath+'/IVA/'+IP_CAM_Number+'/'+str(year)+'/'+month + '/'
            else:
                os.mkdir(curPath+'/IVA/'+IP_CAM_Number+'/'+str(year)+'/'+month)
                return curPath+'/IVA/'+IP_CAM_Number+'/'+str(year)+'/'+month+'/'


    # Create Mouse Event for draw protected area
    def mouseEventCAM1(self, event):
        if self.removeCAM1.isEnabled() and (not self.startCAM1.isEnabled()) == True:
            # print(self.CAM1_draw.width(), self.CAM1_draw.height())
            x = event.pos().x()
            y = event.pos().y()
            print(x, y)
            x = round((x/self.CAM1_draw.width()), 10)
            y = round((y/self.CAM1_draw.height()), 10)
            self.points_CAM1.append([x, y])
            print("Position clicked is ({}, {})".format(int(x*self.CAM1_draw.width()), int(y*self.CAM1_draw.height())))
            # print(self.points_CAM1)

    def mouseEventCAM2(self, event):
        if self.removeCAM2.isEnabled() and (not self.startCAM2.isEnabled()) == True:
            x = event.pos().x()
            y = event.pos().y()
            print(x, y)
            x = round((x/self.CAM1_draw.width()), 10)
            y = round((y/self.CAM1_draw.height()), 10)
            self.points_CAM2.append([x, y])
            print("Position clicked is ({}, {})".format(int(x*self.CAM2_draw.width()), int(y*self.CAM2_draw.height())))

    def mouseEventCAM3(self, event):
        if self.removeCAM3.isEnabled() and (not self.startCAM3.isEnabled()) == True:
            x = event.pos().x()
            y = event.pos().y()
            print(x, y)
            x = round((x/self.CAM1_draw.width()), 10)
            y = round((y/self.CAM1_draw.height()), 10)
            self.points_CAM3.append([x, y])
            print("Position clicked is ({}, {})".format(int(x*self.CAM3_draw.width()), int(y*self.CAM3_draw.height())))

    def startDrawAreaCAM1(self):
        self.drawCAM1.setEnabled(False)
        self.removeCAM1.setEnabled(True)

    def removeAreaCAM1(self):
        while len(self.points_CAM1):
            self.points_CAM1.pop()
        self.drawCAM1.setEnabled(True)
        self.removeCAM1.setEnabled(False)
    
    def startDrawAreaCAM2(self):
        self.drawCAM2.setEnabled(False)
        self.removeCAM2.setEnabled(True)
    
    def removeAreaCAM2(self):
        while len(self.points_CAM2):
            self.points_CAM2.pop()
        self.drawCAM2.setEnabled(True)
        self.removeCAM2.setEnabled(False)

    def startDrawAreaCAM3(self):
        self.drawCAM3.setEnabled(False)
        self.removeCAM3.setEnabled(True)

    def removeAreaCAM3(self):
        while len(self.points_CAM3):
            self.points_CAM3.pop()
        self.drawCAM3.setEnabled(True)
        self.removeCAM3.setEnabled(False)

    def drawArea(self, image, points: list, qlabel: QtWidgets.QLabel, flag_waring:int):
        image_draw = image.copy()
        (width, height) = image.shape[:2]
        image_draw = cv2.resize(image_draw, (qlabel.width(), qlabel.height()))


        if len(points) > 1:
            point1 = []
            for point in points:
                x = int(point[0] * qlabel.width())
                y = int(point[1] * qlabel.height())
                point1.append((x, y))
            cv2.polylines(image_draw, np.array([point1]), 1, (255, 0, 0), 1)
            b, g, r = cv2.split(image_draw)
            if flag_waring == 1:
                cv2.fillPoly(b, np.array([point1]), (0, 255, 0))
                cv2.fillPoly(g, np.array([point1]), (0, 255, 0))
            else:
                cv2.fillPoly(b, np.array([point1]), (0, 255, 0))
                cv2.fillPoly(r, np.array([point1]), (0, 255, 0))               
            image_draw = cv2.merge([b, g, r])
        return image_draw