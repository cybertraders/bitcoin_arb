from tickerlineBTCAUD import get_request as btc_markets_quotes
from bitfinex_basic import get_quotes as bitfinex_quotes
from queuedTicker import Ticker
from forex_python.converter import CurrencyRates
import time

def parse_data(polon_usd,btcm,btfx,usdaud,k):
    k['polon'] = {'btcusd': {'bid':float(polon_usd['highestBid']),'ask':float(polon_usd['lowestAsk'])},
            'btcaud': {'bid':float(polon_usd['highestBid'])*usdaud,'ask':float(polon_usd['lowestAsk'])*usdaud},
            }


    k['btcm'] = {'btcusd':{'bid':float(btcm['bid'])/usdaud,'ask':float(btcm['ask'])/usdaud},
            'btcaud':{'bid':float(btcm['bid']),'ask':float(btcm['ask'])},
            }


    k['btfx'] = {'btcusd':{'bid':float(btfx['bids'][0]['price']),
                        'ask':float(btfx['asks'][0]['price'])},
                'btcaud':{'bid':float(btfx['bids'][0]['price'])/usdaud,
                    'ask':float(btfx['asks'][0]['price'])/usdaud}}
    return k


c = CurrencyRates()
poloniex = Ticker()
k = {}
while True:
    start = time.time()
    btfx = bitfinex_quotes('btcusd')
    btfx_eth = bitfinex_quotes('ethbtc')
    btcm = btc_markets_quotes('BTC','AUD')
    btcm = btc_markets_quotes('ETH','BTC')
    polon = poloniex()
    polon_usd = polon['USDT_BTC']
    polon_eth = polon['BTC_ETH']

    usdaud = c.get_rates('USD')['AUD']
    k = parse_data(polon_usd,btcm,btfx,usdaud,k)

    print k, time.time()-start
