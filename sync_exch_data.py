from tickerlineBTCAUD import get_request as btc_markets_quotes
from bitfinex_basic import get_quotes as bitfinex_quotes
from queuedTicker import Ticker
from forex_python.converter import CurrencyRates
from bitstamp_api import get_quotes as bitstamp
import time

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

    k['bitstamp'] = {'btcusd':
                    {'bid':float(quotes['bstmp_usd']['bid']),
                     'ask':float(quotes['bstmp_usd']['ask'])
                     },
                'btcaud':
                    {'bid':float(quotes['bstmp_usd']['bid'])*quotes['usdaud'],
                    'ask':float(quotes['bstmp_usd']['ask'])*quotes['usdaud']
                    },
                }
    return k


def get_all_quotes(quotes):
    polon = Ticker()
    quotes['btfx_usd'] = bitfinex_quotes('btcusd')
    quotes['btfx_eth'] = bitfinex_quotes('ethbtc')
    quotes['btcm_aud'] = btc_markets_quotes('BTC','AUD')
    quotes['btcm_eth'] = btc_markets_quotes('ETH','BTC')
    quotes['polon_usd'] = polon()['USDT_BTC']
    quotes['polon_eth'] = polon()['BTC_ETH']
    quotes['bstmp_usd'] = bitstamp()
    quotes['usdaud'] = curr.get_rates('USD')['AUD']
    return quotes

def run():
    k = {}
    quotes = {}
    while True:
        start = time.time()
        quotes = get_all_quotes(quotes)
        k = parse_data(quotes,k)

        print k['poloniex'], time.time()-start

if __name__=="__main__":
    run()
