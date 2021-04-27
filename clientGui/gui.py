import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox,
								QHBoxLayout, QVBoxLayout, QGroupBox)
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import sys
from queue import Queue
import asyncio
from server.message import Message


class Gui(QWidget):

	def __init__(self,queue: Queue):
		super().__init__()
		self.queue = queue
		self.queue_timer = QTimer(self)
		self.queue_timer.timeout.connect(self.queueChecker)
		# zaebalsya to play with asyncio, better to use gui functionality to operate with gui functionality
		self.queue_timer.setInterval(10)	# each 10ms call func to check queue messages from websocket
		self.queue_timer.start()

		self.initUI()
		self.connectWindow()

	def queueChecker(self):
		if self.queue.qsize() > 0:
			# get message from websocket and parse it
			string = self.queue.get()
			msg = Message(string)
			print(msg.type)


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
		
		self.qlabel_connect_address = QLabel(parent=self)
		self.qlabel_connect_address.move(100, 70)
		self.qlabel_connect_address.setText("Password")
		self.qlabel_connect_address.show()

		self.qlineedit_server_address = QLineEdit(self)
		self.qlineedit_server_address.move(100, 90)
		self.qlineedit_server_address.show()
		
		self.qbutton_login = QPushButton(parent=self,text="Login")
		self.qbutton_login.resize(self.qbutton_login.sizeHint())
		self.qbutton_login.move(130,130)
		self.qbutton_login.show()

		self.qlabel_connect_servermessage = QLabel(parent=self)
		self.qlabel_connect_servermessage.move(100, 180)
		self.qlabel_connect_servermessage.show()



def gui_run(queue : Queue):
	app = QApplication(sys.argv)
	gui = Gui(queue)
	app.exec_()
	return gui
