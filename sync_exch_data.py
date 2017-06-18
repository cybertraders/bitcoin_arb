from tickerlineBTCAUD import get_request as btc_markets_quotes
from bitfinex_basic import get_quotes as bitfinex_quotes
from queuedTicker import Ticker
from forex_python.converter import CurrencyRates
from bitstamp_api import get_quotes as bitstamp
import time
import traceback
from threading import Thread
import Queue

curr = CurrencyRates()


def parse_data(q,k):
    for i in range(7):
        quotes = q.get()
        key = quotes.keys()[0]
        if not key in k:
            k[key] = {}
        if not quotes[key].keys()[0] in k[key]:
            k[key][quotes[key].keys()[0]] = {}
        secondary_key = quotes[key].keys()[0]
        if key=='poloniex':
            quotes[key][secondary_key]['ask'] = quotes[key][secondary_key]['lowestAsk']
            quotes[key][secondary_key]['bid'] = quotes[key][secondary_key]['highestBid']
        try: print '--->', quotes[key][secondary_key]['ask'],key
        except: print 'error',quotes,key


    return k

class Quotes:
    def get_all_quotes(self,quotes):
        polon = Ticker()
        q = Queue.Queue()
        self.num_threads = 0

        def a1(q):
            self.num_threads += 1
            q.put({'bitfinex':{'btfx_usd':bitfinex_quotes('btcusd')}})

        def a2(q):
            self.num_threads += 1
            q.put({'bitfinex':{'btfx_eth':bitfinex_quotes('ethbtc')}})

        def a3(q):
            self.num_threads += 1
            q.put({'btcmarkets':{'btcm_aud':btc_markets_quotes('BTC','AUD')}})

        def a4(q):
            self.num_threads += 1
            q.put({'btcmarkets':{'btcm_eth':btc_markets_quotes('ETH','BTC')}})

        def a5(q):
            self.num_threads += 1
            q.put({'poloniex':{'polon_usd':polon()['USDT_BTC']}})

        def a6(q):
            self.num_threads += 1
            q.put({'poloniex':{'polon_eth':polon()['BTC_ETH']}})

        def a7(q):
            self.num_threads += 1
            q.put({'bitstamp':{'bstmp_usd':bitstamp()}})

        # def a8(q):
            # self.num_threads += 1
            # q.put({'USDAUD':{'usdaud':curr.get_rates('USD')['AUD']}})

        for func in [a1,a2,a3,a4,a5,a6,a7]:
            t = Thread(target=func,args=(q,))
            t.start()

        while self.num_threads < 7:
            pass

        return q

def run():
    k = {}
    quotes = {}
    get_q = Quotes()
    while True:
        start = time.time()
        quotes = get_q.get_all_quotes(quotes)
        k = parse_data(quotes,k)

        # print k#['poloniex']
        # print 'Download time:',time.time()-start

if __name__=="__main__":
    run()
