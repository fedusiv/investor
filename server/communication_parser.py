from communication_protocol import CommunicationProtocol
from communication_protocol import MessageType
from enum import Enum


class CommunitcationParserReturnCode(Enum):
	ERROR = -1
	OK = 0

class CommunitcationParser():

	@staticmethod
	def login_request(msg):
		print(CommunitcationParser.login_request.__name__)
		return True

	@staticmethod
	def registration_request(msg):
		print(CommunitcationParser.registration_request.__name__)
		return True

	@staticmethod
	def parse_clinet_message(msg):
		# message should be json
		msg = CommunicationProtocol.verify_msg(msg)
		if msg is None:
			# end function is message is none
			return CommunitcationParserReturnCode.ERROR

		switcher = {
			MessageType.LOGIN.value : CommunitcationParser.login_request,
			MessageType.REGISTRATION.value : CommunitcationParser.registration_request
		}
		func = switcher.get(int(msg["type"]))
		func(msg)
		return CommunitcationParserReturnCode.OK
