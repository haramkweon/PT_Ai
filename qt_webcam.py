import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import threading

class CamWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(500, 300) #창 사이즈
        MainWindow.move(500,500) #창 뜰 때 위치
        #이 아래로는 나도 잘 모름 화면을 구성하고 영상을 재생하는 위젯을 만드는거 같음 유지해두는게 나을듯
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.video_viewer_label = QLabel(self.centralwidget)
        self.video_viewer_label.setGeometry(QRect(10, 10, 400, 300))

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

       
        QMetaObject.connectSlotsByName(MainWindow)
    
    def run_cv(self):
        cap = cv2.VideoCapture(0)
        while True:
            self.ret, self.frame = cap.read() #영상의 정보 저장
            if self.ret:
                self.rgbImage = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB) #프레임에 색입히기
                self.convertToQtFormat = QImage(self.rgbImage.data, self.rgbImage.shape[1], self.rgbImage.shape[0],
                                                QImage.Format_RGB888)

                self.pixmap = QPixmap(self.convertToQtFormat)
                self.p = self.pixmap.scaled(400, 300, Qt.IgnoreAspectRatio) #프레임 크기 조정

                self.video_viewer_label.setPixmap(self.p)
                self.video_viewer_label.update() #프레임 띄우기

            else:
                break

        cap.release()
        cv2.destroyAllWindows()

    def video_thread(self):
        thread = threading.Thread(target=self.run_cv)
        thread.daemon = True  # 프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
        thread.start()


    
    