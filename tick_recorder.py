from data_store import MongoDataStore
from streamer import Streaming
import json

if __name__ == "__main__":
    settings = json.load(open("settings.json"))[0]
    symbol_list = settings['pairs']
    account_id= settings['account']['account_id']
    token = settings['account']['token']
    environment = settings['account']['environment']

    store = MongoDataStore()
    streamer = Streaming(symbol_list,account_id,token,environment,store)

    streamer.stream_prices()

