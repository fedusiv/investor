import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox,
								QHBoxLayout, QVBoxLayout, QGroupBox)
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import sys
from queue import Queue
from client import ClientQObject

class Gui(QWidget):

	def __init__(self,queue: Queue):
		super().__init__()
		self.client = ClientQObject(queue)

		self.initUI()
		self.connectWindow()


	# UI part
	def initUI(self):
		self.setFixedSize(400,400)
		self.setWindowTitle('investor')
		self.show()
	
	def connectWindow(self):
		self.qlabel_connect_nickname = QLabel(parent=self)
		self.qlabel_connect_nickname.move(100, 10)
		self.qlabel_connect_nickname.setText("Login")
		self.qlabel_connect_nickname.show()

		self.qlineedit_connect_nickname = QLineEdit(self)
		self.qlineedit_connect_nickname.move(100, 30)
		self.qlineedit_connect_nickname.show()
		
		self.qlabel_connect_password = QLabel(parent=self)
		self.qlabel_connect_password.move(100, 70)
		self.qlabel_connect_password.setText("Password")
		self.qlabel_connect_password.show()

		self.qlineedit_connect_password = QLineEdit(self)
		self.qlineedit_connect_password.move(100, 90)
		self.qlineedit_connect_password.show()
		
		self.qbutton_login = QPushButton(parent=self,text="Login")
		self.qbutton_login.clicked.connect(self.on_login_button_pressed)
		self.qbutton_login.resize(self.qbutton_login.sizeHint())
		self.qbutton_login.move(130,130)
		self.qbutton_login.show()

		self.qlabel_connect_servermessage = QLabel(parent=self)
		self.qlabel_connect_servermessage.move(100, 180)
		self.qlabel_connect_servermessage.show()

	def on_login_button_pressed(self):
		self.client.transfer_login_auth(self.qlineedit_connect_nickname.text(), self.qlineedit_connect_password.text())


def gui_run(queue : Queue):
	app = QApplication(sys.argv)
	gui = Gui(queue)
	app.exec_()
	return gui
