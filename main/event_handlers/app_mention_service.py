from main import client, scheduler
from main.api.cryptocurrency import CryptoCurrency


class AppMentionService():
    @staticmethod
    def latest_listings(**kwargs):
        try:
            channel = AppMentionService.get_channel(**kwargs)
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

                client.chat_postMessage(
                    channel=channel, text="\n".join(messages))
            else:
                client.chat_postMessage(
                    channel=channel, text=response['status']['error_message'])
        except:
            client.chat_postMessage(
                channel=AppMentionService.get_channel(**kwargs), text="Something went wrong, please try again.")

    @staticmethod
    # hh:mm space-separated-crypto-symbols
    def schedule(**kwargs):
        try:
            hours, minutes = kwargs['commands'][0].split(":")
            hours = int(hours) if hours.strip() != '' else 0
            minutes = int(minutes) if minutes.strip() != '' else 0

            # space-separated-crypto-symbols
            kwargs['commands'] = kwargs['commands'][1:]
            symbols = ','.join(kwargs['commands'])
            response = CryptoCurrency.latest_listings(symbols)
            if response['status']['error_code'] != 0:
                client.chat_postMessage(channel=AppMentionService.get_channel(
                    **kwargs), text=response['status']['error_message'])
            else:
                job_id = AppMentionService.get_job_id(**kwargs)

                scheduler.add_job(AppMentionService.latest_listings, kwargs=kwargs,
                                  trigger='interval', minutes=hours*60 + minutes, id=job_id, replace_existing=True)

                AppMentionService.post_schedule_message(
                    hours, minutes, **kwargs)
        except:
            client.chat_postMessage(
                channel=AppMentionService.get_channel(**kwargs), text="Something went wrong, please try again.")

    @staticmethod
    def post_schedule_message(hours, minutes, **kwargs):
        channel = AppMentionService.get_channel(**kwargs)

        cryptocurrency_message = " ".join(kwargs['commands'])

        interval_message = f"{hours}h" if hours > 0 else ""
        interval_message += ":" if hours > 0 and minutes > 0 else ""
        interval_message += f"{minutes}m" if minutes > 0 else ""

        client.chat_postMessage(
            channel=channel, text=f"You successfully added interval scheduler. \n Cryptocurrencies: {cryptocurrency_message}. \n Interval: {interval_message}")

    @staticmethod
    def schedule_remove(**kwargs):
        try:
            job_id = AppMentionService.get_job_id(**kwargs)
            scheduler.remove_job(job_id)
            channel = AppMentionService.get_channel(**kwargs)
            client.chat_postMessage(
                channel=channel, text="You successfully removed interval scheduler.")
        except:
            client.chat_postMessage(
                channel=AppMentionService.get_channel(**kwargs), text="Something went wrong, please try again.")

    @staticmethod
    def get_job_id(**kwargs):
        channel = AppMentionService.get_channel(**kwargs)
        job_id = f'{channel}-scheduler'
        return job_id

    @staticmethod
    def get_channel(**kwargs):
        return kwargs['event_data']['event']['channel']

    @staticmethod
    def help(**kwargs):
        try:

            channel = AppMentionService.get_channel(**kwargs)

            messages = [
                "To get list of the available commands - `@bot_name help`",
                "To get current prices of specific cryptocurrencies - `@bot_name space-separated-crypto-symbols`",
                "To get prices of specific cryptocurrencies at interval - `@bot_name schedule hh:mm space-separated-crypto-symbols`",
                "To remove schedule - `@bot_name schedule_remove`",
            ]

            client.chat_postMessage(channel=channel, text="\n".join(messages))
        except:
            client.chat_postMessage(
                channel=AppMentionService.get_channel(**kwargs), text="Something went wrong, please try again.")
