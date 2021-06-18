# Operate with client data.
# Player data is other part

from player.player_data import PlayerData

class ClientData():

    @property
    def uuid(self):
        return self.__uuid

    @property
    def login(self):
        return self.__login

    @property
    def admin(self):
        return self.__admin

    def __init__(self):
        self.__login = ""
        self.__uuid = ""
        self.player_data = None
        self.__admin = False
        # If connection was with error need keep error message
        self.error_message = ""

    # Accept login
    def set_login_informataion(self, login, uuid):
        self.__login = login
        self.__uuid = uuid
        self.player_data = PlayerData(uuid)

    def set_admin_access(self):
        self.__admin = True
