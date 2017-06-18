from tickerlineBTCAUD import get_request as btc_markets_quotes
from bitfinex_basic import get_quotes as bitfinex_quotes
from queuedTicker import Ticker
from forex_python.converter import CurrencyRates
import time

poloniex = Ticker()
curr = CurrencyRates()


def parse_data(quotes,k):
    k['poloniex'] = {'btcusd':
                    {'bid':float(quotes['polon_usd']['highestBid']),
                    'ask':float(quotes['polon_usd']['lowestAsk'])
                    },
                'btcaud':
                    {'bid':float(quotes['polon_usd']['highestBid'])*quotes['usdaud'],
                    'ask':float(quotes['polon_usd']['lowestAsk'])*quotes['usdaud']
                    },
                'btceth':
                    {'bid':float(quotes['polon_eth']['highestBid']),
                    'ask':float(quotes['polon_eth']['lowestAsk'])
                    },
            }


    k['btcmarkets'] = {'btcusd':
                    {'bid':float(quotes['btcm_aud']['bid'])/quotes['usdaud'],
                     'ask':float(quotes['btcm_aud']['ask'])/quotes['usdaud']
                     },
                'btcaud':
                    {'bid':float(quotes['btcm_aud']['bid']),
                    'ask':float(quotes['btcm_aud']['ask'])
                    },
                'btceth':
                    {'bid':float(quotes['btcm_eth']['bid']),
                    'ask':float(quotes['btcm_eth']['ask'])
                    },
            }


    k['bitfinex'] = {'btcusd':
                    {'bid':float(quotes['btfx_usd']['bids'][0]['price']),
                     'ask':float(quotes['btfx_usd']['asks'][0]['price'])
                     },
                'btcaud':
                    {'bid':float(quotes['btfx_usd']['bids'][0]['price'])/quotes['usdaud'],
                    'ask':float(quotes['btfx_usd']['asks'][0]['price'])/quotes['usdaud']
                    },
                'btceth':
                    {'bid':float(quotes['btfx_eth']['bids'][0]['price']),
                     'ask':float(quotes['btfx_eth']['asks'][0]['price'])
                     },
                }
    return k


def get_all_quotes(quotes):
    polon = poloniex()
    try: quotes['btfx_usd'] = bitfinex_quotes('btcusd')
    except: pass

    try: quotes['btfx_eth'] = bitfinex_quotes('ethbtc')
    except: pass

    try: quotes['btcm_aud'] = btc_markets_quotes('BTC','AUD')
    except: pass

    try: quotes['btcm_eth'] = btc_markets_quotes('ETH','BTC')
    except: pass

    try: quotes['polon_usd'] = polon['USDT_BTC']
    except: pass

    try: quotes['polon_eth'] = polon['BTC_ETH']
    except: pass

    try: quotes['usdaud'] = curr.get_rates('USD')['AUD']
    except: pass

    return quotes

def run():
    k = {}
    quotes = {}
    while True:
        start = time.time()
        quotes = get_all_quotes(quotes)
        k = parse_data(quotes,k)

        print k, time.time()-start

if __name__=="__main__":
    run()
