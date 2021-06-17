import config
import time
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


