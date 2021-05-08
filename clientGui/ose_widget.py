from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QLineEdit, QMessageBox,
								QHBoxLayout, QVBoxLayout, QGroupBox, QTabWidget,
								QScrollArea)
from PyQt5.QtCore import Qt, QSize, QObject, QTimer, pyqtSignal, pyqtSlot

from company_widget import CompanyWidget
from server.companies.company_data import CompanyData

# Open stock Exchange widget
class OseWidget(QWidget):

	def __init__(self):
		super().__init__()

		# Init timer, which will request for companies information
		self.companies_request_timer = QTimer()
		# Run update each 5 seconds
		self.companies_request_timer.setInterval(5000)
		self.companies_request_timer.start()
		# Create layout for ose widget
		ose_layout = QHBoxLayout()
		self.setLayout(ose_layout)
		# Create area for companeis list
		self.scroll_widget = QWidget()	# Create container widget, which will be scrollable
		layout = QVBoxLayout()	# add layout to it
		self.scroll_widget.setLayout(layout)
		self.scroll_area = QScrollArea()	# Create scroll area
		#self.scroll_area.setFixedSize(640,600)
		self.scroll_area.setWidgetResizable(True)
		self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
		self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.scroll_area.setWidget(self.scroll_widget)
		ose_layout.addWidget(self.scroll_area)


	# Store companies widget objects
	company_storage = []

	# When need to update companies list. Nice description I understand
	# Method expects, that will receive c_list as list of CompanyData
	def update_companies_list(self,c_list):
		layout = self.scroll_widget.layout()
		# Remove previous
		if len(self.company_storage) > 0:
			for comp in self.company_storage:
				layout.removeWidget(comp)
			self.company_storage.clear()
		# Add new
		c_id = 0
		for company in c_list:
			cp = CompanyWidget(company.name, company.cost,c_id)
			layout.addWidget(cp)
			self.company_storage.append(cp)
			c_id += 1

