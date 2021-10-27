import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from SubWindow import SubWindow
import re

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.date = QDate.currentDate()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Main Window')
        self.setGeometry(300, 300, 300, 400)
        layout = QVBoxLayout()
        name_hbox = QHBoxLayout()
        goal_hbox = QHBoxLayout()
        age_hbox = QHBoxLayout()
        radio_hbox = QHBoxLayout()
        data_hbox = QHBoxLayout()
        button_hbox = QHBoxLayout()
        layout.addStretch(1)

        #===============================================
        label1 = QLabel('NEXT LEVEL', self)
        label1.setAlignment(Qt.AlignCenter)

        font1 = label1.font()
        font1.setFamily('Times New Roman')
        font1.setPointSize(15)
        label1.setFont(font1)
        self.label1 = label1

        layout.addStretch(1)
        label2 = QLabel('운동목적', self)
        label2.setAlignment(Qt.AlignCenter)
        self.label2 = label2
        goal = QComboBox(self)
        goal.addItem('다이어트')
        goal.addItem('건강')
        goal.addItem('근력증진')
        self.cb = goal

        layout.addStretch(1)
        label3 = QLabel('이름', self)
        label3.setAlignment(Qt.AlignCenter)
        self.label3 = label3
        name = QLineEdit(self)
        self.name = name

        label4 = QLabel('나이', self)
        label4.setAlignment(Qt.AlignCenter)
        self.label4 = label4
        age = QLineEdit(self)
        self.age = age

        label5 = QLabel('키', self)
        label5.setAlignment(Qt.AlignCenter)
        self.label5 = label5
        tall = QLineEdit(self)
        self.tall = tall

        label6 = QLabel('몸무게', self)
        label6.setAlignment(Qt.AlignCenter)
        self.label6 = label6

        weight = QLineEdit(self)
        self.weight = weight

        label7 = QLabel('cm', self)
        label7.setAlignment(Qt.AlignCenter)
        self.label7 = label7

        label8 = QLabel('kg', self)
        label8.setAlignment(Qt.AlignCenter)
        self.label8 = label8
        datetime =self.date.toString(Qt.DefaultLocaleLongDate)
        label9 = QLabel(datetime, self)
        label9.setAlignment(Qt.AlignCenter)
        self.label9 = label9
        
        rbtn1 = QRadioButton('초급', self)
        self.rbtn1 = rbtn1
        rbtn2 = QRadioButton('중급', self)
        self.rbtn2 = rbtn2
        rbtn3 = QRadioButton('고급', self)
        self.rbtn3 = rbtn3

        start_btn = QPushButton('시작', self)
        start_btn.clicked.connect(self.onButtonClicked)
        start_btn.setCheckable(True)
        start_btn.toggle()
        self.start_btn = start_btn

        quit_btn = QPushButton('종료', self)
        quit_btn.clicked.connect(QCoreApplication.instance().quit)
        quit_btn.setCheckable(True)
        quit_btn.toggle()
        self.quit_btn = quit_btn
        #===========================================
        name_hbox.addStretch(1)
        name_hbox.addWidget(label3)
        name_hbox.addWidget(name)
        name_hbox.addStretch(1)

        age_hbox.addStretch(1)
        age_hbox.addWidget(label4)
        age_hbox.addWidget(age)
        age_hbox.addStretch(1)

        goal_hbox.addStretch(1)
        goal_hbox.addWidget(label2)
        goal_hbox.addWidget(goal)
        goal_hbox.addStretch(1)

        data_hbox.addStretch(1)
        data_hbox.addWidget(label5)
        data_hbox.addWidget(tall)
        data_hbox.addWidget(label7)
        data_hbox.addWidget(label6)
        data_hbox.addWidget(weight)
        data_hbox.addWidget(label8)
        data_hbox.addStretch(1)

        radio_hbox.addStretch(1)
        radio_hbox.addWidget(rbtn1)
        radio_hbox.addWidget(rbtn2)
        radio_hbox.addWidget(rbtn3)
        radio_hbox.addStretch(1)

        button_hbox.addStretch(1)
        button_hbox.addWidget(start_btn)
        button_hbox.addWidget(quit_btn)
        button_hbox.addStretch(1)
        
        layout.addWidget(label1)
        layout.addStretch(2)
        layout.addLayout(name_hbox)
        layout.addStretch(1)
        layout.addLayout(age_hbox)
        layout.addStretch(1)
        layout.addLayout(data_hbox)
        layout.addStretch(1)
        layout.addLayout(goal_hbox)
        layout.addStretch(1)
        layout.addLayout(radio_hbox)
        layout.addStretch(1)
        layout.addLayout(button_hbox)
        layout.addStretch(1)

        layout.addWidget(label9)


        #===============================================
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def onButtonClicked(self):
        name_text = self.name.text()
        age_text = self.age.text() 
        tall_text = self.tall.text() 
        weight_text = self.weight.text() 
        
        text=re.compile('[가-힣]').findall(name_text)

        goal = self.cb.currentText()
        print(goal)
    
        if self.rbtn1.isChecked():
            print("초급")
        elif self.rbtn2.isChecked():
            print("중급")
        elif self.rbtn3.isChecked():
            print("고급")
        else:
            QMessageBox.question(self, 'Message', '입력한 값을 확인해주세요',
                                    QMessageBox.Yes)

        if len(name_text) > 5 or len(name_text) < 1 or int(age_text) > 150 or len(age_text) < 1 or int(tall_text) > 200 or len(tall_text) < 1 or int(weight_text) > 200 or len(weight_text) < 1:
            QMessageBox.question(self, 'Message', '입력한 값을 확인해주세요',
                                    QMessageBox.Yes)
        elif len(text) == 0:
            QMessageBox.question(self, 'Message', '입력한 값을 확인해주세요',
                                    QMessageBox.Yes)
        else:
            print(name_text, age_text, tall_text, weight_text)
        

            win = SubWindow()
            r = win.showModal()
            
    def show(self):
        super().show()