import os 
import time
import datetime
import sys
from PyQt5 import QtWidgets, QtGui, QtCore



class Main_window(QtWidgets.QMainWindow):


    # atribut k uložení proměnné z time-edit widgetu, který se předává do druhého okna
    saved_time = None


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # nastavení velikosti a nadpisu
        self.setWindowTitle("TurnOff Aplikace")
        self.setGeometry(500, 300, 404, 280)
        self.setFixedSize(404, 280)

        # vytvoření stacked widgetu
        self.Qtstack = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.Qtstack)

        # vytvoření dvou widgetů do stacked-widget
        self.stack1 = QtWidgets.QWidget()
        self.stack2 = QtWidgets.QWidget()

        # přidání widgetů do stacked-widget
        self.Qtstack.addWidget(self.stack1)
        self.Qtstack.addWidget(self.stack2)

        # nastavení layoutu pro 1. stack
        self.layout_stack1 = QtWidgets.QVBoxLayout()
        self.stack1.setLayout(self.layout_stack1)

        # nastavení layoutu pro 2. stack
        self.layout_stack2 = QtWidgets.QVBoxLayout()
        self.stack2.setLayout(self.layout_stack2)

        # spuštění obou oken
        self.show()
        self.front_window()
        self.back_window()
       

    def front_window(self):  
             
        # layout s textem
        self.text = QtWidgets.QWidget()
        self.layout_text = QtWidgets.QHBoxLayout()
        self.text.setLayout(self.layout_text)
        self.layout_stack1.addWidget(self.text)
        self.layout_stack1.addStretch()

        # Layout pro edit a checkboxy
        layout_edit = QtWidgets.QHBoxLayout()
        self.layout_stack1.addLayout(layout_edit)
        self.layout_stack1.addStretch()

        # Layout pro error hlášku
        layout_error = QtWidgets.QHBoxLayout()
        self.layout_stack1.addLayout(layout_error)

        # Layout pro pushbutton
        layout_button = QtWidgets.QHBoxLayout()
        self.layout_stack1.addLayout(layout_button)

        # widget s textem
        self.text = QtWidgets.QLabel("Zde nastav, za jak dlouhou dobu chceš automaticky vypnout pc. \nMůžeš i uvést, na který monitor chceš hned přepnout.\nMinimální doba je 15 minut. \n\nPoznámka:\nPřed vypnutím se pc automaticky přepne na první monitor.")
        self.text.setFont(QtGui.QFont('Arial', 10))    
        self.layout_text.addWidget(self.text)

        # Widget s time editem
        layout_edit.addStretch()
        self.time_edit = QtWidgets.QTimeEdit(self)
        self.time_edit.setFont(QtGui.QFont('Arial', 16))
        layout_edit.addWidget(self.time_edit)

        # ulozeni času z edit time do třídní proměnné
        self.saved_time = self.time_edit    

        # Widget s políčkami
        layout_edit.addStretch()
        self.checkbox1 = QtWidgets.QCheckBox("1. monitor", self)
        self.checkbox1.setFont(QtGui.QFont('Arial', 10))
        layout_edit.addWidget(self.checkbox1)
        layout_edit.addStretch()
        self.checkbox2 = QtWidgets.QCheckBox("2. monitor", self)
        self.checkbox2.setFont(QtGui.QFont('Arial', 10))
        layout_edit.addWidget(self.checkbox2)
        layout_edit.addStretch()

        #widget s error hlaškou
        self.error = QtWidgets.QLabel(self)
        self.error.setText("<font color='red'>minimální doba je 15 minut</font>")
        self.error.setFont(QtGui.QFont('Arial', 14))
        layout_error.addWidget(self.error)
        self.error.hide()

        # Widget s push buttonem
        self.Push_button_FW = QtWidgets.QPushButton("Enter", self)
        layout_button.addWidget(self.Push_button_FW)

        # logic push button
        self.Push_button_FW.clicked.connect(self.check_minimum_edit_time)

        # logic checkboxs
        self.checkbox1.clicked.connect(self.checkbox_1_clicked)
        self.checkbox2.clicked.connect(self.checkbox_2_clicked)

        

    def back_window(self):

        # layout s textem a odpočítávání času
        self.text_countdown = QtWidgets.QWidget()
        layout_text_countdown = QtWidgets.QHBoxLayout()
        self.text_countdown.setLayout(layout_text_countdown)
        self.layout_stack2.addWidget(self.text_countdown)

        # Layout pro pushbutton
        button_layout = QtWidgets.QHBoxLayout()
        self.layout_stack2.addLayout(button_layout)

        # widget s textem
        layout_text_countdown.addStretch()
        self.text = QtWidgets.QLabel("Automatické vypnutí pc za:")
        self.text.setFont(QtGui.QFont('Arial', 10))    
        layout_text_countdown.addWidget(self.text)
        layout_text_countdown.addStretch()

        # widget s odpočítáváním času
        self.countdown = QtWidgets.QLabel(self)
        self.countdown.setFont(QtGui.QFont('Arial', 16))
        layout_text_countdown.addWidget(self.countdown)
        layout_text_countdown.addStretch()

        # Widget s push buttonem
        self.Push_button_BW = QtWidgets.QPushButton("Stop", self)
        button_layout.addWidget(self.Push_button_BW)

        # logic push button 
        self.Push_button_BW.clicked.connect(self.change_windows)
        self.Push_button_BW.clicked.connect(self.stop_countdown)
        

    def check_minimum_edit_time(self):

        given_time = self.time_edit.time()

        if given_time >= QtCore.QTime(0, 15):

            self.change_windows()
            self.start_countdown()
            self.change_monitor()
        else:
            self.error.show()


    def change_windows(self):
        if self.Qtstack.currentIndex() == 0:
            self.Qtstack.setCurrentIndex(1)
        elif self.Qtstack.currentIndex() == 1:
            self.Qtstack.setCurrentIndex(0)


    def change_monitor(self):
        if self.checkbox1.isChecked():
            print("přepínám na 1. monitor")
        elif self.checkbox2.isChecked():
            print("přepínám na 2. monitor")



    # funkce hlídá, aby bylo vždy odškrtnuté pouze jenom jedno pole
    def checkbox_1_clicked(self):
        if self.checkbox1.isChecked():
            self.checkbox1.setChecked(True)
            self.checkbox2.setChecked(False)
        else:
            self.checkbox1.setChecked(False)


    # funkce hlídá, aby bylo vždy odškrtnuté pouze jenom jedno pole
    def checkbox_2_clicked(self):
        if self.checkbox2.isChecked():
            self.checkbox2.setChecked(True)
            self.checkbox1.setChecked(False)
        else:
            self.checkbox2.setChecked(False)

    # funkce spouští odpočet při kliknutí na tlačítko ENTER
    def start_countdown(self):

        # z času vytvoří řetězec
        string_time = self.saved_time.time().toString()

        # z řetězce vytáhne čas, ale jen v sekundách a uloží proměnnou, která se vkládá do funkce: timer_start()
        x = time.strptime(string_time.split(',')[0],'%H:%M:%S')
        self.seconds = (datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds())

        self.timer_start()


    def stop_countdown(self):
        self.my_qtimer.stop()

    # nastavení odpočtu
    def timer_start(self):       
        self.time_left_int = self.seconds

        self.my_qtimer = QtCore.QTimer(self)
        self.my_qtimer.timeout.connect(self.timer_timeout)
        self.my_qtimer.start(1000)

    # nastavení konce odpočtu
    def timer_timeout(self):
        if self.time_left_int > 0:

            self.time_left_int -= 1
            self.update_number()
        else:
            self.my_qtimer.stop()
            print("Konec odpočítávání - Vypínám PC !!")
            
    # každou vteřinu obnoví číslo, aby uživatel viděl odpočítávání
    def update_number(self):
        
        self.countdown.setText(str(datetime.timedelta(seconds=self.time_left_int)))



class App(QtWidgets.QApplication):

    def __init__(self):
        super().__init__(sys.argv)

    def build(self):
        self.main_window = Main_window()

        sys.exit(self.exec_())



root = App()
root.build()








# kód pro netestovací verzi

# vypnuti pc ---->   os.system("shutdown /s /t 1")

# prepnuti monitoru --> DisplaySwitch.exe /internal
#                       DisplaySwitch.exe /external
  

