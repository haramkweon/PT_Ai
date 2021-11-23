import sys
from MainWindow import MainWindow
from PyQt5.QtWidgets import *
import threading


def main():
    app = QApplication(sys.argv)
    #Main = QMainWindow()
    win = MainWindow()
    
    win.show()
    #Main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    t = threading.Thread(target=main)
    t.start()