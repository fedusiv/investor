from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QLineEdit, QMessageBox,
								QHBoxLayout, QVBoxLayout, QGroupBox, QTabWidget,
								QScrollArea)
from PyQt5.QtCore import Qt, QSize, QObject, QTimer, pyqtSignal, pyqtSlot

class PlayerDataWidget(QWidget):

	def __init__(self):
		super().__init__()

		self.setFixedSize(300,720)
		#layout = QVBoxLayout()
		#self.setLayout(layout)
		self.tab = QTabWidget(self)
		self.tab.setFixedSize(300,680)

		self.player_data = QWidget()
		layout = QVBoxLayout()
		self.player_data.setLayout(layout)

		self.login_label = QLabel()
		self.login_label.setText("Login")
		self.money_label = QLabel()
		self.money_label.setText("Money")

		self.player_data.layout().addWidget(self.login_label)
		self.player_data.layout().addWidget(self.money_label)

		self.tab.addTab(self.player_data, "PlayerData")
		
	def update_data(self, i_list):
		self.login_label.setText(i_list["login"])
		self.money_label.setText(str(i_list["money"]))


