import sys
from MainWindow import MainWindow
from PyQt5.QtWidgets import *
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())