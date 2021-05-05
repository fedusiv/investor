from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QLineEdit, QMessageBox,
								QHBoxLayout, QVBoxLayout, QGroupBox, QTabWidget)

class CompanyWidget(QWidget):
	def __init__(self):
		super().__init__()
		self.resize(580,60)
		self.group_box = QGroupBox("No name", parent = self)
		self.group_box.resize(580,60)

		self.cost_label = QLabel(parent=self.group_box)
		self.cost_label.text = "10.3"
		#self.group_box.addWidget(self.cost_label)
		self.buy_button = QPushButton(parent = self.group_box)
		self.buy_button.setFixedSize(80,28)
		self.buy_button.move(490,27)
		pass

