import os
import requests

from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


class CoinMarketRequestor:
    base_url = 'https://pro-api.coinmarketcap.com'
    version = 'v1'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': os.environ.get('COIN_MARKET_API_KEY'),
    }

    def make_url(self, **kwargs):
        path = kwargs['path'] if kwargs.get('path') else ''
        return f'{self.base_url}/{self.version}/{path}'

    def get(self, path, **kwargs):
        try:
            url = self.make_url(path=path)
            r = requests.get(url, headers=self.headers, **kwargs)
            return r.json()
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
