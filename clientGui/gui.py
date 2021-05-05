import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox,
								QHBoxLayout, QVBoxLayout, QGroupBox, QTabWidget)
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, pyqtSlot
import sys
from queue import Queue
from client import ClientQObject
from company_widget import CompanyWidget

class Gui(QWidget):

	def __init__(self,queue_read: Queue,queue_sent: Queue):
		super().__init__()
		self.client = ClientQObject(queue_read,queue_sent)

		self.initUI()
		self.connetsInit()
		#self.loginWindow()
		self.mainWindow()

	# Logic part
	def initUI(self):
		self.setFixedSize(200,200)
		self.setWindowTitle('investor')
		self.show()
	
	def connetsInit(self):
		#self.connect(self, self.client.login_received, self.on_login_result_received )
		self.client.login_received.connect(self.on_login_result_received)

	def on_login_button_pressed(self):
		self.client.transfer_login_auth(self.qlineedit_connect_nickname.text(), self.qlineedit_connect_password.text())
		# Disable button until there will be responce from server
		self.qbutton_login.setEnabled(False)

	@pyqtSlot(bool)
	def on_login_result_received(self, res):
		if res:
			self.loginWindowDisable()
			self.mainWindow()
		else:
			self.qbutton_login.setEnabled(True)


	# UI description part

	# Open stock Exchange window
	def ose_tab_window(self):
		widget = QWidget()
		widget.layout = QVBoxLayout(widget)
		layout = widget.layout
		cp = CompanyWidget()
		layout.addWidget(cp)
		return widget

	def mainWindow(self):
		self.layout = QVBoxLayout(self)
		self.setFixedSize(640,480)
		# Initialize tab screen
		self.tabs = QTabWidget()
		self.tab1 = self.ose_tab_window()
		self.tab2 = QWidget()
		# Add tabs
		self.tabs.addTab(self.tab1,"Open Stock Exchange")
		self.tabs.addTab(self.tab2,"Market Place")

		self.layout.addWidget(self.tabs)

	def loginWindow(self):
		self.qlabel_connect_nickname = QLabel(parent=self)
		self.qlabel_connect_nickname.move(10, 10)
		self.qlabel_connect_nickname.setText("Login")
		self.qlabel_connect_nickname.show()

		self.qlineedit_connect_nickname = QLineEdit(self)
		self.qlineedit_connect_nickname.move(10, 30)
		self.qlineedit_connect_nickname.show()
		
		self.qlabel_connect_password = QLabel(parent=self)
		self.qlabel_connect_password.move(10, 70)
		self.qlabel_connect_password.setText("Password")
		self.qlabel_connect_password.show()

		self.qlineedit_connect_password = QLineEdit(self)
		self.qlineedit_connect_password.move(10, 90)
		self.qlineedit_connect_password.show()
		
		self.qbutton_login = QPushButton(parent=self,text="Login")
		self.qbutton_login.clicked.connect(self.on_login_button_pressed)
		self.qbutton_login.resize(self.qbutton_login.sizeHint())
		self.qbutton_login.move(30,130)
		self.qbutton_login.show()

		self.qlabel_connect_servermessage = QLabel(parent=self)
		self.qlabel_connect_servermessage.move(10, 150)
		self.qlabel_connect_servermessage.show()
	
	def loginWindowDisable(self):
		self.qlabel_connect_nickname.hide()
		self.qlabel_connect_nickname.hide()
		self.qlineedit_connect_nickname.hide()
		self.qlabel_connect_password.hide()
		self.qlineedit_connect_password.hide()
		self.qbutton_login.hide()
		self.qlabel_connect_servermessage.hide()


def gui_run(queue_receive : Queue, queue_sent : Queue):
	app = QApplication(sys.argv)
	gui = Gui(queue_receive,queue_sent)
	app.exec_()
	return gui
