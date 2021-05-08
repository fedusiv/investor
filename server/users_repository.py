import uuid
from decimal import Decimal

import boto3

from client_data import ClientData

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

class UsersRepository:

    @staticmethod
    def add_user(credentials):
        print(uuid.uuid4().int)
        table.put_item(
            Item={
                'id': Decimal(uuid.uuid4().int % 1e6),
                'login': credentials["body"]["login"],
                'password': credentials["body"]["password"]
            }
        )
        return ClientData(credentials["body"]["login"], credentials["body"]["password"])

    @staticmethod
    def get_user_by_login(credentials):
        password = table.get_item(
            Key={
                'login': credentials["body"]["login"]
            }
        )
        if password == credentials["body"]["password"]:
            return ClientData(credentials["body"]["login"], credentials["body"]["password"])
        else:
            raise Exception()




