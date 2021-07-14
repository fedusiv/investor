import sqlalchemy as sqla
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy.orm import session, sessionmaker

import config

base = declarative_base()
class ClientData(base):
    __tablename__ = 'client_data'

    login = Column(String, primary_key=True)
    password = Column(String)

#Session = sessionmaker(db)  
#session = Session()
#
## Create
#doctor_strange = ClientData(login="Doctor2", password="Scott Derrickson")
#session.add(doctor_strange)
#session.commit()
##


#films = session.query(ClientData)
#for film in films:
#    print(film.login)
#

class DataBase():
    __instance = None

    @staticmethod
    def Instance():
        if DataBase.__instance == None:
            DataBase()
        return DataBase.__instance

    def __init__(self):
        DataBase.__instance = self
        # Initilize access to database
        self.db = sqla.create_engine(config.DATABASE_LINK)
        curSession = sessionmaker(self.db)
        self.session = curSession()
        users = self.session.query(ClientData)
        for user in users:
            print(user.login)

    def login_user(self, login: str):
        obj = self.session.query(ClientData).get(login)
        print(obj.password)
