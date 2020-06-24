import os 
import time
import datetime
import sys
from PyQt5 import QtWidgets, QtGui, QtCore



class MainForm(QtWidgets.QMainWindow):

    # atribute to save variable from time-edit widget, which is passed to the second window.
    saved_time = None


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # settings of size and title
        self.setWindowTitle("TurnOff Aplikace")
        self.setGeometry(500, 300, 404, 280)
        self.setFixedSize(404, 280)

        # create stacked widget
        self.Qtstack = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.Qtstack)

        # create two widget to stacked-widget
        self.stack1 = QtWidgets.QWidget()
        self.stack2 = QtWidgets.QWidget()

        # add widget to stacked widget
        self.Qtstack.addWidget(self.stack1)
        self.Qtstack.addWidget(self.stack2)

        # setting of layout to first stack
        self.layout_stack1 = QtWidgets.QVBoxLayout()
        self.stack1.setLayout(self.layout_stack1)

        # setting of layout to second stack
        self.layout_stack2 = QtWidgets.QVBoxLayout()
        self.stack2.setLayout(self.layout_stack2)

        # launch both windows
        self.show()
        self.front_window()
        self.back_window()
       

    def front_window(self):  
             
        # layout with text
        self.text = QtWidgets.QWidget()
        self.layout_text = QtWidgets.QHBoxLayout()
        self.text.setLayout(self.layout_text)
        self.layout_stack1.addWidget(self.text)
        self.layout_stack1.addStretch()

        # Layout to edit a checkboxs
        layout_edit = QtWidgets.QHBoxLayout()
        self.layout_stack1.addLayout(layout_edit)
        self.layout_stack1.addStretch()

        # Layout to error issue
        layout_error = QtWidgets.QHBoxLayout()
        self.layout_stack1.addLayout(layout_error)

        # Layout to pushbutton
        layout_button = QtWidgets.QHBoxLayout()
        self.layout_stack1.addLayout(layout_button)

        # widget with text
        self.text = QtWidgets.QLabel("Here you set how long it takes you to turn off the PC\nautomatically. You can also specify which monitor you want\nto switch to immediately. The minimum time is 15 minutes. \n\nNote: \nBefore turning off, the PC will automatically switch to the\nfirst monitor.")
        self.text.setFont(QtGui.QFont('Arial', 10))    
        self.layout_text.addWidget(self.text)

        # Widget with time-edite
        layout_edit.addStretch()
        self.time_edit = QtWidgets.QTimeEdit(self)
        self.time_edit.setFont(QtGui.QFont('Arial', 16))
        layout_edit.addWidget(self.time_edit)

        # save time from edit-time to class variables
        self.saved_time = self.time_edit    

        # Widget s checkboxes
        layout_edit.addStretch()
        self.checkbox1 = QtWidgets.QCheckBox("1. monitor", self)
        self.checkbox1.setFont(QtGui.QFont('Arial', 10))
        layout_edit.addWidget(self.checkbox1)
        layout_edit.addStretch()
        self.checkbox2 = QtWidgets.QCheckBox("2. monitor", self)
        self.checkbox2.setFont(QtGui.QFont('Arial', 10))
        layout_edit.addWidget(self.checkbox2)
        layout_edit.addStretch()

        #widget s error issue
        self.error = QtWidgets.QLabel(self)
        self.error.setText("<font color='red'>minimum time is 15 minutes</font>")
        self.error.setFont(QtGui.QFont('Arial', 14))
        layout_error.addWidget(self.error)
        self.error.hide()

        # Widget with pushbutton
        self.Push_button_FW = QtWidgets.QPushButton("Enter", self)
        layout_button.addWidget(self.Push_button_FW)

        # logic with pushbutton
        self.Push_button_FW.clicked.connect(self.check_minimum_edit_time)

        # logic with checkboxs
        self.checkbox1.clicked.connect(self.checkbox_1_clicked)
        self.checkbox2.clicked.connect(self.checkbox_2_clicked)

        
    def back_window(self):

        # layout with text and countdown timer
        self.text_countdown = QtWidgets.QWidget()
        layout_text_countdown = QtWidgets.QHBoxLayout()
        self.text_countdown.setLayout(layout_text_countdown)
        self.layout_stack2.addWidget(self.text_countdown)

        # Layout with pushbutton
        button_layout = QtWidgets.QHBoxLayout()
        self.layout_stack2.addLayout(button_layout)

        # widget with text
        layout_text_countdown.addStretch()
        self.text = QtWidgets.QLabel("Automatic turning off the PC !!")
        self.text.setFont(QtGui.QFont('Arial', 10))    
        layout_text_countdown.addWidget(self.text)
        layout_text_countdown.addStretch()

        # widget with countdown timer
        self.countdown = QtWidgets.QLabel(self)
        self.countdown.setFont(QtGui.QFont('Arial', 16))
        layout_text_countdown.addWidget(self.countdown)
        layout_text_countdown.addStretch()

        # Widget with pushbutton
        self.Push_button_BW = QtWidgets.QPushButton("Stop", self)
        button_layout.addWidget(self.Push_button_BW)

        # logic with pushbutton 
        self.Push_button_BW.clicked.connect(self.change_windows)
        self.Push_button_BW.clicked.connect(self.stop_countdown)
        

    def check_minimum_edit_time(self):
        """
        The function monitors whether the user has entered a minimum value in the countdown time.
        """
        given_time = self.time_edit.time()

        if given_time >= QtCore.QTime(0, 15):

            self.change_windows()
            self.start_countdown()
            self.change_monitor()
        else:
            self.error.show()


    def change_windows(self):
        """
        The function changes windows in the application.
        """
        if self.Qtstack.currentIndex() == 0:
            self.Qtstack.setCurrentIndex(1)
        elif self.Qtstack.currentIndex() == 1:
            self.Qtstack.setCurrentIndex(0)


    def change_monitor(self):
        """
        The function changes the output from the PC to the monitor.
        """
        if self.checkbox1.isChecked():
            os.system("DisplaySwitch.exe / internal")
        elif self.checkbox2.isChecked():
            os.system("DisplaySwitch.exe / external")

    
    def checkbox_1_clicked(self):
        """
        The function ensures that only one checkbox is unchecked at a time.
        """
        if self.checkbox1.isChecked():
            self.checkbox1.setChecked(True)
            self.checkbox2.setChecked(False)
        else:
            self.checkbox1.setChecked(False)


    def checkbox_2_clicked(self):
        """
        The function ensures that only one checkbox is unchecked at a time.
        """
        if self.checkbox2.isChecked():
            self.checkbox2.setChecked(True)
            self.checkbox1.setChecked(False)
        else:
            self.checkbox2.setChecked(False)
    

    def start_countdown(self):
        """
        The function starts the countdown when the ENTER button is clicked.
        """
        # create string from time
        string_time = self.saved_time.time().toString()


        # string pulls the time, but only in seconds, and stores a variable that is inserted into the function: timer_start ()
        x = time.strptime(string_time.split(',')[0],'%H:%M:%S')
        self.seconds = (datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds())

        self.timer_start()

    def stop_countdown(self):
        """
        The function cancels the time countdown.
        """

        self.my_qtimer.stop()


    def timer_start(self):
        """
        The function sets the countdown.
        """

        self.time_left_int = self.seconds

        self.my_qtimer = QtCore.QTimer(self)
        self.my_qtimer.timeout.connect(self.timer_timeout)
        self.my_qtimer.start(1000)

 
    def timer_timeout(self):
        """
        The function sets the end of the countdown.
        """

        if self.time_left_int > 0:

            self.time_left_int -= 1
            self.update_number()
        else:
            self.my_qtimer.stop()
            os.system("shutdown / s / t 1")
            

    def update_number(self):
        """
        The function resets the number every second so that the user can see the countdown.
        """

        self.countdown.setText(str(datetime.timedelta(seconds=self.time_left_int)))



class App(QtWidgets.QApplication):

    def __init__(self):
        super().__init__(sys.argv)

    def build(self):
        self.main_window = MainForm()
        sys.exit(self.exec_())



root = App()
root.build()
