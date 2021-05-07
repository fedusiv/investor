from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QLineEdit, QMessageBox,
								QHBoxLayout, QVBoxLayout, QGroupBox, QTabWidget,
								QSizePolicy)
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class CompanyWidget(QWidget):

	def __init__(self, name : str, cost: float, cmp_id : int):
		super().__init__()
		self.id = cmp_id
		self.setFixedSize(570,60)	# Fixed size does not allow to resize this widget from scroll area
		self.group_box = QGroupBox(name, parent = self)
		self.group_box.resize(570,60)
		layout = QHBoxLayout()
		self.group_box.setLayout(layout)

		self.cost_label = QLabel(parent=self.group_box)
		self.cost_label.setText(str(cost))
		layout.addWidget(self.cost_label)
		self.buy_button = QPushButton(parent = self.group_box)
		self.buy_button.setText("Buy")
		self.buy_button.setFixedSize(80,28)
		self.buy_button.move(480,27)
		self.buy_button.clicked.connect(self.on_buy_button_clicked)

		self.sizePolicy().horizontalPolicy

	# Send the id of company widget
	company_buy_request = pyqtSignal(int)

	# Emit button pressed request
	def on_buy_button_clicked():
		self.company_buy_request.emit(self.id)



