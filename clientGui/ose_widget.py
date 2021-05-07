from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QLineEdit, QMessageBox,
								QHBoxLayout, QVBoxLayout, QGroupBox, QTabWidget)
from PyQt5.QtCore import QObject, QTimer, pyqtSignal, pyqtSlot

# Open stock Exchange widget
class OseWidget(QWidget):
	def __init__(self):
		super().__init__()

		# Init timer, which will request for companies information
		self.companies_request_timer = QTimer()
		# Run update each 5 seconds
		self.companies_request_timer.setInterval(5000)
		self.companies_request_timer.start()

