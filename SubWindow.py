from math import inf
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
class SubWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        image_box = QHBoxLayout()
        layout = QVBoxLayout()

        image_1 = QVBoxLayout()
        image_2 = QVBoxLayout()
        image_3 = QVBoxLayout()
        image_4 = QVBoxLayout()

        #=================================================================

        label1 = QLabel('Today health', self)
        label1.setAlignment(Qt.AlignCenter)

        font1 = label1.font()
        font1.setFamily('Times New Roman')
        font1.setPointSize(15)
        label1.setFont(font1)
        self.label1 = label1

        label2 = QLabel('FITNESS SET', self)
        label2.setAlignment(Qt.AlignCenter)

        #=================================================================

        label3 = QLabel(self)
        pixmap_1 = QPixmap("data/fitness_icon/slr.png")
        pixmap_1 = pixmap_1.scaledToWidth(130)
        label3.setPixmap(QPixmap(pixmap_1))
        self.label3 = label3
        image1_label = QLabel('  사이드레터럴레이즈  ', self)
        
        image_1.addWidget(label3)
        image_1.addWidget(image1_label)

        label4 = QLabel(self)
        pixmap_2 = QPixmap("data/fitness_icon/pushup.png")
        pixmap_2 = pixmap_2.scaledToWidth(130)
        label4.setPixmap(QPixmap(pixmap_2))
        self.label4 = label4
        image2_label = QLabel('             푸쉬업             ', self)

        image_2.addWidget(label4)
        image_2.addWidget(image2_label)


        label5 = QLabel(self)
        pixmap_3 = QPixmap("data/fitness_icon/curl.png")
        pixmap_3 = pixmap_3.scaledToWidth(130)
        label5.setPixmap(QPixmap(pixmap_3))
        self.label5 = label5
        image3_label = QLabel('              컬              ', self)

        image_3.addWidget(label5)
        image_3.addWidget(image3_label)

        label6 = QLabel(self)
        pixmap_4 = QPixmap("data/fitness_icon/squat.png")
        pixmap_4 = pixmap_4.scaledToWidth(130)
        label6.setPixmap(QPixmap(pixmap_4))
        self.label6 = label6
        image4_label = QLabel('            스쿼트             ', self)

        image_4.addWidget(label6)
        image_4.addWidget(image4_label)

    
        #=======================================================================

        layout.addWidget(label1)
        layout.addWidget(label2)
        image_box.addLayout(image_1)
        image_box.addLayout(image_2)
        image_box.addLayout(image_3)
        image_box.addLayout(image_4)

        image_box.setAlignment(Qt.AlignCenter)
        layout.addLayout(image_box) 
       

        self.setWindowTitle('Sub Window')
        self.setGeometry(700, 300, 1000, 500)
        self.setLayout(layout)



    