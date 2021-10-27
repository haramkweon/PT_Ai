import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2


class SubWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        
        layout = QVBoxLayout()

        label1 = QLabel('Today health', self)
        label1.setAlignment(Qt.AlignCenter)

        label2 = QLabel('rout', self)
        label2.setAlignment(Qt.AlignCenter)
   
        layout.addWidget(label1)
        layout.addWidget(label2)

        self.setWindowTitle('Sub Window')
        self.setGeometry(300, 300, 300, 400)
        self.setLayout(layout)


    def showModal(self):   
        return super().exec_()
