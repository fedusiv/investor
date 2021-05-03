# This class operates logic of clients requests and actions
# Reason is to separate operation module from client connection module
import tornado.websocket
from communication_parser import CommunitcationParserResult
from logic_handler import LogicHandler

class ClientOperation():

	def __init__(self, ws : tornado.websocket.WebSocketHandler, logic_handler : LogicHandler):
		self.ws = ws
		self.logic_handler = logic_handler


	def parse_command(self,cmd : CommunitcationParserResult):

		if result_msg.result_type == MessageType.COMPANIES_LIST_ALL:
			c_list = self.logic_handler.companies_all_list_client()
			c_list_msg = CommunicationProtocol.create_companies_all_list(c_list)
			self.write_message(c_list_msg)