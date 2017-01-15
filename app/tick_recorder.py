import json
import threading

from app.data_store import MongoDataStore
from app.streamer import Streaming
import oandapy


class TickRecorder(object):
    def __init__(self):
        self.settings = json.load(open("./app/settings.json"))[0]
        self.symbol_list = self.settings['pairs']
        self.account_id = self.settings['account']['account_id']
        self.token = self.settings['account']['token']
        self.environment = self.settings['account']['environment']
        self.store = MongoDataStore(db_adress='mongo', db_port=27017, db_name='TICKS')

        self.streamer = Streaming(self.symbol_list,self.account_id,self.token,self.environment,self.store)
        self.thread = threading.Thread(target=self.streamer.stream_prices, args=[])
        self.symbols = None

    def start(self):
        """
        Start the streaming
        :return: boolean: thread status
        """
        self.thread.start()
        return self.is_alive()


    def is_alive(self):
        """
        Method to check if the streaming is on
        :return: boolean: thread status
        """
        return self.thread.is_alive()


    def set_default_keys(self, accountId, token):
        """
        Method to modify Oanda access keys
        :param accountId:
        :param token:
        :return:
        """
        self.settings['account']['account_id'] = accountId
        self.settings['account']['token'] = token
        self.account_id = accountId
        self.token = token


    def getkeys(self):
        """

        :return: dictionnary whith account_id,token
        """
        dict = {'account_id':self.settings['account']['account_id'], 'token':self.settings['account']['token']}
        return dict


    def available_symbols(self):
        """
        Get every symbols available for streaming by the broker
        :return: list of symbols
        """
        if self.symbols is None:
            oanda = oandapy.API(environment=self.environment,access_token=self.token)
            symbols = oanda.get_instruments(account_id=self.account_id).get('instruments')
            return [symbol['instrument'] for symbol in list(symbols)]
        else:
            return self.symbols

    def change_traded_symbols(self,traded_symbols):
        #TODO: implement this method
        if not self.is_alive():
            self.symbol_list = traded_symbols
            return True
        else:
            print('Could not yet change traded symbols while the server is running: stop it first')
            return False

