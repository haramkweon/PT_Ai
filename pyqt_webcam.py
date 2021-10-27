import cv2
import threading
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

running = False
def run():
    global running
    cap = cv2.VideoCapture(0)
    width = cap.get(3)
    height = cap.get(4)
    label.resize(width, height)
    while running:
        ret, img = cap.read()
        if ret:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
            h,w,c = img.shape
            qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            label.setPixmap(pixmap)
        else:
            QtWidgets.QMessageBox.about(win, "Error", "Cannot read frame.")
            print("cannot read frame.")
            break

        if cv2.waitKey(1) == ord('q'):
            print("종료되었습니다")
            break
    cap.release()
    print("Thread end.")



app = QtWidgets.QApplication([])
win = QtWidgets.QWidget()
vbox = QtWidgets.QVBoxLayout()
label = QtWidgets.QLabel()

vbox.addWidget(label)

running = True
th = threading.Thread(target=run)
th.start()
print("started..")
win.setLayout(vbox)
win.show()

sys.exit(app.exec_())
