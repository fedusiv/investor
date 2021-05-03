from communication_protocol import CommunicationProtocol
from communication_protocol import MessageType
from enum import Enum
from client_data import ClientData


class CommunitcationParserResult():

	result_type : MessageType

	def __init__ (self, result_type = MessageType.NONE, success = True):
		self.err = success
		self.result_type = result_type

	def init_client_data(self, msg):
		self.client_data = ClientData(msg["body"]["login"])


class CommunitcationParser():

	@staticmethod
	def keep_alive_respond(msg):
		result = CommunitcationParserResult(MessageType.KEEP_ALIVE)
		return result

	@staticmethod
	def login_request(msg):
		result = CommunitcationParserResult(MessageType.LOGIN)
		result.init_client_data(msg)
		print(result.client_data.name)
		return result

	@staticmethod
	def registration_request(msg):
		print(CommunitcationParser.registration_request.__name__)
		return True

	@staticmethod
	def companies_all_list_request(msg):
		result = CommunitcationParserResult(MessageType.COMPANIES_LIST_ALL)
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
			MessageType.KEEP_ALIVE.value : CommunitcationParser.keep_alive_respond
		}
		func = switcher.get(int(msg["type"]))
		result = func(msg)
		return result

