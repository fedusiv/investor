import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time
import copy

import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.options
from tornado import gen

from clients_handler import ClientsHandler
from communication_parser import CommunitcationParser
from communication_parser import CommunitcationParserResult
from communication_protocol import MessageType
from communication_protocol import CommunicationProtocol
from logic_handler import LogicHandler
from client_operation_module import ClientOperation
from users_dao import UsersDao
from message_module import MessagingModule, MessagingParserResult, MessagingTypes
import utils
import config


class Server(tornado.web.Application):

    def __init__(self, io_loop):
        handlers = [(r"/", ClientHandler)]
        settings = dict(debug=True)
        tornado.web.Application.__init__(self, handlers, **settings)
        self.clients = ClientsHandler.Instance()
        self.io_loop = io_loop
        # Rise invinite loop for keep alive checker
        self.io_loop.spawn_callback(self.keep_alive_loop)

        # Init data base
        self.users_dao = UsersDao.Instance()

        # Logic part
        self.logic_handler = LogicHandler.Instance()
        self.io_loop.spawn_callback(self.logic_handler.logic_loop)


    # go through all clients to check if need to send keep alive
    # each defined time in gen.sleep, it goes through all clients required to keep alive
    async def keep_alive_loop(self):
        while True:
            silent_clients = self.clients.list_probably_dead_clients()
            if silent_clients != None:
                for client in silent_clients:
                    client.send_keep_alive()
                    client.alive_last_msg_time = time.time()
            await gen.sleep(0.1)


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

    def open(self):
        print("A client connected to server. ", self.request.remote_ip)
        # When connection happen get clientHandlers instance
        self.client_handlers = ClientsHandler.Instance()
        # Get logic handler
        self.logic_handler = LogicHandler.Instance()
        # Create client operations module
        self.client_operation = ClientOperation(self, self.logic_handler)
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
            self.client_handlers.store_connected_client(self)
            # Client data should be obtain from data base
            self.client_data = copy.deepcopy(client_data)	# Copy and create new object of Client data
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
            clients_list = self.client_handlers.list_connected_clients()
            msg_json = CommunicationProtocol.create_global_message(sender_name,
                                                                    self.logic_handler.server_time,
                                                                    res.msg_text)
            for client in clients_list:
                client : ClientHandler
                client.client_operation.ws.write_message(msg_json)

def ServerStart():
    io_loop_instance = tornado.ioloop.IOLoop.current()
    server = Server(io_loop_instance)
    server.listen(config.PORT)

    # After this line nothing will act, because it starts infinite priority loop
    print("Server is starting")
    io_loop_instance.start()


