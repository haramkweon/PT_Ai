from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap, QImage
#open cv에서는 영상을 프레임단위로 가져오기 때문에 sleep을 통해서 프레임을 연결시켜주어 영상으로 보이게 만드는 것임
#비디오 재생을 위해 스레드 생성
import threading
#화면을 윈도우에 띄우기 위해 sys접근
import sys

#open cv 라이브러리
import cv2


class Ui_MainWindow(object):
    #기본적으로 창만드는 작업
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("ForSign")
        MainWindow.resize(500, 300) #창 사이즈
        MainWindow.move(500,500) #창 뜰 때 위치
        #이 아래로는 나도 잘 모름 화면을 구성하고 영상을 재생하는 위젯을 만드는거 같음 유지해두는게 나을듯
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.video_viewer_label = QtWidgets.QLabel(self.centralwidget)
        self.video_viewer_label.setGeometry(QtCore.QRect(10, 10, 400, 300))

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def run_cv(self, MainWindow):
        cap = cv2.VideoCapture(0)
        while True:
            self.ret, self.frame = cap.read() #영상의 정보 저장
            if self.ret:
                self.rgbImage = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB) #프레임에 색입히기
                self.convertToQtFormat = QImage(self.rgbImage.data, self.rgbImage.shape[1], self.rgbImage.shape[0],
                                                QImage.Format_RGB888)

                self.pixmap = QPixmap(self.convertToQtFormat)
                self.p = self.pixmap.scaled(400, 300, QtCore.Qt.IgnoreAspectRatio) #프레임 크기 조정

                self.video_viewer_label.setPixmap(self.p)
                self.video_viewer_label.update() #프레임 띄우기

            else:
                break

        cap.release()
        cv2.destroyAllWindows()

    # 창 이름 설정
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("ForSign", "ForSign"))

    # video_to_frame을 쓰레드로 사용
    #이게 영상 재생 쓰레드 돌리는거 얘를 조작하거나 함수를 생성해서 연속재생 관리해야할듯
    def video_thread(self, MainWindow):
        thread = threading.Thread(target=self.run_cv, args=(self,))
        thread.daemon = True  # 프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
        thread.start()

#메인문
if __name__ == "__main__":
    import sys

    #화면 만들려면 기본으로 있어야 하는 코드들 건들지않기
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    #영상 스레드 시작
    ui.video_thread(MainWindow)

    #창 띄우기
    MainWindow.show()

    sys.exit(app.exec_())