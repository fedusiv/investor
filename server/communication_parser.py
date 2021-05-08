from client_data import ClientData
from communication_protocol import CommunicationProtocol
from communication_protocol import MessageType
from users_repository import UsersRepository


class CommunitcationParserResult():

	result_type : MessageType

	def __init__ (self, result_type = MessageType.NONE, success = True):
		self.err = success
		self.result_type = result_type

	# For initialization client data
	# On login request it should store credentials, for futher parsing and validating
	def init_client_data(self, msg):
		switcher = {
			MessageType.LOGIN.value: UsersRepository.add_user,
			MessageType.REGISTRATION.value: UsersRepository.get_user_by_login,
		}

		action = switcher.get(int(msg["type"]))
		try:
			self.client_data = action(msg)
			return self
		except Exception:
			print("wrong password")




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
		result = CommunitcationParserResult(MessageType.REGISTRATION)
		result.init_client_data(msg)
		return result

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
			MessageType.KEEP_ALIVE.value : CommunitcationParser.keep_alive_respond,
			MessageType.COMPANIES_LIST_ALL.value : CommunitcationParser.companies_all_list_request
		}

		func = switcher.get(int(msg["type"]))
		result = func(msg)
		return result

