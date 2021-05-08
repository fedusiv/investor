import uuid
from decimal import Decimal
import boto3
from client_data import ClientData
from communication_protocol import MessageType


class UsersDao:

    __instance = None

    @staticmethod
    def instance():
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
        return ClientData(credentials["body"]["login"], credentials["body"]["password"])

    def get_user_by_login(self, credentials):
        table_credentials = self.table.get_item(
            Key={
                'login': credentials["body"]["login"]
            }
        )
        if table_credentials["Item"]["password"] == credentials["body"]["password"]:
            return ClientData(credentials["body"]["login"], credentials["body"]["password"])
        else:
            return MessageType.NONE
