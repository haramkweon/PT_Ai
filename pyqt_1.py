from datetime import date
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QComboBox, QLineEdit, QMessageBox
from PyQt5.QtCore import QCoreApplication, Qt, QDate
import re

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.date = QDate.currentDate()
        self.initUI()

    def initUI(self):
        #======================label====================
        label1 = QLabel('NEXT LEVEL', self)
        label1.setAlignment(Qt.AlignCenter)

        font1 = label1.font()
        font1.setFamily('Times New Roman')
        font1.setPointSize(15)
        label1.setFont(font1)
        
        label2 = QLabel('운동목적', self)
        label2.setAlignment(Qt.AlignCenter)
        
        label3 = QLabel('이름', self)
        label3.setAlignment(Qt.AlignCenter)
        self.name = QLineEdit(self)
        
        label4 = QLabel('나이', self)
        label4.setAlignment(Qt.AlignCenter)
        self.age = QLineEdit(self)
        self.age.resize(40,10)
        
        label5 = QLabel('키', self)
        label5.setAlignment(Qt.AlignCenter)
        self.tall = QLineEdit(self)

        label7 = QLabel('cm', self)
        label7.setAlignment(Qt.AlignCenter)

        label6 = QLabel('몸무게', self)
        label6.setAlignment(Qt.AlignCenter)
        self.weight = QLineEdit(self)

        label8 = QLabel('kg', self)
        label8.setAlignment(Qt.AlignCenter)

        datetime =self.date.toString(Qt.DefaultLocaleLongDate)
        self.label9 = QLabel(datetime, self)
        self.label9.setAlignment(Qt.AlignCenter)
        #======================radio====================

        self.rbtn1 = QRadioButton('초급', self)
        self.rbtn2 = QRadioButton('중급', self)
        self.rbtn3 = QRadioButton('고급', self)

        #======================combo====================

        self.cb = QComboBox(self)
        self.cb.addItem('다이어트')
        self.cb.addItem('건강')
        self.cb.addItem('근력증진')
    
        #======================button====================

        start_btn = QPushButton('시작', self)
        start_btn.setCheckable(True)
        start_btn.toggle()

        quit_btn = QPushButton('종료', self)
        quit_btn.setCheckable(True)
        quit_btn.toggle()
        
        #=============================위치 조정=========================

        hbox = QHBoxLayout()
        radio_hbox = QHBoxLayout()
        goal_hbox = QHBoxLayout()
        name_hbox = QHBoxLayout()
        age_hbox = QHBoxLayout()
        data_hbox = QHBoxLayout()
       
        # 1. 시작, 종료 버튼 
        hbox.addStretch(1)
        hbox.addWidget(start_btn)
        hbox.addWidget(quit_btn)
        hbox.addStretch(1)
        # 2. 라디오 버튼 3개
        radio_hbox.addStretch(1)
        radio_hbox.addWidget(self.rbtn1)
        radio_hbox.addWidget(self.rbtn2)
        radio_hbox.addWidget(self.rbtn3)
        radio_hbox.addStretch(1)
        # 3. 운동 목적
        goal_hbox.addStretch(1)
        goal_hbox.addWidget(label2)
        goal_hbox.addWidget(self.cb)
        goal_hbox.addStretch(1)
        #4. 값 입력
        name_hbox.addStretch(1)
        name_hbox.addWidget(label3)
        name_hbox.addWidget(self.name)
        name_hbox.addStretch(1)

        age_hbox.addStretch(1)
        age_hbox.addWidget(label4)
        age_hbox.addWidget(self.age)
        age_hbox.addStretch(1)

        data_hbox.addStretch(1)
        data_hbox.addWidget(label5)
        data_hbox.addWidget(self.tall)
        data_hbox.addWidget(label7)
        data_hbox.addWidget(label6)
        data_hbox.addWidget(self.weight)
        data_hbox.addWidget(label8)
        data_hbox.addStretch(1)
        
        vbox = QVBoxLayout() 
        vbox.addStretch(1)
        vbox.addWidget(label1)
        vbox.addStretch(2)
        vbox.addLayout(name_hbox)
        vbox.addStretch(1)
        vbox.addLayout(age_hbox)
        vbox.addStretch(1)
        vbox.addLayout(data_hbox)
        vbox.addStretch(1)
        vbox.addLayout(goal_hbox)
        vbox.addStretch(1)
        vbox.addLayout(radio_hbox)
        vbox.addStretch(3)
        vbox.addLayout(hbox)
        vbox.addWidget(self.label9)
        start_btn.clicked.connect(self.button_event)
        quit_btn.clicked.connect(QCoreApplication.instance().quit)
              
        self.setLayout(vbox)
        self.setLayout(radio_hbox)
        self.setLayout(name_hbox)
        self.setLayout(age_hbox)
        self.setLayout(data_hbox)

        self.setWindowTitle('PROJECT')
        self.setGeometry(300, 300, 300, 400)
        self.show()

    def button_event(self):
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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
