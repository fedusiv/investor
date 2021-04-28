import json
from enum import Enum

class MessageType(Enum):
	LOGIN = 1


# Class to parse and create required messages
class CommunicationProtocol():

	@staticmethod
	def create_login_msg(login,password):
		body = [login,password]
		msg = {MessageType.LOGIN.value : body}
		msg_json = json.dumps(msg)
		return msg_json

