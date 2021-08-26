from main.api import coin_market_requestor


class CryptoCurrency:
    @staticmethod
    def latest_listings(symbols):
        params = {'symbol': symbols}
        return coin_market_requestor.get('cryptocurrency/quotes/latest', params=params)
