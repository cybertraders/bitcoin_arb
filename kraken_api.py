'''
https://www.kraken.com/help/api
'''
import krakenex

k = krakenex.API()

def kraken_quotes(instr):
    q = k.query_public('Depth',{'pair': instr})
    bids = q['result'][instr]['bids']
    asks = q['result'][instr]['asks']
    return {'bid':float(bids[0][0]),'ask':float(asks[0][0])}

if __name__=="__main__":
    # print k.query_public('OHLC',{'pair': 'XXBTZEUR','interval':1,})
    # print k.query_public('OHLC',{'pair': 'XETHXXBT','interval':1,})
    # print k.query_public('Depth',{'pair': 'XETHXXBT','interval':1,})
    # print k.query_public('AssetPairs')['result'].keys()
    print kraken_quotes('XETHXXBT')
