# Operate with client data.
# Player data is other part

from player.player_data import PlayerData

class ClientData():

	@property
	def password(self):
		return self.__password

	@property
	def uuid(self):
		return self.__uuid

	def __init__(self, login, password, admin: bool = False):
		self.login = login
		self.__password = password
		# TODO: !!! Change it to database functionality
		self.__uuid = "16af-54fg"
		self.player_data = PlayerData()
		self.admin = admin
