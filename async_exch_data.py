from tickerlineBTCAUD import get_request as btc_markets_quotes
from bitfinex_basic import get_quotes as bitfinex_quotes
from queuedTicker import Ticker
from forex_python.converter import CurrencyRates
from bitstamp_api import get_quotes as bitstamp
from kraken_api import kraken_quotes
import time
import traceback
from threading import Thread
import Queue
import cPickle
from pylab import *

curr = CurrencyRates()


def parse_data(q,k):
    usdaud = curr.get_rates('USD')['AUD']
    ion()
    while True:
        try: quotes = q.get_nowait()
        except:
            break
        key = quotes.keys()[0]
        if not key in k:
            k[key] = {}
        if not quotes[key].keys()[0] in k[key]:
            k[key][quotes[key].keys()[0]] = {}
        secondary_key = quotes[key].keys()[0]
        if key=='poloniex':
            k[key][secondary_key]['ask'] = quotes[key][secondary_key]['lowestAsk']
            k[key][secondary_key]['bid'] = quotes[key][secondary_key]['highestBid']
        else:
            k[key][secondary_key]['ask'] = quotes[key][secondary_key]['ask']
            k[key][secondary_key]['bid'] = quotes[key][secondary_key]['bid']
        try: print '--->', quotes[key][secondary_key]['ask'],key
        except: print 'error',quotes,key
        # cPickle.dump(quotes,open('/home/tom/data/bitarb.pick','w'))
        try:
            clf()
            if 'polon_eth' in k['poloniex']:
                plot([1.9,1.9],[k['poloniex']['polon_eth']['bid'],k['poloniex']['polon_eth']['ask']],'-',lw = 65,label='polon')
                polon_last = [k['poloniex']['polon_eth']['bid'],k['poloniex']['polon_eth']['ask']]
                xlim([1.5,2.5])
            else: plot([1.9,1.9],polon_last,'-',lw = 65,label='polon')
            if 'btcm_eth' in k['btcmarkets']:
                plot([2,2],[k['btcmarkets']['btcm_eth']['bid'],k['btcmarkets']['btcm_eth']['ask']],'-',lw = 65,label='btcm')
                btcm_last = [k['btcmarkets']['btcm_eth']['bid'],k['btcmarkets']['btcm_eth']['ask']]
            else: plot([2,2],btcm_last,'-',lw = 65,label='btcm')
            if 'btfx_eth' in k['bitfinex']:
                plot([2.1,2.1],[k['bitfinex']['btfx_eth']['bid'],k['bitfinex']['btfx_eth']['ask']],'-',lw = 65,label='btfx')
                btfx_last = [k['bitfinex']['btfx_eth']['bid'],k['bitfinex']['btfx_eth']['ask']]
            else: plot([2.1,2.1],btfx_last,'-',lw = 65,label='btfx')
            if 'kraken_eth' in k['kraken']:
                plot([2.2,2.2],[k['kraken']['kraken_eth']['bid'],k['kraken']['kraken_eth']['ask']],'-',lw = 65,label='kraken')
                kraken_last = [k['kraken']['kraken_eth']['bid'],k['kraken']['kraken_eth']['ask']]
            else: plot([2.2,2.2],kraken_last,'-',lw = 65,label='kraken')
            # legend(loc='best')
            draw()
            pause(0.1)
        except: print traceback.format_exc()

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

        def a8(q):
            self.num_threads += 1
            q.put({'kraken':{'kraken_eth':kraken_quotes('XETHXXBT')}})

        t = []
        for func in [a1,a2,a3,a4,a5,a6,a7,a8]:
            t.append(Thread(target=func,args=(q,)))
            t[-1].start()

        max_iter = 100000
        iterator = 0
        while self.num_threads < 8 and iterator < max_iter:
            iterator += 1
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
