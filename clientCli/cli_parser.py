import os, sys
from queue import Queue

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import (QApplication, QWidget, QLineEdit, QMessageBox,
								QHBoxLayout, QVBoxLayout, QTextBrowser)
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, pyqtSlot
from PyQt5.Qt import Qt

from cli_protocol import CliProtocol

class Gui(QWidget):

	def __init__(self,queue_read: Queue,queue_sent: Queue):
		super().__init__()
		self.initUI()

		self.queue_read = queue_read
		self.queue_sent = queue_sent
		
		# queue_read Timer initialization
		self.queue_timer = QTimer(self)
		self.queue_timer.timeout.connect(self.queue_reader)
		# Better to use gui/qt for timer functionality to operate with qt inside qt
		self.queue_timer.setInterval(10)	# each 10ms call func to check queue messages from websocket
		self.queue_timer.start()

		self.cli_protocol = CliProtocol()


	
	# Check reading queue
	def queue_reader(self):
		if self.queue_read.qsize() > 0:
			# get message from websocket and parse it
			msg = self.queue_read.get()
			self.print_cmd_tb("> "+ msg)
	
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Return :
			self.enter_pressed()

	def enter_pressed(self):
		cmd = self.input_line.text()
		if cmd != "":
			self.print_cmd_tb(cmd)
			self.input_line.setText("")
			self.parse_cmd(cmd)
			self.store_cmd(cmd)
		pass

	def initUI(self):
		self.resize(640,480)
		self.setWindowTitle('investor cli')
		self.setAutoFillBackground(True)
		self.setStyleSheet("background-color:#000000") 
		layout = QVBoxLayout()
		self.tb = QTextBrowser()
		self.tb.setStyleSheet("background-color:#1c223d; color:#1d850d")
		self.input_line = QLineEdit()
		self.input_line.setStyleSheet("background-color:#1c223d; color:#1d850d")
		layout.addWidget(self.tb)

		layout.addWidget(self.input_line)
		self.setLayout(layout)
		self.show()
		self.input_line.setFocus()

	# Print cmd to text browser
	def print_cmd_tb(self,cmd : str):
		self.tb.insertPlainText("$ " + cmd + "\n")
	
	def store_cmd(self,cmd: str):
		pass


	##########################
	# Parser
	##########################
	def parse_cmd(self,cmd : str):
		cmd_list = cmd.split(' ')
		switcher = {
			"login" : self.cmd_login,
			"exit" : self.cmd_exit
		}
		func = switcher.get(cmd_list[0],self.wrong_cmd)
		func(cmd_list)

	def wrong_cmd(self, cmd_list):
		self.print_cmd_tb("There is no command " + cmd_list[0])

	def cmd_login(self, cmd_list):
		msg_json = self.cli_protocol.create_login_msg(cmd_list[1],cmd_list[2])
		self.queue_sent.put(msg_json)


	def cmd_exit(self, cmd_list):
		sys.exit(0)

def gui_run(queue_receive : Queue, queue_sent : Queue):
	app = QApplication(sys.argv)
	gui = Gui(queue_receive,queue_sent)
	app.exec_()
	return gui
