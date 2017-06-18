from bitfinex.client import Client

client = Client()

def get_quotes(symbol):
    # symbols = client.symbols()
    # print(symbols)

    # symbol = 'btcusd'

    # print(client.ticker(symbol))
    # print(client.today(symbol))
    # print(client.stats(symbol))

    parameters = {'limit_asks': 1, 'limit_bids': 1}

    # print(client.lendbook('btc', parameters))
    return (client.order_book(symbol, parameters))

def run():
    while True:
        print get_quotes('btcusd')

if __name__=="__main__":
    run()
