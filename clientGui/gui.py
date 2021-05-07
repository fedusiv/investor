import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox,
								QHBoxLayout, QVBoxLayout, QGroupBox, QTabWidget)
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, pyqtSlot

from queue import Queue
from client import ClientQObject
from company_widget import CompanyWidget
from ose_widget import OseWidget

class Gui(QWidget):

	def __init__(self,queue_read: Queue,queue_sent: Queue):
		super().__init__()
		self.client = ClientQObject(queue_read,queue_sent)

		self.initUI()
		self.connetsInit()
		self.loginWindow()

	# Logic part
	def initUI(self):
		self.setFixedSize(200,200)
		self.setWindowTitle('investor')
		self.show()
	
	def connetsInit(self):
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

	# Gui want to update companies list
	def on_companies_list_request(self):
		self.client.send_companies_list_request()

	# When on open stock Exchange user request to buy company
	@pyqtSlot(int)
	def on_buy_company_request(self, cmp_id):
		print("Request to buy company : ", cmp_id)


	# UI description part

	def mainWindow(self):
		self.layout = QVBoxLayout(self)
		self.setFixedSize(640,480)
		# Initialize tab screen
		self.tabs = QTabWidget()
		self.tab_ose = OseWidget()
		self.tab2 = QWidget()
		# Add tabs
		self.tabs.addTab(self.tab_ose,"Open Stock Exchange")
		self.tabs.addTab(self.tab2,"Market Place")

		self.layout.addWidget(self.tabs)

		# Open stock Exchage calls to update list of companies
		self.tab_ose.companies_request_timer.timeout.connect(self.on_companies_list_request)

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
