from tickerlineBTCAUD import get_request as btc_markets_quotes
from bitfinex_basic import get_quotes as bitfinex_quotes
from queuedTicker import Ticker
from forex_python.converter import CurrencyRates
import time

def parse_data(quotes,k):
    k['polon'] = {'btcusd':
                {'bid':float(quotes['polon_usd']['highestBid']),
                 'ask':float(quotes['polon_usd']['lowestAsk'])
             },
            'btcaud':
                {'bid':float(quotes['polon_usd']['highestBid'])*quotes['usdaud'],
                 'ask':float(quotes['polon_usd']['lowestAsk'])*quotes['usdaud']
                 },
            }


    k['btcm'] = {'btcusd':
                    {'bid':float(quotes['btcm_aud']['bid'])/quotes['usdaud'],
                     'ask':float(quotes['btcm_aud']['ask'])/quotes['usdaud']
                     },
                'btcaud':
                    {'bid':float(quotes['btcm_aud']['bid']),
                    'ask':float(quotes['btcm_aud']['ask'])
                    },
            }


    k['btfx'] = {'btcusd':
                    {'bid':float(quotes['btfx_usd']['bids'][0]['price']),
                     'ask':float(quotes['btfx_usd']['asks'][0]['price'])
                     },
                'btcaud':
                    {'bid':float(quotes['btfx_usd']['bids'][0]['price'])/quotes['usdaud'],
                    'ask':float(quotes['btfx_usd']['asks'][0]['price'])/quotes['usdaud']
                    }
                }
    return k


poloniex = Ticker()
c = CurrencyRates()
k = {}
quotes = {}
while True:
    polon = poloniex()
    start = time.time()
    quotes['btfx_usd'] = bitfinex_quotes('btcusd')
    quotes['btfx_eth'] = bitfinex_quotes('ethbtc')
    quotes['btcm_aud'] = btc_markets_quotes('BTC','AUD')
    quotes['btcm_eth'] = btc_markets_quotes('ETH','BTC')
    quotes['polon_usd'] = polon['USDT_BTC']
    quotes['polon_eth'] = polon['BTC_ETH']

    quotes['usdaud'] = c.get_rates('USD')['AUD']
    k = parse_data(quotes,k)

    print k, time.time()-start
