from data_store import MongoDataStore
from streamer import Streaming

if __name__ == "__main__":
    symbol_list = ['EUR_USD','AUD_USD']
    account_id = "1947211"
    token="1478277e965621e98bfc1c0beeb94a53-a4ea82586cd6f2710b3bd9725d42010a"
    environment="practice"

    store = MongoDataStore()
    streamer = Streaming(symbol_list,account_id,token,environment,store)

    streamer.stream_prices()

