import oandapy
import calendar
from datetime import datetime

class Streaming(oandapy.Streamer):
    def __init__(self,instruments_list,account_id,account_token,account_environment,data_store):
        """

        :param instruments_list:
        :param account:
        :param data_handler:
        :param event_handler:
        :return
        """
        super(Streaming,self).__init__(environment=account_environment,access_token=account_token)
        self.instruments_list = instruments_list
        self.account_id=account_id
        self.data_store = data_store

    def add_instrument(self,instrument):
        # Used by data_handler to add an instrument to instrument_list
        if instrument not in self.instruments_list:
            self.instruments_list.append(instrument)

    def stream_prices(self):
        self.rates(account_id=self.account_id,instruments=str(','.join(self.instruments_list)))


    def on_success(self, data):
        if 'tick' in data:
            time=datetime.strptime(data['tick']['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            params={'instrument':data['tick']['instrument'],
                    'time':time,
                    'bid':data['tick']['bid'],
                    'ask':data['tick']['ask'],
                    'epoch':int(calendar.timegm(time.timetuple()))}


            #Store the tick if data_store attached
            if self.data_store is not None: self.data_store.recordTick(params)



    def on_error(self, data):
        print('Streaming: Error with the feed: %s' %data)