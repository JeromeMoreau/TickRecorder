import pymongo


class MongoDataStore(object):
    def __init__(self, db_name='TICKS', db_adress='localhost'):
        """
        Save the ticks data to MongoDB

        :param db_name: name of the database in MongoDB
        :param db_adress: adress of your mongoDB instance
        """
        self.database = self._connect_to_mongodb(db_name, db_adress)


    def _connect_to_mongodb(self, db_name, db_adress):
        """

        :param db_name: name of the database in MongoDB
        :param db_adress: adress of your mongoDB instance
        :return: database's connection
        """
        client = pymongo.MongoClient(db_adress)
        database = client[db_name]
        return database


    def recordTick(self,tick):
        """
        Insert the tick data into th database
        :param tick: dict containing at least: (time,pair,bid,ask) data
        """
        library = self.database['oanda']
        tick = {"time": tick['time'], "pair": tick["instrument"], "bid": tick['bid'], "ask": tick['ask']}
        print(tick)

        try:
            library.insert_one(tick)
        except pymongo.errors.DuplicateKeyError:
            print("duplicate record: ",tick)

