from communication_protocol import CommunicationProtocol
from communication_protocol import MessageType
from enum import Enum
from client_data import ClientData


class CommunitcationParserResult():

	result_type : MessageType

	def __init__ (self, result_type = MessageType.NONE, success = True, uuid = ""):
		self.err = success
		self.result_type = result_type
		self.uuid = uuid

	# For initialization client data
	# On login request it should store credentials, for futher parsing and validating
	def init_client_data(self, msg):
		self.client_data = ClientData(msg["body"]["login"],msg["body"]["password"])

	# To buy requested stock
	def form_stock_buy_request(self,msg):
		body = msg["body"]
		self.company_uuid = body["uuid"]	# what company want to buy
		self.stock_amount = body["amount"]	# amount of stocks want to buy
		self.stock_cost = 	body["cost"]	# what price of one stock was


class CommunitcationParser():

	@staticmethod
	def keep_alive_respond(msg):
		result = CommunitcationParserResult(MessageType.KEEP_ALIVE)
		return result

	@staticmethod
	def login_request(msg):
		result = CommunitcationParserResult(MessageType.LOGIN)
		result.init_client_data(msg)
		return result

	@staticmethod
	def registration_request(msg):
		print(CommunitcationParser.registration_request.__name__)
		return True

	@staticmethod
	def companies_all_list_request(msg):
		result = CommunitcationParserResult(MessageType.COMPANIES_LIST_ALL, uuid=msg["uuid"])
		return result

	@staticmethod
	def client_data_request(msg):
		result = CommunitcationParserResult(MessageType.CLIENT_DATA, uuid=msg["uuid"])
		return result

	@staticmethod
	def stock_buy_request(msg):
		result = CommunitcationParserResult(MessageType.CLIENT_DATA, uuid=msg["uuid"])
		result.form_stock_buy_request(msg)
		return result

	@staticmethod
	def parse_clinet_message(msg):
		# message should be json
		msg = CommunicationProtocol.verify_msg(msg)
		if msg is None:
			# end function is message is none
			return CommunitcationParserResult(False)

		switcher = {
			MessageType.LOGIN.value : CommunitcationParser.login_request,
			MessageType.REGISTRATION.value : CommunitcationParser.registration_request,
			MessageType.KEEP_ALIVE.value : CommunitcationParser.keep_alive_respond,
			MessageType.COMPANIES_LIST_ALL.value : CommunitcationParser.companies_all_list_request,
			MessageType.CLIENT_DATA.value : CommunitcationParser.client_data_request
		}
		func = switcher.get(int(msg["type"]))
		result = func(msg)
		return result

