import time

class TimeModule():
    # Singleton part
    __instance = None
    @staticmethod

    def Instance():
        if TimeModule.__instance == None:
            TimeModule()
        return TimeModule.__instance

    def __init__(self):
        TimeModule.__instance = self
        self.__server_time = 0
        self.__server_world_time = 0
        self.__server_start_time = 0

    #---------------------#
    #Properties part
    #---------------------#
    # Return value, that
    @property
    def server_time(self):
        return self.__server_time

    @property
    def server_world_time(self):
        return self.__server_world_time

    #---------------------#
    #Logic part
    #---------------------#

    # Fucntion mark the moment when it's called as start of server working time
    def start_mark(self):
        self.__server_start_time = 0
        self.__server_world_time = time.time()

    # Tick operation
    def tick(self):
        cur_time = time.time()
        self.__server_world_time = cur_time
        self.__server_time = cur_time - self.__server_start_time
