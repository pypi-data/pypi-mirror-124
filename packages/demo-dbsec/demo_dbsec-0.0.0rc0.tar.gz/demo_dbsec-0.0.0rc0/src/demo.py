from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
#import pandas as pd
from sqlite3 import Connection, OperationalError

class AccessDenied(Exception): ...
class BankingApp:
    def __init__(self,bank:str):
        self.__conn = Connection('./data/Banking.db')
        self.__cur = self.__conn.cursor()
    #Login accounts
    def login(self,user,password):
        #Make a string to mapping with password and user input
        LOGIN = """
        SELECT user
            ,checking
            ,savings
        FROM accounts
        WHERE "user" = '{user}' AND "password" = '{password}' LIMIT 1;"""
        try:
            self.__cur.execute(LOGIN.format(user=user,password=password))
            token = self.__cur.fetchone()
        except OperationalError:
            print('OperationalError: Something wrong happens! Try again.')
            raise AccessDenied('Unwanted Error')
        if token is None: raise AccessDenied('Username or Password is incorrect!')
        else: print('Successful to login!')
        return token
    
    def close(self):
        self.__conn.commit()
        self.__cur.close()
        self.__conn.close()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(487, 300)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.login = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.press_login())
        self.login.setGeometry(QtCore.QRect(170, 220, 75, 23))
        self.login.setMouseTracking(False)
        self.login.setCheckable(False)
        self.login.setChecked(False)
        self.login.setObjectName("login")
        self.register_2 = QtWidgets.QPushButton(self.centralwidget)
        self.register_2.setGeometry(QtCore.QRect(260, 220, 75, 23))
        self.register_2.setObjectName("register_2")
        self.user = QtWidgets.QLineEdit(self.centralwidget)
        self.user.setGeometry(QtCore.QRect(170, 140, 161, 20))
        self.user.setObjectName("user")
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(170, 170, 161, 20))
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(140, 140, 31, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(120, 170, 51, 21))
        self.label_2.setObjectName("label_2")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(170, 190, 91, 21))
        self.checkBox.setObjectName("checkBox")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(35, 20, 421, 101))
        self.textBrowser.setObjectName("textBrowser")
        self.show_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.show_checkbox.stateChanged.connect(self.check_show)
        self.show_checkbox.setGeometry(QtCore.QRect(340, 170, 111, 21))
        self.show_checkbox.setObjectName("show_checkbox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 487, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    #Function denied access message
    def show_deny(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Access Denied")
        msgBox.setText("Your username or password is invalid. Try again.")
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
        res = msgBox.exec_()
        
    def show_success(self,token):
        user,checking,savings = token
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Success to Log in")
        TEXT = f"""YOUR INFORMATION ACCOUNT
        USER : {user}
        CHECKING : {checking} $
        SAVINGS  : {savings} $
        """
        msgBox.setText(TEXT)
        res = msgBox.exec_()
    
    #Function show message UNKNOWN ERROR
    def show_MsgErr(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Unknown Error")
        msgBox.setText("Unknown error happened. Please contact the support team!")
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
        res = msgBox.exec_()
    
    #Press the button function
    def press_login(self):
        __user = self.user.text()
        __pwd = self.password.text()
        app = BankingApp('')
        try:
            token = app.login(__user,__pwd)
            self.show_success(token)
        except AccessDenied:
            self.show_deny()
            print('Error: Incorrect username or password')
    #Check show password
    def check_show(self,state):
        if state == QtCore.Qt.Checked:
            self.password.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.password.setEchoMode(QtWidgets.QLineEdit.Password)
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Internet Banking Application"))
        self.login.setText(_translate("MainWindow", "Log in"))
        self.register_2.setText(_translate("MainWindow", "Register"))
        self.label.setText(_translate("MainWindow", "User :"))
        self.label_2.setText(_translate("MainWindow", "Password:"))
        self.checkBox.setText(_translate("MainWindow", "Remember me"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\"./data/logo.svg\" width=\"410\" height=\"90\" /></p></body></html>"))
        self.show_checkbox.setText(_translate("MainWindow", "Show "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
