import uuid
from decimal import Decimal
import boto3
from client.client_data import ClientData
from communication_protocol import MessageType

# User Data Access Object
class UsersDao:

    __instance = None

    @staticmethod
    def Instance():
        if UsersDao.__instance is None:
            UsersDao()
        return UsersDao.__instance

    def __init__(self):
        UsersDao.__instance = self
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('users')

    def add_user(self, credentials):
        self.table.put_item(
            Item={
                'login': credentials["body"]["login"],
                'password': credentials["body"]["password"]
            }
        )
        return ClientData()

    def get_user_by_login(self, login : str, password):
        table_credentials = self.table.get_item(
            Key={
                'login': login
            }
        )
        client_data = ClientData()
        try:
            if table_credentials["Item"]["password"] == password:
                uuid = table_credentials["Item"]["uuid"]
                client_data.set_login_informataion(login,uuid)
                # Checks if admin tryingto connect to server
                if table_credentials["Item"]["admin"] == True:
                    client_data.set_admin_access()
            else:
                client_data.error_message = "Wrong credentials"
        except:
            client_data.error_message = "No such user"

        return client_data


