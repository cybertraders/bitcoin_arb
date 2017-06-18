from bitstampy import api

def get_quotes():
    q = api.ticker()
    return q

if __name__=="__main__":
    get_quotes()
