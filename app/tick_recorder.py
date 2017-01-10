import json
import threading
import os

from app.data_store import MongoDataStore
from app.streamer import Streaming
import cherrypy


class TickRecorder(object):
    def __init__(self):
        self.settings = json.load(open("./app/settings.json"))[0]
        self.symbol_list = self.settings['pairs']
        self.account_id = self.settings['account']['account_id']
        self.token = self.settings['account']['token']
        self.environment = self.settings['account']['environment']
        #self.store = MongoDataStore(db_adress=os.environ['DB_PORT_27017_TCP_ADDR'],db_port=27017,db_name='TICKS')
        self.store = MongoDataStore(db_adress='mongo', db_port=27017, db_name='TICKS')

        self.streamer = Streaming(self.symbol_list,self.account_id,self.token,self.environment,self.store)
        self.thread = threading.Thread(target=self.streamer.stream_prices, args=[])

    @cherrypy.expose
    def start(self):
        self.thread.start()
        raise cherrypy.HTTPRedirect("/")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def is_alive(self):
        return self.thread.is_alive()

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def setkeys(self):
        accountId = cherrypy.request.json['account_id']
        token = cherrypy.request.json['token']

        self.settings['account']['account_id'] = accountId
        self.settings['account']['token'] = token

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getkeys(self):
        dict = {'account_id':self.settings['account']['account_id'], 'token':self.settings['account']['token']}
        return dict

