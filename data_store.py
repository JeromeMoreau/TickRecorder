import pymongo

class MongoDataStore(object):
    def __init__(self, db_name='TICKS', db_adress='localhost'):
        self.database = self._connect_to_mongodb(db_name, db_adress)


    def _connect_to_mongodb(self, db_name, db_adress):
        client = pymongo.MongoClient(db_adress)
        database = client[db_name]
        return database


    def recordTick(self,tick):
        library = self.database['oanda']
        tick = {"time":tick['time'],"pair":tick["instrument"],"bid":tick['bid'],"ask":tick['ask']}
        print(tick)

        library.insert_one(tick)