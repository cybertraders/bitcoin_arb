'''
https://www.kraken.com/help/api
'''
import krakenex


k = krakenex.API()
# print k.query_public('OHLC',{'pair': 'XXBTZEUR','interval':1,})
print k.query_public('OHLC',{'pair': 'XETHXXBT','interval':1,})
# print k.query_public('AssetPairs')['result'].keys()
