# Class handle stock information of one company.

class Stock():

	@property
	def uuid(self):
		return self.__uuid

	@property
	def amount(self):
		return self.__amount

	def __init__(self, uuid: str, amount : int):
		self.__uuid = uuid
		self.__amount = amount