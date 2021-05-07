import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtCore import pyqtSignal

from server.communication_protocol import CommunicationProtocol
from server.communication_protocol import MessageType
from server.companies.company_data import CompanyData

class CommandParser():

	def __init__(self):
		pass

	def companies_list_all(self,msg):
		# create list of companies and proceed to gui
		body = msg["body"]
		c_list = body["list"]
		cmp_list = []
		for i in range(body["amount"]):
			cur = c_list[i]
			c = CompanyData(cur["name"],cur["uuid"], float(cur["cost"]))
			cmp_list.append(c)
		# send it futher
		return cmp_list



	def parse(self, msg):
		switcher = {
			MessageType.COMPANIES_LIST_ALL.value : self.companies_list_all
		}
		func = switcher.get(int(msg["type"]), self.none_cmd_func)
		res = func(msg)
		return res

	def none_cmd_func(self, msg):
		print(" Wrong cmd", msg["type"])

