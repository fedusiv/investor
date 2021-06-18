import copy
import time

import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.options

from communication_parser import CommunitcationParser
from communication_parser import CommunitcationParserResult
from communication_protocol import MessageType
from communication_protocol import CommunicationProtocol
from client_operation_module import ClientOperation
from message_module import MessagingModule, MessagingParserResult, MessagingTypes
from logic_handler import LogicHandler
from users_dao import UsersDao
from client.clients_handler_callback_type import ClientsHandlerCallbackType
import utils
import config

class ClientHandler(tornado.websocket.WebSocketHandler):

    # Store value, when client was alive last time, if it less than KEEP_ALIVE_TIME, need to send message and check if it is still communicative
    alive_time = 0.0
    # Error count, if it reaches KEEP_ALIVE_ERROR so client is dead and can be disconneceted
    alive_error = 0
    # Store value, when keep_alive message was sent last time
    alive_last_msg_time = 0.0
    # Display if client if logged in to server, server knows who is client, and allow to work with him
    logged_in = False
    # Represent that connected client is admin
    is_admin = False

    @property
    def uuid(self):
        return self.client_data.uuid

    def open(self):
        print("A client connected to server. ", self.request.remote_ip)
        # When connection happen get clientHandlers instance
        self.clients_handler = ClientsHandler.Instance()
        # Get logic handler
        self.logic_handler = LogicHandler.Instance()
        # Create client operations module
        self.client_operation = ClientOperation(self)
        # Get access to users dao
        self.users_dao = UsersDao.Instance()

    # Required this field for web gui
    def check_origin(self, origin):
        utils.unused(origin)
        return True

    def on_close(self):
        print("A client disconnected")
        self.client_handlers.remove_connected_client(self)

    def on_message(self, message):
        # Got message, client alive. Store time for that
        self.alive_time  = time.time()
        self.alive_error = 0
        result : CommunitcationParserResult = CommunitcationParser.parse_clinet_message(message)
        if result.err is False:
            # end execution, wrong message
            return
        # messages related to connection should be proceed here, other need to be sent to separate command executtion module
        if result.result_type == MessageType.KEEP_ALIVE:
            # do nothing. This is just keep alive. Server now knows, that client is alive
            return
        elif result.result_type == MessageType.LOGIN:
            self.on_logged(result)
        # Verification that client is logged in
        elif self.logged_in is True:
            # Verification, that message received form required client. Checking uuid of sender
            if self.client_data.uuid != result.uuid:
                return # If not equal do not go further
            # If messages so handle it here.
            if result.result_type == MessageType.MESSAGING:
                self.messaging_execution(result)
            else:
                # elso go to execution module
                self.command_execution(result)

    def on_logged(self, result: CommunitcationParserResult):
        client_data = self.users_dao.get_user_by_login(result.login, result.password)
        if client_data.uuid != "" :
            self.clients_handler.store_connected_client(self)
            # Client data should be obtain from data base
            self.client_data = copy.deepcopy(client_data) # Copy and create new object of Client data
            # Give to operation module client data
            self.client_operation.client_data = self.client_data
            self.logged_in = True
            # Admin request sent
            if result.admin is True:
                # If client data credentials has admin
                if client_data.admin is True:
                    # Set connection as admin
                    self.is_admin = True
            print("client connected. login : ", self.client_data.login, "\tuuid: " ,self.client_data.uuid, "\t as admin: ", self.is_admin)
        # send message to client
        msg = CommunicationProtocol.create_login_result_msg(self.logged_in,client_data.uuid, msg = client_data.error_message, admin=self.is_admin)
        self.write_message(msg)

    def send_keep_alive(self):
        msg = CommunicationProtocol.create_keep_alive_msg()
        self.write_message(msg)

    def command_execution(self,result_msg : CommunitcationParserResult):
        # Send for further actions for client request
        self.client_operation.parse_command(result_msg)

    def messaging_execution(self, result_msg : CommunitcationParserResult):
        res : MessagingParserResult
        res = MessagingModule.parse_message(result_msg)
        if res.msg_type == MessagingTypes.NONE:
            # Got error in parsing message. Do nothing
            return
        elif res.msg_type == MessagingTypes.GLOBAL:
            sender_name = self.client_data.login
            clients_list = self.clients_handler.list_connected_clients()
            msg_json = CommunicationProtocol.create_global_message(sender_name,
                                                                    self.logic_handler.server_time,
                                                                    res.msg_text)
            for client in clients_list:
                client : ClientHandler
                client.client_operation.ws.write_message(msg_json)

    def send_investment_money(self, debt: float, contract_uuid: str):
        self.client_operation.receive_investment(debt,contract_uuid)

# Singleton to store all handlers
# And manipulate them
class ClientsHandler():
    # Singleton part
    __instance = None

    @staticmethod
    def Instance():
        if ClientsHandler.__instance == None:
            ClientsHandler()
        return ClientsHandler.__instance

    def __init__(self):
        ClientsHandler.__instance = self
        self.logic_handler = LogicHandler.Instance()
        self.logic_handler.set_clients_handler_callback(self.callback_request)

    def callback_request(self, func_id: ClientsHandlerCallbackType, argument):
        switcher = {
            ClientsHandlerCallbackType.SEND_INVEST_MONEY: self.send_investment_money
        }
        func = switcher.get(func_id,self.zero_callback)
        func(argument)

    def zero_callback(self, argument):
        utils.unused(argument)
        pass

    # Functionality part
    __client_storage = []
    def store_connected_client(self, client):
        if client in self.__client_storage:
            # do nothing it's already there
            return
        self.__client_storage.append(client)

    def remove_connected_client(self, client):
        self.__client_storage.remove(client)

    def list_connected_clients(self):
        return self.__client_storage

    # Get to list clients handler
    def get_connected_by_uuid(self, uuid):
        for client in self.__client_storage:
            client : ClientHandler
            if client.uuid == uuid:
                return client
        return None

    # Return the list of clients, that KEEP_ALIVE_TIME did not send any message
    # If error is bigger disconnect
    def list_probably_dead_clients(self):
        silent_clients = []
        for client in self.__client_storage:
            if client.alive_error > config.KEEP_ALIVE_ERROR:
                client.close()
                # disconnect
                continue
            if client.alive_error > 0:
                if time.time() - client.alive_last_msg_time > config.KEEP_ALIVE_TIME:
                    # need to send message of keep_alive. Did not received after previous time
                    client.alive_error +=1
                    silent_clients.append(client)
                continue
            if client.alive_error == 0:
                # check if client keep alive time is not less than KEEP_ALIVE_TIME
                if time.time() - client.alive_time > config.KEEP_ALIVE_TIME:
                    client.alive_error +=1
                    silent_clients.append(client)
        return silent_clients

    def send_investment_money(self, investors_data):
        for item in investors_data:
            client = self.get_connected_by_uuid(item["player_uuid"])
            if client is None:
                continue
            client.send_investment_money(item["debt"], item["contract"])
