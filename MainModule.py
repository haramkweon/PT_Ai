import sys
from MainWindow import MainWindow
from qt_webcam import CamWindow
from PyQt5.QtWidgets import *
if __name__ == '__main__':
    app = QApplication(sys.argv)
    Main = QMainWindow()
    win = MainWindow()
    cam = CamWindow()
    cam.setupUi(Main)
    cam.video_thread()
    win.show()
    Main.show()
    sys.exit(app.exec_())