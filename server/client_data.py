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
        self.__uuid = ""
        self.player_data = PlayerData()
        self.admin = admin


    def set_uuid(self,uuid:str):
        self.__uuid = uuid
