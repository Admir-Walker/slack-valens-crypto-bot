from main import client, scheduler
from main.api.cryptocurrency import CryptoCurrency


class AppMentionService():
    @staticmethod
    def latest_listings(**kwargs):
        channel = kwargs['event_data']['event']['channel']
        symbols = ','.join(kwargs['commands'])

        response = CryptoCurrency.latest_listings(symbols)

        if response['status']['error_code'] == 0:
            messages = []
            for symbol in kwargs['commands']:
                coin = response['data'][symbol.upper()]
                coin_name = coin['name']
                usd_quote = coin['quote']['USD']
                price = usd_quote['price']
                percent_change_24h = usd_quote['percent_change_24h']

                messages.append(
                    f'{coin_name} - Price: {price}$, Price change in 24h: {percent_change_24h}%.')

            client.chat_postMessage(channel=channel, text="\n".join(messages))
        else:
            client.chat_postMessage(
                channel=channel, text=response['status']['error_message'])

    @staticmethod
    # hh:mm space-separated-crypto-symbols
    def schedule(**kwargs):
        hours, minutes = kwargs['commands'][0].split(":")
        minutes = int(hours)*60 + int(minutes)
        # space-separated-crypto-symbols
        kwargs['commands'] = kwargs['commands'][1:]
        channel = kwargs['event_data']['event']['channel']
        job_id = f'{channel}-scheduler'
        scheduler.add_job(AppMentionService.latest_listings, kwargs=kwargs,
                          trigger='interval', minutes=minutes, id=job_id, replace_existing=True)

    @staticmethod
    def help(**kwargs):
        channel = kwargs['event_data']['event']['channel']

        messages = [
            "To get list of the available commands - `@bot_name help`",
            "To get current prices of specific cryptocurrencies - `@bot_name space-separated-crypto-symbols`"
        ]

        client.chat_postMessage(channel=channel, text="\n".join(messages))
